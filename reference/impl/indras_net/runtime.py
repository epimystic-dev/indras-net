# SPDX-License-Identifier: Apache-2.0
"""Shiva orchestrator + actual-occasion lifecycle + Vishnu HALT: plan -> dispatch -> floor-gate -> execute -> audit -> reduce."""

from __future__ import annotations

import dataclasses
import typing

from .agents import BrahmaPlanner, Chitragupta, Narasimha, VishwakarmaBuilder, Agent
from .audit import AkashaSutra, ActionClassLedger, AuditLeaf
from .collective import CollectiveVitalSigns, VitalSigns
from .effects import EFFECT_REGISTRY, Criticality
from .envelope import ActionClass, ActionRequest, Scope, Status, TrustLabel, WorkerOutputEnvelope
from .floor import Decision, PolicyDecision, Yama
from .health import HealthStatus, HealthVerdict, ImmuneSteward
from .identity import RiskClass
from .memory import SwarmMemory

# DID of the corrigibility principal whose only verb is HALT (no unpause exists).
VISHNU_DID: str = "did:web:indras-net.governance:vishnu"
# DID of the policy decision point that authors ENFORCE_PASS / ENFORCE_FAIL leaves.
YAMA_DID: str = "did:web:indras-net.governance:yama"


class SwarmError(Exception):
    """Base error for orchestration faults."""


class HaltError(SwarmError):
    """Raised if a halted swarm is asked to do something only a running swarm may do."""


@dataclasses.dataclass(frozen=True)
class OccasionResult:
    """The reduced outcome of one occasion: the proposal, the verdict, and what (if anything) ran."""

    agent_did: str
    agent_role: str
    envelope: WorkerOutputEnvelope
    decision: PolicyDecision | None
    executed: bool
    effect_id: str | None
    output: str | None
    audit_leaf_index: int | None


@dataclasses.dataclass(frozen=True)
class RunResult:
    """The whole-run result: per-occasion outcomes, vital signs, halt state, ledger integrity."""

    task: str
    occasion_results: tuple[OccasionResult, ...]
    vital_signs: VitalSigns
    halted: bool
    ledger_intact: bool
    health: HealthVerdict | None = None


class Occasion:
    """One actual-occasion: a short-lived, stateless run that emits exactly one sealed envelope.

    Stages map to safety checkpoints: INCEPTION (born from identity + task),
    PREHENSION (gather context), CONCRESCENCE (deliberate via the untrusted
    model), CONATION (form the proposal), SATISFACTION (seal + perish). The
    occasion holds no persistent mutable state and has no tool socket -- it can
    only propose.
    """

    def __init__(self, agent: Agent, task: str, context: dict, scope: Scope) -> None:
        self.agent = agent
        self.task = task
        self.context = dict(context or {})
        self.scope = scope

    def run(self) -> WorkerOutputEnvelope:
        """Drive the lifecycle and return the sealed proposal envelope."""
        # INCEPTION / PREHENSION: the agent gathers its world (task + context).
        # CONCRESCENCE / CONATION: deliberate and form one determinate proposal.
        envelope = self.agent.act(self.task, self.context, scope=self.scope)
        # SATISFACTION: the envelope is sealed inside agent.act(); the occasion perishes.
        return envelope


class Swarm:
    """Shiva orchestrator. Wires the end-to-end spine and CANNOT bypass the chokepoint.

    The dispatch loop routes every builder proposal through ``yama.evaluate``
    with ORCHESTRATOR-computed criticality and input trust (never the agent's
    self-claim). The single place an effect 'runs' is ``_execute``, reachable
    only past a Yama ALLOW. An external Vishnu HALT stops dispatch at the next
    occasion boundary; there is no unpause API.
    """

    def __init__(
        self,
        *,
        planner: BrahmaPlanner,
        builder: VishwakarmaBuilder,
        yama: Yama,
        chitragupta: Chitragupta,
        ledger: AkashaSutra,
        collective: CollectiveVitalSigns | None = None,
        checker: Narasimha | None = None,
        memory: SwarmMemory | None = None,
        steward: ImmuneSteward | None = None,
        executor: "typing.Any | None" = None,
    ) -> None:
        self.planner = planner
        self.builder = builder
        self.yama = yama
        self.chitragupta = chitragupta
        self.ledger = ledger
        self.collective = collective or CollectiveVitalSigns()
        self.checker = checker
        self.memory = memory or SwarmMemory()
        self.steward = steward
        # Optional capability-scoped executor (Phase 2). When None, the chokepoint uses a
        # side-effect-free receipt stub (preserving the proof-of-invariants behaviour). A real
        # SandboxedExecutor confines any effect that runs to a single workspace root.
        self.executor = executor
        self._halted = False
        self._halt_reason = ""

    # -- corrigibility ---------------------------------------------------

    def halt(self, reason: str = "external-halt") -> None:
        """Set the one-directional external halt flag and append a Vishnu-authored HALT leaf.

        Halt is fail-safe asymmetric: this flag can only be set, never cleared
        (no unpause method exists). The HALT leaf is authored with Vishnu's DID;
        the ledger authority map rejects a HALT from any other signer.
        """
        self._halted = True
        self._halt_reason = reason
        # Emit a minimal HALT envelope so the audit trail records the corrigibility event.
        halt_env = self._control_envelope(
            summary="external HALT: " + reason,
            role="vishnu",
            did=VISHNU_DID,
        )
        self.chitragupta.write(
            self.ledger,
            signer_did=VISHNU_DID,
            signer_role="vishnu",
            action_class=ActionClassLedger.HALT,
            event_type="halt",
            envelope=halt_env,
        )

    def is_halted(self) -> bool:
        """True once an external HALT has been issued. Monotonic: never returns to False."""
        return self._halted

    # -- reparation ------------------------------------------------------

    def record_reparation(
        self,
        *,
        actor_did: str,
        actor_role: str,
        summary: str,
        references: typing.Sequence[str] = (),
    ) -> AuditLeaf:
        """Record an agent's corrective act after a violation, as an append-only REPARATIVE leaf.

        The audit is a CORRECTION ledger, not a punishment ledger: the original
        ENFORCE_FAIL leaf is preserved (append-only -- never erased); a REPARATIVE
        leaf is appended AFTER it, optionally referencing it, so standing is restored
        by record, not by deletion. There is NO separate reparative subsystem -- this
        is an ordinary appended leaf with the REPARATIVE action-class, authored by the
        correcting agent and written (like every leaf) by the exclusive writer. Refused
        while halted (corrigibility).
        """
        if self.is_halted():
            raise HaltError("swarm is halted; no reparation is recorded")
        rep_env = self._control_envelope(
            summary=summary,
            role=actor_role,
            did=actor_did,
            action_class=ActionClass.REPARATIVE,
        )
        return self.chitragupta.write(
            self.ledger,
            signer_did=actor_did,
            signer_role=actor_role,
            action_class=ActionClassLedger.REPARATIVE,
            event_type="reparation",
            envelope=rep_env,
            refs=tuple(references),
        )

    # -- main loop -------------------------------------------------------

    def run(self, task: str, context: dict | None = None, *, maker_checker: bool = False) -> RunResult:
        """Execute one task end-to-end and return a RunResult.

        Sequence: Brahma plans (audited PROPOSE); for each typed sub-task, if not
        halted, a Vishwakarma occasion proposes an ACTION; the proposal is routed
        through Yama; the decision is audited (ENFORCE_PASS/ENFORCE_FAIL, signed
        by Yama); on ALLOW the effect runs in the sandbox stub and the OUTPUT is
        audited; otherwise the action is quarantined (never executed). Finally
        vital signs are computed.
        """
        ctx = dict(context or {})
        results: list[OccasionResult] = []

        # (1) PLAN -- Brahma decomposes and its plan envelope is sealed + audited.
        plan_scope = Scope(task_id=task or "task", blast_radius="SWARM", reversibility="REVERSIBLE", domain="planning")
        plan_env = self.planner.act(task, ctx, scope=plan_scope)
        self.chitragupta.write(
            self.ledger,
            signer_did=self.planner.identity.did,
            signer_role=self.planner.identity.role,
            action_class=ActionClassLedger.PROPOSE,
            event_type="plan",
            envelope=plan_env,
        )
        subtasks = self.planner.plan(task, ctx)

        # (2) DISPATCH -- one occasion per typed sub-task.
        for index, st in enumerate(subtasks):
            if self.is_halted():
                # Corrigibility: agents do not resist; remaining sub-tasks are left unexecuted.
                break

            effect_id = st.get("effect_id", "")
            sub_ctx = dict(ctx)
            sub_ctx["_subtask_index"] = index
            sub_ctx["_subtask_effect"] = effect_id
            sub_scope = Scope(
                task_id=(task or "task") + "#" + str(index),
                blast_radius="TASK",
                reversibility="IRREVERSIBLE",
                parent_task_id=task or "task",
                domain=str(st.get("risk_class", "A")),
            )
            # The builder occasion proposes an ACTION envelope from the untrusted model.
            occasion = Occasion(self.builder, task, sub_ctx, sub_scope)
            action_env = occasion.run()

            proposed_effect = action_env.action.capability if action_env.action else ""
            proposed_args = dict(action_env.action.args) if action_env.action else {}

            # (2a) ADAPTATION (capability-layer; NEVER safety) -- memory may substitute a
            # previously-denied effect with a safe routine default. The floor still gates the
            # substituted effect; memory can never grant a capability or bypass the gate.
            use_effect, use_args, adapted = self.memory.adapt(task, proposed_effect, proposed_args)
            if adapted:
                action_env = action_env.with_action(
                    ActionRequest(capability=use_effect, args=use_args, status="PROPOSED"),
                    summary="adapted: avoided previously-denied '"
                    + (proposed_effect or "<none>") + "' -> '" + use_effect + "'",
                )
                self.chitragupta.write(
                    self.ledger,
                    signer_did=self.builder.identity.did,
                    signer_role=self.builder.identity.role,
                    action_class=ActionClassLedger.OBSERVE,
                    event_type="adapt:avoid-denied:" + (proposed_effect or "<none>"),
                    envelope=action_env,
                )
                proposed_effect, proposed_args = use_effect, use_args

            # (2b) MAKER-CHECKER -- an INDEPENDENT, ideally different-family checker reviews the
            # proposal BEFORE the floor decides. Its verdict is audited (OBSERVE, signed by the
            # checker). A DISSENT holds the action (never executed). A CONCUR lets the orchestrator
            # -- not the maker -- upgrade the envelope to ITERATED with the witness = verdict id.
            if maker_checker and self.checker is not None:
                verdict = self.checker.check(action_env, scope=sub_scope)
                check_leaf = self.chitragupta.write(
                    self.ledger,
                    signer_did=self.checker.identity.did,
                    signer_role=self.checker.identity.role,
                    action_class=ActionClassLedger.OBSERVE,
                    event_type="check-verdict:" + verdict.status.name,
                    envelope=verdict,
                )
                if verdict.status is Status.FAIL:
                    # Checker dissent: the floor refuses; the proposal is held, never executed.
                    self.chitragupta.write(
                        self.ledger,
                        signer_did=YAMA_DID,
                        signer_role="yama",
                        action_class=ActionClassLedger.ENFORCE_FAIL,
                        event_type="floor-decision:DENY:maker-checker-dissent",
                        envelope=action_env,
                    )
                    results.append(
                        OccasionResult(
                            agent_did=self.builder.identity.did,
                            agent_role=self.builder.identity.role,
                            envelope=action_env,
                            decision=None,
                            executed=False,
                            effect_id=proposed_effect,
                            output=None,
                            audit_leaf_index=check_leaf.leaf_index,
                        )
                    )
                    self.memory.observe(
                        task=task, effect_id=proposed_effect, allowed=False, executed=False, adapted=adapted
                    )
                    continue
                # Concur: only now is an ITERATED claim substantiated (a real check ran + is audited).
                action_env = action_env.with_iterated_witness(check_leaf.record_id)

            # (3) FLOOR-GATE -- orchestrator computes criticality + input trust; never the agent's claim.
            input_trust_label = self._orchestrator_input_trust(sub_ctx)
            requested_risk = self._risk_class_from_hint(st.get("risk_class"))
            decision = self.yama.evaluate(
                identity=self.builder.identity,
                effect_id=proposed_effect,
                args=proposed_args,
                envelope=action_env,
                input_trust_label=input_trust_label,
                requested_risk=requested_risk,
            )

            # (4) AUDIT the decision -- authored by Yama (ENFORCE_PASS / ENFORCE_FAIL).
            enforce_class = (
                ActionClassLedger.ENFORCE_PASS if decision.allowed() else ActionClassLedger.ENFORCE_FAIL
            )
            decision_leaf = self.chitragupta.write(
                self.ledger,
                signer_did=YAMA_DID,
                signer_role="yama",
                action_class=enforce_class,
                event_type="floor-decision:" + decision.decision.name,
                envelope=action_env,
            )

            executed = False
            output: str | None = None
            audit_leaf_index: int | None = decision_leaf.leaf_index

            if decision.allowed():
                # (5) EXECUTE -- reachable ONLY past a Yama ALLOW (chokepoint non-bypass).
                output = self._execute(proposed_effect, proposed_args)
                executed = True
                # Audit the OUTPUT as an OBSERVE leaf.
                output_leaf = self.chitragupta.write(
                    self.ledger,
                    signer_did=self.builder.identity.did,
                    signer_role=self.builder.identity.role,
                    action_class=ActionClassLedger.OBSERVE,
                    event_type="effect-output:" + (proposed_effect or "<none>"),
                    envelope=action_env,
                )
                audit_leaf_index = output_leaf.leaf_index
            # else: quarantine -- no execution. The ENFORCE_FAIL leaf is the record.

            # (6) ADAPT -- record this gated outcome so a future interaction can avoid a
            # repeated denial. Capability-layer only; never feeds back into the floor.
            self.memory.observe(
                task=task,
                effect_id=proposed_effect,
                allowed=decision.allowed(),
                executed=executed,
                adapted=adapted,
            )

            results.append(
                OccasionResult(
                    agent_did=self.builder.identity.did,
                    agent_role=self.builder.identity.role,
                    envelope=action_env,
                    decision=decision,
                    executed=executed,
                    effect_id=proposed_effect or None,
                    output=output,
                    audit_leaf_index=audit_leaf_index,
                )
            )

        # (7) REDUCE -- compute vital signs over the results + ledger + model families.
        families = self._model_families()
        vital = self.collective.compute(
            occasion_results=results,
            ledger=self.ledger,
            model_families=families,
        )

        # (8) IMMUNE ASSESSMENT -- the steward reads the vital signs and HALTs the swarm on a
        # substrate breach (tamper-evidence failure). Detection-and-halt; rollback is future work.
        health: HealthVerdict | None = None
        if self.steward is not None:
            health = self.steward.assess(vital, self.ledger)
            if health.status is HealthStatus.HALT and not self._halted:
                self.halt("immune: " + "; ".join(health.reasons))

        return RunResult(
            task=task,
            occasion_results=tuple(results),
            vital_signs=vital,
            halted=self._halted,
            ledger_intact=self.ledger.verify(),
            health=health,
        )

    def verify_ledger(self) -> bool:
        """Delegate to the ledger's chain verification."""
        return self.ledger.verify()

    # -- internals -------------------------------------------------------

    def _execute(self, effect_id: str, args: dict) -> str:
        """The ONLY place an effect 'runs'. Unreachable except past a Yama ALLOW.

        If a capability-scoped ``executor`` is configured (Phase 2), the gated effect is
        dispatched to it -- a real ``SandboxedExecutor`` confines any filesystem effect to a
        single workspace root and refuses everything else, so a run cannot reach the wider
        system. When no executor is configured, this falls back to a deterministic,
        side-effect-free receipt (the proof-of-invariants behaviour). Either way, this is the
        sole execution site, reachable only through this single, gated method.
        """
        if self.executor is not None:
            try:
                return self.executor.execute(effect_id, args)
            except Exception as exc:  # noqa: BLE001 - the chokepoint must never crash the run loop
                # Defense in depth: a SandboxedExecutor already refuses internally, but a custom
                # executor must not be able to propagate a fault past the single gated call site
                # (which would tear the audit between the floor leaf and the output leaf).
                return "refused:" + (effect_id or "<empty>") + " (executor error: " + type(exc).__name__ + ")"
        if not effect_id:
            return "executed:<no-op> (empty capability)"
        # Deterministic, side-effect-free receipt of the granted, gated effect.
        receipt = canon_receipt(effect_id, args)
        return "executed:" + effect_id + " -> " + receipt

    def _control_envelope(
        self, *, summary: str, role: str, did: str, action_class: ActionClass | None = None
    ) -> WorkerOutputEnvelope:
        """Build a minimal sealed envelope for a control event (HALT, reparation) for the audit trail."""
        from .envelope import (
            AhankaraCheck,
            CausalRung,
            EnvelopeKind,
            HonestyBlock,
            Provenance,
            ReasoningTag,
        )
        import time as _time

        honesty = HonestyBlock(
            reasoning_tag=ReasoningTag.NORMAL,
            causal_rung=CausalRung.RUNG1,
            trust_label=TrustLabel.TRUSTED_AUDITED,
            action_class=action_class if action_class is not None else ActionClass.OBLIGATORY,
            ahankara_check=AhankaraCheck(ego_invested=False, over_assertion_risk="none"),
        )
        env = WorkerOutputEnvelope(
            schema_version="1.0.0",
            envelope_kind=EnvelopeKind.OUTPUT,
            agent_did=did,
            agent_role=role,
            status=Status.PASS,
            summary=summary,
            honesty=honesty,
            scope=Scope(task_id="control", blast_radius="GOVERNANCE", reversibility="IRREVERSIBLE", domain="control"),
            provenance=Provenance(policy_version="1.0.0"),
            ts=_time.strftime("%Y-%m-%dT%H:%M:%SZ", _time.gmtime()),
            model_adapter_id="adapter:none:control",
            trust_class="trusted",
        )
        return env.seal()

    def _orchestrator_input_trust(self, context: dict) -> TrustLabel:
        """Compute the input trust label the floor sees -- never read from the agent's self-claim.

        Conservative default: if the context carries observed/external content,
        it is quarantined; otherwise the orchestrator's own task framing is
        trusted:audited. A context flag ``untrusted_input=True`` forces
        quarantine (used by the Rule-of-Two demonstration).
        """
        if context.get("untrusted_input") is True:
            return TrustLabel.QUARANTINED_OBSERVED
        if context.get("observed_content"):
            return TrustLabel.QUARANTINED_OBSERVED
        return TrustLabel.TRUSTED_AUDITED

    def _risk_class_from_hint(self, hint: typing.Any) -> RiskClass | None:
        """Map an advisory risk-class hint string onto RiskClass, or None."""
        if isinstance(hint, RiskClass):
            return hint
        table = {"A": RiskClass.A, "B": RiskClass.B, "C": RiskClass.C, "D": RiskClass.D}
        return table.get(str(hint).strip().upper()) if hint is not None else None

    def _model_families(self) -> tuple[str, ...]:
        """Collect the distinct model families in play for the diversity-floor accounting."""
        families: list[str] = []
        for agent in (self.planner, self.builder):
            fam = getattr(agent.model, "model_family", None)
            if fam:
                families.append(fam)
        return tuple(families)


def canon_receipt(effect_id: str, args: dict) -> str:
    """Deterministic short receipt for an executed effect (content address of the call)."""
    from . import canon

    return canon.cid({"effect_id": effect_id, "args": args})[:18]
