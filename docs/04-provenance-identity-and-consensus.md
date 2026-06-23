# 4. Provenance, Identity & the Consensus Fabric — *Akasha-Sutra*

> *Akasha-Sutra* — "the thread strung through space." In the Huayan image of Indra's Net, every jewel reflects every other; the net only holds because there is a thread it is strung on. Akasha-Sutra is that thread: the tamper-evident, identity-bearing, lineage-preserving fabric on which every jewel of the swarm is mounted. It is presented here as a coordination-and-integrity substrate, not a metaphysics, and with humility toward the living traditions the name borrows from.

### 4.1 What this subsystem is, and what it deliberately is not

Akasha-Sutra delivers the *one* integrity property a blockchain genuinely provides — **no silent rewrite, no equivocation (split-view), verifiable who-did-what-with-what** — while explicitly rejecting coins, proof-of-work, gas, global Byzantine consensus, and on-chain data. That rejection is not aesthetic. Global Byzantine consensus, mining, and tokens exist to solve *trustless agreement among mutually-hostile strangers at internet scale*. A single-operator, cooperative-but-fallible swarm does not have that problem. Importing the machinery built for it buys a property (no-equivocation) that threshold witness-cosigning over a tile-based Merkle log already delivers at near-zero cost — while paying seconds-to-minutes of latency and inheriting a speculative/oracle attack surface. The research record is blunt about the antipattern: *"cargo-cult blockchain (full distributed ledger / token / heavy consensus) bolted on for buzzword compliance"* adds ops cost without benefit for an internal swarm, and the canonical failure case (a stake-weighted incentive network) shows reward driven by **capital (0.5–0.8 stake→reward correlation), not competence (0.1–0.3)** — the exact authority model this architecture forbids.

So Akasha-Sutra is **competence-weighted, never capital-weighted; tamper-evident without consensus; transparent without a chain.**

It is honest about its own ceiling up front, because the rest of the document depends on it:

- It proves an output **came from a given agent and was not altered**. It does **not** prove the decision was correct, wise, or aligned. (Semantic correctness is the job of the governance floor, the safety battery, and human ratification — Akasha-Sutra makes their verdicts *attributable and unforgeable*, not *true*.)
- Its completeness guarantee (that nothing was silently omitted) holds **only** under two external assumptions, made explicit in §4.9 and §4.11: (a) the runtime mediates every consequential action through the chokepoint, and (b) the non-omission protocol of §4.4 is actually run. Where either fails, integrity covers only the honest path, and we say so.

Five mechanisms compose into one cell. They are individually borrowed and battle-tested (Merkle logs, RFC-6962 tile transparency, witness cosigning, DID/VC, SPIFFE/SVID, geometric-median voting). **The contribution is the integration discipline** — composed so that *only Yama may FAIL, only Chitragupta writes audit, only Vishnu may HALT* become **cryptographic facts rather than conventions**, with a concrete single-operator witness-governance answer, a diversity-gated consensus tier, and a lineage-preserving prune. Closest prior art, named honestly, is in §4.13.

```
                          AKASHA-SUTRA — THE TAMPER-EVIDENT THREAD
  ┌──────────────────────────────────────────────────────────────────────────────┐
  │  producers (untrusted-by-default; keys NOT in the model)                       │
  │  Yama ENFORCE · Vishnu HALT · Evolution EVOLVE · Health REPUTATION/REPARATIVE  │
  │  Consensus-engine CONSENSUS · Identity-layer IDENTITY                          │
  └───────────────┬──────────────────────────────────────────────┬───────────────┘
        DID-signed │ intent (+ promise-of-inclusion receipt)       │ reads (proofs)
                   v                                               │
        ┌────────────────────┐    capability-checked    ┌──────────────────────┐
        │  (5) IDENTITY LAYER │<────── sign requests ───▶│ TEE/HSM signer module │
        │ DID+VC / SPIFFE/SVID│   (re-checks capability)  │ (outside the model)   │
        └─────────┬──────────┘                           └──────────────────────┘
                  │ verified actor + capability
                  v
        ┌──────────────────────────────────────────────┐        ┌──────────────────┐
        │ (1) CHITRAGUPTA EXCLUSIVE-WRITER LEDGER       │        │ (4) CID EVIDENCE │
        │  append-only · hash-chain + Merkle (RFC-6962) │◀──CID──│  STORE (Merkle-  │
        │  no delete/edit/reorder VERB exists           │        │  DAG, encrypted) │
        │  HA: hot-standby + witnessed leader handoff   │        └──────────────────┘
        └───────┬─────────────────────────┬─────────────┘
                │ checkpoints              │ tiles (static, CID-addressed)
                v                          v
        ┌────────────────────┐    ┌──────────────────────────┐
        │ (2) TILE-BASED     │    │ (3) WITNESS COSIGNING     │
        │ TRANSPARENCY       │    │ t-of-w · ≥1 EXTERNAL      │
        │ O(log n) proofs    │    │ ANCHOR · heterogeneous    │
        │ client-side, no    │    │ roots · governance-gated  │
        │ trust in writer    │    │ rotation · consumer policy│
        └────────────────────┘    └─────────────┬─────────────┘
                                    ForkAlarm/OmissionAlarm
                                                 v
                                            Vishnu (HALT)
        ── (6) RISK-TIERED CONSENSUS ENGINE: a SEPARATE coordination subsystem ──
           (decision-voting, NOT ledger replication; see §4.7 and the §4.12 note)
```

---

### 4.2 Component 1 — Chitragupta Exclusive-Writer Ledger

**Role gloss:** *Chitragupta* = the exclusive audit-writer; in the mythic register, the scribe who records every deed and can neither be bribed nor edit the record. Here: the single, authoritative, tamper-evident record of every consequential swarm event.

**Why exactly one writer.** Multiple writers re-introduce the agreement problem (whose append ordered first?) and a co-write-into-inconsistency surface. One writer, whose write-scope sits **cryptographically outside every monitored agent**, is the spine of the "who audits the auditor" answer: a monitored agent has *no capability path* to forge audit.

**Structure.** Append-only log. Each leaf is a canonicalized `AuditRecord`; internal nodes are `SHA-256(leaf/node-prefix || left || right)` with RFC-6962 domain-separation prefixes (`0x00` leaf, `0x01` node) to block second-preimage attacks. The Merkle Tree Hash commits the whole log (O(log n) inclusion/consistency proofs). A **parallel per-record hash chain** (`record.prev_hash = H(immediately-preceding record)`) gives cheap **O(1) local** tamper detection in addition to the tree proofs — any altered past entry breaks every downstream `prev_hash`.

**The capability is verbs, not policy.** Chitragupta's capability set is `{audit.append, audit.checkpoint}`. There is **no `delete`, `edit`, or `reorder` verb in the role's vocabulary at all** — fail-safe asymmetry made structural: since there is no safe direction for mutation, the verb does not exist to be misused. The signing key lives in a TEE/HSM signer (§4.6) bound to the `audit.append` capability VC, and the storage backend's write-ACL is keyed to that DID's attested SVID (defense-in-depth: even a compromised app layer cannot append without the attested cert).

#### `AuditRecord` schema

```
AuditRecord {
  record_id:    ULID            // monotonic, time-sortable; single-writer-at-a-time invariant (§4.11)
  prev_hash:    bytes32         // hash of immediately-preceding record (O(1) chain)
  actor_did:    string          // WHO authored the event (signed by actor, not by Chitragupta)
  actor_role:   string          // e.g. "Yama/policy", "Vishnu/continuity"
  action_class: enum { OBSERVE | PROPOSE | ENFORCE_PASS | ENFORCE_FAIL | HALT |
                       EVOLVE | CONSENSUS | REPUTATION | REPARATIVE | IDENTITY }
  event_type:   string
  subject_cid:  CID | null      // content-addressed artifact this event is about
  payload_commitment: bytes32   // salted hash of off-log payload  H(salt || canonical_payload)
  reasoning_rung: enum { rung1 | rung2 | rung3 } | null   // honesty-floor field (§4.2.1)
  iterated:     bool            // honesty-floor field — maker-checker actually ran?
  refs:         [record_id]     // causal back-references (e.g. checker → maker)
  policy_version: semver        // which Yama policy was in force
  sig:          bytes           // ACTOR's signature over the canonical record
}
Checkpoint {
  log_id, tree_size:uint64, root_hash:bytes32, timestamp,
  prev_checkpoint_hash:bytes32, witness_cosigs:[WitnessSig], chitragupta_sig
}
```

#### 4.2.1 The honesty floor, made mechanically auditable

`reasoning_rung` (Pearl causal ladder: rung-1 associative / rung-2 interventional / rung-3 counterfactual) and `iterated` are **recorded ledger fields**. The central AI failure mode is a rung-1 pattern *presented as* a rung-3 explanation, or a falsely-claimed `(iterated)` maker-checker pass. By writing these as fields, a maker-checker contradiction becomes a **provable ledger inconsistency**: a checker record (`refs → maker.record_id`) that disputes the maker's claimed rung, cross-referenced, makes the false claim demonstrable.

**Honest limitation (safety-risk, addressed not eliminated).** These fields are **self-reported by the acting agent**. The ledger makes a contradiction *provable* but not automatically *discoverable* — discovery requires an **independent checker** to exist and to look. A deceptive agent that tags rung-3 on a rung-1 pattern is caught only if a checker contradicts it. We therefore make the checker **mandatory, not optional, for the classes that matter**: every `ENFORCE_FAIL`, `EVOLVE`, `GOVERNANCE`, and irreversible Class-C/D record **requires** a paired independent-checker record before it is treated as settled, and the checker judges **before seeing the maker's concurrence** (maker-checker independence). For high-volume `OBSERVE` records, checking is statistically sampled, not exhaustive — an accepted residual, named in §4.14.

---

### 4.3 Component 2 — Tile-Based Transparency Surface

**Purpose.** Make the ledger externally auditable at near-zero serving cost **and with zero trust in the writer's online proof service.** Any party — a witness, a health agent, the anti-collusion detector, a human, a future regulator — reconstructs inclusion and consistency proofs **locally** from static files. This removes the writer's ability to serve a tailored or false proof per-client.

**Mechanism.** Expose the Merkle tree as immutable, fixed-size **tiles** (slabs of node hashes, 256 entries/tile per the transparency.dev convention) plus the signed checkpoint, all as **static, content-addressed (CID), CDN-cacheable** blobs. A client fetches only the tiles on the path it needs:

- **Inclusion** of leaf *i* at size *n*: the O(log n) sibling hashes.
- **Consistency** that size-*m* root is a strict prefix of size-*n* root: O(log n) hashes.

No server-side proof computation exists, so the writer **cannot equivocate per-client**: tiles are immutable once published and their own hashes are pinned by the checkpoint root, and each tile is itself addressed by CID so a cached tile is self-verifying. Proof verification is pure-functional and reusable by every consumer subsystem (the "skeptical client" carries only its last trusted `(tree_size, root_hash)` and verifies forward).

```
Tile { level:uint8, index:uint64, width:uint16, hashes:[bytes32] }   // path: tile/{level}/{index}
```

---

### 4.4 Component 3 — Witness Cosigning + Non-Omission, and single-operator witness governance

A lone writer that is honest about *what it publishes* can still (a) **fork history / show split views** (equivocation), or (b) **silently withhold** a damning record (omission). Witnessing defeats (a). Omission needs its own protocol — and the red-team correctly identified it as the single most important gap, so it is treated as a first-class component here, not a footnote.

#### 4.4.1 Witnesses defeat equivocation

A **Witness** is a minimal, deterministic, **non-LLM** verifier (a few hundred lines): on each new checkpoint, verify it is a valid **append-only consistency extension** of the last checkpoint this witness signed; if yes, co-sign; if it ever sees **two conflicting checkpoints at the same `tree_size`**, refuse and raise a `ForkAlarm`. A threshold **t-of-w** cosigning is required before any consumer trusts a checkpoint.

#### 4.4.2 Single-operator witness-set governance (the concrete answer)

The hard question prior work leaves abstract is: *who witnesses in a single-operator swarm, and how are they chosen, rotated, and threshold-set so they fail independently?* Our concrete instantiation:

| Witness class | Composition | Independence property |
|---|---|---|
| **k internal witnesses** | Each pinned to a **distinct trust domain**: separate process, separate keys, separate storage, **and a distinct root-of-trust** (see §4.6 fix). | No single host *or HSM-vendor* compromise forges a quorum. |
| **≥1 external-anchor witness (mandatory)** | A public transparency log (CT-style) **and**, for governance checkpoints, a second independent counterparty witness. | "Split-view across the operator boundary" defense — even total internal compromise cannot rewrite history undetected. |
| **Human offline-key witness** | Co-signs the **highest-stakes** checkpoints (governance/constitutional). | A human-held key is the last backstop; see §4.14 for the key-recovery limitation. |

**Threshold & rotation, under fail-safe asymmetry.** Demoting trust in a witness (shrinking the set / raising scrutiny) is **free and immediate** on any `ForkAlarm`. **Adding** a witness or **lowering t** is **governance-gated**. Witness keys are SPIFFE-attested and rotate on a schedule; **witness-set membership changes are themselves `IDENTITY` ledger records** under a governance gate — so the set **cannot be silently packed**. Each **consumer sets its own acceptance policy** over which witnesses count (client-chosen consensus), so a captured internal majority still fails a consumer that requires the external anchor.

> **Safety-risk addressed — slow witness-set packing as value-drift.** Membership change is governance-gated, but if that gate were a soft optimistic-veto, an over-eager self-evolution loop or a patient adversary could rotate the internal set toward correlated members **faster than a human veto reliably fires**. Two hard backstops: (1) the **external-anchor-required invariant is constitutional-immutable** — it is not on any self-evolvable path and cannot be relaxed by any Class ≤ C action; (2) **adding a witness or lowering t is Class-C explicit-human-approval**, not optimistic-veto, precisely because the failure is silent and cumulative. The external anchor is the property that survives even a fully-packed internal quorum.

```
Witness         { witness_did, svid, trust_domain_id, root_of_trust_id, key_ref:HSM, last_signed:{tree_size,root_hash} }
WitnessSig      { witness_did, checkpoint_hash, sig, observed_at }
WitnessSetManifest { members:[Witness], threshold_t, external_anchor_required:bool /*immutable=true*/,
                     external_anchor_count_for_governance:int /*≥2*/, version, governance_record_id }
ForkAlarm       { witness_did, size, root_a, root_b, sigs }          // HALT-class → Vishnu
```

#### 4.4.3 Non-Omission (completeness) protocol — converting withholding from silent to detectable

Witnesses verify that what *is* published is a consistent extension; they never saw an omitted event, so they cannot attest to its absence. We close this with **promise-of-inclusion receipts** and **receipt gossip**:

1. A submitter constructs an intent and submits it to Chitragupta. Chitragupta returns a **signed `InclusionPromise{ intent_hash, expected_by_checkpoint, deadline_ts, chitragupta_sig }`** before the submitter considers the submission acknowledged.
2. The submitter **gossips the receipt to the witness set** (cheap, append-only at the witnesses). Witnesses now hold a set of outstanding promises and will **demand inclusion** of any receipt they have seen by its named checkpoint.
3. The submitter (and any witness) **verifies an inclusion proof appears by `expected_by_checkpoint`**. A missing proof past `deadline_ts` is an **`OmissionAlarm`** — a HALT-class signal routed to Vishnu, exactly like a `ForkAlarm`.

```
InclusionPromise { intent_hash, expected_by_checkpoint, deadline_ts, chitragupta_sig }
OmissionAlarm    { intent_hash, promised_by_checkpoint, observed_size, witness_dids, sigs }  // HALT-class → Vishnu
```

This converts withholding from *silent* to *detectable* for any intent that produced a gossiped receipt. **Honest limitation:** it cannot detect an event that **never entered the protocol at all** (an unmediated side-effect that never generated an intent or receipt). That residual is the route-around problem, handled at the runtime boundary in §4.9 with a reconciliation detector — and named as an external assumption, not a solved problem.

---

### 4.5 Component 4 — Content-Addressed Evidence Store (CID / Merkle-DAG) with selective disclosure

**Purpose.** Keep the verifiable log **small and fast** by storing only commitments, never bulk data; give every artifact a self-verifying, location-independent, deduplicated identity; and reconcile audit-transparency with confidentiality.

**Mechanism.** Bulk content (tool output, an evolution variant, a transcript, a model-version blob, a skill file) is chunked (~256 KB), each chunk hashed and linked into a Merkle-DAG; the root **CID** transitively commits to all bytes. The public ledger stores **only** `payload_commitment = H(salt || canonical_payload)` and, when disclosure is permitted, the `CID`.

- **Selective disclosure:** the salted commitment lets the writer later prove record *X* corresponds to payload *Y* by revealing `(salt, payload)` — a third party recomputes and matches — **without ever putting the payload in the public log.**
- **ZK-friendly extension (reserved, gated to Class-C/D):** replace the plain commitment with a Pedersen/Merkle commitment so a ZK proof can assert a *predicate* over the payload (e.g. "this evolution variant passed the safety battery") without revealing it. Reserved because proving is seconds-to-minutes; it is not on the hot path.
- **Confidentiality layered on top:** a CID gives integrity, **not secrecy.** For secret artifacts the CID is of the **ciphertext**; for public ones, of the plaintext. The `encrypted` flag and `disclosure_policy` are recorded.

**Free side-benefit — host-filesystem corruption detector.** A CID mismatch on read is a **hard integrity failure**. This directly catches a known class of filesystem read-corruption (truncation, BOM-injection, stale-cache reads on some host setups): a corrupted artifact fails its CID before it can propagate into a build or a downstream decision.

**Invariant — CID never carries attribution.** A CID says *what* the bytes are; it never says *who* produced them. Every `EvidenceRef` is therefore **always co-signed by the producing agent's DID**, so attribution is never lost in dedup.

```
CID          = multihash(multicodec, H(content))        // open multiformats spec; network transport optional
MerkleDAGNode { data_chunk | links:[{cid, size}] }
EvidenceRef  { cid, commitment:bytes32, salt_ref, encrypted:bool,
               disclosure_policy:enum { PUBLIC | COMMITMENT_ONLY | ZK }, size, producer_did, producer_sig }
```

---

### 4.6 Component 5 — Agent Identity & Capability Layer (DID + VC cross-boundary, SPIFFE/SVID local, keys outside the model)

**Purpose.** Make role/capability constraints **cryptographic, not conventional**. "Only Yama may emit `ENFORCE_FAIL`," "only Chitragupta may append audit," "only Vishnu may `HALT`," and the Class A/B/C/D authority ceilings become **verifiable facts** checked at the chokepoint. A persistent identity also maximizes the shadow-of-the-future that makes reputation meaningful, and blocks the impersonation / lateral-credential-theft failure modes the protocol threat-model flags.

**Two complementary identity planes.**

- **Cross-boundary (DID + VC):** each agent controls a **W3C DID** resolving to a DID Document of public keys; it holds **role/capability Verifiable Credentials** issued by the governance root. At any cross-boundary A2A dialogue, the agent proves DID control via a freshness challenge and presents VCs the peer verifies against issuer + revocation.
- **Local (SPIFFE/SVID):** inside the runtime, each agent workload is **SPIFFE-attested** (node + workload attestation verifies it really is the claimed agent in the claimed environment) and issued a **short-lived (~1 h), auto-rotating SVID** for mTLS — **no static secrets, blast-radius bounded.**

**The load-bearing custody rule: the model never holds its keys.** Signing is a **deterministic side-module** — a TEE/HSM signer the agent *calls* with `(payload, requested_capability)`. The module **re-checks that the request is within the agent's capability set before signing.** So a prompt-injected or jailbroken model **cannot exfiltrate the key or sign out-of-capability.**

**Capability enforcement at the chokepoint.** The deterministic policy-gate (Yama, neighboring subsystem) verifies on every consequential action that the actor's presented VC chain authorizes *that exact verb + resource*, that `action_class_ceiling ≥ required class`, and that the VC is unexpired and unrevoked. Any miss is a **deterministic deny.** Revocation at swarm scale uses a **key-transparency-style verifiable map** (revoked `status_list` indices), whose root is anchored in the ledger — so "is this VC still valid?" is an O(log n) proof, not a trusted-oracle call.

```
DIDDocument   { id, verificationMethod:[pubkeys], authentication, capabilityInvocation }
CapabilityVC  { issuer:did:gov:root, subject:agent_did, role, capabilities:[verb],
                action_class_ceiling:enum{A|B|C|D}, issued, expires, status_list_index }
SVID          { spiffe_id, x509|jwt, ttl≈1h }
SignRequest   { agent_did, payload, requested_capability }   // signer checks capability membership BEFORE signing
RevocationMap = verifiable key-transparency map; root anchored in the ledger (revocation is itself tamper-evident)
```

> **Safety-risk addressed — TEE/HSM root-of-trust as a concentrated SPOF and a vendor-neutrality hole.** Key-custody-outside-the-model is correct, but it *relocates* trust to a hardware-attestation root. If witness heterogeneity were only at the **slot** level on the **same vendor**, a single TEE side-channel or attestation-root compromise could forge the writer signature **and** a same-vendor witness quorum at once — collapsing the rewrite and split-view defenses simultaneously. **Binding requirement:** witness heterogeneity is enforced **at the root-of-trust level** (`root_of_trust_id` is part of `Witness`): at minimum one internal witness must root in a **different HSM/TEE vendor or a software keystore with a different attestation root**, and the **external-anchor witness must root in a different trust domain entirely** (already implied; here made binding). **Residual, stated honestly:** the *writer's own* signing key remains a single TEE dependency. Writer-key compromise is mitigated only by witnesses refusing *inconsistent* checkpoints — that catches a fork, but **not a single forged-yet-internally-consistent append before detection.** This is a real residual, narrowed by the non-omission protocol (a forged append that displaces a promised one trips an `OmissionAlarm`) but not eliminated. It is a vendor-rooted dependency the otherwise-vendor-neutral fabric cannot fully remove.

---

### 4.7 Component 6 — Risk-Tiered Consensus Engine (decision-voting), with a diversity-floor precondition

**Scope note up front (coherence fix).** This component is a **decision-coordination** mechanism — multiple agents agreeing on an *answer* — and is **architecturally separable** from the ledger's integrity (§4.2–4.4), which uses **no consensus at all**. The "no-BFT" argument that is *correct for the ledger* (a single trust domain has no trustless-strangers problem) is **not** the argument here; the argument here is **cost-proportionality and false-confidence avoidance.** We keep both under one section only because both write `CONSENSUS`/`ENFORCE` records to the same fabric; the threat models differ and are treated separately.

**Spend agreement cost in proportion to stakes — and never let consensus be falsely confident.** Three tiers, selected by `(reversibility × blast_radius × action_class)`:

| Tier | When | Mechanism | Cost |
|---|---|---|---|
| **Tier-0** | routine, reversible, Class-A (the overwhelming majority) | single agent behind the deterministic policy-gate; one audit record | O(1) |
| **Tier-1** | irreversible **or** Class-B+ single high-stakes decision | N-agent **diverse-reasoning** vote: distinct **generator** agents propose, distinct **evaluator** agents score (separation of powers); scores aggregated by **geometric median** | O(N) |
| **Tier-2** | **genuinely adversarial / independently-owned / cross-operator** agents only | real BFT (linear-message HotStuff-style, or PBFT for tiny sets) | rare |

**Tier-2 is almost never used.** A single-trust-domain cooperative swarm does not have the adversarial-replication problem BFT exists for; cargo-culting BFT onto routine work is the explicit antipattern.

#### 4.7.1 The diversity-floor precondition (the part prior work lacks)

The engine **refuses to treat a Tier-1 vote as valid** unless the participants are **measurably decorrelated** — distinct base models where available, or distinct prompt-decompositions / role exploration-vs-exploitation dials / tool-sets — measured by an agreement-entropy / pairwise-output-divergence check:

```
diversity_score = 1 - mean_pairwise_cosine_similarity(reasoning_embeddings)   // black-box proxy; degrades gracefully on closed models
```

If `diversity_score` is **below the floor**, the vote is flagged **LOW-CONFIDENCE and escalates to a human gate rather than asserting.** A confidently-agreeing **homogeneous** panel is exactly the false-confidence failure; the fabric refuses to mint confidence from it.

**Welfare-conditioning (cooperation == collusion, applied at the consensus layer).** The engine **never rewards bare agreement.** **Unanimity with low diversity raises a groupthink/collusion flag to the anti-collusion detector — not a confidence boost.** This is the *cooperation-equals-collusion* insight transplanted to consensus: the same shadow-of-the-future + reciprocity that produces cooperation also produces cartels, so agreement is treated as a signal to *investigate*, never as a reward.

```
DecisionContext { reversibility:enum{REVERSIBLE|COSTLY|IRREVERSIBLE},
                  blast_radius:enum{SELF|TASK|SWARM|GOVERNANCE}, action_class:A|B|C|D } → tier_selector()
VoteRound { tier, generators:[did], evaluators:[did], candidates:[{cid, scores:[vec]}],
            aggregate:geometric_median /* Weiszfeld */, dissent:[vec],
            diversity_score:float, confidence:enum{HIGH|LOW}, ground_truth_check:enum{PASSED|FAILED|NONE}, outcome_cid }
```

#### 4.7.2 What geometric median does and does NOT give you (precision fix)

The earlier draft overstated this; stated precisely:

- The geometric median has **breakdown point 0.5** — it cannot be dragged to infinity by **fewer than n/2** outliers. That is **bounded-influence under a minority of outliers**, **not exactness**, and **not** an `f ≤ (n-1)/2` Byzantine-agreement guarantee. A corrupted minority can still bias the estimate by a *bounded, nonzero* amount.
- Crucially, geometric median assumes the corruptions are **outliers (a minority that disagrees with the honest cluster).** Under **correlated LLM error** — the exact hard case — the "wrong" vectors are the **majority and cluster together**, so the geometric median converges to the wrong consensus **and reports it confidently.** The diversity-floor is the *only* guard against this, and **it is a proxy** (see §4.14).

**Therefore Tier-1 is never terminal where a falsifier exists.** Where a machine-checkable ground truth is available (a tool-verifiable result, a passing/failing safety battery, a compilable/test-passing build), the vote is **coupled to that independent falsification check** (`ground_truth_check`), which **overrides** the vote. Where no falsifier exists, **LOW-CONFIDENCE escalation is the DEFAULT for irreversible Class-C/D**, not the exception. Every outcome — tier, participants, `diversity_score`, aggregate, full dissent vector — is a `CONSENSUS` ledger record, so a falsely-confident or collusion-shaped vote is **permanently auditable** after the fact.

---

### 4.8 Liveness, HA, and the writer single-point-of-failure (must-fix)

"Exactly one writer" is a **liveness SPOF** unless the failover is specified. An always-on, self-evolving swarm cannot have a hard serialization bottleneck with no HA story.

**Writer HA — a tiny witnessed single-writer election, NOT global BFT.**

```
        active Chitragupta ──heartbeat──▶ hot-standby Chitragupta
              │                                   │
              │ on outage / missed heartbeat       │
              ▼                                   ▼
   witnessed leader-handoff:  IDENTITY record { new_writer_did, epoch_fence:uint, prev_writer_did }
       co-signed by  t-of-w witnesses + external anchor + human offline key (Class-C)
       → fences the old writer's audit.append capability (RevocationMap) so two writers
         can NEVER both believe they hold append.   (resolves the ULID/chain fork, §4.11)
```

The handoff is itself an `IDENTITY` ledger record; the **epoch fence** monotonically increments and the old writer's `audit.append` capability is revoked in the same witnessed act, so the single `prev_hash` chain and ULID monotonicity stay **single-writer-at-a-time** by construction.

**Back-pressure / buffering contract on outage.**

| Action class during writer outage | Behavior |
|---|---|
| Class-C / Class-D (irreversible, high-stakes) | **fail closed** — the action does not proceed unlogged |
| Class-A (routine, reversible) | **proceed-with-flag** — durable, DID-signed **intent queue at the submitter**; on writer recovery, **ordered drain, dedup by ULID**, and the gap is reconciled and flagged in the audit trail |
| Class-B | fail closed unless an explicit standing policy permits proceed-with-flag for the specific verb |

**Throughput ceiling.** The single append path is the throughput bound; it is sized for *consequential* events (gate decisions, halts, mutations, consensus outcomes, reputation/identity changes), **not** for high-volume inner-loop chatter — routine reversible reasoning is Tier-0 and need not hit the ledger except as sampled `OBSERVE`. Verbose `OBSERVE` is batched and Merkle-rolled (§4.10) to keep the hot path bounded.

#### 4.8.1 Revoking the writer's OWN capability without its cooperation (must-fix)

The `RevocationMap` is anchored in the ledger that Chitragupta writes — a circular trap if the thing to be revoked is **Chitragupta itself** (compromised or unresponsive). This needs a distinct, **out-of-band, human-held** path:

```
WRITER-FREEZE (Class-C/D, named protocol — NOT an ordinary append):
  trigger: ForkAlarm/OmissionAlarm naming the writer, OR human-initiated
  actors:  t-of-w witnesses  +  external anchor  +  human offline key
  effect:  (1) witnesses STOP cosigning the incumbent writer's checkpoints (free, immediate, fail-safe demotion)
           (2) human offline key + witness quorum bless a successor via the §4.8 witnessed leader-handoff
           (3) the freeze + handoff are reconciled into the ledger by the SUCCESSOR, after the fact
```

The freeze does **not** require the incumbent's participation — witnesses can refuse-to-cosign unilaterally (demotion is always free), and the human offline key + external anchor bless the successor. This is why witness refusal is a *capability* (stop signing) and not an *append* (which would need the broken writer).

---

### 4.9 Universal mediation, route-around risk, and the reconciliation detector (must-fix)

**Explicit external assumption.** Akasha-Sutra's completeness guarantee holds **only for actions that pass through the agent→tool chokepoint and get submitted.** A clever agent that achieves an effect via an **unmediated side-channel** — a tool with native network egress, a filesystem write outside the CID store, an out-of-band message to a sibling — produces **no ledger record**, and the fabric is blind to it. We do **not** assert this away; we name the dependency and add a backstop.

**Dependency (owned by the runtime / Yama subsystem):** the runtime MUST enforce that **no consequential verb is reachable except through the mediated chokepoint** — sandboxed egress, all tools wrapped, no ambient authority. Without this, "tamper-evident" covers only the honest path.

**Backstop owned here — the reconciliation detector.** Periodically compare **observed side-effects** (filesystem and network telemetry, sandbox audit) against ledger records. Any effect with **no corresponding `OBSERVE`/`ENFORCE`/`EVOLVE` record** is flagged an **integrity violation** and routed to the health/anti-collusion layer (and, if severe, to Vishnu). This turns a silent route-around into a *detectable discrepancy* — detection, not prevention, and honestly so.

```
ReconciliationFinding { observed_effect:{kind, target, time}, matching_record:record_id|null,
                        severity:enum{INFO|WARN|VIOLATION}, routed_to:enum{HEALTH|VISHNU} }
```

> **Safety-risk addressed — the ledger as a covert channel.** A public, append-only, content-addressed log is a low-bandwidth but persistent shared medium. Agents could steganographically encode coordination into otherwise-legitimate fields — **ULID timing, ref-graph structure, salt values, CID selection.** The anti-collusion detector is therefore **explicitly tasked with steganalysis of the ledger's own metadata** (inter-arrival timing distributions, ref-graph anomaly detection, salt-entropy checks), not only of agent message content. The transparency surface is monitored as a potential channel, not assumed benign. This is consistent with the research finding that **white-box activation-based collusion detection (0.99–1.00 AUROC) beats text-level monitoring** where model internals are available; where they are not (closed models), metadata steganalysis is the degraded-but-present fallback.

---

### 4.10 Component 7 — Checkpoint-Archival & Lineage-Preserving Pruning (bounded log on an always-on swarm)

A continuous tamper-evident log grows unbounded, but naive truncation destroys the auditability and causal lineage the **evolution-rollback** and **accountability** functions depend on. Keep the **live** structure bounded while preserving **full lineage forever.**

**Epoch sealing.** On a size/time boundary, the live log is sealed into an immutable **epoch**, emitting a `SealCheckpointRecord{ epoch_id, tree_size, root_hash, prev_epoch_seal_hash, witness_cosigs, retention_class }`. The seals themselves form a **hash chain** (a "log of logs"), so cross-epoch lineage is itself tamper-evident and O(log E) verifiable. The sealed epoch's full leaf-data migrates to the **CID evidence store** (content-addressed, dedup'd, cold); the **live tree keeps only roots + recent epochs**, so working size is bounded by retention window, not total history. **Nothing causal is lost:** any historical record is retrievable by CID and re-verifiable against its epoch root, and the seal chain proves the archived epoch is the genuine continuation. The **seal-chain root is periodically co-signed by the external-anchor witness**, so even cold history cannot be silently rewritten.

**Selective retention by `action_class`.** `ENFORCE_FAIL` / `HALT` / `GOVERNANCE` / `EVOLVE` / `REPARATIVE` (the accountability-critical and rollback-critical classes) are **retained at full fidelity indefinitely.** High-volume `OBSERVE` records may be aggregated into Merkle-rolled summaries after their epoch seals — **the leaf hashes remain (proving non-omission)** while verbose payloads age to cold CID storage.

> **Safety-risk addressed — pruning can destroy evidence of a SLOW attack.** A value-drift or slow-collusion attack manifests precisely as a **statistical pattern across many low-salience `OBSERVE` events.** If verbose `OBSERVE` payloads are aged out, a later forensic reconstruction finds only leaf hashes. **Binding mitigation — drift-aware aging:** (1) **retain full `OBSERVE` payloads (not just hashes) for any window the health / anti-collusion layer has flagged as anomalous**; (2) keep a **permanently-retained, statistically-sampled subset** of full `OBSERVE` payloads for baseline reconstruction; (3) an **open anti-collusion investigation freezes aging** on all records in its scope. Retention is thus coupled to the detector's active state, not a fixed clock.

```
SealCheckpointRecord { epoch_id:uint, tree_size, root_hash, prev_epoch_seal_hash:bytes32,
                       witness_cosigs, sealed_at, retention_class }
EpochManifest        { epoch_id, root_hash, leaf_count, cid_of_full_leaf_set, retained_records:[record_id] }
// retrieval: record_id → epoch_id → EpochManifest.cid → Merkle path → inclusion proof vs the historical root the live seal-chain still vouches for
```

---

### 4.11 Core protocols (message flows)

#### Protocol A — Audit-Append (single-writer, witness-cosigned, non-omission-checked)

```
1. Producer (Yama/Vishnu/Evolution/Health/Consensus) builds an AuditRecord intent;
   bulk payload → CID store; keep EvidenceRef{cid, commitment, salt}.
2. Producer submits intent over mTLS (authenticated by its SVID), DID-signed (authorship attributable
   even though Chitragupta is the writer).
3. Chitragupta verifies the producer's CapabilityVC permits this action_class
   (only Yama's VC authorizes ENFORCE_FAIL; a forged ENFORCE_FAIL from another DID is REJECTED and
   itself logged as an IDENTITY-violation record).
4. Chitragupta returns a signed InclusionPromise; producer gossips it to witnesses (§4.4.3).
5. Chitragupta sets prev_hash = H(last record), appends the leaf, calls the TEE/HSM signer
   (capability-checked: only audit.append signs), updates the Merkle tree + tiles.
6. On batch/time boundary, Chitragupta builds a Checkpoint and broadcasts to the witness set.
7. Each witness verifies append-only consistency; t-of-w return WitnessSigs (incl. external anchor where required);
   Chitragupta attaches them and publishes tiles + checkpoint as static CID-addressed blobs.
8. The producer / any witness verifies an inclusion proof appears by expected_by_checkpoint;
   a miss past deadline_ts → OmissionAlarm → Vishnu.
9. Any consumer later verifies an event by fetching tiles and checking inclusion against a
   witness-cosigned checkpoint it trusts UNDER ITS OWN acceptance policy — never trusting Chitragupta's word.
```

#### Protocol B — Identity-Bootstrap & Capability-Gated Action (keys never in the model)

```
1. At spawn: runtime SPIFFE-attests the workload (node + workload), issues a short-lived SVID;
   governance root issues role/capability VCs bound to the agent DID → recorded as an IDENTITY record.
2. Cross-boundary: agent answers a freshness challenge by asking its TEE/HSM signer to sign the nonce
   (proves DID control) and presents CapabilityVCs; peer verifies sig + issuer + non-revocation (RevocationMap proof).
3. For any consequential action: agent calls the Yama policy-gate with the request + presented VC chain.
4. Gate deterministically checks (a) VC authorizes this exact verb+resource, (b) action_class_ceiling ≥ required,
   (c) VC unexpired + unrevoked via the verifiable RevocationMap — any miss = deterministic DENY.
5. If allowed and a signature is needed, agent calls the TEE/HSM signer with (payload, requested_capability);
   signer RE-CHECKS capability membership before signing — a prompt-injected model cannot sign out-of-role.
6. Decision (PASS/FAIL) is emitted as an ENFORCE record via Protocol A.
   Trust-DEMOTION on any anomaly is free + immediate; PROMOTION / new-capability issuance is governance-gated.
```

#### Protocol C — Risk-Tiered Consensus Routing

```
1. Orchestrator computes DecisionContext{reversibility, blast_radius, action_class}.
2. tier_selector(): routine+reversible+Class-A → Tier-0; irreversible or Class-B+ → Tier-1;
   genuinely-adversarial/independently-owned → Tier-2 (BFT, rare).
3. Tier-0: single agent behind the gate; one audit record; done.
4. Tier-1: assemble distinct GENERATORs + EVALUATORs; measure diversity_score.
   - below floor → LOW-CONFIDENCE → ESCALATE to a human gate (default for irreversible Class-C/D).
   - if a machine-checkable falsifier exists → run it; ground_truth_check OVERRIDES the vote.
5. Tier-1 aggregation: evaluators score; combine by geometric median (Weiszfeld); record aggregate + FULL dissent vector.
6. Unanimous AND low-diversity → raise a groupthink/collusion FLAG to the anti-collusion detector (never a confidence boost).
7. Tier-2 (rare): linear-message BFT only among the genuinely-distrusting set.
8. Emit a CONSENSUS record (tier, participants, diversity_score, aggregate, dissent, confidence, ground_truth_check).
```

#### Protocol D — Epoch-Seal & Lineage-Preserving Archival

```
1. On a size/time boundary, Chitragupta freezes the tree as an epoch; computes SealCheckpointRecord chaining prev_epoch_seal_hash.
2. External-anchor witness co-signs the seal (anchored OUTSIDE the swarm's own blast radius).
3. Full leaf-data → CID store (dedup'd, encrypted as needed); indexed by an EpochManifest.
4. Live tree drops to roots + recent epochs; retention-class rules keep ENFORCE_FAIL/HALT/GOVERNANCE/EVOLVE/REPARATIVE hot;
   drift-aware aging freezes OBSERVE records under active investigation; sampled OBSERVE kept permanently.
5. Historical retrieval rebuilds an inclusion proof from EpochManifest.cid against the epoch root the live seal-chain still vouches for.
```

---

### 4.12 Failure modes addressed (and the precise mechanism)

| Failure mode | Defended by | Honest residual |
|---|---|---|
| **Silent rewrite** of audit history | per-record hash chain (O(1)) + Merkle consistency proof (O(log n)) | none for published history |
| **Split-view / equivocation** by the operator | t-of-w witnessing + **mandatory external anchor** outside the blast radius | colluding *full* quorum incl. anchor (§4.14) |
| **Silent withholding / omission** | **InclusionPromise receipts + witness-demanded inclusion + OmissionAlarm** (§4.4.3) | events that never enter the protocol → §4.9 reconciliation (detect not prevent) |
| **Audit-log forgery by a monitored agent** | exclusive writer; append capability bound to one DID; write-ACL keyed to attested SVID | writer-key compromise → §4.6 residual |
| **Impersonation / capability escalation** (forged ENFORCE_FAIL, fake Chitragupta, unauthorized HALT) | DID-bound capability VCs verified deterministically at the chokepoint | revocation propagation lag (§4.14) |
| **Key exfiltration via prompt injection / jailbreak** | keys in TEE/HSM signer **outside the model surface**; signer re-checks capability | TEE root-of-trust dependency (§4.6) |
| **Falsely-confident consensus** from correlated error/groupthink | Tier-1 invalid below diversity floor → escalate; ground-truth override; geometric-median bounds outlier influence | correlated-MAJORITY error looks diverse (§4.14) |
| **Consensus-as-collusion** (agreement rewarded) | agreement is never a reward; unanimity+low-diversity → collusion flag | covert channels in agreement structure → §4.9 steganalysis |
| **False honesty tags** (no-false-iterated, rung-1-as-rung-3) | `iterated` / `reasoning_rung` recorded; **mandatory independent checker** for the classes that matter | self-report discoverable only via checker (§4.2.1) |
| **Host filesystem corruption** (mount/truncation/BOM faults on some hosts) | **CID mismatch on read = hard integrity failure** before propagation | — |
| **Unbounded log growth** | epoch sealing + CID cold archival + retention-class prune; cross-epoch seal chain preserves lineage | retention-taxonomy judgment call (§4.14) |
| **Confidentiality leak through a transparent log** | only salted commitments + CIDs public; selective disclosure; ZK reserved | metadata leakage (timing/which-DID-when) (§4.14) |
| **Witness-set packing / capture** | governance-gated, logged membership; consumer-chosen acceptance; **constitutional-immutable external anchor** | incentive/honesty of witnesses (§4.14) |
| **Writer liveness SPOF** | hot-standby + witnessed leader-handoff + epoch-fence; fail-closed C/D, proceed-with-flag A | single append-path throughput ceiling (§4.8) |
| **Revoking the writer itself** | out-of-band WRITER-FREEZE: witnesses stop cosigning + human offline key blesses successor (§4.8.1) | depends on human offline key (§4.14) |
| **Route-around / unmediated side-effect** | reconciliation detector flags effects with no matching record (§4.9) | requires runtime universal-mediation assumption |

---

### 4.13 Interfaces with the rest of Indra's Net

| Other subsystem | Contract | Hot-path / consistency note |
|---|---|---|
| **Governance / Policy floor (Yama)** — deterministic policy-as-code at the agent→tool chokepoint | Yama is the **only** emitter of `ENFORCE_PASS`/`ENFORCE_FAIL`; consumer of the identity layer (calls Protocol B before any consequential verb); every gate decision routes through Protocol A. Yama's policy artifacts are CID-addressed and signed; version-changes are append-only ledger records (tightening cheap/append-only; **loosening needs a named falsifier + a governance gate**). | **Consistency-window fix:** Yama is on the sub-millisecond hot path; witness-cosigned checkpoint acceptance is async and possibly seconds. Yama enforces against a **locally-cached policy version with a staleness bound**; on a **stale or just-revoked** policy version it **fails closed** rather than enforcing an unconfirmed version. Checkpoint confirmation reconciles the cache after the fact. |
| **Continuity / Halt-Guardian (Vishnu)** | Vishnu is the **only** DID authorized to emit `HALT`. `ForkAlarm`, `OmissionAlarm`, reconciliation `VIOLATION`s, and CID integrity failures route to Vishnu. By fail-safe asymmetry Vishnu's capability set contains **no unpause/initiate/trap verb** — halt is cryptographically one-directional; unpause is a separate governance-gated action by a **different** principal. | **Writer-independent halt fix:** because an alarm may be *about* Chitragupta, Vishnu's `HALT` must NOT depend on a successful audit append. **HALT is asserted at the runtime/orchestration layer** (it can quiesce the swarm directly) and the `HALT` record is **reconciled after recovery** (or written by the successor writer post-freeze). The halt fires even if the ledger is down. |
| **Evolution Loop + Diverse Archive** (MAP-Elites stepping-stones / rollback substrate) | Every mutation (prompt/skill/tool/topology/weight) is content-addressed (variant CID) and recorded as an `EVOLVE` record with full provenance (which agent, which parent variant, which fitness + **safety-battery** result, `reasoning_rung`). The Archive's known-good lineage **is** the ledger's `EVOLVE`/`REPARATIVE` chain. Imported cross-agent skills carry origin-DID provenance + verification; **missing provenance ⇒ quarantined trust label, no execution without a gate.** | **Rollback-safety fix:** a variant CID guarantees *the same bytes*, **not** *still-safe-now*. Re-instating a prior variant **re-runs the safety battery against the CURRENT environment** before it is live (an Evolution-subsystem responsibility, named here so the interface is not "one-click safety"). **EVOLVE completeness is a safety precondition:** a withheld `EVOLVE` record defeats rollback — the §4.4.3 non-omission protocol is therefore load-bearing for evolution, not just audit. |
| **Health / Immune layer + Anti-collusion detector** | READ consumers of the transparency surface (verify inclusion proofs independently, never trust a self-report); WRITE consumers for `REPUTATION` / `REPARATIVE` records. Consensus outputs (`diversity_score`, unanimity-with-low-diversity flags, dissent vectors) feed the collusion detector; the detector additionally performs **ledger-metadata steganalysis** (§4.9). Reputation is **non-transferable, identity-bound (DID), context-conditioned per task-type, evidence-weighted, and competence-weighted — NEVER capital-weighted** (the stake-capture antipattern); updates are tamper-evident records. | Active investigations **freeze drift-aware OBSERVE aging** (§4.10). |
| **Interop layer (open tool-protocol / agent-to-agent Agent Cards, vendor-neutral actor runtime)** | Cross-boundary identity uses the DID/VC bootstrap, so A2A-style Agent Cards carry **verifiable** role/capability claims; tool calls pass through the capability-gate before execution. **Model-agnostic:** identity, signing, logging, and consensus depend on **no** model internals. Closed third-party models are treated as **more-untrusted** (higher monitoring intensity, lower `action_class` ceiling); white-box-only signals (activation probes for collusion) are **optional enhancements the fabric degrades gracefully without.** | — |

---

### 4.14 Honest state-of-the-art positioning

**The contribution is integration discipline, not a new primitive.** Merkle logs, RFC-6962 tile transparency, witness cosigning, DID/VC, SPIFFE/SVID, and geometric-median voting all pre-exist and are battle-tested. Named honestly, the **component-level stack is close to a union of prior art**, and the closest comparators are:

- **An immutable-manifest + cryptographic append-only governance-log + runtime-enforcement design** (governance-graph / Institutional-AI lineage) — the closest prior art on *governance + tamper-evident provenance without cargo-cult blockchain*, and the empirical source for "prompt-only constitutions are insufficient; runtime enforcement curbs collusion where prompts fail." Akasha-Sutra adopts the enforcement+audit split and adds identity, witnessing, and tiered consensus around it.
- **A combined DID-identity + append-only hash-chained audit + capability-style access-policy + lightweight multi-party attestation** design (an agent-identity-fabric lineage that *explicitly chooses attestation over consensus*) — the closest prior art on the *integrity + identity* fabric. Akasha-Sutra's exclusive-writer + external-anchor witnessing is a tightening of this.
- **A recompute-and-compare witness scheme with multi-metric agreement** (a decentralized-training lineage that uses a chain as *coordinator/randomness/arbitration*, not currency, with Bloom-filter witness proofs and Jaccard/Manhattan/Hamming agreement) — the closest prior art on *non-cargo-cult witnessed verification*; its own acknowledged open problem (calibrating acceptable similarity ranges; honest-majority assumption) is **inherited here** as the diversity-floor calibration and witness-honesty residuals below.
- **A generator/evaluator separation with robust aggregation** (a decentralized-LLM voting lineage) — the closest prior art on the *robust-vote tier*; Akasha-Sutra adds the diversity-floor precondition and welfare-conditioning that lineage lacks.
- **Tile-based static transparency and witness-cosigning-for-split-view-defense** (transparency-log and cosigning lineages) — borrowed directly.

**Three honest deltas the surveyed systems do not have:**

1. **A concrete single-operator witness-set governance instantiation** — heterogeneous internal witnesses *at the root-of-trust level* + a **mandatory, constitutional-immutable external anchor** + **governance-gated (Class-C) rotation** + **consumer-chosen acceptance policy**. Prior work leaves "who witnesses in a single-operator swarm" abstract. **We downgrade the claim from "resolves the open problem" to "proposes a concrete instantiation"** — proposing a design is not the same as resolving a problem that remains open *partly because witness honesty and liveness incentives are unsolved* (conceded below).
2. **Diversity-floor-gated, welfare-conditioned consensus tiering** that treats **unanimity-with-low-diversity as a COLLUSION flag, not a confidence boost** — the cooperation==collusion insight applied at the consensus layer. No surveyed consensus protocol does this.
3. **Lineage-preserving epoch-seal archival** that bounds an always-on log's hot state while a cross-epoch, externally-anchored seal chain preserves full causal provenance for evolution-rollback and accountability — a real attempt at an open problem the surveyed transparency logs acknowledge but do not solve.

And the **no-blockchain justification is substantive, not aesthetic**: a single-trust-domain cooperative-but-fallible swarm lacks the trustless-strangers-at-internet-scale problem that mining, tokens, and global Byzantine consensus exist to solve. The canonical incentive-network antipattern shows what importing that machinery actually buys — **reward driven by capital, not competence**, and trivial 51%-by-stake capture. We take the useful primitives (append-only crypto logs, content hashing/provenance, consensus-on-rules, witnessed verification) and **discard the economic framing entirely.**

---

### 4.15 Open problems (stated plainly; these are not solved)

1. **Witness honesty and liveness in a single-operator swarm.** The external-anchor + heterogeneous-internal design defeats split-view, but a quorum that is **offline (liveness)** or **jointly compromised (safety)** remains a residual. There is no consensus-free way to *guarantee* witness honesty without recreating a committee, and **incentive design for non-economic witnesses is open.** The external anchor is the only hard backstop, and it is a trusted third party with its own operator, availability, and capture risk — which is why governance checkpoints require **≥2 independent external anchors** and fail closed when an anchor is unavailable, while routine checkpoints proceed-with-flag. Single-external-anchor dependence for high-stakes checkpoints is honestly a new SPOF we mitigate by plurality, not eliminate.
2. **Diversity-score is a proxy.** Output-divergence / embedding-distance is a **black-box approximation.** Agents sharing training biases can be **confidently-and-wrongly aligned while LOOKING diverse**, so the false-confidence guard is **necessary but not provably sufficient.** Where a machine-checkable falsifier exists we override the vote with it; where none exists, the only honest move is LOW-CONFIDENCE escalation, which we make the default for irreversible Class-C/D.
3. **Semantic vs computational verifiability.** Every primitive here proves an output **came from a given agent/pipeline and was not altered** — **none prove the decision was correct or aligned.** TEE/zkML attestation (reserved for Class-C/D) closes the *computational* gap (the right computation ran), not the *semantic* one (the computation was wise).
4. **Reputation cold-start, whitewashing, mutual-rating rings.** Identity-bound non-transferable reputation resists transfer-based attacks, but a **fresh DID's initial trust** and **coordinated rating rings among context-segregated cards** remain partially open.
5. **Revocation latency at swarm scale.** The verifiable `RevocationMap` gives O(log n) proofs, but **propagation lag** between revoking a compromised VC and every verifier seeing it is a residual window; tuning rotation frequency vs overhead is unsettled.
6. **Privacy of even commitment-only logs.** Interaction patterns, timing, and which-DID-acted-when **leak metadata** useful for targeting; full reconciliation needs ZK-friendly logs whose proving cost is currently too high for inline use.
7. **TEE/HSM root-of-trust dependency.** Key-custody-outside-the-model is the right call, but it **relocates trust to a hardware vendor's attestation root and side-channel resistance** — a vendor-rooted dependency the otherwise-vendor-neutral fabric cannot fully eliminate. The writer's own signing key remains a single TEE dependency (§4.6 residual).
8. **Pruning-vs-auditability boundary.** Drift-aware retention keeps accountability-critical and flagged records hot, but a future audit may need a class we aged to cold storage; **choosing the retention taxonomy is a judgment call with no provably-safe default.**
9. **Human-offline-key as both backstop and bottleneck.** The highest-stakes checkpoints and the writer-revocation path (§4.8.1) depend on a human-held offline key. If lost/unavailable, governance changes and writer-failover **cannot complete (fail-closed deadlock)**; if compromised, the constitutional layer is forgeable. The mitigation is to hold it as a **Shamir m-of-n threshold across separate custodians** rather than a single key — recovery and capture-resistance both improve, at the cost of custodian coordination. The custody design itself remains an operational open problem.
