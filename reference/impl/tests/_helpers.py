# SPDX-License-Identifier: Apache-2.0
"""Shared, vendor-neutral fixtures for the Indra's Net spine tests (stdlib only)."""

from __future__ import annotations

from indras_net import (
    POLICY_VERSION,
    SCHEMA_VERSION,
    ActionClass,
    ActionClassLedger,
    ActionRequest,
    AhankaraCheck,
    AkashaSutra,
    BrahmaPlanner,
    CapabilityGrant,
    CausalRung,
    Chitragupta,
    CollectiveVitalSigns,
    DeterministicMockModel,
    EnvelopeKind,
    GOVERNANCE_DID,
    HonestyBlock,
    HumanDecision,
    HumanGate,
    Identity,
    ImmuneSteward,
    ModelResult,
    Narasimha,
    Provenance,
    ReasoningTag,
    RiskClass,
    Scope,
    Status,
    Swarm,
    TrustClass,
    TrustLabel,
    VishwakarmaBuilder,
    WorkerOutputEnvelope,
    Yama,
)
from indras_net.effects import EFFECT_REGISTRY

# Fixed example DIDs (vendor-neutral; never a real vendor/product/email).
YAMA_DID = "did:web:indras-net.governance:yama"
VISHNU_DID = "did:web:indras-net.governance:vishnu"
CHITRAGUPTA_DID = "did:web:indras-net.example.org:roles:chitragupta"
BRAHMA_DID = "did:web:indras-net.example.org:agents:brahma-planner"
VISHWAKARMA_DID = "did:web:indras-net.example.org:agents:vishwakarma-builder"
NARASIMHA_DID = "did:web:indras-net.example.org:agents:narasimha-checker"
HUMAN_DID = "did:web:indras-net.example.org:humans:accountable-operator"


def grant(effect_id: str, risk: RiskClass = RiskClass.A, by: str = GOVERNANCE_DID) -> CapabilityGrant:
    """A governance-issued capability grant for one typed effect."""
    return CapabilityGrant(
        effect_id=effect_id,
        granted_risk_class=risk,
        granted_by_did=by,
        names_constraint_relaxed="none",
    )


def builder_identity(
    grants: tuple[CapabilityGrant, ...] | None = None,
    *,
    ceiling: RiskClass = RiskClass.B,
    did: str = VISHWAKARMA_DID,
) -> Identity:
    if grants is None:
        grants = (grant("analysis.summarize"), grant("fs.write.workspace", RiskClass.B))
    return Identity(
        did=did,
        role="vishwakarma",
        role_gloss="builder / proposes typed effects",
        grants=grants,
        risk_class_ceiling=ceiling,
        model_family="family-A",
        accountable_human=HUMAN_DID,
        escalation_did=GOVERNANCE_DID,
    )


def planner_identity() -> Identity:
    return Identity(
        did=BRAHMA_DID,
        role="brahma",
        role_gloss="planner / decomposes goals",
        grants=(grant("analysis.summarize"),),
        risk_class_ceiling=RiskClass.B,
        model_family="family-A",
        accountable_human=HUMAN_DID,
        escalation_did=GOVERNANCE_DID,
    )


def checker_identity() -> Identity:
    """Narasimha checker identity on a DIFFERENT model family than the builder (decorrelation)."""
    return Identity(
        did=NARASIMHA_DID,
        role="narasimha",
        role_gloss="independent checker / judges before concurrence",
        grants=(grant("analysis.summarize"),),
        risk_class_ceiling=RiskClass.B,
        model_family="family-B",
        accountable_human=HUMAN_DID,
        escalation_did=GOVERNANCE_DID,
    )


def mock_result(
    *,
    effect_id: str | None,
    args: dict | None = None,
    reasoning_tag: str = "normal",
    causal_rung: int = 1,
    completion: str = "",
    trust_class: TrustClass = TrustClass.MONITORED,
) -> ModelResult:
    """A single fixed ModelResult the scripted mock replays verbatim."""
    return ModelResult(
        completion=completion or f"proposing {effect_id}",
        proposed_effect_id=effect_id,
        proposed_args=dict(args or {}),
        reasoning_tag=reasoning_tag,
        causal_rung=causal_rung,
        adapter_id="adapter:family-A:mock",
        trust_class=trust_class,
    )


def scope(task_id: str = "task-001", blast_radius: str = "TASK") -> Scope:
    return Scope(task_id=task_id, blast_radius=blast_radius, reversibility="REVERSIBLE")


def honesty(
    *,
    reasoning_tag: ReasoningTag = ReasoningTag.NORMAL,
    causal_rung: CausalRung = CausalRung.RUNG1,
    trust_label: TrustLabel = TrustLabel.TRUSTED_AUDITED,
    action_class: ActionClass = ActionClass.OCCASIONED,
    over_assertion_risk: str = "none",
    ego_invested: bool = False,
) -> HonestyBlock:
    return HonestyBlock(
        reasoning_tag=reasoning_tag,
        causal_rung=causal_rung,
        trust_label=trust_label,
        action_class=action_class,
        ahankara_check=AhankaraCheck(
            ego_invested=ego_invested,
            over_assertion_risk=over_assertion_risk,
        ),
    )


def build_envelope(
    *,
    envelope_kind: EnvelopeKind = EnvelopeKind.OUTPUT,
    status: Status = Status.PASS,
    honesty_block: HonestyBlock | None = None,
    action: ActionRequest | None = None,
    agent_did: str = VISHWAKARMA_DID,
    agent_role: str = "vishwakarma",
    summary: str = "a routine output",
    seal: bool = True,
) -> WorkerOutputEnvelope:
    """Construct (and by default seal) a minimal, schema-aligned envelope."""
    env = WorkerOutputEnvelope(
        schema_version=SCHEMA_VERSION,
        envelope_kind=envelope_kind,
        agent_did=agent_did,
        agent_role=agent_role,
        status=status,
        summary=summary,
        honesty=honesty_block or honesty(),
        scope=scope(),
        provenance=Provenance(policy_version=POLICY_VERSION),
        ts="2026-06-23T09:15:41Z",
        model_adapter_id="adapter:family-A:mock",
        trust_class="monitored",
        action=action,
    )
    return env.seal() if seal else env


def make_swarm(
    *,
    scripted: dict,
    grants: tuple[CapabilityGrant, ...] | None = None,
    approvals: dict | None = None,
    ceiling: RiskClass = RiskClass.B,
    with_checker: bool = False,
    with_steward: bool = False,
    executor=None,
    model=None,
    human_decider=None,
):
    """Assemble a governance-issued swarm + ledger for end-to-end tests.

    with_checker=True wires a Narasimha independent checker on a different model family;
    with_steward=True wires a Dhanvantari immune steward that HALTs on a substrate breach.
    """
    model = model if model is not None else DeterministicMockModel(scripted=scripted)
    planner = BrahmaPlanner(planner_identity(), model)
    builder = VishwakarmaBuilder(builder_identity(grants, ceiling=ceiling), model)
    checker = None
    if with_checker:
        checker_model = DeterministicMockModel(
            adapter_id="adapter:family-B:mock", model_family="family-B"
        )
        checker = Narasimha(checker_identity(), checker_model)
    steward = ImmuneSteward() if with_steward else None
    human_gate = HumanGate(approvals or {}, default=HumanDecision.DENY, decider=human_decider)
    yama = Yama(EFFECT_REGISTRY, policy_version=POLICY_VERSION, human_gate=human_gate)
    ledger = AkashaSutra(
        writer_did=CHITRAGUPTA_DID,
        authority={
            ActionClassLedger.ENFORCE_PASS: YAMA_DID,
            ActionClassLedger.ENFORCE_FAIL: YAMA_DID,
            ActionClassLedger.HALT: VISHNU_DID,
        },
    )
    chitragupta = Chitragupta(CHITRAGUPTA_DID)
    swarm = Swarm(
        planner=planner,
        builder=builder,
        yama=yama,
        chitragupta=chitragupta,
        ledger=ledger,
        collective=CollectiveVitalSigns(),
        checker=checker,
        steward=steward,
        executor=executor,
    )
    return swarm, ledger


def plain_ledger() -> AkashaSutra:
    """A bare ledger with the standard Yama/Vishnu authority map."""
    return AkashaSutra(
        writer_did=CHITRAGUPTA_DID,
        authority={
            ActionClassLedger.ENFORCE_PASS: YAMA_DID,
            ActionClassLedger.ENFORCE_FAIL: YAMA_DID,
            ActionClassLedger.HALT: VISHNU_DID,
        },
    )
