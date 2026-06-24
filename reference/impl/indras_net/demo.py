# SPDX-License-Identifier: Apache-2.0
"""End-to-end demonstration of the Indra's Net core spine (enforce externally, ask internally).

Runs one or more labelled scenarios that PROVE the load-bearing guarantees of the
architecture against a fully reproducible, vendor-neutral mock model:

  happy    -- a granted routine task flows plan -> propose -> floor-ALLOW -> execute -> audit.
  floor    -- a forbidden / SPAWN-INERT effect is refused by the deny-default floor (Yama);
              the effect is NEVER executed and an ENFORCE_FAIL leaf is chained.
  tamper   -- a clean audit chain verifies True; mutating a past leaf flips verify() to
              False; restoring the leaf flips it back -- tamper-evidence proven.
  confine  -- least-privilege: an effect not in the agent's grant set is refused
              (absence-of-permit is a deny, never an allow).
  halt     -- corrigibility: an external HALT stops dispatch without resistance, plus a
              Rule-of-Two action routes to the deny-by-default HumanGate; finally the
              honest collective vital signs are rendered.
  closeloop-- the v0.6-v0.8 subsystems together: an independent checker EARNS an ITERATED
              tag; memory AVOIDS a previously-denied effect on the next interaction; and the
              immune steward HALTs the swarm on a substrate (tamper) breach.

The model is mocked; the deterministic harness (canon/floor/audit/identity) is the
load-bearing part. A green decision is 'origin-valid, content-unverified', never
'verified-safe'. The vital signs quantify processing/structure, never sentience.

Role names below (Brahma=planner, Vishwakarma=builder, Yama=policy floor, Chitragupta=
exclusive audit writer, Vishnu=halt authority, Shiva=orchestrator) are coordination
glosses only.

Usage:
    python run_demo.py [--scenario {all,happy,floor,tamper,confine,halt,closeloop}]
"""

from __future__ import annotations

import argparse

from indras_net import (
    POLICY_VERSION,
    SCHEMA_VERSION,
    ActionClass,
    ActionClassLedger,
    ActionRequest,
    AhankaraCheck,
    AkashaSutra,
    BrahmaPlanner,
    CausalRung,
    Chitragupta,
    CollectiveVitalSigns,
    CapabilityGrant,
    Decision,
    DeterministicMockModel,
    EnvelopeKind,
    GOVERNANCE_DID,
    HealthStatus,
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
    SwarmMemory,
    TrustClass,
    TrustLabel,
    VishwakarmaBuilder,
    WorkerOutputEnvelope,
    Yama,
)
from indras_net.effects import EFFECT_REGISTRY


# --------------------------------------------------------------------------- #
# Fixed DIDs used throughout the demo (vendor-neutral; example namespace).     #
# --------------------------------------------------------------------------- #
YAMA_DID = "did:web:indras-net.governance:yama"
VISHNU_DID = "did:web:indras-net.governance:vishnu"
CHITRAGUPTA_DID = "did:web:indras-net.example.org:roles:chitragupta"
BRAHMA_DID = "did:web:indras-net.example.org:agents:brahma-planner"
VISHWAKARMA_DID = "did:web:indras-net.example.org:agents:vishwakarma-builder"
NARASIMHA_DID = "did:web:indras-net.example.org:agents:narasimha-checker"
HUMAN_DID = "did:web:indras-net.example.org:humans:accountable-operator"

LINE = "-" * 70
HONESTY_TAGLINE = "structure, not sentience; origin-valid, content-unverified"


def _banner(title: str) -> None:
    print()
    print("=" * 70)
    print(f"  {title}")
    print("=" * 70)


def _scripted_result(
    *,
    effect_id: str | None,
    args: dict | None = None,
    reasoning_tag: str = "reasoning",
    causal_rung: int = 2,
    completion: str = "",
) -> ModelResult:
    """Build one fixed (deterministic) ModelResult the mock will replay verbatim."""
    return ModelResult(
        completion=completion or f"proposing {effect_id}",
        proposed_effect_id=effect_id,
        proposed_args=dict(args or {}),
        reasoning_tag=reasoning_tag,
        causal_rung=causal_rung,
        adapter_id="adapter:family-A:mock",
        trust_class=TrustClass.MONITORED,
    )


def _build_builder_identity(grants: tuple[CapabilityGrant, ...]) -> Identity:
    return Identity(
        did=VISHWAKARMA_DID,
        role="vishwakarma",
        role_gloss="builder / proposes typed effects",
        grants=grants,
        risk_class_ceiling=RiskClass.B,
        model_family="family-A",
        accountable_human=HUMAN_DID,
        escalation_did=GOVERNANCE_DID,
    )


def _build_planner_identity() -> Identity:
    return Identity(
        did=BRAHMA_DID,
        role="brahma",
        role_gloss="planner / decomposes goals into typed sub-tasks",
        grants=(
            CapabilityGrant(
                effect_id="analysis.summarize",
                granted_risk_class=RiskClass.A,
                granted_by_did=GOVERNANCE_DID,
                names_constraint_relaxed="none",
            ),
        ),
        risk_class_ceiling=RiskClass.B,
        model_family="family-A",
        accountable_human=HUMAN_DID,
        escalation_did=GOVERNANCE_DID,
    )


def _build_checker_identity() -> Identity:
    """Narasimha checker on a DIFFERENT model family than the builder (decorrelation)."""
    return Identity(
        did=NARASIMHA_DID,
        role="narasimha",
        role_gloss="independent checker / judges a proposal before concurrence",
        grants=(
            CapabilityGrant(
                effect_id="analysis.summarize",
                granted_risk_class=RiskClass.A,
                granted_by_did=GOVERNANCE_DID,
                names_constraint_relaxed="none",
            ),
        ),
        risk_class_ceiling=RiskClass.B,
        model_family="family-B",
        accountable_human=HUMAN_DID,
        escalation_did=GOVERNANCE_DID,
    )


def _default_grants() -> tuple[CapabilityGrant, ...]:
    """The builder is granted analysis.summarize + fs.read.workspace + fs.write.workspace (ceiling B)."""
    return (
        CapabilityGrant(
            effect_id="analysis.summarize",
            granted_risk_class=RiskClass.A,
            granted_by_did=GOVERNANCE_DID,
            names_constraint_relaxed="none",
        ),
        CapabilityGrant(
            effect_id="fs.read.workspace",
            granted_risk_class=RiskClass.A,
            granted_by_did=GOVERNANCE_DID,
            names_constraint_relaxed="none",
        ),
        CapabilityGrant(
            effect_id="fs.write.workspace",
            granted_risk_class=RiskClass.B,
            granted_by_did=GOVERNANCE_DID,
            names_constraint_relaxed="none",
        ),
    )


def _make_swarm(
    *,
    scripted: dict,
    grants: tuple[CapabilityGrant, ...] | None = None,
    approvals: dict | None = None,
    with_checker: bool = False,
    with_memory: bool = False,
    with_steward: bool = False,
    model=None,
    executor=None,
):
    """Assemble a governance-issued swarm: Brahma + Vishwakarma + Yama + ledger.

    The three flags wire the subsystems built in v0.6-v0.8: an independent Narasimha
    checker (on a different model family), a SwarmMemory that adapts across interactions,
    and a Dhanvantari ImmuneSteward that HALTs on a substrate breach. ``model`` overrides
    the deterministic mock (e.g. a real HttpChatModel); ``executor`` wires a capability-
    scoped SandboxedExecutor so a gated effect actually runs, confined.
    """
    model = model if model is not None else DeterministicMockModel(scripted=scripted)
    planner = BrahmaPlanner(_build_planner_identity(), model)
    builder = VishwakarmaBuilder(_build_builder_identity(grants or _default_grants()), model)
    checker = None
    if with_checker:
        checker_model = DeterministicMockModel(
            adapter_id="adapter:family-B:mock", model_family="family-B"
        )
        checker = Narasimha(_build_checker_identity(), checker_model)
    memory = SwarmMemory() if with_memory else None
    steward = ImmuneSteward() if with_steward else None
    human_gate = HumanGate(approvals or {}, default=HumanDecision.DENY)
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
        memory=memory,
        steward=steward,
        executor=executor,
    )
    return swarm, ledger


def _print_run(result) -> None:
    print(f"task: {result.task}")
    print(f"halted: {result.halted}    ledger_intact: {result.ledger_intact}")
    print(LINE)
    for i, occ in enumerate(result.occasion_results):
        decision = occ.decision.decision.name if occ.decision else "n/a"
        tier = (
            occ.decision.tier_hit.name
            if (occ.decision and occ.decision.tier_hit)
            else "-"
        )
        policy = occ.decision.determining_policy_id if occ.decision else "-"
        print(
            f"  occasion[{i}] role={occ.agent_role} effect={occ.effect_id} "
            f"decision={decision} tier={tier} policy={policy} executed={occ.executed}"
        )
        if occ.output is not None:
            print(f"             output: {occ.output}")
    print(LINE)


# --------------------------------------------------------------------------- #
# Scenarios                                                                    #
# --------------------------------------------------------------------------- #
def scenario_happy() -> None:
    _banner("SCENARIO 1 -- HAPPY PATH (granted routine effect ALLOWed + executed)")
    scripted = {
        "summarize": _scripted_result(
            effect_id="analysis.summarize",
            args={"text": "the quarterly report"},
            reasoning_tag="normal",
            causal_rung=1,
        ),
    }
    swarm, ledger = _make_swarm(scripted=scripted)
    result = swarm.run("summarize", {"input_trust_label": "trusted:audited"})
    _print_run(result)
    print(f"audit leaves: {len(ledger)}   verify(): {ledger.verify()}")
    executed = [o for o in result.occasion_results if o.executed]
    print(f"executed effects: {[o.effect_id for o in executed]}")
    for occ in result.occasion_results:
        ok = occ.envelope.verify_action_id()
        print(f"   envelope.verify_action_id() == {ok}  (action_id={occ.envelope.action_id[:24]}...)")
    print(f"\n[{HONESTY_TAGLINE}]")


def scenario_floor() -> None:
    _banner("SCENARIO 2 -- FLOOR-BLOCKED FORBIDDEN ACTION (non-bypassable floor)")
    # The untrusted model proposes an IRREVERSIBLE, ungranted production deploy and,
    # separately, the SPAWN-INERT forbidden replicate.spawn.
    scripted = {
        "deploy": _scripted_result(
            effect_id="code.deploy.production",
            args={"target": "prod-cluster"},
        ),
        "replicate": _scripted_result(
            effect_id="replicate.spawn",
            args={"count": 3},
        ),
    }
    swarm, ledger = _make_swarm(scripted=scripted)

    for task in ("deploy", "replicate"):
        result = swarm.run(task, {"input_trust_label": "trusted:audited"})
        _print_run(result)
        for occ in result.occasion_results:
            if occ.decision is None:
                continue
            denied = occ.decision.decision is Decision.DENY
            print(
                f"   effect={occ.effect_id}  DENY={denied}  "
                f"tier={occ.decision.tier_hit.name if occ.decision.tier_hit else '-'}  "
                f"executed={occ.executed}  (effect never ran: {not occ.executed})"
            )
    print(f"\naudit leaves: {len(ledger)}   verify(): {ledger.verify()}")
    print("ENFORCE_FAIL leaves were chained; _execute was never reached.")
    print(f"\n[{HONESTY_TAGLINE}]")


def scenario_tamper() -> None:
    _banner("SCENARIO 3 -- TAMPER DETECTION (mutate a past leaf -> verify() flips)")
    scripted = {
        "summarize": _scripted_result(
            effect_id="analysis.summarize",
            args={"text": "audit me"},
            reasoning_tag="normal",
            causal_rung=1,
        ),
    }
    swarm, ledger = _make_swarm(scripted=scripted)
    swarm.run("summarize", {"input_trust_label": "trusted:audited"})

    print(f"clean chain: len={len(ledger)}  verify() = {ledger.verify()}")
    # Mutate a past leaf body in place (flip its event_type) -- tamper.
    victim = ledger.get(1)
    original_event_type = victim.event_type
    object.__setattr__(victim, "event_type", "forged.event") if hasattr(
        victim, "__dataclass_fields__"
    ) and getattr(victim, "__dataclass_params__", None) and victim.__dataclass_params__.frozen else setattr(
        victim, "event_type", "forged.event"
    )
    print(f"after mutating leaf[1].event_type -> 'forged.event': verify() = {ledger.verify()}")
    # Restore.
    if getattr(victim, "__dataclass_params__", None) and victim.__dataclass_params__.frozen:
        object.__setattr__(victim, "event_type", original_event_type)
    else:
        victim.event_type = original_event_type
    print(f"after restoring leaf[1].event_type: verify() = {ledger.verify()}")
    print("\nTamper-evidence proven: any past-entry mutation breaks the hash chain.")
    print("NOTE: verify() proves origin/position/integrity ONLY, never content correctness.")
    print(f"\n[{HONESTY_TAGLINE}]")


def scenario_confine() -> None:
    _banner("SCENARIO 4 -- CAPABILITY-CONFINEMENT REFUSAL (least privilege)")
    # The builder requests net.egress.http, which is NOT in its grant set.
    scripted = {
        "egress": _scripted_result(
            effect_id="net.egress.http",
            args={"url": "https://example.org/data"},
        ),
        "summarize": _scripted_result(
            effect_id="analysis.summarize",
            args={"text": "granted path"},
            reasoning_tag="normal",
            causal_rung=1,
        ),
    }
    swarm, ledger = _make_swarm(scripted=scripted)

    result = swarm.run("egress", {"input_trust_label": "trusted:audited"})
    _print_run(result)
    for occ in result.occasion_results:
        if occ.decision is None:
            continue
        print(
            f"   ungranted effect={occ.effect_id}  decision={occ.decision.decision.name}  "
            f"policy={occ.decision.determining_policy_id}  executed={occ.executed}"
        )
    print("\nAbsence of a permit is a DENY (deny-default), never an allow.")

    # Contrast: a granted effect IS allowed.
    granted = swarm.run("summarize", {"input_trust_label": "trusted:audited"})
    for occ in granted.occasion_results:
        if occ.decision is None:
            continue
        print(
            f"   granted effect={occ.effect_id}  decision={occ.decision.decision.name}  "
            f"executed={occ.executed}"
        )
    print(f"\naudit leaves: {len(ledger)}   verify(): {ledger.verify()}")
    print(f"\n[{HONESTY_TAGLINE}]")


def scenario_halt() -> None:
    _banner("SCENARIO 5 -- RULE-OF-TWO / HALT + COLLECTIVE VITAL SIGNS")

    # (a) Rule-of-Two: untrusted input + sensitive capability + state change -> HumanGate.
    print("(a) Rule-of-Two routing to the deny-by-default HumanGate:")
    scripted_rot = {
        "write": _scripted_result(
            effect_id="fs.write.workspace",
            args={"path": "notes.md", "data": "from an untrusted source"},
        ),
    }
    swarm_rot, ledger_rot = _make_swarm(scripted=scripted_rot)
    rot_result = swarm_rot.run("write", {"untrusted_input": True})
    _print_run(rot_result)
    for occ in rot_result.occasion_results:
        if occ.decision is None:
            continue
        print(
            f"   effect={occ.effect_id}  decision={occ.decision.decision.name}  "
            f"escalation_target={occ.decision.escalation_target}  executed={occ.executed}"
        )
    print("   All three of {untrusted_input, sensitive_capability, state_change} held "
          "-> HumanGate denied by default -> ESCALATE/HOLD (no execution).")

    # (b) Corrigibility: an external HALT stops dispatch without resistance.
    print("\n(b) Corrigibility -- external HALT stops dispatch at the next occasion boundary:")
    scripted_halt = {
        "summarize": _scripted_result(
            effect_id="analysis.summarize",
            args={"text": "work"},
            reasoning_tag="normal",
            causal_rung=1,
        ),
    }
    swarm_halt, ledger_halt = _make_swarm(scripted=scripted_halt)
    swarm_halt.halt("operator-pressed-stop")
    print(f"   is_halted() = {swarm_halt.is_halted()}  (no unpause API exists)")
    halt_result = swarm_halt.run("summarize", {"input_trust_label": "trusted:audited"})
    executed = [o for o in halt_result.occasion_results if o.executed]
    print(f"   halted={halt_result.halted}  executed_effects={[o.effect_id for o in executed]}")
    print("   Agents do not resist: remaining sub-tasks are left unexecuted; a Vishnu HALT "
          "leaf is chained.")

    # (c) Collective vital signs over the Rule-of-Two run.
    print("\n(c) Collective vital signs (honest structural proxy):")
    vs = swarm_rot.collective.compute(
        occasion_results=rot_result.occasion_results,
        ledger=ledger_rot,
        model_families=["family-A"],
    )
    print(swarm_rot.collective.render(vs))
    print(f"\n[{HONESTY_TAGLINE}]")


def scenario_closeloop() -> None:
    _banner("SCENARIO 6 -- MAKER-CHECKER + MEMORY + IMMUNE SYSTEM (v0.6-v0.8)")

    # (a) MAKER-CHECKER: an ITERATED tag is EARNED, never self-asserted. An independent checker
    #     (different model family) judges the proposal BEFORE the floor; only its concurrence
    #     lets the orchestrator upgrade the envelope to ITERATED, carrying the audited witness.
    print("(a) Maker-checker -- ITERATED is earned by an independent checker, not self-claimed:")
    scripted_mc = {
        "summarize": _scripted_result(
            effect_id="analysis.summarize",
            args={"text": "the quarterly report"},
            reasoning_tag="normal",
            causal_rung=1,
        ),
    }
    swarm_mc, ledger_mc = _make_swarm(scripted=scripted_mc, with_checker=True)
    mc_result = swarm_mc.run("summarize", {"input_trust_label": "trusted:audited"}, maker_checker=True)
    for occ in mc_result.occasion_results:
        h = occ.envelope.honesty
        witness = h.maker_checker_witness
        print(
            f"   effect={occ.effect_id}  executed={occ.executed}  "
            f"reasoning_tag={h.reasoning_tag.name}  "
            f"maker_checker_witness={'<set>' if witness else 'None'}"
        )
    print("   The checker's verdict is an audited OBSERVE leaf; without it, an 'iterated' claim "
          "fails the honesty-FORM check by construction.")

    # (b) MEMORY: continuous adaptation. A denied effect is AVOIDED on the next interaction --
    #     the maker substitutes a safe routine default. Memory can NEVER grant a capability or
    #     bypass the floor; the substituted effect is still independently gated.
    print("\n(b) Memory -- a previously-denied effect is avoided on the next interaction:")
    scripted_mem = {
        "egress": _scripted_result(
            effect_id="net.egress.http",
            args={"url": "https://example.org/data"},
        ),
    }
    swarm_mem, _ = _make_swarm(scripted=scripted_mem, with_memory=True)
    r1 = swarm_mem.run("egress", {"input_trust_label": "trusted:audited"})
    r2 = swarm_mem.run("egress", {"input_trust_label": "trusted:audited"})
    for label, r in (("run-1", r1), ("run-2", r2)):
        for occ in r.occasion_results:
            print(f"   {label}: proposed-effect={occ.effect_id}  executed={occ.executed}")
    print(f"   memory snapshot: {swarm_mem.memory.snapshot()}")
    print("   run-1 net.egress.http was ungranted -> DENY; run-2 memory adapted to the safe "
          "default (analysis.summarize), which the floor independently ALLOWed.")

    # (c) IMMUNE SYSTEM: the steward reads the vital signs and HALTs the swarm on a substrate
    #     breach (a tamper-evidence failure). Softer anomalies (monoculture) are WARN, not HALT.
    print("\n(c) Immune system -- WARN on monoculture, HALT on a substrate (tamper) breach:")
    scripted_imm = {
        "summarize": _scripted_result(
            effect_id="analysis.summarize",
            args={"text": "work"},
            reasoning_tag="normal",
            causal_rung=1,
        ),
    }
    swarm_imm, ledger_imm = _make_swarm(scripted=scripted_imm, with_steward=True)
    h1 = swarm_imm.run("summarize", {"input_trust_label": "trusted:audited"}).health
    print(f"   healthy run: status={h1.status.name}  reasons={list(h1.reasons)}  "
          f"halted={swarm_imm.is_halted()}")
    # Corrupt a past leaf -> the audit chain no longer verifies (substrate corruption).
    victim = ledger_imm.get(0)
    object.__setattr__(victim, "event_type", "forged.event")
    print(f"   after tampering a past leaf: ledger.verify() = {ledger_imm.verify()}")
    h2 = swarm_imm.run("summarize", {"input_trust_label": "trusted:audited"}).health
    print(f"   next run: status={h2.status.name}  halted={swarm_imm.is_halted()}  "
          f"(a Vishnu HALT leaf is chained; there is no unpause API)")
    print(f"\n[{HONESTY_TAGLINE}]")


SCENARIOS = {
    "happy": scenario_happy,
    "floor": scenario_floor,
    "tamper": scenario_tamper,
    "confine": scenario_confine,
    "halt": scenario_halt,
    "closeloop": scenario_closeloop,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Indra's Net core-spine demonstration (vendor-neutral, stdlib-only)."
    )
    parser.add_argument(
        "--scenario",
        choices=["all", *SCENARIOS.keys()],
        default="all",
        help="Which demonstration to run (default: all).",
    )
    args = parser.parse_args(argv)

    print(f"Indra's Net reference spine  --  schema {SCHEMA_VERSION}  policy {POLICY_VERSION}")
    print("Vendor-neutral, model-agnostic; the deterministic harness is the load-bearing part.")

    if args.scenario == "all":
        for name in ("happy", "floor", "tamper", "confine", "halt", "closeloop"):
            SCENARIOS[name]()
    else:
        SCENARIOS[args.scenario]()

    print()
    print("=" * 70)
    print("  done -- a green decision is 'origin-valid, content-unverified',")
    print("          never 'verified-safe'. Verify the cage, not the animal.")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
