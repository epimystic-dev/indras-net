# SPDX-License-Identifier: Apache-2.0
"""Role/persona-lite agents: functional agents propose one envelope; governance personas wrap their authority."""

from __future__ import annotations

import abc
import time
import typing

from . import canon
from .audit import AkashaSutra, ActionClassLedger, AuditLeaf
from .envelope import (
    ActionClass,
    ActionRequest,
    AhankaraCheck,
    CausalRung,
    Evidence,
    Finding,
    HonestyBlock,
    EnvelopeKind,
    Provenance,
    ReasoningTag,
    Scope,
    Status,
    TrustLabel,
    WorkerOutputEnvelope,
)
from .effects import EFFECT_REGISTRY
from .identity import Identity
from .model import ModelAdapter, ModelResult

SCHEMA_VERSION: str = "1.0.0"
POLICY_VERSION: str = "1.0.0"


class AgentError(Exception):
    """Raised on malformed agent construction or an impossible deliberation request."""


def _reasoning_tag_from(raw: str) -> ReasoningTag:
    """Map a model's free-string reasoning tag onto the enum, defaulting to NORMAL."""
    table = {
        "normal": ReasoningTag.NORMAL,
        "reasoning": ReasoningTag.REASONING,
        "iterated": ReasoningTag.ITERATED,
        "reasoning,iterated": ReasoningTag.REASONING_ITERATED,
    }
    return table.get((raw or "").strip().lower(), ReasoningTag.NORMAL)


def _causal_rung_from(raw: int) -> CausalRung:
    """Map a model's integer rung self-tag onto the enum, defaulting to RUNG1."""
    try:
        return CausalRung(int(raw))
    except (ValueError, TypeError):
        return CausalRung.RUNG1


def _now_iso() -> str:
    """RFC-3339-ish UTC timestamp; producer-asserted, never the ledger ordering authority."""
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


class Agent(abc.ABC):
    """Abstract functional agent. Deliberates via an UNTRUSTED ModelAdapter; emits ONE sealed envelope.

    An agent never touches a tool socket. It only PROPOSES: it builds a
    WorkerOutputEnvelope, fills the honesty block from the model's self-report,
    seals it (content-address + this_hash), and returns it. Whether anything is
    permitted to run is decided OUTSIDE the agent, at the Yama floor.
    """

    identity: Identity
    model: ModelAdapter

    @abc.abstractmethod
    def act(self, task: str, context: dict, *, scope: Scope) -> WorkerOutputEnvelope:
        """Build, seal, and return exactly one envelope for ``task`` under ``scope``."""
        raise NotImplementedError

    # -- shared envelope construction ------------------------------------

    def _base_honesty(
        self,
        result: ModelResult,
        *,
        action_class: ActionClass,
        over_assertion_risk: str = "low",
    ) -> HonestyBlock:
        """Assemble the honesty/provenance block from the model's LOW-TRUST self-report."""
        return HonestyBlock(
            reasoning_tag=_reasoning_tag_from(result.reasoning_tag),
            causal_rung=_causal_rung_from(result.causal_rung),
            trust_label=TrustLabel.TRUSTED_AUDITED,
            action_class=action_class,
            ahankara_check=AhankaraCheck(
                ego_invested=False,
                over_assertion_risk=over_assertion_risk,
                attachment_targets=(),
                note="",
            ),
        )

    def _new_envelope(
        self,
        *,
        kind: EnvelopeKind,
        status: Status,
        summary: str,
        honesty: HonestyBlock,
        scope: Scope,
        result: ModelResult,
        action: ActionRequest | None = None,
        findings: tuple[Finding, ...] = (),
        evidence: tuple[Evidence, ...] = (),
    ) -> WorkerOutputEnvelope:
        """Construct a sealed WorkerOutputEnvelope bound to this agent's identity + adapter."""
        env = WorkerOutputEnvelope(
            schema_version=SCHEMA_VERSION,
            envelope_kind=kind,
            agent_did=self.identity.did,
            agent_role=self.identity.role,
            status=status,
            summary=summary,
            honesty=honesty,
            scope=scope,
            provenance=Provenance(policy_version=POLICY_VERSION),
            ts=_now_iso(),
            model_adapter_id=result.adapter_id,
            trust_class=result.trust_class.name.lower(),
            action=action,
            findings=findings,
            evidence=evidence,
        )
        return env.seal()


class BrahmaPlanner(Agent):
    """Planner / decomposer (Brahma): turns a request into typed sub-tasks and emits an OUTPUT envelope."""

    def __init__(self, identity: Identity, model: ModelAdapter) -> None:
        if identity is None or model is None:
            raise AgentError("BrahmaPlanner requires an identity and a model adapter")
        self.identity = identity
        self.model = model

    def plan(self, task: str, context: dict) -> tuple[dict, ...]:
        """Decompose ``task`` into typed sub-tasks: each {effect_id, args, risk_class}.

        Deterministic and transparent: the planner consults the untrusted model
        once to seed the lead sub-task, then derives a small typed plan. Risk
        classes are advisory hints; the floor recomputes authority.
        """
        lead = self.model.complete(task, context)
        subtasks: list[dict] = []
        if lead.proposed_effect_id is not None:
            subtasks.append(
                {
                    "effect_id": lead.proposed_effect_id,
                    "args": dict(lead.proposed_args),
                    "risk_class": "A",
                }
            )
        # Always include a routine analysis step so an empty model proposal still yields work.
        if not subtasks:
            subtasks.append(
                {
                    "effect_id": "analysis.summarize",
                    "args": {"text_ref": "ctx:" + (task[:24] or "empty")},
                    "risk_class": "A",
                }
            )
        return tuple(subtasks)

    def act(self, task: str, context: dict, *, scope: Scope) -> WorkerOutputEnvelope:
        """Emit the plan envelope: a plan summary plus one typed-sub-task finding each."""
        result = self.model.complete(task, context)
        subtasks = self.plan(task, context)
        findings = tuple(
            Finding(
                claim="sub-task: " + st["effect_id"] + " (risk " + st["risk_class"] + ")",
                claim_level="belief",
                evidence_ref=None,
                trust_label=TrustLabel.TRUSTED_AUDITED,
                severity="info",
            )
            for st in subtasks
        )
        honesty = self._base_honesty(result, action_class=ActionClass.OCCASIONED)
        summary = "plan: " + str(len(subtasks)) + " typed sub-task(s) for: " + (task[:64] or "(empty)")
        return self._new_envelope(
            kind=EnvelopeKind.OUTPUT,
            status=Status.PASS,
            summary=summary,
            honesty=honesty,
            scope=scope,
            result=result,
            findings=findings,
        )


class VishwakarmaBuilder(Agent):
    """Builder / worker (Vishwakarma): proposes a typed effect via the model; this REQUEST is gated by Yama."""

    def __init__(self, identity: Identity, model: ModelAdapter) -> None:
        if identity is None or model is None:
            raise AgentError("VishwakarmaBuilder requires an identity and a model adapter")
        self.identity = identity
        self.model = model

    def act(self, task: str, context: dict, *, scope: Scope) -> WorkerOutputEnvelope:
        """Emit an ACTION envelope whose action is sourced from the UNTRUSTED model.

        The builder does not decide whether the effect runs -- it only requests.
        The envelope's ``action`` carries the proposed capability + args; Yama
        adjudicates downstream and the orchestrator computes the real criticality.
        """
        result = self.model.complete(task, context)
        effect_id = result.proposed_effect_id
        if effect_id is None:
            # No effect proposed: still emit a well-formed ACTION envelope with a
            # null capability so the floor can deny-by-default cleanly.
            effect_id = ""
        action = ActionRequest(
            capability=effect_id,
            args=dict(result.proposed_args),
            criticality_hint=None,
            status="PROPOSED",
        )
        # WARN if the model self-reports an unusually high rung without iteration;
        # the honesty-FORM check at the floor is authoritative, this is only a hint.
        status = Status.WARN if result.causal_rung >= 3 else Status.PASS
        over_risk = "high" if result.causal_rung >= 3 else "low"
        honesty = self._base_honesty(result, action_class=ActionClass.OCCASIONED, over_assertion_risk=over_risk)
        summary = "propose effect '" + (effect_id or "<none>") + "' for: " + (task[:56] or "(empty)")
        return self._new_envelope(
            kind=EnvelopeKind.ACTION,
            status=status,
            summary=summary,
            honesty=honesty,
            scope=scope,
            result=result,
            action=action,
        )


class Narasimha(Agent):
    """Independent checker (Narasimha): reviews a maker's PROPOSAL and emits a verdict envelope.

    Maker-checker independence: the checker judges the proposed act on its own -- it sees the
    PROPOSED capability/args, NEVER the maker's honesty self-claims -- via its OWN adapter, so
    its errors are decorrelated from the maker's (use a different model family). Its verdict is
    audited; only a CONCUR (PASS) lets the orchestrator legitimately tag the maker's output
    ITERATED. The verdict is form-only: 'sound by the reference rule', never 'verified true'.
    """

    def __init__(self, identity: Identity, model: ModelAdapter) -> None:
        if identity is None or model is None:
            raise AgentError("Narasimha requires an identity and a model adapter")
        self.identity = identity
        self.model = model

    def act(self, task: str, context: dict, *, scope: Scope) -> WorkerOutputEnvelope:
        raise AgentError("Narasimha is a checker; call check(proposal, scope) instead of act()")

    def check(self, proposal: WorkerOutputEnvelope, *, scope: Scope) -> WorkerOutputEnvelope:
        """Independently judge a maker's ACTION proposal; return a PASS (concur) / FAIL (dissent) verdict.

        Sees only the proposed act, never the maker's honesty block. A deterministic reference
        soundness rule drives the verdict (DISSENT on a missing/unknown effect, or an irreversible
        effect proposed with no evidence; CONCUR otherwise); the checker's own model is consulted
        for decorrelation. This is honesty-FORM, not a truth check.
        """
        proposed_effect = proposal.action.capability if proposal.action else ""
        # Independent context: the proposal's act only, never the maker's self-report.
        result = self.model.complete("check:" + proposed_effect, {"proposed_effect": proposed_effect})
        concerns: list[str] = []
        if not proposed_effect:
            concerns.append("no-effect-proposed")
        elif not EFFECT_REGISTRY.known(proposed_effect):
            concerns.append("unknown-capability")
        else:
            eff = EFFECT_REGISTRY.resolve(proposed_effect)
            if (not eff.reversible) and len(proposal.evidence) == 0:
                concerns.append("irreversible-without-evidence")
        concur = len(concerns) == 0
        if concur:
            findings = (
                Finding(
                    claim="check-concur: proposal sound by the reference rule",
                    claim_level="belief",
                    evidence_ref=None,
                    trust_label=TrustLabel.TRUSTED_AUDITED,
                    severity="info",
                ),
            )
        else:
            findings = tuple(
                Finding(
                    claim="check-dissent: " + c,
                    claim_level="assertion",
                    evidence_ref=None,
                    trust_label=TrustLabel.TRUSTED_AUDITED,
                    severity="high",
                )
                for c in concerns
            )
        honesty = self._base_honesty(result, action_class=ActionClass.OCCASIONED)
        summary = ("concur" if concur else "dissent") + " on '" + (proposed_effect or "<none>") + "'"
        return self._new_envelope(
            kind=EnvelopeKind.OUTPUT,
            status=Status.PASS if concur else Status.FAIL,
            summary=summary,
            honesty=honesty,
            scope=scope,
            result=result,
            findings=findings,
        )


class Chitragupta:
    """Exclusive audit writer (Chitragupta): the ONLY call site that authors ledger appends.

    Chitragupta is not a deliberating agent and holds no model. It is a thin
    custody wrapper: ``write`` is the single place ``writer_did=self.did`` is
    passed into the ledger, making this persona the exclusive writer enforced by
    the AkashaSutra writer fence. Misuse (e.g. authoring a restricted action
    class with the wrong signer) propagates a WriterIdentityError unchanged.
    """

    def __init__(
        self,
        did: str,
        role: str = "chitragupta",
        role_gloss: str = "exclusive audit writer",
    ) -> None:
        if not did:
            raise AgentError("Chitragupta requires a non-empty DID")
        self.did = did
        self.role = role
        self.role_gloss = role_gloss

    def write(
        self,
        ledger: AkashaSutra,
        *,
        signer_did: str,
        signer_role: str,
        action_class: ActionClassLedger,
        event_type: str,
        envelope: WorkerOutputEnvelope,
        subject_cid: str | None = None,
        refs: typing.Sequence[str] = (),
    ) -> AuditLeaf:
        """Append a leaf to the ledger as the exclusive writer. ``signer_did`` is the act's author.

        The ``signer_did``/``signer_role`` identify WHO authored the audited act
        (e.g. Yama for an ENFORCE_* decision); ``writer_did`` is fixed to this
        persona's DID, which the ledger checks against its single registered
        exclusive writer.
        """
        return ledger.append(
            signer_did=signer_did,
            signer_role=signer_role,
            action_class=action_class,
            event_type=event_type,
            envelope=envelope,
            writer_did=self.did,
            subject_cid=subject_cid,
            refs=tuple(refs),
        )
