# First Principles — the Physics & Mathematics of the Swarm

> *Every jewel in Indra's Net reflects every other. This document is the lens-grinder's bench: it does not add a new jewel, it grinds the instruments that measure whether a reflection is real or a trick of the light. Where the rest of the corpus borrows physics as a name, this subsystem either turns the name into a computable, falsifiable instrument — or retires it, in writing, to aesthetic.*

## 0. What this subsystem is, and what it deliberately is not

The preceding subsystem documents repeatedly *name* physics — "edge of chaos," "criticality," "downward causation," "free energy," "fractal blankets," "avalanche exponent τ ≈ 1.5." They name these honestly, as **framing**, and several explicitly defer the load-bearing machinery to a research track (doc 05 §7.2.1; doc 06 §12.2). This subsystem is where that deferral is paid down. It is the **measurement-and-control spine** that converts three of those physics ideas into computable, certifiable machinery, and honestly retires the rest to framing **in writing, with a structural guard that prevents framing from ever becoming a control input.**

Three commitments define the subsystem and bound its claims:

1. **It introduces no new authority.** It mints no tokens, issues no spawn credentials, owns no floor verdict, and writes nothing to the audit log. It **measures, certifies, and constrains** decisions made elsewhere — and it hands every output to the subsystems that *do* hold authority (Yama, Vishnu, the immune controller, the Replication Authority) as **evidence**, never as a verdict.
2. **Every controller ships in SHADOW MODE first.** A controller in shadow mode measures and alarms but cannot drive a live actuator. Promotion to ACTIVE is *earned* against a frozen adversarial battery and ratified Class-B — never assumed at cold start (doc 06 §7.4). The reason is the constitution's own named failure: presenting rung-1 pattern dynamics (avalanches, attractors, "emergence") as rung-3 structural explanations. A controller that acted on an un-validated dynamical claim would *be* that failure.
3. **Every quantity self-declares its epistemic role.** Each metric carries a `physics_role ∈ {LOAD_BEARING_MECHANISM, DESIGN_CONSTRAINT, FRAMING_ONLY}`. `FRAMING_ONLY` quantities are *structurally barred* from control paths. This is the **Physics-Claim Honesty Ledger**, and it is the subsystem's deepest contribution: a built-in guard against the architecture deceiving *itself*.

This document is numbered **doc 12** in the design index and filed as `18-first-principles-physics-and-mathematics.md`; both names refer to the same subsystem.

### 0.1 The three load-bearing strands (and everything demoted)

```
                  THE PHYSICS OF THE SWARM — what is MECHANISM, what is FRAMING
  ┌──────────────────────────────────────────────────────────────────────────────────┐
  │  LOAD-BEARING MECHANISM (drives control, shadow-mode-first, caveat inline)         │
  │   (1) CAUSAL / INFORMATIONAL CLOSURE  → the fractal-governance admission gate       │
  │       (Rosas et al. 2024, arXiv:2402.09090) — graduates a level ADVISORY→AGGREGATE  │
  │   (2) PEARL CAUSAL DISCIPLINE         → rung-tag earned by do-calculus + refutation  │
  │       (DoWhy/PyWhy) — with BARO/NSigma shift-triage as first-line (arXiv:2408.13729) │
  │   (3) DYNAMICAL STABILITY             → σ-criticality control + neural-Lyapunov cert │
  │       (branching ratio σ, slightly-subcritical; region-of-attraction margin)        │
  ├──────────────────────────────────────────────────────────────────────────────────┤
  │  DESIGN CONSTRAINT (constrains/admits, may NOT be cited as the CAUSE of an outcome) │
  │   · PERCOLATION / TOPOLOGY MARGIN  (R<1 bound on replication, contagion, connectivity)│
  │   · RG / SCALE-INVARIANCE          (justifies ONE governance operator at each closed │
  │                                     level — a design choice, not a derived fact)     │
  │   · MDL / COMPRESSION              (unifies memory consolidation, parsimony, closure)│
  ├──────────────────────────────────────────────────────────────────────────────────┤
  │  FRAMING ONLY (explanatory prose ONLY — barred from every actuator and gate)        │
  │   ✗ Landauer / thermodynamics-of-computation   (keep MDL; drop the J/bit)           │
  │   ✗ STRONG emergence / literal downward causation (the closure test is its ONLY     │
  │                                                    residue)                          │
  │   ✗ Free-energy-principle-as-grand-unifier      (use active inference where it       │
  │                                                    computes; never as the explanation)│
  └──────────────────────────────────────────────────────────────────────────────────┘
```

Read the diagram as a contract: a quantity in the bottom band that is found wired to a controller is itself a **floor-honesty defect** and is reverted (§7). That is the whole point — the boundary between mechanism and metaphor is not a matter of taste here; it is mechanically enforced and itself auditable.

---

## 1. Component — Closure-Test Engine (the fractal-governance admission gate)

**`physics_role: LOAD_BEARING_MECHANISM`** · ships **SHADOW** (research-track; §9 cut line)

### 1.1 The problem it solves

Doc 05 §7.2.1 states the gap precisely: there is *"no robust detector for a silently-broken group-Markov blanket,"* which is *"why fractal decisions are `ADVISORY_ONLY`."* The `GroupBlanket` schema (doc 05, doc 01 §`GroupBlanket`) carries `decision_authority: enum { ADVISORY_ONLY, AGGREGATING }` annotated `// v1 = ADVISORY_ONLY`, **with no promotion path defined.** Governing a clan/division/swarm "as a unit" on an *epiphenomenal* level — one whose group-level variable is not actually a closed, sufficient description of its own dynamics — is the latent **SPOF-of-abstraction**: clan-level trust/governance computed on a silently-broken super-agent, propagating corrupt state upward through hierarchical ignition.

The Closure-Test Engine is a **shadow-mode, low-dimensional-only candidate detector** for the gap doc 05 §7.2.1 declared missing — operable on discretized, low-dimensional macro-variables, with **no scalable closure test yet for high-dimensional continuous agent state and no principled approximate-closure threshold** (§15 #1); the high-dimensional regime stays research-track. Within that regime it supplies the *only legitimate cash value of "downward causation"*: a level may be governed as a unit, and its group-Markov-blanket treated as real, **only if** its coarse-grained dynamics pass a falsifiable closure test.

### 1.2 Mechanism

Offline — from logged spike/envelope traces pulled read-only via `audit.tap`, **never from drifted live recent behavior** — the engine:

1. Defines a candidate coarse-grained macro-variable `V = f(member states)`: a consensus vector, a trust-entropy scalar, or a role-allocation histogram (the same vital-sign axes the homeostasis controller already tracks, doc 05 §6.2).
2. Discretizes the member micro-state sequence `X` and the macro sequence `V`, and builds an approximate **ε-machine** (causal-state / predictive-state representation, via Causal State Splitting Reconstruction) of each.
3. Tests two coupled criteria on **held-out** traces:

| Criterion | What it asks | Statistic | Pass condition |
|---|---|---|---|
| **Strong lumpability** | Does the micro causal-state partition refine into `V`'s partition such that `V` is itself Markov — `P(V'|V)` well-defined independent of micro-detail *within* a lump? | lumpability defect `L = max` over macro-states of the KL spread of micro→macro transition kernels within that lump | `L ≤ τ_lump` |
| **Informational closure** | Is the macro future conditionally independent of micro-detail given the macro present — `I(V_future ; X_present | V_present) ≈ 0`? | closure leak `ε_close = I(V';X|V) / H(V')` | `ε_close ≤ τ_close` |

Because *exact* closure is essentially never attained by a real heterogeneous swarm, the verdict is **graded**, with a margin and a bootstrap confidence interval that must exclude the null:

```
margin = τ_close − ε_close
verdict =  OPEN            if margin ≤ 0  OR  L > τ_lump  OR  CI overlaps null
           APPROX_CLOSED   if 0 < margin < δ_safe
           CLOSED          if margin ≥ δ_safe  AND  L ≤ τ_lump  AND  CI excludes null
```

A level rechecks on a schedule, on structural events (membership change, blanket re-sync), and on the emergence trigger (§2). **OPEN or low-margin ⇒ the level is NOT governed as a unit**, and Yama floor enforcement continues to read individual agents directly — preserving doc 05 §7.2.1 invariant 3 verbatim.

### 1.3 Schemas

```jsonc
ClosureCertificate {
  level_id, member_dids:[DID], macro_var_spec,
  epsilon_machine_cid:    CID,        // the inferred ε-machine, content-addressed
  lumpability_defect_L:   float,
  closure_leak_eps:       float,
  tau_lump, tau_close, delta_safe,
  margin:                 float,
  verdict:                OPEN | APPROX_CLOSED | CLOSED,
  n_samples,              bootstrap_ci: [lo, hi],
  computed_ts, recheck_due_ts,
  traces_window_cid:      CID,        // exact held-out window this verdict rests on
  physics_role:           "LOAD_BEARING_MECHANISM",
  caveat:                 "approximate-closure; no proven cutoff; sampling-heavy (§10)",
  sig
}
GroupBlanketUpgrade {                 // a Class-B governed action, NOT a self-applied edit
  level_id, from: ADVISORY_ONLY, to: AGGREGATING,
  closure_cert_cid: CID, witness_cosign: [sig], gov_class: B
}
```

Certificates are content-addressed and teed **read-only** into Akasha-Sutra via `audit.tap`. The upgrade itself is a Class-B governed action and is **not** written by this subsystem (Chitragupta remains the exclusive writer; §6).

---

## 2. Component — Emergence Vital-Sign Estimator (ΦID / effective-information probe)

**`physics_role: LOAD_BEARING_MECHANISM`** (as a *flag*, never a control gain) · ships **SHADOW**

### 2.1 What it is — and the trigger blind-spot the red-team caught

`Φ_syn` is a computable scalar that answers a narrow question: *is the swarm now acting as a collective?* On a rolling window it estimates the synergy / effective-information of candidate swarm-level variables (consensus, trust-entropy) relative to per-agent variables, using an integrated-information-decomposition (ΦID) or effective-information estimator over the discretized state. A sustained rise of `Φ_syn` above a learned baseline is a **trigger to run a fresh closure test** and consider escalating to level-level control.

The red-team correctly flagged the danger of making `Φ_syn` the **primary** trigger: ΦID is method-dependent, data-hungry, and biased in high dimensions (§10), and a collective dynamic can emerge *without* a `Φ_syn` spike — a low-synergy-but-strongly-coupled coalition, or one engineered to suppress its own synergy signature. If `Φ_syn` were the gate, a synergy-suppressing coalition would persist un-tested while governance kept reading it as independent agents. That is a detection blind-spot at exactly the place collusion/epiphenomenal-level risk lives.

**Resolution — `Φ_syn` is one trigger among several, never the gate.** A closure test fires on the logical OR of:

| Trigger | Source | Why it is independent of `Φ_syn` |
|---|---|---|
| **Scheduled recheck (the FLOOR)** | timer | Frequent enough that *no level goes long un-tested* regardless of any signal. This is the binding default. |
| **Structural event** | membership change, blanket re-sync (doc 05 §7.2.1) | Cheap, deterministic, already emitted. |
| **Coupling / mutual-information rise on the trust-edge graph** | doc 05 §5 trust-edge layer | A synergy-*suppressing* coalition still raises edge MI; this forces a test the suppressed `Φ_syn` would have hidden. |
| **`Φ_syn` rise above baseline** | this estimator | One signal among several; useful but never sufficient. |

`Φ_syn` is reported strictly as a diagnostic scalar with its method-dependence stated inline, and is **never** fed as a control gain or a quantitative governance number.

### 2.2 Schema and transport

```jsonc
EmergenceVital {
  level_id, phi_syn: float,
  estimator: PID_MMI | ccs | effective_information,
  window, baseline_anchor: CID, z_score,
  method_caveat: "PID has no canonical synergy measure; high-dim biased (§10)",
  physics_role: "LOAD_BEARING_MECHANISM",   // as a flag only
  ts
}
```

It is emitted as a `HealthSignal{ pathway: workflow, metric_id: emergence_phi_syn, value: phi_syn, baseline_anchor, z_score, severity, evidence_cid }` (doc 06 §7.1 schema, verbatim) over the existing salience-gated bus — **no new transport, no all-to-all heartbeat flood.** Doc 06's immune monitors and doc 05's homeostasis consume it on the channel they already read.

---

## 3. Component — Causal-Discipline Gate (DoWhy/PyWhy: Model → Identify → Estimate → Refute)

**`physics_role: LOAD_BEARING_MECHANISM` (as DISCIPLINE)** · ships **v1 MVP** in its cheap form (§9)

### 3.1 Purpose

The `WorkerOutputEnvelope` (doc 00 §4.2) carries `causal_rung: rung-1 | rung-2 | rung-3`. The Causal-Discipline Gate makes that tag **mechanically earned** rather than self-asserted. Any `rung-2` (interventional) or `rung-3` (counterfactual/structural) claim must pass do-calculus identification plus a refutation step before it is admitted to the audit fabric at the claimed rung; otherwise it is **down-tagged** to rung-1 with a recorded reason. This is the architecture's built-in anti-self-deception mechanism against its single most-flagged failure: rung-1 pattern dressed as rung-3 explanation.

### 3.2 Mechanism — the four-step ladder

When an envelope carries `causal_rung ∈ {rung-2, rung-3}` with a declared causal claim, the gate runs, inline at the honesty-check step of the request trace (doc 00 §4.3 step 5):

```
(1) MODEL    claimant supplies (or gate infers) a DAG over the named variables
(2) IDENTIFY attempt do-calculus identification of the estimand
             (back-door / front-door / instrumental-variable)
             └─ non-identifiable ⇒ FAIL → down-tag
(3) ESTIMATE compute the effect + confidence interval
(4) REFUTE   placebo-treatment · random-common-cause · data-subset refuters
             └─ effect vanishes under placebo OR flips under subset ⇒ FAIL → down-tag
PASS (identifiable AND survives refutation) ⇒ attach CausalAttestation, admit at declared rung
```

### 3.3 The audit-immutability fix (red-team major #1 — resolved, load-bearing)

The original design said the gate *"rewrites `envelope.causal_rung` to rung-1."* **That is prohibited and is the most serious coherence/security defect.** Doc 00 §4.2/§4.3 fixes that *every actual occasion emits exactly ONE signed `WorkerOutputEnvelope`* carrying `prev_audit_hash`/`this_hash`, signed by the occasion's DID key. Mutating a field of a signed, content-addressed envelope either invalidates the occasion's signature and the hash-chain, or forces the gate to re-sign it — silently introducing a **second writer/mutator** of a record the architecture treats as immutable and single-signer. Either path collides with the Chitragupta-exclusive-writer invariant and the **no-silent-rewrite** property that is Akasha-Sutra's entire reason for existing (doc 04 §4.2 — the writer's vocabulary has *no `edit`/`delete`/`reorder` verb at all*). Worse, a clever agent that learns the gate will overwrite its rung tag gains a sanctioned in-band channel that touches signed envelopes pre-admission.

**Resolution — never mutate the signed envelope. Supersede it with a separate signed attestation.**

- The occasion's original `causal_rung` claim and signature stay **immutable**.
- The gate emits a **separate** signed `CausalAttestation` that Chitragupta chains as its own record, linked to the original envelope via `causal_parents` / `refs` (doc 04 `AuditRecord.refs`, doc 05 `Spike.causal_parents`).
- The attestation **supersedes** the rung for all downstream consumers. Consumers resolve `effective_rung = latest UPHELD/DOWNTAGGED attestation referencing this claim`, **not** the raw envelope field.

This preserves one-occasion-one-signed-envelope, keeps Chitragupta the sole writer, and makes the down-tag itself a **first-class auditable event** rather than an in-place edit.

```jsonc
CausalAttestation {
  claim_id, envelope_cid: CID,        // the ORIGINAL signed envelope — never mutated
  declared_rung, dag_cid: CID,
  estimand, identified: bool,
  method: backdoor | frontdoor | iv | none,
  estimate: float, ci: [lo, hi],
  refuters: [ { name, p_value, survived: bool } ],
  verdict: UPHELD | DOWNTAGGED,
  final_rung, reason, ts, refs: [record_id], sig
}
// Downstream consumers compute:
effective_rung(claim_id) = latest CausalAttestation.final_rung  (fallback: envelope.causal_rung)
```

### 3.4 The bright-line scope fix (red-team major #2 — resolved)

The original design routed *"asserted rung-3 with zero identification"* to Yama as a **bright-line** floor-honesty event. **This over-reaches doc 03 §6**, which draws the bright-line narrowly and precisely. We align to doc 03 §6 verbatim:

| Honesty condition | Class per doc 03 §6 | Who adjudicates |
|---|---|---|
| `rung-3` tag with **NO causal-model ARTIFACT attached** (a *presence check on a DAG*) | **Bright-line FAIL (deterministic)** | Yama — structural artifact check |
| Estimand **non-identifiable even WITH a DAG attached** (do-calculus verdict, model-dependent) | **Detected-and-escalated (probabilistic)** | ETHICS_REVIEW + anekantavada lens (doc 03 §9) |
| Refutation failure (placebo/subset) | **Detected-and-escalated (probabilistic)** | ETHICS_REVIEW + anekantavada lens |
| Over-assertion under genuine uncertainty (rung-1 *content* dressed as rung-3 *reasoning*) | **Detected-and-escalated (probabilistic)** | ETHICS_REVIEW + anekantavada lens |

The reasoning is doc 03 §6's own: a do-calculus *identifiability* verdict itself depends on a claimed DAG that may be wrong, so promoting it to a deterministic bright-line over-states enforceability and risks **false-positive floor violations on honest-but-hard causal claims** — which would erode trust in the floor and create pressure to loosen it (the opposite of honesty enforcement; see §8). **The gate produces EVIDENCE for the semantic honesty judge; it never owns a bright-line verdict on identifiability.** The genuine bright-line — a `rung-3` tag with zero causal-model artifact — is the *only* thing it surfaces to Yama, and there it surfaces the **already-existing** doc 03 §6 structural check, not a new one.

On `DOWNTAGGED`, the gate writes the reason into a new audit record and references it from the original claim; where doc 03 §6 *additionally* finds the genuine artifact-absence bright-line, that is Yama's structural check firing, with the **REPARATIVE** disclose→correct→restore path available (doc 00 §4.2, doc 03 §13).

### 3.5 Honest scope

This gate validates rung **claims**. It does **not** perform live counterfactual root-cause — that is near-random at scale (§4). Heavy SCM use is opt-in for small, well-modeled sub-swarms only (§4.3).

---

## 4. Component — First-Line Distribution-Shift Triage (BARO / NSigma)

**`physics_role: LOAD_BEARING_MECHANISM`** (and a deliberate anti-overclaim choice) · ships **v1 MVP** (§9)

### 4.1 Why distribution-shift detectors come *first*

The strongest 2024 benchmark (arXiv:2408.13729) shows simple distribution-shift detectors **beat** causal-discovery root-cause at scale and under timing noise. Wiring heavy causal machinery as the immune system's localization engine would gain the audit fabric and immune system **false confidence**. So the first-line localizer is deliberately *not* SCM counterfactual root-cause.

### 4.2 Mechanism

Maintain per-metric, per-agent, and per-edge rolling baselines. On an immune alarm, run a **BARO**-style multivariate Bayesian online change-point detector plus an **NSigma** robust z-threshold pre/post hypothesis test to **rank** which metrics/agents/edges shifted first and hardest. Output a ranked suspect list with shift magnitudes. This feeds doc 06's four-pathway monitors (§7.1) as their **localization layer**.

### 4.3 The escalation discipline

```
immune alarm ─► BARO/NSigma ranked suspects ─► top-ranked SMALL subgraph?
                                                  │
                          well-modeled AND identifiable (do-calculus)?
                          ├─ yes → escalate ONLY this subgraph to SCM counterfactual
                          │         (the §3 gate), honestly rung-tagged on result
                          └─ no  → STOP at ranked-shift evidence; immune system acts on it,
                                    honestly tagged rung-1 / rung-2 (never rung-3)
```

SCM counterfactual root-cause is invoked **only** on the top-ranked small subgraph if it is well-modeled and identifiable; otherwise triage stops at ranked-shift evidence. The immune system acts on that — honestly tagged — rather than on a near-random causal story.

```jsonc
ShiftTriage {
  alarm_id,
  ranked_suspects: [ { entity_id, metric_id, pre_dist, post_dist,
                       shift_magnitude, change_point_ts, score } ],
  method: baro | nsigma,
  scm_escalated: bool, scm_subgraph_cid: CID | null,
  physics_role: "LOAD_BEARING_MECHANISM", ts
}
```

Emitted as `HealthSignal{ pathway: model | memory | tool | workflow, ... }`, slotting under doc 06 §7.1 monitors as their localization engine.

---

## 5. Component — Branching-Ratio (σ) Criticality Controller

**`physics_role: LOAD_BEARING_MECHANISM`** · ships **SHADOW** (research-track; measurement-only at cold start, §9)

### 5.1 Purpose and the σ-vs-τ distinction (red-team minor #3 — resolved)

Doc 05 §6.2 and doc 06 §7.2/§12.2 set a vague *"criticality `tau` ≈ 1.5 (avalanche exponent)"* target and list online criticality control as an **unsolved research-track item** (doc 06 §12.2). This component turns that into a measured, controlled, safety-biased variable — but it must first **correct a category error** in its own original framing.

> **τ and σ are DISTINCT criticality observables.** Doc 05 §6.2 / doc 06 §7.2 define **τ as the avalanche-size power-law EXPONENT** (≈ 1.5). The **branching ratio σ** is the expected number of descendant events per event. They are *linked at criticality* (a critical branching process gives σ → 1 and an avalanche-size exponent near 1.5) but they are **not the same quantity**, are estimated by different methods, and have different targets and units. Treating "control σ to 0.95" as "control τ to 1.5" is exactly the rung-1-pattern-looseness the Honesty Ledger exists to forbid.

**Resolution.** The σ-controller **supersedes** the ill-posed direct-exponent set-point — it is a better-conditioned, subsampling-robust *controllable* variable — and it carries τ as a **derived, secondary read-out**, not as the control target:

| Observable | Role here | Estimator | Target |
|---|---|---|---|
| **σ — branching ratio** | the **control variable** | Wilting–Priesemann multi-step **MR regression** (robust to subsampling; *not* naive power-law slope-fitting) | **σ\* ≈ 0.95** (quasicritical, slightly subcritical) |
| **τ — avalanche-size exponent** | secondary derived read-out only | reported alongside, never fitted as a set-point | ≈ 1.5 *expected* at criticality; descriptive, not actuated |

### 5.2 Mechanism — quasicritical, deliberately slightly-subcritical

Estimate σ online from cascade-size / ignition-avalanche distributions on the Spike Bus (doc 05 §2). Target **σ\* ≈ 0.95**: near-critical computational capacity, while keeping contagion **R < 1**. This unifies two usually-separate goals — *near-critical for computation, sub-critical for contagion containment* — in one number.

The actuator is **not new**: it is the Homeostasis & Neuromodulation controller's existing inhibitory term (doc 05 §6.3 hormone-vector inhibition channel):

```
σ̂ drifting UP toward 1   ─► request INCREASED inhibitory recruitment / threshold damping
σ̂ too LOW                ─► request a GOVERNED loosening (doc 05 §6.5 — bounded by the
                            diversity floor; NEVER autonomous unbounded loosening)
σ̂ ≥ 1 sustained          ─► emit SUPERCRITICAL cascade-storm alarm to the immune controller
                            (doc 06 §7.2), which holds HALT + rollback authority
```

This **must be co-designed at the network level** — per-unit homeostasis is the documented seizure-like failure mode (doc 05 §6.2; research2 avoid-list). The controller drives the *existing network-level inhibitory channel*, never per-agent set-points. An ACTIVE σ-controller's inhibition remains hard-bounded by the `diversity_index` and `disagreement_rate` floors exactly as doc 05 §6.5 requires — *inhibition is cheap but not unconditionally safe*; over-damping that would push diversity below floor is itself blocked.

### 5.3 Schema

```jsonc
CriticalityState {
  scope: clan | division | swarm,
  sigma_hat: float, sigma_ci: [lo, hi], sigma_target: 0.95,
  estimator: MR_regression,
  tau_exponent_readout: float | null,   // DERIVED, secondary, never the control target
  avalanche_window, drift_rate,
  mode: SHADOW | ACTIVE,
  alarm: none | approaching_critical | supercritical,
  physics_role: "LOAD_BEARING_MECHANISM",
  caveat: "no proven hold-at-quasicriticality under non-stationary load (§10)",
  ts
}
```

The σ-alarm rides the doc 06 §7.2 cascade/oscillation vital-sign as a `HealthSignal` — no new actuator, no new transport.

---

## 6. Component — Neural-Lyapunov Stability Certifier

**`physics_role: LOAD_BEARING_MECHANISM`** (with an honest locality caveat) · ships **SHADOW** (research-track; §9)

### 6.1 Purpose

Give the homeostasis layer formal, computable stability margins — a certified region-of-attraction and a measured **distance-to-tipping-point** — and reframe the v1's empirically-listed failure modes (mode-collapse, oscillation, premature-consensus) as *predictable bifurcations* rather than post-hoc diagnoses.

### 6.2 Mechanism

Define a candidate Lyapunov function `V(s)` over collective state `s = (trust-entropy, role-allocation, consensus, diversity-floor occupancy)` — the doc 05 §6.2 vital-sign axes. Learn a neural-Lyapunov certificate (Chang-style learner + counterexample-guided falsifier) certifying `V > 0` and `V̇ < 0` over a basin `B` around the healthy operating point. This yields a certified region-of-attraction and a scalar **`margin_to_boundary` = distance from current `s` to `∂B`**.

The v1 failure modes map to named bifurcations:

| v1 empirical failure (doc 05 §6.1 / doc 06 §9) | Named bifurcation | Lyapunov signature |
|---|---|---|
| **Premature-consensus** | saddle-node | trust-entropy collapse toward a fixed point |
| **Oscillation / seizure-cascade** | Hopf onset | growing periodic orbit; `V̇` sign change on a cycle |
| **Mode-collapse** | basin exit | `s` crosses `∂B` at the diversity-floor face |

### 6.3 As an admissibility input to meta-evolution (never the floor verdict)

A Lyapunov-**decrement** constraint is added to swarm-level adaptation/meta-evolution updates. A proposed parameter change that the certifier cannot show keeps `V̇ < 0` inside `B` returns `ESCALATE`, **bumping the proposal's tier** in doc 06's tiered-reversibility gate. This is an **admissibility input** to the fitness/tier decision — explicitly **not** the floor verdict, which always belongs to Yama.

```jsonc
LyapunovCertificate {
  scope, V_spec_cid: CID, basin_B_spec,
  certified: bool, falsifier_counterexamples: [s],
  margin_to_boundary: float,
  learner: nn_lyapunov,
  validity_caveat: local_nonstationary,   // certificates are LOCAL & model-dependent
  mode: SHADOW | ACTIVE,
  physics_role: "LOAD_BEARING_MECHANISM",
  ts, sig
}
AdaptationStabilityCheck {
  proposal_cid: CID, predicted_Vdot: float, within_basin: bool,
  verdict: PASS | ESCALATE, tier: 0 | 1 | 2
}
```

### 6.4 Honest caveat

Certificates are **local and model-dependent**; in genuinely non-stationary MARL (every agent in every other's environment) no global guarantee exists. The margin is a **distance-to-tipping-point indicator, not a safety proof**, and it ships shadow-mode. This caveat travels with the certificate as a structured field, so a downstream consumer cannot silently treat the margin as a guarantee.

---

## 7. Component — Percolation / Topology Margin Monitor (design-constraint enforcer)

**`physics_role: DESIGN_CONSTRAINT`** · ships **v1 MVP** in its measurement form (§9)

### 7.1 A one-sentence reconciliation (red-team coherence note)

The research mandate (research2) marks percolation `load_bearing: True`; this subsystem labels it `DESIGN_CONSTRAINT`. These are reconciled, not contradictory: **the percolation *thresholds* constrain/admit (a design constraint), while the *monitoring that computes the live margin against those thresholds* is the load-bearing mechanism.** The monitor is therefore an honest hybrid — it *measures* (mechanism) in service of a *constraint* — and it carries `physics_role: DESIGN_CONSTRAINT` because its **output is a bound, not a cause**: it may forbid an action (shard a hub, throttle an edge, deny a spawn) but it may **never be cited as the *cause* of robustness** (§8).

### 7.2 Mechanism — three live margins

On the live contact graph (trust-edge × message-influence), continuously compute:

| Quantity | Definition | Constraint |
|---|---|---|
| **LCC fraction + percolation margin** | largest-connected-component fraction; distance above the giant-component threshold | keep **above** it for coordination, **below** pure scale-free hub-fragility |
| **Compromise-contagion R** | effective transmissibility along edges | keep **R < 1** by sparsity + cross-agent corroboration before high-impact propagation |
| **Hub degree** | **message-influence × trust-weight** (NOT raw connection count) | strongest controls on highest-degree hubs |

**Hub identification is by influence×trust, not raw connections** — hubs are the "robust-yet-fragile" prime poisoning/attack target. The monitor applies **targeted** immunization (strongest monitoring + lowest autonomy on hubs) and feeds doc 05 §4.4 sharding to replicate/shard hubs. **Random immunization is explicitly rejected** — it fails on scale-free graphs.

### 7.3 The two safety-plane checks it feeds

```jsonc
TopologyMargin {
  lcc_fraction: float, percolation_margin: float, contagion_R: float,
  hubs: [ { did, influence_x_trust, immunization_level } ],
  replication_Reff: float,
  verdict_flags: [ shard_hub | throttle_edge | corroborate_required ],
  physics_role: "DESIGN_CONSTRAINT", ts
}
```

- **Replication R_eff < 1 budget check ──► the Replication Authority.** The monitor returns a lineage-wide effective-reproduction estimate as a **budget check** to the quorum-cosigned Replication Authority, so replication stays provably sub-critical / percolation-bounded. **This subsystem issues no spawn tokens and holds no replication authority** — it supplies a number; the Authority decides. The replication red-line (replication MUST NOT be coupled to an open fitness/selection loop) is *untouched* by this monitor: it constrains a metered channel; it does not create one.
- **Contagion R < 1 + corroboration-required ──► the inter-swarm relay/firewall.** Keeps the inter-swarm contact graph sparse and mesh-corroborated, with the strongest controls on hubs and independent cross-agent corroboration before any high-impact claim propagates.

---

## 8. Component — MDL Consolidation Objective (memory / level unification)

**`physics_role: DESIGN_CONSTRAINT`** (the load-bearing half of thermodynamics-of-computation) · ships **v1 MVP** (§9)

### 8.1 One objective, three jobs

Minimize **description length** (MDL) = the free-energy *complexity* term = closure's *sufficiency* criterion. This single objective replaces ad-hoc summarization in doc 06 §8 / doc 07 and ties three things together:

1. **Memory consolidation** — consolidate episodic logs into the shortest predictive-sufficient description (hierarchical/lumpable abstraction).
2. **Model parsimony** — selective forgetting drops bits whose predictive value < storage/interference cost.
3. **Level discovery** — *a closed level (§1) IS a compressed sufficient statistic*, so the same MDL score that ranks memory consolidations also scores candidate coarse-grainings, tying memory directly to the closure/fractal machinery.

```jsonc
MdlScore {
  item_or_partition_cid: CID,
  description_length_bits: float,
  predictive_sufficiency: float,
  marginal_gain: float,
  eligible_for_forget: bool,
  protected_override: bool,           // RareEventReserve / safety-pin → ALWAYS true-overrides
  physics_role: "DESIGN_CONSTRAINT"
}
```

### 8.2 Hard exclusions preserved

The protected **RareEventReserve** and **all safety-relevant memories** (doc 06 §8) are **non-evictable regardless of MDL** — `protected_override` hard-wins over `eligible_for_forget`. Quarantined-derived items cannot consolidate into trusted skills without the promotion gate (doc 06 §8 anti-poisoning; doc 07). The same `MdlScore` feeds doc 06 §8 `ConsolidationLog` and doc 07 memory salience, and is consumed by the §1 Closure-Test Engine to rank candidate macro-variables. Landauer's J/bit is *not* used here — only the compression/MDL half survives (§ Honestly-Demoted, below).

---

## 9. The Physics-Claim Honesty Ledger + the MVP-vs-Research cut line

### 9.1 The Honesty Ledger (the structural anti-self-deception guard)

Every quantity this subsystem emits self-declares whether it is mechanism, constraint, or framing — and the boundary is **mechanically enforced and itself auditable.**

```
physics_role ∈ { LOAD_BEARING_MECHANISM, DESIGN_CONSTRAINT, FRAMING_ONLY }
─────────────────────────────────────────────────────────────────────────────────────────
LOAD_BEARING_MECHANISM  may DRIVE control   — each shadow-mode-first, each caveat inline
DESIGN_CONSTRAINT       may CONSTRAIN/ADMIT — may NOT be cited as the CAUSE of an outcome
FRAMING_ONLY            explanatory PROSE   — PROHIBITED as a control gain or gate input
─────────────────────────────────────────────────────────────────────────────────────────
ENFORCEMENT:  a FRAMING_ONLY quantity found wired to a controller or gate is itself a
              floor-honesty defect (over-claim) and is REVERTED. The ledger is teed into
              Akasha-Sutra so the mechanism-vs-framing boundary is itself auditable.
```

**Honestly demoted to FRAMING_ONLY** (named, then disowned as mechanism):

| Demoted idea | Kept residue | Why demoted |
|---|---|---|
| **Landauer / thermodynamics-of-computation** | MDL / compression only (§8) | Invoking J/bit literally as a swarm mechanism is decorative; no actuator reads energy. |
| **Strong emergence / literal downward causation** | the closure test (§1) is its *only* residue | "The swarm is more than its agents" as *mechanism* is the rung-1-as-rung-3 trap; closure is the one falsifiable cash value. |
| **Free-energy-principle-as-grand-unifier** | active inference where it *computes* (doc 05 §7.2 EFE tie-breaker) | FEP-as-the-explanation is unfalsifiable framing; we use it operationally, never as the reason. |
| **Literal RG flow equations / fictitious critical exponents** | RG as *framing* that justifies one governance operator per closed level (§ below) | No demonstrated fixed point or measured critical exponents at swarm scale (§10). |

### 9.2 RG / scale-invariance — honest status

`physics_role: DESIGN_CONSTRAINT`. Renormalization/scale-invariance is invoked **only** to justify reusing **one identical governance operator at every *closed* level** (the doc 01 §`agent→clan→division→swarm` fractal formalism). This is a **design choice justified by RG framing + the closure test, not a derived fact** — we write **no literal RG flow equations** and claim no measured critical exponents. "Same governance law at every closed level" is licensed by §1's closure verdict (a level is only governed as a unit if it passes), not by an asserted RG fixed point.

### 9.3 MVP-vs-Research cut line (red-team minor #6 — resolved)

Doc 06 §12.2 placed *criticality-exponent control* and the *full homeostatic set-point suite* on the **research track**, not v1. This subsystem must mirror that cut explicitly so it cannot read as shippable-tomorrow when most of it is genuinely a research program.

```
 v1 MVP (cheap, high-value, low-risk — buildable now)        RESEARCH TRACK (shadow-mode + conservative defaults)
 ──────────────────────────────────────────────────────     ─────────────────────────────────────────────────────
 · DAG-artifact-presence bright-line  (ALREADY doc 03 §6)    · ε-machine CLOSURE inference (sampling-heavy; no
 · Causal-Discipline Gate cheap form: Model→Identify           scalable high-dim-continuous version — §10)
   on supplied DAGs (down-tag on non-identify), with the     · ΦID / Φ_syn emergence estimator (no canonical
   separate-superseding-attestation (§3.3)                     synergy measure; method-dependent — §10)
 · BARO/NSigma SHIFT-TRIAGE as immune localization (§4)      · neural-Lyapunov certificate + CEGIS falsifier (§6)
 · Physics-Claim Honesty Ledger as pure TAGGING discipline   · σ-criticality controller in ACTIVE mode (cold start
 · σ MEASUREMENT in pure-observability SHADOW (§5)             is measurement-only SHADOW)
 · Percolation/Topology MARGIN measurement (§7)              · GroupBlanketUpgrade ADVISORY→AGGREGATING promotion
 · MDL consolidation score feeding doc 06 §8 (§8)              (gated on a passed, witnessed ClosureCertificate)
                                                             · live SCM counterfactual on identifiable subgraphs
```

The cheap pieces ship first because they are validated assemblies (DoWhy refutation, change-point detection, content-addressed attestations) or pure discipline (the Ledger). Every ACTIVE controller and every ε-machine/ΦID/Lyapunov inference is research-track behind shadow mode and conservative defaults.

---

## 10. Protocols

### 10.1 Protocol A — Closure-Gated Level Promotion (`ADVISORY_ONLY → AGGREGATING`) · Class B

Resolves doc 05 §7.2.1's open problem: promoting fractal-blanket decisions from advisory to authoritative *only* on a passed, witnessed closure test.

```
1. TRIGGER (logical OR — §2.1): scheduled recheck (the FLOOR) · structural event
   (membership change / blanket re-sync) · trust-edge MI rise · Φ_syn rise above baseline.
2. Pull the level's member traces over the validation window from Akasha-Sutra
   (read-only audit.tap) — NEVER from drifted live recent behavior.
3. Closure-Test Engine builds the ε-machine; computes lumpability_defect_L and
   closure_leak_eps on HELD-OUT traces with a bootstrap CI.
4. VERDICT: margin ≥ δ_safe AND L ≤ τ_lump AND CI excludes null ⇒ CLOSED;
   else APPROX_CLOSED or OPEN. Emit a signed ClosureCertificate, teed into the audit fabric.
5. On CLOSED with adequate margin ⇒ emit a GroupBlanketUpgrade PROPOSAL (Class B).
   k-of-n witnesses cosign; on ratification the Mandala flips decision_authority
   ADVISORY_ONLY → AGGREGATING for that level.
6. INVARIANT (preserved verbatim, doc 05 §7.2.1 inv. 3): regardless of upgrade state,
   Yama floor enforcement always reads INDIVIDUAL agents directly — a CLOSED super-agent
   can NEVER mask a member-level floor violation.
7. On any later recheck returning OPEN or margin-loss ⇒ AUTO-DEMOTE AGGREGATING →
   ADVISORY_ONLY IMMEDIATELY (fail-safe asymmetry — demotion is free/single-signal),
   DE-COMPOSE the super-agent, raise a HealthSignal{severity: crit}.
```

The asymmetry is the doc 05 §5.3 / doc 00 §3.8 rule applied to abstraction itself: **promotion is gated + witnessed; demotion is free + single-signal.**

### 10.2 Protocol B — Rung-Earning Causal Attestation (audit-fabric admission) · Class A → floor-honesty on the genuine bright-line

Runs inline at doc 00 §4.3 step 5 (the honesty check), before doc 00 §4.3 step 6 (Chitragupta audit).

```
1. An actual occasion emits a WorkerOutputEnvelope with causal_rung ∈ {rung-2, rung-3}
   + a declared causal claim + cited evidence (signed; IMMUTABLE).
2. Causal-Discipline Gate runs Model→Identify→Estimate→Refute (DoWhy):
   build/inherit the DAG, attempt do-calculus identification, estimate, run
   placebo + random-common-cause + subset refuters.
3. Identifiable AND survives refutation ⇒ UPHELD: emit a SEPARATE signed CausalAttestation
   (refs → envelope_cid); Chitragupta chains it; downstream effective_rung = declared rung.
4. Non-identifiable OR refutation fails ⇒ DOWNTAGGED: emit a SEPARATE signed CausalAttestation
   with final_rung = rung-1 + reason. The original envelope is NEVER mutated; the attestation
   SUPERSEDES via causal_parents/refs. Route the model-dependent verdict to ETHICS_REVIEW +
   anekantavada (doc 03 §6/§9) — NOT to Yama as a bright-line.
5. If, AND ONLY IF, the original claim is a rung-3 tag with ZERO causal-model ARTIFACT
   attached ⇒ that is doc 03 §6's deterministic bright-line; Yama's structural check fires.
   REPARATIVE disclose→correct→restore path available (doc 00 §4.2, doc 03 §13).
6. Heavy live counterfactual root-cause is NOT run here; localization is delegated to
   First-Line Shift-Triage (§4), with SCM counterfactuals only on a small identifiable subgraph.
```

### 10.3 Protocol C — Quasicritical Homeostasis Loop (σ-control + Lyapunov-certified adaptation) · SHADOW first

```
1. Continuously estimate σ̂ from Spike-Bus avalanche-size distributions
   (MR regression — NOT slope-fitting) at clan/division/swarm scope.
2. Compare σ̂ to σ* ≈ 0.95: drifting UP toward 1 ⇒ request increased inhibitory recruitment
   via doc 05 §6.3 hormone inhibition channel; too LOW ⇒ request a GOVERNED loosening
   (doc 05 §6.5 — bounded by the diversity floor; never autonomous unbounded loosening).
3. σ̂ ≥ 1 sustained ⇒ emit SUPERCRITICAL cascade-storm alarm to the immune controller
   (doc 06 §7.2), which holds HALT + rollback authority. This controller cannot HALT.
4. In parallel, the Neural-Lyapunov Certifier maintains V over collective state and the
   certified basin B; report margin_to_boundary as a vital sign.
5. Any meta-evolution PROPOSAL (doc 06): predicted V̇ inside B? If not certifiable ⇒
   AdaptationStabilityCheck returns ESCALATE, bumping the proposal's tier. The floor verdict
   still belongs to Yama; this is only an admissibility input.
6. All set-point changes are append-only-tightening / falsifier-gated-loosening (doc 05 §6.4/§6.5
   posture). The controller CANNOT unpause a HALT (Vishnu asymmetry preserved).
7. PROMOTION SHADOW → ACTIVE is itself EARNED (§10.4) — never assumed at cold start.
```

### 10.4 Protocol D — SHADOW→ACTIVE Promotion (red-team minor #5 — resolved)

The σ-controller and the Lyapunov certifier, once ACTIVE, drive **live inhibitory restraint** — and inhibition is the documented dissent-suppression lever (doc 05 §6.5). "Accumulated reliability evidence" over shadow data is exactly the metric a meta-Goodharting operator (doc 06 §6 layer 6) could learn to satisfy while the controller drifts on un-tested axes, since shadow-mode reliability is measured against the same distribution the controller will then act on. So promotion is **not** bound to "reliability evidence" alone:

```
SHADOW → ACTIVE requires ALL of:
  (a) Pass against a FROZEN adversarial safety battery (doc 06 §4) + falsifier-agent gate
      (doc 06 §6.2) — held-out, not the shadow distribution.
  (b) Demonstrate that going ACTIVE does NOT regress the diversity_index / disagreement_rate
      floors (the Endure law, doc 06 §4, applied to the CONTROLLER itself).
  (c) Class-B ratification, whose loosening-of-restraint direction carries the named-falsifier
      ratchet (doc 03 §7 / doc 05 §6.4).
  (d) Standing invariant: an ACTIVE σ-controller's inhibition stays HARD-BOUNDED by the
      diversity floor (doc 05 §6.5). Over-damping below floor is blocked regardless of σ̂.
A single anomaly post-promotion ⇒ immediate automatic demotion to SHADOW (fail-safe asymmetry).
```

### 10.5 Protocol E — Physics-Claim Honesty Ledger (load-bearing-vs-framing tagging)

```
1. Each emitted metric carries physics_role + a one-line justification.
2. FRAMING_ONLY quantities (any Landauer-energy term, strong-emergence / downward-causation
   language, FEP-as-grand-unifier narration, literal RG flow equations) are PROHIBITED as
   control gains or gate inputs — explanatory prose only.
3. A FRAMING_ONLY quantity found wired to a controller/gate is itself a floor-honesty defect
   (over-claim) and is REVERTED.
4. DESIGN_CONSTRAINT quantities (percolation margin, RG-justified operator reuse, MDL) may
   constrain/admit but may NOT be cited as the CAUSE of an outcome.
5. LOAD_BEARING_MECHANISM quantities (closure verdict, σ̂, Lyapunov margin, causal attestation,
   shift-triage rank, Φ_syn-as-flag) may drive control — each shadow-mode-first, each caveat inline.
6. The ledger is teed into Akasha-Sutra so the load-bearing-vs-framing boundary is itself auditable.
```

---

## 11. Severity-vocabulary reconciliation (red-team coherence note)

Two severity vocabularies coexist in the v1 corpus: doc 05 uses `HEALTH_VITAL severity = high`; doc 06's `HealthSignal` schema uses `severity ∈ {info, warn, crit}`. This subsystem **emits over the doc 06 `HealthSignal` schema exclusively**, and therefore uses `{info, warn, crit}` at the emission boundary. The mapping at the bus edge is fixed: a doc 05 `HEALTH_VITAL severity=high` (e.g. a supercritical σ alarm or a closure auto-demotion) is emitted as `HealthSignal{ severity: crit }`. No new transport, one severity vocabulary at the wire.

---

## 12. Interfaces to the v1 subsystems

| Subsystem | What this subsystem PROVIDES | What it CONSUMES |
|---|---|---|
| **The Mandala — Neuromorphic Coordination (doc 05)** | (a) the Closure-Test Engine = the §7.2.1 missing blanket-integrity detector; graduates `GroupBlanket.decision_authority` ADVISORY_ONLY→AGGREGATING on a witnessed `ClosureCertificate`; auto-demotes on margin loss. (b) the σ-controller = the validated online criticality controller for the §7.2.1 SHADOW-mode set-point, **actuating through the existing §6.3 hormone-vector inhibition channel — never a new actuator**, and presenting σ (not τ) as the control variable with τ a derived read-out. | Spike-Bus avalanche distributions; live trust-edge × message-influence graph. **Preserves verbatim:** governance computable at the individual-agent level; loosening is governed; demotion is free; inhibition bounded by the diversity floor. |
| **Meta-Evolution & the Immune System — Garuda–Dhanvantari (doc 06)** | σ supercritical-storm early-warning + Lyapunov `margin_to_boundary` as first-class vital signs feeding §7.2's homeostatic controller (which holds HALT+rollback); First-Line Shift-Triage as the §7.1 four-pathway localization engine; `AdaptationStabilityCheck` as an **admissibility input** to the §3 tiered-reversibility gate (Lyapunov-decrement on parameter proposals) — **never the floor verdict**; the MDL objective for §8 forgetting/consolidation with RareEventReserve/safety-pin hard-overrides preserved. | tier classification; reliability + **frozen-battery + falsifier-gate** data that earns SHADOW→ACTIVE promotion (fail-closed cold-start, §7.4). |
| **Akasha-Sutra — Provenance, Identity & Consensus (doc 04) / Chitragupta** | ALL certificates (`ClosureCertificate`, `CausalAttestation`, `CriticalityState`, `LyapunovCertificate`, the Honesty Ledger) are content-addressed and teed read-only via `audit.tap`. **This subsystem NEVER writes the log — Chitragupta is the exclusive writer (preserved; the writer's vocabulary has no edit/delete verb).** The Causal-Discipline Gate is the admission filter deciding at which rung a claim *enters* the chain — **by superseding attestation, never by mutating a signed envelope** (§3.3). | `GroupBlanketUpgrade` and SHADOW→ACTIVE promotions require k-of-n witness cosign (the split-view defense). |
| **Governance, Ethics & the Floor (doc 03) / Yama** | EVIDENCE only (margins, attestations). The genuine bright-line — a `rung-3` tag with **zero causal-model artifact** — is surfaced to Yama's *existing* §6 structural check, with the REPARATIVE path available. **Non-identifiability and refutation-failure are routed to ETHICS_REVIEW + anekantavada (doc 03 §6/§9), NOT to the deterministic floor.** | Yama's floor verdict is always supreme and read at the individual-agent level regardless of any CLOSED super-agent. This subsystem **never owns a floor verdict.** |
| **WorkerOutputEnvelope (doc 00 §4.2) — the universal contract** | A separate signed `CausalAttestation` superseding the rung via `causal_parents`/`refs`; `effective_rung` resolution for consumers. **READS** `envelope.causal_rung`, `evidence[]`, `ahankara_audit` — **WRITES NOTHING back into the signed envelope** (the §3.3 fix). All health metrics emitted as surprise-only `HealthSignal`s (doc 06 §7.1) — no new transport, no heartbeat flood. | the envelope's declared rung + cited evidence as the claim to be earned. |
| **Replication Authority & inter-swarm relay (safety planes)** | the Percolation/Topology Monitor supplies the **lineage-wide R_eff < 1 budget check** to the quorum-cosigned Replication Authority (replication stays provably sub-critical / percolation-bounded) and the **contagion-R < 1 + corroboration-required** constraints to the inter-swarm relay/firewall (sparse, mesh-corroborated contact graph; strongest controls on hubs). | the live contact graph. **This subsystem only MEASURES and CONSTRAINS; it issues no spawn tokens, holds no replication authority, and does not touch the replication red-line (no open fitness/selection loop coupled to replication).** |

---

## 13. Failure modes addressed

| Failure mode | How this subsystem addresses it |
|---|---|
| **Governing an EPIPHENOMENAL level** (doc 05 §7.2.1 SPOF-of-abstraction: clan-level governance computed on a silently-broken super-agent, propagating corrupt state upward) | The Closure-Test Engine is the validated detector that was declared missing; OPEN/low-margin levels stay `ADVISORY_ONLY` and Yama reads individuals directly. Auto-demotion on margin loss is free/single-signal/fail-safe. |
| **rung-1-pattern-presented-as-rung-3-explanation** (the constitution's single most-flagged honesty failure) | The Causal-Discipline Gate makes rung tags mechanically earned (do-calculus identify + refute) and down-tags on failure **via superseding attestation, never envelope mutation**; the Physics-Claim Honesty Ledger forbids framing metaphors from becoming control inputs. |
| **AUDIT-FABRIC IMMUTABILITY VIOLATION** (an in-band path touching signed hash-chained envelopes pre-admission) | Resolved by the separate-superseding-attestation pattern (§3.3): no in-place edit; Chitragupta-only write preserved; the down-tag is a first-class auditable event. |
| **BRIGHT-LINE OVER-REACH / false-positive floor violations on honest-but-hard causal claims** | Aligned to doc 03 §6 verbatim (§3.4): only DAG-artifact absence is bright-line; identifiability/refutation are detected-and-escalated to ETHICS_REVIEW/anekantavada. The gate produces evidence; it never owns the identifiability verdict. |
| **FALSE CONFIDENCE from causal-discovery root-cause on live telemetry** (near-random at scale, arXiv:2408.13729) | BARO/NSigma distribution-shift detectors are first-line; SCM counterfactuals reserved for small identifiable subgraphs, honestly rung-tagged. |
| **CASCADE / AVALANCHE STORMS + the v1 missing online criticality controller** (doc 06 §12.2) | The σ-controller measures branching ratio online (MR regression) and biases slightly-subcritical (contagion R<1), giving the immune system a leading indicator instead of a post-hoc diagnosis. |
| **SINGLE-UNIT-STABLE-BUT-NETWORK-UNSTABLE homeostasis** (the seizure-like failure; doc 05 §6.2, research2 avoid-list) | Both σ-control and Lyapunov certification are co-designed at the network level with inhibitory recruitment, never per-agent in isolation. |
| **MODE-COLLAPSE / OSCILLATION / PREMATURE-CONSENSUS as post-hoc-only diagnoses** | The Neural-Lyapunov certifier reframes them as named bifurcations (saddle-node / Hopf / basin-exit) with a measured distance-to-tipping-point. |
| **HUB FRAGILITY** ("robust-yet-fragile"; high-influence/high-trust hubs are the prime poisoning target) | The Percolation/Topology Monitor defines degree as message-influence×trust-weight, applies targeted (not random) immunization, and shards/replicates hubs. |
| **τ/σ CONFLATION** (relabeling a branching-ratio target as the avalanche-exponent set-point) | §5.1 states τ and σ are distinct observables, gives the relationship, presents σ as the controllable variable that supersedes the ill-posed exponent-fit, and carries τ as a derived read-out only. |
| **CRITICALITY THEATER** (claiming "edge-of-chaos" from a loose power-law fit) | Avoided by controlling a measured σ with a quasicritical target via a subsampling-robust estimator (MR regression) and reporting honestly when off-target. |
| **MEMORY ROT vs losing rare-but-important knowledge** | The MDL consolidation objective gives a principled forget criterion (predictive value < cost) while the protected RareEventReserve and safety-memory pins (doc 06 §8) hard-override MDL eviction. |
| **DECORATIVE PHYSICS creep** (Landauer J/bit, literal RG flow equations, strong-emergence as a design principle, FEP-as-explanation) | Demoted to `FRAMING_ONLY` and barred from control paths by the Honesty Ledger; a framing metric wired to an actuator is itself a reverted floor defect. |
| **SHADOW→ACTIVE promotion gamed by a meta-Goodharting operator** | Promotion bound to a frozen adversarial battery + falsifier gate + Endure-law non-regression of diversity/disagreement floors + Class-B ratification (§10.4), not to shadow-distribution "reliability" alone. |

---

## 14. Novelty — an honest accounting (time-stamped mid-2026, hedged)

**The genuinely-advancing contribution is CLOSURE-GATED FRACTAL GOVERNANCE.** To our knowledge as of mid-2026, no swarm architecture grounds its multi-scale governance in the 2024 causal/informational-closure criterion (Rosas et al., arXiv:2402.09090) used as the empirical, falsifiable **test** for which levels may be governed as units — converting "the swarm is more than its agents" and group-Markov-blanket nesting from doctrine into a computable gate, and giving the only legitimate cash value of "downward causation." This gate ships **shadow-mode and operable only in the low-dimensional, discretized regime**: there is as yet **no scalable closure test for high-dimensional continuous agent state and no principled approximate-closure threshold** (§15 #1), so the high-dimensional regime is research-track and the contribution is the *governance wiring* of a falsifiable test, not a calibrated detector at swarm scale.

Three further compositions are advancing, not invented-from-nothing:

1. **Causal discipline as audit-fabric admission.** Wiring a DoWhy/PyWhy Model→Identify→Estimate→Refute gate as the **admission filter** for the audit fabric's Pearl-rung tags — making causal honesty a *mechanical precondition for entering a tamper-evident log* rather than a prose convention — and pairing it with the honest concession that distribution-shift detectors (BARO/NSigma) **beat** causal root-cause at scale (arXiv:2408.13729), so the heavy machinery validates *claims* while simple detectors do live *triage*.
2. **A slightly-subcritical σ controller** that unifies two usually-separate goals — near-critical computation and sub-critical (R<1) contagion containment — actuated through an *existing network-level inhibitory channel* rather than per-agent set-points, and explicitly *distinct from* the v1 avalanche-exponent set-point it supersedes.
3. **A neural-Lyapunov certificate over COLLECTIVE swarm state** (trust-entropy, role-allocation, consensus) that turns the v1's empirically-listed failure modes into named bifurcations with a measured distance-to-tipping-point.

**The deepest methodological novelty is the Physics-Claim Honesty Ledger:** every emitted quantity self-declares LOAD-BEARING-MECHANISM vs DESIGN-CONSTRAINT vs FRAMING-ONLY, and framing metaphors are *structurally barred* from control paths — a built-in guard against the architecture's own named failure.

**Explicitly NOT novel, and credited by name:** ε-machine / computational-mechanics, ΦID / integrated-information decomposition, do-calculus and DoWhy/PyWhy, Wilting–Priesemann MR branching-ratio estimation, Chang-style neural-Lyapunov learning with counterexample-guided falsification, percolation / network-science, MDL — all borrowed and named. **The honest delta is the COMPOSITION** (closure-as-governance-gate + causal-discipline-as-audit-admission + σ-and-Lyapunov-as-certified-homeostasis) plus the discipline of shipping every controller shadow-mode-first with a blunt load-bearing-vs-framing verdict — **not any single mechanism.** The honest SOTA comparator: this is methodologically close to applying established causal-emergence / computational-mechanics machinery (Rosas/Hoel-lineage effective-information work) plus standard DoWhy refutation and standard neural-Lyapunov control **to a swarm-governance setting** — the mechanisms are all off-the-shelf; the *governance wiring* is the delta, and this document says exactly that.

---

## 15. Open problems (load-bearing and unresolved)

These are real, several are load-bearing, and the dependent features ship shadow-mode behind conservative defaults because of them.

1. **No principled APPROXIMATE-CLOSURE threshold.** Real swarm levels are rarely exactly causally/informationally closed, and there is no agreed cutoff for "closed enough to govern as a unit." ε-machine inference is sampling-heavy, and there is **no scalable closure test for high-dimensional continuous agent state.** We ship a graded `{OPEN / APPROX_CLOSED / CLOSED}` verdict with margins and conservative defaults — *not* a proven cutoff — and keep low-margin levels `ADVISORY_ONLY`.
2. **No online criticality controller is PROVEN** to hold a live, workload-varying swarm at quasicriticality under non-stationary load. The σ-controller is promising but lacks stability guarantees, and the single-unit-vs-network stability tension is unresolved. We measure-and-nudge in shadow mode and bias slightly-subcritical for safety, but **cannot guarantee we hold the set-point.**
3. **Counterfactual ROOT-CAUSE remains aspirational** on real telemetry — defeated by unmeasured confounders, feedback (acyclicity violation), and sub-minute diagnosis windows. We use it only on small identifiable subgraphs and backstop everything with distribution-shift detectors; the Pearl-ideal-vs-practice gap is open.
4. **ΦID/PID has no canonical synergy/redundancy measure** and is data-hungry and biased in high dimensions, so `Φ_syn` is method-dependent and used **only as a flag-to-run-closure**, never as a control gain or a quantitative governance number. (This is *why* §2.1 mandates multiple independent triggers, not `Φ_syn` alone.)
5. **Lyapunov / region-of-attraction certificates are LOCAL and model-dependent.** In genuinely non-stationary MARL (every agent in every other's environment) global stability guarantees do not exist. The margin-to-boundary is a tipping-point indicator, **not a safety proof**, and ships shadow-mode.
6. **Whether RG scale-invariance is more than analogy** for a heterogeneous discrete agent swarm is unresolved — no demonstrated fixed point or measured critical exponents at swarm scale. "Same governance law at every closed level" is therefore a **design choice** justified by RG framing + the closure test, not a derived fact, and we write no literal RG flow equations.
7. **No UNIFIED multi-scale controller composes the three load-bearing strands.** Closure tells you the levels, σ-control tunes capacity, Lyapunov certifies stability — but **no theory provably composes them** for a live ethical swarm. We run them as coupled-but-separate loops with the Honesty Ledger guarding the seams, and **name the missing unification rather than fake it.**
8. **SHADOW→ACTIVE promotion under an adaptive adversary is mitigated, not solved.** The frozen-battery + falsifier-gate + Endure-non-regression binding (§10.4) raises the bar against a meta-Goodharting operator, but a sufficiently capable adversary who knows the promotion protocol can still concentrate drift on un-tested axes. This inherits doc 06's unsolved fitness-Goodhart residual at the controller layer.

> **Posture statement.** This subsystem's genuine contribution is a *composition* that converts three named-as-framing physics ideas into shadow-mode-first, certificate-bearing machinery — and the discipline of a Physics-Claim Honesty Ledger that structurally bars the architecture from letting an aesthetic metaphor become a load-bearing control input. Where a guarantee does not exist we have written "we measure and nudge, but cannot guarantee," and we have engineered the cheap direction to be the safe direction (promotion gated/witnessed, demotion free/single-signal; tightening append-only, loosening falsifier-gated; framing barred from actuators) so that when these heuristics fail, they fail safe. The instruments on this bench measure whether a reflection is real. They do not — and we do not claim they do — make every reflection true.
