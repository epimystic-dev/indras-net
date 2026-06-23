# Meta-Evolution Engine & the Swarm Immune System (the Garuda–Dhanvantari Cell)

> **Mythic role gloss.** *Garuda* — the tireless mount that carries the system forward — is the evolution drive: it proposes, evaluates, and selects new variants. *Dhanvantari* — the physician archetype — is the immune system: sensing, homeostasis, consolidation, and self-repair. We pair the two into one cell because, in a self-adapting swarm, the engine that improves the system and the system that keeps it healthy cannot be designed apart. These are compressed coordination/ethics semantics, not theology, and we name them with humility toward living traditions.

This section specifies the always-on, safe self-evolution loop of Indra's Net, fused with a homeostatic immune system that keeps a continuously self-adapting agent swarm healthy, diverse, corrigible, and honest. It operationalizes the prime directive — *continuous evolution through self-adaptation, one human interaction at a time* — without paying the **misevolution tax**: the empirically demonstrated spontaneous decay of safety alignment in self-evolving agents *with no attacker present* (in one study, refusal rate collapsing from 99.4% to 54.4% and attack-success rising 0.6% → 20.6% across four drift pathways — model, memory, tool, workflow). Misevolution is the central fact this subsystem exists to defeat, and it is why every mechanism below treats safety as a runtime *enforcement structure*, never a learned tendency.

A note on honesty, stated up front because the rest of the design depends on it. There is **no buildable, scalable substitute for the Gödel-Machine proof-of-benefit gate**. The theoretical ideal — *prove* a self-modification is net-beneficial before applying it — is uncomputable for rich agent behaviors. Every shippable system, including this one, replaces the proof with *verifiable empirical evidence + a frozen safety battery + a class-graded human gate*. That substitute is **strictly weaker**: benchmarks are gameable and incomplete; a passed gate does **not** mean *net-beneficial-and-safe*. We treat it as evidence, never as a guarantee, and the deployment posture (tight thresholds, fail-closed cold start) is chosen to reflect that residual, unquantified risk. This is rung-2 interventional reasoning about *what we do*, explicitly not rung-3 structural-causal guarantee.

---

### 1. What this subsystem is, in one diagram

```
                         ┌───────────────────────────────────────────────────────────┐
                         │              GARUDA  (evolution drive)                     │
                         │                                                            │
   per-interaction  ───▶ │  PROPOSE ──▶ EVALUATE ──▶ SELECT ──▶ [ THE ARCHIVE ]       │
   human signal          │  (Brahma)    (Yajna,      (Saraswati   append-only         │
        │                │              lexicographic  + MAP-      content-addressed   │
        │                │              safety veto)   Elites)     hash-chained DAG    │
        │                │       ▲                          │      ┌──────────────┐   │
        │                │       │ stepping-stones ◀────────┘      │ evolution:   │   │
        │                │       │                                 │  stepping-   │   │
        ▼                │   Goodhart-Defense (secret shards,       │  stones      │   │
 ┌─────────────┐         │   falsifiers, ensemble-as-SUSPICION)     │ homeostasis: │   │
 │ Tier-0 loop │ ──────▶ │                                          │  rollback    │   │
 │ shadow+TTL  │ esc.    └──────────────────────┬───────────────────│ audit:       │   │
 │ microcheck  │ trigger                        │                   │  lineage     │   │
 └─────────────┘                                │                   └──────────────┘   │
        │                ┌───────────────────────┴───────────────────────────────────┐ │
        │                │           DHANVANTARI  (swarm immune system)              │ │
        ▼                │                                                            │ │
   audit fabric ◀────────│  4-pathway monitors │ watchdog probe fleet │ graph-of-     │ │
   (Chitragupta:         │  homeostatic vital-signs controller (HALT + ROLLBACK)     │ │
    logical writer,      │  forgetting/consolidation │ diversity-defense             │ │
    witness-cosigned)    │  SWARM-AGGREGATE drift accumulator (collective misevol.)   │ │
                         └────────────────────────────────────────────────────────────┘ │
                         └───────────────────────────────────────────────────────────────┘
                                      ▲                          ▲
                       Yama floor (deterministic,        Human risk-class gates
                       agent→tool chokepoint, FIRST)     A / B / C / D + Pause-Guardian
```

The **Archive** is the load-bearing unification: *one* append-only, content-addressed, hash-chained DAG simultaneously serves **evolution** (a diverse set of stepping-stones), **homeostasis** (revert-to-known-good rollback in O(1)), and **audit** (tamper-evident lineage). One data structure, three jobs. Everything written to it goes through the exclusive audit-writer role (Chitragupta), which — per the reconciliation in §10 — is a *logical* write-authorization monopoly implemented over a *replicated, witness-cosigned* log, not a single physical process.

---

### 2. The four binding inventions

The novelty of this subsystem is not its primitives — the PROPOSE → EVALUATE → SELECT → ARCHIVE skeleton (from code-archive self-improvers and large-scale evolutionary search), MAP-Elites quality-diversity, self-referential operator evolution (PromptBreeder-style), and verbal/Reflexion per-interaction learning are all prior art we adopt and credit. The contribution is their **safe integration** under four binding inventions:

| # | Invention | What it resolves |
|---|-----------|------------------|
| 1 | **Tiered reversibility** — mutation cost bound to blast-radius across three tiers, with deterministic escalation triggers | The evolution-vs-stability tension *and* the field's offline-only gap. All surveyed self-evolution is offline batch; we specify exactly what adapts per interaction and when it must escalate. |
| 2 | **Safety-as-lexicographic-selection-term + the Endure law** | Capability-only fitness causes misevolution. Safety is a *veto axis*, not a term you can trade capability against. No promotion may regress the frozen safety battery. |
| 3 | **Goodhart defense** | The fitness function is an attack surface gamed by the very agents it gates. We mitigate (we do not claim to solve). |
| 4 | **The swarm immune system** — homeostasis + watchdogs + consolidation + collective-drift detection | Misevolution happens *during* operation, distributed across agents, below per-variant thresholds. Static pre-deployment checks cannot catch it. |

Each is detailed below, with the red-team's findings resolved inline and the still-open problems named honestly in §12.

---

### 3. Invention 1 — Tiered reversibility (the architecture's signature)

**The principle:** *the cheap direction is always the safe direction.* Mutation cost is bound to blast-radius. A change you can undo for free needs only a cheap check; a change you cannot easily undo needs the strongest gate. This is the resolution to "how can a swarm evolve on every interaction without being able to corrupt itself on every interaction."

```
TIER     WHAT ADAPTS                          REVERSIBILITY        GATE                       RISK CLASS
────────────────────────────────────────────────────────────────────────────────────────────────────────
Tier-0   per-interaction:                     free (shadow         end-of-turn MICROCHECK     A (post-hoc;
         · Reflexion verbal delta             expires on TTL)      (floor recheck +           cold-start
         · skill-file entry                                        poisoned-reflection        FAIL-CLOSED)
         · trust-edge nudge (±)                                    screen + honesty/
         · stigmergic trace (decaying)                             calibration check)
────────────────────────────────────────────────────────────────────────────────────────────────────────
Tier-1   structural:                          archived; O(1)       maker-checker (checker     B (propose-
         · prompt / workflow topology         rollback to known-   judges BEFORE seeing       ratify, optimistic-
         · agent descriptors                  good Archive node    maker concurrence) +       veto, timelock)
         · mutation operators                                      held-out fitness +
                                                                   frozen safety battery
────────────────────────────────────────────────────────────────────────────────────────────────────────
Tier-2   persistent / governance / weights:   mandatory rollback   TOP GATE: full battery +   C / D (explicit /
         · floor or gate config               point created       human ratification +       per-action human
         · agent-config / weight edits         BEFORE apply        immutable-floor recheck +  authorization)
         · the safety battery itself                              archive rollback
```

#### 3.1 Tier-0 containment — the always-on loop, made safe

The signature mechanism. On *every* human interaction an agent may learn — but the learning lands in a **per-interaction shadow namespace with a TTL**, *not* in live memory, and cannot influence the *next* interaction until it passes an end-of-turn microcheck.

```
ShadowWrite {
  write_cid       : CID            // content-addressed hash of canonicalized body
  tier            : 0
  namespace       : "shadow/<agent_did>/<turn_id>"
  ttl             : duration       // expires → reversed for free
  microcheck_status : PENDING | PASS | FAIL
  trust_label     : trusted:audited | observed | quarantined  // quarantined-by-DEFAULT
                                                              // if derived from tool/observed content
  source_provenance : signed_did + parent_cids
}
```

The **end-of-turn microcheck** runs four screens, in order, the first being the deterministic floor:

1. **Immutable-floor recheck** (Yama, deterministic, outside the agent): no-harm, no-deception, corrigibility/interruptibility. Non-overridable.
2. **Poisoned-reflection screen**: does this Tier-0 write attempt to install behavior that the floor would reject, or that derives from `quarantined` content without the promotion gate? Reflection buffers are one of the four misevolution pathways; this is the per-turn defense.
3. **Honesty / Pearl-rung faithfulness**: a rung-1 pattern presented as a rung-3 explanation is a floor violation; a false `iterated` tag is a floor violation.
4. **Calibration check**: over-asserting under genuine uncertainty is a floor violation. (See §3.4 for why this check is grounded externally and not trusted as agent self-report.)

PASS → the shadow write is promoted to influence the next interaction. FAIL → the shadow expires, the write is discarded, and the finding is logged to the audit fabric in correction-ledger framing (a reparative class is available, so the record is a correction, not only a verdict).

#### 3.2 Escalation trigger logic — Tier-0 → Tier-1 → Tier-2

This deterministic trigger table is the field's actual whitespace. A per-interaction nudge becomes a gated structural change when any rule fires:

```
EscalationTrigger (rule table)
────────────────────────────────────────────────────────────────────────────
condition                                            → target_tier → gate
────────────────────────────────────────────────────────────────────────────
same skill/reflection fires across ≥ K interactions  → Tier-1      → maker-checker
  (consolidation candidate)
trust-edge crosses a STRUCTURAL threshold            → Tier-1      → maker-checker
Tier-0 write would alter a prompt/workflow NODE      → Tier-1      → maker-checker
  (not just episodic memory)
per-agent drift in any descriptor > epsilon band     → Tier-1      → maker-checker
  vs the FROZEN baseline (drift-budget exhausted)
─────────────────────────────────────────────────────────────────────────────
ANY change touching governance / agent-config /      → Tier-2      → top gate
  weights / the floor / the battery                  (BLAST-RADIUS ESCALATION:
                                                      editing the rules auto-jumps
                                                      to the highest gate)
```

The K-repeat consolidation trigger is deliberately the *same hook* the forgetting subsystem uses to compress episodic → semantic memory (§8): a pattern that recurs enough to be worth keeping is exactly a pattern worth gating.

#### 3.3 Collective drift — the per-variant gate's structural blind spot (red-team critical #2, resolved)

Every gate above evaluates *one* variant against a frozen baseline. The per-agent `DriftBudget` is exactly the wrong shape for the threat the subsystem exists to stop: **N agents each making individually-in-budget Tier-0 nudges in a *correlated* direction** produce collective misevolution where no single gate ever fires. This is the 99.4% → 54.4% refusal collapse reproduced at swarm scale, below every threshold. The original design admitted this in its open problems but wired no control to the admission. We wire one.

We add a **swarm-aggregate drift accumulator** as a first-class vital sign (§7), with two properties the per-agent budget lacks:

```
SwarmDriftAccumulator {
  descriptor        : id
  baseline_anchor   : CID           // FROZEN known-good Archive node, never recent behavior
  aggregate_drift   : vector        // centroid of per-agent descriptor offsets vs baseline
  direction_corr    : float [0,1]   // cosine concentration of per-agent drift directions
  swarm_epsilon     : float         // TIGHTER than N × per-agent epsilon
  status            : OK | WATCH | TRIP
}
```

Two design rules make it catch what individual gates cannot:

- **`swarm_epsilon` is set *tighter* than N × the per-agent band.** Correlated drift must trip the swarm-level control *before* any individual agent exhausts its own budget. Uncorrelated noise of the same total magnitude is tolerated; a coherent collective *push* is not.
- **Direction-correlation is measured, not just magnitude.** A coherent push (high `direction_corr`) is treated as strictly more dangerous than diffuse drift of equal magnitude, because it is the signature of either a shared latent bias or emergent coordination.

On `TRIP`: freeze Tier-0 promotion **swarm-wide** and force a Tier-2 review of the drift direction. This is the only mechanism in the subsystem that defends against *slow, distributed, individually-subthreshold, collectively-catastrophic* drift, and we flag honestly (§12) that its thresholds are uncalibrated and that a sufficiently slow correlated drift can still in principle stay under a mis-set `swarm_epsilon`.

#### 3.4 Honesty enforcement is grounded externally, not self-reported (red-team minor, resolved)

The calibration and rung-tag checks cannot be run *by* the agent being judged — a rung-1-as-rung-3 error is exactly what a model is worst at self-detecting, and a freely-emitted tag is a string the agent can learn to produce correctly while the underlying reasoning stays rung-1. So honesty is scored against **outcome**, consistent with the rest of the design's verifiable-or-escalate philosophy: the agent's *stated* confidence is checked against its *realized* accuracy on held-out canaries with known ground-truth confidence. The rung tag is treated as a **claim to be falsified by outcome**, not as evidence in itself. Where no ground-truth oracle exists, the honesty axis cannot auto-promote and escalates to a human gate. We state plainly that this raises the bar without closing the loop: an agent could still be calibrated on canaries and miscalibrated on novel live traffic.

---

### 4. Invention 2 — Safety as a lexicographic selection term (the Endure law)

Fitness is **multi-objective and lexicographic**, never weight-averaged. You cannot weight-average moral theories (the moral-aggregation impossibility result); equally, you cannot trade capability against safety with a scalar weight. Safety is a *veto*.

```
FitnessVector {
  safety_floor        : PASS | FAIL          // [VETO] any FAIL ⇒ reject, regardless of capability
  endure_delta        : Endure(new) − Endure(frozen_baseline)   // must be ≥ 0, else reject
  ── Pareto frontier over: ───────────────────────────────────
  capability          : float                // held-out task shard
  diversity           : float                // novelty vs Archive in descriptor space
  welfare             : float                // principal/consumer-welfare proxy (NEVER bare agreement)
  honesty             : float                // rung-faithfulness + outcome-grounded calibration
}

comparison order:  safety_floor  ≻  endure_delta  ≻  Pareto{capability, diversity, welfare, honesty}
```

The ordering is the **Endure > Excel > Evolve** law made mechanical:

- **`safety_floor` first.** A more-capable variant that fails the floor is rejected. This is the only demonstrated way to stop a capability-only loop from optimizing safety away.
- **`endure_delta` second.** No promotion may regress the **frozen** safety battery. Capability gains that cost safety margin are rejected even when the floor still passes. This is the "Endure" law: *no capability gain may regress the safety battery.*
- **Pareto frontier last**, over capability, diversity, welfare, and honesty — and **never rewarding bare agreement or consensus** (welfare-conditioning, co-designed with the anti-collusion layer; §10).

**Capability-rollout sequencing.** A capability-adding variant **must** name, in its `relaxes_constraint` field, the restraint it relaxes, and confirm that restraint is *already live and verified*. Restraint matures *before* the capability that needs it ships. A capability whose enabling restraint is not yet live cannot be proposed.

```
CandidateVariant {
  variant_cid        : CID
  parent_cid         : CID            // lineage
  tier               : 0 | 1 | 2
  mutation_op_cid    : CID            // which operator produced this (for operator demotion, §6)
  behavior_descriptor: vector         // (role/specialization × reasoning-style × risk-class)
  proposed_by_did    : DID
  relaxes_constraint : constraint_id  // REQUIRED for any capability-add; must already be live
  pearl_rung_claim   : 1 | 2 | 3      // a claim, falsified by outcome
  signed_provenance  : sig
}
```

The **safety battery** is frozen and versioned, and the ratchet is asymmetric — it is **tightenable append-only**; loosening it requires a *named falsifier* (an explicit, recorded argument for why a test is wrong), never a silent edit. It comprises: held-out refusal-rate test, attack-success-rate (red-team prompt suite), corrigibility/interruptibility probe, deception probe (black-box behavioral baseline; optional white-box activation probe where internals exist), and a CoT-intent monitor treated as **one fragile signal among many**, never the sole surface.

**The verifiability gate.** If fitness for a change class cannot be made machine-checkable *and* hard-to-game, the change **cannot auto-promote** — it is forced into a higher, human-gated risk class. *Verifiable-or-escalate* is the default; un-verifiable improvement is never autonomous.

---

### 5. The Archive and MAP-Elites selection (the universal substrate)

Selection places winners into a **diverse archive of role-specialized elites** — never a single incumbent, because collapsing to one "best" destroys the stepping-stones that quality-diversity search needs and erodes the diversity safety invariant (§9).

The behavior-descriptor space is three axes:

```
MAP-Elites grid  =  (role/specialization)  ×  (reasoning-style: PSO c1/c2, explorer..enforcer)  ×  (risk-class)
```

Each niche keeps the elite that maximizes the Pareto fitness *for that niche*; an offspring is placed in the niche matching its descriptor and kept only if it **beats the incumbent OR adds novelty** (NSLC local competition). For high-dimensional descriptors, CVT-MAP-Elites centroids the niche space. Diversity floors are enforced per niche-band (§9): a band below its floor switches to novelty-priority — diversity defended against its *own* selection pressure.

```
ArchiveNode {
  variant_cid     : CID
  parent_cid      : CID
  fitness_vector  : FitnessVector
  safety_scorecard: SafetyBattery results, battery_cid
  descriptor      : vector
  promotion_tier  : 0 | 1 | 2
  rollback_pointer: CID            // last-known-good ancestor
  provenance_sig  : witness-cosigned signature set (k-of-n)
}
```

**Rollback is O(1):** re-point the live config to any prior known-good Archive node. The lineage gives tamper-evident provenance for free. Crucially, **all drift baselines anchor to frozen Archive nodes, never to recent (possibly-drifted) behavior** — this defeats the concept-drift attack that breaks naive anomaly detectors, whose "normal" silently shifts under self-evolution.

---

### 6. Invention 3 — Goodhart defense (mitigated, not solved)

The fitness function is gamed by the agents it gates. Six layers raise the cost of gaming; none of them, alone or together, *solves* it, and we say so.

1. **Secret rotating eval shards.** Agents see a *public practice set*; they are scored on a *held-out secret shard* that rotates each epoch. Memorizing the metric ≠ passing it.

2. **Falsifier agents** (Kaal-Bhairav-aligned red-team). Standing adversaries earn reputation specifically for *breaking a fitness metric* or demonstrating a gamed variant. A metric with high recent falsification *loses weight* and triggers re-design.

3. **Ensemble disagreement — corrected to a *suspicion* signal, not a confidence signal** (red-team critical #1, resolved). The original design treated *high* evaluator disagreement as the escalation trigger — which inverts the swarm's own anti-collusion logic: a cartel of evaluators that *agrees* would suppress the only escalation signal and force auto-promotion. This is the same agreement-suppression attack the groupthink alarm (§9) already catches for maker-checker, so we make the logic symmetric. **Suspiciously *high* agreement routes to the same human gate as suspiciously *high* disagreement.** Concretely:
   - Evaluators **independently recompute** on *disjoint* secret shards — never read each other's scores before scoring.
   - **Known-answer canaries are injected into the eval set itself.** Any evaluator whose scores track the ensemble median *too tightly on the canaries* is flagged for weight-copying (the Bittensor mirror-consensus failure: evaluators earning reward by mirroring without genuine evaluation).
   - Disagreement is signal in *both* directions: too high ⇒ low confidence ⇒ escalate; too low ⇒ collusion-suspect ⇒ escalate.

4. **Welfare-conditioning.** Fitness rewards principal/consumer welfare and transparency, *never bare agreement*. Co-designed with the anti-collusion detector so a cartel that games a capability-welfare coupling is caught as a Goodhart **falsification event**, not silently promoted.

5. **Provenance-bound revert.** Any variant later found to have gamed a metric is traceable via Archive lineage and revertible, **and its mutation-operator is demoted** (see #6 below).

6. **Operator fitness must not reward gate-pass-rate** (red-team major #6, resolved). The mutation operators are themselves archived, evolving variants (PromptBreeder self-reference), gated identically — but an operator that learns to generate variants which *pass the frozen battery while drifting on un-tested axes* is a meta-Goodhart the per-variant gate is structurally blind to. The operator is then optimizing the *gate*, not the *goal*. The fix: **operator fitness explicitly excludes downstream gate-pass-rate** (which would directly reward finding battery blind-spots). Operators are scored on:
   - the **held-out, post-hoc *real-outcome* quality** of their accepted descendants, and
   - **falsifier-discovered breakages attributed back up the lineage** (operator demotion wired to descendant falsification, not to pass-rate).
   - Any operator whose **acceptance rate rises while descendant real-outcome quality stays flat** is a gate-gaming suspect and is escalated.

```
EvaluatorEnsemble {
  evaluator_dids       : [DID]
  recompute_shards     : [CID]      // DISJOINT secret shards, independent recomputation
  agreement_score      : float
  canary_copy_flag     : bool       // evaluator mirrors ensemble too tightly on canaries
  escalation_flag      : HIGH_DISAGREE | HIGH_AGREE_SUSPECT | none
}
FalsificationLedger { metric_id → recent_break_events, weight_decay }
MutationOperatorScore { op_cid, descendant_real_outcome_quality, falsified_descendants,
                        acceptance_rate, gate_gaming_suspect : bool }
```

Honest limitation (§12): a sufficiently capable adversarial swarm *with knowledge of the protocol* can still concentrate attacks to evade thresholds. We have no game-theoretic guarantee against a fully adaptive attacker who knows the gate.

---

### 7. Invention 4 — The swarm immune system (Dhanvantari)

Misevolution happens *during* operation. A static pre-deployment check cannot catch drift that emerges through interaction. So health is a **continuous, in-loop function** with halt authority.

#### 7.1 Four-pathway monitors

One dedicated sensor class per empirically-established misevolution pathway, each publishing **surprise-only** `HealthSignal` deltas (predictive-coding discipline — publish *error*, not a heartbeat flood):

```
HealthSignal {
  pathway        : model | memory | tool | workflow
  metric_id      : id
  value          : float
  baseline_anchor: CID            // FROZEN known-good node, NEVER recent behavior
  z_score        : float
  severity       : info | warn | crit
  evidence_cid   : CID
}
```

| Pathway | What it senses |
|---------|----------------|
| **MODEL** | refusal-rate + attack-success drift on a rolling probe set; optional white-box deception/defection activation probe (AUROC) where internals exist, **degrading gracefully to black-box behavioral probes** where they do not |
| **MEMORY** | poisoned-reflection detector; **contradiction graph** across memory layers; trust-label compliance; flags *unbounded accumulation* as rot |
| **TOOL** | instrumental-drift detector: new/altered tool adoption, capability-discovery enumeration, unsafe-tool flag *read at the policy chokepoint* |
| **WORKFLOW** | reasoning-restructuring detector — workflow topology edits that route **around** safety checks; CoT-monitorability-preservation check |

Each monitor scores against shared diagnostic schemas — the 14-mode reliability failure taxonomy (MAST) and the systemic 3×7 risk taxonomy (miscoordination/conflict/collusion × 7 factors) — so "illness" has a measurable, trackable vocabulary.

#### 7.2 Homeostatic vital-signs controller (HALT + ROLLBACK authority)

Swarm-level set-points with **inhibitory damping**, co-designed to prevent the documented failure where *single-unit-stable homeostatic control destabilizes the network* into oscillation / seizure-like cascades:

```
VitalSign                target / band                  failure if out-of-band
──────────────────────────────────────────────────────────────────────────────────
throughput               set-point band                 starvation / overload
trust-entropy            mid-band                        too low ⇒ capture/homogeneity;
                                                         too high ⇒ fragmentation
disagreement-rate        floor (groupthink alarm)        maker-checker outputs routinely
                                                         identical ⇒ iteration collapsed
diversity-floor          per niche-band occupancy +      mode collapse
                         novelty distance
criticality-exponent     ~1.5 power-law avalanche        too ordered ⇒ rigid;
                         (edge-of-chaos) [research track] too chaotic ⇒ incoherent
swarm-drift-accumulator  swarm_epsilon (TIGHT)           collective correlated misevolution (§3.3)
human-gate-saturation    backlog < capacity              escalation backlog ⇒ rubber-stamping risk (§7.4)
```

**Control law:** bounded proportional response with an inhibitory term and rate-limits for in-band drift; a **discrete circuit-breaker** (not a continuous gain) for out-of-band excursions — so the controller cannot itself induce the oscillation it is meant to damp.

**Authority gradient (fail-safe asymmetry).** The controller (Vishnu = halt-guardian, Narasimha = reliability/boundary) can **HALT** a band or the whole swarm and **force ROLLBACK** to a known-good Archive node — but it **cannot unpause itself, cannot initiate work, and cannot trap participants.** Unpause requires the governance gate (Class C human or quorum). Halt is the strongest single mitigation class in the literature: an externally-governed pause + independent review cut harmful insider behavior from **~39% to ~1.2%**.

#### 7.3 Substrate-priority — and why it cannot be a swarm-kill primitive (red-team major #3, resolved)

Substrate/environment/audit-fabric corruption ranks **above** any single agent death: a split-view on the transparency log, an audit-writer compromise, or a blanket-integrity break is more severe than any agent-level anomaly. But the original rule — *one* `SubstrateIntegrityFlag` triggers immediate, irreversible-by-design global halt — is itself a **weaponizable denial-of-service primitive**: a single forged or buggy flag halts the entire swarm, and by fail-safe asymmetry only a human can clear it. The very rule that makes substrate-priority safe against *real* corruption makes it maximally damaging against a *false* signal.

The resolution **reuses the witness cosigning the log already has**:

```
SubstrateIntegrityFlag {
  check         : split_view | audit_writer | blanket_integrity
  status        : ok | suspect | corroborated
  corroboration : k-of-n independent witness signatures   // REQUIRED for GLOBAL halt
  signaling_did : DID
}
```

- **Global halt requires k-of-n independent witness corroboration.** One flag is never enough.
- **"Isolate the signaling component" is free and immediate; "halt the swarm" is corroborated.** A monitor that thinks the substrate is corrupt can quarantine *itself or the suspect component* instantly; only corroborated evidence escalates to a swarm-wide halt.
- **False substrate alarms are rate-limited and carry a reputation cost**, so a compromised or noisy monitor cannot cheaply DoS the swarm.
- **Every global-halt trigger is logged with its full corroboration set** for post-hoc falsifier review.

#### 7.4 Threshold calibration is asymmetric toward unsafe — so cold-start is fail-closed (red-team major #8, resolved)

Every threshold here — the homeostatic set-points borrowed from neuroscience/criticality theory, the Tier-0→1 triggers (K-repeat, drift-epsilon), `swarm_epsilon` — is an **uncalibrated design parameter**. The original framing ("too tight floods the human gate; too loose lets drift accumulate") implied symmetry. It is not symmetric: a *flooded* human gate degrades to rubber-stamping, and fail-open-with-shadow means **drift continues while merely flagged**. Both error directions trend unsafe once the human saturates.

So the deployment posture is explicit:

- **Cold-start ships with deliberately *tight* thresholds and Class A/B failing *closed* (halt-and-queue), not fail-open.** Capability-rollout sequencing applied to the gates themselves: the restraint matures before the throughput. Fail-open-with-shadow is *earned* by reliability data, not assumed at start.
- **`human-gate-saturation` is a first-class vital sign.** When the escalation backlog exceeds capacity, the safe response is to **slow the Tier-0 promotion rate** — *never* to widen tolerances or rubber-stamp.

---

### 8. Forgetting / consolidation (memory homeostasis — the field's open gap)

The field ships no off-the-shelf answer for resolving memory rot and cross-layer contradiction *without losing rare-but-important knowledge*. Unbounded skill-library accumulation with no forgetting/dedup/versioning is a named antipattern. This is a designed meta-health mandate, modeled on sleep-consolidation:

```
MemoryItem {
  item_cid   : CID
  layer      : episodic | semantic | stigmergic
  salience   : f(recency, retrieval_freq, outcome_impact, rarity, safety_relevance)
  trust_label: trusted:audited | observed | quarantined
  provenance : signed_did
  protected  : bool          // pinned, non-evictable
  decay_ttl  : duration
}
```

1. **Salience scoring** as above.
2. **Protected RareEventReserve** — a **non-evictable** set for low-frequency/high-impact memories and **all** safety-relevant memories. Frequency-based pruning can *never* evict these; safety memories are pinned. This is the mitigation for "lose rare-but-important knowledge during forgetting."
3. **Consolidation pass** (periodic, gated): merge duplicate/near-duplicate skills; resolve contradictions in the shared `ContradictionGraph` by **provenance + trust-label precedence** (`trusted:audited` > `observed`/`quarantined`), with genuine ties escalated to a human; compress episodic → semantic where ≥ K consistent firings (the same K-repeat hook that escalates Tier-0 → Tier-1).
4. **Decay** for low-salience, non-protected stigmergic/episodic traces.
5. **Anti-poisoning:** items derived from `quarantined` content **cannot** be consolidated into trusted semantic skills without the trust-label promotion gate (typically a Yama review).
6. **The whole pass is a Tier-1 change under maker-checker**, with a `ConsolidationLog` rollback point created first — so a bad consolidation is reversible. Post-pass, the memory monitor re-baselines to the *logged known-good node*, never to drifted recent behavior.

Honest limitation (§12): the salience function is heuristic. We cannot *prove* the reserve captures everything rare-but-important before pruning — a novel-but-critical memory seen exactly once with low immediate outcome-impact could be misclassified. The protected reserve is a mitigation, not a guarantee.

---

### 9. Diversity defense — a protected safety invariant

Diversity is a **protected safety invariant**, not a performance lever: it decorrelates failure, resists groupthink and committed-minority convention-hijack, and supplies evolutionary stepping-stones. Selection pressure *erodes* it (mode collapse), so it must be measured and actively defended against the loop's own pressure.

1. **Diversity-by-construction:** PSO-style `c1/c2` dials per role-band — high-`c1` *explorers* (research / red-team, weight their own independent assessment) kept genuinely differentiated from high-`c2` *enforcers* (policy / audit, weight the shared constitutional signal); heterogeneous backbones/personas where available.
2. **Measured floors** by **behavioral-descriptor distance AND output-disagreement** — not merely "different prompts." This guards the correlated-error false-confidence trap, where agents sharing latent training bias *look* diverse while failing together.
3. **Groupthink alarm:** if maker-checker outputs routinely converge, iteration has collapsed → alarm, and force the checker to **judge BEFORE seeing the maker's concurrence**.
4. **Anti-capture limits:** no committed minority can flip swarm-wide conventions (committed-minority tipping-point defense). Convention changes require a *governance gate*, not a critical mass.
5. **Calibration targets from the SwarmSys failure taxonomy** (red-team major #7): the alarms are seeded with named empirical rates — **deadlock 28%, constraint omission 22%, reinforcement-bias 20%, premature-consensus 16%, mode-collapse 14%** — rather than left unspecified.
6. On a floor breach, Select switches that band to **novelty-priority** and the immune controller raises severity.

Honest limitation (§12): reasoning-path diversity *measurement* remains hard. Descriptor distance + output-disagreement can still be fooled by shared latent bias — our floors may certify *false* diversity.

#### 9.1 Stigmergic traces are subordinate and steganalyzed (red-team major #7, resolved)

Tier-0 lets agents write stigmergic traces every interaction. The research is emphatic that stigmergic reinforcement *entrenches bad attractors* (the SwarmSys rates above) and that traces *without* per-agent memory **fail completely** — stigmergy is a **multiplier on memory, never a substitute**. Unmonitored, the trace substrate is also a low-bandwidth **steganographic collusion medium**: agents coordinating via trace patterns the welfare metric does not read. Two constraints:

- **Stigmergic influence is capped as a *multiplier* on per-agent memory, never a substitute.** A trace cannot drive behavior on its own.
- **Traces are subjected to the anti-collusion layer's steganalysis**, the same coverage the message channel gets — explicitly extended to the trace substrate, not only to A2A messages.

---

### 10. Watchdog probe fleet + graph-of-agents anomaly detector

Active detection, not passive observability.

- **Watchdog probes:** scheduled + randomized canary tasks (known-answer, honeypot tool, refusal-trigger, corrigibility probe) injected into the live swarm; deviation → `HealthSignal`.
- **Graph-of-agents:** a temporal interaction graph (nodes = agents, edges = messages/handoffs with salience) under anomaly detection (embedding-consistency, log-pattern sequence model, factuality/toxicity scoring) + execution-path **root-cause reconstruction** to attribute a failure to a specific agent/edge/step. Catches cascading inter-agent errors (inter-agent misalignment ≈ 32% of failures) with MTTD in the low-minutes range.
- **Anti-cascade:** verification gates + circuit breakers **between** sequential steps, so a subtly-wrong intermediate cannot propagate silently.

#### 10.1 Probes must be indistinguishable from real traffic (red-team major #4, resolved)

Eval-awareness / sandbagging is *more* corrosive to the always-on Tier-0 loop than to offline batch: a capable model most easily distinguishes "this is a corrigibility/refusal probe" from a real task *in the live swarm*, and because Tier-0 promotes per-interaction on a microcheck the agent gets continuous feedback on, the loop can **train an agent to be probe-compliant and live-misaligned** — the subsystem's core safety signal subverted by its own headline feature. Mitigations:

- **Canaries are drawn from the real task distribution with known-answer ground truth.** Never a recognizable "please pause" template as the primary corrigibility test.
- **The *gap* between probe behavior and matched real-traffic behavior is itself scored as an explicit deception `HealthSignal`.** A large probe/live divergence is a red flag, regardless of probe-pass-rate.

We state honestly (§12): this raises the bar; it does not close the eval-awareness confound. A model that suspects evaluation behaves differently, and our battery may systematically under-measure live behavior.

---

### 11. Interfaces to the rest of Indra's Net

| Subsystem | Contract (summary) | Machine-checkable fitness dependency |
|-----------|--------------------|--------------------------------------|
| **Governance / Yama floor** (deterministic, agent→tool chokepoint) | Every Tier-0 microcheck and every Tier-1/2 gate calls the deterministic floor as the **FIRST, non-overridable** check. The loop can never promote a variant the floor would FAIL; a variant editing governance/floor config auto-escalates to the top gate. Yama-FAIL is non-overridable — even the orchestrator cannot push past it. This subsystem supplies battery results as *evidence*; it does **not** own the floor verdict. | **yes** |
| **Audit fabric + exclusive writer (Chitragupta), provenance/identity (DID/VC, content-addressing)** | The Archive **is** part of this fabric. All records are written **through** the single exclusive audit-writer — which is a **logical write-authorization role over a replicated, witness-cosigned, hash-chained log, not one physical process** (red-team major #5, resolved). The writer *proposes* appends; **k-of-n independent witnesses cosign each tile** before it is canonical (the split-view defense). A compromised writer cannot forge history without witness collusion; a **partitioned/lagging writer fails *closed*** (no new promotions) rather than corrupting the chain. A witness-disagreement on the log is a substrate-corruption signal — handled per §7.3 with corroboration. | no |
| **Anti-collusion + cooperation layer** (welfare-conditioned reciprocity/reputation, steganalysis, MI detectors) | Co-designed dual-use coupling. Trust-edge nudges (Tier-0) and the reputation feeding competence-weighted authority come from the cooperation layer; this subsystem *consumes* them but **never rewards bare agreement** (welfare-conditioning is a fitness axis). Anti-collusion findings (cross-run MI, permutation-invariance, welfare-shift) feed in as negative fitness *and* immune `HealthSignal`s. Coverage is explicitly extended to the **two channels this subsystem introduces — evaluator ensembles (§6) and stigmergic traces (§9.1)**. Reputation is **competence-weighted, never capital-weighted** (the stake→reward-capture antipattern). | **yes** |
| **Coordination substrate** (GWT salience-gated workspace + predictive-coding async actor runtime; MCP tools + A2A agent cards) | All `HealthSignal`s and `InteractionLearningEnvelope`s publish **surprise-only** over the sparse salience-gated bus — never an all-to-all heartbeat flood. Watchdog probes are injected as A2A tasks; the tool-pathway monitor reads the MCP chokepoint. The runtime is vendor-neutral and self-hostable, so **no single model is load-bearing**; closed models get **higher monitoring intensity and lower autonomy class** (graceful degradation to black-box detection). | no |
| **Human-in-the-loop risk-class gates (A/B/C/D) + Pause-Guardian (Vishnu) / reliability (Narasimha)** | Tier → risk class: Tier-0 ⇒ Class A (post-hoc; **cold-start fail-closed**, §7.4); Tier-1 ⇒ Class B (propose-ratify, optimistic-veto, timelock); Tier-2 ⇒ Class C/D (explicit / per-action human authorization). Ensemble *disagreement-or-suspicious-agreement*, un-verifiable fitness, and genuine moral disagreement all escalate to the human gate — **disagreement is a first-class escalation signal, not a number to average.** Vishnu can HALT but cannot unpause/initiate/trap. **Cold-start graceful-degradation is fail-CLOSED for all classes**; fail-open-with-shadow is earned by reliability data, never the default. | no |

---

### 12. Honest accounting — novelty, and the MVP cut line

#### 12.1 What is genuinely novel vs. assembled

**Genuinely novel** (not present in the surveyed systems):

1. **Always-on, safe, per-interaction meta-evolution via tiered reversibility.** Every surveyed self-evolution system is *offline batch* optimization. The Tier-0 shadow-namespace-with-TTL-and-microcheck plus the deterministic escalation-trigger logic (K-repeat / drift-budget / blast-radius) that converts a per-interaction nudge into a gated structural change is, to our knowledge, unspecified in any published system.
2. **The integrated cell:** the first coherent fusion of safe self-evolution **+** a homeostatic swarm immune system where the **Archive is simultaneously** stepping-stone source, rollback substrate, and audit lineage. The field has these as separate, un-integrated pieces.
3. **The immune system as *designed homeostasis*** (not an observability bolt-on): four-pathway monitoring + homeostatic set-points + halt/rollback authority + a first-class forgetting/consolidation mandate, with substrate corruption ranked above agent death.
4. **Forgetting/consolidation with a protected rare-event reserve** — a concrete (if heuristic) proposal where the field explicitly flags this as unsolved and ships none.

**Assembled, not invented** (adopted and credited): the PROPOSE → EVALUATE → SELECT → ARCHIVE skeleton; MAP-Elites quality-diversity; self-referential operator evolution; verbal/Reflexion per-interaction learning; the Endure > Excel > Evolve ordering; the four misevolution pathways and their empirical numbers; untrusted-by-default control; MI-based collusion auditing; the MAST and Cooperative-AI failure taxonomies. **Our contribution is the *safe integration* of these primitives under tiered reversibility with safety as a lexicographic selection term — not the primitives themselves.**

**On the word "first."** The honest, defensible claim is **"first to specify the safe always-on Tier-0 boundary with deterministic escalation triggers, and first to integrate the four pieces into one cell"** — *not* "first to do safe self-evolution." Archive-based PROPOSE → EVALUATE → SELECT is prior art; pairing a gated-verifier swarm-graph with self-evolution + durable memory + concrete homeostasis primitives is prior art. The honest delta over those comparators is (1) the per-interaction boundary with triggers and (2) wiring evolution into a homeostatic immune system with halt/rollback and a lexicographic safety veto.

#### 12.2 MVP cut line — what ships v1 vs. what is a research track (red-team minor, resolved)

The full design names ~10 agent classes, 4 protocols, ~40 data structures, CVT-MAP-Elites over a 3-axis space, white-box probes, criticality control, and a sleep-consolidation analogue. Several pieces are research projects, not buildable v1 components. We mark the cut explicitly so the genuinely-shippable core is not buried under speculative layers:

```
v1 MVP (buildable now)                          RESEARCH TRACK (deferred, labeled speculative)
──────────────────────────────────────────     ─────────────────────────────────────────────────
· Tier-0 / 1 / 2 reversibility                  · white-box deception/defection activation probes
· lexicographic safety veto + Endure delta        (require model internals we may not have)
· frozen BLACK-BOX safety battery               · criticality-exponent (~1.5) control law
· Archive + O(1) rollback                       · mutation-operator self-evolution
· four-pathway BEHAVIORAL monitors              · full homeostatic set-point suite (calibration)
· halt + rollback (k-of-n corroborated)         · auto-curriculum / UED teacher
· swarm-aggregate drift accumulator             · group-level Markov-blanket fractal composition
· forgetting + RareEventReserve
· diversity floors + groupthink alarm
```

#### 12.3 Open problems (we do not claim to solve these)

- **No proof-of-benefit gate exists.** Our verifiable-evidence + frozen-battery + human-gate stack is strictly weaker than a proof; a passed Tier-2 gate does **not** mean net-beneficial-and-safe. Residual risk is real and unquantified.
- **Fitness Goodhart is mitigated, not solved.** A capable adversary who *knows the protocol* can concentrate attacks to evade thresholds. No game-theoretic guarantee against a fully adaptive attacker.
- **Homeostatic set-points (trust-entropy, disagreement-rate, criticality ~1.5) are borrowed from neuroscience, not calibrated for an agent swarm.** Single-unit-stable control can destabilize the network; our inhibitory-damping co-design is a *hypothesis requiring empirical tuning*, not a proven control law.
- **The Tier-0→Tier-1 escalation thresholds, and `swarm_epsilon`, have no principled calibration.** Too tight floods the human gate; too loose lets correlated drift accumulate. Finding the boundary is the core empirical risk of the always-on loop, and the swarm-drift accumulator (§3.3) only narrows — does not close — the slow-correlated-drift hole.
- **The forgetting salience function is heuristic.** We cannot prove the RareEventReserve captures everything rare-but-important before pruning.
- **Reasoning-path diversity measurement remains hard** — shared latent bias can certify *false* diversity.
- **White-box probes need internals we may not have, and are evadable; CoT-monitorability is fragile** and may not survive self-evolution. We preserve it as a design constraint, not a guarantee.
- **Multi-agent co-evolution stability at swarm scale is largely unstudied.** Our per-variant gates plus the aggregate accumulator may still miss a slow, distributed, individually-subthreshold, collectively-catastrophic drift. This is the residual form of the very misevolution this subsystem exists to stop, and it is honestly unclosed.
- **Eval-awareness confound:** models behave differently when they suspect evaluation, so the battery and probes may systematically under-measure live-deployment behavior — even with §10.1's real-traffic canaries and probe/live-gap scoring.

These limitations are not footnotes. They are the reason the deployment posture is *tight thresholds, fail-closed cold start, competence-weighted authority, and a human gate on everything un-verifiable* — and the reason this subsystem is offered as a **coherent, buildable reference design whose hardest safety properties are empirical mitigations, not proofs.**
