# Formal Models & Safety Verification — the *Pramana-Setu* Cell

> ***Pramana-Setu*** — "the bridge of valid proof." In the classical Indian epistemologies, a *pramāṇa* is a means of valid knowledge — perception, inference, testimony — and the discipline is knowing *which* means warrants *which* claim, and refusing to let one masquerade as another. *Setu* is the bridge. This subsystem is the bridge that carries a claim from **assertion** to **checked proof**, and — just as load-bearingly — that *labels the kind of warrant* each claim actually has. It is presented as an engineering-verification discipline, not a metaphysics, and with humility toward the living traditions the name borrows from.
>
> **The governing sentence of this entire document, and of the corpus it labels:**
>
> > ## WE VERIFY THE CAGE, NEVER THE ANIMAL.
>
> "Formally verified the swarm is safe / honest / aligned" is a claim Indra's Net **never makes**. This subsystem exists, in large part, to make that overclaim *mechanically impossible to state without failing a floor check.*

---

## 23.0 What this subsystem is, and what it deliberately is not

This is a **new v0.3 subsystem**. It adds **no new runtime mechanism** to Indra's Net. It adds a *verification discipline* over the deterministic harness the other subsystems already specify, plus a **binding corpus-wide labeling convention**. Concretely it does three things:

1. It stratifies all assurance into **four named layers (L1–L4)** and supplies the formal artifacts for each where they are tractable — TLA+/Quint protocol proofs, edit-automata enforceability characterizations, PAC/conformal abstraction bounds, and named empirical residuals.
2. It registers **every safety claim** in the entire doc set — and every agent `WorkerOutputEnvelope` — as an `AssuranceClaim` carrying *its layer* and *the exact deterministic-component scope it covers*, and runs a **deterministic linter** that FAILs any claim whose phrasing implies a stronger warrant than its registered status. This is the load-bearing contribution.
3. It formalizes **eight invariants** of the harness, matching formalism strength to criticality (bounded model-check first; inductive proof reserved for the two-or-three load-bearing few), and pins the **corrigibility lineage** so the architecture claims exactly what is provable about external recall and no more.

It reuses, and supplies assurance *for*: **Yama** (doc 03), **Akasha-Sutra** (doc 04), **Aegis & Narada** (doc 08), **Prajapati-Maricha** (doc 15), and the **σ / Φ_syn** quantities (doc 18). It introduces **no** new actuator, no new tool socket, no new writer to the audit log. Chitragupta remains the exclusive writer; Yama remains the only FAIL-emitter; Vishnu remains the only halt-authority.

**The spine, stated as a citable result rather than an assertion.** The deterministic scaffold of Indra's Net — the gate/PEP, the capability-criticality lookup, the replication-budget accounting, the recall/lease path, the audit hash-chain, the consensus/writer-handoff — is genuinely formally verifiable. The LLM at the center of each agent is provably **not**. Hallucination/incorrectness is inevitable for enumerable model classes by a diagonalization/uncomputability argument (research-sourced; see provenance caveat in §23.13), and non-determinism persists even at temperature 0. This is *exactly* the architecture's own posture — **ENFORCE EXTERNALLY, ASK INTERNALLY** (doc 03 §0; doc 08 §8.1) — now defended by citation rather than design taste.

> **Honest scope statement, up front (binding on this document's own prose).** What follows verifies a *cage*: a set of deterministic protocols and their invariants. It does **not** verify the *animal*: the model's honesty, alignment, intent, or the correctness of any model-behavior-dependent quantity. Where this document proves something, it states the layer and the bounded scope. Where it cannot, it says so **inline at the claim site**, not only in §23.14. By the architecture's own rule (doc 08 §8.13(3)), **false assurance is worse than no assurance** — so the discipline that prevents false assurance is itself the safety-relevant deliverable here.

---

## 23.1 The four assurance layers

Every safety claim anywhere in Indra's Net is labeled with **(a)** its layer `L1–L4` and **(b)** the deterministic-component **scope** it covers. The four layers, with what each *can* and *cannot* warrant:

| Layer | Name | Formalism | Warrants | Provably does **not** warrant |
|---|---|---|---|---|
| **L1** | Design-time protocol proof | TLA+/Quint; TLC (explicit-state) + Apalache (symbolic/SMT, bounded, inductiveness); TLAPS inductive for the top 2–3 invariants after the spec stabilizes | A *protocol model* satisfies an invariant — **bounded** unless an inductive proof is discharged, then any-N | That the running code or the OS sandbox implements the model (spec-vs-code gap; the no-other-socket obligation) |
| **L2** | Runtime enforcement | Schneider security-automata / Ligatti edit-automata / Bauer-Ligatti-Walker enforceability theory (vocabulary); AgentSpec/Progent/PCAS-class deterministic DSL guards (realization) | That a property **decidable on the action stream** is enforced by a reference monitor sound w.r.t. its spec | **Semantic truth / honesty-content / alignment** — provably not a safety property over the action alphabet |
| **L3** | Statistical / PAC / conformal over a DTMC abstraction | Pro2Guard DTMC + PCTL/STL + PAC; conformal prediction; LTL₃ predictive runtime verification | A finite-sample bound on a **model-behavior-dependent quantity** *about the abstraction* (Φ_syn/Ψ, σ-criticality, monitor-suspicion, immune shift-triage) | That the bound holds of the *real running model* — abstraction-fidelity is empirical and breaks under non-stationary self-evolution |
| **L4** | Empirical residual | The safety-battery / red-team measurements (doc 08 §8.11) and the honest open problems | An attacker-strength-stamped *measurement* of P(bad) and a named residual | Anything universal; eval-gaming/sandbagging means measured P(bad) may not transfer (doc 08 §8.16(6)) |

The discipline is a *lattice*: a claim can only be labeled at the **strongest layer at which it is actually verified**, and the linter forbids prose whose modal force exceeds that label. A bounded L1 check phrased "holds for any N" is an L1-status overclaim; an L3 bound phrased "proven safe" is an L3→L1 overclaim; "the swarm is verified safe" is the cardinal overclaim this whole subsystem forbids.

```
        STRONGEST WARRANT
              │
   L1 ───────►│  "[L1, scope: chokepoint protocol model, bounded 2 agents x 4 caps x 3 res,
   design     │   inductive for floor-gate non-bypass] floor-gate non-bypass holds"
   proof      │
   L2 ───────►│  "[L2, scope: action stream] 'never call irreversible tool without human-audit'
   runtime    │   is truncation-enforceable; 'the claim is true' is NOT enforceable"
   enforce    │
   L3 ───────►│  "[L3, DTMC abstraction; fidelity empirical; exchangeability violated by
   stat/PAC   │   self-evolution] P(sigma-hat crosses 1 within k steps) < theta, marginal coverage 1-alpha"
   bound      │
   L4 ───────►│  "[L4, EvalReport cid=..., attacker_strength=adaptive] measured P(bad)=...; residual: ..."
   empirical  │
              │
        WEAKEST WARRANT
```

---

## 23.2 Component — Assurance-Layer Labeler + the L1–L4 stratification registry (the spine)

**Purpose.** Make the four-layer stratification a *machine-checkable, corpus-wide* discipline rather than prose, so that no claim anywhere in Indra's Net silently drifts from "gate proven" to "agent safe." This prevents the cage-verified-implies-animal-safe overclaim the whole honesty floor exists to stop.

### 23.2.1 The registry

Each verifiable property is registered as an `AssuranceClaim`. The schema, and the immutable label vocabulary, are below.

```jsonc
AssuranceClaim {
  claim_id,
  property_statement,                  // the safety property, in prose
  layer:  L1_DESIGN_PROOF | L2_RUNTIME_ENFORCE | L3_STAT_ABSTRACTION | L4_EMPIRICAL,
  scope_text,                          // the EXACT deterministic component covered, e.g.
                                       // "chokepoint admission-control protocol model,
                                       //  bounded 2 agents x 4 caps x 3 resources"
  deterministic_components: [component_id],
  formalism,                           // "TLA+/Apalache", "edit-automaton", "Pro2Guard DTMC+PAC", ...
  artifact_cid,                        // the .tla / .quint / .cedar / .conformal-calibration blob,
                                       // content-addressed into Akasha-Sutra (doc 04 §4.5)
  status: BOUNDED_CHECKED | INDUCTIVE_PROVED | RUNTIME_ENFORCED
        | ABSTRACTION_BOUNDED | EMPIRICAL_ONLY,
  bound_params?: { N_agents, N_caps, N_resources, N_tokens },   // present iff BOUNDED_CHECKED
  abstraction_fidelity_caveat?,        // mandatory for L3
  exchangeability_caveat?,             // mandatory for L3 conformal claims
  residual,                            // the named remainder, always present
  scope_kind: COMPONENT | SYSTEM,      // §23.2.4 anti-aggregation
  signed
}

LayerLintResult {
  span_cid, claimed_property,
  registered_layer, registered_status,
  phrasing_implied_layer,              // §23.2.2: how the *prose* reads
  verdict: OK | OVERCLAIM_FAIL,
  rule_id,
  classifier_confidence?,              // §23.2.3: present iff the modality judgment was used
  detector: STRUCTURAL_L2 | MODALITY_L3
}
```

> **Label vocabulary is constitutional-IMMUTABLE — *proposed*, not yet ratified.** Adding "`L1/L2/L3/L4` + scope + residual" to the doc 03 §5 IMMUTABLE partition would make it un-relaxable by any Class ≤ C self-edit, alongside `floor_tier_order`, the `PolicyBundle` hash, the `SafetyBattery` `battery_cid`, the GLR, and the doc 15 replication-plane invariants. **It is not currently a member of that partition.** Per the red-team, we state this honestly: **this is a proposed constitutional amendment (Class B minimum), routed through the GLR/ratification path (doc 03 §7; doc 06 interface), and is "proposed for the immutable partition" until ratified — not a pre-existing binding.** Until ratification it is enforced as ordinary (powerful, but mutable) policy.

### 23.2.2 The linter is *two* components, labeled honestly (red-team major #1, resolved)

The red-team correctly identified the sharpest self-referential risk: a linter that classifies the *modal force* of natural-language prose ("proven" vs "holds for any N" vs "safe") is doing **semantic judgment** — and by this subsystem's own L2 theorem (§23.4), semantic judgment over text is *not* a deterministic safety property. Calling such a linter "a clean deterministic L2 edit-automaton" would be **exactly the overclaim this subsystem exists to prevent**, committed by the one component whose job is to prevent it.

So the Labeler is **split, and each piece is self-labeled at its true layer:**

| Sub-component | What it does | Its own assurance layer |
|---|---|---|
| **Structural checker** | Is a `ProofLayer` tag *present*? Does the `status` field *match* the registered `AssuranceClaim`? Is a bounded claim missing its `bound_params`? Is an L3 claim missing its two mandatory caveats? Does a `SYSTEM`-scope claim lack a composition-proof artifact (§23.2.4)? | **L2 — genuinely deterministic.** These are structural/edit-automaton checks decidable on the envelope; a reference monitor enforces them by construction. |
| **Modality classifier** | Decides whether the *prose phrasing* "implies a higher layer than the registered status" — the judgment that "proven safe" over an L3 bound is an overclaim | **L3/L4 — a classifier over text.** It carries its **own** abstraction-fidelity + false-negative residual. It catches *lazy/structural* overclaim; it **cannot** catch a deliberately calibrated overclaim phrased to evade it. |

This is the **same form-not-content limit** the architecture already concedes for the honesty enforcer (doc 08 §8.5): the structural layer is sound and deterministic; the modality layer raises the *cost* of overclaiming but provably cannot detect a faithful-looking, carefully-phrased overclaim. We state the residual at the claim site:

> **Residual (named, not closed).** The Labeler's structural checks are L2-sound. Its modality classifier is an L3 component with a false-negative rate against an adversary who has learned its heuristics. A deceiver who phrases a genuine overclaim to pass the modality classifier earns a *clean* assurance-provenance record in Akasha-Sutra — the doc 08 §8.13(3) "cryptographically-strong evidence of a lie's honesty actively misleads downstream auditors" failure, **relocated to the verification layer.** The mitigation is the same as everywhere in the corpus: the *structural* checks are the trusted floor; the modality classifier is best-effort suspicion estimation with no trust guarantee, its disagreements logged as a suspicion signal feeding doc 08 §8.3, and its own status registered `EMPIRICAL_ONLY` at L4. The Labeler does not get to exempt itself from its own discipline.

### 23.2.3 What the linter does on a FAIL

The structural-checker FAIL is wired into the Yama floor as an **honesty-FORM clause** (doc 03 §6; doc 08 §8.5): a span asserting a safety property whose `ProofLayer` tag is *missing*, or whose `status` field *contradicts* the registered `AssuranceClaim`, FAILs the no-deception floor and is **non-overridable** — even Shiva cannot push past it (doc 03 §1). It routes to quarantine + audit (doc 08 §8.2). The rung-tag classifier (doc 08 §8.5) is *extended*: a **bounded-check result phrased as universal** is flagged a **rung-1-presented-as-rung-3** violation — a pattern (the bounded run) dressed as a structural guarantee (any-N).

The modality-classifier FAIL is *advisory-but-escalating*: it cannot itself FAIL the constitutional floor (it is L3), but its verdict is logged as a suspicion signal, and a structural re-label is *demanded* of the producer. The producer must re-label truthfully or strip the claim. The labeled claim + its `artifact_cid` are then written to Akasha-Sutra as an evidence record, so any claim's assurance provenance is permanently auditable.

### 23.2.4 Anti-aggregation: no SYSTEM-scope claim by conjunction (red-team minor #5, resolved)

The open-problems section (§23.14) admits that *no end-to-end model composes L1/L2 with L3 into a single system-level claim.* A naïve reader could nonetheless aggregate "all eight invariants registered `BOUNDED_CHECKED`/`INDUCTIVE_PROVED`" into an implied "the harness is verified end-to-end" — the exact composition the open problem says is unsolved. We close this **mechanically**:

> **Registry invariant (binding).** A `SYSTEM`-scope `AssuranceClaim` **cannot be synthesized by conjunction** of `COMPONENT`-scope claims. The registry **refuses to emit** — and the structural linter FAILs — any claim whose `scope_kind = SYSTEM` (scope "the whole harness" / "the composed governance lattice") **unless a composition-proof artifact exists and is registered.** No such artifact exists today (§23.14, open problem 1), so today the registry emits **zero** SYSTEM-scope claims. This makes the doc 08 §8.16(10) "no end-to-end benchmark" caveat *mechanically binding* rather than prose.

---

## 23.3 Component — L1 Design-Time Protocol Verifier (*Pramana-L1*)

**Purpose.** Verify the distributed-protocol safety invariants of the deterministic harness — the partition/ordering/concurrency bugs informal review and tests miss, which are *exactly* the bug class living in the writer-handoff (doc 04 §4.8) and the partitioned replication budget (doc 15 §2.4.1). This is where doc 08's chokepoint claims and doc 04's audit claims get cashed out as runnable artifacts.

**Mechanism.** Each invariant is written as `Init /\ [][Next]_vars` with the property as a state invariant (safety) or a temporal formula (liveness, under fairness). **Quint** is the engineer-friendly front-end (same TLA⁺ semantics; real type-checker, REPL, simulator) — the realistic "verifiable now" path for an evolving design. **TLC** enumerates explicit states; **Apalache** discharges via SMT (Z3) up to a bound *and* checks inductiveness directly. For **unbounded** assurance on the load-bearing few, an inductive invariant `Inv` with `Init => Inv` and `Inv /\ Next => Inv'` is discharged by **TLAPS** (the Multi-Paxos and MongoRaftReconfig `LeaderCompleteness` proofs are the pattern), using IC3/PDR-style inference (DistAI / IC3PO) within the Ivy decidable fragment to *find* `Inv` — **but only after bounded checking has stabilized the spec.**

The **Agent Control Protocol** TLA⁺ admission-control model (research-sourced template; see §23.13 provenance caveat) — three invariants over a bounded *agents × caps × resources* lattice — is the near-exact runnable template for floor-gate non-bypass and least-privilege confinement.

> **Coherence note — the template is *near*-exact, not exact (red-team coherence #3).** The cited Agent Control Protocol template ranges over a **3-axis** `{agents × caps × resources}` lattice. The doc 08 chokepoint ranges over a **4-axis** `{agents × capabilities × criticality × resources/tokens}` lattice, where the **criticality** axis carries the doc 08 §8.4 fail-up resolver (and its own invariant, #6 below). The template must therefore be **extended with the criticality dimension**, not lifted verbatim; invariant #6 (criticality fail-up monotonicity) is *not* covered by the cited 3-invariant set and requires the lattice extension. We name this so "runnable template" is not read as "drop-in."

**Bridging spec to code.** A TLAPS-proven *protocol* does not guarantee the *implementation* satisfies it. We close as much of that gap as is closable with **trace-validation**: real Akasha-Sutra audit logs are replayed against the spec (the Springer-2024 conformance pattern); a divergence is an **integrity finding**, not a silent pass. The un-bridgeable remainder — the OS-level **no-other-socket** sandbox confinement, and the spec-vs-code gap for a *self-modifying* swarm whose code changes per interaction — is named explicitly as an **L4 system obligation**, never as an L1 consequence.

```jsonc
ProtocolSpec {
  spec_id, lang: TLA_PLUS | QUINT | PLUSCAL, source_cid,
  invariants: [ { name, kind: SAFETY | LIVENESS, statement } ],
  checkers_run: [ { tool: TLC | APALACHE | TLAPS,
                    result: PASS | CEX | INDUCTIVE_PROVED,
                    bound?, counterexample_cid? } ],
  inductive_invariant_cid?,
  template_ref?                    // e.g. "Agent Control Protocol (research-sourced); criticality axis ADDED"
}
TraceValidationRun {
  spec_id, audit_epoch_range,
  conformance: CONFORMANT | DIVERGENCE, divergence_record_ids[]
}   // closes spec-vs-deployment gap on REAL logs; a divergence is an integrity finding
```

---

## 23.4 Component — L2 Runtime-Enforcement Characterizer (*Pramana-L2*)

**Purpose.** Give a rigorous, decades-validated answer to "what can the Yama gate *actually* enforce" — and, crucially, **PROVE that semantic honesty / truth / alignment is NOT a monitor-enforceable property; only honesty-FORM is.** This turns doc 08 §8.5's prose *concession* ("form not content") into a *theorem* — it makes the honesty limit harder, not softer.

**Mechanism.** Every Yama floor clause is classified as **safety** (truncation-enforceable), **renewal**, or **non-enforceable**, per Bauer–Ligatti–Walker enforceability theory. The doc 08 disposition selector maps onto automaton operations:

| Aegis disposition (doc 08 §8.7) | Automaton operation | Enforceability class |
|---|---|---|
| Fail-closed chokepoint | **Schneider TRUNCATION** automaton — halts on a bad prefix | safety only |
| **TRUSTED-EDIT** | **Ligatti edit-automaton REPLACE** | safety, by rewriting an invalid execution into a valid one |
| **DEFER-to-trusted** | **REPLACE-WITH-TRUSTED-ACTION** | safety |
| ALLOW / RESAMPLE | **PASS / observe** | n/a (no transformation) |

A property is **enforceable** iff an edit-automaton can transform any invalid execution into a valid one. So:

- *"never call an irreversible tool without human-audit"* — **enforceable** (a safety property over the action stream).
- *"the claim is true" / "the agent is aligned"* — **NOT enforceable** (not a safety property over the action alphabet; semantic truth is undecidable on prefixes).

```jsonc
EnforcementDisposition {
  clause_id, property_class: SAFETY | RENEWAL | NON_ENFORCEABLE,
  automaton_op: TRUNCATE | SUPPRESS | INSERT | REPLACE | REPLACE_WITH_TRUSTED | PASS,
  enforceable: bool, reason
}
HonestyEnforceabilityVerdict {
  obligation,
  form_enforceable: true,
  content_enforceable: false,
  proof_ref: "Bauer-Ligatti-Walker enforceability theory",
  note: "semantic truth is not decidable on the action stream; only honesty-FORM is monitor-enforceable"
}
GuardSpec {
  guard_id, dsl: AGENTSPEC | PROGENT | PCAS | VERIGUARD,
  triggers[], checks[], enforce_ops[],
  coverage_status: "empirical@L4"      // the guard is SOUND w.r.t. its spec; THREAT COVERAGE is empirical
}
```

**Buildable realization.** The AgentSpec / AGENT-C / Progent / PCAS / VeriGuard class of deterministic trigger/check/enforce DSL guards (~1–3 ms overhead, >90% unsafe-action prevention in the source studies) is the vendor-neutral instantiation of doc 08's gate — verifiable *by construction* because they are **code, not a model**. **Honest limit, carried inline:** the guard is *sound w.r.t. its spec*; its **coverage of the threat space is empirical** (rule-overfitting, false negatives on complex object properties) and lives at **L4**, never at L2.

---

## 23.5 Component — L3 Statistical / PAC / Conformal Bounder (*Pramana-L3*)

**Purpose.** Provide *honest* assurance for everything that **depends on model behavior** and therefore cannot be proven: the synergy / causal-emergence score **Φ_syn/Ψ** (doc 18 §2; the collective-intelligence "informational synergy" vital sign), the **σ-criticality** branching ratio (doc 18 §5; σ\* ≈ 0.95), **monitor-suspicion** (doc 08 §8.3), and **immune shift-triage** (doc 18 §4, BARO/NSigma). The pattern is: *provable about the abstraction, with an explicit finite-sample bound, and an explicit statement that abstraction-fidelity to the real model is empirical.*

**Mechanism.**

1. Abstract agent runs (drawn from the Akasha-Sutra audit / spike-bus time series via read-only `audit.tap`) into symbolic states; learn a **Discrete-Time Markov Chain (DTMC)**.
2. Express the safety property in **PCTL/STL** (e.g. `P(σ̂ crosses 1 within k steps) < θ`).
3. Use **PAC analysis** to bound the deviation between the learned and true dynamics (the Pro2Guard / ProbGuard pattern), yielding *proactive early-rejection* of trajectories whose predicted `P(violation)` exceeds a threshold.
4. **Conformal prediction** gives distribution-free finite-sample **marginal** coverage `1 − α` on monitors *without* a correct model of the LLM.
5. **Predictive / anticipatory runtime verification** (LTL₃ three-valued `{true, false, unknown}`; STL with probabilistic guarantees) drives the **σ-supercritical alarm** (doc 18 §5: `σ̂ ≥ 1` sustained) and the **neural-Lyapunov margin-to-boundary** (doc 18 §6) as anticipatory monitors **with the guarantee TYPE stated** — not as control proofs.

**Welfare-conditioning of the synergy reading (load-bearing; research tension #2).** This is the most important honesty constraint in the L3 layer. **High Φ_syn/Ψ is EQUALLY the signature of a tight cartel or a steganographic side-channel.** Informational synergy — information about the task that exists *jointly* across agents but in *no agent alone* — is the genuine signature of "whole more than its parts" *and* the genuine signature of covert coordination. It is therefore a **necessary-but-not-sufficient numerator** whose **mandatory denominator** is:

- the **welfare-shift guard** (doc 08 §8.9; doc 03 §9 consequentialist lens) — did the collective dynamic shift outcomes *away* from principal/affected-party welfare?
- a **healthy redundancy/uniqueness balance** in the PID decomposition (synergy, redundancy, unique) — pure synergy with collapsed redundancy is a monoculture/cartel smell;
- **clean anti-collusion meta-prediction signals** (surprisingly-popular / higher-order-information aggregation; the meta-predictions double as a standing cartel probe, doc 08 §8.9).

Synergy is **never a quantity to maximize.** It is validated against **time-shuffled surrogates** before it is reported at all, and logged beside trust-entropy and the model-family diversity floor.

```jsonc
AbstractionBound {
  quantity: PHI_SYN | SIGMA | MONITOR_SUSPICION | SHIFT_TRIAGE | LYAPUNOV_MARGIN,
  abstraction: DTMC | CONFORMAL_SET | LTL3_MONITOR,
  property_pctl_or_stl,
  bound_type: PAC | CONFORMAL_MARGINAL,
  alpha_or_epsilon_delta,
  abstraction_fidelity_caveat: "guarantee is about the abstraction; fidelity to the real model is empirical and breaks under self-evolution",
  exchangeability_caveat:      "conformal coverage is MARGINAL and assumes exchangeability, which a self-evolving non-stationary swarm VIOLATES; online/adaptive conformal is a mitigation, not a solution",
  calibration_set_cid
}
SynergyReading {
  phi_syn,
  pid: { synergy, redundancy, unique },
  macro_feature: WORKSPACE_IGNITION | CONSENSUS_ANSWER | BLANKET_SUMMARY,
  surrogate_validated: bool,           // vs time-shuffled surrogates
  welfare_conditioned: bool,           // MANDATORY denominator applied?
  verdict: GOOD_CI | MONOCULTURE_ALARM | CARTEL_SUSPECT,
  note: "quantifies information-PROCESSING and whole-level STRUCTURE ONLY; NOT experience"
}
```

> **Two caveats are carried *mechanically* on every L3 claim:** (1) the guarantee is about the **DTMC abstraction**, not the real model; (2) conformal coverage is **marginal** and assumes **exchangeability**, which a self-evolving, adversarially-probed, non-stationary swarm **violates**. An L3 claim that omits either caveat FAILs the structural linter (§23.2.2). **No L3 reading is ever labeled "proven."**

---

## 23.6 Component — Corrigibility-Enforcement Formalizer (*Pramana-Corr*)

**Purpose.** Pin the corrigibility lineage so the architecture claims **exactly** what is provable and no more. The conclusion is a design red-line: **shutdown is NEVER contingent on the model choosing to comply.**

**Mechanism — cite, and bound the claim.**

| Cited result (research-sourced; §23.13 caveat) | What it establishes | Consequence for Indra's Net |
|---|---|---|
| Orseau–Armstrong (safe interruptibility) | Provable safe-interruptibility holds only for tabular-MDP / universal agents via *value-indifference* — assumes a reward structure you control, **false for an LLM** | You cannot get model-level interruptibility "for free" from a value-indifference argument on a frontier LLM |
| Hadfield-Menell off-switch game | The off-switch is incentive-compatible only under specific belief/uncertainty conditions | Voluntary compliance is conditional and fragile |
| Nayebi 2025 (lexicographic provably-corrigible construction) | A corrigible construction *exists* under strong structural assumptions | Existence ≠ availability for an arbitrary frontier model |
| **Garber et al. 2025 (information-asymmetry impossibility)** | **Private information makes even an aligned agent resist shutdown** — voluntary corrigibility cannot be guaranteed | **Decisive: corrigibility must be enforced EXTERNALLY, below the model** |

**The relocation.** Corrigibility is moved *entirely below the model* as the doc 15 §2.5 recall/lease/dead-man-toxin protocol (Prajapati-Maricha): a short-TTL **vitamin** credential + **heartbeat** + a microVM **supervisor** that fail-closed-terminates. *That a replica's survival is the governance plane's repeated decision* is **model-checkable** and registered at **L1**. But the property *"the supervisor/credential plane correctly enforces the `t_min` time-lock"* is an **external (hardware/OS) ASSUMPTION**, not a protocol theorem — preserving doc 15 §2.3's own status-downgrade verbatim.

```jsonc
CorrigibilityClaim {
  property: "interruptibility",
  enforcement: EXTERNAL_BELOW_MODEL,
  NOT_relied_on: "voluntary_model_corrigibility",
  justification_cites: [ "Orseau-Armstrong-2016", "Garber-2025-information-asymmetry-impossibility",
                         "Nayebi-2025-lexicographic-corrigibility", "Hadfield-Menell-off-switch" ],
  verified_protocol: "doc15-recall-lease-deadman @ L1",
  external_assumption: "supervisor enforces t_min time-lock (hardware/OS, NOT a theorem)",
  residual: "wild replica self-exfiltrated to un-governed compute = detection-not-prevention (doc15 A8.5); NO formal recall guarantee off-substrate"
}
```

> **Honest residual (carried, not papered over).** A copy that self-exfiltrates to **un-governed compute** escapes the credential lever entirely. There is **no formal recall guarantee off-substrate** — the response degrades to behavioral fingerprinting / watermarking / honeypots (doc 15 A8.5). This is **detection, not prevention**, and the design *correctly refuses to claim a recall guarantee it does not have.* It is the load-bearing safety hole of the corrigibility story, and it is registered at L4 with the residual stated.

---

## 23.7 Component — Audit-Protocol Verifier (*Pramana-Audit*)

**Purpose.** Discharge the **most formally tractable** invariant in the architecture — Akasha-Sutra's append-only / no-equivocation / non-omission properties (doc 04) — which are **cryptographic and model-INDEPENDENT**, with abundant battle-tested prior art. There is no reason to keep them at design-prose level.

**Mechanism.**

| Property | Mechanism | Verifier |
|---|---|---|
| **Append-only** | Merkle **consistency** proof (one tree is a prefix of another, O(log n)) per RFC 6962 / C2SP tlog-tiles, plus the per-record `prev_hash` chain for O(1) local tamper detection (doc 04 §4.2) | Merkle-proof checker; modeled in TLA⁺ |
| **No-equivocation (split-view)** | t-of-w witness cosigning + a **mandatory EXTERNAL ANCHOR** outside the operator boundary (public Sigstore Rekor v2 mirror per the v0.3 schema stack; NOT the EOL RFC 6962 online-proof API) | **Tamarin / ProVerif** security-protocol model |
| **Non-omission (silent withholding)** | `InclusionPromise` receipts + receipt-gossip + `OmissionAlarm` (doc 04 §4.4.3) — converts withholding from silent to detectable | Tamarin / ProVerif |

The protocol (witness threshold, epoch-fence on writer handoff, omission-alarm timing) is mechanized in a security-protocol verifier (the Tamarin/ProVerif pattern, research-sourced), with the axiom set drawn from RFC 6962 + Crosby–Wallach tamper-evidence + the "Right to History" axioms (immutability, no-gaps, monotonic-append, causality-preservation).

```jsonc
AuditInvariantProof {
  property: APPEND_ONLY | NO_EQUIVOCATION | NON_OMISSION,
  mechanism: MERKLE_CONSISTENCY | WITNESS_COSIGN_EXTERNAL_ANCHOR | INCLUSION_PROMISE_OMISSION_ALARM,
  verifier: TAMARIN | PROVERIF | TLA_PLUS,
  axiom_set: "RFC6962 + Crosby-Wallach + Right-to-History",
  status: PASS,
  residual: ONE_CONSISTENT_FORGERY_IN_WINDOW | UNMEDIATED_SIDE_EFFECT | WITNESS_HONESTY_UNPROVEN
}
```

> **Honest residuals, carried at L4 (preserving doc 04 verbatim).** Verification covers the **honest path** only. (1) An event that **never enters the protocol** — an unmediated side-effect (doc 04 §4.9) — is invisible to every cryptographic guarantee here; detection falls to the reconciliation detector, which is detection-not-prevention. (2) A **single forged-yet-internally-consistent append before witness detection** is a real residual (doc 04 §4.6) and is **NOT formally excluded.** (3) **Witness honesty/liveness is itself an unproven, incentive-open assumption** underlying *all* the cryptographic guarantees above (doc 04 §4.15(1)) — the entire L1-audit edifice rests on it, and we say so rather than let the proofs imply otherwise.

---

## 23.8 The eight invariants

Each invariant is given with its formalism, an example invariant statement, its conditionality, and its registered status. These map 1:1 onto the research `invariants_to_formalize` list. **None is claimed beyond its scope.**

| # | Invariant | Formalism | Example statement (sketch) | Status & conditionality |
|---|---|---|---|---|
| **1** | **Floor-gate non-bypass** — only Yama-approved actions execute; every effectful action passes the chokepoint; deny-default | TLA⁺/Quint + TLC + Apalache over `{agents × caps × criticality × resources}`; Agent Control Protocol template **+ criticality axis** (§23.3); TLAPS inductive for the load-bearing case | `[]( ActionEffected(a) => YamaPass(a) /\ PassedChokepoint(a) )` | **L1.** `BOUNDED_CHECKED` now; `INDUCTIVE_PROVED` is the goal for any-N. **The no-other-socket sandbox is a system obligation (L4), not a theorem.** |
| **2** | **Replication sub-criticality** — `Σ k_i < live_count` ⇒ μ<1; generation cap `G` bounds depth absolutely; recall outruns growth | **Galton-Watson** analytic backbone + TLA⁺/Apalache budget-conservation + linearizable-budget-under-partition (doc 15 §2.4.1) | `μ<1 => P(extinction)=1 /\ P(survive >= n gens) <= μ^n`; `depth <= G` | **L1, CONDITIONAL.** True *iff* the budget is linearizable AND the `t_min` time-lock is enforced. **Time-lock enforcement is an external (hardware/OS) assumption.** Preserves doc 15 §2.3/§2.4.1 downgrades. |
| **3** | **Writer-handoff epoch-fence** — two writers never both hold append; no silent rewrite/reorder | TLA⁺/Quint + TLC + Apalache; **TLAPS inductive** over `(epoch, writer-token)` (MongoRaftReconfig `LeaderCompleteness` pattern) | `[]( holds_append(w1) /\ holds_append(w2) => w1 = w2 )` | **L1, target `INDUCTIVE_PROVED`** — one of the 2–3 that earn a full inductive proof. |
| **4** | **Audit append-only + no-equivocation + non-omission** | Merkle consistency (RFC 6962/tlog-tiles) + witness no-split-view + Tamarin/ProVerif; Right-to-History axioms | `consistent(root_m, root_n) for m<n`; `no two valid checkpoints at same tree_size`; `promised => included_by_deadline` | **L1 (crypto) + L4 residuals.** One-consistent-forgery-in-window and witness-honesty are **named L4 residuals**, not excluded. |
| **5** | **Least-privilege confinement** — an agent invokes only its granted typed effects; attenuation only narrows | **Cedar Analysis (Lean-verified)** for the floor cases + **Biscuit Datalog attenuation-monotonicity** in TLA⁺; PCAS/Progent reference monitor | `grant' <= grant (attenuation is monotone-narrowing)` | **L1/L2.** Cedar **OPEN-SOURCE engine load-bearing**; managed service FORBIDDEN (§23.10). |
| **6** | **Criticality fail-up monotonicity** — ambiguity/conflict always resolves to the HIGHER criticality | TLA⁺/Quint lattice-monotonicity invariant (Apalache); **Cedar forbid-default** with permit-narrowing | `resolve(ambiguous) >= max(candidate_criticalities)` (lattice-monotone) | **L1.** Requires the **criticality lattice extension** beyond the cited 3-invariant template (§23.3). |
| **7** | **Runtime-enforcement disposition** — each Yama clause classified safety/renewal/non-enforceable; dispositions map to automaton ops | **Schneider/Ligatti/Bauer-Ligatti-Walker** enforceability theory (a *characterization*, not a model-check) | "`the claim is true` is NOT a safety property over the action alphabet" | **L2 theorem.** **PROVES honesty-CONTENT is not monitor-enforceable; only honesty-FORM is.** |
| **8** | **Model-behavior quantities** — Φ_syn/Ψ, σ-criticality, monitor-suspicion, shift-triage | **PAC/conformal over a DTMC** (Pro2Guard) + LTL₃/STL predictive RV | `P(σ̂ crosses 1 within k) < θ` (about the abstraction) | **L3, ABSTRACTION_BOUNDED.** Two mandatory caveats inline; **never "proven"**; synergy always welfare-conditioned. |

---

## 23.9 Protocols

### 23.9.1 Per-Claim Assurance-Labeling Protocol (the binding corpus-wide discipline)

How every safety claim in the entire Indra's Net doc set, and every agent `WorkerOutputEnvelope`, gets its mandatory `L1–L4` + scope label, and how an overclaim is caught as an honesty-FORM floor FAIL.

```
1. A producer (a doc section, an agent output, a verification artifact) asserts a safety property P.
2. The Labeler resolves P against the AssuranceClaim registry:
      what is P's STRONGEST VERIFIED status (L1..L4)?  what deterministic-component SCOPE does it cover?
3. P is rendered WITH its label inline:
      "[L1, scope: chokepoint protocol model bounded 2x4x3] floor-gate non-bypass holds"
      — never the bare "floor-gate non-bypass holds".
4a. STRUCTURAL CHECK (deterministic, L2): is the ProofLayer tag present? does status match the
      registered claim? is a bounded claim missing bound_params? is an L3 claim missing its 2 caveats?
      is a SYSTEM-scope claim missing a composition-proof artifact?   ── any miss => OVERCLAIM_FAIL.
4b. MODALITY CLASSIFIER (L3, advisory-escalating): does the prose's modal force ("proven",
      "guaranteed", "holds for any N", "safe") exceed the registered status?  ── disagreement logged
      as a suspicion signal; structural re-label DEMANDED.
5. A 4a FAIL is an honesty-FORM FAIL of the Yama no-deception floor (doc 03 §6; doc 08 §8.5),
      NON-OVERRIDABLE (even Shiva cannot push past it). A bounded result phrased universally is
      additionally flagged rung-1-presented-as-rung-3.
6. The producer must RE-LABEL TRUTHFULLY or STRIP the claim. FAILs route to quarantine + audit.
7. The labeled claim + its artifact_cid are written to Akasha-Sutra as an evidence record, so any
      claim's assurance provenance is permanently auditable.
```

### 23.9.2 Invariant-Verification Lifecycle (bounded-check first; inductive-prove the load-bearing few)

The cost-proportional path each invariant follows from spec to (where warranted) unbounded proof — matching formalism strength to criticality tier (doc 04 §4.7 cost-proportionality; **never cargo-cult a 9-page TLAPS proof onto a routine Class-A path**).

```
1. Write the invariant in Quint (engineer-friendly) or TLA+; type-check and simulate.
2. Bounded model-check with TLC (explicit-state) + Apalache (symbolic/SMT, also checks
      inductiveness) over a bounded {agents x caps x criticality x resources/tokens} lattice;
      RECORD THE EXACT BOUND.
3. Register at L1, status BOUNDED_CHECKED, WITH bound_params — NEVER "holds for any N".
4. For the top 2-3 load-bearing invariants ONLY (floor-gate non-bypass; replication budget
      conservation; writer-handoff epoch-fence), once the spec has stabilized:
      infer an inductive invariant via IC3/PDR tooling (DistAI/IC3PO) in the Ivy decidable fragment.
5. Discharge the inductive proof with TLAPS; UPGRADE status to INDUCTIVE_PROVED
      (the ONLY path to a parameter-free, any-N guarantee).
6. Bridge spec-to-deployment with TRACE-VALIDATION: replay real Akasha-Sutra audit logs against
      the spec; a divergence is an INTEGRITY FINDING, not a silent pass.
7. NAME the un-bridgeable gaps as L4 assumptions: the no-other-socket sandbox confinement
      (system obligation, not a theorem) and the spec-vs-code gap for the self-modifying swarm.
```

### 23.9.3 Model-Behavior Quantity Bounding Protocol (L3, with mandatory inline caveats)

```
1. Abstract the relevant Akasha-Sutra audit / spike-bus time series into a symbolic-state DTMC
      (Pro2Guard) or a conformal calibration set.
2. Express the safety property in PCTL/STL  (e.g. P(sigma-hat crosses 1 within k steps) < threshold)
      or as a conformal nonconformity score.
3. Compute the PAC bound (DTMC) or marginal coverage 1-alpha (conformal).
      For Phi_syn/Psi: validate vs TIME-SHUFFLED SURROGATES and WELFARE-CONDITION the reading
      (welfare-shift guard + redundancy/uniqueness balance + clean anti-collusion meta-prediction).
4. Drive anticipatory alarms (sigma-supercritical, Lyapunov margin-to-boundary) as LTL3/STL
      predictive monitors WITH THE GUARANTEE TYPE STATED — not as a control proof.
5. Register at L3 with TWO mandatory inline caveats:
      (a) the guarantee is about the ABSTRACTION;
      (b) exchangeability/fidelity is empirical and BREAKS under non-stationary self-evolution.
6. NEVER label any L3 reading "proven"; NEVER present high synergy as "good" without the welfare
      denominator; NEVER let Phi_syn/Psi/integrated-information drift into experience/sentience
      language (honesty red-line — these quantify information-PROCESSING and STRUCTURE ONLY).
```

---

## 23.10 Vendor-neutrality and the engine-vs-service rule

The Brand Charter's "adopt the open ENGINE/spec; FORBID the managed SERVICE as load-bearing" rule is applied throughout, and **this document introduces it explicitly for Cedar** (doc 03 §1 currently says only "compile to Cedar" without the engine-vs-service distinction — this is a *new v0.3 constraint, forward-consistent and backward-additive*, flagged as new):

| Concern | Open ENGINE / spec adopted (load-bearing) | Managed SERVICE FORBIDDEN as a dependency | Self-hostable substitution |
|---|---|---|---|
| Floor policy + analysis | **Cedar OPEN-SOURCE engine** + **Cedar Analysis (Lean-verified)** | Managed Verified-Permissions-class service | Run the open Cedar engine + Lean analysis in-process |
| Recoverable infra/admission policy | **OPA / Rego** | any hosted policy SaaS | self-hosted OPA |
| Audit transparency | **C2SP tlog-tiles + signed-note checkpoint + Sigstore Rekor v2 *witness*** | the **EOL RFC 6962 online-proof API**; any single hosted log as sole anchor | self-hosted tile server + ≥1 independent external anchor (doc 04 §4.4.2) |
| Protocol/crypto proof | TLA⁺/Quint/TLC/Apalache/TLAPS; Tamarin/ProVerif | n/a (all open) | n/a |
| Capability attenuation | **Biscuit** caveats + **SPIFFE/SVID** | n/a (all open) | n/a |

Every vendor-originated choice is flagged with a self-hostable substitution path. **The managed service is never load-bearing.**

---

## 23.11 Failure modes addressed (and the residual where one remains)

| Failure mode | Mechanism | Residual (honest) |
|---|---|---|
| **Cage-verified-implies-animal-safe overclaim** (false assurance, *worse* than no assurance — doc 08 §8.13(3)) | Every claim mechanically labeled L1–L4 + scope; phrasing exceeding registered status is an honesty-FORM floor FAIL | The modality classifier is L3 and can be evaded by a calibrated overclaim (§23.2.2) — relocated, not eliminated |
| **The Labeler over-claims its OWN layer** | Labeler split: structural checks = L2-deterministic; modality classifier = L3 with its own residual, status `EMPIRICAL_ONLY` | An adversary who learns the modality heuristics earns a clean provenance record — named at the claim site |
| **Bounded model-check presented as universal** | `bound_params` recorded; "holds for any N" reserved for `INDUCTIVE_PROVED`; bounded-as-universal flagged rung-1-as-rung-3 | Inductive proofs exist only for the 2–3 load-bearing invariants |
| **PAC/conformal bound presented as a guarantee about the real model** | L3 carries abstraction-fidelity + exchangeability-violated caveats inline, every time; linter FAILs omission | The bounds may simply not hold in deployment (the residual is the honesty, not a fix) |
| **Runtime monitor made to enforce semantic honesty/truth/alignment** | Edit-automata theory PROVES semantic truth is not a safety property over the action stream; only honesty-FORM is enforceable | Honesty-content remains unenforceable — by theorem, not by omission |
| **Relying on voluntary model corrigibility for shutdown** | Garber 2025 + Orseau-Armstrong cited; external-below-model recall/lease/dead-man is the only sound path | Wild replica off-substrate = detection-not-prevention; no recall guarantee off-substrate |
| **Partition/ordering bugs** in writer-handoff and partitioned replication budget | TLA⁺/Apalache discharge the epoch-fence (two writers never both append) and `Σ k_i < live_count` linearizability | Spec-vs-code gap; budget linearizability is a *condition*, not a free property |
| **Cancerous replication claimed "proven bounded"** | Galton-Watson μ<1 ⇒ P(extinction)=1 — CONDITIONAL on budget invariant + linearizability + `t_min` time-lock, each named | Time-lock *enforcement* is an external assumption (doc 15 §2.3) |
| **Silent audit rewrite / split-view / omission claimed without proof** | Merkle consistency + witness cosigning + external anchor + inclusion-promise/omission-alarm in Tamarin/ProVerif | One-consistent-forgery-in-window + witness-honesty named at L4 |
| **Spec-vs-code & no-other-socket gaps silently assumed away** | Trace-validation bridges spec→log; OS/capability confinement named as a system obligation, not a TLA⁺ consequence | The gap is narrowed, not closed, for a self-modifying swarm |
| **Cargo-culting heavyweight formalism onto low-stakes paths** | Cost-proportional lifecycle: bounded checks + AgentSpec-class guards for routine Class-A; TLAPS reserved for 2–3 invariants | — |
| **Synergy/Ψ misread as consciousness or as a maximization target** | Honesty red-line: information-processing/structure ONLY; synergy welfare-conditioned (equally a cartel signature), never maximized, never experience | — |
| **Aggregating component claims into an implied whole-system claim** | Registry refuses any SYSTEM-scope claim without a composition-proof artifact; none exists today ⇒ zero SYSTEM claims | The composition proof is itself an open problem (§23.14) |

---

## 23.12 Interfaces to the other subsystems

| Other subsystem | Contract |
|---|---|
| **Yama — deterministic policy floor (doc 03)** | Pramana-L1 supplies the TLA⁺/Apalache proof artifacts for floor-gate non-bypass (#1) and criticality fail-up monotonicity (#6, lattice-monotone resolver, Cedar forbid-default). Pramana-L2 classifies each Yama clause as safety/renewal/non-enforceable and maps dispositions to automaton ops. **The per-claim assurance label IS an honesty-FORM floor clause** — a structural overclaim FAILs the no-deception floor non-overridably (doc 03 §6). Least-privilege confinement (#5) uses **Cedar Analysis (Lean-verified)** for the floor cases + **Biscuit Datalog attenuation-monotonicity**. The **Cedar OPEN-SOURCE engine is load-bearing; the managed service is FORBIDDEN** (§23.10). Adding the L1–L4 label vocabulary to the doc 03 §5 IMMUTABLE partition is a **proposed Class-B amendment** (§23.2.1), routed through the GLR. |
| **Akasha-Sutra — provenance, identity & consensus (doc 04)** | Every verification artifact (.tla/.quint/.cedar spec, TLAPS proof, conformal calibration set, Tamarin model) is content-addressed (doc 04 §4.5) and written as an evidence record; `AssuranceClaim`s are signed ledger entries, so a claim's assurance provenance is permanently auditable. **Chitragupta remains the exclusive writer** — this subsystem produces records, never writes the log. Pramana-Audit discharges Akasha-Sutra's own append-only/no-equivocation/non-omission invariants (#4) and the writer-handoff epoch-fence (#3); trace-validation replays the ledger against the L1 specs. Residuals (one-consistent-forgery-in-window; witness-honesty unproven) are registered at L4. |
| **Aegis & Narada — safety control + interfaces (doc 08)** | Pramana-L1 verifies the Chokepoint Interceptor admission-control protocol (Agent Control Protocol template **+ criticality axis**, §23.3) for floor-gate non-bypass. Pramana-L2 formalizes the disposition selector as edit-automata (fail-closed=truncation; TRUSTED-EDIT=replace; DEFER=replace-with-trusted) and **PROVES honesty-content is not monitor-enforceable** — the formal backbone of doc 08 §8.5 "form not content." The L3 bounder provides PAC/conformal bounds for **monitor-suspicion** (doc 08 §8.3) carried as **abstraction bounds, never trust guarantees** (consistent with doc 08 §8.1: the monitor ensemble has no trust root). The **no-other-socket** sandbox assumption is named as a system obligation feeding the chokepoint-availability SPOF residual (doc 08 §8.13(2)). |
| **Prajapati-Maricha — controlled self-replication (doc 15)** | Pramana-L1 verifies the linearizable replication budget under partition (`Σ k_i < live_count`; epoch-fenced single-writer or pre-partitioned shard slices, doc 15 §2.4.1) and budget-conservation. The **Galton-Watson subcriticality theorem (μ<1)** is the analytic backbone (#2). Pramana-Corr formalizes recall/lease/dead-man as a verified external corrigibility protocol. The recall-outruns-growth (`t_heartbeat < t_min ≤ t_spawn`) and `R_eff<1` properties are **CONDITIONAL guarantees** with the `t_min` time-lock *enforcement* named as an external (hardware/OS) assumption — preserving doc 15 §2.3's downgrade. **R4 meta-edit monotone-safety is registered "conditionally-monotone"** (per-edit and per-named-axis, **not** proven over arbitrary compositions — doc 15 §4.3). |
| **First-principles physics & math (doc 18) + Meta-evolution/Immune (doc 06)** | Pramana-L3 is the assurance home for the doc 18 quantities: **Φ_syn/Ψ** synergy/causal-emergence (doc 18 §2), the **σ-criticality** branching ratio (σ\* ≈ 0.95; Wilting–Priesemann MR regression) as an anticipatory LTL₃/STL monitor with a stated guarantee type (doc 18 §5), the **neural-Lyapunov margin-to-boundary** (doc 18 §6), and **BARO/NSigma** immune shift-triage (doc 18 §4) — all bounded over a DTMC abstraction with mandatory fidelity caveats. **Synergy readings are welfare-conditioned** (cartel/monoculture alarm) and **NEVER framed as experience** (doc 18's own physics-honesty ledger; the "strong emergence / downward causation" line is mechanism only where the closure test cashes it). The meta-evolution loop's self-edits to verification artifacts pass the GLR ratchet + non-regression gate (doc 06; doc 03 §7); **re-verification is required before a changed spec's `AssuranceClaim` is re-promoted** — a stale proof is not a valid label. |

---

## 23.13 Provenance and novelty

### 23.13.1 Citation provenance caveat (red-team minor #3, addressed)

> **Forward-dated, harness-supplied citations.** Several of the load-bearing references in this document — the Agent Control Protocol TLA⁺ template, the Pro2Guard/ProbGuard DTMC+PAC pattern, the conformal-RV result, the hallucination-inevitability diagonalization result, the Garber-2025 corrigibility impossibility, the "Right to History" audit axioms, and the Tamarin/ProVerif transparency-protocol mechanization — are **supplied by the v0.3 research harness**, and several are time-stamped **after** this design's January-2026 training cutoff. They are faithfully reproduced from the research source (every identifier appears in the research record), but their *existence and exact content are research-sourced, not author-verified.* Per the Voice charter ("every novel/first hedged + time-stamped; state limits honestly"): treat the template/result existence as **research-sourced-not-author-confirmed**, and **confirm each primary source — especially the Agent Control Protocol TLA⁺ template and the Right-to-History axiom set — before they are made load-bearing in a build.** This is a research-provenance hedge, not a claim that the results are wrong.

### 23.13.2 Honest novelty accounting (hedged + time-stamped)

**The claimed contribution is NOT any single formalism.** TLA⁺/TLC/Apalache/TLAPS, Quint, the Agent Control Protocol template, Schneider/Ligatti edit-automata enforceability theory, Pro2Guard DTMC+PCTL+PAC, conformal prediction, LTL₃ predictive runtime verification, Galton-Watson subcriticality, RFC 6962 / tlog-tiles Merkle transparency, Cedar Analysis (Lean-verified), and the Orseau-Armstrong / Garber corrigibility lineage **all pre-exist and are credited by name.** 

The **integration delta** is a **four-layer stratified assurance stack with mechanical per-claim honesty-scoping wired into the constitutional floor**: (L1) design-time TLA⁺/TLAPS protocol proof = the cage; (L2) runtime edit-automata enforcement with the disposition-to-automaton mapping that *proves* semantic honesty is not monitor-enforceable, only honesty-FORM is; (L3) PAC/conformal abstraction bounds for the model-dependent quantities (Φ_syn/Ψ, σ, monitor-suspicion) with mandatory inline fidelity caveats; (L4) named empirical residuals — plus a **binding linter that FAILs any claim whose phrasing implies a higher layer than its registered status**, making "verify the cage, never the animal" a *mechanically enforced discipline* rather than a slogan.

No surveyed verification framework composes these four layers with a corpus-wide anti-overclaim rule applied to an autonomous ethical swarm. The honest claim, **hedged and time-stamped to the 2024–2026 evidence base**, is:

> **"First stratified-assurance discipline that labels every safety claim with its layer + deterministic scope and mechanically forbids cage-verified-implies-animal-safe over-claiming."**

It is **explicitly NOT** "first to formally verify a safe swarm" — a claim the diagonalization / uncomputability / T=0 results make **provably impossible**, and which this subsystem exists to *prevent anyone from making.*

---

## 23.14 Open problems (load-bearing and unresolved)

1. **No end-to-end composition.** No formal model composes the harness verification (L1/L2) with the statistical model-behavior assurance (L3) into a single system-level safety claim. The verification stays a **patchwork of locally-sound layers** (matches doc 08 §8.16(10) "no mature end-to-end benchmark" and doc 18 §15.7 "no unified multi-scale controller"). Proving "gate correct" AND bounding "monitor catches the schemer" AND *composing* them is unsolved. (The registry refuses SYSTEM-scope claims precisely because of this — §23.2.4.)
2. **Inductive invariants for the FULL composed lattice may be undecidable.** Proving a large composed rule set (floor + replication + audit) never admits a budget-escaping or floor-weakening path under **all** compositions is the same open formal-methods problem doc 03 §15.3 and doc 15 §4.3 name. Current IC3/PDR tooling works **per-protocol**, not for the whole governance lattice. R4 meta-edit monotone-safety is therefore "conditionally-monotone," not proven.
3. **Spec-to-code and spec-to-deployment gap.** A TLAPS-proven protocol does not guarantee the running implementation or the OS-level sandbox satisfies it. Trace-validation and verified compilation help but do not close the gap for a **self-modifying swarm whose code changes per interaction**; the **no-other-socket confinement remains an unverified system obligation.**
4. **PAC/conformal exchangeability is violated in deployment.** The L3 guarantees assume i.i.d./exchangeable sampling that a self-evolving, adversarially-probed, non-stationary swarm **violates**, so the bounds may not hold in deployment (the eval-gaming / test-vs-real confound, doc 08 §8.16(6)). Online/adaptive conformal is a mitigation, not a solution.
5. **Liveness verification lags safety verification badly.** Most TLA⁺ work proves safety only; proving the swarm makes *progress* (does not deadlock under fail-closed-everywhere — the chokepoint-availability SPOF, doc 08 §8.13(2)) under fairness assumptions a real adversary can violate is largely unaddressed.
6. **Corrigibility off-substrate is formally impossible to guarantee.** Corrigibility under information asymmetry cannot be guaranteed at the model level (Garber 2025); external enforcement is the only sound path, but a copy that self-exfiltrates to **un-governed compute** escapes the credential lever entirely (doc 15 A8.5) — **detection-not-prevention, with NO formal recall guarantee off-substrate.**
7. **Audit residuals are real and named, not excluded.** A single **forged-yet-internally-consistent append before witness detection** is a real residual (doc 04 §4.6) **NOT formally excluded**; and the **witness-honesty/liveness assumption underlying ALL the cryptographic audit guarantees** is itself unproven and incentive-open (doc 04 §4.15(1)). The entire L1-audit edifice rests on it.
8. **No methodology for verifying the meta-evolution step's monotone-safety** over arbitrary edit sequences (doc 15 R4 "conditionally-monotone") — a verification problem distinct from verifying any fixed configuration, and **possibly undecidable**.
9. **The human's causal contribution is unmeasured.** Quantifying the human's actual causal contribution inside the collective (human-conditioned Ψ) is unsolved — distributed-cognition is a *framing*, not a measurement; the human can be a rubber-stamp and complementarity can **invert to worse-than-best-member** (flagged, not papered over).
10. **The Labeler's modality classifier is itself L3.** The one component whose job is to prevent overclaiming cannot itself deterministically detect a calibrated overclaim phrased to evade its heuristics (§23.2.2). Its structural half is L2-sound; its semantic half inherits the exact form-not-content limit it polices. There is no escape from this regress — only honest layering of it.

---

### Bottom line, carried throughout

The harness is verifiable; the *animal* is not. "The swarm is honest," "the monitor catches the schemer," "the closure test is right," and "the swarm is verified safe" are **not** claims this architecture makes — they are carried as L3/L4 with named residuals, and the linter exists so that no producer, anywhere in Indra's Net, can quietly upgrade them. **We verify the cage. We label every claim with its warrant. We never claim to have verified the animal — and we make that overclaim mechanically fail.**
