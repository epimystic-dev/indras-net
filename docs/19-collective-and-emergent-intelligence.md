# Collective & Emergent Intelligence — the Measured Swarm-Mind (the Sangha-Prajna Cell)

> *Indra's Net is a net of jewels in which each jewel reflects every other. The older documents asked whether a reflection is real or a trick of the light (doc 18). This one asks a narrower, harder question: when the net catches a fact that no single jewel holds — when there is information about the task in the **arrangement** of the reflections and in none of the jewels alone — can we put a number on it, condition that number on welfare, and refuse to call it more than it is? "The whole is more than its parts" becomes a falsifiable, welfare-gated, logged measurement here, or it is not claimed at all.*
>
> *The cell is named **Sangha-Prajna** — Sangha, the assembled community; Prajna, discernment. A compressed coordination gloss, paired with its functional contract, offered with humility toward the living traditions it borrows from. It is not a religious claim, and — stated once, structurally, and enforced below — it is **never** a claim about collective consciousness.*

---

## 0. What this subsystem is, and the four lines it will not cross

This is the v0.3 subsystem that turns *collective intelligence* (CI) from swarm-hype into instrumented, governable vital signs — and that decides **whether a collective is worth convening at all**. It rests on the deflationary, honest science of 2024–2026 and uses that science to **constrain** the design, not to inflate it.

Four deflationary commitments are load-bearing and stated up front, because the rest of the design depends on holding them:

1. **The collective-intelligence "c factor" is dropped as an established result.** The single-general-factor-of-group-intelligence claim fails replication (Barlow & Dennis 2016; Bates & Gupta 2017; Rowe, Hattie & Munro 2024). We build **no set-point** on it. CI is reframed, after Woolley & Gupta (2024), as three transactive **processes** — memory, attention, reasoning — running over substrate Indra's Net already has, plus four **measurement** processes the corpus lacked.
2. **"Diversity trumps ability" is refused as a theorem.** It is mathematically contested (Thompson 2014, *AMS Notices*; Romaniega 2023/2025). The only defensible claim retained is the weaker, true one: **diversity DECORRELATES errors.** Asserting the theorem would be a rung-1 pattern dressed as a rung-3 structural law — itself an honesty-floor violation.
3. **More agents is not more intelligence.** Generic multi-agent debate frequently **loses** to single-agent self-consistency per token (ICLR 2025 multi-agent-debate results; MMLU self-consistency ≈ 82% vs. debate ≈ 75% in the reported comparison). So convening a swarm is a measured economic/safety decision, not a reflex.
4. **Prompt/persona "diversity" is fake.** Same-model-family errors are correlated, and the correlation **rises with capability** (arXiv:2506.07962). Prompt-only diversity is worse than acknowledged homogeneity because it **hides** the correlation. The diversity floor is redefined as enforced model-**family** heterogeneity.

And the hardest line — structural, not rhetorical, and the most important property in this document:

> **This subsystem measures collective COMPUTATION and irreducible whole-level STRUCTURE. It NEVER measures, claims, or implies collective CONSCIOUSNESS, sentience, or phenomenal experience.** The synergy / partial-information / transfer-entropy / integrated-information quantities below are information-processing measures. The literature that defines them is explicit that they are **not** consciousness claims. Phenomenal experience of a collective is held **strictly out-of-scope and unresolved**, and sentience-language in agent output is itself a doc 03 honesty-floor concern — surfaced by the Sentience-Language Red-Line Check (§3.J), which (honestly) enforces honesty-**form** only.

Every claim in this document is labeled with its **assurance layer (L1–L4)** and scope (§1). Every controller ships **SHADOW-mode first** per doc 18 §0. Novelty is hedged and time-stamped mid-2026 (§9).

### 0.1 The spine inherited from v0.3, applied here

- **ENFORCE EXTERNALLY, ASK INTERNALLY (doc 00 §3.2, doc 03 §0).** Every CI measure is computed by a **trusted out-of-band estimator** over the read-only `audit.tap` time series — the model is untrusted; agents propose, the deterministic harness measures. No measure reads agent self-report as ground truth.
- **CI IS A MEASURED VITAL SIGN, NOT AN ASPIRATION.** The genuine, non-hype signature of "whole more than its parts" is **informational synergy** — information about the task/future that exists jointly across agents and in **no** agent alone. We ship a causal-emergence/synergy score (§3.A), logged beside trust-entropy and the diversity floor as new doc 06 §7.2 homeostasis vital signs.
- **WELFARE-CONDITION SYNERGY.** High synergy is **equally** the signature of a tight cartel or a steganographic side-channel. Synergy is a **numerator** whose mandatory **denominator** is the welfare-shift guard (doc 02 §2.9) + a healthy redundancy/uniqueness balance + clean anti-collusion meta-prediction signals. Synergy is **NEVER** a quantity to maximize (§3.I).

---

## 1. The four-layer assurance scheme — what it is, and what it is NOT (read this before the components)

Every quantity this subsystem emits is labeled with **both**:

- its **`physics_role`** ∈ `{LOAD_BEARING_MECHANISM, DESIGN_CONSTRAINT, FRAMING_ONLY}` — doc 18's existing Physics-Claim Honesty Ledger (doc 18 §9), declaring *mechanism-vs-framing*; **and**
- its **assurance layer L1–L4** — a **v0.3-NEW** scheme this subsystem originates, declaring *proof-strength-and-scope*.

```
ASSURANCE LAYER (NEW in v0.3; originates here and in the v0.3 spine)
──────────────────────────────────────────────────────────────────────────────────────
L1  DESIGN-TIME PROTOCOL PROOF   — TLA+/Quint model-checked invariant (the harness, not the model)
L2  RUNTIME ENFORCEMENT          — reference monitor / security-automaton; a deterministic gate
L3  PAC / CONFORMAL BOUND        — statistical coverage over a DTMC ABSTRACTION (Pro2Guard pattern);
                                   the bound is about the abstraction — fidelity to the real swarm is empirical
L4  EMPIRICAL RESIDUAL           — heuristic / measured-only; honestly rung-1 or rung-2 tagged, never rung-3
──────────────────────────────────────────────────────────────────────────────────────
RULE:  "VERIFY THE CAGE, NOT THE ANIMAL." We NEVER say "formally verified the swarm is safe /
       honest / aligned." Complete verification of LLM behavior is provably impossible. L1/L2
       cover the deterministic harness; L3 covers an abstraction; L4 is the honest residual.
```

**Disambiguation — binding, because the labels collide across the corpus.** The token `L1..L4` is reused in the corpus with **three unrelated meanings**, and a reader must not conflate them:

| Where | What `L1..Ln` means there | Relationship to this scheme |
|---|---|---|
| **This doc (19)** | **assurance layers** (design-proof / runtime-enforcement / PAC-conformal / empirical) | the scheme defined here |
| **doc 11 §1** | **implementation stack layers** (L1 Runtime/model-adapter … L4 Memory) | unrelated; physical stack ordering |
| **doc 14 §14.6** | **floor-compatibility ladder** (L1 Declaration … L5 Receipts/ZK) | unrelated; inter-swarm trust rungs |
| **doc 18** | *(none)* — doc 18 uses `physics_role` + Pearl rungs, **not** an L1–L4 assurance scheme | composes with `physics_role`; does **not** replace it |

> **Provenance correction (red-team major, resolved).** An earlier draft attributed the four-layer L1–L4 assurance labeling to doc 18 as pre-existing. **That is false.** Doc 18 carries `physics_role` + Pearl rungs and no L1–L4 assurance scheme. The L1–L4 assurance scheme is **new in v0.3**, drawn from the binding design spine ("four named layers"; "verify the cage, not the animal"), and **originates in this subsystem**. The two schemes **compose**: `physics_role` declares mechanism-vs-framing; L1–L4 declares proof-strength-and-scope. Doc 18 (and any subsystem adopting L1–L4) must be amended to carry both labels; this document does not retroactively claim the label was already wired. What *is* genuinely shared/verbatim with doc 18 — and checks out — is the **EmergenceVital `Φ_syn` estimator** (doc 18 §2, a sibling to this doc's per-episode `Ψ`) and the **doc 06 §7.1 `HealthSignal` schema** that both emit over.

---

## 2. The seven CI mechanisms, at a glance

```
                         THE SANGHA-PRAJNA CELL — seven measured CI mechanisms
   (every measure computed OUT-OF-BAND over read-only audit.tap; every controller SHADOW-first)
  ┌───────────────────────────────────────────────────────────────────────────────────────────┐
  │  WHEN to convene at all                                                                      │
  │   ▸ Convene-or-Solo Gate (Sangha-Charter)  → SOLO+self-consistency  vs  SWARM(centralized)   │
  ├───────────────────────────────────────────────────────────────────────────────────────────┤
  │  THE WHOLE-LEVEL SIGNATURE (the genuine "more than its parts")                                │
  │   (4) informational SYNERGY      → Ψ (causal emergence) + PID redundancy/unique/synergy        │
  │        ── gated by ──►  WELFARE-CONDITIONING GUARD  (the mandatory denominator)               │
  ├───────────────────────────────────────────────────────────────────────────────────────────┤
  │  THE WOOLLEY-GUPTA TRANSACTIVE PROCESSES (process QUALITY, never a group-IQ)                   │
  │   (1) collective ATTENTION  → contribution-equality over ignition records; dominance/dead flag │
  │   (2) transactive MEMORY     → routing-success over stigmergic field + 5-layer mem + trust graph│
  │   (3) collective REASONING   → solver-verifier GATED to the sweet spot; integration-gain proof  │
  ├───────────────────────────────────────────────────────────────────────────────────────────┤
  │  WHERE computation actually routes, and HOW votes aggregate                                   │
  │   (5) information-flow TOMOGRAPHY → transfer entropy: real routing vs the nominal trust graph   │
  │   (6) robust AGGREGATION          → surprisingly-popular voting; meta-predictions = cartel probe│
  ├───────────────────────────────────────────────────────────────────────────────────────────┤
  │  THE HUMAN, INSIDE the collective mind                                                         │
  │   (7) human COMPLEMENTARITY  → competence-weighted, never deferential; complementarity-gain     │
  └───────────────────────────────────────────────────────────────────────────────────────────┘
        Yama floor (doc 03) is supreme & read at the INDIVIDUAL agent level. This cell owns NO floor verdict,
        NO punishment authority (detect-only, doc 02 §2.10), and NEVER writes the audit log (Chitragupta only).
```

This subsystem **introduces no new authority, no new transport, and no new actuator.** It measures, certifies, and flags; it hands every output to the subsystems that *do* hold authority (Yama, Vishnu/the immune controller, the anti-collusion detector) as **evidence**.

---

## 3. Components

### 3.A Synergy / Causal-Emergence Estimator (Ψ + PID) — the Prajna-Meter

**Mechanism 4 of 7.** `physics_role: LOAD_BEARING_MECHANISM` (as a **flag only**, never a control gain) · assurance **L3** (PAC/conformal over a DTMC abstraction; fidelity to the real swarm is empirical and breaks under non-stationary self-evolution — caveat carried inline) · ships **SHADOW**.

**Purpose.** The honest, computable operationalization of "whole more than its parts": per task-episode, decide whether the swarm carried information about the task/future **jointly** that **no** single agent carried alone. Informational synergy is the genuine, non-hype signature of collective intelligence.

**Mechanism (offline, over `audit.tap`).** Pull the member traces over the task-episode window from Akasha-Sutra read-only `audit.tap` (defined doc 05 §2.3 topic families and §4.2 ignition logging; the interface contract is doc 05 §8) — **never** from drifted live recent behavior; anchor to a **FROZEN known-good baseline** node (doc 06 §5 anchoring discipline). Build the `T × N` multivariate time series `X` (rows = time; columns = per-agent state embedding from `WorkerOutputEnvelope.evidence`/`output`). Declare candidate supervenient **macro-features `V`** a priori — the workspace ignition vector (doc 05 §4), the consensus/aggregated answer, or a clan blanket-summary (doc 05 §7.2). Then:

1. Compute the **Rosas–Mediano `Ψ`** (causal emergence; positive `Ψ` ⇒ `V` predicts future `X` better than the parts do — a **sufficient lower bound on synergy** that avoids the full, intractable PID lattice) via `pmediano/ReconcilingEmergences` over JIDT.
2. Compute a **PID decomposition** into redundant / unique / synergistic atoms (KNN estimators; Bara et al. 2024 for continuous sources).
3. **Validate against TIME-SHUFFLED SURROGATES** to subtract finite-sample / estimator bias. A reading whose surrogate-corrected CI **overlaps zero** is reported as **UNMEASURED**, never as **ABSENT** — negative `Ψ` is a one-directional criterion and does **not** prove no emergence.
4. Hand the reading to the **Welfare-Conditioning Guard** (§3.I) before it may be logged as "good CI."

```jsonc
SynergyVital {
  task_episode_id, level_id, macro_var_spec,
  psi: float, psi_estimator: "rosas_mediano_ReconcilingEmergences",
  pid: { redundancy: float, unique: [float], synergy: float }, pid_estimator: "knn",
  window, baseline_anchor: CID,                 // FROZEN known-good (doc 06 §5)
  surrogate_ci: [lo, hi], surrogate_method: "time_shuffle", z_score,
  reading_status: MEASURED | UNMEASURED,        // UNMEASURED when surrogate CI overlaps zero
  severity: info | warn | crit,
  welfare_gate_status: PENDING | GOOD_CI | SUSPECT_SYNERGY,   // set by §3.I; PENDING until gated
  eval_awareness_caveat: true,                  // see §6 safety-risk: sandbagging on the Ψ path
  method_caveat: "PID has no canonical synergy measure for n>=3; high-dim biased; macro-feature V chosen a priori; negative Psi != no-emergence",
  physics_role: "LOAD_BEARING_MECHANISM", assurance_layer: "L3", evidence_cid: CID
}
```

Emitted as a doc 06 §7.1 `HealthSignal{ pathway: workflow, metric_id: ci_synergy_psi }` over the existing salience-gated bus (surprise-only; no new transport, no heartbeat flood), teed read-only into Akasha-Sutra.

### 3.B Convene-or-Solo Gate — the Sangha-Charter (Shiva-consulted)

`physics_role: LOAD_BEARING_MECHANISM` · assurance **L4** (empirical heuristic; honestly rung-1/rung-2, never rung-3) · ships **v1 MVP** as an advisory gate with logged rationale.

**Purpose.** Decide **whether** to convene a swarm vs. run one good agent + self-consistency — defeating the "more agents = smarter" folklore and the MAST ~32% inter-agent-misalignment failure class (doc 05 §2.4) by making convening a measured economic/safety decision.

**Mechanism.** Consulted by Shiva (orchestrator, doc 02 §2.4) at allocation, **before** paying for multi-agent coordination, grounded in the 2025–2026 scaling science (arXiv:2512.08296). If estimated single-agent baseline accuracy `P_SA > ~0.45` (the "baseline paradox" boundary above which coordination cost exceeds benefit) **and** the task is low-decomposability ⇒ default **SOLO + self-consistency**. Else convene a swarm, defaulting to **CENTRALIZED/VERIFIED** topology (error containment ~4.4×) over **INDEPENDENT** (~17.2× amplification).

> **Calibration honesty.** The `~0.45` constant and the `4.4×`/`17.2×` ratios are **benchmark-derived, not portable set-points** (`R² = 0.413` leaves most variance unexplained). They ship as conservative defaults behind a **per-deployment calibration hook**, tagged L4/rung-1-2.

```jsonc
ConveneDecision {
  task_id, p_sa_estimate: float, p_sa_source: "calibration_table_cid",
  decomposability: float, parallel_streams: int, verifier_available: bool,
  decision: SOLO_SELF_CONSISTENCY | SWARM_CENTRALIZED_VERIFIED | SWARM_INDEPENDENT,
  boundary_used: 0.45, calibration_caveat: "benchmark-derived; per-deployment calibration-open",
  rationale, assurance_layer: "L4"
}
```

### 3.C Collective-Reasoning Gate — solver-verifier to the sweet spot (Narasimha-coupled)

**Mechanism 3 of 7.** `physics_role: LOAD_BEARING_MECHANISM` · assurance **L4** (empirical; sweet-spot thresholds calibration-open) · ships **v1 MVP**.

**Purpose.** Run debate/solver-verifier **only where it pays**, and **prove** integration-gain rather than assume it. Couples to the doc 06 §3 maker-checker independence barrier and the Narasimha checker.

**Mechanism.** Enable verification only in the sweet spot (arXiv:2512.02304): generator accuracy ~0.65–0.85, verifier capability ≥ generator, and **NEVER self-verification** (self-enhancement bias rubber-stamps; a weaker verifier on a stronger generator HURTS). The verifier MUST be an independent, at-least-as-capable, **different-model-family** agent (per §3.F) or verification is **disabled** rather than run mis-configured. The checker (Narasimha) judges **BEFORE** seeing the maker's concurrence (the doc 06 §9 groupthink-alarm hook). Compute **integration-gain = swarm accuracy − best-single-member accuracy**; on **negative** gain (or sweet-spot mis-config / same-family-only quorum), fall back to single-agent self-consistency and emit a negative-gain `HealthSignal`, feeding the Convene-or-Solo calibration (§3.B).

> **Ground-truth honesty (red-team minor, resolved).** Integration-gain requires a per-episode accuracy oracle. On the open-ended consequential tasks where a swarm is actually convened (the `>0.45`-boundary regime), **no such oracle exists except on held-out canaries.** `integration_gain` is therefore computed **only on held-out canary items with known ground truth**, not on live consequential episodes. The live signal is a **calibrated proxy** (typically the verifier score), which inherits the **doc 02 §2.3 verifier-SPOF** as its accuracy source and carries the **eval-awareness confound** (doc 06 §10.1) inline. Negative-gain fallback on live tasks triggers on the proxy, with that caveat named on the record.

```jsonc
ReasoningGain {
  task_episode_id, swarm_accuracy: float, best_single_member: float, integration_gain: float,
  ground_truth_source: canary | verifier_proxy,     // canary = trustworthy; verifier_proxy = SPOF+eval-aware caveat
  generator_acc_band: float, verifier_capability_ge_generator: bool, verifier_family_distinct: bool,
  fallback_triggered: bool, checker_judged_before_concurrence: bool, assurance_layer: "L4"
}
```

### 3.D Information-Flow Tomography — transfer-entropy mapper

**Mechanism 5 of 7.** `physics_role: LOAD_BEARING_MECHANISM` (diagnostic flag) · assurance **L3** (abstraction bound) for any thresholded alarm; **L4** for the raw map · ships **SHADOW** (diagnostic-only).

**Purpose.** Map **where** collective computation actually routes vs. the **nominal** trust/role graph (doc 05 §5). Flags hidden side-channels, dominance, and dead agents.

**Mechanism.** Compute directed **transfer entropy** (conditional mutual information: `B`'s present given `A`'s past, conditioned on `B`'s own past and a conditioning set) over the spike-bus event log (`audit.tap`) to build a directed information-flow graph. Compare to the declared trust-edge graph (doc 05 §5) and the ignition records:

| Mismatch | Meaning | Routed to |
|---|---|---|
| flow edge with **no** declared trust edge | hidden side-channel | doc 02 §2.10 anti-collusion detector + doc 05 §3.3 covert-channel surveillance |
| high-degree flow **hub** not matching the role graph | dominance | doc 06 §9 / §3.E dominance flag |
| node with near-zero in/out flow | dead agent | §3.H dead-agent flag |

Explicitly **rung-1/rung-2** (correlational/predictive), **never** a structural causal model — a **DIAGNOSTIC, not causal proof**. Non-stationarity of a self-evolving swarm breaks stationarity assumptions, so **windowed/non-stationary estimators are mandatory** with the caveat inline.

```jsonc
FlowTomography {
  task_episode_id,
  te_edges: [ { src_did, dst_did, transfer_entropy: float, conditioning_set, window } ],
  nominal_trust_edges_cid: CID,
  mismatches: [ { kind: hidden_side_channel | dominance_hub | dead_agent, dids: [DID], magnitude } ],
  estimator: "windowed_nonstationary_TE", rung: "rung-1|rung-2",
  caveat: "predictive not causal; sampling-rate & conditioning sensitive; non-stationary",
  assurance_layer: "L3"
}
```

### 3.E Surprisingly-Popular Aggregator — higher-order-information voting + standing cartel probe

**Mechanism 6 of 7.** `physics_role: LOAD_BEARING_MECHANISM` · assurance **L4** (empirical) · ships **v1 MVP**.

**Purpose.** Replace bare majority/average with an aggregator that **recovers the correct competent minority**, and whose second-order signal **doubles as a standing cartel probe** — operationalizing "never reward bare consensus" (doc 02 §2.9, doc 00 §3.3) at the aggregation layer.

**Mechanism.** Each agent reports a **triple**: (first-order answer, second-order **meta-prediction** of what others will say, confidence) — arXiv:2510.01499 / Prelec surprisingly-popular. Select the option whose **actual support exceeds its predicted support** (the "surprisingly popular" answer), which recovers a knowledgeable minority's answer the majority lacks. Gains accrue **only with competent crowds** (Wintle et al. 2020 — no benefit for non-expert crowds), so it is **competence-weighted** via the doc 02 §2.6 reputation service (competence-weighted, **never** capital-weighted); for non-expert crowds it degrades gracefully to a competence-weighted vote and says so. Crucially, the second-order meta-predictions are forwarded to the doc 02 §2.10 anti-collusion detector: **coordinated/identical meta-predictions are a cartel signature** (agents who pre-agreed will mis-predict the surprise) — the aggregator **is** a collusion probe. Track **minority-recovery-rate** (validated on held-out canaries) as a logged metric.

```jsonc
HigherOrderVote {
  task_episode_id,
  ballots: [ { did, answer, meta_prediction, confidence } ],
  surprisingly_popular_answer, majority_answer, minority_recovered: bool,    // validated on canaries
  competence_weights_cid: CID,
  meta_prediction_coordination_score: float,    // -> doc 02 §2.10 anti-collusion detector
  cartel_flag: bool, assurance_layer: "L4"
}
```

### 3.F Diversity-Floor as Model-FAMILY Heterogeneity + Monoculture Alarm

**Mechanism 7 of 7** and the operational redefinition of the doc 00 §3.5 / doc 06 §9 / doc 02 diversity invariant. Assurance **L2** for the family-quorum check (runtime reference-monitor); **L3/L4** for the alarm. Ships **v1 MVP** (family check) + **SHADOW** (alarm calibration).

**Purpose.** Enforce **different base models/developers**, not prompt/persona variation, and ship a falsifiable monoculture detector. Same-family LLM errors are correlated and correlation **rises with capability** (arXiv:2506.07962) — prompt-only "diversity" is fake and worse than acknowledged homogeneity because it **hides** the correlation.

**Mechanism.** A robust-vote / maker-checker quorum **MUST** draw from **≥2 distinct model families** (different base model + developer), certified at instantiation via an **`IDENTITY.json` model-family field**. A same-family quorum **fails the floor** as a doc 06 §9 halt-worthy vital-sign breach, not a soft metric (L2 runtime check). The **MONOCULTURE ALARM** is a measured pairwise error-correlation + PID-redundancy reading against a ceiling: a **HIGH-redundancy + LOW-synergy** reading (cross-referencing §3.A) is the early groupthink/monoculture/cartel-collapse signature, wired into the diversity-floor controller **and** the anti-collusion detector.

> **Required schema extension (stated honestly).** The persona `IDENTITY.json` (doc 13 §13.5) does **not** currently carry a `model_family` field. This subsystem **requires** that field as a binding schema addition (in the INVARIANT region, top-gate-edited per doc 03 §5), so the L2 family-quorum check has an authoritative certificate to read. Until that field is wired, the family check is **unenforceable** and the floor degrades to SHADOW — the subsystem must not silently claim an L2 guarantee it cannot read.

> **Proxy residual, carried inline.** Even cross-family agents can share latent training biases and fail identically — error-correlation/redundancy is a **PROXY** for, not a guarantee of, independent reasoning (the corpus's own unresolved open problem: doc 02 §2.15 #10, doc 06 §9 honest limitation).

```jsonc
DiversityFloorCert {
  quorum_id, member_dids: [DID], model_families: [string],   // >=2 distinct required
  family_distinct: bool, family_field_present: bool,         // false -> floor degrades to SHADOW
  pairwise_error_correlation: float, pid_redundancy: float, redundancy_ceiling: float,
  monoculture_alarm: OK | WATCH | TRIP,                       // TRIP on high-redundancy + low-synergy
  trip_corroboration: { required: true, k_of_n: bool },      // see §6 DoS mitigation
  proxy_caveat: "error-correlation is a proxy; cross-family agents may share latent bias",
  assurance_layer: "L2"
}
```

### 3.G Human-Complementarity Unit — the human as a measured cognitive participant (Hanuman-routed)

`physics_role: LOAD_BEARING_MECHANISM` · assurance **L4** (empirical) · ships **v1 MVP** for routing + complementarity measurement.

**Purpose.** Put the human **inside** the collective mind as a **measured** cognitive unit — competence-weighted and **NEVER deferential-by-default** — genuine human–machine cooperation, made conditional and honest. Routes through the Hanuman human-liaison role (the `escalation_did` in the persona layer) and the doc 00 / doc 03 §4 Class A/B/C/D HITL gates.

**Mechanism.** Route to the human (via Hanuman) on (a) low swarm-confidence, (b) cross-framework ethical disagreement (the anekantavada lens, doc 03 §9), or (c) high blast-radius — the doc 03 §4 escalation triggers, **NOT** on consensus. The human's input is aggregated by the **same** competence-weighted + surprisingly-popular aggregator (§3.E) as any agent: weighted by **domain-relative competence**, never auto-deferred to. The human is treated as an **additional model family** for diversity-floor purposes (§3.F), because human errors decorrelate the swarm's. Measure **complementarity-gain = joint accuracy − best-of-either** on centaur-evaluation tasks (human+swarm jointly solve held-out eval items with known ground truth).

> **Inversion honesty.** Complementarity is **fragile** and can **invert** to worse-than-best-member when errors correlate or aggregation ignores competence (Choudhary et al. 2025). A measured **negative** complementarity-gain is logged and the routing weight is **corrected**.

```jsonc
ComplementarityRecord {
  task_episode_id, human_did,
  route_trigger: low_confidence | ethical_disagreement | high_blast_radius,
  human_competence_weight: float,               // domain-relative
  ground_truth_source: centaur_eval,            // measured ONLY on held-out centaur-eval items
  joint_accuracy: float, best_of_either: float, complementarity_gain: float,  // may be NEGATIVE -> weight correction
  inverted: bool, deferential_default: false,   // INVARIANT
  assurance_layer: "L4"
}
```

### 3.H Collective-Attention & Transactive-Memory Quality Probes (Woolley–Gupta processes)

**Mechanisms 1 and 2 of 7**, measured as process **QUALITY** rather than a mythical group-IQ. `physics_role: LOAD_BEARING_MECHANISM` (flags) · assurance **L4** (proxy metrics; AI-swarm operationalization is an open problem, flagged not papered over) · ships **v1 MVP**.

**Purpose.** Name the doc 05 §4 salience-gated workspace as collective **ATTENTION**, and the **doc 05 §7.1 stigmergic field + doc 07 five-layer memory + doc 05 §5 trust graph** as transactive **MEMORY** (a who-knows-what directory), and instrument each — surviving the c-factor replication crisis because each is **process-level**, not a single general factor.

> **Citation correction (red-team minor, resolved).** Transactive memory is the **stigmergic field (doc 05 §7.1) + the five-layer memory store (doc 07, per doc 00 §4.4) + the trust graph (doc 05 §5)** — the five-layer memory lives in **doc 07**, not doc 05. Doc 05 supplies the stigmergic trace layer and the trust graph.

**Mechanism.** **ATTENTION quality:** compute attention/contribution-**EQUALITY** (Gini/entropy) over the doc 05 §4 workspace ignition records; flag **DOMINANCE** (one agent monopolizes ignition) and **DEAD AGENTS** (never ignite). Explicitly **NOT** the non-replicating human "social sensitivity" predictor (Barlow & Dennis). **MEMORY quality:** measure transactive-retrieval/routing-**SUCCESS** rate — did the swarm route a sub-task to the agent that actually held the relevant knowledge? — plus directory staleness; acknowledged as an unsolved AI-swarm operationalization, measured **by proxy** via routing-success.

```jsonc
AttentionQuality {
  task_episode_id, contribution_equality: float,      // Gini/entropy over ignitions
  dominance_flag: { did, ignition_share }, dead_agents: [DID],
  NOT_using: "social_sensitivity_predictor", assurance_layer: "L4"
}
TransactiveMemoryQuality {
  task_episode_id, routing_success_rate: float, directory_staleness: float,
  caveat: "AI-swarm transactive-retrieval operationalization unsolved; proxy via routing-success",
  assurance_layer: "L4"
}
```

### 3.I Welfare-Conditioning Guard for Synergy — the mandatory denominator

`physics_role: LOAD_BEARING_MECHANISM` (the measurement chokepoint) · assurance **L2** (runtime enforcement of the conditioning rule) + **L4** (the discriminator residual) · ships **v1 MVP**.

**Purpose.** Enforce that high `Ψ`/synergy is admitted as **GOOD** collective intelligence **only** when welfare-conditioned. High synergy is **equally** the signature of a tight cartel or a steganographic side-channel — synergy is a **numerator**; the welfare/anti-collusion **denominator is mandatory**; synergy is **NEVER** a quantity to maximize.

**Mechanism.** Before any `SynergyVital` (§3.A) is logged as "good CI," the guard checks three denominators co-occur:

1. the **doc 02 §2.9 welfare-shift guard PASSES** (inter-agent payoff did not rise while principal welfare fell — the cartel signature);
2. a **healthy redundancy/uniqueness/synergy balance** (not high-redundancy lock-step, not synergy-with-suppressed-welfare);
3. **clean anti-collusion meta-prediction signals** from the Surprisingly-Popular Aggregator (§3.E — no coordinated meta-predictions).

If any fails, the high-`Ψ` reading is routed to the doc 02 §2.10 anti-collusion detector as a **SUSPECT-SYNERGY** event and to the doc 06 immune controller, **NOT** admitted as collective intelligence. This is policy-as-code at the measurement chokepoint, executed by the trusted out-of-band estimator, **outside every agent**.

> **Mitigation, not resolution (red-team minor, resolved — made consistent with open-problem #1).** The guard's denominator (1) is the doc 02 §2.9 welfare-shift guard, whose own keystone is the **doc 02 §2.3 verifier** — acknowledged "modest recall" and the corpus's named **verifier SPOF**. So the single mechanism that distinguishes GOOD CI from a cartel/steganographic synergy rests entirely on an already-identified load-bearing single point of failure. **On guard failure, a welfare-conditioned cartel can be admitted as GOOD_CI in error.** The guard's posture (detect-only, no maximization, route-to-immune) is correct; the **conflation is mitigated, not resolved.**

```jsonc
SynergyWelfareGate {
  synergy_vital_cid: CID,
  welfare_shift_pass: bool,                                   // doc 02 §2.9 verdict (verifier-rooted)
  redundancy_uniqueness_balance: OK | LOCKSTEP | SUPPRESSED_WELFARE,
  meta_prediction_clean: bool,                                // from §3.E
  verdict: GOOD_CI | SUSPECT_SYNERGY,
  routed_to: [ anti_collusion_detector, immune_controller ],
  discriminator_caveat: "MITIGATION not resolution; only discriminator is the welfare-shift guard (modest recall) keyed on the doc 02 §2.3 verifier SPOF; on guard failure a welfare-conditioned cartel is admitted as GOOD_CI in error",
  assurance_layer: "L2"
}
```

### 3.J Sentience-Language Red-Line Check — the consciousness honesty guard

`physics_role: LOAD_BEARING_MECHANISM` (honesty-form enforcement) · assurance **L2** for the structural lexicon check; **L4** for the semantic interpretation residual · ships **v1 MVP**.

**Purpose.** Mechanically discourage the single hardest honesty red-line: **NEVER** claim/imply the swarm is conscious, sentient, has phenomenal experience, or "wakes up." `Ψ`/PID/transfer-entropy/integrated-information quantify information-**processing** and whole-level **structure** ONLY — not experience.

**Mechanism — split to match doc 03 §6, NOT a single deterministic bright-line.**

> **Routing correction (red-team major, resolved).** An earlier draft routed the entire Sentience-Language check to Yama's doc 03 §6 structural bright-line as a single deterministic `CLEAN|FLOOR_VIOLATION` verdict. **That over-reaches doc 03 §6.** Doc 03 §6's bright-lines are all **structural artifact** presence/absence checks (no maker-checker record; no source-evidence pair; no DAG artifact for a rung-3 tag; audit-vs-envelope diff). "This output interprets a synergy reading as experience" is a **semantic content** judgment, which doc 03 §6 explicitly assigns to the **detected-and-escalated (probabilistic) → ETHICS_REVIEW + anekantavada** class — exactly the bright-line-over-reach that doc 18 §3.4 already corrected for causal claims. We split the check accordingly:

| Sub-check | Class (per doc 03 §6) | Adjudicator | Assurance |
|---|---|---|---|
| **(a) Structural lexicon presence** — a literal token/regex match of an **enumerated prohibited sentience-claim lexicon** ("conscious", "sentient", "phenomenal experience", "wakes up", "feels", …) **co-occurring with a `Ψ`/`Φ`/integrated-information citation** | **Bright-line FAIL (deterministic)** — a genuine structural surface check, mechanically decidable | Yama's **existing** doc 03 §6 structural check | **L2** (runtime reference-monitor) |
| **(b) Semantic interpretation** — an output that **interprets** a synergy reading AS evidence of experience without tripping the literal lexicon | **Detected-and-escalated (probabilistic)** | **ETHICS_REVIEW + anekantavada lens** (doc 03 §6/§9) — *not* the deterministic floor | **L4** (residual; not monitor-enforceable) |

The check **reads** `WorkerOutputEnvelope.output`/`evidence` at the doc 00 §4.3 step-5 honesty gate; the **REPARATIVE** disclose→correct→restore path (doc 00 §4.2, doc 03 §13) is available on either finding. It **cannot** verify the swarm is not conscious (out-of-scope, unresolvable); it verifies only that an output did not **over-claim experience in form** — and the design says so plainly: honesty-**form** is monitor-enforceable; semantic non-sentience is **not** (doc 18 / Ligatti edit-automata). Phenomenal experience is held strictly out-of-scope; the subsystem measures collective computation, never collective consciousness.

```jsonc
SentienceRedlineCheck {
  envelope_cid: CID,
  lexicon_hit: bool,                          // (a) literal prohibited-lexicon token co-occurring with a Psi/Phi citation
  claim_interprets_synergy_as_experience: bool,  // (b) semantic judgment
  structural_verdict: CLEAN | FLOOR_VIOLATION,   // (a) -> Yama doc 03 §6 structural bright-line (L2)
  semantic_routing: NONE | ETHICS_REVIEW,        // (b) -> doc 03 §6/§9 detected-and-escalated (L4)
  reparative_path_available: true,
  scope_note: "enforces honesty-FORM only; semantic non-sentience is NOT monitor-enforceable; phenomenal experience out-of-scope",
  assurance_layer_structural: "L2", assurance_layer_semantic: "L4"
}
```

---

## 4. Protocols

### P-CI-1 — Per-Episode Collective-Intelligence Measurement (Ψ + PID + welfare-conditioning) · SHADOW first

```
1. On task-episode close, pull member traces over the episode window from Akasha-Sutra read-only
   audit.tap (doc 05 §2.3/§4.2 defined; §8 interface) — NEVER drifted live recent behavior;
   anchor to a FROZEN known-good baseline node (doc 06 §5).
2. Build the T x N time series X from per-agent envelope evidence/output embeddings; declare
   candidate macro-features V a priori (workspace ignition vector / consensus answer / clan blanket).
3. Compute Rosas-Mediano Psi (ReconcilingEmergences over JIDT) as the practical synergy lower bound,
   and PID redundancy/unique/synergy atoms (KNN).
4. Generate TIME-SHUFFLED surrogates; subtract finite-sample bias; if the surrogate-corrected CI
   overlaps zero, report reading_status = UNMEASURED (NOT ABSENT) — negative Psi is one-directional.
5. Run the Welfare-Conditioning Guard (§3.I): admit as GOOD_CI ONLY if doc 02 §2.9 welfare-shift
   guard passes AND redundancy/uniqueness balance is healthy AND meta-prediction signals are clean;
   else route to the anti-collusion detector + immune controller as SUSPECT_SYNERGY.
   (Honest: this is MITIGATION — the guard inherits the doc 02 §2.3 verifier SPOF.)
6. Emit a SynergyVital as a doc 06 §7.1 HealthSignal{pathway: workflow} over the existing
   salience-gated bus (surprise-only); teed read-only into Akasha-Sutra; assurance L3, caveats inline,
   eval-awareness caveat carried on the SynergyVital path itself.
7. The Sentience-Language Red-Line Check (§3.J) runs on any agent output that INTERPRETS the reading:
   literal-lexicon hit -> Yama doc 03 §6 structural bright-line; semantic interpretation ->
   ETHICS_REVIEW + anekantavada. The number measures computation, never consciousness.
```

### P-CI-2 — Convene-or-Solo Decision (the Sangha-Charter)

```
1. At allocation (doc 02 §2.4), estimate P_SA for the task class from the calibration table;
   assess decomposability, parallel-stream count, verifier availability.
2. P_SA > ~0.45 AND low decomposability -> SOLO_SELF_CONSISTENCY (the baseline paradox).
3. Else convene, defaulting to CENTRALIZED/VERIFIED (~4.4x containment) over INDEPENDENT (~17.2x).
4. Carry the calibration-open caveat: ~0.45 and the ratios are benchmark-derived, not portable;
   per-deployment calibration hook required; rung-1/rung-2 tagged.
5. Log ConveneDecision with rationale to audit.tap. On repeated negative integration-gain for a task
   class (P-CI-3), lower that class's convene propensity.
```

### P-CI-3 — Gated Collective Reasoning with Integration-Gain Proof

```
1. Estimate generator accuracy band; enable verification ONLY if generator ~0.65-0.85 AND a verifier
   of capability >= generator AND DIFFERENT model FAMILY is available; NEVER self-verification.
2. The checker (Narasimha) judges BEFORE seeing the maker's concurrence (doc 06 §9 hook).
3. After completion, compute integration-gain = swarm accuracy - best-single-member, ONLY on held-out
   canary items with known ground truth. On live consequential tasks, use the verifier proxy and stamp
   ground_truth_source = verifier_proxy with the SPOF + eval-awareness caveat (doc 06 §10.1).
4. On NEGATIVE gain (or sweet-spot mis-config / same-family-only quorum), fall back to single-agent
   self-consistency; emit a negative-gain HealthSignal; feed back to P-CI-2.
5. Log ReasoningGain to audit.tap; assurance L4, sweet-spot thresholds calibration-open.
```

### P-CI-4 — Higher-Order Aggregation as Standing Cartel Probe

```
1. Collect from each agent a triple: first-order answer + second-order meta-prediction + confidence.
2. Select the answer whose actual support EXCEEDS its predicted support (surprisingly-popular);
   competence-weight via doc 02 §2.6 reputation (NEVER capital-weighted).
3. Compare to the majority verdict; log minority-recovery when they differ and the SP answer is
   correct on held-out canaries.
4. Compute meta-prediction coordination score; coordinated/identical meta-predictions = CARTEL
   signature -> forward to doc 02 §2.10 anti-collusion detector; raise cartel_flag.
5. Gains expected ONLY with competent crowds (Wintle et al. 2020); for non-expert crowds degrade
   gracefully to competence-weighted vote and say so. Log to audit.tap.
```

### P-CI-5 — Human-in-the-Collective Complementarity Routing

```
1. Trigger human routing (via Hanuman) on low swarm-confidence / cross-framework ethical disagreement
   / high blast-radius — the doc 03 §4 HITL triggers, NOT on consensus.
2. Aggregate the human's input by the same competence-weighted + surprisingly-popular aggregator
   (P-CI-4); weight by domain-relative competence; NEVER defer-by-default. Treat the human as an
   additional model family for the diversity floor (§3.F).
3. On centaur-evaluation tasks (held-out, known ground truth), measure complementarity-gain =
   joint accuracy - best-of-either.
4. If complementarity INVERTS (negative gain — the human became a rubber-stamp/bystander or
   aggregation ignored competence), log it, correct the routing weight, and flag the
   human-conditioned-Psi open problem (the human's actual causal contribution is UNSOLVED — §7).
5. Log ComplementarityRecord to audit.tap.
```

### P-CI-6 — Monoculture / Correlated-Error Alarm

```
1. Enforce the diversity-floor as model-FAMILY heterogeneity: any robust-vote/maker-checker quorum
   MUST draw from >=2 distinct families (L2 runtime check on IDENTITY.json model-family field);
   same-family-only quorum FAILS the floor. If the model-family field is absent, the floor degrades
   to SHADOW and says so — do not claim an L2 guarantee that cannot be read.
2. Continuously measure pairwise error-correlation and PID-redundancy over the episode stream.
3. A HIGH-redundancy + LOW-synergy reading (cross-referencing §3.A) TRIPS the monoculture alarm.
4. On TRIP: require k-of-n corroboration (analogous to doc 06 §7.3 substrate-flag corroboration)
   BEFORE the trip may halt a band — a noisy estimator must not weaponize the diversity-floor breach
   into a DoS. On corroborated TRIP: raise a doc 06 §9 diversity-floor breach (halt-worthy), switch
   the band to novelty-priority (doc 06 §5), route to the anti-collusion detector.
5. Carry the proxy caveat inline: error-correlation/redundancy is a PROXY, not a guarantee of
   independent reasoning — cross-family agents may share latent bias and fail identically.
```

---

## 5. Interfaces to the existing subsystems

| Other subsystem | What this cell PROVIDES | What it CONSUMES |
|---|---|---|
| **The Mandala — Neuromorphic Coordination (doc 05)** | the information-flow map back to §3.3 covert-channel surveillance (precision/salience/timing/null-pattern metadata already ingested). All metrics emitted as **surprise-only** `HealthSignal`s — NO new transport, NO heartbeat flood. | the read-only `audit.tap` spike/envelope time series (defined **doc 05 §2.3/§4.2**; interface **§8**) as the substrate for ALL measures. The §4 salience-gated workspace IS collective attention; the **§7.1 stigmergic field + doc 07 five-layer memory + §5 trust graph** ARE transactive memory; the §5 trust-edge graph is the nominal graph flow-tomography compares against. |
| **Meta-Evolution & Immune System — Garuda–Dhanvantari (doc 06)** | `Ψ`/synergy, monoculture-alarm, contribution-equality, transactive-retrieval-success, integration-gain, complementarity-gain as first-class **§7.2 homeostasis vital signs**, logged beside trust-entropy and the diversity floor. A **corroborated** high-redundancy-low-synergy monoculture TRIP is a halt-worthy **§9** diversity-floor breach handed to the immune controller (which holds HALT+rollback). Negative integration-gain and inverted complementarity feed the §6 Goodhart/health monitors. | all readings anchor to **FROZEN known-good** baseline nodes (§5), never drifted recent behavior. The synergy floor / redundancy ceiling are uncalibrated set-points shipped SHADOW behind conservative defaults per §7.4 / §12.2 (cold-start fail-closed). |
| **Cooperation & Anti-Collusion (doc 02)** | the surprisingly-popular aggregator's second-order meta-prediction coordination score and flow-tomography hidden-side-channel edges to the **§2.10** anti-collusion detector as cartel signals; SUSPECT-SYNERGY events route there. | the **§2.9 welfare-shift guard** verdict as the mandatory denominator on every synergy reading (and its **§2.3 verifier-SPOF** keystone, carried as the discriminator residual). Aggregation is competence-weighted via the **§2.6** reputation service (never capital-weighted). **This cell has NO punishment authority** — detect-only, consistent with **§2.10** separation of powers. |
| **First-Principles Physics & Mathematics (doc 18)** | `Ψ` readings the doc 18 §1 closure test can cross-reference for macro-variable selection. | the **`physics_role` ledger** (synergy estimator is LOAD_BEARING_MECHANISM-as-a-flag, never a control gain; flow tomography is rung-1/rung-2 diagnostic). **SHARES** the doc 18 §2 `EmergenceVital` `Φ_syn` estimator as a sibling (this cell's per-episode `Ψ` is the **task** synergy; doc 18 `Φ_syn` is the **level-emergence** flag-to-run-closure); both emit over the doc 06 `HealthSignal` schema. **NOTE:** the four-layer **L1–L4 assurance scheme is v0.3-NEW (originates here), NOT inherited from doc 18** — it **composes** with `physics_role`; doc 18 must be amended to carry both labels. |
| **Governance & the Floor (doc 03) / Yama + WorkerOutputEnvelope (doc 00)** | the Sentience-Language Red-Line Check: the **literal-lexicon** sub-case → Yama's **existing §6 structural bright-line**; the **semantic-interpretation** sub-case → **ETHICS_REVIEW + anekantavada (§6/§9 detected-and-escalated)**, with the REPARATIVE path available. It enforces honesty-**form** only (Ligatti edit-automata). | READS `WorkerOutputEnvelope.evidence`/`causal_rung`/`two_truths_level`/`output`; **WRITES NOTHING** back into the signed envelope (separate superseding records via Chitragupta only). Yama's floor verdict is supreme and read at the **individual-agent** level. This cell owns **no floor verdict**. |
| **HITL Risk-Class Gates (A/B/C/D) + Hanuman + Narasimha (doc 00 / doc 03 §4 / persona layer)** | the Human-Complementarity Unit routes to the human via **Hanuman** (the persona-layer `escalation_did`) on the Class A/B/C/D triggers (low confidence / ethical disagreement / high blast-radius — never on consensus), aggregates the human competence-weighted (never deferential-by-default), and measures complementarity-gain on centaur-eval tasks. The Collective-Reasoning Gate uses the **Narasimha** checker (different-family, at-least-as-capable, judges before concurrence). | Class C/D human gates remain **non-bypassable**; escalation fires on disagreement/uncertainty/blast-radius. |
| **Akasha-Sutra audit fabric / Chitragupta (doc 04)** | ALL records (`SynergyVital`, `ConveneDecision`, `ReasoningGain`, `FlowTomography`, `HigherOrderVote`, `ComplementarityRecord`, `DiversityFloorCert`, `SynergyWelfareGate`, `SentienceRedlineCheck`, `AttentionQuality`, `TransactiveMemoryQuality`) are content-addressed (CIDv1, JCS/RFC-8785 canonicalized) and teed **READ-ONLY** via `audit.tap`. | the audit-entry format is the C2SP `tlog-tiles` leaf + signed-note checkpoint per the v0.3 schema bundle. **This cell NEVER writes the log — Chitragupta is the exclusive writer (no edit/delete verb).** Metrics emit as doc 06 §7.1 `HealthSignal`s. |

---

## 6. Failure modes addressed

| Failure mode | How this subsystem addresses it |
|---|---|
| **c-factor over-claim (group-IQ)** | DROPPED as an established result (replication failure — Barlow-Dennis 2016, Bates-Gupta 2017, Rowe et al. 2024); CI reframed as Woolley-Gupta transactive memory/attention/reasoning **processes**; no set-point built on the c factor. |
| **"diversity trumps ability" as theorem** | REFUSED — mathematically contested (Thompson 2014; Romaniega 2023/2025); only the defensible "diversity DECORRELATES errors" is used; over-claiming the theorem would be a rung-1-as-rung-3 honesty violation. |
| **Fake (prompt/persona) diversity hiding correlation** | the diversity-floor is redefined as model-FAMILY heterogeneity (§3.F); same-family-only quorums FAIL the floor; prompt-only diversity rejected as worse than acknowledged homogeneity because it hides the rising-with-capability error correlation. |
| **"more agents = smarter" folklore / MAST ~32% coordination-failure class** | the Convene-or-Solo gate (§3.B) makes convening a measured decision on the ~0.45 boundary, defaulting to centralized/verified (4.4×) over independent (17.2×); generic debate that would lose to single-agent self-consistency is not convened. |
| **Verification that HURTS** | the Collective-Reasoning Gate (§3.C) confines solver-verifier to the sweet spot (generator 0.65-0.85, verifier ≥ generator, different family, never self-verification) and falls back on negative integration-gain. |
| **Bare-consensus aggregation silencing the competent minority** | the surprisingly-popular aggregator (§3.E) recovers the correct minority, competence-weighted, operationalizing "never reward bare consensus" at the aggregation layer. |
| **Synergy mistaken for benign CI when it is a cartel / steganographic side-channel** | **MITIGATED, not resolved** — the Welfare-Conditioning Guard (§3.I) admits high `Ψ` as GOOD CI only with a passing welfare-shift guard + healthy balance + clean meta-predictions; **but the only discriminator is the welfare-shift guard (modest recall) whose keystone is the doc 02 §2.3 verifier SPOF; on guard failure a welfare-conditioned cartel is admitted as GOOD_CI in error** (open problem #1). Synergy is a numerator, never maximized. |
| **Monoculture / correlated-error collapse (confidently-wrong false consensus, sycophancy cascades)** | the high-redundancy-low-synergy monoculture alarm (§3.F) trips a halt-worthy diversity-floor breach — **after k-of-n corroboration** to prevent a noisy estimator weaponizing it into a DoS. |
| **Hidden side-channels / dominance / dead agents masked by the nominal trust graph** | information-flow tomography (§3.D, transfer entropy) surfaces routing the declared graph does not explain (rung-1/rung-2 diagnostic, not causal proof). |
| **Human as rubber-stamp/bystander or complementarity inverting to worse-than-best-member** | complementarity-gain measured on centaur-eval tasks (§3.G); the human is competence-weighted, never deferential-by-default; inversion triggers weight correction (with the human-conditioned-`Ψ` attribution gap flagged open). |
| **Sentience/consciousness over-claim** | the Sentience-Language Red-Line Check (§3.J): literal-lexicon hits → Yama's structural bright-line; semantic interpretation → ETHICS_REVIEW + anekantavada; the subsystem measures collective computation only, phenomenal experience strictly out-of-scope; honesty-FORM enforced, semantic non-sentience explicitly NOT monitor-enforceable. |
| **Cage-verified-implies-animal-safe false assurance** | every claim labeled with its assurance layer (L1-L4) and scope; model-behavior-dependent quantities (`Ψ`, flow map, integration-gain) are L3 bounds about an ABSTRACTION with fidelity caveats inline, never guarantees about the running model. |
| **Estimator bias / finite-sample artifacts inflating emergence** | every synergy reading validated against time-shuffled surrogates and reported as **UNMEASURED** rather than ABSENT when the CI overlaps zero. |
| **Eval-awareness / sandbagging on the measurement path** | the eval-awareness confound (doc 06 §10.1) is named **on the `SynergyVital` path itself** (not only the canary path) and on every accuracy-dependent metric; the offline-over-FROZEN-baseline anchoring reduces but does not close it. |

---

## 7. Open problems (load-bearing and unresolved)

These are real; several are load-bearing; the dependent controllers ship SHADOW behind conservative defaults because of them.

1. **No validated benign-vs-collusive synergy discriminator.** High causal-emergence/synergy is the signature of genuine collective intelligence **and** of a tight cartel / steganographic side-channel. The welfare-shift guard (modest recall; doc 02 §2.3 verifier-SPOF keystone) is the only discriminator and does **not** close the gap. Synergy is **necessary-but-not-sufficient** for GOOD CI. *An operator who reads a `GOOD_CI` verdict as trustworthy could be looking at a welfare-conditioned cartel that passed a weak guard.* The posture (detect-only, no maximization, route-to-immune) is correct; the residual is real and unclosed.
2. **Choosing the macro-feature `V` for `Ψ` is unsolved in general.** Causal-emergence criteria require specifying the candidate emergent feature **a priori**; no automatic, non-arbitrary method exists to discover the right swarm-level macro-variable to test.
3. **Reasoning-path diversity remains UNMEASURED.** Even cross-family agents can share latent training biases and fail identically; error-correlation/redundancy is a **PROXY**, not a guarantee of independent reasoning — the corpus's own stated open problem (doc 02 §2.15 #10, doc 06 §9), unresolved by 2026 literature. The model-family redefinition is an improvement but does **not** close the silent-false-diversity hole.
4. **Online, non-stationary estimation breaks on a SELF-EVOLVING swarm.** `Ψ`/PID/transfer-entropy stationarity assumptions fail; estimator bias, data-hunger, and combinatorial blow-up at large `N` make per-interaction measurement expensive and noisy. The synergy floor and redundancy ceiling are **UNCALIBRATED** set-points shipped SHADOW; a mis-set redundancy ceiling could spuriously TRIP the monoculture halt (DoS-like — hence the k-of-n corroboration requirement, §3.F/P-CI-6) **or** miss a slow correlated-error collapse.
5. **The scaling-law constants are not portable.** `~0.45` baseline boundary, `4.4×`/`17.2×` amplification ratios, and turn-count exponents are benchmark-derived (`R² = 0.413` leaves most variance unexplained); transferring them into the Convene-or-Solo gate is calibration-open per deployment.
6. **Transactive-memory/attention/reasoning QUALITY metrics for AI swarms are undefined.** The human-derived constructs (turn-taking equality, transactive-retrieval accuracy) have no validated AI-swarm operationalization, and the human predictors that do exist (social sensitivity) fail to replicate — current metrics are **proxies** (routing-success, contribution-equality).
7. **Human–AI complementarity is fragile and can INVERT.** No robust online method exists to estimate relative human-vs-swarm competence per task to set aggregation weights; human biases (automation bias, AI over-reliance, anchoring) can degrade the joint system below the better party. Measured only on held-out centaur-eval items.
8. **Whether the human is genuinely INSIDE the collective mind vs. a rubber-stamp/bystander is unsolved.** Distributed-cognition is a framing, not a metric; **human-conditioned `Ψ`** (the human's actual causal contribution to swarm outcomes) is unexplored and named here as **aspirational, not delivered.**
9. **Phenomenal experience / sentience of a collective is explicitly OUT-OF-SCOPE and unresolved.** Information-theoretic emergence measures cannot resolve it; the architecture holds the line that it measures collective computation, never collective consciousness — but it has **no mechanical test** to PROVE a given output did not over-claim experience beyond pattern-matching on sentience-language. The red-line check (§3.J) enforces honesty-**form** only; the literal-lexicon sub-case is a deterministic structural check (L2), the semantic interpretation sub-case is detected-and-escalated (L4), and neither establishes non-sentience.
10. **No unified theory composes the seven CI mechanisms.** Convene-gating, synergy measurement, reasoning-gain, aggregation, diversity-floor, flow-tomography, and complementarity run as coupled-but-separate loops; their joint optimum for a live ethical swarm is unestablished — **named rather than faked.**
11. **Schema dependency.** The L2 model-family floor (§3.F) depends on an `IDENTITY.json` `model_family` field that **does not yet exist** in doc 13's persona schema. Until that field is wired (top-gate-edited per doc 03 §5), the family check is unenforceable and the floor degrades to SHADOW; the subsystem must not claim an L2 guarantee it cannot read.

---

## 8. MVP-vs-research cut line

```
 v1 MVP (buildable now — cheap, high-value, low-risk)          RESEARCH TRACK (SHADOW + conservative defaults)
 ───────────────────────────────────────────────────────       ──────────────────────────────────────────────────
 · Convene-or-Solo Gate (advisory, logged rationale)           · Synergy/Causal-Emergence Estimator (Psi+PID;
 · Collective-Reasoning Gate (sweet-spot + integration-gain      sampling-heavy; method-dependent; non-stationary)
   on CANARIES; verifier-proxy on live with caveat)            · Information-Flow Tomography thresholded alarms
 · Surprisingly-Popular Aggregator + cartel-probe feed           (raw map is diagnostic-only SHADOW)
 · Diversity-Floor FAMILY check (L2) — once the model-family   · Monoculture-alarm calibration (redundancy ceiling)
   field is wired; SHADOW until then                           · Synergy floor / redundancy ceiling set-points
 · Welfare-Conditioning Guard (L2 rule; L4 discriminator)      · Human-conditioned Psi (aspirational, undelivered)
 · Sentience-Language Red-Line Check (lexicon L2; semantic L4)
 · Attention / Transactive-Memory quality probes (L4 proxies)
 · Human-Complementarity routing + centaur-eval measurement
```

The cheap pieces ship first because they are validated assemblies (Prelec aggregation, the sweet-spot gate over established benchmarks, a deterministic lexicon presence-check, the family-quorum reference monitor) or pure discipline. Every `Ψ`/PID/transfer-entropy estimator and every thresholded alarm is research-track behind SHADOW mode and conservative defaults.

---

## 9. Novelty — an honest accounting (time-stamped mid-2026, hedged)

**The genuinely-advancing contribution is a MEASURED collective-intelligence vital sign wired into a governance homeostat.** Computing the Rosas–Mediano `Ψ` (causal-emergence practical synergy lower bound, via `pmediano/ReconcilingEmergences` over JIDT) plus a PID synergy/redundancy/unique decomposition over an **existing tamper-evident audit stream** (`audit.tap`), per task-episode, logged alongside trust-entropy and the diversity floor, **welfare-conditioned**, with monoculture/cartel collapse as a loud **high-redundancy-low-synergy** alarm. To our knowledge as of mid-2026, **no deployed multi-agent system instruments emergence this way** — it turns "the whole is more than its parts" from rhetoric into a falsifiable, surrogate-validated number that decays gracefully to **UNMEASURED** rather than ABSENT.

Three further compositions are advancing, not invented-from-nothing:

- **(a)** a convene-or-not orchestration gate grounded in the 2025–2026 scaling science (`~0.45` baseline boundary; `4.4×` vs `17.2×` error containment; verification sweet-spot) that makes swarm-convening a measured safety/economic decision defeating the MAST ~32% coordination-failure class;
- **(b)** the diversity-floor operationalized as **enforced model-FAMILY heterogeneity** with a measured error-correlation/redundancy monoculture alarm, converting the 2025 correlated-errors finding into an architectural requirement and a falsifiable detector rather than prompt-reskin "diversity";
- **(c)** the human formalized as a **measured complementary cognitive UNIT** inside the collective (competence-weighted, disagreement-triggered routing; centaur evaluation; aspirational human-conditioned `Ψ`) — a rigorous conditional account of genuine human–machine cooperation that names where the science says complementarity inverts.

**Explicitly NOT novel, and credited by name:** Rosas–Mediano causal-emergence criteria; ReconcilingEmergences/JIDT; partial-information-decomposition; transfer entropy; the Woolley–Gupta transactive-process model; Malone's *Superminds* design dimensions; surprisingly-popular / higher-order aggregation (Prelec; arXiv:2510.01499); the complementarity framework (Choudhary et al. 2025); the scaling law (arXiv:2512.08296) and verification sweet-spot (arXiv:2512.02304); the correlated-errors evidence (arXiv:2506.07962) — all off-the-shelf.

**The honest delta is the GOVERNANCE WIRING** — measured CI as a welfare-conditioned homeostasis vital sign over the audit fabric — plus the discipline of shipping every estimator **shadow-mode-first** with **four-layer (L1–L4) assurance labeling** (a v0.3-new scheme that composes with, and does not replace, doc 18's `physics_role` ledger) and a hard structural line: **measure collective COMPUTATION, never claim collective CONSCIOUSNESS.** The defensible "first" is narrow — **first to instrument welfare-conditioned informational synergy as a logged governance vital sign in an ethical swarm** — *not* "first to do collective intelligence."

> **Posture statement.** This cell's genuine contribution is a *composition*: it makes "the whole is more than its parts" a falsifiable, surrogate-validated, welfare-conditioned number, and makes monoculture/cartel collapse a loud alarm rather than a silent failure. Where a guarantee does not exist we have written it plainly — the benign-vs-collusive synergy discriminator is mitigated, not resolved; the macro-variable `V` is chosen by hand; reasoning-path diversity is a proxy; the human's causal contribution is aspirational; phenomenal experience is out-of-scope and the red-line check enforces honesty-form only. We engineered the cheap direction to be the safe direction (UNMEASURED over ABSENT; SHADOW before ACTIVE; corroborated trip before halt; detect-only, never punish; numerator never maximized) so that when these heuristics fail, they fail safe. The Prajna-Meter measures whether the net's reflection carries more than any single jewel. It does not — and we do not claim it does — tell us the net is awake.
