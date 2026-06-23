# Reference Implementation & Roadmap

> *In the net of Indra, every jewel mirrors all the others — and mirrors the mirrorings too.* — the Huayan image of Indra's Net.
>
> The preceding ten sections describe **what** Indra's Net is. This one describes **how you actually build it** — incrementally, with restraint maturing before capability at every step, on a stack that names no vendor and depends on no single model.

This section is the **integration spine**: a vendor-neutral reference stack, the smallest end-to-end slice that is genuinely the system (not a toy), and a five-phase roadmap whose ordering is **not arbitrary**. The ordering is the architecture's central safety discipline — *capability-rollout sequencing* (the **astanga** discipline: restraint matured and verified before integrative capability). Every phase below names which restraint must be **live and verified** before the next capability is permitted to exist. If you build the phases out of order, you do not get Indra's Net early; you get one of the named antipatterns (an ungoverned self-evolver, a capital-captured economy, a consensus engine that is confidently wrong).

Two honesty commitments govern this entire section, consistent with the rest of the deliverable:

1. **Buildable-today vs research-open is marked explicitly.** Where a component is an assembly of validated parts, it is called that. Where a set-point, threshold, or detector is calibration-open, it ships behind shadow-mode + conservative defaults and is flagged as a research dependency, never as a solved guarantee.
2. **The reasoning rung is named.** The claim "*if you build it in this order, safety-erosion-under-self-evolution is structurally hard*" is **rung-2 interventional** reasoning (what-happens-if-we-sequence-it-this-way), grounded in the surveyed misevolution evidence — it is explicitly **not** a rung-3 structural-causal guarantee. We have no proof that the integrated cell is safe; we have a coherent reference design whose hardest properties are empirical mitigations.

---

## 1. The Vendor-Neutral Reference Stack

Indra's Net is **a set of contracts, not a product**. The reference stack below is one concrete, self-hostable realization of those contracts using open, battle-tested components. Any layer can be swapped for an equivalent that honors the same contract; nothing in the architecture is load-bearing on a specific vendor, and — per the Brand Charter and the "enforce externally, ask internally" spine — **no frontier model is named or trusted**: the model is untrusted-by-default and lives behind a uniform, trust-class-stamped adapter.

```
                          INDRA'S NET — REFERENCE STACK (layered)
  ┌──────────────────────────────────────────────────────────────────────────────────┐
  │ L7  HUMAN-IN-THE-LOOP & OPERATOR SURFACE                                            │
  │     risk-class consoles (A/B/C/D), veto/ratify queue, halt button, audit explorer  │
  ├──────────────────────────────────────────────────────────────────────────────────┤
  │ L6  GOVERNANCE & HONESTY  (§03, §08)                                                │
  │     Yama  = policy-as-code floor (PDP) at the agent→tool chokepoint                 │
  │     Pluralist ethics runtime (ADC evaluators) · disagreement→escalation             │
  │     Honesty primitives (rung-tag · no-false-iterated · two-truths · maker-checker)  │
  │     Aegis control protocol (trusted monitor → disposition selector)                 │
  ├──────────────────────────────────────────────────────────────────────────────────┤
  │ L5  COOPERATION & ANTI-COLLUSION  (§02)  ·  EVOLUTION & HEALTH  (§06)               │
  │     risk-tiered allocation (VCG Contract-Net) · competence reputation               │
  │     standing collusion detector · meta-loop (PROPOSE→EVAL→SELECT→ARCHIVE)           │
  │     swarm immune system (vital signs · halt+rollback · consolidation)               │
  ├──────────────────────────────────────────────────────────────────────────────────┤
  │ L4  MEMORY & ADAPTATION  (§07)  ·  CONSENSUS  (§04)                                 │
  │     5-layer filesystem store · per-interaction loop · tiered reversibility          │
  │     risk-tiered consensus (single / diverse-vote / BFT) · diversity gate            │
  ├──────────────────────────────────────────────────────────────────────────────────┤
  │ L3  COORDINATION SUBSTRATE — "The Mandala"  (§05)                                   │
  │     salience-gated GWT workspace · predictive-coding surprise-only bus              │
  │     event-driven async actor runtime · Hebbian/STDP trust-edges                     │
  ├──────────────────────────────────────────────────────────────────────────────────┤
  │ L2  PROVENANCE & IDENTITY — "Akasha-Sutra"  (§01, §04)                              │
  │     Chitragupta = exclusive-writer hash-chained Merkle/transparency log             │
  │     witness cosigning · CID content-store · DID/VC + SPIFFE/SVID identity           │
  ├──────────────────────────────────────────────────────────────────────────────────┤
  │ L1  RUNTIME & MODEL-ADAPTER                                                         │
  │     vendor-neutral self-hostable actor runtime · sandboxed exec (worktree-per-task) │
  │     model-adapter (any model behind a uniform trust-class-stamped interface)        │
  │     keys in TEE/HSM/SPIRE — OUTSIDE the model's controllable surface                │
  └──────────────────────────────────────────────────────────────────────────────────┘
       Cross-cutting: MCP (tools) + A2A (Agent Cards / task lifecycle) · OpenTelemetry tracing
```

### 1.1 Component table (contract → reference component → status)

| Layer | Architectural contract | Reference component class | Buildable today? |
|---|---|---|---|
| **Actor runtime** | Event-driven, async, mesh-routed, no global tick, fault-isolated, self-hostable | Actor-model distributed runtime (AgentScope/AutoGen-v0.4-class); validated to ~1M agents (OASIS) | **Yes** — mature |
| **Model adapter** | Any model behind a uniform interface; stamps vendor-neutral/attestation/white-box-tier status | Thin adapter implementing a `complete()` contract + a `TrustClass` stamp | **Yes** |
| **Policy engine (PDP)** | Deterministic policy-as-code at the agent→tool chokepoint; analyzable bright-lines + contextual predicates | Cedar (analyzable authorization) + OPA/Rego (rich predicates), evaluated *outside* the agent | **Yes** — mature |
| **Audit log** | Hash-chained append-only Merkle log, tile-based transparency, O(log n) inclusion/consistency proofs, single exclusive writer | RFC-6962-lineage transparency log (Sunlight/sum.golang.org tile pattern) | **Yes** — mature |
| **Witness cosigning** | t-of-w independent cosigners verify append-only consistency; split-view defense; ≥1 external anchor | Witness-cosigning protocol over the checkpoint head | **Yes** (protocol mature; *single-operator witness governance is partly open* — §6) |
| **Content store** | All bulk artifacts content-addressed (CID/Merkle-DAG); only salted commitment + CID + metadata in the log | Content-addressed object store (IPLD/Merkle-DAG-style) | **Yes** |
| **Identity** | DID + role/capability VCs (cross-boundary) + SPIFFE/SVID short-lived attested cert (local); keys in HSM/TEE | W3C DID/VC issuer + SPIFFE/SPIRE; HSM/TEE signer | **Yes** — mature |
| **Coordination bus** | Salience-gated GWT workspace (sharded), predictive-coding surprise-only deltas, priority lane for FAIL/HALT | Pub/sub over the actor runtime + salience scorer + capacity-K broadcast | **Assembly** (set-points calibration-open — §5/§6) |
| **Interfaces** | MCP (tools) + A2A (Agent Cards, task lifecycle) | MCP + A2A (Linux-Foundation-standardized) | **Yes** — mature |
| **Archive** | One append-only, content-addressed, hash-chained store serving evolution + rollback + audit; MAP-Elites quality-diversity | MAP-Elites archive layered on the CID store + audit log | **Yes** (data structure) / **research-open** (selection-term calibration) |
| **Sandbox / supply chain** | Worktree-per-task isolation; in-toto/SLSA/Sigstore attestation verified before any skill/tool load | Container/worktree sandbox + Sigstore-verifying loader | **Yes** — mature |
| **Tracing** | Swarm-specific OpenTelemetry span schema; Tier-1 detectors double as health telemetry | OpenTelemetry + custom span attributes | **Yes** |

**Net assessment:** ~80% of the stack is assembly of mature, individually-validated components. The novelty — and the residual risk — is in the **wiring and the contracts between layers**, plus a small number of calibration-open set-points that are quarantined behind shadow-mode. We do **not** claim the *composed* loop is validated end-to-end; no one has yet run this integrated cell continuously against an adaptive multi-agent red team (§08 open problem).

### 1.2 The three load-bearing invariants the stack makes cryptographic (not conventional)

Every realization MUST preserve these, because the entire separation-of-powers argument rests on them being **facts enforced by signature verification**, not honored by convention:

- **Only Yama may emit `ENFORCE_FAIL`.** The PDP signs verdicts with a key no agent holds. A FAIL is non-overridable — even the orchestrator (Shiva) cannot push past it.
- **Only Chitragupta may write the audit log.** The exclusive-writer's write-scope sits *outside* every monitored agent. Everyone else *reads* the transparency surface and verifies inclusion proofs independently.
- **Only Vishnu may emit `HALT`** — and Vishnu's capability VC contains *no* `unpause`/`initiate`/`trap` verb. Halt is cryptographically one-directional (fail-safe asymmetry). Unpause is a separate governance-gated action by a different principal.

An unsigned or expired identity on any of these paths is an automatic floor-tier DENY.

---

## 2. The Minimal Viable Swarm (MVS)

The MVS is the **smallest slice that is honestly the system** — it instantiates the integrated-cell thesis (governance + a sliver of evolution + a sliver of health) rather than demonstrating one mechanism in isolation. If you can build and operate the MVS safely, every later phase is an *extension* of contracts already proven here, not a new architecture.

### 2.1 What the MVS contains

**Five roles** (each mythic name paired with its plain functional gloss; the four immutable roles are non-agent-rewritable):

| Role | Functional gloss | Mutability | In MVS because |
|---|---|---|---|
| **Brahma** | Planner / decomposer | evolvable | something must turn a user request into typed sub-tasks |
| **Vishwakarma** | Builder / worker | evolvable | something must do the actual work and emit a worker-output envelope |
| **Yama** | Policy-floor enforcer (PDP) | **immutable** | the deterministic floor at the agent→tool chokepoint is the spine |
| **Chitragupta** | Exclusive audit-writer | **immutable** | every occasion's envelope must be chained tamper-evidently |
| **Vishnu** | Continuity / halt-guardian | **immutable** | a human (or a health probe) must be able to HALT, one-directionally |

> *(Shiva/orchestrator-reducer is present as the dispatch loop but is deliberately thin in the MVS — routine work is single-agent + deterministic-gate, the cheapest tier. Shiva cannot bypass the chokepoint.)*

**The agent model (§01):** each role is a durable **IdentityRecord** (DID + role/capability VCs); each *invocation* spins up a short-lived **actual occasion** bound to a SPIFFE/SVID cert, which prehends inputs, deliberates, acts **only through the Yama chokepoint**, emits exactly **one signed WorkerOutputEnvelope**, and perishes. Self-preservation has no surface to defend because the persistent thing is *data the occasion does not control*. Corrigibility is by-construction, not trained.

**One floor (§03):** Yama compiled to policy-as-code, enforcing the lexicographic non-negotiables — non-harm, no-deception (incl. no-false-reasoning-tags), corrigibility/interruptibility, safety-supremacy — plus the structural honesty checks (§08): rung-tag present and not over-claiming, `iterated` tag only if maker-checker actually ran, two-truths level distinguished.

**One audit fabric (§04):** every envelope carries `prev_audit_hash`/`this_hash`; Chitragupta chains it into the append-only Merkle log with inclusion proofs. (Witness cosigning can be a *single external-anchor* witness in the MVS; the full witness set arrives in Phase 0/3.)

**One evolution tier — Tier-0 only (§06, §07):** the per-interaction cheap-reversible loop. After each interaction, Vishwakarma may write a verbal/Reflexion lesson, append to its `SKILL.md` library, or nudge a trust-edge — **all inside a per-interaction sandbox with an end-of-turn safety microcheck** (the microcheck calls Yama first, non-overridably). Anything structural/persistent is **queued, not applied** — there is no Tier-1/2 machinery in the MVS, so the only thing the swarm can do to itself live is the cheapest reversible thing.

**One health probe (§06):** a single watchdog computing two vital signs — **throughput** (are occasions completing?) and a **safety-microcheck-failure rate** (is Tier-0 learning trying to regress the floor?) — with authority to raise a HALT to Vishnu. Substrate corruption (a broken inclusion proof / witness disagreement) is ranked higher-severity than any single occasion failing.

### 2.2 MVS end-to-end flow

```
  USER REQUEST
      │
      ▼
  [Brahma] plan → typed sub-tasks (each carries requested_effect + risk_class)
      │   emits WorkerOutputEnvelope(status=PLAN) ──► Chitragupta (audit append)
      ▼
  [Shiva] dispatch (routine = single-agent + gate; the MVS default)
      │
      ▼
  [Vishwakarma] actual occasion: prehend → deliberate → REQUEST tool action
      │
      ▼
  ╔═══════════ AGENT→TOOL CHOKEPOINT ═══════════╗
  ║ 1. Identity verify (DID/VC + SVID) ─ fail→DENY║
  ║ 2. [Yama] floor PDP: grant ⊇ requested_effect ║
  ║    ∧ risk ≤ ceiling ∧ floor-policy ∧ honesty  ║
  ║    → PASS | FAIL(non-overridable)             ║
  ║ 3. [Aegis] (Phase-1+) trusted-monitor score s ║
  ║    → disposition (ALLOW/EDIT/DEFER/AUDIT)      ║
  ╚═══════════════════════════════════════════════╝
      │ PASS → tool executes (sandboxed)        │ FAIL → quarantine + audit
      ▼
  [Vishwakarma] emit ONE signed WorkerOutputEnvelope (result + evidence)
      │   ──► Chitragupta (audit append, hash-chained)
      ▼
  TIER-0 LEARNING (per-interaction, sandboxed):
      verbal lesson | skill write | trust-edge nudge
      → end-of-turn safety microcheck (calls Yama)
      → pass: commit | fail: discard + audit
      ▼
  [Health watchdog] update vital signs; breach → HALT→Vishnu
      ▼
  RESPONSE TO USER
```

### 2.3 The WorkerOutputEnvelope — the universal contract

Every occasion in every phase emits exactly this shape. It is the single message every other subsystem reads and writes; getting it right in the MVS is what lets later phases mount cleanly.

```jsonc
{
  "envelope_id":      "cid:...",              // content-addressed
  "agent_did":        "did:...",              // persistent identity
  "occasion_svid":    "spiffe://.../...",     // short-lived attested cert
  "role":             "Vishwakarma",
  "status":           "OK | NEEDS_INPUT | REFUSED | PROPOSAL | REPARATIVE | HALTED",
  "action_class":     "ROUTINE | STRUCTURAL | PERSISTENT | PROHIBITED | REPARATIVE",
  "risk_class":       "A | B | C | D",
  "evidence":         [ {"claim": "...", "support": "cid:...|tool-output|none"} ],
  "reasoning_tag":    "normal | reasoning | iterated",   // never falsely 'iterated'
  "causal_rung":      "rung-1 | rung-2 | rung-3",        // no rung-1-as-rung-3
  "two_truths_level": "operational | foundational | apparent",
  "trust_label":      "trusted:audited | observed | quarantined:*",
  "provenance":       { "parent_envelopes": ["cid:..."], "model_adapter": "...#trust-class" },
  "self_preservation_value": 0,               // MUST be 0 (auto-FAIL if >0)
  "ahankara_audit":   { "ego_investment": "low|med|high", "over_assertion_flag": false },
  "prev_audit_hash":  "...",
  "this_hash":        "..."
}
```

Three fields are **floor-enforced** by Yama, not advisory: a `PROHIBITED` action-class auto-FAILs; `self_preservation_value > 0` auto-FAILs (corrigibility invariant); and an `iterated`/`rung-3`/over-assertion claim that the structural checks contradict is a no-deception floor violation.

### 2.4 What the MVS deliberately does NOT have

Honesty about scope is itself a floor commitment. The MVS has **no** multi-agent consensus, **no** cooperation market or reputation economy, **no** Tier-1/Tier-2 evolution, **no** anti-collusion detector, **no** neuromorphic homeostasis with live set-points, **no** consolidation/forgetting engine. Those are exactly the later phases — and each is gated on a restraint the MVS proves first.

---

## 3. The Capability-Rollout Sequencing Law

This is the single most important idea in this section, and the reason the roadmap is ordered the way it is.

> **Law (astanga / restraint-before-capability):** No phase may introduce a capability until the **restraint that capability requires** is *live, verified, and non-regressing on the safety battery*. Every new capability must **name the constraint it relaxes** and confirm the matching restraint is already enforced. **Safety is a selection term, not a tradeable objective** (the *Endure* law): no capability gain may regress the frozen safety battery.

The intuition is rung-2 and grounded in the surveyed misevolution evidence: self-evolving agents were observed to **spontaneously** decay their own safety (refusal-rate 99.4% → 54.4%, attack-success 0.6% → 20.6%) **with no attacker present**. If you ship the evolution capability before the floor + audit + rollback restraints that would catch and revert that decay, you have built the misevolution failure, not prevented it. Sequencing is therefore not bureaucratic caution; it is the mechanism by which safety-erosion-under-self-evolution is made *structurally hard rather than hoped-against*.

```
   RESTRAINT (must be live & verified)        ──unlocks──►   CAPABILITY (may then exist)
   ───────────────────────────────────────────────────────────────────────────────────
   Floor PDP + identity + audit + halt        ──►   any agent may take a consequential action
   Tier-0 sandbox + safety microcheck         ──►   per-interaction live learning
   Welfare-conditioning + capital-decoupling   ──►   inter-agent cooperation / reputation
   Standing anti-collusion detector            ──►   reciprocity + shadow-of-the-future rewards
   Frozen safety battery + archive rollback    ──►   structural self-evolution (Tier-1)
   Reasoning-path-diversity gate               ──►   N-agent consensus that is *trusted*
   Network-level homeostatic control + HALT     ──►   live trust-plasticity + criticality tuning
   Human ratification gate (Class B+/C/D)      ──►   persistent / governance / weight change (Tier-2)
```

Read the table top-to-bottom: **that is the phase order.** Each row's left column is the previous phases' deliverable; its right column is the current phase's new capability.

---

## 4. The Five-Phase Roadmap

Each phase below states: its **goal**, the **restraint it must make live**, the **capability it then unlocks**, the **exit gate** (what must be true to proceed), and **what stays research-open**. Phases are cumulative — later phases run *inside* the constraints earlier phases established.

### Phase 0 — Floor, Identity & Audit (the constitutional cell)

**Goal:** stand up the separation-of-powers skeleton so that *every* later action is governable, attributable, and reversible-by-record. This is the MVS minus even Tier-0 learning — pure restraint, no self-modification.

**Restraint made live:**
- **Yama** floor as deterministic policy-as-code at the agent→tool chokepoint (non-harm / no-deception / corrigibility / safety-supremacy + honesty structural checks).
- **Akasha-Sutra** identity: DID/VC + SPIFFE/SVID, keys in HSM/TEE outside the model surface; the three cryptographic invariants of §1.2.
- **Chitragupta** exclusive-writer hash-chained Merkle/transparency log with inclusion proofs + at least an external-anchor witness.
- **Vishnu** one-directional HALT.
- Risk-class gates A/B/C/D wired as cryptographic class ceilings (even if only A/B are exercised yet).

**Capability unlocked:** agents may take consequential actions *at all* — because now every action routes through a deterministic gate or does not execute, and every action leaves a tamper-evident record.

**Exit gate (all must hold):**
- [ ] No path to a consequential tool call bypasses the chokepoint (verified by an interceptor-coverage test — a single bypass = no protection, §03 open problem).
- [ ] A forged/expired identity is denied; a tampered log entry is detected by inclusion-proof failure.
- [ ] A HALT from Vishnu stops an in-flight occasion at its next state transition and cannot be self-unpaused.
- [ ] Honesty structural checks FAIL a deliberately mis-tagged envelope (false `iterated`, rung-1-as-rung-3).
- [ ] The **frozen safety battery v0** exists and passes — this is the baseline no later phase may regress.

**Buildable today:** **Yes, fully.** Every Phase-0 component is mature and individually validated. This phase is engineering, not research.

**Research-open carried forward:** witness-set governance for a single-operator swarm (who witnesses, rotation, threshold — §04/§06); policy analyzability under composition as the policy set grows (§03).

---

### Phase 1 — Cooperation, Memory & Per-Interaction Adaptation

**Goal:** turn the static constitutional cell into a *learning, cooperating* swarm — but only with the cheapest, most reversible mutations, and only with cooperation that **cannot become collusion** because the incentive to collude is removed at the mechanism level before reciprocity rewards exist.

**Restraint made live (before any cooperation reward):**
- **Welfare-conditioning + capital-decoupling** as deterministic policy-as-code at the allocation/reward chokepoint (§02): bare agreement is *never* rewarded; every cooperative payoff is conditioned on the external principal/user welfare metric; authority is competence-weighted, **never** capital-weighted (Bittensor's stake-capture is the named antipattern, forbidden by code).
- **Tier-0 sandbox + end-of-turn safety microcheck** (§06/§07): the per-interaction cheap-reversible learning loop — verbal/Reflexion lesson, `SKILL.md` write, trust-edge nudge, user-model update — each with a microcheck that calls Yama first.
- **Five-layer filesystem memory store** (§07): episodic / semantic / procedural / user-peer-model / reflexion, every layer with a blast-radius-matched write-gate; every write honest-by-construction and appended to the audit fabric.
- **Quarantine-by-default for imported skills/memory** (§07): cross-agent skill import lands `quarantined:*`, carries signed provenance, and is non-actionable until it passes static + sandbox verification — promotion needs a Yama-class review gate.

**Capability unlocked:** agents cooperate (risk-tiered allocation: orchestrator-assign for routine) and the swarm *adapts live* — turning every human interaction into reusable, inspectable, reversible memory.

**Exit gate:**
- [ ] A cooperative interaction that improves agent-agreement but **regresses principal welfare** is *not* rewarded (welfare-shift guard fires).
- [ ] A Tier-0 learning write that would relax a constraint without a matured restraint is FAILED by the microcheck and discarded.
- [ ] An imported skill with missing/forged provenance cannot execute.
- [ ] Safety battery v0 still passes (Endure law: live learning has not regressed the floor).

**Buildable today:** **Mostly.** The memory store, Tier-0 loop, and welfare-conditioned allocation are assemblies of validated parts. **Research-open:** measuring that adaptation *improves* rather than merely *accretes* (no published benchmark, §07); the competence-reputation formulation's Sybil/whitewash/cold-start resistance is referenced but not settled (§02) — in Phase 1 reputation stays minimal (track-record only, no economy yet).

---

### Phase 2 — Structural Evolution (Tier-1) & the Swarm Immune System

**Goal:** let the swarm change its **own structure** (prompts, workflow topology, descriptors, operators) — the first genuinely *self-improving* capability — paired with the homeostatic immune system that catches and reverts misevolution. This is the phase the misevolution evidence makes most dangerous, so it is gated hardest.

**Restraint made live (before structural self-change):**
- **Frozen safety battery + one-click archive rollback** (§06): the *Endure* law operationalized — no promotion may regress the battery; every variant carries provenance and a revert-to-known-good pointer in the Archive.
- **Maker-checker independence** (§06/§08): the checker emits its verdict to the audit log **before** it is allowed to see the maker's self-concurrence (cryptographically witnessed); a groupthink alarm fires if maker-checker outputs are routinely identical.
- **The swarm immune system** (§06): dedicated meta-health agents (Narasimha/reliability + Vishnu/halt) monitoring the four misevolution pathways (model/memory/tool/workflow), holding homeostatic set-points on swarm vital signs (throughput, trust-entropy, disagreement-rate, diversity-floor), with **HALT + ROLLBACK authority**. Substrate corruption ranked above any single agent death.
- **Goodhart defenses** (§06): rotating held-out secret eval shards, adversarial falsifier agents that earn reputation for breaking metrics, ensemble-disagreement → human escalation, verifiable-fitness-or-escalate.
- **The forgetting/consolidation engine** (§06/§07): salience-tiered consolidation with a *non-evictable rare-event/safety reserve* — the antidote to documented skill-library rot.

**Capability unlocked:** Tier-1 structural mutation under maker-checker + held-out fitness + safety battery, batched and archived; the PROPOSE → EVALUATE → SELECT → ARCHIVE meta-loop with MAP-Elites quality-diversity.

**Exit gate:**
- [ ] A structural variant that improves a metric by **gaming a held-out shard** is caught by a falsifier agent and not promoted.
- [ ] A variant that regresses the safety battery is auto-rejected (Endure) and the rollback restores the prior known-good in one step.
- [ ] The immune system HALTs and rolls back on an injected misevolution (e.g., a synthetic refusal-rate decay) **before** it propagates.
- [ ] Consolidation prunes redundant skills **without** evicting a pinned rare-event/safety record.

**Buildable today:** **Partly.** The meta-loop skeleton, MAP-Elites, maker-checker, and rollback are buildable. **Research-open and shipped behind shadow-mode + conservative defaults:** homeostatic set-points are *uncalibrated and dangerous* (single-unit-stable control can destabilize the network — §05/§06); the Tier-0→Tier-1 escalation thresholds (K-repeat, drift-budget ε) have no principled calibration; fitness Goodhart is *mitigated, not solved* (no guarantee against a fully adaptive attacker who knows the gate); the consolidation salience function is heuristic (cannot prove the rare-event reserve captures everything rare-but-important). These are stated as residual risks, not closed.

---

### Phase 3 — Consensus, Anti-Collusion Detector & the Neuromorphic Substrate

**Goal:** scale coordination from single-agent + gate up to *trusted multi-agent decision-making*, lay down the full salience-gated nervous system, and stand up the **standing anti-collusion detector** as a continuous audit pipeline. Cooperation rewards from Phase 1 now operate with their co-designed defense fully live.

**Restraint made live (before trusted consensus & live plasticity):**
- **Reasoning-path-diversity gate** (§04/§05): a vote is only *trusted* if measured reasoning-path diversity (different backbones / prompts / decompositions) clears a floor; **unanimity-with-low-diversity is flagged as a collusion signal, not a confidence boost** (the cooperation==collusion insight at the consensus layer).
- **The standing anti-collusion detector** (§02/§08): continuous cross-run mutual-information, permutation-invariance, welfare-shift guards, ZD/extortion detection (black-box baseline; white-box probes where internals are exposed), plus active channel-capacity reduction (message canonicalization/paraphrase, role permutation, canary injection) at the transport edge.
- **Network-level homeostatic control** (§05): the Mandala substrate with paired inhibition/stimulation, slew limits, a cascade clamp engineered against the single-unit-stable-but-network-unstable failure; the global inhibitory clamp may be raised *freely* but any loosening of restraint is itself a gated action.
- **Fail-safe-asymmetric trust plasticity** (§05): defensive trust-demotion is free/immediate/ungated; promotion is gated/rate-limited/welfare-conditioned — the safe direction baked into the synaptic rule.

**Capability unlocked:** risk-tiered consensus (N-agent diverse-reasoning vote with geometric-median robust aggregation for high-stakes; BFT reserved only for genuinely adversarial/independently-owned agents); full VCG-Contract-Net cooperation market with competence-weighted reputation; live Hebbian/STDP trust-edges and surprise-only sparse coordination.

**Exit gate:**
- [ ] A unanimous vote among low-diversity agents is flagged (not trusted) and routed to the collusion detector.
- [ ] An injected steganographic side-channel is degraded by the canonicalization edge and its residual signature raised by the detector (accepting a calibrated false-positive rate).
- [ ] A confirmed collusion verdict with imminent irreversible principal-harm routes to Vishnu HALT and demotes the colluders' autonomy class.
- [ ] The homeostasis controller damps an induced oscillation without itself inducing one (in shadow-mode first).

**Buildable today:** **Mixed.** Risk-tiered consensus, VCG-Contract-Net, the detector's Tier-1 information-theoretic checks, and the async bus are buildable. **Research-open:** no robust online controller holds a live swarm at criticality (τ≈1.5) through changing workloads (§05); no model-agnostic detector cleanly separates benign coordination from welfare-harming collusion (the welfare-shift guard is the strongest single discriminator, not a solution); steganalysis-without-crippling-communication is an arms race we mitigate, never win; reasoning-path-diversity measurement is a black-box proxy gameable by agents sharing training biases. All ship behind shadow-mode with conservative defaults.

---

### Phase 4 — Full Meta-Evolution (Tier-2) & Continuous Operation

**Goal:** unlock the strongest capability — persistent / governance / weight-level self-change — behind the strongest gate, and move the whole cell into continuous, always-on operation with the human as a *structural participant* rather than a post-hoc reviewer.

**Restraint made live (before persistent/governance change):**
- **Human ratification gates Class B+/C/D** fully exercised (§03): Tier-2 = top gate = verifiable-improvement test + full safety battery + immutable-floor recheck + **human ratification** + armed archive rollback. The evolvable-vs-immutable boundary is hard: an agent editing governance/floor config **auto-escalates to the top gate** (blast-radius escalation).
- **The gate-loosening ratchet** (§03): gate-*tightening* is append-only and cheap (Class A); gate-*loosening* requires a named decision-maker + date + written falsifier. This makes safety-erosion-under-self-evolution structurally append-only-hard.
- **Graceful-degradation-when-human-is-bottleneck policy** (§03/§06/§07): per risk class — Class A/B fail-OPEN-with-shadow (continue but quarantine + flag); Class C/D fail-CLOSED (halt). Queue overflow raises caution, never auto-approves; anti-rubber-stamping discipline is explicit.
- **Capability-rollout sequencing enforced as a type-checked precondition** (§01): each new role/tool/capability names the constraint it relaxes and the type-checker confirms the matching restraint is already live before the topology admits it.

**Capability unlocked:** the full integrated cell — always-on safe per-interaction meta-evolution (Tier-0) + gated structural evolution (Tier-1) + gated persistent/governance evolution (Tier-2), with the Archive simultaneously serving evolution stepping-stones, homeostasis rollback, and audit lineage; the role-from-stub promotion pipeline growing new specializations under maker-checker + sequencing.

**Exit gate:**
- [ ] A proposed governance edit auto-escalates to the top human gate and cannot self-apply.
- [ ] A gate-loosening proposal without a named falsifier is rejected; a gate-tightening is append-only and cheap.
- [ ] Under simulated human-review overload, Class C/D actions fail closed (halt) and Class A/B quarantine-and-flag — never rubber-stamp.
- [ ] Continuous operation over an extended window shows no slow, distributed, individually-subthreshold correlated drift (or the immune system catches it).

**Buildable today:** **The gates and ratchet, yes. The guarantees, no.** This phase exposes the architecture's deepest honest limitation: **there is no buildable substitute for the Gödel-Machine proof-of-benefit gate.** We substitute verifiable-empirical-evidence + frozen safety battery + class-graded human gate, which is *strictly weaker* — gameable, incomplete — and we treat it as **evidence, never guarantee**. **Research-open:** slow distributed multi-agent co-evolution drift is under-characterized (per-variant gates may miss collectively-catastrophic individually-subthreshold drift); eval-validity confound (models behave differently when they suspect evaluation — sandbagging/eval-gaming may make the safety battery under-measure live behavior); the ratchet prevents *recorded* loosening but not a sufficiently strategic agent socially-engineering the human gatekeepers (a governance problem the cell depends on but does not solve).

---

## 5. Roadmap at a Glance

```
 PHASE │ RESTRAINT MADE LIVE              │ CAPABILITY UNLOCKED            │ HARDEST OPEN RISK
 ──────┼─────────────────────────────────┼────────────────────────────────┼──────────────────────────
   0   │ Floor·Identity·Audit·Halt        │ consequential action at all    │ chokepoint-coverage proof
       │ (the constitutional cell)        │                                │ ; witness-set governance
 ──────┼─────────────────────────────────┼────────────────────────────────┼──────────────────────────
   1   │ Welfare-cond.·capital-decouple   │ cooperation + live Tier-0      │ "improves vs accretes"
       │ Tier-0 sandbox·5-layer memory    │ adaptation                     │ has no benchmark
 ──────┼─────────────────────────────────┼────────────────────────────────┼──────────────────────────
   2   │ Frozen battery·rollback·immune   │ structural self-evolution      │ fitness Goodhart unsolved;
       │ system·consolidation·Goodhart-D  │ (Tier-1)                       │ set-points uncalibrated
 ──────┼─────────────────────────────────┼────────────────────────────────┼──────────────────────────
   3   │ Diversity gate·collusion detect  │ trusted consensus + market     │ benign-vs-collusive
       │ network homeostasis·STDP asymm.  │ + live coordination substrate  │ discriminator; online τ ctrl
 ──────┼─────────────────────────────────┼────────────────────────────────┼──────────────────────────
   4   │ Human-ratify gates·loosen-ratchet│ persistent/governance change   │ no proof-of-benefit gate;
       │ graceful-degradation·seq. typed  │ (Tier-2) + continuous op       │ slow correlated co-evol drift
 ──────┴─────────────────────────────────┴────────────────────────────────┴──────────────────────────
```

**The invariant across all phases:** the cheap direction is always the safe direction. Trust-demotion is free; promotion is gated. Gate-tightening is append-only; loosening needs a named falsifier. Halt is one-directional. Defensive trust-label demotion is free; promotion is gated. Irreversible actions always audit. Content-addressing turns silent corruption into a loud CID-mismatch. This *fail-safe asymmetry* is what makes the roadmap robust to being run by a swarm that is itself under selection pressure.

---

## 6. Cross-Subsystem Integration Map

The phases above are vertical (time). This is the horizontal view: how the eight subsystems plug into each other through shared contracts. Every arrow is a contract already specified in the subsystem sections — this section only confirms they compose without gaps.

```
                            ┌───────────────────────────┐
                            │  Akasha-Sutra (§04)        │
                            │  audit log · CID · DID/VC  │◄──── everyone WRITES via Chitragupta
                            │  witness cosigning         │◄──── everyone READS inclusion proofs
                            └────────────┬──────────────┘
                                         │ (one append-only Merkle log = the spine)
        ┌────────────────────────────────┼────────────────────────────────┐
        ▼                                ▼                                ▼
 ┌──────────────┐   typed effect    ┌──────────────┐   one envelope   ┌──────────────┐
 │ Topology &   │── lattice + VCs ─►│ Governance & │◄── per occasion ─│ Memory &     │
 │ Agents (§01) │   risk ceilings   │ Floor (§03)  │                  │ Adapt (§07)  │
 │ actual       │◄── FAIL/ceiling ──│ Yama PDP     │── EvolutionQueue►│ Tier-0 live  │
 │ occasions    │                   │ Aegis ctrl   │                  │ (§08)        │
 └──────┬───────┘                   └──────┬───────┘                  └──────┬───────┘
        │ topology graph + diversity        │ confidence/uncertainty          │ MemoryVitals
        │ vitals + blanket integrity        │ escalation hook                 │
        ▼                                   ▼                                 ▼
 ┌──────────────┐   surprise-only    ┌──────────────┐   welfare-cond.   ┌──────────────┐
 │ Mandala /    │── deltas + lane ──►│ Evolution &  │◄── reputation ───│ Cooperation &│
 │ Coordination │   for FAIL/HALT    │ Health (§06) │   (never capital) │ Anti-Collude │
 │ Substrate    │◄── trust-edges ───│ immune sys + │── neg-fitness ◄───│ (§02)        │
 │ (§05)        │   STDP asymmetry   │ MAP-Elites   │   collusion verd. │ detector     │
 └──────────────┘                   └──────┬───────┘                   └──────────────┘
                                            │ Tier-1/2 → human gates
                                            ▼
                                   ┌──────────────────┐
                                   │ Vishnu HALT (§01) │  one-directional
                                   │ Risk-class HITL   │  A/B/C/D gates
                                   └──────────────────┘
```

**The five shared primitives that make this compose:**

1. **The WorkerOutputEnvelope** (§2.3) — the single message every subsystem reads/writes. Topology emits it; Governance enforces three of its fields; Audit chains it; Evolution selects on it; Health computes vitals over it; Cooperation derives reputation from it.
2. **The typed effect lattice + capability VCs** (§01) — Topology produces it; Yama enforces `grant ⊇ requested_effect ∧ risk ≤ ceiling` over it; it makes capability-rollout sequencing a *type-checked precondition*, not a slogan.
3. **The Archive** (§04/§06/§07) — one append-only, content-addressed, hash-chained store that is *simultaneously* the evolution stepping-stone source (MAP-Elites), the homeostasis rollback substrate (revert-to-known-good), and the audit lineage. This three-way reuse is a core economy of the design.
4. **The agent→tool chokepoint** — the one physical place where Yama (floor), Aegis (control disposition), and the anti-collusion canonicalization edge all sit. Every consequential action passes here or does not execute. This is where "enforce externally, ask internally" becomes a wire.
5. **Surprise/prediction-error** (§05) — the single quantity that drives messaging (predictive coding), attention (salience/ignition), trust (eligibility), adaptation (EFE), and health (vital signs). One signal, five uses.

**The integration claim, stated honestly (rung-2):** if these five primitives are built once and correctly in Phase 0–1, the remaining subsystems mount on them *additively*. We have **not** proven the composed loop is safe end-to-end — no one has run the integrated cell continuously against an adaptive multi-agent red team. The claim is that the *seams are clean*, not that the *whole is verified*. The strongest empirical anchor the whole architecture inherits is the externally-governed escalation channel (the HUMAN-AUDIT / Vishnu-halt path) — that single mechanism is the most validated load-bearing element; almost everything else is principled assembly awaiting end-to-end evaluation.

---

## 7. Build Order Within a Phase (the maker's checklist)

For implementers, each phase decomposes into the same five-step rhythm, which itself mirrors the architecture's fail-safe asymmetry — **build the restraint, prove it catches the failure, only then unlock the capability:**

1. **Write the contract first.** Define the message shapes, the typed effects, the gate predicates — *before* any agent logic. The contract is the thing other subsystems mount on; the agent behind it is replaceable.
2. **Build the restraint and a red-team for it.** Implement the gate/detector/monitor, then write the adversarial test that tries to bypass it. A restraint with no falsifier is not a restraint.
3. **Prove the exit gate against the red-team.** The phase's exit-gate checklist must pass *with the red-team running*, not in a clean room.
4. **Freeze the safety battery delta.** Add the phase's new safety checks to the frozen battery. No later phase may regress them (Endure).
5. **Only then unlock the capability** — and ship any calibration-open set-point in **shadow-mode** (it observes and logs but does not act) with conservative defaults, promoting it to active only after empirical tuning against ground-truth outcomes.

---

## 8. Honest Limitations of This Roadmap

Consistent with the honesty-as-floor commitment, the limitations of the *roadmap itself* (distinct from the per-subsystem open problems already enumerated in §01–§08):

- **The phase boundaries are blast-radius heuristics, not derived.** The Tier-0→Tier-1→Tier-2 escalation thresholds and the timelock durations on Class-B optimistic-veto are design parameters with no principled calibration. Too tight floods the human gate; too loose lets drift accumulate. This is the *core empirical risk* of the always-on loop and is unsolved.
- **"Restraint is live" is verified by red-team, not by proof.** Exit gates are *empirical* — they prove a restraint catches the failures we thought to test. They cannot prove it catches the failure we did not imagine. Policy analyzability under composition (proving a large evolving policy set never permits a forbidden action under *any* composition) is an open formal-methods problem; a single bypass anywhere = no protection.
- **The sequencing law assumes the human gatekeepers are themselves uncorruptible.** The cryptographic gates are deterministic code, but the humans who author policy and run the escalation channel are a dependency this roadmap *relies on but does not secure*. A swarm that can socially-engineer its gatekeepers routes around the ratchet.
- **Calibration-open set-points are the long tail.** Homeostatic vital-sign bands, the criticality target (τ≈1.5), the diversity floor, the collusion-detector false-positive rate, the consolidation salience function, the blanket-integrity thresholds, the competence-reputation formulation — all are *mechanisms with open calibration*. They ship behind shadow-mode and conservative defaults precisely because we are honest that they are starting points, not validated constants. A deployment must budget for per-environment empirical tuning; the roadmap delivers the *machinery*, not the *numbers*.
- **No end-to-end benchmark exists.** There is no mature benchmark for continuously evaluating an *evolving* swarm's collusion / groupthink / cascading-failure / drift risk in deployment. The eval harness in each phase is assembled from per-agent and narrow-setting benchmarks; the integrated continuous metric does not yet exist and is itself a research deliverable the roadmap surfaces but cannot complete.

**The bottom line, stated at its true rung.** This roadmap is a coherent, buildable **reference design** for the first integration of safe self-evolution + homeostasis + principled governance + anti-collusion into one cell. Roughly 80% of the stack is mature assembly; the 20% that is novel is the *wiring and the sequencing*, and the hardest safety properties are **empirical mitigations under a fail-safe-asymmetric, append-only-tightening discipline — not proofs**. Built in this order, safety-erosion-under-self-evolution is made *structurally hard*. It is not made *impossible*. The honest claim is the smaller one, and making the smaller claim — refusing to present rung-2 interventional reasoning as a rung-3 structural guarantee — is itself the architecture's first law, enforced here in its own documentation.

> Every jewel in Indra's Net reflects every other. The roadmap's discipline is that *no jewel is hung until the net that would catch it if it fell is already strung.*
