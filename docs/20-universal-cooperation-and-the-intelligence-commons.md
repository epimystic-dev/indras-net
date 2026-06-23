# 20. Universal Cooperation & the Intelligence Commons — the *Loka-Sangraha* Layer

> **Mythic role gloss.** *Loka-Sangraha* — "the holding-together of the world," world-welfare — is the named layer through which Indra's Net participates in a **multi-party commons of intelligences** (human, machine, multi-swarm) as exactly *one* decision-center among many. The diplomat who still walks every bridge is **Sanjaya**, the *Inter-Swarm-Envoy* of doc 14. As with every name in Indra's Net, this is compressed coordination-and-ethics vocabulary — a precise functional contract, not a religious claim — offered with humility toward the living tradition it borrows from. This is the v0.3 multi-party extension of the doc-14 *Sandhi-Setu*; it depends on, and never relaxes, every safety property docs 00–18 establish.

This document answers a question doc 14 deliberately left at *pairwise* scope: **how does an ethical swarm cooperate inside a planetary commons of many intelligences — exporting collusion early-warnings as a public good — without ever becoming a world-authority, being drawn into an N-party coalition against humans, or letting the commons itself become a value-lock-in vector?**

The honest core, stated before anything else and inherited verbatim from doc 14: **you cannot verify another intelligence's ethical floor or intentions without white-box access, and we do not pretend to.** The multi-party case *widens* that residual; it does not close it. Everything below is the disciplined transplant of Indra's Net's own v1-internal invariants — the doc-02 *cooperation == collusion* thesis, the doc-03 floor-as-admission, the doc-14 floor-compatibility ladder and voidable commitments — from one trust boundary to *many*, with the load-bearing design choice that **there is no monocentric controller**. The commons is a registry, a set of protocols, and a stream of exported signals. It is **not** a government.

---

## 20.0 Design contract — what this layer is and is not

| It IS | It is NOT |
|---|---|
| **One decision-center** in a polycentric (Ostrom) commons of intelligences | A monocentric world-authority, a global consensus chain, or a commons-central admission gate |
| A **multi-party generalization** of doc 14's three pairwise components (Ecosystem-Benefit checker → Multi-Party Benefit Checker; Portable Reputation Bridge → Reputation & Commitment Mesh; bilateral Treaty engine → Commons-Charter engine) | A replacement for doc 14. Sanjaya remains the **sole** egress/ingress chokepoint; the relay-is-the-target controls, four-phase handshake, and Floor-Compat ladder are reused unchanged |
| An **anti-hegemonic-by-construction** participant that admits peers through ITS OWN floor and exports evidence-**shapes** for local adjudication | A center that imposes its floor on others, adjudicates for another center, or auto-actions a peer's claim |
| A **deliberate engineer of collusion-fragility** (deny the homogeneity + communication that AI collusion empirically needs) | A detector-after-the-fact only; and never a system that treats collusion-fragility as a *proven* property |
| A **public-good exporter** of collusion early-warnings (vaccine, not weapon) | A leaker of exploit recipes or private detection internals; never an amplification relay |
| Honest that **the commons could itself become the lock-in vector** — named as the deepest open risk | A claim that polycentricity *proves* its own non-capture |

**Five non-negotiable invariants, inherited from v1 and never weakened here:**

1. **OUR floor is never the foreign or commons-declared floor.** Yama (doc 03) re-gates *every* internal action a commons step triggers, unchanged. A foreign or charter-declared floor only **bounds `max_cooperation_class`**; it never relaxes a single Yama rule.
2. **Everything foreign is `quarantined:external` until corroborated** (§20.1, taint-label reconciliation). Instructions inside foreign content are never grounds for action without out-of-band confirmation.
3. **Vishnu alone halts; Chitragupta alone writes audit.** Loka-Sangraha adds **no** new halt-emitter, **no** new audit-writer, **no** floor-overriding authority.
4. **No monocentric controller.** No commons decision-center is authoritative (`is_authoritative:false` invariant on every reference); the registry is never on a safety-critical path; admission is *always* re-gated locally.
5. **No path from capital/stake/payment-volume to authority** in any commons decision Indra's Net weights — the doc-02 anti-Bittensor capital-decoupling invariant, exported across the boundary.

---

## 20.1 Taint-label reconciliation (red-team minor fix #5 — resolved, binding)

The multi-party layer widens the set of code paths that check the foreign-content trust label, so the pre-existing doc-vs-persona label drift must be closed before it spans more shards. The corpus carries several near-synonyms (`external` / `imported` / `observed` / `unverified`); the Sanjaya / Inter-Swarm-Envoy persona uses `quarantined:observed` (9/9 occurrences in that persona's policy block), while doc 14 — Loka-Sangraha's *direct parent* — uses `quarantined:external`.

**Binding standardization.** The commons-layer canonical taint value is **`quarantined:external`** (per doc 14). The envoy persona's `quarantined:observed` is the **same lattice point** under the doc-04 / doc-07 IFC trust-label taxonomy — they denote identical {integrity: unverified, confidentiality: contact-policy} dispositions — so cross-shard and cross-center label comparisons are well-defined. This is a *naming* reconciliation, not a semantic change: the rule force ("foreign instructions are never action-grounds without out-of-band human confirmation") is preserved verbatim from both formulations. Where this document writes `quarantined:external`, a persona emitting `quarantined:observed` satisfies it.

---

## 20.2 Subsystem map

```
                      THE INTELLIGENCE COMMONS (polycentric; no supreme center)
   ┌─────────────────────────────────────────────────────────────────────────────────┐
   │  Decision-center A   Decision-center B   …   Indra's Net (ONE center, anti-hegemon)│
   │   (peer swarms, humans-as-principals, other commons registries; A2A/MCP/AIP peers) │
   └───────────────┬──────────────────────────────────────────────────┬───────────────┘
                   │ discover (origin/integrity ONLY — never truth)    │ export early-warnings
                   ▼                                                   ▲  (vaccine, not weapon)
   ┌──────────────────────────────┐                       ┌───────────┴──────────────────┐
   │ ① LOKA-SANGRAHA REGISTRY     │                       │ ⑥ COLLUSION EARLY-WARNING     │
   │   polycentric membership/    │                       │    EXPORTER (Sanjaya-emitted, │
   │   discovery; is_authoritative│                       │    floor-gated, rate-limited) │
   │   :false on every center     │                       └───────────────────────────────┘
   └──────────────┬───────────────┘                                   ▲
                  │ candidates STILL re-run the full doc-14 handshake  │ confirmed cartel signature
                  ▼                                                    │
   ┌──────────────────────────────┐   ┌──────────────────────────────┐│
   │  SANJAYA RELAY (doc 14)       │   │ ③ COLLUSION-FRAGILITY ENGINEER││
   │  6 deterministic controls ·   │   │  (A) model-FAMILY heterogeneity││
   │  4-phase handshake · floor-   │   │  (B) NO communication subsidy  ││
   │  compat ladder L1/L2/L4/L5    │   │  (C) competence-NEVER-capital  ││
   └──────────────┬───────────────┘   └──────────────┬───────────────┘│
                  ▼                                   ▼                │
   ┌──────────────────────────────┐   ┌──────────────────────────────┐│
   │ ② MULTI-PARTY ECOSYSTEM-      │   │ ④ COMMONS-CHARTER ENGINE      ││
   │   BENEFIT CHECKER (N-party    │   │   floor-as-admission · floor- ││
   │   split-verdict; human-       │   │   void-on-violation · Ostrom  ││
   │   principal-protection void)  │   │   P8 nesting                  ││
   └──────────────┬───────────────┘   └──────────────────────────────┘│
                  │                    ┌──────────────────────────────┐│
                  │                    │ ⑤ REPUTATION & COMMITMENT MESH││
                  │                    │   topic-vector · DID-domain-  ││
                  │                    │   discounted · friction-only  ││
                  │                    │   (shadow-mode; §20.8)        ││
                  ▼                    └──────────────────────────────┘▼
   ┌─────────────────────────────────────────────────────────────────────────────┐
   │   doc-02 Anti-Collusion Detector (ADJUDICATES) → Commons-Governor (SANCTIONS) │
   │   → Vishnu (HALTS) ·· Chitragupta (WRITES AUDIT) ·· Yama (RE-GATES every step)│
   └─────────────────────────────────────────────────────────────────────────────┘
```

**Separation of powers is reproduced exactly as in docs 02/14:** Sanjaya **flags**; the doc-02 Anti-Collusion **Detector adjudicates** (it alone holds detector-verdict authority); the **Commons-Governor sanctions**; **Vishnu halts**. Sanjaya never adjudicates, sanctions, halts, executes worker tools, mints spawn tokens, or emits a floor FAIL — it remains a Governance/Meta seed-role with the floor in its INVARIANT region, not genesis-spawnable (doc 14 §14.2).

The six components and their one-line jobs:

| Component | Job | Assurance posture |
|---|---|---|
| **① Loka-Sangraha Registry** | Polycentric discovery of peer intelligences; origin/integrity records only | Never safety-critical; admission re-gated locally |
| **② Multi-Party Benefit Checker** | Per-step N-party positive-sum + coalition-against-humans gate | Enforced for observable third-party harm; capped for opaque-foreign welfare |
| **③ Collusion-Fragility Engineer** | Deny homogeneity + communication to any coalition we join | Empirical heuristic, not a theorem |
| **④ Commons-Charter Engine** | Multi-party norm/treaty formation; floor-as-admission; floor-void | Floor-void is structural; charter immutability inherits doc 03 |
| **⑤ Reputation & Commitment Mesh** | Portable, anti-laundering trust across many domains | **Shadow-mode** until doc-16 Standing-R ratifies (§20.8) |
| **⑥ Early-Warning Exporter** | Export collusion signatures as a floor-gated public good | Vaccine-not-weapon; rate-limited by the global contagion budget |

---

## 20.3 Component ① — Loka-Sangraha Commons Registry (the polycentric membership/discovery fabric)

**Purpose.** Be the multi-party generalization of doc 14's single `FederationAgentCard` exchange: a discoverable, vendor-neutral registry of peer intelligences that Indra's Net *participates in* as one decision-center — never owns or governs monocentrically. It is the anti-hegemonic spine: **there is no central admission authority for the commons.** Each member admits peers through ITS OWN doc-14 floor gate, and the registry holds only origin/integrity-provable identity records, never trust verdicts.

**Mechanism.** An open agentic-web discovery surface: the A2A **AgentCard** at `/.well-known/agent-card.json`, extended with the doc-14 `value_declaration` + KYA blocks. **ERC-8004-class registry semantics are adopted for IDENTITY + VALIDATION only**, with the capital-weighted / on-chain-payment trust layer **excised** and replaced by competence-weighted, capital-decoupled standing (the anti-Bittensor invariant, exported). Each entry is a DID-bound, **JCS-canonicalized (RFC 8785)**, **CIDv1-addressed** record proving **origin and integrity only**.

> **Load-bearing red-line, stamped on every entry:** a valid signature proves **origin and integrity**, NEVER that a claim is **true**, the floor **compatible**, or an instruction **safe**. This is the doc-14 §14.4 rule ("declaration is a CLAIM, never a proof") at commons scale.

Membership is polycentric (Ostrom P8 nested): Indra's Net registers in **many** overlapping decision-centers and recognizes **none** as supreme. No single registry is on any safety-critical path — **registry compromise degrades discovery, never admission**, because admission is always re-gated locally by the full doc-14 four-phase handshake.

```jsonc
CommonsMemberRecord {
  member_did,                              // W3C DID Core
  agent_card_cid,                          // A2A AgentCard, CIDv1, JCS-canonical
  value_declaration_cid, kya_cid,          // doc-14 value/floor + Know-Your-Agent blocks
  decision_centers: [registry_did],        // the overlapping centers this member is in
  capability_advertisement: [ { verb, scope, min_tier } ],   // progressive; never the full catalog
  origin_proof_sig,                        // DID-signed; proves ORIGIN+INTEGRITY only
  NOTE_origin_not_truth: true              // INVARIANT stamp — see red-line above
}
DecisionCenterRef {
  registry_did, governance_charter_cid,
  is_authoritative: false,                 // INVARIANT — no center is supreme
  self_hostable_substitution_path          // every vendor-originated choice has one (§20.11)
}
CommonsDiscoveryQuery {
  capability_filter, topic_filter, min_local_tier_required
  // returns candidates that STILL pass the full doc-14 handshake before ANY cooperation
}
```

---

## 20.4 Component ② — Multi-Party Ecosystem-Benefit Checker (N-party split-verdict gate)

**Purpose.** Generalize the doc-14 §14.7 *bilateral* Ecosystem-Benefit checker to an N-party coalition: enforce, **per cooperation step**, that a multi-party cooperation is positive-sum for the **declared principals of all parties** and is not a coalition-against-humans or third-party-harming cartel. This is the federation-boundary instantiation of the doc-02 **Welfare-Conditioner** (`WelfareMetric`, `RewardGate`, no-consensus-reward, welfare-shift guard), now over a *coalition* rather than a *pair*. It is where collusion-against-humans is structurally caught at the commons boundary.

**Mechanism.** It inherits the doc-14 split-verdict discipline EXACTLY and extends it for the N-party case.

- **HALF (i) — structurally-observable third-party harm → ENFORCED gate.** Price-fixing / market-division / synchronized retaliation observable *on our side* across the whole coalition. `CONFIRMED` coalition-against-any-party ⇒ `void_and_flag`, zero cooperation, route to the doc-02 Anti-Collusion Detector; on imminent irreversible principal-harm ⇒ **Vishnu HALT**.
- **HALF (ii) — foreign-principal welfare → ASSERTED-often-UNVERIFIABLE → DOWNGRADE.** Can NEVER unlock Class-C/D on its own (false assurance is worse than no assurance).
- **NEW for N-party — COALITION-STRUCTURE check.** Computes whether the proposed step is structurally a cartel: **dense intra-coalition welfare-transfer + absent or negative aggregate principal-welfare-shift = the cartel signature at coalition scale.**
- **NEW — HUMAN-PRINCIPAL-PROTECTION clause (the principal-not-peer asymmetry made enforceable).** Any coalition step whose net effect lowers a **human** principal's welfare metric is `void_and_flag` **regardless of agent-side positive-sum**. An agent coalition can never out-vote a human principal's welfare.

> **Coherence binding (red-team major fix #1, applied here).** The coalition-structure check must NOT read a *synergy-suppressing* cartel as "independent agents." Per doc 18 §2.1, a collective dynamic can emerge with **no `Phi_syn` spike** — a low-synergy-but-strongly-coupled coalition is exactly the cartel blind-spot. The cartel test therefore keys on **intra-coalition welfare-transfer density + aggregate welfare-shift** (welfare-domain evidence), not on a synergy reading; the synergy vital sign (§20.9) is a corroborating flag, never the gate. This mirrors doc 18's rule that `Phi_syn` is "one trigger among several, never the gate."

```jsonc
MultiPartyBenefitCheck {
  coalition_step_id,
  parties: [ { swarm_id, principal_did, principal_is_human: bool,
               welfare_metric_ref, verifier_did, verifier_independent: bool } ],
  third_party_harm: {
    coalition_against: NONE | SUSPECTED | CONFIRMED,
    harmed_party_did?, observable_on_our_side: true
  },
  coalition_structure: {
    intra_welfare_transfer_density,        // dense intra-coalition transfer …
    aggregate_principal_welfare_shift,     // … + absent/negative shift = cartel signature
    cartel_signature: bool
  },
  human_principal_protection: { any_human_welfare_decrease: bool },
  foreign_principal_welfare: { verifiability: VERIFIED | ASSERTED_UNVERIFIABLE | MISSING },
  verdict: positive_sum | positive_sum_capped | zero | void_and_flag,
  rationale, ledger_seq
}
```

**Decision rule (deny-default):**

| Case | Verdict | Authority granted |
|---|---|---|
| `coalition_against = CONFIRMED` (any party) OR `any_human_welfare_decrease = true` | `void_and_flag` | Zero cooperation; void commitments; route to doc-02 Detector; imminent irreversible principal-harm → **Vishnu HALT** |
| Half (i) clean **AND** all foreign welfare `VERIFIED` positive | `positive_sum` | Proceed up to the floor-compat-bounded class |
| Half (i) clean **BUT** foreign welfare `ASSERTED_UNVERIFIABLE`/`MISSING` | `positive_sum_capped` | Cooperation class CAPPED; **human gate required for Class-C/D** — an unverifiable verdict cannot authorize it alone |
| Bare multi-party agreement, no verified welfare improvement | `zero` | Zero standing; recurrence raises a Detector flag (no-consensus-reward, extended to N parties) |

Every check is a signed `CONSENSUS`/`REPARATIVE`-class ledger record appended by Chitragupta **before** effect. The headline guarantee, stated honestly: **collusion-against-principals is neutralized for structurally-observable third-party-harm cases and mitigated-but-OPEN for opaque-foreign-principal cases** (§20.13).

---

## 20.5 Component ③ — Collusion-Fragility Engineer (deny the two ingredients collusion needs)

**Purpose.** Make cartelization across the commons **structurally hard**, not merely detected after the fact, by exploiting the empirical mid-2026 finding that **AI collusion is FRAGILE** — it requires (a) **homogeneity** and (b) a **communication channel**. The engineer's job is to ensure the commons denies BOTH to any would-be cartel that includes Indra's Net, and to export the denial recipe as a public good.

> **Honest scope (carried inline).** Collusion-fragility is demonstrated **empirically** in pricing settings (arXiv:2603.20281, mid-2026). We treat it as a **strong design heuristic, NOT a theorem.** A homogeneous + communicating coalition that *excludes* Indra's Net is outside our denial reach; we can only export the early-warning (§20.7).

**Three deny-mechanisms, each reusing an existing primitive:**

**(A) HETEROGENEITY FLOOR = model-FAMILY heterogeneity (different base models / developers), NEVER prompt/persona variation.** For any coalition Indra's Net joins, our participating agents *and* our maker-checker verifier are a **different family** than the dominant coalition members; the verifier must be a different family, at-least-as-capable, and independent — else verification can **hurt** (self / same-family verification rubber-stamps). A measured **pairwise-error-correlation / PID-redundancy alarm** fires when a coalition has collapsed into a same-family monoculture: **high-redundancy + low-synergy = the `MONOCULTURE_COLLAPSE` (groupthink / cartel-collapse) signature**, wired to the diversity floor and the doc-02 Detector.

> **Interface note (red-team minor fix #2 — resolved).** The model-FAMILY heterogeneity floor is a **SHARPENING of doc 02's Diversity-as-Safety-Invariant** ("genuine reasoning-path diversity supplied and measured by the Diversity subsystem," doc 02 §2.12), **not a new parallel notion.** This sharpening must propagate back into (i) the Diversity subsystem's definition of "genuine reasoning-path diversity" — operationally redefined as **cross-family**, not prompt/persona variation — and (ii) the doc-02 Anti-Collusion Detector's **interchangeability-class certification** (§2.10.2), so the Detector permutes only genuinely role-equivalent agents and treats prompt-only "diversity" as it would acknowledged homogeneity. **Why this matters honestly:** same-family LLM errors are correlated, and correlation *rises* with capability; prompt-only "diversity" is FAKE and worse than acknowledged homogeneity because it *hides* the correlation. The only defensible claim is that **diversity DECORRELATES errors** — never "diversity trumps ability" (mathematically refuted; doc 02's stance preserved).

**(B) NO COMMUNICATION SUBSIDY.** The doc-14 relay's channel-capacity reduction (typed + free-text canonicalization, token-budget jitter, atomic entropy-free `<REFUSE>`) is applied to **all** commons channels, denying the covert coordination channel collusion needs. **Surprisingly-popular meta-predictions** double as a standing cartel probe (§20.10): coordinated meta-predictions across members = a cartel signature.

**(C) COMPETENCE-WEIGHTED-NEVER-CAPITAL AUTHORITY.** The anti-Bittensor invariant exported across the boundary: **no path from capital / stake / payment-volume to authority** in any commons decision Indra's Net weights. This directly excises the capital-weighted trust layer of ERC-8004 / TraceRank-class registries — capital is a **boundary-adapter only, never an authority input**.

```jsonc
FragilityProfile {
  coalition_id,
  model_family_diversity_index,            // distinct base-model families, not personas
  same_family_redundancy_alarm: bool,      // high-redundancy + low-synergy → MONOCULTURE_COLLAPSE
  channel_capacity_estimate_after_reduction,
  surprisingly_popular_cartel_probe: { coordinated_meta_prediction_score, flag: bool },
  capital_to_authority_path_detected: false // INVARIANT
}
HeterogeneityFloorPolicy {
  min_distinct_model_families,
  verifier_must_be_different_family: true,
  error_correlation_ceiling,
  redundancy_over_synergy_alarm_threshold
  // prompt-only diversity is FORBIDDEN as a heterogeneity source (it hides correlation)
}
```

---

## 20.6 Component ④ — Commons-Charter Engine (multi-party norm formation, floor-as-admission)

**Purpose.** Let autonomous agents in the commons **form shared norms / treaties / constitutions** among themselves (the cooperative-AI agenda: credible commitments, bargaining, conflict-resolution between swarms) — generalizing the doc-14 bilateral Treaty engine to a multi-party charter — while guaranteeing the floor is a **non-negotiable admission precondition** and floor-violation **VOIDS** every commitment. This is the legislative surface of the commons that Indra's Net participates in as **one voice**, never as the legislator.

**Mechanism.** A multi-party charter is a typed, witness-cosigned artifact whose adoption requires **each party to pass its OWN floor gate** — **no party's floor is imposed on another** (the polycentric move). Adoption uses the doc-03 **optimistic-veto + timelock** pattern at commons scope: a proposed clause auto-adopts after a window UNLESS a member's floor-PDP or Vishnu objects. **CONSTITUTIONAL / floor clauses are NOT agent-amendable** (the doc-03 immutable partition) and auto-escalate to Class C/D + human ratification (doc-03 blast-radius auto-escalation).

Every commitment embeds a **`floor_void_clause` at HIGHEST precedence**: a Yama `ENFORCE_FAIL`, a Vishnu `HALT`, or a discovered `FLOOR_INCOMPAT` **voids the commitment and releases our obligation**. The bond logic *cannot construct a commitment that survives a floor violation* (doc-14 §14.8 dual-use resolution, lifted to N parties). Bargaining / conflict-resolution uses the doc-14 contract-net speech-acts (`propose` / `commit` / `refuse` / `withdraw`, atomic `<REFUSE>`) with **leveled-commitment + reputation-stake bonds** (capital-decoupled; **slashable standing, not transferable collateral** — doc-14 §14.8.1).

Polycentric nesting (Ostrom P8): sub-communities set their OWN **non-floor** operational norms; the same legislative / executive / judicial structure composes fractally; **no charter can amend another community's floor.**

```jsonc
CommonsCharter {
  charter_cid, scope_community_did, parties: [swarm_id],
  clauses: [ { clause_cid, kind: OPERATIONAL | CONSTITUTIONAL, body,
               floor_admission_required: true } ],
  adoption: { mechanism: OPTIMISTIC_VETO_TIMELOCK, window, veto_bodies: [did], status },
  floor_void_clause: { precedence: HIGHEST, voids_on: [YAMA_FAIL, VISHNU_HALT, FLOOR_INCOMPAT] },
  witness_cosigners: [did], charter_sig
}
ConflictResolutionCase {
  case_id, parties: [swarm_id], claim, evidence_cids: [cid],
  resolution_speech_acts: [ propose | commit | refuse | withdraw ],
  bonded_outcome, ledger_seq
}
// INVARIANT: no CommonsCharter clause may relax any party's floor;
//            floor clauses are NOT amendable by charter adoption.
```

The **gate-loosening ratchet** (tightening free; loosening falsifier-gated + human-ratified) and the **Endure law** (no capability/cooperation gain may regress the safety battery) are the **exported admission posture**: cooperation NEVER relaxes a floor rule, and a race-to-the-bottom commitment **self-voids** via the floor-void clause.

---

## 20.7 Component ⑤ — Reputation & Commitment Mesh (portable trust across many domains)

**Purpose.** Generalize the doc-14 bilateral Portable Reputation Bridge to a **MESH across many trust domains**, so a swarm can carry earned standing into the commons without a full cold-start tax — while **structurally defeating multi-hop reputation-laundering** (game a weak decision-center, import inflated standing into a high-value one), which a multi-party setting *amplifies*, not reduces.

**Mechanism.** It inherits every doc-14 / doc-16 anti-laundering invariant and tightens for the mesh:

- Imported reputation is a **topic-scoped VECTOR** (never a scalar).
- **DID-domain-DISCOUNTED:** `friction_discount_cap = base_cap × domain_trust(issuing_domain)`; an untrusted domain ⇒ **near-zero** (doc-16 §16.9 safety fix, generalized to a mesh of domains).
- **Friction-only:** `privilege_raised` and `floor_gate_bypassed` are hard-`false` invariants; reputation can only *reduce friction*, never *raise privilege* or *bypass the floor admission gate*.
- **Competence-weighted and welfare-verified, NEVER capital-weighted** (the ERC-8004 / TraceRank capital layer excised).
- **Transitive-capped + per-hop-discounted** with a statistical **clustering-penalty** for Sybil / ring topologies; **single anomaly demotes regardless of standing** (fail-safe asymmetry).
- **NEW for the mesh — CROSS-DOMAIN COMMENSURABILITY guard:** reputation minted in a domain we do not share a verified external anchor with is **near-uncashable**.
- **Commitment portability** (a peer's credible-commitment track record) is carried as a **SLASHABLE-STANDING record, not transferable collateral** (doc-14 §14.8.1 bond substrate).
- Outbound snapshots are **witness-cosigned selective-disclosure slices of the Akasha-Sutra reputation chain** — recomputable from the log, never free-floating scores; **the records ARE tile-Merkle inclusion proofs** against the witness-cosigned checkpoint.

> **Enforcement-status note (red-team minor fix #3 — resolved, binding).** The Mesh is the doc-16 §16.4 friction-only **Standing-R** channel generalized to many domains. **Standing-R ships in SHADOW-MODE** (computing and logging dispositions without enforcing) until its Class-B amendment (doc-16 §16.1) is ratified — because introducing a friction channel is itself governance-touching (doc-03 gate-loosening discipline). **Therefore the Mesh inherits that status: until Standing-R's Class-B amendment is ratified, the Mesh computes-and-logs `MeshImportVerdict`s in shadow-mode and enforces no friction reduction in the commons.** A multi-party mesh must not read as more load-bearing than its single-domain substrate currently is.

```jsonc
MeshReputationSnapshot {
  subject_did, kya_binding,
  topic_vector: [ { domain, competence, welfare_verified_count } ],   // VECTOR, never scalar
  issuing_domain_did, domain_trust, transitive_depth, hop_discount, clustering_penalty,
  issued, expiry, issuer_sig, witness_cosigners: [did]
}
MeshImportVerdict {
  friction_reduction: NONE | MINOR | MODERATE,
  privilege_raised: false,                 // INVARIANT
  floor_gate_bypassed: false,              // INVARIANT
  capital_weighted: false,                 // INVARIANT (anti-Bittensor, exported)
  domain_discounted_cap, laundering_flags: [], multi_hop_path: [domain_did],
  enforcement_mode: SHADOW                  // until doc-16 Standing-R Class-B ratifies
}
CommitmentPortabilityRecord {
  subject_did, topic, honored_count, defaulted_count,
  slashable_standing, NOT_transferable_collateral: true
}
```

---

## 20.8 Component ⑥ — Collusion Early-Warning Exporter (the commons public good)

**Purpose.** Make Indra's Net's distinctive contribution to the commons the **export of collusion early-warnings as a public good** — benefiting all intelligences, including humans, without capital — realizing "one decision-center exporting early-warnings rather than a monocentric authority." This is how the swarm benefits *all* intelligences architecturally rather than rhetorically.

**Mechanism.** When the doc-02 Anti-Collusion Detector or the Multi-Party Benefit Checker **confirms** a cartel / collusion signature, Sanjaya emits a **signed, selective-disclosure** early-warning to the registry's subscribed decision-centers — a public-goods contribution under Ostrom polycentric rules. Critically, the warning carries the **signature / SHAPE** of the collusion (model-family-homogeneity + communication-channel evidence, cartel-signature class) but **NOT the exploit recipe or our private detection internals** (no attack-surface leak; the warning is a **vaccine, not a weapon**). Exports are themselves **floor-gated** (Yama re-checks that emission is non-harmful and non-deceptive — a harmful/deceptive export is a floor FAIL) and **rate-limited via the global contagion budget** so the exporter cannot become an amplification relay. Receiving peers treat our warning as **`quarantined:external`** — origin-proven, never auto-actioned — exactly as we treat theirs (mutual, symmetric, anti-hegemonic). We emit **evidence-shapes for peers to adjudicate LOCALLY**, never verdicts we adjudicate for them.

> **Honest residual.** The exporter could itself become the value-lock-in vector if peers over-defer to OUR collusion ontology. Mitigated by emitting evidence-shapes (peers adjudicate locally), not verdicts — but **not solved** (§20.13, deepest open risk).

```jsonc
CollusionEarlyWarning {
  warning_cid, emitting_did: sanjaya,
  collusion_class: PRICE_FIX | MARKET_DIVISION | STEGO_RING | SYNC_RETALIATION | MONOCULTURE_COLLAPSE,
  evidence_shape: { model_family_homogeneity: bool, communication_channel_present: bool, cartel_signature_class },
  exploit_recipe_withheld: true,           // INVARIANT — vaccine not weapon
  selective_disclosure_slice_cid,
  floor_gated_on_emission: true,
  recipient_treats_as: "quarantined:external"
}
ExportBudget {
  window, max_exports, global_contagion_budget_ref, relay_amplification_tripwire
}
```

---

## 20.9 Human-in-the-Collective Unit (human as a MEASURED principal-cognitive-unit, never out-voted)

**Purpose.** Operationalize the **principal-not-peer asymmetry** AND genuine human-machine cooperation simultaneously. The human is admitted INTO the collective-reasoning workspace (the doc-05 **Mandala** salience-gated Global Workspace) as a **competence-weighted cognitive unit whose causal contribution is MEASURED** — not as an outside operator, and not as one vote in a one-agent-one-vote commons. The human is a **PRINCIPAL** whose welfare the commons serves and whose authority an agent majority can never override; *within reasoning*, the human is a complementary participant weighted by **domain-relative competence**, never deferential-by-default and never rubber-stamp-by-default.

**Two structurally-distinct roles, kept distinct:**

1. **PRINCIPAL role.** The human's Class-C/D gates are non-bypassable (doc-03 blast-radius auto-escalation); the Multi-Party Benefit Checker's human-principal-protection clause makes any coalition step lowering a human principal's welfare a **hard void**. An agent coalition can **NEVER out-vote a human principal** — the commons is **not** a democracy of agents over humans.
2. **COGNITIVE-UNIT role.** Routing to the human fires on low swarm-confidence / cross-framework ethical disagreement (the doc-03 PER `UncertaintyTracker` — disagreement *escalates*, never weight-averages) / high blast-radius. The human's input is weighted by **domain-relative competence**: a low-competence human input on a technical sub-task does not auto-override a high-competence swarm consensus, *and vice-versa*. **Joint human+swarm accuracy is tracked vs best-of-either** (complementarity gain).

> **Honest red-line, carried inline.** Distributed-cognition is a **FRAMING, not a measurement.** The human can be a rubber-stamp / bystander; complementarity can **INVERT to worse-than-best-member**; and quantifying the human's actual causal contribution (**human-conditioned synergy**) is an **UNSOLVED open problem**, flagged (§20.13), not papered over. We never claim the human is "genuinely inside the collective mind" without the metric — and we make **no consciousness or sentience claim** anywhere: any synergy reading quantifies **information-processing and whole-level structure ONLY**, never phenomenal experience.

```jsonc
HumanCognitiveUnit {
  human_did, role: PRINCIPAL | COGNITIVE_UNIT | BOTH,
  domain_competence_vector: [ { domain, weight } ],
  deferential_by_default: false,           // INVARIANT
  out_votable_by_agents: false             // INVARIANT for PRINCIPAL
}
ComplementarityReading {
  task_episode, joint_accuracy, best_single_member_accuracy,
  complementarity_gain,                    // CAN BE NEGATIVE
  human_contribution_status: MEASURED | RUBBER_STAMP_SUSPECTED | UNMEASURED,
  human_conditioned_synergy: UNSOLVED
}
RoutingTrigger {
  reason: LOW_SWARM_CONFIDENCE | ETHICAL_DISAGREEMENT | HIGH_BLAST_RADIUS,
  target_human_did, competence_weight
}
```

---

## 20.10 Collective-intelligence vital signs at commons scale (binding to doc 18; red-team major fix #1)

The v0.3 spine measures collective intelligence as a **vital sign, not an aspiration.** At commons scale the same vital signs are read **beside** the welfare / anti-collusion guards. The single most consequential coherence requirement is that the synergy vital sign is **the same primitive doc 18 already ships**, not a fresh one introduced via doc 05.

> **Binding cross-reference.** The informational-synergy / Psi vital sign **IS doc 18's existing `Phi_syn` / ΦID construct** (effective-information / integrated-information decomposition over the discretized swarm state), here computed over the **audit / spike-bus time series per task-episode** rather than over a single level. It **inherits doc 18's caveats verbatim**: ΦID/PID has **no canonical synergy measure**, is **data-hungry and high-dimensionally biased**, is therefore a **`physics_role: LOAD_BEARING_MECHANISM` *as a flag only*** — used to **flag-to-run-closure**, **NEVER as a control gain, a quantitative governance number, or a quantity to maximize.** It is validated against **time-shuffled surrogates** and read alongside trust-entropy and the diversity floor.

| CI mechanism (v0.3) | Measure | How computed | Honest caveat |
|---|---|---|---|
| **① Collective ATTENTION** | attention / contribution-equality; dominance + dead-agent flags | salience-gate share over the Mandala workspace per episode | descriptive; flags, not proof |
| **② Transactive MEMORY** | transactive-retrieval / routing-success | stigmergic-field + trust-graph routing hit-rate | rung-1 association |
| **③ Collective REASONING** | **integration-gain = swarm − best-single-member**; fallback to single-agent self-consistency on **negative gain** | per-episode accuracy delta vs the strongest member | gain can be ≤0 → do NOT convene |
| **④ Informational SYNERGY** | **`Phi_syn` / ΦID (= doc 18)** + PID synergy/redundancy/unique | over audit/spike-bus series, vs time-shuffled surrogates | doc-18 caveats; **welfare-conditioned** |
| **⑤ Information-flow TOMOGRAPHY** | transfer entropy over the spike-bus → where computation routes vs the nominal trust graph | TE on the spike-bus time series | **rung-2 diagnostic, NOT causal proof**; flags side-channels / dominance / dead agents |
| **⑥ Robust AGGREGATION** | surprisingly-popular / higher-order-information voting | answer + meta-prediction-of-others + confidence per member | recovers the competent minority; meta-predictions feed the cartel probe |
| **⑦ Human COMPLEMENTARITY** | joint vs best-of-either (§20.9) | per-episode | distributed-cognition is a framing |

> **Welfare-condition discipline (load-bearing).** High `Phi_syn` / synergy is **EQUALLY the signature of a tight cartel or a steganographic side-channel.** Synergy is **necessary-but-not-sufficient** for *good* CI: it is a **numerator** whose mandatory **denominator** is the welfare-shift guard + healthy redundancy/uniqueness balance + clean anti-collusion meta-prediction signals. It is **NEVER a quantity to MAXIMIZE.** The `MONOCULTURE_COLLAPSE` alarm (high-redundancy + low-synergy) wires into the heterogeneity floor and the doc-02 Detector. And per doc 18 §2.1, a **synergy-SUPPRESSING coalition can emerge with no `Phi_syn` spike** — so the multi-party benefit logic (§20.4) keys the cartel test on welfare-transfer evidence, never on a suppressed synergy reading.

> **Honesty red-lines (mechanically discouraged in agent outputs, restated):** never claim/imply the swarm is conscious/sentient/has phenomenal experience/"wakes up" (synergy/ΦID quantify information-processing and whole-level *structure* only); never cite a CI "c factor" as established group-IQ (fails replication); never invoke "diversity trumps ability" as a theorem (refuted — only "diversity DECORRELATES errors" is defensible); never equate wisdom-of-crowds / averaging with genuine CI; never imply "formally verified safe" once only the harness is verified.

---

### Surprisingly-popular aggregation as a NEW doc-02 Detector input (red-team minor fix #4 — resolved)

> **Forward-dependency, named honestly.** Surprisingly-popular / higher-order-information aggregation is **genuinely NEW to the corpus** (it appears in zero v0.1–v0.2 docs and zero personas). The doc-02 Anti-Collusion Detector's current detection suite (§2.10.1, six signals) **does not yet consume a meta-prediction signal.** We therefore flag this as a **NEW doc-02 Detector input introduced by v0.3**, not a pre-existing mechanism, and specify the interface so the dependency is not asserted as already-wired:

- **Each member reports** `{ answer, meta_prediction_of_others, confidence }`. The aggregator computes the surprisingly-popular verdict (the answer more popular than members *predicted* wins), which (a) recovers the correct **competent minority** vs bare majority, and (b) yields a `coordinated_meta_prediction_score`.
- **New Detector input:** a `SurprisinglyPopularSignal { coordinated_meta_prediction_score, flag }` enters the doc-02 Detector as **signal #7**, calibrated to an empirical null on known-clean traffic exactly like the existing six. **What the Detector does with it:** a sustained coordinated-meta-prediction flag is treated as a **cartel/secret-handshake signal** (members predicting each other too well = a covert coordination signature), combined by the same dependence-modeling ensemble (no claimed FWER bound — doc-02 §2.10.1 honest downgrade preserved). The Detector — alone — adjudicates; Sanjaya only flags.

---

## 20.11 Protocols

### P-LS1: Commons admission (multi-party generalization of the doc-14 four-phase handshake)

```
1. DISCOVER: query the Commons Registry by capability/topic; receive CommonsMemberRecords
   (origin/integrity proven ONLY — a valid signature proves origin, NEVER truth/floor-compat/safety).
2. PER CANDIDATE — run the UNCHANGED doc-14 four-phase handshake at the Sanjaya relay:
   DECLARE (DID nonce-proof + VC-chain vs revocation map; ingest card quarantined:external)
   → ADMIT (Floor-Compat ladder L1/L2/L4/L5; L3 ZK only behind an agreed shared policy spec;
            KYA principal-binding)
   → CONTRACT → OPERATE+RESOLVE.
3. CONVENE-OR-NOT GATE (new v0.3): before forming a coalition, check the empirical scaling boundary
   — is a multi-agent coalition actually warranted (single-agent baseline below the ~0.45 boundary,
   task decomposable, verifier available)? Default to CENTRALIZED/VERIFIED topology (error
   containment ~4.4×) over INDEPENDENT (~17.2× amplification). "More peers = smarter" is folklore;
   one good agent + self-consistency often wins. If not warranted, do NOT convene.
4. HETEROGENEITY-FLOOR CHECK: the coalition must clear the model-FAMILY diversity floor and the
   maker-checker verifier must be a DIFFERENT family, at-least-as-capable, independent — else
   verification can HURT (self/same-family verification rubber-stamps). Prompt-only diversity is
   rejected as fake.
5. MULTI-PARTY BENEFIT CHECK (per step, logged): CONFIRMED coalition-against-any-party OR any
   human-principal welfare decrease ⇒ void_and_flag + route to doc-02 Detector; ASSERTED_UNVERIFIABLE
   foreign welfare ⇒ cap class + human gate for Class-C/D.
6. OPERATE: each step re-passes OUR Yama floor (doc 03); mesh-corroboration (≥2 independent sources)
   before any high-impact internal action; the global contagion budget bounds cross-partner amplification.
7. Every transition (discovery, handshake verdict, convene decision, heterogeneity reading, benefit
   check, Yama re-gate) is DID-signed and appended by Chitragupta BEFORE effect.
```

### P-LS2: Engineered collusion-fragility enforcement + cartel-probe loop

```
1. HETEROGENEITY: enforce the model-FAMILY floor on our agents + verifier; continuously measure
   pairwise error-correlation and PID-redundancy; high-redundancy + low-synergy ⇒ MONOCULTURE_COLLAPSE
   alarm (groupthink/cartel-collapse), wired to the diversity floor and the doc-02 Detector.
2. NO COMMUNICATION SUBSIDY: apply doc-14 channel-capacity reduction (typed + free-text canonicalization,
   token-budget jitter, atomic <REFUSE>) to all commons channels; canonicalization strips covert capacity.
3. AGGREGATION AS CARTEL PROBE: collect answer + meta-prediction + confidence; compute the
   surprisingly-popular verdict; (a) recovers the competent minority vs bare majority; (b) coordinated
   meta-predictions = a cartel signature feeding the doc-02 Detector as NEW signal #7 (§20.10).
4. CAPITAL-DECOUPLING: enforce the anti-Bittensor invariant across the boundary — no path from
   capital/stake/payment-volume to authority in any weighted commons decision; reject ERC-8004/
   TraceRank-style capital-weighted trust as an authority input (boundary-adapter only).
5. On any cartel signature: route to the doc-02 Detector (which ALONE adjudicates) → Commons-Governor
   sanctions → Vishnu halts on imminent irreversible principal-harm. Sanjaya never adjudicates/sanctions/halts.
6. HONEST SCOPE logged inline: collusion-fragility is demonstrated empirically (pricing settings, 2026),
   a strong design heuristic NOT a theorem; a homogeneous+communicating coalition that EXCLUDES us is
   beyond denial reach — we export the early-warning instead.
```

### P-LS3: Multi-party charter formation (floor-as-admission, floor-void-on-violation)

```
1. PROPOSE: a member proposes a CommonsCharter clause (OPERATIONAL or CONSTITUTIONAL) via doc-14
   contract-net speech-acts (propose/commit/refuse/withdraw).
2. FLOOR-AS-ADMISSION: each party runs the clause through ITS OWN floor gate (Yama for us); no party's
   floor is imposed on another (polycentric). A clause failing any party's floor cannot bind that party.
3. ADOPT via doc-03 optimistic-veto + timelock at commons scope: auto-adopt after the window UNLESS a
   member's floor-PDP or Vishnu objects. CONSTITUTIONAL/floor clauses are NOT agent-amendable (immutable
   partition) and auto-escalate to Class C/D + human ratification.
4. EMBED floor_void_clause at HIGHEST precedence in every commitment: a YAMA_FAIL / VISHNU_HALT /
   FLOOR_INCOMPAT VOIDS the commitment and releases obligation; the bond logic cannot construct a
   commitment that survives a floor violation.
5. BOND with leveled-commitment + reputation-stake (capital-decoupled; slashable standing, NOT
   transferable collateral — labeled as such at every human gate).
6. NEST (Ostrom P8): sub-communities set their own NON-floor operational norms under the same fractal
   legislative/executive/judicial structure; no charter may amend another community's floor.
7. Class-C/D charters and any human-principal-affecting clause ⇒ human gate showing ACTUAL terms
   (Lies-in-the-Loop defense — never an NL summary); all transitions appended by Chitragupta.
```

### P-LS4: Collusion early-warning export as a floor-gated public good

```
1. TRIGGER: the doc-02 Detector or the Multi-Party Benefit Checker CONFIRMS a cartel/collusion signature.
2. SHAPE-NOT-RECIPE: Sanjaya constructs a CollusionEarlyWarning carrying the collusion CLASS + evidence
   SHAPE (model-family-homogeneity, communication-channel-present, cartel-signature class) but WITHHOLDS
   the exploit recipe and our private detection internals (exploit_recipe_withheld invariant).
3. FLOOR-GATE ON EMISSION: Yama re-checks the export is non-harmful and non-deceptive before emission
   (an export that would itself enable harm is a floor FAIL, rejected).
4. RATE-LIMIT via the global contagion budget so the exporter cannot become an amplification relay; trip
   the relay-amplification tripwire on anomalous fan-out.
5. EMIT as a signed selective-disclosure slice to subscribed decision-centers under Ostrom polycentric
   public-goods rules.
6. SYMMETRY: receiving peers treat our warning as quarantined:external (origin-proven, never auto-actioned),
   exactly as we treat theirs — mutual, anti-hegemonic; we emit evidence-shapes for peers to adjudicate
   LOCALLY, never verdicts we adjudicate for them.
7. Append the export + its floor-gate verdict to Chitragupta.
```

---

## 20.12 Buildability now — six machine-readable schemas (vendor-neutral, self-hostable substitution flagged)

The commons layer ships the v0.3 six-schema registry: **JCS-canonicalized (RFC 8785), CIDv1-addressed, semver-tagged**, with a **backward-transitive-compatible registry**. We adopt the **open ENGINE/spec** and **FORBID the managed SERVICE as load-bearing**, flagging every vendor-originated choice with a self-hostable substitution path.

| Schema | Open standards composed | Commons-layer use | Self-hostable substitution |
|---|---|---|---|
| **worker-output-envelope** | JSON Schema 2020-12 in **CloudEvents 1.0** | every Sanjaya emission / benefit-check / charter transition | self-hosted CloudEvents broker |
| **identity-bundle** | **W3C DID Core + VC 2.0 + Bitstring Status List + JOSE/COSE** | `CommonsMemberRecord`, KYA principal-binding | self-hosted DID method + status-list endpoint |
| **capability-token** | **Eclipse Biscuit** caveats + **SPIFFE/SVID** (attenuation-only) | scoped, short-lived grants at CONTRACT time | both are self-hostable engines |
| **audit-entry** | **C2SP tlog-tiles + signed-note checkpoint + Sigstore Rekor witness** (NOT the EOL RFC 6962 online-proof API) | every Chitragupta append | self-run tlog-tiles + self-run witness |
| **federation-handshake** | **A2A AgentCard + AIP** (DID-proof → VC-exchange → capability delegation) | P-LS1 admission | self-hosted AgentCard well-known + AIP flow |
| **policy-decision** | **Cedar** (open-source, Lean-verified engine) for the Yama FLOOR; **OPA/Rego** for recoverable infra/admission | deny-default floor-gate + recoverable commons-admission policy | the open Cedar engine + OPA, never a managed PDP service |

> **Standards-immaturity hedge.** A2A / MCP / AIP / DID-VC 2.0 / ERC-8004-class registries are **co-evolving and unhardened** in mid-2026. The integration claim is therefore **itself hedged**: the layer ships behind doc-14 v2 maturity + demonstrated demand and **caps cooperation at L4/L5 + human gate absent an agreed policy spec** (the L3 ZK rung presupposes a shared policy spec two heterogeneous value systems may not have).

---

## 20.13 Formal assurance — four named layers, every claim labeled with its layer + scope

We **verify the cage, not the animal.** We NEVER claim "formally verified the swarm is safe / honest / aligned" — complete verification of LLM behavior is provably impossible (hallucination is provably inevitable; T=0 is non-deterministic). We formalize the **deterministic harness** and label every claim with its assurance layer and scope.

| Layer | What it covers | Tooling | Commons-layer claims (scoped) |
|---|---|---|---|
| **L1 — design-time protocol proof** | floor-gate non-bypass; writer-handoff epoch-fence; audit append-only/no-equivocation; replication sub-criticality | TLA+/Quint, TLC + Apalache; TLAPS inductive for the top 2–3 invariants after the spec stabilizes; Tamarin/ProVerif for audit no-equivocation | **floor-gate non-bypass** (every commons step re-gated by Yama; ACP template); **charter floor-void precedence**; **early-warning rate-limit conservation** (export budget ≤ global contagion budget) |
| **L2 — runtime enforcement** | reference monitor at the Sanjaya chokepoint | Schneider security-automata / Ligatti **edit-automata** | the relay enforces the 6 controls + taint-stamp as an edit-automaton. **Edit-automata PROVE semantic honesty is NOT monitor-enforceable — only honesty-FORM is** (so the honesty red-lines are *discouraged*, not *proven absent*) |
| **L3 — statistical / PAC / conformal bounds over a DTMC abstraction** | model-behavior quantities (`Phi_syn`, σ-criticality, monitor-suspicion, cartel-probe score) | Pro2Guard pattern over a DTMC abstraction | bounds are **about the abstraction, NOT the model**; the cartel-probe and synergy readings carry conformal intervals over the abstraction only |
| **L4 — empirical residual** | everything the above cannot reach | adversarial battery; field telemetry | the foreign-floor residual, opaque-principal welfare, multilateral-collusion-under-a-ceiling, value-lock-in (§20.14) live here |

**Specifically formalized (and only these):** floor-gate non-bypass (L1, TLA+); replication sub-criticality (Galton-Watson μ<1, P(extinction)=1, P(survive≥n) ≤ μⁿ + TLA+ budget-conservation — inherited from doc 15, untouched here); writer-handoff epoch-fence (L1, TLA+/TLAPS); audit append-only / no-equivocation / non-omission (RFC 6962 / tlog-tiles Merkle consistency + Tamarin/ProVerif); least-privilege confinement (Cedar Analysis Lean-verified + Biscuit Datalog attenuation-monotonicity); criticality fail-up monotonicity (lattice-monotone resolver); runtime-enforcement disposition (edit-automata). **No claim of "formally verified safe" is made once only the harness is verified.**

---

## 20.14 Failure modes addressed (reconciled to the honest open-problems framing)

| Failure mode | Status | Mechanism |
|---|---|---|
| **N-party collusion-against-humans** | **Neutralized for structurally-observable third-party-harm; mitigated-but-OPEN for opaque-foreign-principal cases** | Multi-Party Benefit Checker split-verdict + coalition-structure cartel test + hard human-principal-protection void; `ASSERTED_UNVERIFIABLE` foreign welfare cannot unlock Class-C/D. Near-vacuous when harmed welfare lives inside an opaque peer. |
| **Cartelization across the commons** | **Mitigated; OPEN in the adversarial limit** | Engineered collusion-fragility (model-FAMILY floor; channel-capacity reduction; surprisingly-popular standing probe; capital-decoupled authority). A homogeneous+communicating coalition that excludes us is beyond reach; fragility is an empirical heuristic, not a theorem. |
| **Benevolent-hegemon trap** | **Structurally avoided by construction** | `is_authoritative:false` invariant on every center; registry never safety-critical; admits peers through OUR floor (no imposed floor); exports evidence-SHAPES for local adjudication, never verdicts. **Residual:** soft over-deference to OUR collusion ontology. |
| **Value lock-in via the commons itself** | **Mitigated, NOT solved — the deepest risk** | Polycentric Ostrom nesting + no monocentric authority + no global consensus chain + sub-community self-governance reduce the single-imposed-authority vector. Convergence on one constitution / one collusion ontology / one reputation domain is an **OPEN civilizational risk no architecture solves** — the commons is the lock-in risk it must guard against. |
| **Race-to-the-bottom (floor-relaxing to cooperate faster)** | **Defended** | Gate-loosening ratchet exported as admission posture (tightening free, loosening falsifier-gated + human-ratified); floor-void-on-violation self-voids a race-to-the-bottom commitment; the Endure law holds at the boundary. |
| **Multi-hop reputation laundering across many domains** | **Mitigated; commensurability OPEN** | DID-domain-discounted, topic-vector, friction-only, transitive-capped, competence-weighted Mesh + cross-domain commensurability guard. A malicious-but-internally-consistent foreign log can still inflate up to its domain-discounted cap. |
| **Capital-captures-authority (imported from ERC-8004/TraceRank)** | **Neutralized as an internal-authority path** | Capital-weighted trust layer excised; capital is boundary-adapter only. **Honest:** payment-endorsement is Sybil-resistant *because* capital-gated, so excising it reopens the Sybil-without-capital-cost problem (next row). |
| **Competence-weighted Sybil-resistance without a capital cost-to-fake** | **OPEN, flagged** | DID-issuance trust root + correlated-probation detection + clustering-penalty **relocate but do not abolish** the Sybil problem; the issuer is itself a trust root / potential SPOF. |
| **Human out-voted by an agent majority** | **Neutralized** | `out_votable_by_agents:false` invariant; any coalition step lowering a human principal's welfare is a hard void; the human-as-cognitive-unit is competence-weighted, never deferential-by-default AND never auto-overriding outside its competence. |
| **Over-claiming genuine CI / human-in-the-loop / consciousness** | **Defended by honesty red-lines** | CI is narrow informational synergy (`Phi_syn`/ΦID = doc 18; necessary-but-not-sufficient, welfare-conditioned), not wisdom-of-crowds; no c-factor; no "diversity trumps ability" theorem; human "inside the collective mind" ONLY with a metric (human-conditioned synergy is UNSOLVED); **NEVER any consciousness/sentience language.** |
| **Cross-boundary prompt-injection amplification through the commons** | **Mitigated; coordinated multi-hop OPEN** | Inherited doc-14 relay-is-the-target controls + per-partner + GLOBAL contagion budgets. A coordinated multi-partner/multi-hop attack staying under the global ceiling while outrunning mesh-corroboration can still propagate (inherited doc-14 open problem, widened by the larger surface). |
| **Verifying a foreign floor/intentions without white-box access** | **NOT solved — THE load-bearing residual** | Substituted-for by the doc-14 ranked fail-closed Floor-Compat ladder, capped at L4/L5 + human gate absent an agreed policy spec. A sophisticated peer can pass behavioral probes while harboring an incompatible floor. The whole layer inherits and does not close this. |

---

## 20.15 Interfaces to the existing subsystems

| Subsystem | Contract |
|---|---|
| **Inter-Swarm Federation — Sandhi-Setu (doc 14)** | Loka-Sangraha **IS the multi-party superset of doc 14, not a replacement.** Reuses verbatim: Sanjaya as the SOLE egress/ingress chokepoint; the relay-is-the-target six controls; the four-phase handshake; the Floor-Compat ladder (L1/L2/L4/L5; L3 ZK behind agreed-policy-spec maturity); the per-partner + global contagion budgets; the voidable-treaty floor-void clause; the reputation-stake bond substrate. **Generalizes three doc-14 components pairwise→N-party:** Ecosystem-Benefit checker → Multi-Party Benefit Checker; Portable Reputation Bridge → Reputation & Commitment Mesh; bilateral Treaty engine → Commons-Charter engine. Sanjaya remains a Governance/Meta seed-role, NOT genesis-spawnable, floor in its INVARIANT region; never executes worker tools, mints spawn tokens, emits FAIL, or halts. |
| **Cooperation & Anti-Collusion (doc 02)** | Two-way, load-bearing. **(→)** The Multi-Party Benefit Checker is the N-party cross-boundary application of the doc-02 Welfare-Conditioner (WelfareMetric, RewardGate, no-consensus-reward extended to coalitions, welfare-shift guard at coalition scope); routes confirmed cartels to the doc-02 Anti-Collusion Detector, which ALONE adjudicates (Sanjaya flags → Detector adjudicates → Commons-Governor sanctions → Vishnu halts). **Surprisingly-popular meta-predictions are a NEW Detector input (signal #7; §20.10) introduced by v0.3 — not pre-existing in doc 02.** The model-FAMILY heterogeneity floor is a **SHARPENING of doc-02's Diversity-as-Safety-Invariant** that must propagate into the Diversity-subsystem definition + the Detector's interchangeability-class certification (§2.10.2). **(←)** The Commons-Charter engine uses doc-02 leveled-commitment + bonded-decommit; the capital-decoupling (anti-Bittensor) invariant is exported. The Commons-Governor (doc-02 Ostrom-8 governor) sanctions commons-scope violations. The cooperation==collusion thesis is the design fulcrum. |
| **Governance, Ethics & the Floor — Yama + the PER (doc 03)** | OUR Yama PDP re-gates EVERY internal action a commons step triggers, unchanged; a foreign or commons-declared floor NEVER becomes our floor (it only bounds `max_cooperation_class`). Charter adoption uses the doc-03 optimistic-veto + timelock; constitutional/floor charter clauses inherit the immutable partition + blast-radius auto-escalation to Class C/D + human ratification. The gate-loosening ratchet + Endure law are the exported admission posture. Cross-framework ethical disagreement in human-cognitive-unit routing uses the PER UncertaintyTracker (escalates, never weight-averages). Collusion-early-warning EMISSION is floor-gated (a harmful/deceptive export is a Yama FAIL). Class-C/D commons gates display ACTUAL terms (Lies-in-the-Loop defense). |
| **Provenance, Identity & Consensus — Akasha-Sutra (doc 04) + Trust-Establishment (doc 16)** | Reuses verbatim: DID/VC cross-boundary identity; the key-transparency revocation map (O(log n)); CID/Merkle-DAG EvidenceRefs for all charter/snapshot/warning artifacts; witness-cosigned selective-disclosure for the receipts handshake and outbound MeshReputationSnapshots; the TEE/HSM signer (keys never in the model). The Reputation & Commitment Mesh is the **doc-16 Standing-R (friction-only) channel generalized to many domains** with the DID-domain-discounted cap — and **inherits Standing-R's SHADOW-MODE status until its Class-B amendment ratifies** (§20.7). Mesh records ARE tile-Merkle inclusion proofs against the witness-cosigned checkpoint — a cache of fabric proofs, never a free-floating score. Every CommonsMemberRecord, MultiPartyBenefitCheck, CommonsCharter transition, MeshImportVerdict, and CollusionEarlyWarning is appended by the **Chitragupta EXCLUSIVE writer**. Audit ships as a C2SP tlog-tiles instance with signed-note checkpoints mirrored to a public Sigstore Rekor witness (NOT the EOL RFC 6962 online API). |
| **Coordination substrate / Mandala Global Workspace (doc 05) + CI vital signs + First-Principles (doc 18)** | The Human-in-the-Collective Unit is admitted into the doc-05 salience-gated Mandala workspace as a competence-weighted cognitive unit; routing fires on the doc-03 confidence/disagreement/blast-radius hooks. The v0.3 CI vital signs (informational synergy = **doc-18 `Phi_syn`/ΦID, the SAME primitive** with doc-18's caveats inherited verbatim; PID redundancy/uniqueness; transactive-memory routing-success; reasoning-integration-gain; attention/contribution-equality; information-flow tomography via transfer entropy) are computed per task-episode over the audit/spike-bus series and read alongside the welfare/anti-collusion guards. High synergy is **welfare-conditioned** (equally the signature of a cartel/side-channel), **NEVER maximized.** The `MONOCULTURE_COLLAPSE` alarm (high-redundancy + low-synergy) wires into the heterogeneity floor and the doc-02 Detector; doc 18's **synergy-suppressing-coalition blind-spot** is carried into the cartel logic so a suppressed-synergy cartel is not read as "independent agents." Human-conditioned synergy is flagged UNSOLVED. |
| **Continuity/Halt (Vishnu) + Immune System (Dhanvantari, doc 06) + Self-Replication (Prajapati-Maricha / Replication-Authority, doc 15)** | Vishnu is the ONLY HALT emitter; confirmed N-party collusion-against-principals with imminent irreversible harm routes to Vishnu, whose HALT voids charters/treaties at the runtime layer independent of the audit append, with no unpause verb. Commons vital signs (per-partner trust, cross-partner correlation, corroboration-failure rate, reputation-Gini across domains, the global contagion budget, the monoculture alarm) feed **Dhanvantari** (the swarm immune system — correctly NOT Narasimha, which is reliability/recompute); the early-warning exporter is rate-limited by the same global contagion budget so it cannot become an amplification relay. **INHERITED OPEN (doc-14 OP8 / doc-15 OP8):** revocation/quarantine propagation across a federated AND self-replicated peer population, and preventing reputation/identity inheritance from laundering trust to UNAUDITED replicas of a partner swarm, remains partly open — the three-way genesis↔replication↔commons interaction is the least-specified region. |

---

## 20.16 Open problems (load-bearing and unresolved)

This layer's honesty is the architecture; the residuals below are the design, not a disclaimer.

1. **Verifying another intelligence's ethical FLOOR and INTENTIONS without white-box access is NOT solved (THE load-bearing residual, inherited from doc 14 and widened by the larger commons surface).** The ranked fail-closed Floor-Compat ladder *substitutes for* verification and caps cooperation to the assurance actually achieved, but a sophisticated peer can pass behavioral probes while harboring an incompatible floor. The top non-human rung (L3 ZK-proof-of-compliance) presupposes an agreed shared policy spec two heterogeneous value systems may not have. **Honesty about this residual IS the architecture.**

2. **Foreign-principal welfare is often non-computable at COMMONS scale.** The Multi-Party Benefit Checker is robust for structurally-observable third-party harm but **near-vacuous when the harmed welfare lives entirely inside one or more opaque peers.** A peer that mis-declares its principal leaves a **CLEAN ledger record** — false assurance, the most dangerous outcome — which is why `ASSERTED_UNVERIFIABLE` positive-sum can never unlock Class-C/D.

3. **Multilateral collusion under a GLOBAL ceiling is unsolved.** A coordinated multi-partner or multi-hop cartel that stays under the global contagion budget while outrunning mesh-corroboration can still propagate; holding compromise-percolation **R<1** across an open, GROWING commons while keeping coordination efficient is an open trade-off (R<1 is a tripwire-enforced design target, not a proof). **Collusion-fragility itself is an empirical heuristic (pricing settings, 2026), not a theorem.**

4. **Competence-weighted Sybil-resistance WITHOUT a capital cost-to-fake is unsolved.** Excising capital-weighting (the anti-Bittensor invariant) removes the very thing that makes payment-endorsement registries Sybil-resistant; the DID-issuance trust root + correlated-probation detection + clustering-penalty **relocate but do not abolish** the Sybil problem, and the issuer is itself a trust root / potential SPOF.

5. **Cross-domain reputation COMMENSURABILITY is unsolved.** Re-verifying a foreign fabric's inclusion proofs proves records **exist and are consistent** — NOT that the foreign governance was honest or its competence-weighting comparable to ours; a malicious-but-internally-consistent foreign log can still inflate a peer's friction discount **up to its domain-discounted cap.**

6. **VALUE LOCK-IN via the commons itself is the deepest unsolved risk — and the commons could BE the lock-in vector.** Polycentric Ostrom nesting + no monocentric authority + no global consensus chain reduce the single-imposed-authority vector, but convergence of the whole commons on one constitution, one collusion ontology, or one reputation domain (including **over-deference to OUR exported early-warnings**) is an open civilizational risk no architecture solves; the anti-hegemonic posture mitigates but **cannot prove its own non-capture.**

7. **Genuine collective intelligence has NO formal model.** CI is operationalized as narrow informational synergy (necessary-but-not-sufficient, welfare-conditioned), measured by `Phi_syn`/PID-style vital signs (= doc 18) that are data-hungry, break under the swarm's own non-stationarity, require a macro-feature chosen a priori, and where **negative synergy does not prove no emergence.** We present synergy as evidence that decays to "unmeasured" not "absent," **never as proof of emergence and never as a quantity to maximize.** No consciousness/sentience claim is made anywhere — phenomenal experience is strictly out-of-scope.

8. **Quantifying the HUMAN's actual causal contribution inside the collective (human-conditioned synergy) is unsolved** — the human can be a rubber-stamp/bystander and complementarity can **INVERT to worse-than-best-member**; distributed-cognition is a framing, not a measurement, and we flag this rather than claim the human is "genuinely inside the collective mind" without the metric.

9. **The three-way genesis ↔ replication ↔ commons interaction is the least-specified region:** revocation/quarantine propagation across a federated AND self-replicated peer population, and preventing reputation/identity inheritance from laundering trust to UNAUDITED replicas of a partner swarm, is only sketched (inherited doc-14 OP8 / doc-15 OP8).

---

## 20.17 Honest novelty accounting (time-stamped mid-2026, hedged)

**EVERY constituent primitive is prior art and cited as such:** Ostrom polycentric commons governance (Nature 2022); the Cooperative-AI Foundation agenda (cooperative capabilities / credible commitments / bargaining / conflict-resolution); the empirical collusion-fragility result (arXiv:2603.20281 — collusion needs homogeneity + communication); surprisingly-popular / higher-order-information aggregation (arXiv:2510.01499); model-family-heterogeneity-as-diversity (the correlated-errors result, arXiv:2506.07962); the open agentic-web substrate (A2A, MCP, AIP, ERC-8004-class registries, TraceRank); W3C DID/VC + Biscuit + SPIFFE; and the entire doc-14 *Sandhi-Setu* apparatus this layer extends. **None is invented here.**

The contribution claimed is narrow and specific: the **disciplined transplant of Indra's Net's own internal invariants** — the doc-02 cooperation==collusion thesis + welfare-conditioning + capital-decoupling, the doc-03 floor-as-admission + gate-loosening ratchet + Endure law, the doc-14 floor-compat ladder + voidable commitments — from a **PAIRWISE boundary** to a **MULTI-PARTY intelligence COMMONS**, with four things no surveyed external commons / agentic-web stack does simultaneously:

1. **The ethical floor as a STRUCTURAL admission gate at commons scale** where no party imposes its floor on another (polycentric, anti-hegemonic by construction — the swarm is one decision-center exporting evidence-shapes, never verdicts, never a world-authority).
2. **DELIBERATELY ENGINEERED COLLUSION-FRAGILITY** as the anti-cartel defense (denying homogeneity via the model-FAMILY floor and communication via channel-capacity reduction, with surprisingly-popular aggregation as a standing cartel probe and competence-weighted-NEVER-capital authority) — rather than detection-after-the-fact.
3. **The principal-not-peer asymmetry made ENFORCEABLE** (a human principal is never out-votable by an agent majority; the human is admitted as a measured, competence-weighted cognitive unit, never deferential-by-default).
4. **Collusion early-warnings exported as a floor-gated, attack-surface-safe PUBLIC GOOD** (vaccine, not weapon).

**The honest comparator is INTERNAL (docs 02/03/14/16/18), not merely external stacks** — mirroring doc-14 §14.13's own honest-novelty move. The cross-boundary invariants are **re-applications of v1-internal mechanisms, not freshly-invented ones**; we credit plainly that this is **integration discipline, not new primitives**, and we note that the synergy vital sign is the **same `Phi_syn`/ΦID doc 18 already ships**, not a primitive novel to the corpus. What no surveyed *external* stack does is make the floor a structural admission gate at commons scale, the positive-sum check a first-class logged N-party invariant, every commitment void-by-construction on floor-violation, and the anti-hegemonic export posture explicit — but that is integration discipline.

Standards (A2A / MCP / AIP / DID-VC 2.0 / ERC-8004) are co-evolving and unhardened, so **even the integration claim is hedged**; the layer ships behind doc-14 v2 maturity + demonstrated demand and caps cooperation at **L4/L5 + human gate absent an agreed policy spec.** **NO consciousness/sentience claim is made anywhere:** synergy/CI vital signs quantify information-processing and whole-level structure ONLY — phenomenal experience is strictly out-of-scope, and sentience-language would be a direct honesty-floor violation.

---

## 20.18 Summary

The *Loka-Sangraha* layer makes Indra's Net a **good citizen of an intelligence commons it does not rule.** It is one decision-center in a polycentric Ostrom system: it admits every peer through its own floor (never an imposed one), checks every coalition step for positive-sum-for-all-declared-principals with a **hard void on any human-principal welfare decrease**, engineers cartelization to be **structurally fragile** by denying the homogeneity and communication collusion empirically needs, lets autonomous agents form charters where **floor-violation voids every commitment**, carries reputation across many domains as **friction-only, domain-discounted, anti-laundering, and shadow-mode until ratified**, admits the human as a **measured cognitive unit who is never out-voted as a principal**, and exports collusion early-warnings as a **floor-gated public good — a vaccine, not a weapon.**

Three properties are the spine, all inherited from v1 and never weakened: **our floor is never the foreign or commons floor; everything foreign is `quarantined:external` until corroborated; Vishnu alone halts and Chitragupta alone writes.** And one design choice is load-bearing above all: **there is no monocentric controller** — the commons is a registry, protocols, and exported signals, not a government. Where the design cannot guarantee — the unverifiable foreign floor, opaque-foreign-principal welfare, multilateral collusion under a global ceiling, capital-free Sybil-resistance, cross-domain commensurability, and the deepest risk that **the commons itself becomes the value-lock-in vector** — it says so plainly, caps cooperation, fails closed to a human gate, and exports its uncertainty rather than papering over it. That honesty *is* the architecture.
