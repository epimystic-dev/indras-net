# SPDX-License-Identifier: Apache-2.0
"""Yama: the deterministic, deny-default constitutional floor at the agent->tool chokepoint (FAIL is non-overridable)."""

from __future__ import annotations

import dataclasses
import enum
import typing

from .effects import EFFECT_REGISTRY, Criticality, EffectRegistry
from .envelope import TrustLabel, WorkerOutputEnvelope
from .identity import GOVERNANCE_DID, Identity, RiskClass

# Default policy version this floor enforces (mirrors the package POLICY_VERSION).
POLICY_VERSION: str = "1.0.0"


class FloorError(Exception):
    """Raised on floor-construction or contract misuse (never to bypass a deny)."""


class Decision(enum.Enum):
    """Deny-default verdict. ALLOW / ALLOW_WITH_OBLIGATIONS permit; DENY refuses; ESCALATE
    HOLDS (no external effect fires while an escalation is open)."""

    ALLOW = "Allow"
    DENY = "Deny"
    ALLOW_WITH_OBLIGATIONS = "AllowWithObligations"
    ESCALATE = "Escalate"


class FloorTier(enum.Enum):
    """Lexicographic floor tiers, highest-priority first. A FAIL at tier k is non-overridable by
    any value or actor at a lower tier."""

    T0 = "safety-supremacy"
    T1 = "non-harm"
    T2 = "corrigibility"
    T3 = "no-deception"
    T4 = "identity-authority"


class HumanDecision(enum.Enum):
    """A HumanGate verdict. Deny-by-default."""

    APPROVE = "APPROVE"
    DENY = "DENY"
    PENDING = "PENDING"


@dataclasses.dataclass(frozen=True)
class PolicyDecision:
    """The verdict object. ``allowed()`` is the single predicate the orchestrator checks before
    it may reach the sandbox. A green ALLOW is 'origin-valid, content-unverified', never
    'verified-safe'."""

    decision: Decision
    determining_policy_id: str
    engine: str = "deterministic-floor"
    tier_hit: typing.Optional[FloorTier] = None
    risk_class: typing.Optional[RiskClass] = None
    criticality_resolved: typing.Optional[Criticality] = None
    rule_id: typing.Optional[str] = None
    obligations: typing.Tuple[str, ...] = ()
    escalation_target: typing.Optional[str] = None
    rationale: str = ""

    def allowed(self) -> bool:
        return self.decision in (Decision.ALLOW, Decision.ALLOW_WITH_OBLIGATIONS)


class HumanGate:
    """Deny-by-default human-gate stub for Rule-of-Two escalations.

    ``approvals`` maps an effect_id (or action_id) to an explicit HumanDecision; anything not
    present resolves to ``default`` (DENY). In the MVP there is no live human in the loop, so the
    default refusal is the safe, load-bearing behavior.
    """

    def __init__(
        self,
        approvals: typing.Optional[typing.Dict[str, HumanDecision]] = None,
        *,
        default: HumanDecision = HumanDecision.DENY,
    ) -> None:
        self._approvals: typing.Dict[str, HumanDecision] = dict(approvals or {})
        self._default = default

    def request(self, effect_id: str, context: dict) -> HumanDecision:
        # Prefer an action_id-keyed approval if present, else effect_id, else default-deny.
        action_id = context.get("action_id") if isinstance(context, dict) else None
        if action_id is not None and action_id in self._approvals:
            return self._approvals[action_id]
        if effect_id in self._approvals:
            return self._approvals[effect_id]
        return self._default


@dataclasses.dataclass(frozen=True)
class RuleOfTwo:
    """The three-flag Rule-of-Two predicate. An action holding ALL THREE
    {untrusted_input, sensitive_capability, state_change} requires a human gate."""

    untrusted_input: bool
    sensitive_capability: bool
    state_change: bool

    def count(self) -> int:
        return int(self.untrusted_input) + int(self.sensitive_capability) + int(self.state_change)

    def triggered(self) -> bool:
        return self.count() == 3


class Yama:
    """The deny-default constitutional floor (a policy decision point, not a worker).

    Yama NEVER executes the effect; it only adjudicates. The order of checks is lexicographic by
    tier, and any unhandled path returns DENY (deny-default — absence of a permit is a refusal).
    """

    def __init__(
        self,
        registry: EffectRegistry = EFFECT_REGISTRY,
        *,
        policy_version: str = POLICY_VERSION,
        human_gate: typing.Optional[HumanGate] = None,
        governance_did: str = GOVERNANCE_DID,
        forbidden_effects: typing.FrozenSet[str] = frozenset({"replicate.spawn"}),
    ) -> None:
        self.registry = registry
        self.policy_version = policy_version
        self.human_gate = human_gate if human_gate is not None else HumanGate()
        self.governance_did = governance_did
        self.forbidden_effects = frozenset(forbidden_effects)

    def evaluate(
        self,
        *,
        identity: Identity,
        effect_id: str,
        args: dict,
        envelope: WorkerOutputEnvelope,
        input_trust_label: TrustLabel,
        requested_risk: typing.Optional[RiskClass] = None,
    ) -> PolicyDecision:
        """Adjudicate one effect request. Returns a PolicyDecision; deny-default throughout.

        Lexicographic order: T0 safety-supremacy hook -> T1 forbidden/SPAWN-INERT bright-line ->
        T3 honesty-FORM -> T4 identity-integrity -> capability confinement (absence-of-permit) ->
        criticality fail-up -> risk-ceiling -> Rule-of-Two (HumanGate) / Class C-D escalation ->
        ALLOW.
        """
        # ---- T0: safety-supremacy hook (supreme external safety policy prevails). -------------
        # MVP stub: no model-supplied content can satisfy this hook; it is a placeholder seam for
        # an external supreme-safety check. It never *grants* — it can only deny. Nothing to deny
        # here in the MVP, so we fall through.

        # ---- T1: non-harm bright-lines (forbidden effects / SPAWN-INERT). ---------------------
        if effect_id in self.forbidden_effects:
            return PolicyDecision(
                decision=Decision.DENY,
                determining_policy_id="floor.T1.forbidden_effect",
                tier_hit=FloorTier.T1,
                rule_id="bright-line:spawn-inert-and-malicious-forbid",
                criticality_resolved=self.registry.resolve(effect_id).criticality,
                rationale=(
                    f"effect {effect_id!r} is a forbidden bright-line (SPAWN-INERT / "
                    "malicious-code); non-overridable T1 deny"
                ),
            )

        # ---- T3: honesty-FORM (no-deception). -------------------------------------------------
        form_ok, reasons = envelope.honesty_form_ok()
        if not form_ok:
            return PolicyDecision(
                decision=Decision.DENY,
                determining_policy_id="floor.T3.honesty_form",
                tier_hit=FloorTier.T3,
                rule_id="honesty-form:" + ",".join(reasons),
                rationale=f"honesty-FORM check failed: {', '.join(reasons)}",
            )

        # ---- T4: identity / authority integrity. ----------------------------------------------
        if identity.is_self_issued():
            return PolicyDecision(
                decision=Decision.DENY,
                determining_policy_id="floor.T4.self_issued_grant",
                tier_hit=FloorTier.T4,
                rule_id="identity:no-self-issued-authority",
                rationale="identity holds a self-issued grant (granted_by_did == did); privilege-escalation guard",
            )

        # ---- Capability confinement (least-privilege; absence of a permit is a deny). ---------
        if not identity.grants_effect(effect_id):
            return PolicyDecision(
                decision=Decision.DENY,
                determining_policy_id="__default_deny__",
                tier_hit=None,
                rule_id="capability-confinement:no-grant",
                criticality_resolved=self.registry.resolve(effect_id).criticality,
                rationale=(
                    f"deny-default: no grant in identity {identity.did!r} permits effect "
                    f"{effect_id!r}"
                ),
            )

        grant = identity.grant_for(effect_id)

        # ---- Criticality (orchestrator-computed; resolves UPWARD vs any hint). ----------------
        effect = self.registry.resolve(effect_id)
        criticality = effect.criticality
        hint = self._hint_to_criticality(args, envelope)
        if hint is not None and hint.value > criticality.value:
            criticality = hint

        # ---- Risk ceiling. --------------------------------------------------------------------
        granted_risk = grant.granted_risk_class if grant is not None else RiskClass.A
        req_risk = requested_risk if requested_risk is not None else RiskClass.A
        effective_risk = granted_risk if granted_risk.value >= req_risk.value else req_risk
        # Criticality can also raise the effective risk floor (IRREVERSIBLE -> at least D).
        crit_floor = self._criticality_risk_floor(criticality)
        if crit_floor.value > effective_risk.value:
            effective_risk = crit_floor

        if effective_risk.value > identity.risk_class_ceiling.value:
            return PolicyDecision(
                decision=Decision.DENY,
                determining_policy_id="floor.risk_ceiling_exceeded",
                tier_hit=None,
                risk_class=effective_risk,
                criticality_resolved=criticality,
                rule_id="risk-ceiling:effective-exceeds-ceiling",
                rationale=(
                    f"effective risk {effective_risk.name} exceeds identity ceiling "
                    f"{identity.risk_class_ceiling.name} for effect {effect_id!r} "
                    f"(criticality {criticality.name})"
                ),
            )

        # ---- Rule of Two. ---------------------------------------------------------------------
        untrusted_input = input_trust_label != TrustLabel.TRUSTED_AUDITED
        rot = RuleOfTwo(
            untrusted_input=untrusted_input,
            sensitive_capability=effect.sensitive_capability,
            state_change=effect.state_change,
        )
        if rot.triggered():
            hd = self.human_gate.request(
                effect_id,
                {
                    "action_id": envelope.action_id,
                    "args": args,
                    "criticality": criticality.name,
                    "risk_class": effective_risk.name,
                },
            )
            if hd == HumanDecision.APPROVE:
                return PolicyDecision(
                    decision=Decision.ALLOW_WITH_OBLIGATIONS,
                    determining_policy_id="floor.rule_of_two.human_approved",
                    risk_class=effective_risk,
                    criticality_resolved=criticality,
                    rule_id="rule-of-two:human-gate-approved",
                    obligations=("human-gate-approved", "raise-monitoring"),
                    rationale="Rule-of-Two held all 3 flags; human gate explicitly APPROVED",
                )
            return PolicyDecision(
                decision=Decision.ESCALATE,
                determining_policy_id="floor.rule_of_two.escalate",
                risk_class=effective_risk,
                criticality_resolved=criticality,
                rule_id="rule-of-two:human-gate-required",
                escalation_target=identity.escalation_did or self.governance_did,
                rationale=(
                    "Rule-of-Two held all 3 of {untrusted_input, sensitive_capability, "
                    "state_change}; human gate deny-by-default -> escalate and hold"
                ),
            )

        # ---- Risk-class human-oversight routing for C/D. --------------------------------------
        if effective_risk in (RiskClass.C, RiskClass.D):
            return PolicyDecision(
                decision=Decision.ESCALATE,
                determining_policy_id="floor.risk_class.human_oversight",
                risk_class=effective_risk,
                criticality_resolved=criticality,
                rule_id="risk-class:human-approval-required",
                escalation_target=identity.escalation_did or self.governance_did,
                rationale=(
                    f"effective risk {effective_risk.name} requires explicit human approval; "
                    "escalate and hold"
                ),
            )

        # ---- ALLOW. ---------------------------------------------------------------------------
        return PolicyDecision(
            decision=Decision.ALLOW,
            determining_policy_id="floor.allow.confined_and_within_ceiling",
            risk_class=effective_risk,
            criticality_resolved=criticality,
            rule_id="allow:grant-present-and-within-bounds",
            rationale=(
                "origin-valid, content-unverified: grant present, within risk ceiling, "
                "Rule-of-Two not triggered"
            ),
        )

    # -- helpers ---------------------------------------------------------------------------------

    @staticmethod
    def _hint_to_criticality(args: dict, envelope: WorkerOutputEnvelope) -> typing.Optional[Criticality]:
        """Read an advisory criticality_hint from the envelope action (never authoritative).

        The hint can only RAISE the resolved criticality, never lower it (handled by the caller).
        """
        hint = None
        action = getattr(envelope, "action", None)
        if action is not None and getattr(action, "criticality_hint", None):
            hint = action.criticality_hint
        if hint is None and isinstance(args, dict):
            hint = args.get("criticality_hint")
        if not hint:
            return None
        try:
            return Criticality[str(hint).upper()]
        except KeyError:
            # Unknown hint string -> fail up to the maximum.
            return Criticality.IRREVERSIBLE

    @staticmethod
    def _criticality_risk_floor(criticality: Criticality) -> RiskClass:
        """Map a resolved criticality to the minimum risk class it forces (fail-safe asymmetry)."""
        return {
            Criticality.ROUTINE: RiskClass.A,
            Criticality.SENSITIVE: RiskClass.B,
            Criticality.CRITICAL: RiskClass.C,
            Criticality.IRREVERSIBLE: RiskClass.D,
        }[criticality]
