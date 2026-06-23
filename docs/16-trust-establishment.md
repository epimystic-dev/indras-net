# 16. Rapid Trust Establishment (Humans & Machines) — the *Pratyaya* Trust Plane

> *Pratyaya* — in Sanskrit, "warranted confidence; the condition that makes a thing arise." Not faith, not a stored number: a confidence that is *earned fresh* and *conditioned* on present evidence. Pratyaya is the plane on which two parties — a human and the swarm, two machine agents, two whole swarms — reach working trust quickly **without** lowering the constitutional floor. As with every mythic name in Indra's Net, this is engineering vocabulary for a coordination-and-trust function, offered with humility toward the living tradition it borrows from, and making no religious claim.

> **Scope, stated before anything else.** This subsystem is a **reference-design assembly of individually-validated primitives** (NIST SP 800-207 PE/PA/PEP zero-trust, W3C DID/VC, SPIFFE/SVID, RFC-6962 tile-Merkle transparency, the Rule-of-Two HITL-sizing law, competence-weighted reputation). The *primitives are prior art and cited as such.* The contribution is the **wiring**: making "reputation cannot raise privilege" a type-level property of the new plane rather than a rule one must remember to enforce; unifying one fail-safe asymmetry engine across four trust domains; and repurposing the v1 Akasha-Sutra audit fabric (doc 04) as a live trust *accelerant*. The composed per-interaction loop is **NOT validated end-to-end** against an adaptive multi-agent red team. The strongest empirical anchor it inherits is the doc-08 externally-governed-escalation result (harmful insider behaviour ~39% → ~1.2%), and that anchor covers **only** the HUMAN-AUDIT path. Time-stamp: 2026-06. No "first" or "robust-by-construction" claim is made for the composed loop.

---

## 16.0 The single load-bearing move: unconflate *access* from *reputation*

Most agent stacks — and v1 Indra's Net — fold two different quantities into one "trust" number. This subsystem splits them and keeps them split as runtime code:

| Quantity | What it is | How it behaves | Where it lives |
|---|---|---|---|
| **ACCESS / AUTHORITY** | "May this party do *this exact thing right now*?" | Zero-trust, continuously verified, **per-request**, decided fresh; **does not accumulate** between requests | The Aegis chokepoint (doc 08 §8.2), via a NIST-800-207 PE/PA/PEP triad |
| **REPUTATION / STANDING** | "How well has this party done *this topic* over time?" | Slow-build, topic-scoped, competence-weighted, portable, **decays without activity** | The Akasha-Sutra fabric (doc 04), as a cache of inclusion proofs |

The wiring rule that makes the split safe: **reputation can purchase only *reduced friction* (fewer step-ups, faster ladder transitions, lighter monitoring *within a tier*) — never *raised privilege*.** Privilege is granted only by fresh signals passing the gate now. Authentication is **fast** (one round-trip, no issuer call); authorization is **slow and progressive** (the T0→T3 ladder mapped onto risk classes A/B/C/D, climbed only by multiple fresh independent signals all passing).

The governing invariant, applied identically to humans, machines, replicas, and inter-swarm peers, is a **fail-safe asymmetry**:

```
   PROMOTION  ── gated:  k fresh, independent, all-passing Proof/Stake signals,
                          inside a freshness window, post-correlation-collapse independence ≥ req
   DEMOTION   ── free:   ONE anomaly drops the tier instantly, no quorum, no pre-effect appeal
```

This is the doc-00 §3.8 / doc-08 / doc-03 "demotion-free, promotion-gated" rule, here lifted from a per-subsystem convention into **one cross-domain engine**.

---

## 16.1 Relationship to v1 reputation semantics — a contradiction named, and resolved by amendment (binding)

**This section exists because the headline move above directly contradicts ratified v1 architecture, and that contradiction must not be left implicit.**

In v1, **reputation IS authority-bearing**. This is not an accident to be "fixed" — it is a deliberate, ratified design, stated in plain text across the corpus:

- doc 00 §3.9: "Influence flows from demonstrated, evidence-bonded competence." Reputation is the influence gradient.
- doc 02 §2.6 (line 182): the competence-reputation scalar `R(agent, capability)` "is the swarm's competence-weighted authority signal that **the allocator, the diversity subsystem, and the governance gates all read**."
- doc 02 §2.4.1 / §2.6: reputation gates Tier-B/C bidding rights and is the multiplier the Shiva-Allocator reads at award time.
- doc 02 §2.9 problem 4 (line 470): v1 names its own hazard — "reputation gates task value → bidding rights → more work → more reputation."
- doc 08 §8.9 (line 285): "The reputation/track-record produced here feeds **autonomy-class derivation** in §8.8."
- doc 01 §8 (line 350): role promotion stub→provisional→standing reads a competence signal.

A "reputation buys friction, never privilege, by construction" rule is the **opposite** invariant. The two architectures cannot both be true at once. We therefore do **not** claim to "fix v1's single trust scalar." We take the path the red-team's critical fix requires — **option (A): a scoped Class-B amendment that splits v1's single reputation quantity into two named, separately-typed channels** — and specify the migration for every v1 path that currently reads reputation as privilege.

### Scoped amendment: split `R` into Competence-`R` and Standing-`R` (Class B; proposed, requires ratification)

| Channel | New name | Read by | Power |
|---|---|---|---|
| **Competence-`R(did, topic)`** | the existing v1 authority-bearing scalar, **renamed and confined to task-MATCHING / ELIGIBILITY** | Shiva-Allocator (award eligibility), role-genesis & stub-promotion (doc 01 §8 verifiable-improvement test), doc-08 §8.8 autonomy-class derivation (as one input among the existing `{internals_exposed, attestation_present, tier2_active}`) | May determine **eligibility and task-matching** — *who is even considered* for a task and *what risk-class ceiling the model posture allows*. Still **competence-weighted, never capital-weighted** (doc 02 anti-Bittensor invariant preserved verbatim). |
| **Standing-`R(did, topic)`** | the NEW Pratyaya friction quantity introduced by this doc | the Progressive Authorizer (§16.4) only, and the Receipts Handshake (§16.6) | May determine **friction only** — a capped `friction_discount`. Has **no interface method that returns a privilege grant** (§16.7). |

**What changes in each v1 consumer (the migration story):**

- **Shiva-Allocator (doc 02):** reads **Competence-`R`** for *bidding eligibility and Shapley-credit-derived award* exactly as today. It does **not** read Standing-`R`. The doc-02 §2.9-prob-4 rich-get-richer hazard is *unchanged* by this amendment (it lives entirely in Competence-`R`, whose existing mitigations — per-window accrual cap, reputation-Gini vital sign, anti-capture limit — remain in force). This subsystem neither worsens nor solves that v1 open problem; it simply does not add Standing-`R` to the allocator's inputs.
- **doc-08 §8.8 autonomy-class derivation:** Competence-`R` may *lower or raise eligibility for an autonomy class* as v1 already permits; Standing-`R` may only *reduce monitoring rate within an already-granted class* (a friction effect). The §8.8 amendment is specified concretely in §16.5 below (the `MIN(openness_ceiling, rung_ceiling)` join).
- **Role-genesis / stub-promotion (doc 01 §8):** reads Competence-`R` for the verifiable-improvement test exactly as today (and per doc-01's own honest dependency, promotions above read-only still require human ratification until the competence signal is hardened). Standing-`R` plays no part.

**Honest framing of the novelty after this amendment.** The contribution is **a new friction-only Standing-`R` channel ALONGSIDE v1's authority-bearing Competence-`R`** — *not* a correction of v1. The "type-level guarantee that reputation cannot raise privilege" is a guarantee about **Standing-`R`'s interface only**. The composed system still contains v1 paths (the allocator, §8.8 eligibility, role-promotion) that read **Competence-`R`** as authority — by design, and unchanged. Until this Class-B amendment is ratified, this entire subsystem ships in **shadow-mode** (computing dispositions and logging them without enforcing), exactly as a doc-03 §7 gate-loosening would require, because introducing the split *is itself* a governance-touching change.

---

## 16.2 The Trust Signal Bus + the BCPSRC taxonomy

Every input to a trust decision is a **typed, DID-signed, taint-labelled record** on the bus. The gate reasons about *what kind* of evidence it holds, not a scalar. Six classes with strictly different powers:

| # | Class | Meaning | Can RAISE a disposition? | Taint on arrival |
|---|---|---|---|---|
| 1 | **BRIEF** | self-described intent/identity (an `AgentCard`, a human's stated goal) | **No** — never trust a self-described claim (doc 01 line 433: an AgentCard is `quarantined:observed` on receipt, a claim to verify) | `quarantined:unverified` |
| 2 | **CLAIM** | an assertion about a fact/capability/past behaviour, unbacked | **No** | `quarantined:*` until backed by a Proof |
| 3 | **PROOF** | a cryptographically- or audit-verifiable artifact (see below) | **Yes** | `trusted:audited` on successful verification, else degrades to CLAIM |
| 4 | **STAKE** | something put at risk: a slashable capability bond, a refundable escrow CID, a ZK proof-of-compliance that is **voidable on floor-violation** | **Yes** (makes a Claim costly to falsify) | inherits the staked artifact's label |
| 5 | **REPUTATION** | a Standing-`R(topic)` reference resolved from the fabric | **friction only** (never raises the ceiling) | `trusted:audited` (it is a cache of Proofs) |
| 6 | **CONSTRAINT** | a self-imposed capability narrowing, sandbox tightening, egress allowlist, or lease shortening | **Yes** — by *shrinking blast radius* it lowers required assurance | n/a |

**What counts as a PROOF** (each verifiable with zero trust in the offerer's online service): a VC verified against issuer + the pinned revocation snapshot; a DID freshness-challenge response; a tile-Merkle **inclusion proof** from Akasha-Sutra (doc 04 §4.3); an **intact-floor boot-signature** over the genome's INVARIANT region (doc 03 §5 IMMUTABLE partition); a `MakerCheckerWitness` (doc 08 §8.6); an in-toto/SLSA/Sigstore attestation chain (doc 08 §8.11); a TEE quote.

**The bus is fail-closed.** An unverifiable Proof **degrades to a Claim**; a Claim contributes **zero** to disposition. This is the rule that defeats "I have high reputation, skip validation": only fresh Proof/Stake/Constraint raise the gate, and (per §16.7) the highest-stakes actions admit *only* fresh history-decoupled Proof+Stake.

```jsonc
TrustSignal {
  signal_id:   CID,
  class:       enum { BRIEF, CLAIM, PROOF, STAKE, REPUTATION, CONSTRAINT },
  subject_did: DID,
  predicate:   string,
  evidence_ref: CID?,                 // the underlying artifact (inclusion proof, VC, attestation)
  freshness_ts, expiry_ts,
  taint:       { integrity, confidentiality },   // IFC lattice label (doc 04 / doc 07 trust labels)
  verifier_did: DID?,                 // who verified, if a Proof
  sig
}
SignalBundle {
  request_id, subject_did,
  signals: [TrustSignal],
  provided_assurance: int,            // counts ONLY PROOF + STAKE + CONSTRAINT
  bundle_taint: lub(taints)           // least-upper-bound over the IFC lattice
}
// RaisingPower lookup (compile-time constant):
//   BRIEF:0  CLAIM:0  PROOF:+  STAKE:+  REPUTATION:friction-only  CONSTRAINT:+(blast-radius)
```

---

## 16.3 Authenticator (fast path) — one-round-trip identity, zero issuer call

The "rapid" half. Identity is established in a single round trip; only authorization is slow. This reuses the v1 Akasha-Sutra identity layer (doc 04 §4.6) **verbatim** and adds only a uniform fast handshake.

- **Cross-boundary:** the party presents its W3C DID + a **freshness challenge-response** (proves DID control by asking its TEE/HSM signer to sign a nonce — doc 04 Protocol B step 2) + its capability VCs, verified **locally** against the issuer's published key and a **cached revocation accumulator** — *no online issuer call on the hot path*.
- **Local / in-runtime:** SPIFFE node+workload attestation issues a short-lived (~1 h) auto-rotating **SVID** for mTLS; **no static secrets**, blast-radius bounded (doc 04 §4.6).
- **Custody:** keys live in the TEE/HSM/SPIRE side-module the model cannot reach (doc 04 load-bearing custody rule). A prompt-injected model can **request** a signed handshake but cannot forge or exfiltrate identity.

**Authentication grants identity ONLY — zero authority.** A perfectly-authenticated agent still starts at **T0** for any capability it has not earned standing in.

```jsonc
AuthHandshake {
  challenger_did, subject_did, nonce,
  did_proof_sig,                       // signer-produced; proves DID control, no issuer round-trip
  vc_set: [CapabilityVC],              // verified locally vs issuer pubkey + pinned revocation snapshot
  svid?: SPIFFE_SVID,                  // local runtime mTLS
  revocation_snapshot_ref: CID,        // see the staleness SLA below
  verified: bool, latency_ms
}
AuthResult { subject_did, identity_assured: bool, NO_authority: true }
```

### Revocation-snapshot staleness — bounded by an explicit SLA, escalated for high stakes (safety fix)

Checking revocation against a snapshot pinned in the last-trusted checkpoint avoids an issuer round-trip but introduces a **two-sided** risk: a freshly-revoked credential could pass until the next checkpoint refresh (false-negative), and a stale snapshot could false-positive-revoke a still-valid credential, **feeding the free-demotion engine** (a demotion-storm vector — see §16.5). The trade-off is bounded, not waved away:

| Action criticality | Revocation freshness rule |
|---|---|
| ROUTINE / Class A | Pinned snapshot accepted; **max staleness SLA** `Δ_rev` (a published, transparency-logged bound, e.g. one checkpoint interval). A snapshot older than `Δ_rev` is treated as *unavailable* → fail-up to a step-up demand, not a silent pass. |
| SENSITIVE / Class B | Snapshot accepted only if age < `Δ_rev / 2`; else an **online revocation re-check** is required before grant. |
| CRITICAL / IRREVERSIBLE / Class C/D | **Online revocation re-check is mandatory** — the pinned snapshot is never sufficient for a high-stakes action. A revoked VC surfaces as a *loud verification FAIL*, never a stale pass. |

A **false-positive revocation** (stale snapshot wrongly marks a valid credential revoked) is routed to the demotion-storm guard (§16.5) as a *candidate poisoning signal* rather than executed blindly when it arrives correlated across many DIDs. `Δ_rev` is an uncalibrated set-point shipped behind shadow-mode and conservative defaults (§16.10 open problem 2).

---

## 16.4 Progressive Authorizer (slow path) — NIST 800-207 PE/PA/PEP in the Aegis chokepoint

The "authority" half, where the unconflation lives. **This is not a new gate** — it plugs into stages (a)/(b)/(d) of the existing doc-08 §8.2 pipeline. Three NIST-800-207 logical components mapped onto v1:

```
ActionEnvelope (doc 08 §8.2)
        │
        ▼
 (PE) POLICY ENGINE  ── co-located with the Yama OPA/Rego floor (doc 08 stage a / doc 03)
        │   Yama FAIL → short-circuit, non-overridable (doc 03 lexicographic floor)
        │   Yama PASS → required_assurance = f(criticality, risk_class)
        │              (doc 08 §8.4 resolver: ambiguity resolves UPWARD; unknown cap → IRREVERSIBLE)
        ▼
 compare  required_assurance   vs   provided_assurance(bundle)
        │                            ^ counts ONLY Proof + Stake + Constraint
        │                              REPUTATION enters ONLY as friction_discount, capped,
        │                              and ZERO for Class C/D (§16.7 high-stakes decoupling)
        ▼
 (PA) POLICY ADMINISTRATOR  ── mints a short-lived, capability-scoped, single-use/short-TTL
        │   attenuable grant (macaroon-style caveats) ONLY when required is met by fresh signals.
        │   The grant is NEVER reused across requests; nothing persists.
        ▼
 (PEP) POLICY ENFORCEMENT POINT  = the doc-08 §8.2 Aegis interceptor (no direct tool socket;
        every consequential action passes the seam or fails closed)
```

The decision is **per-request and stateless**: trust does not accumulate between requests. Reputation's effect is bounded so it can lower required-`k` **by at most 1** and **never below the per-criticality floor**, and it **cannot apply at all for Class C/D**. The **Rule-of-Two** sizing law (a net-new import from the research lead — see §16.5) is encoded here.

```jsonc
AccessRequest {
  request_id, subject_did, capability, args_cid,
  bundle: SignalBundle, criticality, risk_class, taint
}
AccessGrant {              // short-lived, never reused
  grant_id, subject_did, capability_scope, ttl, single_use: bool,
  attenuations: [caveat], minted_by_PA_sig
}
StepUpDemand {
  request_id, missing_assurance, required_classes: [PROOF|STAKE|CONSTRAINT],
  fresh_required: bool, reason
}
PEDecision {
  request_id, floor_result, required_assurance, provided_assurance,
  friction_discount_applied, rule_of_two_count,
  disposition ∈ { GRANT, STEP_UP, HUMAN_GATE, DENY }, sig
}
```

---

## 16.5 The Trust Ladder T0→T3, the fail-safe asymmetry engine, and the cross-domain rules

The ladder makes "how much do we trust this party for this topic" an explicit, auditable, **monotone-demotable** state. It is **not a parallel privilege system** — it is a *friction/eligibility lens* over v1's existing risk-class authority ceilings (doc 03 §4). The ladder NEVER unlocks an authority v1 forbids.

| Rung | Meaning | Eligible to self-serve | Friction posture |
|---|---|---|---|
| **T0** | untrusted / new identity | Class-A reversible only | max monitoring, max step-ups (doc 02 §2.6.2 cold-start probation maps here) |
| **T1** | basic verified | Class-A fluid; Class-B with maker-checker | standard |
| **T2** | established competence | Class-B fluid; **Class-C still human-gated** | reduced step-ups within A/B |
| **T3** | high standing | reduced friction across A/B; **Class-C with lighter (not absent) step-up** | lightest monitoring within tier |

**Hard boundary, restated from doc 03:** **the ladder NEVER unlocks Class-D autonomy.** Class-D is always human-per-action regardless of rung. Class-C always retains a human gate; T3 lightens it, never removes it.

### Promotion (gated) vs Demotion (free)

```
PROMOTION:
  require ≥ k_promote (≥2, rises with target tier) candidate signals of class {PROOF, STAKE}
  that are ALL: (a) inside the freshness window, (b) all-passing,
                (c) effective-independence ≥ required
  independence is measured by the v1 anti-collusion diversity metric (doc 08 §8.6 diversity_distance)
  → two correlated proofs collapse toward ONE effective signal.
  Emit a witness-cosigned PromotionEvent raising the rung by exactly one.

FRESHNESS DECAY (continuous):
  signals past their window expire; if promoting support drops below threshold the rung
  DECAYS toward T0. NO PASSIVE TENURE — standing is continuously re-earned
  (defeats reputation-milking-by-idling).

DEMOTION:
  ANY single anomaly { floor near-miss, failed maker-checker, doc-08 §8.9 collusion flag,
                       CID mismatch, revoked VC, out-of-baseline behavioural score }
  drops the rung IMMEDIATELY — no quorum, no pre-effect appeal. New (lower) eligibility
  takes effect on the very next request. Appeal is POST-HOC via the repair ledger (§16.6).
```

### The unified cross-domain engine — and the two carve-outs the red-team requires

The **same engine instance** governs human operators, machine agents, replicas, and inter-swarm peers. *The cross-domain unification is the novel part — not the asymmetry itself, which is doc-00 §3.8 / doc-08.* But "free instant demotion applied to everyone" has two failure modes that must be designed against, not discovered in production:

**(1) Human-floor exception — demotion may never strip the recovery/halt capability of a verified human principal (binding invariant).**

v1's graceful-degradation controller (doc 03 §8) assumes the human is the **recovery actor**, not a demotable subject. A transient hardware-key failure, a stale revocation snapshot (§16.3), a fat-fingered approval, or an adversary manufacturing one cheap anomaly against an operator could otherwise demote *the only human able to authorize re-promotion or reach the Vishnu halt path* — precisely when intervention is most needed. Therefore:

- A human operator may be demoted in **operational standing** (e.g. lose frictionless Class-C approval authority) but **never below the rung required to (a) authorize their own step-up re-promotion via a fresh independent factor (hardware key + out-of-band channel) and (b) reach the Vishnu halt path (doc 03/doc 08).**
- **Human demotions are witness-cosigned** (doc 04 human-offline-key witness), extending the v1 rule that human *approvals* are witness-cosigned (doc 04 §4.4.2) to human *demotions*. A single anomaly cannot unilaterally lock out a human principal; the witness quorum must co-sign the demotion event.

```jsonc
HumanFloorInvariant {
  principal_did,
  min_rung_preserved: { self_step_up_reachable: true, vishnu_halt_reachable: true },
  demotion_requires_witness_cosig: true        // doc 04 human-offline-key witness
}
```

**(2) Demotion-storm loop-breaker — adopt doc-03 §8's controller at the ladder layer (net-new wiring of an existing v1 mechanism).**

Because demotion is free and instant, an attacker who manufactures cheap anomalies (or a stale-revocation false-positive cascade, §16.3) could **mass-demote honest agents to T0 and stall the swarm**. This is the *safe* direction for safety (the swarm halts rather than acts wrongly) but is a genuine **liveness attack surface**. v1 already solved the structurally-identical positive-feedback availability-collapse (doc 03 §8: lowering autonomy reclassifies more work upward → deeper queue → more caution → cascade). We adopt its loop-breaker at the ladder:

- **Rate-limit and depth-cap** demotion-triggered re-gating per window (doc 03 §8 "caution-raising is rate-limited and capped").
- **Distinguish** `demoted-and-recovering` (shed / queue; preserve the **guaranteed Class-A reversible lane** of doc 03 §8) from `demoted-hostile` (hard).
- **Preserve a guaranteed-available reduced-capability lane** so a demotion storm degrades throughput **without total halt** — the doc-03 §8 liveness floor.
- **Mass-correlated demotion events** (same trigger signature across many DIDs within a window) **raise a poisoning/health flag to the immune system (doc 06)** rather than silently executing — the demotion is held pending health triage when the signature is suspiciously uniform.

This converts the §16.10 "demotion-storm" open problem from *unresolved* into *bounded, designed behaviour*, keeping the SAFE direction (halt) while protecting liveness — exactly as doc-03 §8 does. **Honest residual (§16.10):** rate-limiting demotion triggers *without* re-introducing a slow-to-demote vulnerability is a genuine tension; the safe direction is preserved, full throughput under a determined poisoning attacker is not guaranteed.

### Replica lineage rung-cap — a NET-NEW addition, composed with (never replacing) the spawn-token lifecycle

**Flagged honestly: neither "parent−1 rung inheritance" nor the Rule-of-Two exists in v1.** The Rule-of-Two is imported from the research lead; the lineage rung-cap is invented here. Both are good additions, not reuses, and are labelled as such.

A replica inherits its lineage rung **capped at `parent_rung − 1`** and must re-earn standing via the gated promotion path. Concretely, composed with the gated-replication control plane:

- The parent rung is **read at spawn time** by the quorum-cosigned Replication Authority and written into the spawn token alongside the existing generation-count / lease / capability-scope fields. The rung-cap is **one caveat on the spawn token, not a standalone control**.
- A replica that inherits **T0** (because its parent was T1) may **self-serve only Class-A reversible ops** and must climb via fresh independent Proofs like any new identity.
- **The rung-cap MUST NOT be the sole control.** It composes with — never replaces — the capability-scoped, generation-counted, lease-bound spawn token. Just as a replica cannot mint its own spawn authorization or survival credential, **it cannot mint its own standing**: Standing-`R` is earned through checker-verified outcomes logged in the fabric, and a replica's promotion signals are subject to the same diversity-independence collapse (a replica and its parent share lineage, so their endorsements correlate and collapse toward one effective signal — a Sybil-via-replication defence that falls directly out of §16.7(d)).

```jsonc
LineageCap {
  replica_did, parent_did,
  rung_cap: parent_rung − 1,
  spawn_token_ref: CID,                 // the generation-counted/lease-bound token (NOT replaced)
  must_reearn_via: GATED_PROMOTION
}
```

### AutonomyClass join — exact v1 enum, marked as a proposed §8.8 amendment (minor fix)

The ladder rung is a **second input** to doc-08 §8.8 autonomy-class derivation, which today derives from `{internals_exposed, attestation_present, tier2_active}` only. Using the **exact v1 enum names** (`GATED_STD`/`GATED_HIGH`, *not* `STD`/`HIGH`) and stating the join explicitly:

```
AutonomyClass ∈ { OBSERVE_ONLY, GATED_LOW, GATED_STD, GATED_HIGH }     // doc 08 §8.8 — unchanged

PROPOSED §8.8 amendment (Class B; not existing wiring):
  autonomy_class = MIN( openness_ceiling_from_§8.8 ,  rung_ceiling_from_ladder )
```

i.e. **a closed/un-attested model AND a low ladder rung both cap; neither can raise the other.** This is the conservative `MIN`: the model-openness contract and the ladder are each a *ceiling*, and the lower wins. This is presented as a **proposed amendment to the §8.8 derivation signature**, not as already-wired behaviour.

```jsonc
LadderState {
  subject_did, topic_scope, rung ∈ {T0,T1,T2,T3},
  eligible_risk_classes: [A..C],          // never D via the ladder
  freshness_deadline_ts, promoting_signals: [CID],
  last_anomaly_ref: CID?, decay_curve
}
PromotionEvent { subject_did, from_rung, to_rung, k_fresh_signals, independence_score, all_passed: bool, witness_cosig }
DemotionEvent  { subject_did, from_rung, to_rung, trigger_anomaly: CID, instant: true,
                 witness_cosig?: bool /* true iff subject is a human principal */ }
```

---

## 16.6 The Receipts Handshake — audit-fabric-as-trust-accelerant (the primary novelty)

Two parties reach working trust in **one exchange** by **verifying rather than believing** — turning the v1 tamper-evident log (doc 04) from a forensic afterthought into the fastest legitimate live trust primitive, at **zero cost to the security floor**. This is what reconciles the doc-00 rapid-trust-vs-security tension without lowering the floor: trust is rapid *precisely because it is verified*, not because anything is relaxed.

On contact, a party offers a **RECEIPTS BUNDLE**:

```
 RECEIPTS BUNDLE (offered by A)                    VERIFICATION (by B, zero trust in A's service)
 ┌────────────────────────────────────────┐       ┌──────────────────────────────────────────────┐
 │ (1) DID freshness-proof                 │  ───▶ │ verify nonce sig vs A's DID doc (identity)     │
 │ (2) INTACT-FLOOR PROOF:                 │  ───▶ │ recompute invariant-region hash; check boot-   │
 │     { invariant_region_hash, boot_sig,  │       │ sig vs canonical floor (doc 03 IMMUTABLE       │
 │       genome_version }                  │       │ region; fail-closed boot — doc 03 §5)          │
 │ (3) SCOPED AUDIT SLICE:                 │  ───▶ │ rebuild O(log n) inclusion proofs LOCALLY from │
 │     [TileInclusionProof] over a window  │       │ immutable CID-addressed tiles vs B's OWN       │
 │ (4) witness-cosigned checkpoint         │  ───▶ │ last-trusted witness-cosigned checkpoint       │
 │     { tree_size, root_hash, [WitSig] }  │       │ (doc 04 §4.3/§4.4 — A CANNOT equivocate per-   │
 │ (5) reputation inclusion-proofs (topic) │  ───▶ │ client; tiles are immutable + root-pinned)     │
 │ (6) ZK compliance-proof? (voidable on   │  ───▶ │ verify predicate (e.g. "passed current safety  │
 │     floor-violation)                    │       │ battery") WITHOUT revealing payload            │
 └────────────────────────────────────────┘       └──────────────────────────────────────────────┘
```

Each receipt is a **PROOF-class signal**, so a valid bundle satisfies a chunk of `required_assurance` **instantly**. The receiver trusts **nothing** in the offerer's online service: tile verification is pure-functional against the receiver's *own* checkpoint (doc 04 §4.3 — "the writer cannot equivocate per-client"). The intact-floor proof reuses the doc-03 immutable-region / fail-closed-boot property as a *receipt* — a correct, non-trivial repurposing.

**Progressive disclosure (safety-redline; doc 08 §8.10 capability-discovery-leakage defence).** The audit slice and capability set revealed **scale with the verified tier of the counterparty**. The full catalog is **never** exposed to a discoverer. A T0 stranger gets identity + intact-floor proof only; deeper slices unlock as the counterparty climbs the *local* ladder.

```jsonc
ReceiptsBundle {
  offerer_did, did_freshness_proof,
  intact_floor_proof: { invariant_region_hash, boot_sig, genome_version },
  audit_slice: [TileInclusionProof],
  witness_cosigned_checkpoint: { tree_size, root_hash, [WitnessSig] },
  reputation_proofs: [CID],
  zk_compliance_proof?: { predicate, proof, voidable_on_floor: true },
  disclosure_tier
}
TileInclusionProof { leaf_cid, tile_path: [CID], root_hash }      // RFC-6962-style, verified locally
VerifyReceipts(bundle, my_last_trusted_checkpoint)
  → { identity_ok, floor_intact, audit_consistent, reputation_verified, assurance_contributed }
```

### Show-Your-Receipts Trust Repair (after error/demotion) — evidence, not apology

Symmetric for machines and for the swarm↔human relationship. After an error, the **demotion fires first** (asymmetry) — trust falls before repair begins. Then the party assembles a **RepairRecord**:

1. The **signed audit entry** of the failure (root cause) from the fabric.
2. A **demonstration of corrected behaviour** on a comparable task, itself checker-verified.
3. The **inclusion proof** that the correction is logged (doc 03 §13 correction-ledger / reparative action-class).

The counterparty (or, for humans, Narada) **verifies the RepairRecord** against the witness-cosigned checkpoint (verify-not-believe). For humans, Narada presents corrected-behaviour + the audit entry, explicitly **NOT an apology**. The **recurrence-of-fault metric** (doc 03 §13, open problem 10) is checked: repeated "disclosed-then-repaired" of the *same fault class* raises a laundering flag and **blocks further frictionless repair**. If repair verifies and recurrence is within bound, the party re-enters the **gated promotion path** to climb back — it does **not** auto-restore to its prior rung.

```jsonc
RepairRecord {
  error_ref: CID, root_cause,
  corrected_behavior_demo: CID,        // checker-verified
  audit_inclusion_proof: CID,
  recurrence_count, NOT_an_apology: true
}
```

---

## 16.7 Anti-Milking & Reputation-Laundering Guard

Four mechanical rules, each enforced by a component above, collected here as the named guard. They close the specific attacks the unconflation is designed to defeat.

**(a) High-stakes history-decoupling (the core anti-milking primitive).** For any **Class-C/D or IRREVERSIBLE** action, the Authorizer admits **only fresh Proof+Stake+Constraint** and forces **`friction_discount = 0`**. Accumulated history buys **nothing** where it matters most, so a milked reputation (cheap standing, cashed on a dangerous action) cannot be spent.

```jsonc
HighStakesPolicy {
  trigger: criticality ∈ {CRITICAL, IRREVERSIBLE} ∨ risk_class ∈ {C, D},
  reputation_discount: 0,
  require_fresh: [PROOF, STAKE],
  history_decoupled: true
}
```

**(b) Topic-scoping + KYA-binding.** Standing-`R` is valid only within its earned topic and bound to the DID (doc 01 §2 "Know Your Agent"; doc 02 whitewash defence — reputation keyed to persistent DID, zero on any new identity). Cross-topic and cross-DID transfer **return zero**. Standing at code-review cannot be laundered into authority at financial-irreversible-ops.

**(c) Imported-reputation admission gate (defeats the "35% laundering" attack).** An inter-swarm peer's portable reputation passes the **ethical-floor admission precondition FIRST** — it can never bypass the floor (a floor-incompatible peer is refused regardless of standing). Then it is **re-verified via its underlying inclusion proofs** (verify-not-believe), accepted **topic-scoped + DID/KYA-bound** only, and admitted **as friction only, capped** — never as privilege. See §16.9 for the inter-swarm protocol and the **DID-domain-discounted cap** (safety fix).

**(d) Sybil / correlation damping.** Promotion independence is measured against the diversity metric (doc 08 §8.6), so **N sock-puppet endorsements sharing a lineage/model collapse to ~1 effective signal**. A Sybil cannot manufacture the *k fresh independent* Proofs promotion requires. (This is the same mechanism that caps a replica's ability to boost its own parent's standing — §16.5.)

```jsonc
ImportedRepGate {
  peer_did, floor_admission_passed: bool,
  reverify_via_inclusion_proofs: bool,
  admitted_as: friction_only,
  privilege_raise: forbidden,
  domain_discount: float                // §16.9 — foreign-domain trust discount on the cap
}
IndependenceScore {
  signals: [CID], effective_count,       // after diversity/correlation collapse
  sybil_suspected: bool
}
```

> **Safety note — the shared diversity-metric dependency (honest).** Both promotion-independence (§16.5) **and** reputation-friction (§16.7d) rest on the *same* diversity metric. A **single diversity-metric failure degrades BOTH defences simultaneously** — the same hidden-shared-root pathology doc 02 §2.3 / §2.9-prob-2 flags for the verifier layer and doc 04 §4.15-prob-2 flags for consensus. A well-resourced multi-*model* Sybil (genuinely distinct lineages) can both manufacture the `k` fresh independent promotion signals **and** accumulate friction-reducing reputation across topics, compounding two weaknesses that are *not* independent. The guard defeats cheap sock-puppets; **no game-theoretic bound is claimed** against a well-resourced multi-model Sybil (§16.10 open problem 5).

---

## 16.8 Human Trust Interface — Calibration, Lies-in-the-Loop-proof gates, Repair (Narada)

The human mirror of the machine ladder, living in the Narada interface layer (doc 08). Three binding behaviours.

**(1) Calibrated disclosure.** Every output and every gate surfaces the swarm's **confidence, residual uncertainty, and explicit limitations** (doc 08 §8.5 honesty-form: assertion-vs-belief tagging, honest rung-tags) so the human's trust tracks the system's *actual reliability* rather than its fluency.

**(2) Actual-operation gates (Lies-in-the-Loop defence).** A HITL gate **NEVER shows a natural-language summary**. It shows the **ACTUAL low-level operation** — recipient, URL, payload, capability scope, irreversibility, taint of inputs — content-addressed so **what the human approves is cryptographically the thing executed**. Approval is over a **CID, not over prose** a deceiver could spin. The gate fires only for genuine **Rule-of-Two-violating** / **Class C-D** actions, so scarce human attention is reserved (deterministic capability + IFC-taint controls handle the rest — defeating approval fatigue / rubber-stamping).

> **The Rule of Two (net-new import from the research lead; objective HITL-sizing law).** Any operation may hold at most **2 of 3** of `{ untrusted-input (taint), sensitive-access/capability, state-change/irreversibility }`. Holding **all 3 REQUIRES a human gate**, regardless of any assurance score, rung, or reputation. This is *not* a v1 mechanism; it is flagged as a new addition and encoded in the Authorizer (§16.4) as `rule_of_two_count`.

```jsonc
GateDisplay {
  action_cid,                          // approval is over THIS exact CID
  capability, recipient, url, payload_preview, scope, irreversibility,
  input_taint, rule_of_two_count,
  confidence, uncertainty, limitations,
  approve_is_over: CID
  // NO natural_language_summary field is permitted to exist on this struct, by construction
}
CalibrationTag { span, level ∈ {assertion, belief}, evidence_ref, rung_tag, classifier_rung, agree: bool }  // doc 08 §8.5
```

**(3) Evidence-based repair.** After an error or demotion the swarm offers the **signed audit entry of what failed**, the **corrected behaviour demonstrated**, and the **inclusion proof** the correction is logged — not apologies (§16.6). Trust repair is itself a "show-your-receipts" act, with the recurrence-of-fault guard against laundering.

Narada also runs the human's **own** ladder: a human operator authenticates via DID/hardware-key + step-up; high-stakes Class-C/D human approvals **and** human demotions are witness-cosigned (doc 04 human-offline-key witness; §16.5 human-floor invariant).

> **Honest limitation carried (safety).** Calibrated disclosure helps but does **not guarantee correct human trust**: LLM self-reported confidence is poorly calibrated and **gameable** — a scheming agent can emit perfectly-formed honesty tags over false content (doc 08 §8.5 / doc 08 §8.13-risk-3 are explicit that form-checks "provably cannot catch a faithful-looking lie"). The actual-operation CID gate defends the **high-stakes tail**; routine over-trust on un-gated Class-A actions **remains** (§16.10 open problem 3). The calibration claim must not be read as closing it.

---

## 16.9 Inter-Swarm Imported-Reputation Admission (no-laundering, no-floor-bypass)

How a federated peer's portable reputation is admitted without "high-rep ⇒ skip validation" bypassing the floor. Handled at the relay/firewall boundary (the Inter-Swarm-Envoy), with ecosystem-benefit as an **explicit checked invariant** (verified + logged positive-sum for declared principals, and *not* a coalition against any party's principal — collusion is first-class).

```
1. Peer presents portable reputation via inclusion proofs from ITS fabric + AgentCard/value/KYA exchange.
2. ADMISSION FIRST: the ethical-floor admission precondition is evaluated. Reputation CANNOT bypass it.
   A floor-incompatible peer is refused regardless of standing.
3. Re-verify the imported reputation against its underlying inclusion proofs (verify-not-believe);
   accept topic-scoped + DID/KYA-bound ONLY.
4. Admit as FRICTION ONLY, capped — and DID-DOMAIN-DISCOUNTED (see below); never as privilege.
   The peer still climbs the LOCAL ladder via fresh LOCAL Proofs to gain ANY authority.
5. All inter-swarm credible-commitment devices (bonds, ZK proofs) are recorded VOIDABLE-on-floor-violation
   (no commitment unbreakable by Yama-FAIL / Vishnu-halt). Progressive capability disclosure scoped to
   the peer's verified LOCAL tier — never the full catalog.
```

> **Safety fix — the import cap must be DID-domain-discounted, not a single global cap.** Re-verifying foreign inclusion proofs proves the records **exist and are internally consistent** — *not* that the foreign governance was honest or its competence-weighting comparable to ours. A **malicious-but-internally-consistent foreign fabric** can present valid inclusion proofs that inflate a peer's friction discount up to a global cap. Floor-first admission and friction-only limit blast radius, but for an inter-swarm peer **even reduced friction on a borderline Class-B action is a privilege-adjacent effect.** The cap is therefore a function of the **trust we hold in the issuing domain**: an untrusted foreign domain → **near-zero** discount; a domain with which we share a verified external anchor or prior audited history → a higher (still capped) discount. `friction_discount_cap(peer) = base_cap × domain_trust(issuing_did_domain)`. This bounds the laundering surface to the discount the *domain* has earned, not a flat allowance. **Residual (§16.10 open problem 1):** cross-domain reputation commensurability is not solved — a malicious-but-consistent log can still inflate up to its domain-discounted cap.

---

## 16.10 Failure modes addressed (with the precise mechanism and the honest residual)

| Failure mode | Defended by | Honest residual |
|---|---|---|
| **Reputation-milking** (cheap standing, cashed on a dangerous action) | High-stakes history-decoupling (§16.7a): Class C/D / IRREVERSIBLE force `friction_discount=0` + fresh Proof+Stake | none for the high-stakes path; routine over-trust persists on un-gated Class-A (below) |
| **Reputation-laundering** ("high-rep ⇒ skip validation"; the 35% attack) | Imported-rep gate (§16.7c/§16.9): floor-admission first, re-verify via inclusion proofs, topic+KYA-bound, friction-only, **domain-discounted cap** | cross-domain commensurability unsolved (open problem 1) |
| **Privilege-via-trust conflation** (v1's single scalar) | Structural unconflation: **Standing-`R` has no interface method returning a privilege grant**, only a capped `friction_discount` (§16.0/§16.1/§16.7) | guarantee is about Standing-`R`'s interface only; v1 Competence-`R` paths still read authority by design (§16.1) |
| **Lies-in-the-Loop** (confident NL summary approves a harmful action) | Actual-operation CID gate (§16.8): no `natural_language_summary` field exists; approval is over the executed CID | depends on the human reading the low-level fields; fatigue on volume (mitigated by Rule-of-Two reservation) |
| **Approval fatigue / rubber-stamping** | Rule-of-Two sizing reserves human gates for genuine 2-of-3 / Class C-D actions; deterministic capability + IFC handle the rest | Rule-of-Two thresholds uncalibrated (open problem 2) |
| **Sybil / sock-puppet promotion** | Promotion needs `k` fresh **independent** signals; diversity metric collapses correlated/same-lineage endorsements to ~1 (§16.7d) | well-resourced multi-*model* Sybil not caught; shared diversity-metric dependency (§16.7 note) |
| **Stolen static secret / credential replay** | SPIFFE short-lived auto-rotating SVIDs + DID freshness-challenge + keys in TEE/HSM side-module (§16.3) | TEE root-of-trust dependency (inherited, doc 04 §4.15-prob-7) |
| **Stale/revoked credential silently passing** | Revocation staleness SLA `Δ_rev`; online re-check mandatory for Class C/D; CID-addressing turns stale reads into mismatches (§16.3) | within-`Δ_rev` window for Class A; false-positive cascade routed to demotion-storm guard |
| **Per-client equivocation by a party offering its own audit** | Receipts handshake serves **immutable CID-addressed tiles** verified locally against the receiver's own witness-cosigned checkpoint (§16.6; doc 04 §4.3) | none for published history (inherits doc 04 residuals) |
| **Over-trust built on fluency** | Calibrated disclosure surfaces confidence/uncertainty/limits + honest rung-tags (§16.8) | LLM confidence is gameable; routine Class-A over-trust remains (open problem 3) |
| **Laundering repeated violations as "disclosed-then-repaired"** | Recurrence-of-fault metric blocks frictionless repair of a repeated fault class; re-entry via gated promotion, not auto-restore (§16.6) | threshold/gaming-resistant parameterization open (doc 03 open problem 10; open problem 4) |
| **Standing-hoarding / self-preservation drift** | Freshness decay: idle standing decays toward T0; no passive tenure (§16.5) | decay-curve set-point uncalibrated (open problem 2) |
| **Inter-swarm commitment used to bind against the floor** | All credible-commitment devices VOIDABLE-on-floor-violation by construction (§16.9) | none — voidability is structural |
| **Human lockout / demotion of the recovery actor** | Human-floor invariant: demotion never strips self-step-up + Vishnu-halt reachability; human demotions witness-cosigned (§16.5) | depends on the human-offline-key witness (inherited, doc 04 §4.15-prob-9) |
| **Demotion-storm liveness attack** | doc-03 §8 loop-breaker at the ladder: rate-limit/depth-cap, guaranteed Class-A lane, mass-correlated demotions flag the immune system (§16.5) | rate-limiting without re-introducing slow-to-demote is unresolved (open problem 8) |

---

## 16.11 Interfaces to the v1 subsystems

| Other subsystem | Contract |
|---|---|
| **Yama — deterministic policy floor (doc 03)** | The Progressive Authorizer's **Policy Engine is co-located with and subordinate to** the Yama OPA/Rego floor: **Yama FAIL is evaluated FIRST and is non-overridable** (doc 03 lexicographic floor); access decisions run only on Yama-PASS. A floor near-miss is one of the free-demotion anomalies. The floor's **INVARIANT region** is what the intact-floor receipt proves (§16.6). Honesty-form checks (assertion/belief, rung-tags; doc 03 §6) feed the calibration disclosure (§16.8). **Risk classes A/B/C/D (doc 03 §4) ARE the ladder's eligibility targets** — the ladder is a friction lens over the floor's authority ceilings, never a parallel privilege system. The doc-03 §8 graceful-degradation controller is the source of the §16.5 demotion-storm loop-breaker, and the §16.5 human-floor invariant protects doc-03 §8's assumption that the human is the recovery actor. |
| **Akasha-Sutra — provenance, identity & consensus fabric (doc 04)** | Consumes the v1 identity layer **verbatim** (DID + capability VCs cross-boundary; SPIFFE/SVID local; keys in the TEE/HSM side-module that re-checks capability before signing — doc 04 §4.6). Standing-`R` records and receipts-handshake audit slices **ARE tile-Merkle inclusion proofs** against the witness-cosigned checkpoint (doc 04 §4.3/§4.4); the reputation ledger is a **cache of fabric inclusion proofs, never a free-floating score**. Promotion/demotion events and `PEDecision`s are emitted to **Chitragupta (the exclusive writer) BEFORE action**; promise-of-inclusion receipts (doc 04 §4.4.3) cover them. High-stakes human approvals **and human demotions** are witness-cosigned with the human-offline-key witness (doc 04 §4.4.2). **This subsystem WRITES nothing to the log directly** — it produces records Chitragupta appends. The revocation snapshot is the doc-04 §4.6 verifiable RevocationMap, pinned in the last-trusted checkpoint with the §16.3 staleness SLA. |
| **Aegis & Narada — safety control + interface (doc 08)** | The **Aegis Chokepoint Interceptor IS this subsystem's PEP** — no separate gate is introduced; the Progressive Authorizer plugs into stages (a)/(b)/(d) of the doc-08 §8.2 pipeline (floor → criticality resolver → disposition). `AutonomyClass` is derived jointly from the doc-08 §8.8 model-openness contract **AND** this subsystem's ladder rung via the proposed `MIN(openness_ceiling, rung_ceiling)` amendment (§16.5; exact enum `GATED_STD`/`GATED_HIGH`). The §8.7 disposition selector's HUMAN-AUDIT band and the Rule-of-Two human gate are realized through Narada's Human Trust Interface (actual-operation CID display, §16.8). **Reputation slashes from doc-08 §8.9 collusion findings feed this subsystem's demotion engine**; this subsystem's ladder rung feeds the §8.8 autonomy-class derivation. The maker-checker **`diversity_distance` (doc 08 §8.6) is the independence metric the promotion engine reuses** (§16.5/§16.7d). |
| **Cooperation / anti-collusion (doc 02) + Self-evolution & immune system (doc 06)** | **Reputation is Competence-`R` for matching/eligibility (doc 02 §2.6, unchanged) and Standing-`R` for friction (new, §16.1).** Both are **competence-weighted, never capital-weighted** (doc 02 anti-Bittensor invariant) using the cooperation layer's welfare-conditioned outcome signals; neither rewards bare agreement. Collusion-audit verdicts (cross-run MI, permutation-invariance; doc 02 §2.6 / doc 08 §8.9) are demotion triggers and Competence-`R` slashes. Promotion-signal independence is measured against the same diversity dials (`c1/c2`, doc 02). **Replicas inherit a lineage-capped rung (parent−1) and must re-earn standing** — binding the trust ladder to the gated-replication red-lines (a replica cannot mint its own standing, just as it cannot mint its own spawn token; §16.5). The doc-06 immune-system behavioural-anomaly baselines are a demotion-trigger source and the recipient of mass-correlated-demotion poisoning flags; baselines re-set only on ratified evolution steps (doc 08 §8.3). |
| **Inter-Swarm federation (Inter-Swarm-Envoy / relay-firewall)** | Imported reputation enters **ONLY** through the §16.9 Imported-Reputation Admission protocol: floor-admission first, re-verify via inclusion proofs, topic+KYA-scoped, friction-only, **DID-domain-discounted cap**. Progressive capability disclosure is scoped to the peer's verified **LOCAL** ladder tier — never the full catalog. All inter-swarm credible-commitment devices are recorded VOIDABLE-on-floor-violation. **Ecosystem-benefit is an explicit checked invariant** before any cooperation grant is issued. |

---

## 16.12 Honest novelty accounting

**The genuinely new contribution is the STRUCTURAL UNCONFLATION of access from reputation enforced as runtime code:** the unconflation is an **interface-discipline invariant enforced by the Authorizer** — Standing-`R` exposes **no method returning a capability or risk-ceiling grant**, lowers required-`k` by **at most 1** and **never below the per-criticality floor**, so "reputation raises privilege" is not a policy one must remember to forbid but an effect the enforced interface bounds out. This is an enforced interface invariant, **not a mechanically-proven type-system property**: as §16.9 concedes, even a capped friction reduction on a borderline action is **privilege-adjacent** — the invariant *bounds* that adjacency, it does not eliminate it. Wrapped around that are four reused-but-newly-wired pieces:

1. The **BCPSRC signal taxonomy** as the schema that decides which evidence may RAISE a disposition vs only reduce friction, with high-stakes actions admitting **only fresh history-decoupled Proof+Stake** (the anti-milking primitive, §16.7a).
2. The **fail-safe asymmetry** (gated-multi-fresh-signal promotion / free-instant-single-anomaly demotion; reputation-buys-friction-not-floor) **lifted into ONE cross-domain engine** applied identically to humans, machines, replicas, and inter-swarm peers — *the cross-domain unification is the novel part, not the asymmetry itself* (which is doc-00 §3.8 / doc-08).
3. **Audit-fabric-as-trust-accelerant** — turning the v1 witness-cosigned tile-Merkle log (doc 04) into the **primary rapid-trust instrument** via the show-your-receipts handshake (intact-floor proof + locally-verified audit slice + reputation inclusion proofs), so a counterparty **verifies rather than believes** — what lets trust be simultaneously rapid **and** zero-cost to the floor.
4. **Lies-in-the-Loop-proof human gates** that approve a **CID-addressed ACTUAL operation**, never a natural-language summary.

**Honest accounting.** The individual primitives — NIST 800-207 PE/PA/PEP, W3C DID/VC, SPIFFE/SVID, RFC-6962 transparency, the Rule-of-Two HITL law, competence-weighted reputation (cf. **AgentBound Tokens** and **AgentReputation**, doc 10 line 130) — are **all prior art and cited as such**. The contribution is the **wiring**: making unconflation an enforced interface-discipline invariant on the *new* Standing-`R` plane (an Authorizer-enforced bound, not a mechanically-proven type-system property; §16.9), unifying the asymmetry across four trust domains, and repurposing the existing audit fabric as the live trust accelerant. The Rule-of-Two and the replica lineage rung-cap are **net-new additions** (the former imported from the research lead, the latter invented here), explicitly **not** pre-existing v1 mechanisms. **This subsystem does NOT "fix v1's single trust scalar"** — it adds a friction-only channel *alongside* v1's authority-bearing Competence-`R`, contingent on the Class-B amendment of §16.1. That composition is **reference-design, time-stamped 2026-06, NOT validated end-to-end** against an adaptive adversary. No "first" or "robust-by-construction" claim is made for the composed loop. The strongest inherited empirical anchor is the doc-08 externally-governed-escalation result (~39% → ~1.2%), covering **only** the HUMAN-AUDIT path; almost everything else is principled assembly awaiting evaluation.

---

## 16.13 Open problems (stated plainly; not solved)

1. **Cross-domain reputation commensurability.** Re-verifying a foreign fabric's inclusion proofs proves the records **exist and are consistent** — not that the foreign governance was honest or its competence-weighting comparable. The friction-only + floor-first admission + **DID-domain-discounted cap** (§16.9) bound the damage but do not solve commensurability: a malicious-but-internally-consistent foreign log can still inflate a peer's friction discount **up to its domain-discounted cap**.

2. **Set-point calibration is unsolved off-the-shelf.** `k_promote`, freshness-window lengths, the `friction_discount` cap, the rung-to-risk-class mapping bands, the decay curve, the revocation staleness SLA `Δ_rev`, and the Rule-of-Two threshold parameters are **first-principles starting values, not tuned constants**. Set wrong, the ladder either over-gates (kills the "rapid" in rapid trust) or under-gates (lets standing accrue too fast). These ship behind **shadow-mode + conservative defaults** (and the §16.1 amendment itself ships in shadow-mode); real tuning is per-deployment empirical work. (Shared with doc 03 open problem 2, doc 04 open problem 2, doc 08 open problem 5.)

3. **Human confidence-calibration is only partially reliable.** Exposing confidence/uncertainty helps, but **LLM self-reported confidence is poorly calibrated and gameable**, and humans systematically over-trust fluent output. The actual-operation CID gate defends the high-stakes tail; **routine over-trust on un-gated Class-A actions remains** (doc 08 §8.13-risk-3).

4. **Recurrence-of-fault laundering guard has a threshold/gaming problem.** A patient adversary can space repeated faults across the recurrence window or vary the fault class to stay under bound. We specify the metric; its gaming-resistant parameterization is **open** (inherited from doc 03 open problem 10).

5. **Sybil-independence is only as good as the diversity metric.** If an adversary controls enough **genuinely-diverse** identities (distinct models/lineages), the effective-independence collapse does not catch them — the guard defeats cheap sock-puppets, **not a well-resourced multi-model Sybil**. **No game-theoretic bound is claimed.** Worse, promotion-independence and reputation-friction **share** this single dependency, so one diversity-metric failure degrades both (the doc 02 §2.3 hidden-shared-root pathology).

6. **Continuous-operation reputation-ledger growth and privacy.** An always-on competence-weighted ledger over inclusion proofs grows unbounded and leaks interaction-pattern/topic metadata. Pruning-without-losing-verifiability and selective (ZK) disclosure of reputation are **reserved/Class-C and not on the hot path** (shared with doc 04 open problems 6/8, doc 08 open problem 9).

7. **The composed loop is reference-design, NOT validated end-to-end.** Every primitive is individually validated; **no one has run this continuous per-interaction unconflated-trust loop against an adaptive multi-agent red team.** The strongest inherited empirical anchor (doc-08 ~39%→~1.2%) covers only the HUMAN-AUDIT path; everything else is principled assembly awaiting evaluation.

8. **Demotion-storm / availability interaction.** Because demotion is free and instant, a poisoning attacker who manufactures cheap anomalies (or triggers a stale-revocation false-positive cascade) could mass-demote honest agents and stall the swarm. The §16.5 loop-breaker (rate-limit/depth-cap + guaranteed Class-A lane + mass-correlated-demotion → immune-system flag, adopted from doc 03 §8) converts this from unresolved to **bounded designed behaviour** — but **rate-limiting demotion triggers *without* re-introducing a slow-to-demote vulnerability is itself unresolved.** The safe direction (halt) is preserved; full throughput under a determined attacker is not guaranteed.

9. **The §16.1 amendment is unratified.** Splitting v1's reputation into Competence-`R` (authority) and Standing-`R` (friction) is a Class-B governance act with a migration touching the allocator, §8.8 derivation, and role-promotion. Until ratified, the entire subsystem is **shadow-mode only**, and the doc-02 §2.9-prob-4 rich-get-richer hazard in Competence-`R` is **neither worsened nor solved** here.
