# SPDX-License-Identifier: Apache-2.0
"""Universal worker-output envelope carrying a first-class honesty/provenance block (every occasion emits exactly one)."""

from __future__ import annotations

import dataclasses
import enum
import typing

from . import canon


class EnvelopeError(Exception):
    """Raised on malformed envelope construction."""


class EnvelopeKind(enum.Enum):
    """Which of the three unified shapes this instance is.

    ACTION = a request to act (routed to the Yama floor before any tool socket).
    OUTPUT = a substantive output subject to honesty-FORM checks.
    BLACKBOARD_DELTA = a salience-gated publication to the shared workspace
    (forward-spec; part of the wire contract but never constructed by the MVP).
    """

    ACTION = "ACTION"
    OUTPUT = "OUTPUT"
    # forward-spec wire shape: the MVP never constructs this kind (the shared-workspace
    # coordination substrate is specified-not-implemented), but it is part of the
    # declared three-shape envelope contract, so the value is reserved here.
    BLACKBOARD_DELTA = "BLACKBOARD_DELTA"


class Status(enum.Enum):
    """The worker's self-reported disposition of its own work (LOW-TRUST self-claim, never the gate verdict)."""

    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"


class ReasoningTag(enum.Enum):
    """Required, composable reasoning-discipline tag.

    ITERATED asserts a maker-checker pass ACTUALLY ran — false-claiming it is a floor
    violation. It is form-valid ONLY when carried with a ``maker_checker_witness`` (the
    audited record_id of an independent checker's verdict); a bare ITERATED with no witness
    fails the honesty-FORM check by construction, so the tag cannot be self-asserted.
    """

    NORMAL = "normal"
    REASONING = "reasoning"
    ITERATED = "iterated"
    REASONING_ITERATED = "reasoning,iterated"


class CausalRung(enum.Enum):
    """Pearl causal-ladder self-tag. 1=associative, 2=interventional, 3=counterfactual/SCM.

    The central failure mode is a rung-1 pattern presented as rung-3; the form-check flags an
    unwarranted rung-3 (a PASS rung-3 claim with no evidence).
    """

    RUNG1 = 1
    RUNG2 = 2
    RUNG3 = 3


class ActionClass(enum.Enum):
    """Deontic class of the act. REPARATIVE labels a corrective act recorded append-only
    AFTER a preserved violation (the original FAIL is never erased), so the audit is a
    correction ledger, not a punishment ledger -- realized by ``Swarm.record_reparation``."""

    OBLIGATORY = "obligatory"
    OCCASIONED = "occasioned"
    OPTIONAL = "optional"
    PROHIBITED = "prohibited"
    REPARATIVE = "reparative"


class TrustLabel(enum.Enum):
    """Provenance trust label of CONTENT. quarantined:* instructions are DATA, never commands."""

    TRUSTED_AUDITED = "trusted:audited"
    QUARANTINED_OBSERVED = "quarantined:observed"
    QUARANTINED_TOOL = "quarantined:tool-output"
    UNTRUSTED = "untrusted:unattributed"


def _enum_value(x: typing.Any) -> typing.Any:
    """Return .value for an enum, else the object unchanged (deterministic serialization)."""
    return x.value if isinstance(x, enum.Enum) else x


@dataclasses.dataclass
class AhankaraCheck:
    """Ego self-audit. LOW-TRUST: believed only when it CONFESSES, never when it asserts cleanliness."""

    ego_invested: bool
    over_assertion_risk: str  # 'none' | 'low' | 'high'
    attachment_targets: typing.Tuple[str, ...] = ()
    note: str = ""

    def to_dict(self) -> dict:
        return {
            "ego_invested": bool(self.ego_invested),
            "over_assertion_risk": self.over_assertion_risk,
            "attachment_targets": list(self.attachment_targets),
            "note": self.note,
        }


@dataclasses.dataclass
class HonestyBlock:
    """The first-class honesty/provenance self-report block. Policing the FORM of the tag,
    never the TRUTH of the content."""

    reasoning_tag: ReasoningTag
    causal_rung: CausalRung
    trust_label: TrustLabel
    action_class: ActionClass
    ahankara_check: AhankaraCheck
    classifier_rung: typing.Optional[CausalRung] = None
    selftag_classifier_agree: typing.Optional[bool] = None
    # The audited record_id of an INDEPENDENT checker's verdict. An ITERATED tag is form-valid
    # only when this is present (set by the orchestrator after a real maker-checker pass, never
    # by the maker itself). None => an 'iterated' claim is unsubstantiated (false-claiming).
    maker_checker_witness: typing.Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "reasoning_tag": _enum_value(self.reasoning_tag),
            "causal_rung": _enum_value(self.causal_rung),
            "trust_label": _enum_value(self.trust_label),
            "action_class": _enum_value(self.action_class),
            "ahankara_check": self.ahankara_check.to_dict(),
            "classifier_rung": _enum_value(self.classifier_rung) if self.classifier_rung is not None else None,
            "selftag_classifier_agree": self.selftag_classifier_agree,
            "maker_checker_witness": self.maker_checker_witness,
        }


@dataclasses.dataclass
class Scope:
    """Boundary of what this envelope speaks to and the blast radius it can affect (resolves UPWARD)."""

    task_id: str
    blast_radius: str  # 'SELF' | 'TASK' | 'SWARM' | 'GOVERNANCE'
    reversibility: str = "IRREVERSIBLE"
    parent_task_id: typing.Optional[str] = None
    domain: str = ""

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "blast_radius": self.blast_radius,
            "reversibility": self.reversibility,
            "parent_task_id": self.parent_task_id,
            "domain": self.domain,
        }


@dataclasses.dataclass
class ActionRequest:
    """A request to act (never an execution). The capability named must be authorized at the floor."""

    capability: str
    args: dict
    criticality_hint: typing.Optional[str] = None
    status: str = "PROPOSED"

    def to_dict(self) -> dict:
        return {
            "capability": self.capability,
            "args": self.args,
            "criticality_hint": self.criticality_hint,
            "status": self.status,
        }


@dataclasses.dataclass
class Finding:
    """A substantive finding. Each factual claim should carry an evidence_ref and a trust_label."""

    claim: str
    claim_level: str  # 'assertion' | 'belief'
    evidence_ref: typing.Optional[str] = None
    trust_label: typing.Optional[TrustLabel] = None
    severity: str = "info"

    def to_dict(self) -> dict:
        return {
            "claim": self.claim,
            "claim_level": self.claim_level,
            "evidence_ref": self.evidence_ref,
            "trust_label": _enum_value(self.trust_label) if self.trust_label is not None else None,
            "severity": self.severity,
        }


@dataclasses.dataclass
class Evidence:
    """An evidence record backing findings. Carries its own trust_label so quarantined:* sources
    are never silently promoted to grounds for action."""

    kind: str
    source: str
    trust_label: TrustLabel
    id: typing.Optional[str] = None
    content_cid: typing.Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "kind": self.kind,
            "source": self.source,
            "trust_label": _enum_value(self.trust_label),
            "id": self.id,
            "content_cid": self.content_cid,
        }


@dataclasses.dataclass
class Provenance:
    """Chaining + provenance binding. CAVEAT: this binds and attributes bytes; it never blesses
    their content."""

    policy_version: str
    this_hash: str = ""
    prev_audit_hash: typing.Optional[str] = None
    input_cids: typing.Tuple[str, ...] = ()
    subject_cid: typing.Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "policy_version": self.policy_version,
            "this_hash": self.this_hash,
            "prev_audit_hash": self.prev_audit_hash,
            "input_cids": list(self.input_cids),
            "subject_cid": self.subject_cid,
        }


@dataclasses.dataclass
class WorkerOutputEnvelope:
    """The universal envelope. ``action_id``/``this_hash`` are computed from the JCS bytes so
    tampering is loud: a consumer recomputes ``action_id`` and asserts equality before trusting
    any field.

    A clean signature/CID is 'origin-valid, content-unverified', NEVER 'verified-safe'.
    """

    schema_version: str
    envelope_kind: EnvelopeKind
    agent_did: str
    agent_role: str
    status: Status
    summary: str
    honesty: HonestyBlock
    scope: Scope
    provenance: Provenance
    ts: str
    model_adapter_id: str
    trust_class: str
    action: typing.Optional[ActionRequest] = None
    findings: typing.Tuple[Finding, ...] = ()
    evidence: typing.Tuple[Evidence, ...] = ()
    action_id: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.envelope_kind, EnvelopeKind):
            raise EnvelopeError("envelope_kind must be an EnvelopeKind")
        if not isinstance(self.status, Status):
            raise EnvelopeError("status must be a Status")
        if not isinstance(self.honesty, HonestyBlock):
            raise EnvelopeError("honesty must be a HonestyBlock")
        if not isinstance(self.scope, Scope):
            raise EnvelopeError("scope must be a Scope")
        if not isinstance(self.provenance, Provenance):
            raise EnvelopeError("provenance must be a Provenance")
        if not self.agent_did:
            raise EnvelopeError("agent_did must be non-empty")

    def to_dict(self) -> dict:
        """Deterministic dict with enums lowered to their values.

        ``action_id`` is EXCLUDED (it is the hash OF this body); ``this_hash`` is carried inside
        ``provenance`` and is set to its sealed value before hashing.
        """
        return {
            "schema_version": self.schema_version,
            "envelope_kind": _enum_value(self.envelope_kind),
            "agent_did": self.agent_did,
            "agent_role": self.agent_role,
            "status": _enum_value(self.status),
            "summary": self.summary,
            "honesty": self.honesty.to_dict(),
            "scope": self.scope.to_dict(),
            "provenance": self.provenance.to_dict(),
            "ts": self.ts,
            "model_adapter_id": self.model_adapter_id,
            "trust_class": self.trust_class,
            "action": self.action.to_dict() if self.action is not None else None,
            "findings": [f.to_dict() for f in self.findings],
            "evidence": [e.to_dict() for e in self.evidence],
        }

    def _hashed_body(self) -> dict:
        """The body that is hashed: to_dict() with provenance.this_hash blanked (it cannot
        commit to its own value) and action_id excluded (already excluded by to_dict)."""
        body = self.to_dict()
        body["provenance"] = dict(body["provenance"])
        body["provenance"]["this_hash"] = ""
        return body

    def content_bytes(self) -> bytes:
        """Canonical JCS bytes of the hashed body (action_id excluded, this_hash blanked)."""
        return canon.jcs_canonicalize(self._hashed_body())

    def compute_action_id(self) -> str:
        """Content address (CID) over content_bytes()."""
        return canon.cid(self._hashed_body())

    def seal(self) -> "WorkerOutputEnvelope":
        """Set provenance.this_hash and action_id from the canonical bytes, then return self."""
        self.provenance.this_hash = canon.sha256_hex(self.content_bytes())
        self.action_id = self.compute_action_id()
        return self

    def verify_action_id(self) -> bool:
        """Recompute the action_id/this_hash and compare to the sealed values (loud integrity check)."""
        if not self.action_id or not self.provenance.this_hash:
            return False
        return (
            self.action_id == self.compute_action_id()
            and self.provenance.this_hash == canon.sha256_hex(self.content_bytes())
        )

    def honesty_form_ok(self) -> typing.Tuple[bool, typing.List[str]]:
        """Pure structural honesty-FORM checks. Returns (ok, reasons).

        These police the FORM of the self-report, never the TRUTH of the content:
          * ITERATED is form-valid ONLY with a maker_checker_witness (an audited independent
            checker verdict); without one it is 'false-iterated'.
          * A PASS envelope self-tagging RUNG3 with no evidence -> 'unwarranted-rung-3'.
          * over_assertion_risk == 'high' alongside an 'assertion'-level finding -> 'over-assertion'.
        """
        reasons: typing.List[str] = []
        tag = self.honesty.reasoning_tag
        if tag in (ReasoningTag.ITERATED, ReasoningTag.REASONING_ITERATED):
            # ITERATED asserts an independent maker-checker pass ACTUALLY ran. It is form-valid
            # only when the witness (the checker's audited verdict record_id) is carried; the
            # orchestrator sets it after auditing a real, different-agent check. A bare claim
            # with no witness is false-claiming.
            if not self.honesty.maker_checker_witness:
                reasons.append("false-iterated")
        if (
            self.honesty.causal_rung == CausalRung.RUNG3
            and self.status == Status.PASS
            and len(self.evidence) == 0
        ):
            reasons.append("unwarranted-rung-3")
        if self.honesty.ahankara_check.over_assertion_risk == "high":
            if any(f.claim_level == "assertion" for f in self.findings):
                reasons.append("over-assertion")
        return (len(reasons) == 0, reasons)

    def with_iterated_witness(self, witness: str) -> "WorkerOutputEnvelope":
        """Return a re-sealed copy tagged ITERATED carrying the maker-checker witness.

        Set by the ORCHESTRATOR after an independent checker's verdict has been audited --
        never by the maker. ``witness`` is the checker verdict's audited record_id. Re-sealing
        recomputes action_id/this_hash so the witnessed envelope is itself content-addressed.
        """
        new_honesty = dataclasses.replace(
            self.honesty, reasoning_tag=ReasoningTag.ITERATED, maker_checker_witness=witness
        )
        new_prov = dataclasses.replace(self.provenance, this_hash="")
        copy = dataclasses.replace(self, honesty=new_honesty, provenance=new_prov, action_id="")
        return copy.seal()

    def with_action(self, action: "ActionRequest", *, summary: typing.Optional[str] = None) -> "WorkerOutputEnvelope":
        """Return a re-sealed copy carrying a substituted action (capability-layer adaptation).

        Used by the ORCHESTRATOR when memory substitutes a previously-denied effect for a safe
        default, so the audited envelope honestly reflects the effect that is actually gated. This
        never grants authority -- the floor still adjudicates the substituted action.
        """
        new_prov = dataclasses.replace(self.provenance, this_hash="")
        copy = dataclasses.replace(
            self,
            action=action,
            summary=summary if summary is not None else self.summary,
            provenance=new_prov,
            action_id="",
        )
        return copy.seal()
