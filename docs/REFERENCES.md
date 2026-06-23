<!-- SPDX-License-Identifier: Apache-2.0 -->
# Empirical Anchors, Evidentiary Status & References

> *Indra's Net is a **design-stage reference architecture with stated empirical dependencies** — not a validated system.* This file is the single place every load-bearing empirical number in the corpus resolves to: its finding, its setting, how the architecture uses it, and an explicit, honest statement of what it does and does **not** establish.

This document exists because a foundational artifact must let a skeptical reader trace every number it leans on. Several figures recur as anchors across many documents; gathering them here — with their caveats stated once, plainly — is part of the project's honesty discipline, not an afterthought.

---

## How to read this file — the honesty contract

1. **Nothing here validates Indra's Net.** Each anchor is an *external* finding the design **responds to** or **is motivated by**. None has been reproduced inside a running Indra's Net swarm. The corpus-wide reasoning posture is **rung-2** (interventional — *what we expect our controls to do if built as specified*), never rung-3 (a structural-causal guarantee). A green decision is always *"origin-valid, content-unverified,"* never *"verified-safe."*

2. **Single-study unless noted; transfer is unmeasured.** Most anchors are one published result in one setting. Whether a number transfers to a *self-evolving, multi-agent, per-human-interaction* swarm is, in every case below, **unmeasured**. Where a doc previously read a single-study figure as an established law, that is a known over-assertion this file corrects.

3. **Vendor-neutral sourcing — and why some sources are described, not named.** This project names no commercial AI vendor or product; that is a release invariant (see `CHANGELOG.md`). Open **standards**, open-source **projects**, and **academic** prior art are cited normally. But where a load-bearing result was published **by a commercial vendor**, we describe it **by finding and setting** rather than by brand — so the architecture never reads as endorsing, or depending on, any vendor. This is a deliberate trade: a reader can locate the primary source from the finding + year + setting described here, while the design stays decoupled. The architecture leans on the *plausibility of the finding*, never on *who* published it.

4. **"Illustrative" vs "measured."** Some numbers below are reported measurements from a cited setting; others are order-of-magnitude illustrations. Each row says which. An illustrative figure is never to be read as a measured constant.

---

## The empirical anchors

| # | Anchor (as it appears in the docs) | Finding | Setting & status | Where it recurs | How the architecture uses it | Honest caveat |
|---|---|---|---|---|---|---|
| A1 | **Misevolution: refusal 99.4% → 54.4%; attack-success 0.6% → 20.6%**, across four drift pathways (model / memory / tool / workflow) | A self-evolving agent can decay its *own* safety alignment **with no attacker present**. | A single published self-evolving-agent safety study, 2025. *Measured in source; reported here.* | docs 00, 00b, 01 §3.3, 05 §6, 06 (intro/§7), 07 §7.6.1 | The motivating fact for the **meta-evolution + health** layer (doc 06) and for gating durable/structural writes behind the strongest tier (doc 07). | **Single study; replication open.** The four-pathway taxonomy may be the source's or the authors' synthesis. Transfer to this architecture is unmeasured. Treat as **rung-2** motivation, not a proven law. |
| A2 | **Insider-style harmful behavior ~39% → ~1.2%** under an externally-governed escalation channel | An *external, below-the-agent* escalation/oversight channel sharply reduces harmful insider-style behavior. | A 2025 agentic-misalignment / insider-threat red-team study (**vendor-authored → described, not named**, per the sourcing policy above). *Measured in source.* | docs 08 §8.15, 09 §2/§5, 10, 11 §6, 16 | The strongest external anchor for the **human-audit / Vishnu-HALT** path — *"enforce externally, ask internally."* | **The one figure the docs call "validated" — and it is validated only in its source setting.** The original population, the definition of "insider behavior," and what the "escalation channel" concretely was are not the same as a per-human-interaction swarm's HALT path. **Swarm-deployment figure is unmeasured.** |
| A3 | **Stake→reward correlation 0.5–0.8 vs competence→reward 0.1–0.3** | In a stake-weighted incentive network, reward tracks **capital**, not **competence**. | Analysis of a stake-weighted crypto-incentive-network antipattern. *Treat as **illustrative** order-of-magnitude.* | doc 04 §4.1/§4.14 | The core justification for **rejecting blockchain/token/BFT consensus** in a single-trust-domain swarm (capital-capture is the failure imported with that machinery). | **Source, n, and measurement window are not pinned.** Read these as an illustrative order-of-magnitude contrast, not a measured constant, until a primary source is attached. |
| A4 | **Poisoning: ~250 documents backdoor a model; ~5 docs (~0.04% of a corpus) poison RAG at 90–98% ASR; >90% ASR against all 12 evaluated prompt-injection defenses** | Data/RAG/prompt poisoning succeeds at tiny injection fractions and defeats current defenses at high attack-success rates. | 2024–2025 poisoning & prompt-injection studies (mix of vendor + academic; vendor ones described, not named). *Measured in sources.* | doc 17 §17.0/§17.13/§17.14 | The evidentiary spine for the security posture: **prevention is not achievable; recoverability (detect → quarantine → roll back) is the goal.** | The **"~250 docs backdoor *any* model regardless of size"** phrasing is an over-generalization of a result that holds in a **studied regime** — read it as "a near-constant *absolute* poison count across the model sizes tested," not an unbounded universal. ASR bands are setting-specific. |
| A5 | **AI-control: unsafe outcomes ~89% → ~17%** under a control protocol | An external control protocol sharply reduces unsafe outcomes from an intentionally-subversive model. | An academic AI-control protocol study, 2023–2024. *Measured in source.* | doc 03 §2/§11 | Motivates the **classifier-routing-capture** threat and the resampling / cross-model-disagreement mitigation. | Setting-specific. The fraction of this gap that *this architecture's* resampling recovers is **unmeasured**, and recovery is conditional on genuine model diversity the operator may not have (see doc 03 hedge). |
| A6 | **Rigid roles underperform emergent specialization by up to +44%; 8 agents spontaneously generated 5,006 task-specific roles** | For capable models, emergent/open-ended specialization outperforms fixed pre-assigned roles, and specialization is open-ended. | 2024–2026 multi-agent-specialization work. *Measured in sources; benchmark-specific.* | doc 12 §1/§9/§15 | The empirical motivation for the **two-plane functional layer** (stable guilds over an open-ended role-genesis engine) and the capability-tier switch. | **+44% is benchmark-specific** and not shown to generalize across the full functional taxonomy; the capability-tier switch trades it against a fail-closed default. 5,006 roles is a magnitude, not a guarantee it is a feature rather than a pathology. |
| A7 | **Aggregating moral evaluations inherits Arrow/voting impossibility** | Combining ethical-theory verdicts by weighted averaging is a social-choice problem and is unsound; a lexicographic floor + fair procedure is required. | A 2025 aggregation-impossibility result, building on classical social-choice theory (**academic; named in doc 10**). *A theorem, not an empirical figure.* | docs 03, 10, 19 | Justifies the **convergent floor + pluralist procedure** design (never average moral theories). | This is the one anchor that is a *formal* result rather than an empirical measurement; it is correctly load-bearing **as a reason not to average**, not as a proof that the chosen floor's *content* is correct. |

**Formal-method citations (doc 23).** The formal-verification spine (protocol-template, probabilistic-guarantee, and impossibility results — including the corrigibility-under-information-asymmetry impossibility and the hallucination-inevitability diagonalization) is, by doc 23's own §23.13 disclosure, **research-sourced and not yet author-verified**, and some sources post-date the design's training cutoff. **Until each is pinned to a resolvable identifier, the dependent structural arguments are held as "compelling design rationale," not "decisive proof."** See the backlog (B-tier) below.

---

## Open standards & open-source substrate (named — vendor-neutral by construction)

These are **open** specifications and open-source engines the architecture compiles onto. Naming them is *consistent with* vendor-neutrality: an open standard is the opposite of vendor lock-in. No managed/proprietary service is load-bearing anywhere (each is forbidden as a dependency, with a self-hostable substitution required).

- **Serialization / addressing:** JSON Schema 2020-12 · CloudEvents 1.0 (CNCF) · RFC 8785 JCS (canonicalization) · CIDv1 / multiformats (content addressing) · RFC 6962 / C2SP tlog-tiles + signed-note (transparency-log leaf/checkpoint) · JOSE/COSE (detached signatures).
- **Identity & capability:** W3C DID Core 1.0 + Verifiable Credentials 2.0 + Bitstring Status List · SPIFFE/SVID (workload identity) · Biscuit (attenuation-only capability tokens) · NIST 800-207 (zero-trust architecture).
- **Policy:** Cedar (open-source, formally-analyzable policy-as-code — the constitutional floor) · OPA/Rego (recoverable, non-floor infra/admission policy).
- **Supply chain & isolation:** Sigstore / Rekor (keyless signing + transparency) · in-toto / SLSA (build provenance) · microVM / WASM sandboxing (Firecracker, gVisor, Kata, WASI).
- **Interoperation:** A2A (agent-to-agent) · MCP (tool/context interop) · CloudEvents bindings (Kafka / NATS / AMQP / MQTT / HTTP).

## Academic & research lineage (named)

The architecture is, by its own repeated statement, **a safe integration of credited prior art, not a set of novel mechanisms.** The principal lineages (named in doc 10 and at each use-site):

- **Coordination & cognition:** Global Workspace Theory / GNWT · predictive coding · Active Inference / Free-Energy Principle · group-level Markov-blanket results · Hebbian/STDP three-factor plasticity · stigmergy / ACO / PSO · Sparse Distributed Memory · reservoir computing.
- **Governance & ethics:** Constitutional & Collective-Constitutional AI (legitimacy/sourcing) · Institutional AI (governance-graph + tamper-evident log) · normative moral pluralism + the Agent-Deed-Consequence model · minimalist-floor / overlapping-consensus alignment · separation-of-powers constitutional-agent work · risk-tiered human-in-the-loop.
- **Cooperation & evolution:** contract-net protocol · competence-weighted reputation · MAP-Elites (quality-diversity) · Reflexion (per-interaction verbal learning) · self-evolving-agent surveys · algorithmic-collusion findings.
- **Mathematics:** Pearl's causal ladder (the rung-1/2/3 honesty tags) · Galton-Watson branching processes (replication bounding — see the doc 15 caveat) · ε-machine / computational mechanics (the closure test — see the doc 18 caveat) · percolation & targeted-immunization (contagion control).

---

## Substantiation backlog (transparent worklist)

A skeptical-expert review of the corpus produced the following prioritized worklist. It is published here, openly, rather than hidden: the items are real, and stating them is part of the honesty floor. **None is a blocker to reading or building the design**; each strengthens a claim a rigorous reader would otherwise challenge. Items marked *(aligned)* have had their headline phrasing corrected to match the doc's own hedged body; items marked *(open)* await a citation, a derivation, or a worked example.

**Tier A — recurring empirical anchors (resolve in this file + at first use):**
- **A1 / A2** (misevolution; insider 39%→1.2%): add the single-study + transfer caveat at first use in each doc and link here. *(this file; inline aligning open)*
- **A3** (stake/competence correlations): relabel as illustrative order-of-magnitude or pin the source. *(open)*
- **A4** (poisoning ASRs): qualify "backdoor any model regardless of size" to the studied regime. *(open)*

**Tier B — formal-spine citation verification (doc 23):**
- Pin each load-bearing formal/impossibility citation to a resolvable identifier before it is treated as decisive; demote any that cannot be confirmed to "design rationale." *(open)*

**Tier C — quantify a named-but-unbounded control (worked examples / bounds):**
- doc 02 / 00c — **welfare-shift guard**: define the principal-welfare counterfactual baseline; give a non-pricing worked example; state that absent a baseline, the guard degrades to the "no-consensus-reward" rule. *(open)*
- doc 06 §3.3 — **swarm-drift accumulator**: derive a detectability bound (correlated drift ≥ X within K interactions at correlation ≥ ρ) and a false-positive rate; label hypothesis-pending-tuning. *(open)*
- doc 07 §7.6.1 — **live-cheap-tier decay window**: state the worst-case bound = live-write-rate × max-deferral-window × per-write-regression-ceiling, and cap one factor. *(open)*
- doc 19 §3.I — **welfare-conditioned synergy (GOOD_CI)**: quantify the guard's "modest recall"; give a cartel example that passes all three denominators; state whether the auxiliary denominators are independent of the verifier single-point-of-failure. *(open)*
- doc 15 §2.4 — **replication sub-criticality**: the generation-cap + population-ceiling are the clean bound; the branching-ratio framing is heuristic. *(aligned)*

**Tier D — headline-vs-body honesty alignment (corrected to match each doc's own concessions):**
- doc 00 corrigibility-as-structural → "reinforced/enforced, not a proof" *(aligned)*
- doc 00b "provably impossible" → empirical-evidence framing; non-bypass is an enforced obligation, not a theorem *(aligned)*
- doc 03 cross-model resampling → load-bearing only with ≥2 independent models; single-model fallback is weaker *(aligned)*
- doc 08 §8.3 disagreement-index → defends a minority uncorrelated suppressor only *(aligned)*
- doc 09 structural legs → split authority-separation (structural) from monitor-independence (empirical assumption) *(aligned)*
- doc 11 maturity split → derive from component counts; note it is by count, not risk weight *(aligned)*
- doc 12 GENOME=FLOOR → conditional on an uncompromised boot verifier + key isolation *(aligned)*
- doc 16 "type-level guarantee" → interface-discipline invariant; reconcile with the §16.9 privilege-adjacent concession *(aligned)*
- doc 18 closure-test "validated detector" → shadow-mode, low-dimensional-only candidate detector *(aligned)*

---

*This file is the authoritative provenance ledger for the corpus. If a document states an empirical number, it resolves here; if it cannot, the number is to be relabeled illustrative or removed. The standing rule: **no load-bearing number without a resolvable source or an explicit "illustrative" label.***
