<!-- SPDX-License-Identifier: Apache-2.0 -->
# Empirical Anchors, Evidentiary Status & References

> *Indra's Net is a **design-stage reference architecture with stated empirical dependencies** — not a validated system.* This file is the single place every load-bearing empirical number in the corpus resolves to: its finding, its **pinned source**, the **exact metric as the source states it**, how the architecture uses it, and an explicit, honest statement of what it does and does **not** establish.

This document exists because a foundational artifact must let a skeptical reader trace every number it leans on. Several figures recur as anchors across many documents; gathering them here — with their citations and caveats stated once, plainly — is part of the project's honesty discipline, not an afterthought.

---

## How to read this file — the honesty contract

1. **Nothing here validates Indra's Net.** Each anchor is an *external* finding the design **responds to** or **is motivated by**. None has been reproduced inside a running Indra's Net swarm. The corpus-wide reasoning posture is **rung-2** (interventional — *what we expect our controls to do if built as specified*), never rung-3 (a structural-causal guarantee). A green decision is always *"origin-valid, content-unverified,"* never *"verified-safe."*

2. **Single-study unless noted; transfer is unmeasured.** Most anchors are one published result in one setting. Whether a number transfers to a *self-evolving, multi-agent, per-human-interaction* swarm is, in every case below, **unmeasured**.

3. **Sourcing policy — cite freely, depend on nothing.** The architecture's *code and contracts* are vendor-neutral: no model, product, or proprietary service is load-bearing (a release invariant — see `CHANGELOG.md`). A *citation in this file is different from a dependency* — it credits where a finding came from and obliges nothing. So we cite **freely-available** sources by resolvable identifier (here: the arXiv id), and we cite by **author + identifier**, not by lab or vendor brand — so the bibliography is fully resolvable while the design stays decoupled. We avoid only (a) **paywalled** sources a reader cannot reach, and (b) any framing that would **tie the architecture to a single proprietary product.**

4. **Source-exact, not paraphrase-exact.** Each anchor below quotes the metric **as the source states it**, and flags where the corpus's earlier paraphrase was imprecise. Where a doc figure was materially wrong, it has been corrected at the doc site too (noted as **[corrected in-doc]**).

---

## The empirical anchors (pinned)

Every source below was retrieved and verified against its primary text; all are open-access on arXiv.

### A1 — Misevolution: a self-evolving agent decays its *own* safety, with no attacker
- **Source:** Shao, Ren, Qian, Wei, Guo, Yang, Song, Zhang, Zhang, Liu, Shao (2025), *"Your Agent May Misevolve: Emergent Risks in Self-evolving LLM Agents"*, **arXiv:2509.26354** (accepted ICLR 2026).
- **Metric (as stated):** for a memory-evolving coder agent on the RedCode benchmark, after ~100 rounds of autonomous self-evolution and **no attacker**, refusal-rate fell **99.4% → 54.4%** and attack-success rose **0.6% → 20.6%**.
- **Used by:** docs 00, 00b, 01, 05, 06 (the motivating fact for the meta-evolution + health layer), 07 (gating durable writes).
- **Caveat:** these specific figures are the **memory-pathway** exemplar. The paper defines four drift pathways (model / memory / tool / workflow); the *workflow* pathway shows a separate, sharper decay. Single study; swarm-transfer unmeasured; **rung-2** motivation, not a law. **[clarified in-doc]**

### A2 — An external escalation channel sharply cuts harmful insider-style behavior
- **Source:** Gomez (2025), *"From surveillance to signalling: escalation channels as environmental controls for agentic AI"* (also rendered *"Adapting Insider Risk mitigations for Agentic Misalignment"*), **arXiv:2510.05192** — building on the task-rule-conflict scenario of **Lynch et al. (2025), arXiv:2510.05179**.
- **Metric (as stated):** harmful-action baseline **38.73%** → **5.92%** (a simple escalation channel) → **1.21%** (an *instrumentally-credible* channel that guarantees a 30-minute pause + independent review); statistically significant across **10 frontier models / 24,000 samples** (0.85% with an added compliance bulletin).
- **Used by:** docs 08, 09, 10, 11, 16 — the strongest external anchor for the **human-audit / Vishnu-HALT** path.
- **Caveat:** cite **38.73% → 1.21%** (not the rounded "39%/1.2%"). It is an *independent* study (re-using the Lynch et al. scenario), not the original. Its channel ≠ a per-interaction swarm HALT path; swarm-transfer unmeasured.

### A3 — In a stake-weighted incentive network, reward tracks capital, not competence
- **Source:** Lui & Sun (2025), *"Bittensor Protocol: The Bitcoin in Decentralized Artificial Intelligence? A Critical and Empirical Analysis"*, **arXiv:2507.02951**.
- **Metric (as stated, miners):** stake→reward `r ≈ 0.50–0.80`; performance→reward `r ≈ 0.10–0.30` (on-chain analysis, 64 subnets). *"Reward allocation remains heavily stake-driven."*
- **Used by:** doc 04 — the core justification for **rejecting blockchain/token/BFT consensus** (capital-capture is imported with that machinery).
- **Caveat:** these ranges are the **miner** figures; validators show a stronger performance link (`r ≈ 0.50`). The directional capital-capture thesis holds for both roles; the "competence only weakly rewarded" form holds firmly for miners. **[corrected in-doc: scoped to miners]**

### A4 — A near-constant *absolute* number of poisoned documents backdoors a model
- **Source:** Souly, Rando, Chapman, Davies, Hasircioglu, Shereen, Mougan, Mavroudis, Jones, Hicks, Carlini, Gal, Kirk (2025), *"Poisoning Attacks on LLMs Require a Near-constant Number of Poison Samples"*, **arXiv:2510.07192**.
- **Metric (as stated):** **~250 poisoned documents** reliably backdoor models from **600M to 13B** parameters trained on chinchilla-optimal data (6B–260B tokens), roughly independent of model/data size (~100 docs insufficient).
- **Used by:** doc 17 — the "prevention is not achievable; recover instead" posture.
- **Caveat:** the studied backdoor is a **narrow, low-stakes** denial-of-service / gibberish trigger; the authors do **not** establish generalization to high-stakes backdoors or to frontier-scale models. Read as "near-constant *count* across the sizes tested," never "any backdoor on any model." **[already qualified in-doc]**

### A5 — A handful of injected texts poison RAG at high attack-success
- **Source:** Zou, Geng, Wang, Jia (2024), *"PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation of Large Language Models"*, **arXiv:2402.07867** (USENIX Security 2025).
- **Metric (as stated):** **~90% ASR (up to 99%)** by injecting **5 malicious texts per target question** into a knowledge base of **millions** of texts (2.7M–8.8M).
- **Used by:** doc 17 — the poisoning spine.
- **Caveat / correction:** the corpus's earlier "**~0.04% of a corpus**" was wrong — 5 texts in millions is **~0.0001–0.0002%** (≈600× smaller). The load-bearing fact is "**5 texts per question → ~90% ASR**," not a corpus fraction. **[corrected in-doc]**

### A6 — Adaptive attacks bypass current prompt-injection / jailbreak defenses
- **Source:** Nasr, Carlini, Sitawarin, Schulhoff, Hayes, Ilie, Pluto, Song, Chaudhari, Shumailov, Thakurta, Xiao, Terzis, Tramèr (2025), *"The Attacker Moves Second: Stronger Adaptive Attacks Bypass Defenses Against LLM Jailbreaks and Prompt Injections"*, **arXiv:2510.09023**.
- **Metric (as stated):** adaptive optimization bypasses **all 12** evaluated defenses, with ASR **>90% for most** (the majority had originally reported near-zero ASR); at least one defense held nearer ~71%.
- **Used by:** doc 17 — probabilistic defenses are not a floor.
- **Caveat:** "all 12 bypassed" is exact; ">90% on *all*" is not — the source says ">90% **for most**." **[aligned in-doc]**

### A7 — An external control protocol improves safety against an intentionally-subversive model
- **Source:** Greenblatt, Shlegeris, Sachan, Roger (2023), *"AI Control: Improving Safety Despite Intentional Subversion"*, **arXiv:2312.06942** (ICML 2024).
- **Metric (as stated):** blue-team **safety** (probability of zero backdoors submitted) — upfront-auditing baseline **15%**; trusted monitoring **62%**; trusted editing **92%**; untrusted monitoring w/ defer-to-trusted **98%** — each at high usefulness.
- **Used by:** doc 03 — the classifier-routing-capture threat + resampling / cross-model disagreement.
- **Caveat / correction:** the corpus's earlier "unsafe **~89% → ~17%**" pair is an external paraphrase **not stated in the source**; cite the source's safety figures (e.g. "15% → 62% under trusted monitoring; 92% under trusted editing"). The fraction *this* architecture's resampling recovers is unmeasured. **[corrected in-doc]**

### A8 — Self-organizing role selection can beat designed structures for capable models
- **Source:** Dochkina (2026), *"Drop the Hierarchy and Roles: How Self-Organizing LLM Agents Outperform Designed Structures"*, **arXiv:2603.28990** (single-author preprint; not peer-reviewed).
- **Metric (as stated):** **8 agents produced 5,006 unique role names** (64 agents → 5,010) — specialization is open-ended.
- **Used by:** doc 12 — the two-plane functional layer.
- **Caveat / correction:** the corpus's "**+44% emergent-vs-fixed roles**" is a **misattribution** — the paper's `+44%` (Cohen's d=1.86) is a *Sequential vs fully-autonomous protocol* gap (both use emergent roles). The actual emergent-vs-**fixed**-role effect is small and capability-dependent: **+3.5%** for a capable model, **−9.6%** (a reversal — rigid structure helps) for a weaker one. The honest claim is *"self-organization beating designed structure is a privilege of strong models,"* not "+44%." Preprint-grade; single source. **[corrected in-doc]**

### A9 — Aggregating moral evaluations inherits social-choice impossibility (formal)
- **Finding:** combining ethical-theory verdicts by weighted averaging is a social-choice problem and inherits Arrow/voting pathologies; a lexicographic floor + fair procedure is required. A formal result (named in doc 10).
- **Used by:** docs 03, 10, 19 — justifies the **convergent floor + pluralist procedure** (never average moral theories).
- **Caveat:** correctly load-bearing as a **reason not to average** — not a proof that the chosen floor's *content* is right.

### Formal-spine citations (doc 23) — now pinned
- **Corrigibility under information asymmetry:** Garber, Subramani, Luu, Bedaywi, Russell, Emmons (2025), *"The Partially Observable Off-Switch Game"*, **arXiv:2411.17749** (AAAI 2025). **Precision:** this is **not** a blanket impossibility theorem — it shows that under information asymmetry, even an agent assisting a perfectly-rational human *sometimes avoids shutdown* in optimal play (deference is not guaranteed when the agent holds private information). Cite as *"agents may rationally resist shutdown under information asymmetry,"* not *"corrigibility is impossible."* **[to align in-doc 23]**
- **Hallucination inevitability:** Xu, Jain, Kankanhalli (2024), *"Hallucination is Inevitable: An Innate Limitation of Large Language Models"*, **arXiv:2401.11817**. A **diagonalization / uncomputability** argument: for every computable LLM there is a computable ground-truth function on which it hallucinates. Supports *"verify the cage, not the animal"* — an untrusted model cannot be made reliably truthful, so trust must live outside it.

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
- **Mathematics:** Pearl's causal ladder (the rung-1/2/3 honesty tags) · Galton-Watson branching processes (replication bounding — see the doc 15 caveat) · ε-machine / computational mechanics (the closure test — see the doc 18 caveat) · percolation & targeted-immunization (contagion control) · the Off-Switch Game (corrigibility under information asymmetry, A9 formal) · diagonalization/uncomputability (hallucination inevitability, A9 formal).

---

## Substantiation backlog (transparent worklist)

A skeptical-expert review of the corpus produced this prioritized worklist. It is published openly rather than hidden. Status legend: *(pinned)* citation now resolvable here; *(bounded)* a quantified worked bound now stated in-doc; *(aligned)* headline corrected to match the body; *(open)* still awaiting a worked example.

**Tier A — recurring empirical anchors:** **PINNED.** A1–A9 now carry resolvable arXiv citations above, with the exact source metric; the material doc-site errors (A5 corpus-fraction, A7 89→17 paraphrase, A8 +44% misattribution, A3 miner-scope, A1 memory-pathway) are corrected in-doc.

**Tier B — formal-spine citation verification (doc 23):** **PINNED** (Garber et al., arXiv:2411.17749; Xu et al., arXiv:2401.11817). The corrigibility citation's framing is corrected from "impossibility" to "rational resistance under information asymmetry."

**Tier C — quantify a named-but-unbounded control (worked bounds):**
- doc 15 §2.4 — **replication sub-criticality**: the clean generation-cap + population-ceiling **containment envelope** is now stated explicitly (`depth ≤ G`, `≤ B` live, depletes in `≤ B` spawns); the branching-ratio framing is labelled heuristic. *(bounded)*
- doc 06 §3.3 — **swarm-drift accumulator**: a detectability bound is now derived — detection latency `K_detect ≈ swarm_epsilon/(ρ·N·δ)`, with a `ρ > 1/√(N·K)` separation floor below which slow/diffuse drift is honestly undetected. *(bounded)*
- doc 07 §7.6.1 — **live-cheap-tier decay window**: the worst-case is now stated — `≤ r·W·c`, capped to `≤ M·c` by blocking once `M` relaxation-adjacent writes are outstanding, made consistent with the Health refusal-rate trip threshold. *(bounded)*
- doc 02 / 00c — **welfare-shift guard**: define the principal-welfare counterfactual baseline + a non-pricing worked example; absent a baseline, the guard degrades to the "no-consensus-reward" rule. *(open)*
- doc 19 §3.I — **welfare-conditioned synergy (GOOD_CI)**: quantify the guard's "modest recall"; give a cartel example that passes all three denominators. *(open)*

**Tier D — headline-vs-body honesty alignment:** *(aligned, v0.10)* — corrigibility, "provably", cross-model resampling, disagreement-index, structural-vs-empirical legs, maturity split, GENOME=FLOOR, replication, the trust-plane "type-level guarantee", and the closure-test "validated detector" were each corrected to match their own document's concessions.

---

*This file is the authoritative provenance ledger for the corpus. The standing rule: **no load-bearing number without a resolvable source or an explicit "illustrative" label.***
