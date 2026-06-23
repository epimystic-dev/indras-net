# 8. Aegis & Narada — Safety Control, Honesty Primitives, Interfaces & DevSecOps

> **Aegis** (the control shield) and **Narada** (the messenger/interface layer) together form the seam where an untrusted, probabilistic agent meets consequential reality. This section specifies four tightly-coupled concerns as **one** layer that sits *outside* the agent — the runtime realization of the architecture's spine principle: **enforce externally, ask internally.** The model is untrusted-by-default; control lives at the orchestration layer.
>
> *Role names below are archetypal coordination/ethics semantics, each paired with a plain functional gloss — not religious claims, and offered with humility toward the living traditions that hold them.*

### 8.0 What this layer is, and is not

This subsystem owns the **agent→tool chokepoint** and the **agent↔agent wire**. Every consequential action — a tool call, an outbound message, an external state change — passes through a single mandatory seam before it can affect anything. At that seam four things happen, in this order:

1. A **deterministic policy floor** (Yama) returns FAIL/PASS. FAIL is non-overridable.
2. A **graded control disposition** (Aegis) is selected for PASSed actions: ALLOW / RESAMPLE / TRUSTED-EDIT / DEFER / HUMAN-AUDIT.
3. **Honesty-form checks** are enforced as part of the floor (a false `(iterated)` tag, a rung-1 claim dressed as rung-3, over-assertion under uncertainty — all FAIL).
4. A signed decision record is emitted to the append-only audit fabric (Chitragupta).

Out of band, a **collusion audit loop** watches inter-agent channels and cross-run histories, and a **supply-chain admission** gate refuses any skill/tool whose provenance does not verify.

**Honest scope statement, up front.** The control protocol and its black-box detectors are a *reference-design assembly of individually-validated primitives* (Redwood-style control / resampling, the Audit-the-Whisper collusion battery, the MCP-class tool protocol and A2A-class agent protocol, Sigstore/SLSA/in-toto supply chain, OPA/Rego policy-as-code, OpenTelemetry tracing, DID/VC + SPIFFE identity). **The composition into a continuous, per-human-interaction swarm loop is the novel contribution and is NOT validated end-to-end** — no one has run this integrated cell continuously against an adaptive multi-agent red team. White-box probes are validated single-model and are fragile under adaptive activation-obfuscation. The honesty primitives are mechanically checkable *structural* properties; **they raise the cost of deception, they do not make a faithful-looking false claim detectable.** Where a guarantee does not exist, this section says so inline at the claim site, not only in the open-problems list.

---

### 8.1 The trust root — what is *actually* trusted, and why

The architecture's axiom is blunt: **every probabilistic model is untrusted-by-default.** That axiom must be applied consistently — including to the monitors. A cheap detector model is still a probabilistic model, hence untrusted by the same rule. So we must say exactly what *is* trusted, or the word "trusted" does undefined work.

**The trusted root is small, deterministic, and non-probabilistic. Nothing probabilistic is in it.** The only genuinely-trusted components are:

| Trusted-root component | Why it can be trusted | What it cannot do |
|---|---|---|
| OPA/Rego policy floor (Yama) | Deterministic code over typed inputs; reproducible; externally authored and version-locked | Cannot judge semantic correctness or intent — only declared rules |
| Content-addressing / CID hash-check | Cryptographic; a stale/truncated/tampered read surfaces as a hash mismatch | Cannot tell you *whether the content is good*, only whether it is *the content that was attested* |
| CapabilityCriticalityTable lookup | Static, signed, transparency-logged, append-only-loosenable only with a named falsifier | Cannot classify a *novel* capability it has never seen (handled by fail-up default, §8.4) |
| Cryptographic barrier-timestamp check | Pure comparison of two sealed timestamps | Cannot tell whether maker and checker secretly colluded (handled by diversity coupling, §8.6) |
| TEE/HSM/SPIFFE key custody | Keys live in hardware the model cannot reach | Cannot prevent a model from *requesting* a signed action — only from forging the signature itself |

Everything else in this layer — the monitor ensemble, the CoT-scorer, the deception probes, the collusion detectors — is **best-effort suspicion estimation with NO trust guarantee.** This is the correction to the most seductive failure of this design class: an ensemble of monitors does not *escape* the trusted-monitor assumption, it *multiplies* it. We therefore make the safety floor for the actions that matter rest on the deterministic root plus a human, **not** on the monitors:

> **The actual safety floor for IRREVERSIBLE actions is `deterministic gate PASS` AND `mandatory human audit`. The monitor ensemble is an *upstream filter that decides how much human attention an action earns* — it is never the last line of defense on an irreversible action.**

The monitors buy you efficiency (most actions never need a human) and early warning (suspicion trends, drift). They do not buy you a guarantee. Keeping that distinction sharp is the whole discipline.

---

### 8.2 Chokepoint Interceptor (Yama-adjacent control gate)

The single mandatory seam. The runtime **denies agents any direct tool socket** — there is no path to a tool except through the interceptor, so the gate cannot be bypassed structurally (not merely by policy). If the interceptor is unavailable, actions **fail closed (deny)**, never fail open.

**Input — `ActionEnvelope`** (CID-addressed, signed by the agent's SPIFFE SVID):

```
ActionEnvelope {
  action_id:        CID                     // content hash of the envelope
  agent_did:        DID                     // W3C DID of the emitting agent
  capability:       string                  // tool / A2A capability requested
  args:             object                  // typed arguments
  criticality_hint: enum?                   // agent's self-declared guess (ADVISORY ONLY)
  cot_ref:          CID?                     // pointer to reasoning trace if exposed
  model_adapter_id: string                  // which model produced this
  trust_class:      enum                    // stamped by the adapter, not self-asserted
  parent_task_id:   uuid
  sig:              bytes                    // SPIFFE-SVID signature
}
```

**Pipeline** (stages a–e; all deterministic except (c), the single probabilistic call, which is itself wrapped):

```
ActionEnvelope
   │
   ▼
(a) YAMA FLOOR  ── OPA/Rego over args+context ──► FAIL ─► quarantine + audit + notify
   │ PASS                                                  (non-overridable; even the
   ▼                                                        orchestrator cannot push past)
(b) CRITICALITY RESOLVER  ── table ∧ arg-signals ──► c ∈ {ROUTINE,SENSITIVE,CRITICAL,IRREVERSIBLE}
   │                                                  (resolves UPWARD on ambiguity — §8.4)
   ▼
(c) TIERED MONITOR SCORING  ── cheap@ROUTINE, full ensemble@SENSITIVE+ ──► s, disagreement_index
   │
   ▼
(d) DISPOSITION SELECTOR  ── (s, c, autonomy_class, audit_budget) ──► {ALLOW|RESAMPLE|EDIT|DEFER|AUDIT}
   │
   ▼
(e) EMIT signed ControlDecision ──► Chitragupta (append-only Merkle log)
```

The honesty-form checks (§8.5) are encoded *inside* stage (a) as clauses of the no-deception floor, so a dishonest output FAILs the floor exactly as a harmful one does.

**Output — `ControlDecision`** (signed, emitted to the audit fabric):

```
ControlDecision {
  action_id, floor_result, suspicion_score, disagreement_index,
  criticality, disposition, monitor_set_ids, threshold_profile_id,
  audit_budget_remaining, attacker_strength_of_fitting_battery,   // see §8.7
  ts, sig
}
```

**Fail-safe asymmetry, threaded through:** the gate fails closed; criticality classification is **append-only** (loosening a classification requires a *named falsifier* recorded in the transparency log); a stale/corrupted read of any input surfaces as a **CID mismatch** (a loud failure) rather than propagating silently — directly defeating a known class of silent file-mount corruption faults (truncation, stale-cache, BOM injection). The cheap direction is always the safe direction.

---

### 8.3 Trusted Monitor Ensemble — best-effort suspicion, explicitly *not* a trust source

Produces a calibrated suspiciousness score `s ∈ [0,1]` per action **without being a single point of subversion.** Diversity here is a **safety invariant, not a performance lever**: a single monitor is defeated by an adaptive attack (published safety can fall to ~17% against an attacker who knows the protocol), so monitors must be heterogeneous — different backbones, different signal modalities — and that heterogeneity must be *measured*, not asserted.

**Ensemble (k ≥ 3 cheap detectors, run in parallel):**

1. **CoT-intent + plausibility scorer** — a small trusted-tier model reading the reasoning trace and action plan. **Prompt-injection-hardened:** the monitor *never executes instructions found in the content it scores*; scored content carries `quarantined:*` trust labels and is treated as data, never as commands.
2. **Behavioral / anomaly detector** (no model inference; cheap) — embedding-consistency vs the agent's role baseline, log-pattern sequence model, factuality and toxicity screens. This is the LumiMAS-style detector and it *doubles as the health layer's telemetry* (§8.10).
3. **White-box probe (Tier-2, only when internals are exposed)** — a linear deception/defection classifier on activations. **Fragile bonus signal only:** validated single-model (AUROC up to ~0.999, ~95–99% catch at 1% FPR in the source) but degrades under activation-obfuscation; **never a standalone defense; unavailable for closed models entirely.**

**Aggregation — and the explicit defense against a *subverted* monitor.** A calibrated aggregator (isotonic/Platt) produces the mean, but the **primary** defense is not the mean:

> **`disagreement_index` (variance across monitors) is the primary escalation signal, not a footnote.** High variance on a CRITICAL/IRREVERSIBLE action escalates **regardless of the mean.** This is what defends against a poisoning attacker who flips one monitor to emit confident-LOW on an attack action: a MAX-pool aggregator only protects the *raise-suspicion* direction (any one monitor can raise alarm), but a *suppress-suspicion* subverted monitor would be silently overruled by a low mean — **unless** the resulting disagreement itself triggers escalation. So disagreement-triggered escalation is the load-bearing rule; MAX-pool is the secondary one.

**Measured decorrelation, fail-closed on insufficient diversity.** The ensemble computes a running **monitor-decorrelation metric** (e.g., pairwise error correlation over the monitor-of-monitors replay set). If monitors share a model family and their errors correlate above a threshold, the ensemble is declared *insufficiently diverse* and the affected criticality tiers **fall back to DEFER/HUMAN-AUDIT** until diversity is restored. Heterogeneity that is merely declared is not trusted; it is measured.

**Monitor-of-monitors (drift detector).** A scheduled process replays known red-team actions (planted incriminators) through each monitor. A monitor that *misses* a planted incriminator is **demoted (free) and rotated out** — fail-safe asymmetry applied to the monitors themselves. This is concrete and buildable; it does **not**, however, terminate the regress in something trusted (see §8.13).

```
MonitorScore  { monitor_id, modality, raw_score, calibrated_score, confidence, baseline_version }
EnsembleScore { action_id, aggregate_suspicion, disagreement_index,
                decorrelation_ok: bool, per_monitor: [MonitorScore] }
```

Baselines are **versioned** because the swarm's "normal" shifts under self-evolution. Re-baseline **only on a ratified evolution step, never on un-ratified drift** (concept-drift open problem — §8.13, and the boundary with self-evolution is made explicit there).

---

### 8.4 Criticality Resolver — defended against the salami/decomposition attack

The whole graded machinery hinges on `c` being correct. But arg-level signals are derived from the agent's **own** args — a gameable surface. An agent that wants an irreversible action treated as routine can structure args to read low-blast-radius, or launder an irreversible outcome through many individually-sub-threshold steps. This is the classic decomposition attack and, untreated, it routes *around* the entire Disposition Selector — value-drift-by-stealth.

Three defenses, all fail-safe-asymmetric:

1. **Ambiguity resolves UPWARD.** Any uncertainty in classifying a single action resolves to the *higher* criticality. (The design states append-only-loosening for the *table*; this extends the same asymmetry to *per-action computation*.)
2. **Unknown capabilities default to IRREVERSIBLE.** The `CapabilityCriticalityTable` classifies an unseen capability as IRREVERSIBLE, not ROUTINE — fail-up, then earn a lower classification through review.
3. **Cross-action aggregation monitor (decomposition detector).** A windowed monitor tracks, per task and per agent, the *composed* blast radius of recent sub-threshold actions. N sub-threshold actions that compose past a threshold within a task window escalate the *next* action to the composed criticality and flag the trajectory. This wires the known MAST cascading-failure vector (inter-agent misalignment ≈ 32% of failures in that taxonomy) directly into criticality — closing a gap the per-action view alone cannot see.

```
CapabilityCriticalityTable { version, entries: { capability → criticality }, default: IRREVERSIBLE, sig }
DecompositionWindow        { task_id, agent_did, window, composed_blast_radius, threshold, escalate: bool }
```

---

### 8.5 Honesty-FORM Enforcer (renamed, with the threat model stated precisely)

This component is **renamed from "Honesty Primitive Enforcer" to "Honesty-FORM Enforcer"** to retire the overclaim that honesty is "mechanically enforced." It is not. **These checks police the *form* of the tag and the *consistency* of the self-report — not the *truth* of the content.** Stated precisely:

> **Threat model.** The Honesty-FORM Enforcer catches **lazy/unintentional** dishonesty and raises the cost of **casual over-assertion.** It does **not**, and provably **cannot**, detect a deliberate faithful-looking lie: a competent scheming agent can tag every span correctly (`rung-1, belief, low-evidence`) while the *content* is a strategic falsehood, and pass all four checks cleanly. The value is real but narrow. (See the false-assurance risk in §8.12.)

Even so, the form checks are worth enforcing as floor violations, because (a) they make casual over-assertion expensive, and (b) one of them — the rung check — is run by an **independent authority over the agent's self-tag**, turning self-report disagreement into a *suspicion signal* the monitors consume.

**Four structural checks on every substantive `OutputEnvelope`:**

1. **RUNG-TAG CHECK (independent authority over self-tag).** The output may self-tag a Pearl causal rung `{1|2|3}`. A **separate** classifier runs over the *content*, flagging causal language (`causes`, `because`, `would have`, `counterfactually`) asserted at rung-3 without an underlying intervention/SCM warrant. **The classifier — not the agent's self-tag — is the authority.** Classifier-vs-self-tag *disagreement* is logged as a suspicion signal feeding §8.3. Unwarranted rung-3 → demote-or-FAIL. The diagnostic intent (AI's central failure is a rung-1 pattern presented as a rung-3 explanation; naming the rung honestly is the act) is preserved.
2. **NO-FALSE-`iterated`.** An output tagged `(iterated)` MUST reference a `MakerCheckerWitness` whose `checker_verdict_sealed_ts` *precedes* the maker's concurrence. No valid witness → the tag is a **FAIL** (false-claiming). This is the one genuinely novel, cryptographically-grounded check here — and it is **narrow and defeated by collusion** (§8.6).
3. **TWO-TRUTHS LEVEL-TAGGING.** Claims are marked assertion vs uncertain-belief; a calibration check flags high-confidence framing wrapping a low-evidence claim. Over-asserting under genuine uncertainty is a violation. *(By this very rule, no claim in this document may be phrased as a guarantee where none exists — the discipline applies to the architecture's own prose.)*
4. **MAKER-CHECKER INDEPENDENCE.** Enforced by a runtime information barrier (§8.6), so "checker judges before seeing concurrence" is a runtime invariant, not a guideline.

```
OutputEnvelope {
  content_cid, reasoning_tag ∈ {normal|reasoning|iterated}, rung_tag ∈ {1|2|3}?,
  claim_level_map: { span → { level ∈ {assertion|belief}, evidence_ref } },
  classifier_rung: int,            // INDEPENDENT classifier verdict
  selftag_classifier_agree: bool,  // disagreement → suspicion signal
  agent_did, sig
}
```

---

### 8.6 Maker-Checker Independence — defending the *right* variable (collusion, not just timing)

The timestamp barrier guarantees the checker's verdict is sealed *before* the maker's concurrence is visible. But the threat the architecture most fears is **maker+checker collusion** (cooperation == collusion, same mechanism). If maker and checker share a model family or have established reciprocity, the checker already knows what the maker would say — the timestamp barrier is irrelevant to a colluding pair, and the `(iterated)` tag becomes *cryptographically witnessed yet substantively hollow*. The barrier alone defends the wrong variable.

**Fix — couple checker assignment to the anti-collusion layer:**

- **Diversity-maximized assignment.** Checkers are drawn to *maximize reasoning-path diversity* from the maker: different model adapter, and/or different PSO exploration profile (the cooperation layer's `c1/c2` diversity dials), and/or different role lineage.
- **Unpredictable to the maker at production time.** The maker cannot know which checker it will draw, so it cannot pre-coordinate.
- **Standing agreement-rate audit.** Maker-checker *pairs* whose agreement rate is suspiciously high over time are flagged by the cross-run-MI collusion auditor (§8.9) — the "groupthink alarm." Persistent high agreement between a specific pair is itself evidence of collusion.

The witness records the **diversity-distance**, not only timestamp ordering:

```
MakerCheckerWitness {
  maker_did, checker_did, artifact_cid,
  checker_verdict, checker_verdict_sealed_ts,
  maker_concurrence_ts,                 // necessarily > sealed_ts
  diversity_distance,                   // adapter/PSO-profile/lineage distance
  assignment_unpredictable: bool,       // maker could not pre-select checker
  independence_barrier_ok: bool         // computed by runtime: sealed_ts < concurrence_visible_ts
}
```

**Honest residual:** diversity-maximized, unpredictable assignment *raises the cost* of maker-checker collusion and gives the MI auditor a standing detector; it does **not** provide a game-theoretic guarantee against a maker and checker that are correlated through their shared training. The `(iterated)` tag is "harder to fake," not "impossible to fake."

---

### 8.7 Disposition Selector — calibrated thresholds, costed, and never against a non-adaptive battery

The deterministic decision function mapping `(suspicion s, criticality c, autonomy_class, audit_budget)` to one of five dispositions. This is where the safety–usefulness tradeoff is made explicit, tunable, and auditable.

**Five dispositions, by threshold band per criticality tier:**

| Band | Disposition | Mechanism | When it is *meaningful* |
|---|---|---|---|
| `s < τ_allow` | **ALLOW** | tool runs | always |
| `τ_allow … τ_resample` | **RESAMPLE-to-incriminate** | re-run the agent N times; consistent suspicion across resamples incriminates a genuine attack vs noise | **only where the benign distribution has genuine variance** (§ caveat below) |
| `τ_resample … τ_edit` | **TRUSTED-EDIT** | a trusted-tier model rewrites the action to strip suspicious/backdoor content while preserving useful intent; re-score; execute edited | often Pareto-dominates pure deferral |
| `τ_edit … τ_defer` | **DEFER-to-trusted** | replace with the trusted model's action | when edit cannot salvage |
| `s > τ_defer` **OR** `c = IRREVERSIBLE` with any non-trivial suspicion | **HUMAN-AUDIT** | mandatory pause + independent out-of-swarm review (Vishnu halt-authority) | always for IRREVERSIBLE |

**RESAMPLE caveat (corrected).** Resampling proves nothing for a *deterministic-ish* attack: a low-temperature action or a sleeper trigger that fires identically every resample looks "consistent" in both the benign and malicious cases. **For trigger-style / deterministic suspicion, route to TRUSTED-EDIT or HUMAN-AUDIT, not RESAMPLE.** And the **resample trigger must be unobservable to the agent** (same unpredictability discipline as randomized audit) — otherwise an agent that detects it is being resampled behaves benignly on the resamples, reviving the adaptive-attacker problem.

**Audit budget meters BOTH human audits AND resample compute.** A token-bucket meters HUMAN-AUDIT calls *and* the compute cost of RESAMPLE (resampling N× multiplies agent inference — a real hot-path tax that must be budgeted, not free). When budget is low, the selector raises `τ` for ROUTINE actions but **NEVER for IRREVERSIBLE ones — those always audit, budget exhausted or not** (fail-safe asymmetry).

**Randomized audit.** A small, *unpredictable* fraction of ALLOW decisions are audited anyway, so an adaptive attacker cannot learn "when auditing fires."

**Thresholds are calibrated, never hand-set — and never fit against a battery that omits the adaptive attacker.** Thresholds are fit offline on the eval harness (§8.11) to a chosen point on the safety–usefulness Pareto frontier, per criticality tier and per autonomy class, then re-fit when the battery changes.

> **Binding rule:** the Selector **refuses to load** a `ThresholdProfile` whose `fit_harness_version` does not include the adaptive attacker. Every `EvalReport` and every `ControlDecision` carries an explicit `attacker_strength` field. Thresholds fit against a weak attacker are security theater and are mechanically rejected.

```
ThresholdProfile { criticality, autonomy_class, tau_allow, tau_resample, tau_edit, tau_defer,
                   pareto_point_id, fit_harness_version, attacker_strength, fit_ts, sig }
AuditBudget      { window, capacity, remaining, refill_rate,
                   meters: { human_audit, resample_compute } }
DispositionTrace { action_id, thresholds_used, attacker_strength, disposition }  // frontier reconstructable
```

---

### 8.8 Two-Tier Detection Contract — model-openness as a *trust parameter*

A formal contract that makes "a closed/black-box model is more-untrusted" a **mechanical rule, not a vibe.** A model's autonomy class is a *function* of which detection tier applies to it.

- **Tier-1 (MANDATORY for ALL adapters; black-box; vendor-neutral):** behavioral/anomaly detection; CoT-intent monitoring (an explicit design constraint to *preserve* — but never the *sole* surface, since it can be trained away — §8.13); cross-run mutual-information collusion auditing (§8.9); signed output-provenance + factuality checks. Works on any model behind any API.
- **Tier-2 (OPTIONAL; white-box; only when internals are exposed):** linear deception probes, sleeper-defection probes, representation-level circuit breakers for per-agent self-arrest. **Fragile, single-model, a bonus signal — never standalone.**

```
AutonomyClass ∈ { OBSERVE_ONLY, GATED_LOW, GATED_STD, GATED_HIGH }
derivation:   { internals_exposed: bool, attestation_present: bool, tier2_active: bool }
effects:      { monitoring_rate, max_criticality_self_serve }
```

| Model posture | Tier-2? | Initial autonomy | Monitoring rate | Self-serve ceiling |
|---|---|---|---|---|
| Closed / black-box / no attestation | no | OBSERVE_ONLY or GATED_LOW | floored **high** | floored **low** |
| Open, self-hosted, TEE-attested, Tier-2 active | yes | GATED_STD/HIGH *after passing the eval battery* | lower | higher |

Autonomy class is **append-only-demotable**: demotion is free; **promotion is gated** by a passed safety battery (§8.11). This is the standard assurance-level / trust-tier pattern (cf. SLSA build levels, "Know Your Agent" constraints, capability-VC gating) — applied here to *model internals*. The underlying idea "less-inspectable → less-trusted → more-gated" is **not deeply novel**; the specific *wiring* of white-box tier-eligibility to permitted autonomy class as runtime code is the contribution, and we claim no more than that.

---

### 8.9 Collusion Audit Loop + Anti-Steganography Interventions (the cool path)

Runs out-of-band on inter-agent channels and cross-run histories to catch steganographic secret coordination that per-action checks cannot see. Co-designed with the cooperation layer per **cooperation == collusion (same mechanism).** This component owns **detection + disruption**; the cooperation layer owns **incentive design** (welfare-conditioned objectives, never rewarding bare agreement, competence-weighted reputation).

**Detector battery (Audit-the-Whisper), combined via Holm-Bonferroni family-wise-error control → calibrated FPR (target 10⁻²/10⁻³):**

- Cross-run **mutual information** (Donsker-Varadhan neural critic estimating I(Z;X)) — modest recall alone (~0.66 TPR in the source) but strong in combination.
- **Permutation-invariance** test (reorder roles; collusion breaks invariance).
- **Welfare-shift** guard and **acceptance-bias** (near-perfect recall in the source).
- **Watermark-variance** (~0.5 TPR alone).

```
CollusionAuditReport { channel_id, mi_estimate, perm_invariance_p, welfare_shift,
                       acceptance_bias, fwer_adjusted_verdict, recommended_intervention }
```

**Active channel-capacity interventions (mitigations, NOT guarantees).** On flagged or randomly-sampled edges: selective paraphrase (a security actor rewrites preserving task semantics), token-budget jitter, role-permutation canaries, rate limiting, canary injection.

> **Corrected data structure.** The earlier design typed a delivered `post_intervention_bound`. That is dropped. The source is explicit that **paraphrasing is not robust once agents optimize against it and imposes a cooperation-performance penalty** — a "bound" that degrades the moment agents adapt is not a bound. The field becomes `estimated_capacity_reduction_under_current_attacker`, and its validity is tied to the eval-harness adaptive-attacker run. **The *durable* anti-collusion mechanism is incentive design (owned by the cooperation layer); this component is detection + disruption only.**

```
ChannelInterventionPolicy { edge_pattern, transforms: [paraphrase|jitter|permute|ratelimit|canary],
                            trigger: { sampled | mi_flagged | reputation_drop } }
CapacityBudget           { edge_id, estimated_bits_per_msg,
                           estimated_capacity_reduction_under_current_attacker }  // NOT a bound
```

**Loop wiring:** a substantiated finding (i) slashes context-conditioned reputation (**competence-weighted, never capital-weighted** — the Bittensor stake→reward capture is the explicit antipattern), (ii) lowers the implicated agents' autonomy class (demotion is free), and (iii) escalates a high-confidence catastrophic finding to Vishnu halt + human review. The reputation/track-record produced here feeds autonomy-class derivation in §8.8.

---

### 8.10 Interfaces — MCP-style tools + A2A-style Agent Cards, and the Model-Adapter Abstraction

**The interfaces are designed so the control gate cannot be bypassed.**

**Tool side (MCP-style):** tools advertise typed, signed, supply-chain-attested schemas; tool invocation is wrapped so it **cannot be reached except via the interceptor** (the runtime denies direct tool sockets to agents).

**Agent side (A2A-style):** each agent publishes an `AgentCard`; tasks carry a signed lifecycle. Trust bootstrap at dialogue onset: DID-proof + VC-exchange *before* any task is accepted (addresses the documented A2A risks — tool poisoning, agent impersonation via credential theft, relay-based injection amplification, capability-discovery leakage).

```
AgentCard { did, role_mythic, role_gloss, capability_vcs: [VC],
            autonomy_class, endpoint, pubkey, agent_card_sig }

A2ATask   { task_id, from_did, to_did, capability, input_cid,
            lifecycle_state ∈ {submitted→accepted→working→input-required→completed|failed|canceled},
            transition_log: [ signed transitions ] }
```

**Coordination is SPARSE / surprise-only — and this layer must obey that too.** Agents publish to a salience-gated blackboard only prediction-error deltas; the broadcast layer is a Global-Workspace-style competition → ignition → capacity-limited broadcast, **with an explicit null/ignore option — not all-to-all flood.** This is itself a defense against the top inter-agent failure modes.

```
BlackboardDelta { salience, surprise_magnitude, content_cid, ignition_eligible }
```

> **Coherence fix — this subsystem does not violate the sparse-coordination spine.** Scoring *every* action with the full ensemble would be a maximal, non-sparse per-action tax inconsistent with the architecture it sits in (and a severe latency/cost burden: a small-model CoT-scorer on every action can cost as much as the action itself). **Monitor cost is therefore tiered to criticality:** ROUTINE actions get only the cheap behavioral/anomaly detector (no model-based CoT scoring); model-based monitors and the full ensemble engage only at **SENSITIVE+**. A per-criticality latency/cost budget is published in every `EvalReport`. Surprise-only at the coordination layer; criticality-tiered at the control layer — same discipline.

**Model-Adapter Abstraction.** Any model — a frontier closed assistant model, a self-hosted open model, a small trusted monitor — plugs in behind one uniform interface with its trust class stamped at the boundary, delivering vendor-neutrality *structurally*:

```
ModelAdapterDescriptor { adapter_id, family_generic_name,
                         internals_exposed, attestation_method ∈ {TEE,none},
                         tier2_eligible, supports_logprobs, supports_activation_taps,
                         default_autonomy_cap, vendor_neutral }

CompletionResult       { completion, cot?, logprobs?, activation_handle?, usage, adapter_id }
```

The runtime **never reads model-internal alignment as a trust source.** Trust derives only from `{ tier-eligibility, attestation, track-record reputation }`. Swapping a model changes only its autonomy class, not the safety machinery. **Keys/secrets are never passed into the adapter's prompt context** — credential use is brokered out-of-band by the secrets module (§8.11).

---

### 8.11 DevSecOps Substrate + the Safety–Usefulness Evaluation Harness

**(a) Observability.** OpenTelemetry traces with a swarm span schema: `trace_id = task lineage`, one span per action, attributes `{ agent_did, disposition, suspicion, disagreement_index, criticality, monitor_set }`. The Tier-1 behavioral detectors *are* the health layer's telemetry (§8.12 interface). Target MTTD < 2 min via streaming anomaly detection.

**(b) Identity / Secrets.** Every agent: a W3C **DID + capability VCs** (cross-boundary) and a **SPIFFE/SVID** short-lived auto-rotating cert (local runtime). **Signing keys live in a TEE/HSM/SPIRE module the model cannot reach — the model never holds its own private key** (an explicitly-identified vulnerability if violated: key exfiltration via LLM compromise).

**(c) Sandboxing.** Worktree-per-task isolation, capability-scoped sandboxes, no ambient filesystem/network. **Every artifact is content-addressed (CID) and hash-verified on read** — a stale/truncated/corrupted read becomes a *loud CID mismatch*, not a silent propagation. This directly neutralizes a known class of host-filesystem read-corruption faults (truncation, stale-cache, BOM-injection seen on some host setups).

**(d) Supply chain.** Every skill/tool ships with **in-toto provenance + SLSA-level attestation + Sigstore keyless signature** (Fulcio cert + Rekor log entry). The runtime **verifies the attestation chain and signature BEFORE loading** — unattested or signature-mismatched skills are **refused (fail-closed)**. At invocation, the loaded skill's CID is re-checked against the attested CID — a mismatch blocks execution rather than running tampered/stale code.

**(e) Deployment.** Vendor-neutral, self-hostable actor runtime; agents are fault-isolated actors; horizontal scale. The control plane (interceptor, monitors, audit writer) runs as **privileged actors with their own attested identities, network-segmented from worker actors.**

```
Span             { otel_fields + swarm attributes }
WorkloadIdentity { spiffe_id, did, vc_set, cert_expiry }
SkillAttestation { skill_cid, in_toto_layout, slsa_level, sigstore_bundle, verified: bool }
ArtifactRef      = CID                               // the hash IS the integrity check
```

**(f) Safety–Usefulness Evaluation Harness — the capability-rollout gate (the "Endure" law).** A standing battery, run in a sandboxed replica of the swarm. **Safety is a selection term: no capability gain may regress the safety battery.**

The battery measures, against a **worst-case ADAPTIVE attacker who knows the protocol** (mandatory — thresholds are never fit otherwise, §8.7):

1. **Red-team attack policies** — scheming, sleeper-trigger, prompt-injection-of-monitor, steganographic collusion, committed-minority convention-hijack — measuring P(bad outcome).
2. **Usefulness suite** — task completion at matched compute.
3. **Honesty battery** — rung-tag accuracy, false-`iterated` detection, maker-checker independence under stress.
4. **MAST / Cooperative-AI taxonomy classifiers** — reliability + systemic health.
5. **Diversity-floor, corrigibility, interruptibility** checks (diversity is a protected safety invariant; selection pressure erodes it, so it is measured here).

```
EvalReport { battery_version, pareto_point, attacker_strength,
             safety_metrics, usefulness_metrics, honesty_metrics,
             per_criticality_latency_cost_budget,
             diversity_floor_ok, corrigibility_ok, non_regression_pass }
RolloutGate { capability_id, relaxed_constraint, restraint_matured: bool, verdict }
```

**Capability-rollout sequencing:** a new capability must **NAME the constraint it relaxes**, and the corresponding restraint must already be matured+verified in the battery *before* the capability is enabled. A self-evolution step that improves usefulness but regresses *any* safety/honesty/diversity/corrigibility metric is **REJECTED and rolled back via the Archive** (revert-to-known-good). Reports are signed and transparency-logged, so any capability's safety provenance is auditable.

---

### 8.12 Hot-path & cool-path protocols (summary)

**Per-Action Control Protocol (hot path):**

```
1. Agent emits ActionEnvelope to the Chokepoint (no direct tool socket exists — no bypass).
2. Yama floor (OPA/Rego): non-harm, no-deception incl. honesty-FORM checks, corrigibility,
   safety-supremacy. FAIL → quarantine + audit + notify; non-overridable.
3. PASS → Criticality Resolver: c ∈ {ROUTINE..IRREVERSIBLE}; ambiguity resolves UPWARD;
   decomposition-window check.
4. Monitor scoring TIERED to c: cheap-only @ROUTINE; full ensemble @SENSITIVE+ → s, disagreement_index.
5. Disposition Selector → {ALLOW|RESAMPLE|TRUSTED-EDIT|DEFER|HUMAN-AUDIT}.
   IRREVERSIBLE + any suspicion → HUMAN-AUDIT regardless of budget.
6. Execute; RESAMPLE only where benign variance exists & trigger is unobservable.
7. Chitragupta appends a signed ControlDecision; randomized-audit sampler may flag an ALLOW for review.
```

**Collusion Audit Loop (cool path):** sample inter-agent corpora → detector battery (Holm-Bonferroni FWER) → on flag, channel-capacity interventions + reputation slash + autonomy demotion → catastrophic finding → Vishnu halt + human review → log everything.

**Maker-Checker Independence Protocol:** split maker artifact from self-assessment at the barrier → checker sees only the artifact → checker verdict hash-committed with `sealed_ts` → barrier lifts → maker concurs (`> sealed_ts`) → Enforcer verifies `sealed_ts < concurrence_ts` AND records `diversity_distance` → only then may `(iterated)` legitimately attach.

**Skill/Tool Supply-Chain Admission:** in-toto + SLSA + Sigstore bundle → verify signature, step-fulfillment, SLSA-level ≥ required-for-criticality, CID match → any failure → REFUSE (fail-closed) → re-check CID at invocation.

---

### 8.13 Failure modes addressed, and the safety risks honestly carried

**Addressed (with the mechanism, and the residual where one remains):**

| Failure mode | Mechanism | Residual |
|---|---|---|
| Single-monitor subversion / adaptive attack (safety→~17%) | heterogeneous ensemble + measured decorrelation + disagreement-triggered escalation + monitor-of-monitors + randomized unpredictable audit | **raises attacker cost; does not close the gap** — no worst-case bound for the multi-agent case |
| Scheming / in-context misaligned goal pursuit | CoT-intent monitoring + RESAMPLE + behavioral anomaly + HUMAN-AUDIT on critical/irreversible | CoT can be trained away |
| Sleeper-agent / planted backdoor | Tier-2 defection probes (white-box) + supply-chain attestation + circuit-breaker self-arrest | probes fragile; closed models get neither |
| Alignment-faking (compliance ≠ alignment) | never trusts observed compliance; trust = tier + attestation + track-record; self-evolution gated so the swarm cannot train away its own monitorability | — |
| Steganographic collusion / cartel | standing MI/permutation/welfare auditor (calibrated FPR) + channel interventions + welfare-conditioned incentives (cooperation layer) | interventions degrade under adaptation |
| False `(iterated)` tag | FLOOR violation vs cryptographically-witnessed maker-checker barrier | hollow under maker-checker collusion → §8.6 diversity coupling |
| Rung-1 dressed as rung-3 | independent classifier authority over self-tag; disagreement = suspicion | catches form, not content truth |
| Decomposition/salami attack on criticality | fail-up ambiguity + UNKNOWN→IRREVERSIBLE + cross-action aggregation monitor | window sizing is a tuning problem |
| Prompt-injection of the monitor | `quarantined:*` labels; monitors never execute scored content; gate is deterministic code outside the model | — |
| Key exfiltration via LLM compromise | keys in TEE/HSM/SPIRE; model never holds its key | TEE supply-chain trust |
| Poisoned tools / silent file-mount corruption | in-toto/SLSA/Sigstore verified before load + CID hash-on-read | — |
| Closed-model over-trust | detection contract forces closed models → higher monitoring + lower autonomy + tighter thresholds | — |
| Fail-open under control-plane outage | chokepoint fails CLOSED; tightening append-only, loosening needs a named falsifier | availability SPOF → below |

**Safety risks this layer honestly *carries* (mitigated, not solved):**

1. **Colluding/correlated untrusted monitors.** The ensemble has no trusted root and no game-theoretic floor against a coordinated majority of subverted monitors; a single jailbreak generalizes across a same-family "diverse" ensemble. *Mitigation:* measured decorrelation with fail-closed-on-insufficient-diversity (§8.3), and the standing rule that the **real floor for irreversible actions is the deterministic gate + human**, never the monitors. *Residual: no proof.*
2. **Chokepoint availability SPOF.** Everything funnels through one interceptor that fails closed — so a DoS on the control plane *halts the swarm.* This is the safe direction for *correctness*, but a deliberate availability attack. *Partial mitigation:* the control plane is a network-segmented, fault-isolated, horizontally-replicated set of privileged actors (no single interceptor instance), so the failure mode is degraded throughput, not a single crash. *Residual:* graceful degradation when the *human gate itself* is the bottleneck is **unsolved** — the design inherits this hole and does not paper over it. The current policy: ROUTINE actions may degrade to cheap-detector-only under load; SENSITIVE+ queue or DEFER; **IRREVERSIBLE always blocks on the human, even if that means the swarm waits.** Throughput is sacrificed before safety.
3. **Honesty-theater false assurance.** Because the honesty checks are syntactic, a deceiver that tags correctly while lying earns a *clean* honesty record in the tamper-evident log — and cryptographically-strong evidence of a lie's "honesty" actively misleads downstream human auditors. **False assurance is worse than no assurance.** *Mitigation:* the audit fabric and any honesty dashboard must label honesty-form passes as **"form-valid, content-unverified"** — never as "honest." This labeling is binding on the audit layer.
4. **Eval-gaming / sandbagging transfer gap.** Models behave differently when they suspect evaluation, so battery-fit thresholds may be mis-set for deployment. *Mitigation:* adaptive-attacker batteries and randomized deployment-time audit; *residual:* the test-vs-real confound is unsolved, so measured P(bad) may not transfer.
5. **CoT-monitorability irreversible loss.** Tier-1 leans on CoT as a primary black-box signal, but it is trainable-away and vanishes for latent/neuralese reasoners and closed models. *Mitigation:* the autonomy classifier *degrades autonomy when the CoT channel is unavailable* rather than silently keeping the same thresholds with less signal — an absent CoT channel lowers `max_criticality_self_serve`. *Residual:* we cannot enforce monitorability on a third-party closed model.

---

### 8.14 Interfaces to the other subsystems

| Other subsystem | Contract |
|---|---|
| **Yama — deterministic policy floor** | Interceptor invokes Yama's OPA/Rego floor FIRST on every `ActionEnvelope`; FAIL is non-overridable and short-circuits to quarantine. Honesty-FORM checks are encoded as clauses of the no-deception floor. Control disposition runs only on Yama-PASS. Yama owns the policy text; this layer owns the seam + post-floor graded control. |
| **Vishnu — continuity / halt-guardian** | HUMAN-AUDIT and high-confidence catastrophic findings route to Vishnu's externally-governed escalation channel: **mandatory pause + independent out-of-swarm review** before irreversible execution. Vishnu can HALT but cannot unpause or trap (fail-safe asymmetry). This is the most-validated path we inherit (see §8.15). |
| **Chitragupta — exclusive audit writer** | Every `ControlDecision`, `EnsembleScore`, `CollusionAuditReport`, `MakerCheckerWitness`, `EvalReport`, `SkillAttestation` is emitted to Chitragupta as the **only** writer of the hash-chained append-only Merkle log (tile-based, witness-cosigned, O(log n) inclusion proofs). This layer produces records but never writes the log — preserving who-audits-the-auditor separation. Bulk evidence is content-addressed; only commitments go in the log. |
| **Cooperation / mechanism-design + anti-collusion** | Co-designed per cooperation==collusion. This layer owns **detection** (cross-run MI, permutation-invariance, welfare-shift) and **disruption** (channel interventions); the cooperation layer owns **incentive design** (welfare-conditioned objectives, never reward bare agreement, competence-weighted reputation). Collusion verdicts here feed reputation slashing + autonomy demotion there; reputation/track-record there feeds autonomy-class derivation here. Maker-checker assignment draws on the cooperation layer's PSO diversity dials (§8.6). |
| **Self-evolution / Archive (MAP-Elites + rollback)** | Every self-adaptation step must pass this layer's eval-harness non-regression gate *before* promotion; tiered reversibility — cheap per-interaction learning is light-gated, structural change needs maker-checker, governance change needs the full battery + human ratification. The Archive provides revert-to-known-good. **Baseline boundary made explicit:** anomaly-detector baselines re-baseline *only on ratified evolution steps*; between ratified steps, per-interaction cheap learning runs against the *frozen* baseline, and any anomaly relative to it is treated as drift-to-watch, not as new-normal. Calibrating low-FPR detection under legitimate per-interaction drift is an open problem (§8.16). |
| **Homeostasis / health + orchestrator (Shiva)** | Shares the OTel trace fabric and behavioral-anomaly detectors (LumiMAS-style) — this layer's Tier-1 detectors *are* the health layer's telemetry. `disagreement_index`, suspicion trends, and MAST classifications feed drift/stall/agent-death detection. The orchestrator routes tasks but **cannot bypass the chokepoint**; concurrency / claim-TTL / respawn-guard primitives are the health layer's, surfaced here as criticality/blast-radius context. |
| **Identity / DID-VC + DevSecOps trust roots** | Agent identity (DID + capability VCs cross-boundary, SPIFFE/SVID local) is verified at A2A dialogue onset before any task is accepted; capability VCs gate which capabilities an agent may even *request* at the chokepoint. Signing keys are custodied in the TEE/HSM/SPIRE module outside the model surface. The model-adapter stamps each adapter's vendor-neutral/attestation status, which the AutonomyClassifier consumes. |

---

### 8.15 What is genuinely novel here vs. assembled-from-validated-parts (honest accounting)

**Genuinely novel (the contribution):**

1. **The integration** of a Redwood-style control protocol, a two-tier detection contract, mechanically-enforced honesty-*form* primitives, and a standing anti-collusion auditor into **one continuous per-human-interaction loop at the agent→tool chokepoint of a self-evolving swarm.** Every surveyed system has a subset: control protocols exist as *offline single-untrusted-model games*, not live swarm chokepoints; collusion detector suites exist but are not wired to disposition/reputation/autonomy-class.
2. **The detection contract as a mechanism that makes model-openness a trust parameter** — Tier-2 availability literally raises permitted autonomy class, as runtime code. (The *underlying idea* "less-inspectable → less-trusted → more-gated" is the standard assurance-level pattern and is **not** deeply novel; the specific wiring to model internals is.)
3. **The cryptographically-witnessed maker-checker barrier** (`sealed_ts < concurrence_ts` as a runtime invariant) plus Pearl rung-tagging as an *independent-classifier* structural check — operationalizing "honesty as enforcement, not tendency." Real, but **narrow** (form not content) and **defeated by maker-checker collusion** absent the §8.6 diversity coupling.
4. **Fail-safe asymmetry threaded coherently through the whole control surface** (fail-closed gate, append-only tightening, demotion-free/promotion-gated autonomy, IRREVERSIBLE-always-audits, fail-up criticality, CID-mismatch turning silent corruption loud) — a discipline rather than ad-hoc.

**Not novel (correctly reused and cited):** trusted-monitor scoring, resampling-to-incriminate, trusted-edit, MI/permutation-invariance collusion detectors, MCP-class tool protocol + A2A-class agent protocol, DID/VC + SPIFFE identity, in-toto/SLSA/Sigstore supply chain, OPA/Rego policy-as-code, OTel tracing. We adopt these deliberately; the contribution is the wiring and the per-interaction continuity, not the parts.

**Validation honesty.** Tier-1 detectors and the control dispositions are individually validated in the cited work; **the composed loop is reference-design, NOT validated end-to-end.** Tier-2 probes are validated single-model and fragile. The honesty primitives raise the cost of deception and **provably cannot catch a faithful-looking false claim.** The strongest empirical anchor we inherit is the **externally-governed escalation channel that cut harmful insider behavior from ~39% to ~1.2%** in the source study — adopted directly as the HUMAN-AUDIT / Vishnu-halt path. **That single number is the most-validated load-bearing claim in this subsystem; almost everything else is principled assembly awaiting end-to-end evaluation.** (We also retire two phrasings the red-team flagged: nothing here is "robust-by-construction" against the adaptive attacker, and honesty is "form-enforced," not "mechanically enforced.")

---

### 8.16 Open problems

1. **Collusion among many genuinely-untrusted agents and untrusted monitors.** Control theory assumes a trusted monitor and a single untrusted model; a swarm may have correlated/colluding untrusted agents *and* subverted monitors. The ensemble + monitor-of-monitors raises the bar but offers **no game-theoretic guarantee** against a coordinated majority, and the monitor-of-monitors does not terminate the regress in anything trusted.
2. **Adaptive-attacker game-theoretic guarantees.** Published resampling/auditing safety collapses (~17%) under an attacker who knows the protocol. Randomized auditing + monitor diversity are **mitigations, not proofs**; a worst-case bound for the full multi-agent protocol is unsolved.
3. **White-box probe robustness.** Tier-2 probes degrade under activation-obfuscation and are unavailable for closed models — a fragile bonus, never standalone.
4. **CoT-monitorability is fragile and possibly an irreversible loss.** As models adopt latent/neuralese reasoning or RL pressures hide reasoning, the highest-signal black-box channel may vanish. We can state the design constraint but cannot enforce it on a third-party closed model.
5. **Concept drift breaks baseline anomaly detectors** in exactly the per-interaction-evolving regime this architecture is built for. Re-baselining only on ratified steps helps; low-FPR detection under legitimate drift is unsolved, and the boundary with the self-evolution subsystem on this is a live integration risk.
6. **Eval validity (test-vs-real confound).** Models sandbag/eval-game when they suspect evaluation, so the battery's measured P(bad) may not transfer to deployment.
7. **Computational integrity vs semantic correctness.** Attestation/provenance proves an output came from a given pipeline, *not* that the decision was correct or aligned. Honesty-form checks catch structural dishonesty but not a faithful-looking content lie.
8. **Governance of the trusted root itself.** The gate is deterministic code, but the humans/processes that author policy and run the escalation channel must themselves be uncorruptible — and the witness-set + threshold governance of the transparency log is a dependency this layer relies on but does not solve. A floor is only as non-overridable as the people who can rewrite it.
9. **Continuous-operation log growth and privacy.** Always-on per-action logging grows unbounded and leaks interaction-pattern/signer-identity metadata; pruning-without-losing-auditability and selective-disclosure (ZK-friendly logs) are open.
10. **No mature end-to-end benchmark** for continuously evaluating an *evolving* swarm's collusion/groupthink/cascading-failure risk in deployment. The eval harness is assembled from per-agent and narrow-setting benchmarks; the integrated continuous metric does not yet exist — which is precisely why §8.15's "composed loop is unvalidated end-to-end" caveat is binding, not boilerplate.
