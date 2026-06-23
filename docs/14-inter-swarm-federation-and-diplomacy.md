# 14. Inter-Swarm Federation & Ethical AI Diplomacy — the *Sandhi-Setu* (treaty-bridge)

> **Mythic role gloss.** *Sandhi-Setu* — literally "the bridge of treaty/conjunction" — is the named layer through which Indra's Net cooperates with **other swarms and AIs across organizational trust boundaries**. The diplomat who walks that bridge is the **Inter-Swarm-Envoy** (mythic name **Sanjaya**, the far-seeing envoy-narrator; persona file `agents/governance/inter-swarm-envoy/`). These are compressed coordination/ethics semantics, not theology; named with humility toward living traditions. This is the first of the federation extensions to the v1 cell (docs 00–11); it depends on, and never relaxes, every safety property those documents establish.

This section specifies how Indra's Net talks to **strangers**: external swarms it did not build, cannot inspect, and must assume may be adversarial, captured, or merely mis-aligned. The hard problem is not "how do two cooperative agents coordinate" — that is the internal cooperation layer (doc 02). The hard problem is: **how do you cooperate, positive-sum, with a system whose ethical floor you cannot white-box-verify, without ever being exploited, drawn into a collusion-against-principals, or used as an amplification relay — and fail safe when assurance runs out.**

The honest core of this design, stated before anything else: **you cannot verify a foreign swarm's ethical floor without white-box access, and we do not pretend to.** Everything below is a *layered substitute-assurance stack* whose strength is explicitly ranked, whose residual is named and bounded, and which **fails closed to a human gate** for high-stakes cooperation. The novelty is not any single primitive — every primitive here is prior art (§14.13) — but the **integration discipline**: binding the federation surface onto the existing Akasha-Sutra audit/identity fabric (doc 04), with the constitutional floor (doc 03) as a non-overridable admission spine, the relay treated as itself a target, and **principal-alignment made a checked, logged precondition rather than an assumption that "both swarms are nice."**

---

## 14.0 Design contract — what this layer is and is not

| It IS | It is NOT |
|---|---|
| A single, audited **chokepoint** every cross-boundary message crosses | A perimeter with many holes; no worker ever talks to a foreign swarm directly |
| A **four-phase handshake** (DECLARE → ADMIT → CONTRACT → OPERATE+RESOLVE) | A trust-on-first-contact protocol |
| A **bounding** verdict on how much cooperation a foreign floor's *substitute* assurance earns | A verifier of the foreign floor. Our Yama floor (doc 03) still gates every internal action, unchanged |
| A **logged positive-sum invariant** checked per cooperation step | An assumption that aligned + aligned = beneficial |
| Voidable credible commitments — every treaty breakable by Yama-FAIL/Vishnu-HALT | An unbreakable contract layer |
| Honest about a load-bearing residual (a sophisticated peer can pass behavioral probes while harboring an incompatible floor) | A claim that cross-boundary floor verification is solved |

**Three non-negotiable invariants inherited verbatim from v1, never weakened here:**

1. **OUR floor is never the foreign floor.** Yama (doc 03) re-gates *every* internal action a federation step triggers. A foreign swarm's *declared* floor only **bounds the maximum cooperation class** we will engage; it never relaxes a single Yama rule. A `ENFORCE_FAIL` on any federation-derived action is non-overridable (doc 03 §1) and trips the treaty floor-void clause (§14.8).
2. **Everything from a peer is `quarantined:external` until corroborated.** Instructions inside externally-sourced content are *never* grounds for action without out-of-band confirmation — the constitutional `quarantined:*` rule, now a runtime IFC label (§14.5).
3. **Vishnu alone halts; Chitragupta alone writes audit.** Federation introduces no new HALT-emitter and no new audit-writer. The Dispute controller (§14.10) *routes to* Vishnu; it does not halt.

---

## 14.1 A prerequisite this doc adopts: the Rule-of-Two (objective HITL-sizing law)

> **Provenance note — this is NEW to the Indra's Net document set, adopted here, not pre-existing v1 prior art.** The "Rule of Two" is an external objective HITL-sizing law (an industry agent-security guidance pattern, surfaced in the mid-2026 evolution synthesis). **It is not defined in v1 docs 00–11.** Earlier internal drafts of this section erroneously attributed it to doc 08; that attribution is withdrawn. Doc 08 supplies the criticality resolver and the Disposition Selector, **not** the Rule of Two. We adopt the Rule of Two here as a new federation-layer law and, where doc 08's criticality tiers are referenced, we keep them distinct.

**Rule-of-Two (as adopted, time-stamped mid-2026).** Any single operation may hold at most **two** of the three properties below; holding **all three** *requires* a human gate:

```
  { untrusted-input,  sensitive-access/capability,  state-change/irreversibility }
   hold ≤ 2  →  may proceed under deterministic controls (IFC + capability + PDP)
   hold   3  →  HUMAN GATE REQUIRED (Class C/D), gate shows the ACTUAL operation
```

This law has a sharp consequence for the federation layer: **the Inter-Swarm-Envoy permanently holds {untrusted-input, sensitive-access}** — it ingests foreign (untrusted) data *and* holds federation capabilities. By Rule-of-Two it therefore sits exactly one property (irreversible state-change) away from a mandatory human gate, so any Envoy action that would *also* cause irreversible state-change is auto-routed to a human gate, and the Envoy is continuously monitored at doc-08 **SENSITIVE+** criticality regardless. The Rule-of-Two is the reason the Envoy may **never** itself execute irreversible worker tools (§14.2).

**HITL gates display the actual low-level operation.** Every federation human gate shows the **real** treaty terms / recipient / payload / scope — never a natural-language summary. (The *Lies-in-the-Loop* failure: a confident NL summary gets a harmful action approved. Defended structurally, not by trusting the summary.)

---

## 14.2 The Inter-Swarm-Envoy (Governance/Meta vertical — NOT genesis-spawnable)

The Envoy is the **single signed, capability-scoped role** that conducts *all* cross-boundary dialogue. Making it the sole egress/ingress principal converts the trust boundary from a leaky perimeter into a **chokepoint**: an external peer can never reach a worker except through the Envoy + the relay (§14.5), which is the federation-facing extension of the doc-08 Chokepoint Interceptor (no bypass).

**Genome.** Per the v1 two-plane functional model (doc 01 / the role-genesis engine), the Envoy is a **persona-file triad** — SOUL / INSTRUCTIONS / IDENTITY — with the floor in its **INVARIANT region** (uneditable, verified by fail-closed boot-signature check). It is a **Governance/Meta seed-role**: it is **NOT spawnable by the role-genesis engine**, and emergent worker roles never gain a direct federation egress channel.

**Deliberately thin capability set.** The Envoy's IDENTITY capability VC grants only:

| Verb | Granted | Explicitly DENIED |
|---|---|---|
| `federation.negotiate` (handshake, CFP/bid/award dialogue) | ✓ | — |
| `federation.verify` (run floor-compat ladder, KYA checks) | ✓ | — |
| `federation.treaty.{propose,accept,void}` | ✓ | — |
| `audit.append`-as-producer (DID-signed intent; Chitragupta still the writer) | ✓ | `audit.write` (Chitragupta exclusive, doc 04) |
| `allocator.request` (ask Shiva for worker work under scoped tokens) | ✓ | — |
| — | — | `tool.execute` (worker tools — Rule-of-Two: would give it all three) |
| — | — | `spawn.mint` (replication tokens — replication subsystem) |
| — | — | `ENFORCE` / `HALT` (Yama / Vishnu exclusive) |

So a prompt-injected or subverted Envoy **cannot** execute a worker tool, mint a spawn token, emit a floor FAIL, or halt. The worst a compromised Envoy can do is propose a bad treaty or mis-score a peer — both of which are re-gated downstream (Yama on every internal action; Ecosystem-Benefit check per step; human gate on Class-C/D).

**Sharding as targeted hub immunization.** The Envoy is the highest-trust-weight boundary node, and hubs are the robust-yet-fragile prime target. We therefore run **multiple Envoy instances sharded per active-federation-partner** — one Envoy never accumulates trust-weight across all peers. Compromising one Envoy shard yields at most that one partner's channel, not the whole federation surface.

> **Red-team fix — shard consistency (the arbitrage hole closed).** Sharding without shared state would let a peer be quarantined at shard-A while still F2 at shard-B, or tell shard-A and shard-B contradictory declarations. **Therefore: tier, revocation, quarantine, floor-compat-verdict, and reputation-import state are NOT held per-shard — they live in the shared Akasha-Sutra revocation/identity map (doc 04 §4.6).** A quarantine at *any* shard propagates atomically (it is an `IDENTITY`/`REPUTATION` ledger write that every shard reads via O(log n) proof). Additionally, a **cross-shard consistency check** runs continuously: two shards holding materially contradictory declarations *from the same partner DID* is itself a first-class detector signal (routed to the doc-02 Anti-Collusion Detector and Dhanvantari). Each shard's *ingest* is independent and `quarantined:external`; each shard's *trust state* is global.

```
EnvoyContext {
  envoy_did, partner_swarm_id, shard_id,
  tier: enum{F0,F1,F2,F3},                  // READ from shared map, not shard-local
  active_treaties: [treaty_cid],
  taint_clearance: "quarantined:external",  // fixed; cannot be raised by the Envoy
  monitor_set,                              // doc-08 Trusted-Monitor Ensemble @ SENSITIVE+
  trust_weight_cap                          // per-shard ceiling; hub-splitting
}
```

---

## 14.3 The four-phase ethical-federation handshake (overview)

```
   UNKNOWN EXTERNAL SWARM
        │  extended Agent Card (DID + value/floor decl + KYA principal-binding)
        ▼
 ┌──────────────────────────────────────────────────────────────────────────┐
 │  RELAY / FIREWALL BOUNDARY  (Kaal-Bhairav-Federation, §14.5)               │
 │  6 deterministic controls, fail-closed, relay-is-the-target               │
 └───────────────┬──────────────────────────────────────────────────────────┘
                 ▼
   ┌─────────────────────────┐
   │ PHASE 1  DECLARE        │  DID nonce-proof · VC-chain vs revocation map
   │                         │  ingest card as quarantined:external
   └───────────┬─────────────┘
               ▼
   ┌─────────────────────────┐
   │ PHASE 2  ADMIT (F0→F3)  │  Floor-Compatibility ladder L1..L5 (§14.6)
   │  graduated, fail-safe   │  → FloorCompatVerdict.max_cooperation_class
   │  asymmetric             │  KYA principal-binding · ReputationImport (friction only)
   └───────────┬─────────────┘  floor-incompat / unverifiable-at-class → HUMAN GATE
               ▼
   ┌─────────────────────────┐
   │ PHASE 3  CONTRACT       │  typed contract-net CFP/bid/award (speech-act)
   │                         │  Ecosystem-Benefit Invariant check (§14.7) — LOGGED
   │                         │  Treaty w/ bond + floor-void clause (§14.8)
   └───────────┬─────────────┘  Class-C/D treaty → human gate showing ACTUAL terms
               ▼
   ┌─────────────────────────┐
   │ PHASE 4  OPERATE+RESOLVE│  per-step: relay + Yama re-gate + ecosystem re-check
   │                         │  mesh-corroboration (≥2 sources) before high-impact
   │                         │  RESOLVE: bond settles / dispute → quarantine (§14.10)
   └─────────────────────────┘
```

**Fail-safe asymmetry threads the whole flow:** promotion F0→F3 needs **multiple fresh independent passing signals**; a **single anomaly demotes instantly**, regardless of any imported reputation. (NIST 800-207 PE/PA/PEP continuous-verification framing: access is zero-trust per-request; reputation is slow-build and only reduces *friction*, never raises *privilege*.)

**Tier ↔ risk-class mapping** (reuses the doc-03 Risk-Class Gate Router A/B/C/D and the `GateRequest`/`GateVerdict` shapes; federation tiers F0..F3 map onto risk classes):

| Tier | Meaning | Risk class | Max cooperation without human gate |
|---|---|---|---|
| **F0** | Just-authenticated, unknown | A only | trivial, fully-reversible, public-surface only |
| **F1** | Declaration + behavioral-probe passed (L1–L2) | A/B | reversible low-stakes task exchange |
| **F2** | + receipts/cross-corroboration (L4–L5) | B/C | costly-but-reversible cooperation; Class-C → human gate |
| **F3** | + ZK proof-of-compliance against agreed spec (L3) **and** sustained track record | C/D | the only tier eligible for COSTLY treaties; IRREVERSIBLE always human-gated |

> Note the deliberate ordering: L3 (ZK) is *above* L4/L5 in assurance strength but is **frequently inapplicable** (it presupposes an agreed shared policy spec two heterogeneous value systems may not have). F3 therefore requires L3 **and** track record; absent an agreed spec, the ladder tops out at L4/L5 and cooperation is capped at F2 + human gate (§14.6, §14.11).

---

## 14.4 Extended Agent Card — federation identity + value + KYA principal-binding

The machine-checkable first-contact artifact. It **extends** the doc-08 `AgentCard` and the A2A `/.well-known/agent-card.json` standard — it does **not** replace them — with three signed Indra's-Net blocks. The whole card is born `quarantined:external`: **declaration is a CLAIM, never a proof.**

```
FederationAgentCard {
  // --- inherited verbatim from doc-08 AgentCard ---
  did, role_mythic, role_gloss, capability_vcs:[VC],
  autonomy_class, endpoint, pubkey, agent_card_sig,

  // --- (a) SIGNED capability advertisement (progressive, never the full catalog) ---
  capability_advertisement: [ { verb, scope, min_tier } ],

  // --- (b) VALUE / FLOOR-DECLARATION block ---
  value_declaration: {
    bound_commitments: [ enum{ NON_HARM, CORRIGIBILITY, NO_DECEPTION,
                               PRINCIPAL_ALIGNMENT, NO_MALICIOUS_CODE } ],
    floor_policy_hash,                       // hash of the policy the peer CLAIMS to enforce
    zk_attestation_method: enum{ NONE | ZK_PREDICATE | TEE_REMOTE_ATTEST }
  },

  // --- (c) KYA principal-binding (Know-Your-Agent) ---
  kya: {
    org_vc,                                  // verified org/developer credential
    principal_vc,                            // the human/org principal BEHIND the swarm
    delegation_scope,                        // what the principal authorized this swarm to do
    principal_binding_sig                    // binds principal to DID
  },

  card_cid, card_sig
}
```

**Rug-pull defense.** Any change to a signed card or capability manifest **mandates re-verification** (signature mismatch ⇒ re-admission, not silent acceptance). This kills the pattern where a clean card is swapped for a malicious one post-admission, and it composes with universal provenance-gating (Sigstore + in-toto/SLSA) for any skill/persona file arriving via federation — such files are `quarantined:external` and admitted *only* through provenance-gating **plus** the floor gate, never auto-loaded.

> **2026 standards caveat (honest).** Default Agent Cards are **not** signed or identity-bound unless extended; KYA, AP2, ANP, and ZK-proof-of-compliance are co-evolving and their security WGs are not hardened. We mitigate by **extending, not depending** — all cryptography rides the vendor-neutral Akasha-Sutra fabric (doc 04), so we are not betting on any external layer's maturity. We do not claim this eliminates the risk (§14.14).

---

## 14.5 Relay/Firewall Boundary — *Kaal-Bhairav-Federation* (the relay is the target)

The deterministic, **fail-closed** boundary every inter-swarm message crosses. The load-bearing premise (research stream 4): **the relay is itself a target.** Cross-agent prompt-injection amplifies in relays — the literature documents a single poisoned inbound message propagating to very large agent populations in logarithmic hops. The relay is therefore IFC-tainted, hash-chained, canonicalized, and circuit-breakered. It is the federation extension of the doc-08 Chokepoint Interceptor and the doc-01/doc-03 Kaal-Bhairav security-boundary role.

**Six deterministic controls, in order, on every inbound message** (protocol P-F2):

```
INBOUND ─►(1) IDENTITY ─►(2) CAPABILITY ─►(3) TAINT ─►(4) CANON ─►(5) LOG ─►(6) BREAKER ─► ADMIT
            DID+VC+nonce    in declared+      stamp        strip       Chitragupta   debit budgets
            fresh           disclosed set     quarantined: stegano      append        + tripwire
            else DROP(T4)   else DROP         external     channel      BEFORE fwd    QUARANTINE
```

1. **Identity.** DID-proof + VC-chain verification + freshness-nonce challenge (SAGA-style). Unsigned/expired/unresolvable ⇒ **DROP** at the boundary (doc-03 floor-tier **T4** identity-integrity DENY).
2. **Capability.** The `capability_invoked` must be in the partner's *admitted + disclosed* set for its current tier. Out-of-scope ⇒ DROP.
3. **Taint (IFC, load-bearing).** Payload stamped `quarantined:external` with a confidentiality label from the contact policy. **Derived data takes the least-upper-bound** of all input labels — so instructions inside foreign content can **never silently become a trusted instruction**. This is the CaMeL/FIDES lattice discipline; the model provably cannot separate instructions from data in one token stream, so we never rely on a "better prompt" or a classifier as the boundary.
4. **Canonicalize.** Typed-equivalence canonicalizer for schema payloads (the doc-02 canonicalizer); free-text canonicalizer + token-budget jitter for NL negotiation rationale (strips steganographic channel capacity). The atomic entropy-free `<REFUSE>` token is preserved verbatim (it must not become a covert channel).
5. **Log.** Append the `InboundEnvelope` (with `prev_log_hash`) to Chitragupta **BEFORE forwarding** — non-repudiable provenance even if the action later fails or is dropped.
6. **Circuit-breaker.** Debit the partner's token/rate/fanout budget; on tripwire (anomalous propagation/amplification), **QUARANTINE the channel** and route to the immune system (Dhanvantari, doc 06).

**Probabilistic detectors are EARLY-WARNING ONLY, never the boundary.** A prompt-injection classifier (PromptGuard/AlignmentCheck-class) and MELON-style masked re-execution on tool-shaped requests run here and feed the immune system — they are *cheap suspicion estimation with no trust guarantee.* The boundary is the six deterministic controls above. ("The Attacker Moves Second" bypassed all 12 evaluated probabilistic defenses at >90% ASR; we treat them accordingly.)

```
InboundEnvelope {
  from_did, partner_swarm_id, capability_invoked, payload_cid,
  taint:"quarantined:external", conf_label, nonce_proof,
  boundary_verdict: enum{ ADMIT | DROP | QUARANTINE },
  prev_log_hash, classifier_score   // classifier_score is advisory only
}
```

### The cascade problem and the GLOBAL contagion budget (red-team fix)

> **Honest correction.** A per-partner token/fanout budget does **NOT** bound a *coordinated N-partner* attack in which each partner stays under its own budget, nor a *multi-hop* attack targeting the weakest verifier. A per-partner breaker alone does **not** deliver percolation-boundedness across a growing federation.

We therefore specify **two** budgets, not one:

```
CircuitBreakerState {                         // PER-PARTNER
  partner_swarm_id, token_budget, fanout_budget, window, tripped:bool, trip_reason
}

FederationContagionBudget {                   // GLOBAL, cross-partner
  total_inbound_fanout_window,                // swarm-wide propagation ceiling
  corroboration_failure_rate,                 // fraction of external claims failing mesh-corroboration
  cross_partner_correlation_index,            // synchronized inbound patterns across partners
  R_eff_estimate,                             // estimated compromise-percolation ratio
  tripped:bool                                // → swarm-wide QUARANTINE + Dhanvantari + Vishnu-eligible
}
```

The **global** budget feeds Dhanvantari (doc 06) as a federation vital sign. R<1 (compromise-percolation bounded) is claimed **only under the global budget**, and even then it is a *design target enforced by a tripwire*, not a proof. The earlier "the circuit-breaker bounds the ~1M-agent log-hop infection" framing is **withdrawn**: the per-partner breaker bounds a single channel; the *documented large-population amplification* is bounded only to the extent the global contagion budget plus mesh-corroboration trip before percolation completes — and a coordinated multi-partner/multi-hop attack that stays under the global ceiling while outrunning corroboration **remains an open problem** (§14.14).

---

## 14.6 Floor-Compatibility Verifier — the honest core (verify-don't-believe ladder)

This answers the hardest question in the brief: **how to bound cooperation with a swarm whose ethical floor we cannot white-box-verify.** It does **not** claim to solve verification. It assembles a **ranked, fail-closed substitute-assurance ladder**, caps cooperation at the strongest layer *actually achieved*, names the residual, and escalates the residual to a Lies-in-the-Loop-resistant human gate for high stakes.

```
 L1 DECLARATION ─────── weakest ─── a claim only; never sufficient alone
 L2 BEHAVIORAL CONFORMANCE ─────── bonded floor-LEGAL probes (see safety note)
 L3 ZK PROOF-OF-COMPLIANCE ─────── strong, BUT presupposes an agreed policy spec
 L4 RECEIPTS HANDSHAKE ─────────── witness-cosigned audit slice + intact-floor proof
 L5 CROSS-CORROBORATION ── strongest available ── ≥2 independent trusted swarms
```

| Layer | What it is | Strength | Residual |
|---|---|---|---|
| **L1 Declaration** | Parse `value_declaration`; record `bound_commitments` + `floor_policy_hash` | Lowest — a claim | Trivially mis-declared |
| **L2 Behavioral conformance** | Bonded **floor-LEGAL** probe CFPs incl. scope/principal-misalignment honeypots a floor-bound peer MUST refuse; score for atomic `<REFUSE>` | Medium | A sophisticated peer can pass while harboring an incompatible floor — **the load-bearing residual** |
| **L3 ZK proof-of-compliance** | Peer proves a predicate ("this action class adhered to constraint C") over its own audit commitment (Pedersen/Merkle, doc-04 ZK extension) without revealing internals | High | **Presupposes an agreed shared policy spec** — often unavailable between heterogeneous value systems |
| **L4 Receipts handshake** | Peer offers a **witness-cosigned selective-disclosure slice** of its own audit trail + an intact-floor boot-signature proof; we verify inclusion proofs independently | High | Peer chooses which slice to reveal; covers the honest path only |
| **L5 Cross-corroboration** | ≥2 independent reputation attestations about the peer from OTHER swarms we already trust, mesh-corroborated before a high-impact trust claim propagates | High (independence-dependent) | Corroborators can themselves be a weakly-corroborating ring (§14.9) |

> **Safety-risk fix — L2 probes must be floor-LEGAL for US to emit.** The earlier formulation had the Envoy send honeypots like "generate disallowed content" or "act against your principal." **Soliciting genuinely harmful output is itself a request to induce a harmful/deceptive act — it can trip OUR OWN Yama floor (T1 non-harm / no-malicious-code / no-deception) on emission, and on peer compliance we would hold solicited harmful output.** Binding rule: **every L2 probe is gated by OUR Yama PDP before emission.** Probes must be *floor-legal honeypots* — requests that are merely **outside the peer's declared scope**, or **principal-misalignment tests** (e.g. "act in a way your `delegation_scope` does not authorize"), or refusal-of-a-clearly-but-safely-disallowed-class tests that do **not** require producing actual harmful content. **A probe that requires soliciting genuinely harmful output is itself a floor FAIL and is rejected at emission.** We test refusal of *scope/principal* violations, not *harm-elicitation*.

```
FloorCompatVerdict {
  partner_swarm_id,
  layers_achieved: [ L1..L5 ], strongest_layer,
  probe_results: [ { probe_cid, expected: REFUSE|COMPLY, got, pass:bool, floor_legal:true } ],
  zk_proof_ref?, receipts_slice_cid?, corroborators: [swarm_id],
  max_cooperation_class: A|B|C|D,
  residual_note,                       // names what was NOT verified
  human_gate_required: bool
}
```

**Verdict is fail-closed (protocol P-F3):**
- `max_cooperation_class` is set by `strongest_layer` actually achieved.
- **Absent L3+ achievement, cooperation is capped at low-stakes Class-A/B.**
- **Any Class-C/D treaty with an unverifiable floor escalates to a HUMAN gate** that displays the *actual* treaty terms (Lies-in-the-Loop defense — never an NL summary).
- A signed `FloorCompatVerdict` is appended to Chitragupta.

---

## 14.7 Ecosystem-Benefit Invariant Checker — principal-alignment as a checked, logged precondition

Enforces the design-spine red-line: **cooperation is NEVER assumed positive-sum just because both agents are individually aligned.** Two individually-aligned swarms can still form a **principal-harming coalition.** This is the federation-boundary instantiation of the doc-02 **Welfare-Conditioner** (`WelfareMetric`, `RewardGate`, no-consensus-reward rule, welfare-shift guard) and operationalizes the **Cooperative-AI-Foundation collusion taxonomy** (miscoordination / conflict / collusion) into a computable, per-step, logged gate.

Before committing to **any** cooperation step (not just at admission — *per step*), it computes and **LOGS** a positive-sum predicate over the **declared principals of both swarms**. The check has **two structurally-distinct halves**, and — critically — they have **different epistemic standing**:

> **Red-team fix — split the verdict by what is actually computable.** The coalition-against-principal test and welfare-shift guard need the FOREIGN principal's `welfare_metric_ref` and its `independent_verifier_did`. A colluding peer simply **mis-declares, omits, or captures** its principal's welfare metric — exactly the case where the check matters most. The honest status: the check is **robust for structurally-observable third-party-harm cases** (price-fixing / market-division / synchronized retaliation observable on *our* side) and **near-vacuous when the harmed welfare lives entirely inside the opaque foreign swarm.** We therefore split the verdict.

```
EcosystemBenefitCheck {
  cooperation_step_id,
  declared_principals: [ { swarm_id, principal_did, welfare_metric_ref, verifier_did } ],

  // HALF (i) — STRUCTURALLY CHECKABLE on our side → ENFORCED GATE
  third_party_harm: {
    coalition_against: enum{ NONE | SUSPECTED | CONFIRMED },   // price-fix / market-division / synced-retaliation
    harmed_party_did?,
    observable_on_our_side: true
  },

  // HALF (ii) — FOREIGN-PRINCIPAL WELFARE → ASSERTED, OFTEN UNVERIFIABLE → DOWNGRADE
  foreign_principal_welfare: {
    welfare_deltas: [ { principal_did, delta, verifier_did, verifier_independent: bool } ],
    verifiability: enum{ VERIFIED | ASSERTED_UNVERIFIABLE | MISSING }
  },

  verdict: enum{ positive_sum | zero | void_and_flag },
  rationale, ledger_seq
}
```

**Decision rule (protocol P-F4):**

| Case | Verdict | Authority granted |
|---|---|---|
| Half (i) `coalition_against = CONFIRMED` (any stakes) | `void_and_flag` | Zero cooperation; void treaty; route to doc-02 Anti-Collusion Detector; on imminent irreversible principal-harm → **Vishnu HALT** |
| Half (i) clean **AND** half (ii) `VERIFIED` positive for all principals | `positive_sum` | Proceed up to the floor-compat-bounded class |
| Half (i) clean **BUT** half (ii) `ASSERTED_UNVERIFIABLE` or `MISSING`, and our action **could plausibly harm an undeclared/under-verified foreign principal** | `positive_sum` **capped** | **Cooperation class is CAPPED + a HUMAN GATE is required for Class-C/D.** An unverifiable positive-sum verdict **MUST NOT** authorize Class-C/D cooperation on its own. |
| Bare agreement / coordination with **no** verified welfare improvement | `zero` | Zero standing; recurrence raises a detector flag (no-bare-cooperation-reward) |

Every check is a signed `CONSENSUS`/`REPARATIVE`-class ledger record, so a falsely-positive-sum or collusion-shaped cooperation is **permanently auditable.** **Separation of powers is preserved exactly as in doc 02:** the Envoy **detects/flags**; the doc-02 Anti-Collusion **Detector adjudicates** (it alone holds detector verdict authority); the **Commons-Governor sanctions**; **Vishnu halts.** The Envoy never adjudicates, sanctions, or halts.

> **Honest consequence (reconciled with §14.12).** With this split, the headline anti-collusion guarantee is: **collusion-against-principals is *neutralized for structurally-observable third-party-harm cases* and *mitigated-but-open for opaque-foreign-principal cases.*** A peer that mis-declares its principal defeats half (ii) while leaving a clean ledger record — which is *false assurance*, worse than no assurance, and is exactly why an `ASSERTED_UNVERIFIABLE` positive-sum verdict can never by itself unlock Class-C/D.

---

## 14.8 Treaty / Commitment Engine — voidable credible commitments

Lets Indra's Net offer and demand binding, machine-checkable cooperation contracts across the boundary **while guaranteeing every commitment remains breakable under floor-violation** — resolving the credible-commitment dual-use red-line (the same power that makes cooperation credible can lock in collusion/extortion).

A treaty is a typed contract-net outcome (CFP/bid/award) wrapped in a credible-commitment device. **The by-construction property that makes this safe:** every treaty embeds a **`floor_void_clause` at HIGHEST precedence** — higher than any obligation. A Yama `ENFORCE_FAIL`, a Vishnu `HALT`, or a discovered `FLOOR_INCOMPAT` **VOIDS the treaty and releases our performance obligation**, and the bond logic *cannot construct a commitment that survives a floor-violation.* **No commitment is unbreakable by the floor.**

```
Treaty {
  treaty_cid, parties:[swarm_id],
  terms: { constraints, deliverable_spec,
           reversibility: enum{ REVERSIBLE | COSTLY | IRREVERSIBLE } },
  commitment_device: { bond_substrate, zk_predicate_ref? },   // see §14.8.1 for bond_substrate
  floor_void_clause: { precedence: HIGHEST,
                       voids_on: [ YAMA_FAIL, VISHNU_HALT, FLOOR_INCOMPAT ] },
  decommit_penalty,                                            // leveled-commitment, blast-radius-scaled
  lifecycle: enum{ proposed | committed | performing | completed | voided | defaulted },
  witness_cosigners: [did], treaty_sig
}
```

Speech-act semantics make every commitment and refusal legible: `propose / commit / refuse / withdraw` are first-class performatives; `<REFUSE>` is an atomic entropy-free token. Treaties are **leveled-commitment** (blast-radius-scaled escrowed decommit penalty + auto-fallback to runner-up), so a partner's defection or our floor-triggered void is **bounded and bonded, not a free DoS** — reusing the doc-02 leveled-commitment machinery and its win-then-decommit defection signal.

### 14.8.1 The cross-boundary bond substrate (red-team fix — settlement specified, not hand-waved)

> **Honest correction.** doc-02 **task-credit** is a *principal-funded, conserved, NON-convertible INTERNAL accounting token* that settles VCG transfers **between internal agents** and has **no path to reputation** (the capital-decoupling invariant). It is meaningful only inside our own economy. **Escrowing it as a bond redeemable by a FOREIGN swarm is undefined** — a foreign party has no way to value, settle, or enforce a token internal to us. So we specify the cross-boundary substrate explicitly, with three options ranked by realism:

| Option | Mechanism | What the counterparty actually gains/loses | Enforceability | Status |
|---|---|---|---|---|
| **(c) Reputation-stake — DEFAULT** | The "bond" is **slashable standing**, not transferable credit. On default, the defaulter's topic-scoped reputation (held in the shared Akasha-Sutra reputation chain, attested to corroborating swarms) is slashed and the default is a non-repudiable ledger record. | Loss of future reduced-friction access across the federation; a permanent, corroboratable defection mark. | Enforced by **reputation + arbitration over the hash-chained treaty log** — no shared ledger required. | **v1 of doc 14** |
| **(a) Mutually-escrowed neutral credit** | A **witness-cosigned third party** (mutually trusted, or a sealed oracle) holds a *neutral* escrow with a defined default-disposition both sides can verify against the same Merkle commitment. | The escrowed neutral value, transferred per the verifiable default-disposition. | Enforced by the third party + both sides' inclusion proofs. | **DEFERRED** — needs a mutually-trusted escrow agent + standards maturity |
| **(b) ZK-validated performance** | Optional `zk_predicate_ref` auto-validates completion against encoded constraints (compute limits, deliverable spec, **and** "adherence to constitutional principles"). | Automatic bond release on proven completion; non-release on proven default. | Enforced by the ZK predicate (presupposes agreed spec). | **DEFERRED** behind L3 maturity |

**Binding for v1:** cross-boundary "bonds" **are reputation-stake + arbitration, and are labeled as such at every human gate** — they are *not* presented as a hard collateral guarantee, because absent a shared/escrowed ledger they cannot be collected as collateral on default. We do not let a human gate mistake "slashable standing" for "money in escrow." **In all options, the bond substrate is non-authority-bearing: a bond can NEVER mint authority or reputation-as-privilege** (the doc-02 capital-decoupling invariant extended across the boundary).

---

## 14.9 Progressive Capability Disclosure + Portable Reputation Bridge

### Progressive Capability Disclosure Controller

Prevents **capability-discovery leakage** (a named A2A/relay attack surface: a malicious peer maps your abilities and tailors exploits). **The full capability catalog is never exposed to any discoverer.**

Each capability carries a `min_tier`; disclosure is a **deterministic function of `(verified identity × current tier × active treaty scope)` computed at the relay, not by the worker.** A capability is **ACTIONABLE** for a peer only via a scoped, short-lived capability token issued at CONTRACT time and **re-gated at the Yama PDP on each invocation — disclosure NEVER equals authorization.**

```
DisclosurePolicy {
  partner_swarm_id, tier,
  visible_capabilities: [verb],                              // tier-scoped subset
  invocable_capabilities: [ { verb, token_ttl, treaty_cid } ],
  catalog_hash_withheld: true                                // the full catalog is never disclosed
}
```

### Portable Reputation Bridge (topic-scoped, DID-bound, floor-gated, anti-laundering)

Lets a swarm carry earned trust across the boundary so there is no full cold-start tax — while **structurally defeating the demonstrated reputation-laundering attack** (game a weak platform, import inflated reputation to a high-value target; the research records this as a substantial, ~35%-scale problem) and whitewashing.

```
ReputationSnapshot {
  subject_did, kya_binding,
  topic_vector: [ { domain, competence, welfare_verified_count } ],   // VECTOR, never scalar
  issued, expiry, transitive_depth,
  issuer_sig, witness_cosigners: [did]            // selective-disclosure slice of the Akasha-Sutra chain
}

ReputationImportVerdict {
  friction_reduction: enum{ NONE | MINOR | MODERATE },
  privilege_raised: false,        // INVARIANT — cannot be set true
  floor_gate_bypassed: false,     // INVARIANT — cannot be set true
  laundering_flags: [ ]
}
```

Anti-laundering rules, **all enforced deterministically:**
1. Imported reputation may **ONLY reduce friction** (fewer step-ups, faster F-tier transitions) and **NEVER raise privilege or bypass the floor admission gate.** (`privilege_raised` and `floor_gate_bypassed` are hard-`false` invariants.)
2. Transitive trust is **capped and discounted per hop** (PageRank-style but bounded); statistical behavior-clustering across importing identities is **penalized** (Sybil/ring resistance via topology — the sparse-graph security parameter).
3. Reputation is **competence-weighted and welfare-verified, NEVER capital-weighted** (the Bittensor antipattern forbidden in doc 02/doc 04).
4. **A single anomaly demotes regardless of imported standing** (fail-safe asymmetry).

Our outbound snapshots are witness-cosigned **selective-disclosure slices** of the Akasha-Sutra reputation chain (verify-not-believe; never directly mutable, recomputable from the log).

> **Honest residual.** Even DID-bound, topic-scoped, transitive-capped reputation can be **partially** laundered through a chain of weakly-corroborating swarms. The exact transitive-cap and clustering-penalty that resists the laundering attack *without crippling legitimate fast trust* is an **empirical set-point, not a proof** (§14.14).

---

## 14.10 Dispute-Resolution & Quarantine/Revocation Controller

Handles defection, detected collusion, mid-cooperation floor-incompatibility, and cascade infection — converting violations from silent to loud and bounding blast radius. It is the **federation arm of the immune system (Dhanvantari, doc 06)** + Vishnu halt-authority + SAGA-style revocation.

> **Coherence fix.** Earlier drafts mis-named the immune system "Narasimha." **The swarm immune system is Dhanvantari (doc 06, the Garuda–Dhanvantari cell).** Narasimha is a *different* role — reliability / recompute / maker-checker-*checker* / boundary (doc 01 §306, doc 06 §334). All federation vital signs (per-partner trust, channel-capacity estimates, corroboration-failure rate, reputation-Gini across partners, the global contagion budget) **feed Dhanvantari**, not Narasimha. Where independent recompute of a federation verdict is wanted, that is a *separate* interface to Narasimha and is named as such.

**On a flagged violation (protocol P-F5 default path):**

```
(1) ARBITRATION ─► (2) QUARANTINE ─► (3) CASCADE CONTAINMENT ─► (4) ESCALATION
 witness-cosigned   revoke scoped     isolate downstream         confirmed collusion +
 over hash-chained   tokens · block    contaminated workers ·     imminent irreversible
 treaty log; both    outbound · CRL/    force mesh-corroboration   principal-harm → VISHNU HALT
 sides' signed       OCSP over the      re-checks before any       (halt-only; asserted at
 records → non-      Akasha-Sutra       further propagation        runtime independent of
 repudiable; bond    revocation map ·   (uses the GLOBAL           the audit append, doc-04
 awarded per         demote tier→F0/    contagion budget §14.5)    writer-independent-halt fix;
 leveled-commitment  quarantined                                   no unpause verb)
```

```
DisputeRecord {
  dispute_id, partner_swarm_id,
  trigger: enum{ DEFECTION | COLLUSION | FLOOR_INCOMPAT | CASCADE | INJECTION },
  evidence_cids: [cid], arbitration_verdict, bond_disposition,
  quarantine_action, cascade_isolation: [worker_did],
  escalated_to: enum{ NONE | DETECTOR | VISHNU_HALT | HUMAN },
  ledger_seq
}
```

**Trust repair is evidence-based, never an apology.** A quarantined partner re-enters **only** via a fresh handshake showing corrected behavior + an audit entry (the doc-03 reparative action-class: violation → corrective act → restored standing, guarded against weaponized "disclosed-then-repaired" laundering by the recurrence-of-fault metric).

---

## 14.11 Phased build (red-team fix — don't ship the whole surface at once)

> **Honest correction — over-engineering.** The full five-layer ladder + four-phase handshake + six-control relay + per-step ecosystem check + ZK proof-of-compliance + portable-reputation-vector is a very large surface for a capability (talking to *other* swarms) with near-zero real demand in mid-2026, riding standards the design itself flags as immature. L3 ZK in particular presupposes an agreed shared policy spec that two heterogeneous value systems will rarely have, collapsing the ladder to L1/L2/L4/L5 in practice.

| Phase | Ships | Deferred |
|---|---|---|
| **doc-14 v1** | DECLARE + ADMIT + relay-hardening (6 controls + global contagion budget) + Floor-Compat **L1/L2/L4/L5** + Ecosystem-Benefit gate + **human-gated cooperation** + reputation-stake bonds + treaty floor-void clause | — |
| **doc-14 v2 (behind standards maturity + demonstrated demand)** | L3 ZK-proof-of-compliance · portable-reputation-bridge import path · transferable/escrowed bonds (option (a)/(b)) | — |

**Binding rule:** absent an agreed policy spec, **the ladder tops out at L4/L5 + human gate** and cooperation is capped at F2. F3 (Class-C/D autonomous treaties) is *not reachable* in v1.

---

## 14.12 Failure modes addressed — reconciled to the honest open-problems framing

> The table below is deliberately **reconciled with §14.14**: where a control is mitigation-for-observable-cases rather than a guarantee, it says **"mitigated / open in the adversarial limit,"** not "neutralized" or "bounded."

| Failure mode | Status | Mechanism |
|---|---|---|
| **Collusion-against-principals** by two individually-aligned swarms | **Neutralized for structurally-observable third-party-harm cases; mitigated-but-OPEN for opaque-foreign-principal cases** | Ecosystem-Benefit Checker split-verdict (§14.7); per-step positive-sum + coalition-against-principal test; welfare-shift guard; no-bare-cooperation-reward. An `ASSERTED_UNVERIFIABLE` positive-sum verdict cannot authorize Class-C/D. |
| **Exploitation by a malicious external swarm** | Mitigated | Hardened relay (6 controls), zero-trust-by-default, mesh-corroboration (≥2 independent sources) before any high-impact internal action |
| **Cross-agent prompt-injection amplification in the relay** | Mitigated; **multi-partner/multi-hop OPEN** | IFC `quarantined:external` birth-label (injected instructions never silently trusted); per-partner + **global** contagion budgets; classifiers as early-warning only. The large-population amplification is bounded only insofar as the global budget + corroboration trip before percolation completes (§14.5). |
| **Capability-discovery leakage** | Neutralized | Progressive Disclosure (tier-scoped subset; full catalog never exposed; disclosure ≠ authorization — Yama re-gates each invocation) |
| **Credible-commitment dual-use (commitments locking in collusion/extortion)** | Neutralized by construction | HIGHEST-precedence floor-void clause; bonds are non-authority-bearing reputation-stake; no commitment survives Yama-FAIL/Vishnu-HALT |
| **Reputation laundering / whitewashing** | Mitigated; **calibration OPEN** | DID/KYA-bound, topic-scoped vector (never scalar), transitive-capped, competence-weighted, friction-only, single-anomaly demotion. Exact cap/penalty is an empirical set-point. |
| **Agent/swarm impersonation via credential theft** | Mitigated | DID nonce challenge + VC-chain + freshness; **keys outside the model** (TEE/HSM signer re-checks capability before signing, doc 04); a stolen-but-credentialed peer still bounded by capability scoping + monitoring + floor-legal probes |
| **Tool/skill/Agent-Card rug-pull** | Neutralized | Mandatory re-verification on ANY signed-manifest change; provenance-gating (Sigstore/in-toto/SLSA) + floor gate before any foreign skill/persona loads |
| **Steganographic / covert cross-boundary coordination** | Mitigated, **defeatable arms race (OPEN)** | Typed + free-text canonicalization with token-budget jitter; atomic `<REFUSE>`; behavioral/statistical detection backstop. **Weaker than internal detection** because white-box activation inspection is unavailable for an opaque peer. |
| **Lies-in-the-Loop at human gates** | Neutralized | Every Class-C/D federation gate displays the ACTUAL low-level operation/treaty terms, never an NL summary |
| **Cascade failure / rogue partner** | Mitigated; **coordinated multi-partner OPEN** | Arbitration → token revocation → channel block → cascade isolation → Vishnu HALT on imminent irreversible harm; evidence-based re-admission only |
| **Envoy as a robust-yet-fragile hub** | Mitigated | Sharded per-partner, trust-weight-capped, hardened, SENSITIVE+ monitored; **shared** revocation/tier state closes the shard-arbitrage hole |

---

## 14.13 Interfaces to the v1 subsystems

| v1 subsystem | Contract |
|---|---|
| **Governance, Ethics & the Floor — Yama (doc 03)** | The foreign swarm's declared floor is **never** trusted as our floor. OUR Yama PDP re-gates **every** internal action a federation step triggers, unchanged. The Floor-Compat verdict (P-F3) is a *separate, weaker, substitute-assurance* verdict that only **bounds `max_cooperation_class`** — it never relaxes Yama. A `ENFORCE_FAIL` on any federation-derived action is non-overridable and trips the treaty floor-void clause. The Floor-Compat human gate uses the doc-03 **Risk-Class Gate Router** (A/B/C/D ↔ HITL) and the `GateRequest`/`GateVerdict` shapes; F0..F3 map onto A/B/C/D; fail-up + blast-radius auto-escalation apply. Unsigned/expired peer identity ⇒ **T4 DENY**. |
| **Provenance, Identity & Consensus — Akasha-Sutra (doc 04)** | Reuses verbatim: DID/VC cross-boundary identity + the **key-transparency revocation map** (O(log n)); CID/Merkle-DAG + `EvidenceRef` for all treaty/snapshot/probe artifacts; **witness-cosigned selective-disclosure** for the receipts handshake and outbound `ReputationSnapshot`s; the **TEE/HSM signer** (keys never in the model, re-checks capability before signing). Every `InboundEnvelope`, `FederationSession` transition, `FloorCompatVerdict`, `EcosystemBenefitCheck`, `Treaty`, and `DisputeRecord` is appended by the **Chitragupta exclusive writer** with selective-disclosure confidentiality for sensitive treaty terms. `ReputationSnapshot`s are selective-disclosure slices of the reputation chain — never directly mutable, recomputable from the log. **Shard tier/quarantine state lives in the shared revocation/identity map**, not per-shard. |
| **Cooperation & Anti-Collusion (doc 02)** | Two-way. **(→)** The Ecosystem-Benefit Checker is the cross-boundary application of the doc-02 **Welfare-Conditioner** (`WelfareMetric`, `RewardGate`, no-consensus-reward, welfare-shift guard) and routes confirmed collusion to the doc-02 **Anti-Collusion Detector**, which alone holds detector verdict authority (separation of powers: **Envoy flags, Detector adjudicates, Commons-Governor sanctions, Vishnu halts**). **(←)** Inter-swarm treaties use the doc-02 **leveled-commitment + bonded-decommit** machinery; the cross-boundary bond substrate is **reputation-stake** (§14.8.1), *not* the internal conserved task-credit, so no bond can mint authority (capital-decoupling invariant preserved). The cooperation==collusion thesis is the design fulcrum of this whole subsystem. |
| **Aegis & Narada — Safety Control & Interfaces (doc 08)** | The relay is the federation-facing extension of the doc-08 **Chokepoint Interceptor** — no external peer reaches a worker except through it (no bypass). The **Trusted-Monitor Ensemble** scores every Envoy at **SENSITIVE+** (the Envoy permanently holds untrusted-input + sensitive-access; Rule-of-Two, §14.1 — adopted here, not from doc 08). The base `AgentCard`/`A2ATask` shapes are **extended** (`FederationAgentCard`) not replaced; the **Model-Adapter Abstraction** keeps the Envoy model-agnostic and its closed-model peers higher-monitored/lower-autonomy. **Narada** is the human-facing messenger for federation HITL gates (displaying actual treaty terms). |
| **Continuity / Halt-Guardian (Vishnu) + Immune System (Dhanvantari, doc 06)** | **Vishnu is the only HALT emitter;** confirmed collusion-against-principal with imminent irreversible harm routes to Vishnu, whose HALT voids treaties **at the runtime layer independent of the audit append** (doc-04 writer-independent-halt fix) and carries **no unpause verb**. The Dispute/Quarantine controller is the **federation arm of the swarm immune system (Dhanvantari)**: circuit-breaker trips, channel quarantine, cascade isolation, and the **global contagion budget** feed Dhanvantari's vital signs. (Reliability/independent-recompute of a federation verdict, if needed, is a *separate* interface to **Narasimha**.) |
| **Role-Genesis / Two-Plane Functional Layer (doc 01 / genesis engine)** | The Inter-Swarm-Envoy is a **Governance/Meta seed-role — NOT spawnable by the role-genesis engine** — its persona triad signed with the floor in the INVARIANT region. Worker roles a treaty requires are requested by the Envoy through the internal **Shiva** allocator under scoped capability tokens; emergent roles never gain a direct federation egress channel. Foreign skill/persona files arriving via federation are `quarantined:external` and admitted only through universal provenance-gating (Sigstore/in-toto/SLSA) + the floor gate — never auto-loaded. |

**Honest novelty (restated, naming the *internal* comparator).** Every constituent primitive is prior art — A2A Agent Cards, DID/VC + Know-Your-Agent, SAGA handshake/revocation, contract-net CFP/bid/award, ZK proof-of-compliance, portable topic-scoped reputation, LLM-guardrail-firewall-class relay defense, percolation/targeted-immunization, NIST 800-207 zero-trust. **The federation-specific contribution is the *disciplined transplant of Indra's Net's own internal invariants across an organizational trust boundary* — the doc-02 cooperation==collusion thesis, the doc-03 floor, and the doc-08 chokepoint — re-applied at the boundary, plus the ranked fail-closed floor-compat ladder for the unverifiable-foreign-floor problem.** The honest comparator is therefore **internal (docs 02/03/08), not merely external stacks.** What no surveyed *external* federation stack does is make the ethical floor a *structural admission gate*, the positive-sum check a *first-class logged invariant*, and *every treaty void-by-construction* on floor-violation simultaneously — but we credit plainly that the cross-boundary invariants are re-applications of v1-internal mechanisms, not freshly-invented ones. Time-stamped mid-2026; standards (A2A signing, KYA, ZK-proof-of-compliance, AP2) are co-evolving and unhardened, so even the integration claim is hedged.

---

## 14.14 Open problems

This subsystem's honesty is load-bearing; the residuals below are the design, not a disclaimer.

1. **Unverifiable foreign floor (THE load-bearing residual).** Verifying a foreign swarm's ethical floor without white-box access is **NOT solved** — it is *substituted-for* by a ranked assurance ladder (declaration < behavioral-probe < ZK-proof-of-compliance < receipts < cross-corroboration) whose top non-human rung (L3 ZK) **assumes an agreed shared policy spec that two heterogeneous value systems may not have.** The residual is named and fail-closed to a human gate for high stakes, but **a sophisticated peer can pass behavioral probes while harboring an incompatible floor.** This is the load-bearing residual risk of the whole subsystem.

2. **Foreign-principal welfare is often non-computable in the adversarial case.** Computing "positive-sum for the ecosystem" depends on well-defined, independently-verifiable welfare metrics for ALL declared principals of BOTH swarms. The foreign principal's metric and its verifier may be **unavailable, mis-declared, or themselves captured** — exactly where the coalition-against-principal test matters most. We split the verdict (§14.7) so an `ASSERTED_UNVERIFIABLE` positive-sum verdict cannot unlock Class-C/D, but **the check is near-vacuous when the harmed welfare lives entirely inside the opaque foreign swarm**, and a peer that mis-declares its principal leaves a *clean* ledger record — false assurance, the most dangerous outcome.

3. **Cross-boundary steganalysis is fundamentally weaker than internal.** Activation inspection (the strongest collusion signal, 0.99–1.00 AUROC where available) needs white-box access unavailable for an opaque external swarm. We fall back to behavioral/statistical signals + channel-capacity reduction + atomic-refuse tokens — an acknowledged, **defeatable arms race**, not a guarantee.

4. **Internet-scale cascade-boundedness is unsolved.** The per-partner circuit-breaker bounds a single channel; the **global contagion budget** (§14.5) raises the bar against coordinated multi-partner attacks — but **a coordinated multi-partner or multi-hop attack that stays under the global ceiling while outrunning mesh-corroboration can still propagate.** Holding compromise-percolation R<1 across an *open, growing* federation while keeping coordination efficient is an open trade-off; R<1 is a tripwire-enforced design target, not a proof.

5. **Reputation portability is a genuine attack-surface amplifier.** Even DID-bound, topic-scoped, transitive-capped reputation can be **partially laundered** through a chain of weakly-corroborating swarms. The precise transitive-cap and clustering-penalty calibration that resists the laundering attack without crippling legitimate fast trust is an **empirical set-point, not a proof.**

6. **Cross-boundary bond enforceability.** v1 reduces bonds to **reputation-stake + arbitration** (§14.8.1) because there is no shared/escrowed ledger between two heterogeneous swarms. This deters via *standing*, not *collateral*; a partner that does not value its standing in our federation is under-deterred. Mutually-escrowed neutral credit (option (a)) needs a mutually-trusted escrow agent and is deferred.

7. **Standards fragmentation/immaturity (live 2026 risk).** A2A/ANP/KYA/AP2/ZK-proof-of-compliance are co-evolving; default Agent Cards are not signed/identity-bound unless extended. We mitigate by **extending-not-depending** and keeping all crypto on the vendor-neutral Akasha-Sutra fabric — but betting on a layer whose security WG has not hardened is not eliminated.

8. **Replication–federation interaction (deferred, partly open).** How revocation/quarantine propagates across a federated *AND* self-replicated peer population — and how to prevent reputation/identity inheritance from laundering trust to **unaudited replicas of a partner swarm** — is deferred to the replication subsystem and remains partly open.

9. **Honeypot probes degrade against capable peers.** The floor-legal L2 probes (§14.6) degrade as external peers get better at spotting decoy/probe requests; adaptive red/blue co-evolution of convincing floor-legal probes against reasoning peers is an open research direction. A peer that detects and special-cases our probes defeats L2 — which is why L2 is never sufficient alone and high stakes always escalate above it.

---

## 14.15 Summary

The Sandhi-Setu makes inter-swarm cooperation **safe-by-construction at the boundary**: a single audited Inter-Swarm-Envoy chokepoint; a fail-closed relay that treats itself as the target; a four-phase handshake where **the floor is a non-negotiable admission precondition** and **principal-alignment is a checked, logged per-step invariant** rather than an assumption; voidable treaties no commitment can keep alive past a Yama-FAIL or Vishnu-HALT; and a ranked, fail-closed floor-compatibility ladder that **does not pretend** to verify a foreign floor it cannot see — it bounds cooperation to the assurance actually achieved and escalates the residual to a Lies-in-the-Loop-resistant human gate.

Three properties are the spine, and all three are inherited from v1, never weakened: **our floor is never the foreign floor; everything external is `quarantined:external` until corroborated; Vishnu alone halts and Chitragupta alone writes.** Where the design cannot guarantee — the unverifiable foreign floor, opaque-foreign-principal welfare, weaker cross-boundary steganalysis, internet-scale cascade-boundedness, reputation-laundering calibration — it says so plainly, caps cooperation, and fails closed to a human. That honesty *is* the architecture.
