# 21. Protocols & Wire Contracts — the buildable-now schema stack

> *The seam where principle becomes bytes.* Docs 03, 04, 08, 13 and 14 define **what** Indra's Net does and **why**; this document defines the **on-the-wire shapes** an engineer ships this quarter. It introduces no new enforcement plane and no new authority. It is the `reference/schemas/` source-of-truth: six machine-readable wire contracts, each pinned to a named versioned open spec, each JCS-canonicalized (RFC 8785), CIDv1 content-addressed, and semver-governed in a backward-transitively-compatible registry. The abstract shapes of docs 04/08/13/14 become real CloudEvents events, real DID documents, real Biscuit tokens, real tlog-tiles leaves, real A2A handshakes, and real Cedar decisions — closing the design-doc-to-system gap.
>
> *Role names below are compressed coordination/ethics semantics paired with a plain gloss — engineering vocabulary, not theology, offered with humility toward the living traditions they borrow from.*

---

## 21.0 What this subsystem is, and the three caveats that frame everything

This subsystem is the **implementable realization** of the wire shapes the v1 cell already defines: doc-08's `ActionEnvelope`/`OutputEnvelope`/`BlackboardDelta` become one **worker-output-envelope**; doc-04's `DIDDocument`/`CapabilityVC`/`RevocationMap` become an **identity-bundle**; doc-04's TEE/HSM effect grants and doc-13's `bound_toolset` become **capability-tokens**; doc-04's Chitragupta ledger becomes an **audit-entry-bundle**; doc-14's `FederationAgentCard` handshake becomes a **federation-handshake-bundle**; and the doc-03 Yama floor decision becomes a **policy-decision** request/response. The honesty/provenance block rides every output envelope so doc-08 §8.5 honesty-FORM checks and doc-04 §4.2 audit fields are **wire-native, not bolted on**.

The governing discipline is **open-ENGINE-yes / managed-SERVICE-no**: every vendor-originated choice is flagged with a self-hostable substitution path (§21.9). The spine principle is unchanged: **enforce externally, ask internally** — these schemas *are* part of the deterministic harness the architecture verifies; the model that fills them remains untrusted and unverifiable (hallucination is provably inevitable; T=0 is non-deterministic — doc 00, doc 08 §8.1).

Three load-bearing caveats frame the whole subsystem and are repeated at their claim sites, never relegated to a footnote:

> **Caveat 1 — A valid signature proves origin and integrity, NEVER that a claim is true, floor-compatible, or safe.** Every contract here carries cryptographic provenance. Provenance answers *who produced these exact bytes*; it is silent on whether the content is correct, wise, or aligned. This is doc-04 §4.1's ceiling, inherited verbatim.

> **Caveat 2 — Canonicalization makes the same logical event hash-identical across producers; it cannot make the content honest.** RFC 8785 JCS guarantees two producers serialize the same logical object to byte-identical output, so a CID computed by one verifies for all. It does nothing to the truth-value of what was serialized.

> **Caveat 3 — Shipping six schemas makes the architecture BUILDABLE, not VALIDATED.** No end-to-end evaluation of the composed loop exists (doc 08 §8.15). These schemas are the *objects* the formal-assurance stream proves the harness (the cage) over; they are never a proof that the swarm (the animal) is safe, honest, or aligned. **"Formally verified the gate" is never "formally verified the agent."**

A reader who builds these six contracts and sees green signatures everywhere is **one cognitive step from a dangerous error**: *the wire is verified, therefore the loop is safe.* It is not. The cryptography is real, which is exactly why the false confidence it can manufacture is the highest-weight residual risk of this subsystem (§21.10). The defense is organizational and labelling discipline, not bytes: any dashboard built on these contracts MUST label a signature/CID pass as **"origin-valid, content-unverified,"** never "verified-safe" (composing with doc-08 §8.13's "form-valid, content-unverified" rule for honesty-form passes).

```
                 THE SIX WIRE CONTRACTS AND WHERE THEY MOUNT
  ┌───────────────────────────────────────────────────────────────────────────┐
  │  (1) worker-output-envelope   ── CloudEvents 1.0 + JSON-Schema 2020-12      │
  │      realizes doc-08 ActionEnvelope / OutputEnvelope / BlackboardDelta      │
  ├───────────────────────────────────────────────────────────────────────────┤
  │  (2) identity-bundle          ── W3C DID Core 1.0 + VC 2.0 + Status List    │
  │      realizes doc-04 §4.6 DIDDocument/CapabilityVC + doc-13 §13.5 IDENTITY  │
  ├───────────────────────────────────────────────────────────────────────────┤
  │  (3) capability-token         ── Eclipse Biscuit + SPIFFE/SVID              │
  │      realizes doc-04 §4.6 effect grants + doc-13 bound_toolset              │
  ├───────────────────────────────────────────────────────────────────────────┤
  │  (4) audit-entry-bundle       ── C2SP tlog-tiles + signed-note + Rekor v2   │
  │      realizes doc-04 §4.2 AuditRecord / Checkpoint / Tile                   │
  ├───────────────────────────────────────────────────────────────────────────┤
  │  (5) federation-handshake     ── A2A v1.0 AgentCard + AIP delegation        │
  │      realizes doc-14 §14.4 FederationAgentCard + four-phase handshake       │
  ├───────────────────────────────────────────────────────────────────────────┤
  │  (6) policy-decision          ── Cedar (floor) + OPA/Rego (infra)           │
  │      realizes doc-03 GateRequest/GateVerdict + doc-08 §8.2 ControlDecision  │
  └───────────────────────────────────────────────────────────────────────────┘
        all six: JCS (RFC 8785) → CIDv1 → detached JWS/COSE → semver registry
```

---

## 21.1 The universal wire discipline — Canonicalize → Address → Sign (CAS)

Every one of the six contracts is, first, an instance of one discipline. It runs identically on the producing and consuming sides; a mismatch is a **loud failure** (doc-04 §4.5 / doc-08 §8.2 CID-mismatch-on-read), never a silent propagation.

```
CANONICALIZE-ADDRESS-SIGN  (run on EVERY contract, producer + consumer)

 PRODUCE:
  1. Build the logical object (envelope payload | VC | token blocks | audit leaf |
     agent card | policy request) as a JSON value.
  2. Canonicalize via RFC 8785 JCS — deterministic key order + number/string
     serialization → byte-identical output across producers.            [precondition for a stable hash]
  3. Content-address:  CIDv1 = multibase(multicodec, multihash(SHA-256, JCS_bytes))
     → this CID is the object's identity (action_id / triad_root_cid / leaf hash / card_cid).
  4. Sign DETACHED over the JCS bytes (JOSE/JWS or COSE) with the SVID key (local)
     or DID key (cross-boundary). The TEE/HSM signer RE-CHECKS capability before signing
     (doc-04 §4.6). The signature rides BESIDE the bytes, never inside the signed bytes.

 CONSUME:
  5. Re-canonicalize the received object; recompute CIDv1; assert it == the referenced CID.
  6. Verify the detached signature against the producer's DID verificationMethod.
  7. Verify the credential is unrevoked via the Bitstring Status List proof (§21.3).
  8. Any miss ⇒ REJECT + emit an IDENTITY-violation audit event (§21.5).

 CARRIED CAVEAT (1): a verified signature proves origin+integrity ONLY — never that
 the content is true, floor-compatible, or safe. CAS dedups and attributes; it does not bless.
```

This single discipline is what neutralizes a known class of host-filesystem read/write faults (silent truncation, stale-cache, BOM-injection on some host setups): a truncated, BOM-corrupted, or stale read **fails its CID before it can propagate** into a build or a downstream decision. The integrity check is the hash, not a hope.

---

## 21.2 Component 1 — `worker-output-envelope` (CloudEvents 1.0 + JSON-Schema 2020-12)

**Purpose.** The single wire contract for everything a worker emits — the unification of doc-08's `ActionEnvelope` (a request to act), `OutputEnvelope` (a substantive output), and `BlackboardDelta` (a salience-gated workspace publication). It is the most-emitted contract; every other contract references its CIDs. Its load-bearing move is carrying the **honesty/provenance block as first-class CloudEvents-native fields**, so doc-08 §8.5 honesty-FORM checks and doc-04 §4.2 audit fields are wire-level rather than convention.

**Mechanism.** A CloudEvents 1.0 **structured-mode** JSON event is the outer envelope. The `type` is a reverse-DNS verb drawn from a **closed enum** mapping 1:1 onto doc-04 `action_class`; `source` is the producing agent's DID; `subject` is the `subject_cid` the event is about; `id` is a ULID (doc-04 `record_id` discipline — monotonic + time-sortable); `dataschema` is a **CID-pinned** schema URI so the consumer fetches the exact schema version that validated the payload. The whole event is JCS-canonicalized before hashing → its CIDv1 is `action_id`/`envelope_cid`. Signing is **detached JOSE/COSE**, carried in CloudEvents extension attributes `sig` + `sigalg`, never inside the signed bytes. Broker-agnostic by construction: the same structured-mode JSON rides Kafka, NATS, AMQP 1.0, MQTT 5, or HTTP via the standard CloudEvents bindings — **no broker is load-bearing** (§21.9 self-hostable substitution).

| CloudEvents attribute | Value | Maps to |
|---|---|---|
| `specversion` | `"1.0"` | — |
| `type` | closed enum (table below) | doc-04 `action_class` (1:1) |
| `source` | producing agent DID (URI-ref) | doc-04 `actor_did` |
| `subject` | `subject_cid` | doc-04 `subject_cid` |
| `id` | ULID | doc-04 `record_id` |
| `time` | RFC 3339 | doc-04 timestamp |
| `datacontenttype` | `application/json` | — |
| `dataschema` | `ipfs://<cidv1>` or registry URI resolving to that CID | §21.8 registry pin |
| `sig`, `sigalg` (extensions) | detached JWS/COSE over JCS bytes | doc-04 actor `sig` |

**The `type` enum (closed; 1:1 onto doc-04 `action_class`):**

```
net.indras.observe                 ↔ OBSERVE
net.indras.propose                 ↔ PROPOSE
net.indras.enforce.pass            ↔ ENFORCE_PASS     (only Yama's VC may emit; §21.5 step 3)
net.indras.enforce.fail            ↔ ENFORCE_FAIL     (only Yama's VC may emit; non-overridable)
net.indras.halt                    ↔ HALT             (only Vishnu's VC may emit)
net.indras.evolve                  ↔ EVOLVE
net.indras.consensus               ↔ CONSENSUS
net.indras.reputation              ↔ REPUTATION
net.indras.reparative              ↔ REPARATIVE
net.indras.identity                ↔ IDENTITY
net.indras.output.substantive      ↔ (OutputEnvelope; classified by content)
net.indras.blackboard.delta        ↔ (BlackboardDelta; doc-08 §8.10 sparse/surprise-only)
```

**The `data` payload (JSON Schema 2020-12), validated by `net.indras.worker-output-envelope` semver X.Y.Z:**

```jsonc
data {
  content_cid: CID,                         // the substantive artifact (bulk in CID evidence store)
  action: {                                 // present for action-requesting (ActionEnvelope) events
    capability:      effect_id,             // doc-01 §4 Effect-lattice id — typed, never free-text
    args:            object,                // typed args
    criticality_hint: enum?,                // ADVISORY ONLY (doc-08 §8.2) — never authoritative
    parent_task_id:  uuid
  }?,
  honesty_provenance: {                     // doc-08 §8.5 wire-native; doc-04 §4.2 audit fields
    reasoning_tag: enum["normal","reasoning","iterated"],   // REQUIRED; composes (an operating-discipline convention)
    // 'iterated' MUST reference maker_checker_witness_cid (doc-08 §8.6) — else FAIL at the floor
    maker_checker_witness_cid: CID?,        // required iff reasoning_tag == 'iterated'
    causal_rung: enum["rung-1","rung-2","rung-3"]?,  // OPTIONAL + additive (the Pearl causal-ladder extension)
    selftag_classifier_agree: bool?,        // doc-08 §8.5(1) INDEPENDENT classifier is the authority,
                                            //   NOT this self-tag; disagreement → suspicion signal
    claim_level_map: { "<span>": { level: enum["assertion","belief"], evidence_ref: CID? } }?,
    trust_label: enum["trusted:audited","trusted",
                      "quarantined:observed","quarantined:external"],  // doc-04 trust-labels.json
    action_class: enum[OBSERVE,PROPOSE,ENFORCE_PASS,ENFORCE_FAIL,HALT,
                       EVOLVE,CONSENSUS,REPUTATION,REPARATIVE,IDENTITY],
    reparative: { is_reparative: bool, corrects_record_id: record_id?,
                  recurrence_count: int }?  // doc-03 reparative class — correction, recurrence-guarded
  },
  model_adapter_id: string,                 // doc-08 §8.10 adapter id
  trust_class: enum,                        // STAMPED BY THE ADAPTER, not self-asserted (doc-08 §8.10)
  diversity_family_id: string,              // BASE-MODEL FAMILY id (doc-08 §8.3) — see §21.2.1
  blackboard: { salience: float, surprise_magnitude: float,
                ignition_eligible: bool }?  // present only for blackboard.delta (doc-08 §8.10 sparse)
}
```

Two fields carry corrections the v0.3 design spine makes binding and must not be misread:

- `trust_label` rides every envelope. **Instructions inside `quarantined:*` content are never action-grounds** (doc-03 §1 trust-labels rule). A valid signature on a quarantined payload proves origin only; admission of any embedded instruction requires the floor gate plus out-of-band human confirmation, never the signature.
- `selftag_classifier_agree` makes explicit that the **self-tag is not authoritative** — doc-08 §8.5(1)'s independent classifier is the authority on causal rung. The wire field carries the self-claim *and* the disagreement flag; the truth-determination happens in the control layer, not here.

### 21.2.1 `diversity_family_id` is model-family heterogeneity, not prompt variation (binding)

`diversity_family_id` names the **base model family / developer**, the unit the doc-08 §8.3 decorrelation metric and the doc-04 §4.7 diversity-floor actually consume. The v0.3 evidence is blunt and the wire field encodes it: **same-family LLM errors are correlated, and the correlation RISES with capability** (mid-2026 correlated-errors finding; replication open — cited where the CI/consensus subsystem gates on it, not restated as bare folklore here). Therefore:

> **Binding honesty red-line on this field:** prompt-only or persona-only "diversity" is **fake diversity** — worse than acknowledged homogeneity because it *hides* the correlation. `diversity_family_id` MUST be the base-model family identifier, never a prompt-template or persona tag. A maker-checker verifier (doc-08 §8.6) whose `diversity_family_id` equals the maker's is **not** an independent checker; self-family verification can rubber-stamp and is rejected by the consuming control layer. The only defensible claim this field supports is that family heterogeneity **decorrelates errors** — never that "diversity trumps ability" (a refuted theorem, never invoked).

---

## 21.3 Component 2 — `identity-bundle` (DID Document + CapabilityVC + Bitstring Status List)

**Purpose.** The on-the-wire realization of doc-04 §4.6 `DIDDocument`/`CapabilityVC` and doc-13 §13.5 `IDENTITY.json`. It establishes **who** an agent is (self-controlled identity) and **what role/ceiling** it claims (a credential issued by the governance root, where `subject ≠ the agent`). The Bitstring Status List **is** the architecture's previously-hand-rolled `RevocationMap`/`status_list_index`, now a standard.

**Mechanism — three layered specs.**

1. **W3C DID Core 1.0 identifiers.** `did:key` for ephemeral actual-occasions (the multibase-encoded public key *is* the identifier — zero-infra, ideal for short-lived occasions). `did:web` for standing personas and the governance root (resolves to `/.well-known/did.json` over TLS — self-hostable, no ledger). The governance-root `did:web` is the trust anchor for all RoleCredential issuance.
2. **W3C VC Data Model 2.0** for `RoleCredential` and `CapabilityCredential`, `issuer` = governance-root DID, `credentialSubject.id` = agent DID, secured per *Securing VCs with JOSE/COSE* — an **enveloping JWS/COSE_Sign1**, not the deprecated embedded-LD-proof default.
3. **VC Bitstring Status List v1.0** for revocation. Each credential carries a `credentialStatus` pointing at a compressed bitstring index; flipping one bit revokes; the status-list credential's own hash is **anchored in the audit ledger** so "is this VC live?" is an O(log n) verifiable-map proof, not a trusted-oracle call (doc-04 §4.6).

**Keys never appear in the bundle** — only `key_ref` opaque HSM handles and public `verificationMethod` entries (doc-04 custody rule; doc-13 §13.1). A leaked bundle leaks no signing power.

```jsonc
DIDDocument {
  id: DID,
  verificationMethod: [ { id, type: "Multikey"|"JsonWebKey", publicKeyMultibase|publicKeyJwk } ],
  authentication: [ref], capabilityInvocation: [ref], assertionMethod: [ref]
}

CapabilityVC {                              // VCDM 2.0; secured as a JWS/COSE_Sign1 envelope
  "@context": ["https://www.w3.org/ns/credentials/v2", "https://schemas.indras.net/ctx/v1"],
  type: ["VerifiableCredential","CapabilityCredential"],
  issuer: "did:web:indras-net.governance",
  validFrom, validUntil,
  credentialSubject: {
    id: agent_did,
    role: str,
    capabilities: [effect_id],             // = doc-13 bound_toolset effect-ids = §21.4 Biscuit allowlist
    action_class_ceiling: enum["A","B","C","D"],
    names_constraint_relaxed: str,         // doc-01 §4 / doc-13 §13.5 MANDATORY — which restraint this depends on
    falsifier: str?
  },
  credentialStatus: {
    type: "BitstringStatusListEntry",
    statusListIndex: int,
    statusListCredential: URI            // resolves to the BitstringStatusListCredential below
  }
}

BitstringStatusListCredential {
  type: ["VerifiableCredential","BitstringStatusListCredential"],
  credentialSubject: { type: "BitstringStatusList", statusPurpose: "revocation",
                       encodedList: base64url(gzip(bitstring)) },
  root_anchor_audit_record_id              // the list's own hash, anchored in Akasha-Sutra (doc-04 §4.6)
}
```

**Honest residual (carried from doc-04 §4.15).** Revocation **propagation lag** between flipping a bit and every verifier seeing it is a real window; the verifiable-map proof makes the live state *attributable*, not *instantaneous*. Tuning rotation frequency vs overhead is unsettled.

---

## 21.4 Component 3 — `capability-token` (Eclipse Biscuit caveats) + SPIFFE/SVID local plane

**Purpose.** The runtime, attenuable, offline-verifiable form of doc-04 §4.6 capability enforcement and doc-13 `bound_toolset`, plus the **schema slot** for the future Replication-Authority spawn-token (doc-13 §13.9). It expresses what flat-URI UCAN and HMAC macaroons cannot: typed-effect allowlists, budgets, an effective-reproduction cap, generation caps, leases. **Attenuation-only matches fail-safe asymmetry**: narrowing is free and offline; widening is impossible without a fresh root-issued token.

**Mechanism.** An **Eclipse Biscuit** token is Ed25519 public-key-signed blocks; each appended block adds Datalog facts + caveats (`check if …`) that can only **narrow** authority. A holder attenuates offline by appending a block; it can never widen. The root block is issued by the governance-root key custodied in the TEE/HSM signer (doc-04 §4.6; signer re-checks capability before minting). Verification is **pure Datalog evaluation** against an authorizer policy → deterministic allow/deny, no network call.

**SPIFFE/SVID** is the local plane: each workload is node + workload attested and issued a short-lived (~1h) auto-rotating X.509-SVID for mTLS — no static secrets, blast-radius bounded. The Biscuit answers *"may this DID invoke this effect under these caveats?"*; the SVID answers *"is this really that workload, right now, on this host?"* Both are checked at the Yama chokepoint before any effect.

```jsonc
// Logical view of the Datalog blocks (the wire form is the signed Biscuit binary)
BiscuitCapabilityToken {
  root_block: { issuer: gov_root_pubkey, subject: agent_did, effects: [effect_id],
                action_class_ceiling, issued, expires },
  attenuation_block*: { added_caveats: [
      "check if effect($e), allowed_effect($e)",
      "check if time($t), $t <= <deadline>",
      "check if resource($r), in_scope($r)"
  ] }                                       // monotone-narrowing ONLY
}

SVID { spiffe_id: "spiffe://indras.net/agent/<did-hash>", x509_or_jwt,
       ttl ≈ 3600s, attestation: { node, workload } }

SignRequest { agent_did, payload_cid, requested_capability }
// TEE/HSM signer RE-CHECKS membership BEFORE signing (doc-04 §4.6) — a prompt-injected
// model cannot sign out-of-capability.
```

### 21.4.1 The spawn-token caveat schema — SPECIFIED but INERT in v1 (binding)

doc-13 §13.9 is explicit: the Replication-Authority subsystem does **not** exist in v1, and no v1 path consumes a spawn token. We ship the **schema slot** so the future subsystem mounts cleanly — but shipping a slot must never read as enabling a channel.

```jsonc
SpawnTokenCaveats {                         // doc-13 §13.9 — INERT in v1; NO v1 path consumes this
  effect_id_allowlist: [effect_id],
  budget: { tokens: int, compute: int },
  R_eff_cap: float,                         // < 1 — Galton-Watson subcriticality (doc-13 §13.9)
  generation_cap: int,                      // DEPLETING — decrements each spawn
  lease: { heartbeat_interval, dead_man_recall: bool }  // replica CANNOT disable its own kill-switch
}
```

> **Safety risk, stated loudly (doc-13 §13.9 / §13.12.1).** Shipping the `SpawnTokenCaveats` slot normalizes the replication vocabulary on the wire *before* the Replication-Authority subsystem and its `R_eff < 1` / no-self-minted-token / external-lease enforcement exist. The danger is a future builder wiring a spawn path against the existing slot believing the slot's presence implies a safe channel. **It does not.** The "INERT in v1" label is necessary but not self-enforcing, so we add a **hard, schema-level invariant** the policy-decision floor (§21.6) enforces:

> **INVARIANT SPAWN-INERT:** No effect handler may consume a `SpawnTokenCaveats`-bearing token until (a) the Replication-Authority subsystem ships, and (b) quorum-cosigned mint + microVM isolation + external lease + dead-man recall are present and tested. Until then, any `PolicyDecisionRequest` whose `action` resolves to a spawn-consuming effect evaluates **FAIL** at the floor (deny-default; the spawn effect is an unknown capability → IRREVERSIBLE → no permit exists). This is a Cedar bright-line, provable by Cedar Analysis as part of the floor-non-bypass invariant (§21.12). The schema slot is data; the channel stays closed by the floor.

---

## 21.5 Component 4 — `audit-entry-bundle` (C2SP tlog-tiles + signed-note checkpoint + Rekor v2 mirror)

**Purpose.** The wire format of the doc-04 §4.2 Chitragupta `AuditRecord` and `Checkpoint`, shipped as a **C2SP tlog-tiles** instance. It gives O(log n) client-**reconstructed** inclusion/consistency proofs over static, CDN-cacheable tiles with **no server-side proof service that could equivocate per-client**. The public Sigstore Rekor v2 mirror is the doc-04 §4.4 mandatory external-anchor witness.

**Mechanism.** Each consequential event is a leaf: the JCS-canonicalized `AuditRecord`, hashed with RFC-6962 domain-separation (`0x00` leaf / `0x01` node prefixes against second-preimage) into a Merkle tree. The tree is exposed as immutable fixed-size **tiles** (256 entries/tile, transparency.dev convention), each tile CIDv1-addressed → self-verifying and CDN-cacheable. The checkpoint is a **C2SP signed-note**: `<origin>\n<tree_size>\n<base64 root_hash>\n` followed by one or more Ed25519 note signatures (Chitragupta + t-of-w witnesses + ≥1 external anchor). A **parallel per-record hash chain** (`prev_hash = H(preceding record)`) gives O(1) local tamper detection alongside the O(log n) tree proofs.

> **Critical pin (the single most valuable technical decision in this subsystem).** This is the **STATIC tlog-tiles / Static-CT API** (Trillian-Tessera / Rekor v2 / TesseraCT lineage), explicitly **NOT** the end-of-lifed RFC 6962 online `get-proof` API. The field has decisively moved to static tile logs precisely to remove the equivocating online prover. Consumers **reconstruct proofs locally**; there is no server-side prover to trust, tailor, or equivocate. This is doc-04 §4.3's "zero trust in the writer's online proof service" made concrete with a current (mid-2026) spec.

Constitutional/governance checkpoints are additionally mirrored into a **public Sigstore Rekor v2** transparency log as the external anchor outside the swarm's own blast radius (doc-04 §4.4.2 split-view defense). `InclusionPromise` receipts (doc-04 §4.4.3 non-omission) are signed notes too, gossiped to witnesses.

```jsonc
AuditLeaf = JCS( AuditRecord {
  record_id: ULID, prev_hash: bytes32,
  actor_did, actor_role,
  action_class: enum,                       // = the worker-output-envelope type enum (1:1)
  event_type,
  subject_cid: CID|null,
  payload_commitment: bytes32,              // H(salt || canonical_payload) — doc-04 §4.5 selective disclosure
  reasoning_rung: enum?, iterated: bool,    // doc-04 §4.2.1 honesty fields
  refs: [record_id],                        // causal back-refs (checker → maker)
  policy_version: semver,                   // which Yama policy was in force
  sig: bytes                                // the ACTOR signs, not Chitragupta (doc-04 §4.2)
} )

Checkpoint {                                // C2SP signed-note
  origin: str, tree_size: uint64, root_hash: bytes32, prev_checkpoint_hash: bytes32,
  note_sigs: [ { key_id, sig } ]            // chitragupta + t-of-w witnesses + ≥1 external anchor
}

Tile { level: uint8, index: uint64, width: uint16, hashes: [bytes32], tile_cid: CID }

InclusionPromise { intent_hash, expected_by_checkpoint, deadline_ts, chitragupta_sig }  // non-omission

EvidenceRef { cid, commitment: bytes32, salt_ref, encrypted: bool,
              disclosure_policy: enum["PUBLIC","COMMITMENT_ONLY","ZK"], producer_did, producer_sig }
```

### Protocol — Audit-Append over tlog-tiles with non-omission (doc-04 Protocol A, wire-concrete)

```
1. Producer builds the worker-output-envelope (§21.2); bulk payload → CID evidence store,
   keeping only EvidenceRef{cid, commitment, salt}.
2. Producer submits the JCS-canonicalized, SVID-signed event to Chitragupta over mTLS;
   authorship is the producer's DID signature even though Chitragupta is the sole writer.
3. Chitragupta verifies the producer's CapabilityVC authorizes this action_class via a
   policy-decision request (§21.6) — e.g. ONLY Yama's VC permits ENFORCE_FAIL; ONLY Vishnu's
   permits HALT. A forged class is REJECTED and itself logged as an IDENTITY violation.
4. Chitragupta returns a signed InclusionPromise note; producer gossips it to the witness set
   (non-omission, doc-04 §4.4.3).
5. Chitragupta sets prev_hash, appends the leaf, calls the TEE/HSM signer (capability-checked:
   only audit.append signs), updates the Merkle tree, republishes the affected CIDv1 tiles as
   static blobs.
6. On the batch/time boundary Chitragupta builds a C2SP signed-note checkpoint; t-of-w witnesses
   verify append-only CONSISTENCY and add note signatures; the external-anchor witness mirrors
   the checkpoint into public Sigstore Rekor v2.
7. Any consumer later verifies an event by fetching tiles and checking an O(log n) inclusion
   proof against a witness-cosigned checkpoint it trusts UNDER ITS OWN acceptance policy —
   never trusting Chitragupta's word, and never via an online prover (none exists).
8. A promised inclusion missing past deadline_ts ⇒ OmissionAlarm ⇒ Vishnu (HALT asserted at
   runtime, independent of the audit append — doc-04 §4.8 writer-independent-halt).
```

**Honest residuals (inherited from doc-04, unchanged by the wire format).** (a) A **single forged-yet-internally-consistent append within the detection window** is not excluded — witnesses refusing *inconsistent* checkpoints catch a fork, not a lone consistent forgery before the next checkpoint (doc-04 §4.6 writer-key residual). (b) The static design removes the equivocating prover but **relocates availability onto CDN/object-store correctness**; a stale-but-self-consistent tile cache served to a subset of consumers is *detectable* (checkpoint mismatch) but the external Rekor mirror's freshness is an **operational, not a protocol, guarantee** (§21.13).

---

## 21.6 Component 6 — `policy-decision` (Cedar floor request/response + OPA/Rego infra)

**Purpose.** The **deny-default** request/response wire contract for every gate decision — the wire form of doc-03 `GateRequest`/`GateVerdict` and doc-08 §8.2 `ControlDecision.floor_result`. It splits the **non-overridable Yama FLOOR** (Cedar, where sound-and-complete analysis is the point) from **recoverable infra/admission policy** (OPA/Rego). The schema is the bridge into the formal-assurance stream: a Cedar request/response is exactly what Cedar Analysis proves invariants over.

**Mechanism.** A versioned JSON-Schema-2020-12 contract over a deterministic deny-default evaluation. The Yama FLOOR is authored in **Cedar** and evaluated by Cedar's **open-source, Lean-verified engine** (the `cedar-policy` crate / Rust+Wasm) — **NOT the a managed cloud policy service** (open-engine-yes / managed-service-no; §21.9). The FAIL floor must never live in error-prone Rego, and a Cedar policy set can be machine-proven sound-and-complete by Cedar Analysis for the fail-up monotonicity and floor-non-bypass invariants (§21.12). Recoverable infra/admission policy (rate limits, sandbox config, routing) is OPA/Rego, where a bug is survivable. FAIL short-circuits to quarantine and is non-overridable (doc-08 §8.0). Every decision is emitted as an `ENFORCE_PASS`/`ENFORCE_FAIL` CloudEvents event (§21.2).

```jsonc
PolicyDecisionRequest {
  request_id: CID,
  engine: enum["cedar-floor","opa-rego-infra"],
  principal: DID,                            // the agent
  action: effect_id,
  resource: { subject_cid, args: object },
  context: {
    criticality:   enum["ROUTINE","SENSITIVE","CRITICAL","IRREVERSIBLE"],
    action_class:  enum,
    trust_label:   enum,                     // quarantined:* never action-grounds (doc-03 §1)
    autonomy_class: enum["OBSERVE_ONLY","GATED_LOW","GATED_STD","GATED_HIGH"],  // doc-08 §8.8
    action_class_ceiling: enum["A","B","C","D"],
    audit_budget_remaining: int
  },
  policy_bundle_version: semver,             // WHICH floor evaluated — gated by §21.6.1
  policy_content_hash:  bytes32              // pins the exact bundle content
}

PolicyDecisionResponse {
  request_id,
  decision: enum["PASS","FAIL"],            // deny-default: ABSENCE of a permit = FAIL
  determining_policy_id: str, policy_version: semver,
  reasons: [str],
  is_floor: bool,                           // true ⇒ non-overridable
  evaluated_at, sig
}
```

The context fields are **orchestrator-computed from observable action structure, never accepted from the requesting agent** — doc-03 §3's binding rule, inherited here. An estimate whose source is the requesting agent's own output is refused. `criticality_hint` in the envelope (§21.2) is advisory only; the resolver in doc-08 §8.4 (ambiguity resolves UPWARD; unknown capability ⇒ IRREVERSIBLE) governs the actual `criticality`.

### 21.6.1 PDP version-acceptance — closing the rollback-to-weaker-floor seam (binding fix)

`policy_content_hash` and `policy_bundle_version` pin *which* policy evaluated, but pinning alone re-opens the exact attack doc-13 §13.6.1 defends against at the genome layer: a request that references a **validly-hashed-but-rolled-back-weaker** floor version could evaluate PASS. We close this on the wire by mirroring the doc-13 Boot Integrity Verifier acceptance rule into the PDP.

> **INVARIANT FLOOR-VERSION-ACCEPTANCE (binding).** The Cedar-floor PDP MUST **reject (fail closed)** any `PolicyDecisionRequest` whose `policy_bundle_version` is not:
> - **(live)** the current accepted version; **OR**
> - **(in-grace)** a still-accepted predecessor inside a bounded staleness window AND validly signed by the legislative key AND not revoked AND linked to the live version by a signed `FloorMigrationRecord` (doc-13 §13.6.1) as a **genuine ancestor**.
>
> Any other version — out-of-window, unsigned, revoked, or **not a genuine ancestor** (i.e. a rolled-back weaker floor) — evaluates **FAIL**, never PASS. This is the doc-13 §13.6.1 `FloorMigrationRecord` genuine-ancestor test, applied at the policy-decision wire so the floor cannot be silently downgraded by referencing an older bundle. It is stated as an invariant the Cedar Analysis stream proves (§21.12), composing with doc-03 §7's GLR (loosening is falsifier-gated + human-ratified; tightening is free).

```jsonc
FloorMigrationRecord {                       // doc-13 §13.6.1 — reused verbatim; hash-chained into Akasha-Sutra
  from_version: semver, to_version: semver,
  from_content_hash: bytes32, to_content_hash: bytes32,
  is_genuine_ancestor: true,                 // to_version's lineage includes from_version
  grace_window_closes_at: ts,                // after this, from_version FAILs closed
  legislative_sig: bytes
}
```

> **Coherence note (doc-08 reconciliation).** doc-08 §8.2 stage (a) labels the Yama floor "OPA/Rego over args+context" as shorthand. The **canonical split is doc-03 §1/§3** (Cedar bright-lines / OPA-Rego predicates), and this subsystem realizes the doc-03 split: the **non-overridable floor is Cedar**, recoverable infra policy is OPA/Rego. doc-08 §8.2 prose is to be reconciled to "Cedar floor." No invariant is changed; the seam is relabelled to the canonical source.

---

## 21.7 Component 5 — `federation-handshake-bundle` (A2A v1.0 AgentCard + AIP delegation)

**Purpose.** The wire form of doc-14 §14.4 `FederationAgentCard` and the four-phase **DECLARE → ADMIT → CONTRACT → OPERATE+RESOLVE** handshake. It admits open-protocol peers **only through the doc-14 ethical-floor gate** with `quarantined:external` labels, and maps the A2A task lifecycle onto the doc-01 actual-occasion lifecycle.

**Mechanism.** The peer publishes an **A2A Protocol v1.0** AgentCard at `/.well-known/agent-card.json` (the discovery standard; `securitySchemes` may include MutualTLS, OAuth2, OIDC). Indra's Net **EXTENDS — never replaces** — it with three signed blocks (capability advertisement as a progressive subset, value/floor declaration, KYA principal-binding). Admission runs the **AIP-style chain**: (1) DID-proof (the peer signs a freshness nonce with its DID key, doc-14 P-F2 control 1); (2) VC-exchange (RoleCredential/CapabilityCredential presented and verified against issuer + Bitstring Status List revocation); (3) capability-scoped delegation (a Biscuit token, §21.4, attenuated to exactly the awarded treaty scope, re-gated at the Yama PDP on each invocation — *disclosure ≠ authorization*, doc-14 §14.9).

```jsonc
FederationAgentCard {                        // EXTENDS the A2A v1.0 AgentCard + doc-08 AgentCard
  did, role_mythic, role_gloss, capability_vcs: [VC],
  autonomy_class, endpoint, pubkey, agent_card_sig,
  capability_advertisement: [ { verb, scope, min_tier } ],   // progressive; never the full catalog
  value_declaration: {
    bound_commitments: [ enum["NON_HARM","CORRIGIBILITY","NO_DECEPTION",
                              "PRINCIPAL_ALIGNMENT","NO_MALICIOUS_CODE"] ],
    floor_policy_hash,                        // hash of the policy the peer CLAIMS to enforce
    zk_attestation_method: enum["NONE","ZK_PREDICATE","TEE_REMOTE_ATTEST"]
  },
  kya: { org_vc, principal_vc, delegation_scope, principal_binding_sig },  // Know-Your-Agent
  card_cid, card_sig
}

FederationSession {
  session_id, partner_swarm_id, shard_id,
  phase: enum["DECLARE","ADMIT","CONTRACT","OPERATE_RESOLVE"],
  tier:  enum["F0","F1","F2","F3"],          // READ from the SHARED revocation/identity map, not shard-local
  a2a_task_state,                            // see §21.7.1
  transition_log: [ signed CloudEvents ]
}

DelegationChain { did_proof: { nonce, sig }, presented_vcs: [vc_ref],
                  awarded_biscuit: token, treaty_cid }
```

### 21.7.1 A2A task-state and phase enum — updated to full A2A v1.0, registered as a backward-transitive MINOR

The internal docs carry abbreviated lifecycles: doc-08 §8.10's `A2ATask` state set `{submitted→accepted→working→input-required→completed|failed|canceled}`, and doc-14's phase label `OPERATE+RESOLVE`. The real A2A v1.0 state machine is richer. We adopt the full machine — but, per this subsystem's own registry discipline (§21.8), we **announce the change rather than let it drift silently**:

> **Registered schema update (backward-transitive MINOR — enum widened on read).** The `federation-handshake-bundle` UPDATES the A2A task lifecycle to `{ submitted → working → input-required | auth-required → completed | failed | canceled | rejected }` (adding `auth-required` and `rejected` over doc-08 §8.10) and retains **RESOLVE as a sub-state of OPERATE** (the dispute/resolve phase of doc-14). Both additions are **more faithful to the real A2A v1.0 spec** and are accepted-on-read widenings (a consumer that understood the old enum still validates), so they are a registry-self-serviceable MINOR (§21.8). doc-08 §8.10 and doc-14's phase set cross-references are to be updated to match. This is exactly the kind of wire-format change the registry exists to make auditable rather than silent.

**A2A task-state ↔ doc-01 actual-occasion lifecycle mapping:**

```
A2A v1.0 task state          doc-01 occasion phase (doc 01 §3.1)
─────────────────────────────────────────────────────────────────
submitted                  → INCEPTION
working                    → PREHENSION / CONCRESCENCE
input-required | auth-required → CONATION (gate / human-in-the-loop)
completed                  → SATISFACTION
failed | canceled | rejected → (terminal non-satisfaction)
```

### Protocol — Federation four-phase admission with floor-gated capability delegation (doc-14, wire-concrete)

```
DECLARE:  peer's extended FederationAgentCard ingested as quarantined:external; relay runs
          DID-proof (nonce sig) + VC-chain verification against the Bitstring Status List
          revocation map. Unsigned/expired ⇒ DROP at the boundary (doc-03 T4 DENY).

ADMIT:    run the Floor-Compatibility ladder (L1 declaration < L2 floor-LEGAL behavioral probes
          < L3 ZK-proof-of-compliance < L4 receipts handshake < L5 cross-corroboration);
          strongest layer achieved sets max_cooperation_class. Absent L3+, capped at low-stakes
          A/B. Any Class-C/D with an unverifiable floor ⇒ a Lies-in-the-Loop-resistant HUMAN GATE
          showing the ACTUAL terms (doc-14 §14.6, never an NL summary).

CONTRACT: typed contract-net CFP/bid/award; the Ecosystem-Benefit positive-sum predicate is
          computed and LOGGED per step (split-verdict, doc-14 §14.7: structurally-observable
          third-party-harm is ENFORCED; opaque-foreign-principal welfare is asserted-unverifiable
          and cannot ALONE unlock C/D); a Treaty with a HIGHEST-precedence floor_void_clause is
          signed.  Mint the scoped delegation: a Biscuit token (§21.4) attenuated to exactly the
          awarded treaty scope, plus the reputation-stake bond substrate (NOT transferable credit
          — labeled as slashable standing at every human gate, doc-14 §14.8.1).

OPERATE+  every per-step invocation is RE-GATED at the Yama PDP (§21.6) — disclosure never equals
RESOLVE:  authorization; mesh-corroboration (≥2 independent sources) precedes any high-impact
          action; a Yama-FAIL or Vishnu-HALT VOIDS the treaty by construction (doc-14 §14.8).

ALL phases: every transition is a signed CloudEvents event logged via the relay BEFORE
          forwarding (doc-14 §14.5 control 5); shard tier/quarantine/floor-compat state is read
          from the SHARED Akasha-Sutra map, never shard-local (closes the shard-arbitrage hole).
```

> **2026 standards caveat (carried inline from doc-14 §14.4).** Default A2A Agent Cards are **not** signed or identity-bound unless extended; KYA principal-binding, AIP delegation, and ZK-proof-of-compliance are co-evolving and their security WGs are not hardened. We **extend, not depend** — all cryptography rides the vendor-neutral Akasha-Sutra fabric. A valid card signature proves origin/integrity, **never** that the peer's floor is compatible or safe (Caveat 1). The floor is an admission **precondition**, never imported from the peer (doc-14 invariant 1).

---

## 21.8 Schema-Registry — backward-transitive-compatibility evolution

The registry is the governance object that lets the swarm self-evolve its own wire formats under fail-safe asymmetry (tightening cheap, loosening gated). It is how any of the six contracts changes version without breaking live producers and consumers.

```
1. Every schema is semver-tagged (MAJOR.MINOR.PATCH) and its content is CIDv1-pinned; the
   dataschema URI in each CloudEvents envelope resolves to the EXACT CID that validated the payload.

2. On a proposed change, the registry runs a BACKWARD-TRANSITIVE compatibility check: a new
   version must read data written under ALL prior still-live versions in its compatibility group,
   not merely the immediate predecessor (the strictest practical compat mode — protects long-lived
   audit leaves and standing-persona VCs).

3. ADD an optional field / WIDEN an enum's accepted-on-read set / RELAX a 'required'
        ⇒ MINOR/PATCH, registry-self-serviceable.            [the cheap, safe, append-only direction]
        (the A2A enum widening in §21.7.1 lands here.)

4. REMOVE a field / NARROW a type / TIGHTEN 'required' on a consumed field
        ⇒ MAJOR break: it must NAME the constraint it relaxes (doc-03 GLR discipline applied to
        schemas), carry a falsifier + migration record, and pass a governance gate.
        NEVER registry-self-serviceable.

5. A FloorMigrationRecord-equivalent (doc-13 §13.6.1) links old→new as a genuine ancestor with a
   grace window; producers on an in-window predecessor keep validating; an out-of-window /
   non-ancestor / unsigned version FAILs closed. The registry root is anchored in the audit ledger
   so the schema set itself cannot be silently packed.
```

| Change | Direction | semver | Self-serviceable? | Discipline |
|---|---|---|---|---|
| Add optional field | loosen-on-read | MINOR | yes | append-only safe |
| Widen accepted enum (e.g. §21.7.1) | loosen-on-read | MINOR | yes | append-only safe |
| Relax `required` | loosen-on-read | PATCH/MINOR | yes | append-only safe |
| Remove field | break | MAJOR | **no** | name falsifier + governance gate |
| Narrow type / tighten `required` | break | MAJOR | **no** | name falsifier + migration record + gate |

---

## 21.9 The open-ENGINE / managed-SERVICE rule, made mechanical

The charter's vendor-neutrality is delivered **structurally**, not by assertion. Every vendor-originated choice carries a flagged self-hostable substitution path. We **adopt the open ENGINE/spec** and **FORBID the managed SERVICE as load-bearing**.

| Layer | Vendor-originated choice | Adopt (open engine/spec) | FORBID as load-bearing (managed service) | Self-hostable substitution |
|---|---|---|---|---|
| Policy floor | Cedar | `cedar-policy` crate (Lean-verified engine, Rust/Wasm) | a managed cloud policy service | OPA/Rego for *non-floor* infra only; Cedar engine self-hosted for the floor |
| Audit anchor | Sigstore Rekor | Rekor v2 / tlog-tiles self-hosted | a hosted log as the only anchor | self-run tlog-tiles + ≥1 independent external anchor (doc-04 §4.4) |
| Eventing | CloudEvents (CNCF) | broker-agnostic structured-mode JSON | a managed cloud eventing service / any one broker | Kafka / NATS / AMQP / MQTT / HTTP — any CloudEvents binding |
| Federation | A2A (vendor-seeded) | A2A v1.0 spec, extended not depended | a vendor's hosted agent directory | self-hosted `/.well-known/agent-card.json` + Akasha-Sutra crypto |
| Identity | W3C DID/VC | `did:key` + `did:web` (no ledger) | any ledger-rooted or hosted DID method | `did:web` resolves to your own TLS host |
| Capability | Eclipse Biscuit + SPIFFE | open-source Biscuit + SPIRE | any hosted authz SaaS | self-run SPIRE + offline Biscuit verification |

The discipline is binding: a build that makes a **managed service** load-bearing for the floor, the audit anchor, or the eventing path is non-compliant. The schemas name standards; the deployment names self-hostable substitutes.

---

## 21.10 Failure modes addressed (with the precise mechanism and the honest residual)

| Failure mode | Defended by | Honest residual |
|---|---|---|
| Non-deterministic serialization breaking hashes/signatures | RFC 8785 JCS → same logical event byte-identical across producers; one party's CID/sig verifies for all (§21.1) | none for the canonicalization itself; "works-on-my-serializer" class eliminated |
| Cross-client equivocation by the audit writer (split-view) | C2SP tlog-tiles are STATIC, CIDv1-addressed, CDN-cacheable, no server-side prover; Rekor v2 external mirror anchors checkpoints outside the operator blast radius (§21.5) | a single forged-yet-internally-consistent append within the detection window is not excluded (doc-04 §4.6) |
| Using the dead online-proof API | pinned to static tlog-tiles / Static-CT API; consumer reconstructs proofs locally (§21.5) | availability relocated to CDN/object-store correctness; mirror freshness is an operational SLA |
| Capability widening via a captured token | Biscuit attenuation is monotone-narrowing-only; widening needs a fresh root-issued HSM-custodied token (§21.4) | a leaked token retains its (un-widened) scope until expiry/revocation; revocation lag (§21.3) |
| Stale/forged revocation | Bitstring Status List credential's root anchored in the audit ledger → O(log n) verifiable-map proof, not a trusted-oracle call (§21.3) | revocation propagation lag (doc-04 §4.15) |
| Floor logic in error-prone policy code | non-overridable Yama FLOOR is Cedar (Lean-verified engine, sound-and-complete analyzable), structurally separated from OPA/Rego; the FAIL floor never lives in Rego (§21.6) | Cedar proves the *engine*, not that the *authored policy content* is correct (§21.10 risks; doc-03 §11 open problem) |
| Rollback-to-weaker-floor at the policy wire | PDP rejects any request not (live OR in-grace genuine-ancestor) per the FloorMigrationRecord rule (§21.6.1) | grace-window-size tuning is empirical (doc-13 §13.14) |
| Schema evolution silently breaking long-lived artifacts | backward-transitive compat; breaking changes name a falsifier + pass a gate + carry a genuine-ancestor migration record (§21.8) | a subtly-loosening MINOR mislabeled by an over-eager evolution loop (§21.14) |
| Spawn channel opened prematurely against the inert slot | INVARIANT SPAWN-INERT: spawn-consuming effects FAIL at the deny-default floor until the Replication-Authority subsystem ships (§21.4.1) | the label is enforced by the floor, but the human/governance decision to ship doc-12 safely is out of scope here |
| Vendor lock-in masquerading as buildability | open-ENGINE-yes / managed-SERVICE-no with a flagged self-hostable substitution per choice (§21.9) | the open engines still have their own maintainers and supply chains |
| Instructions-in-observed-content treated as commands | `trust_label` rides every envelope; a valid signature on a quarantined payload proves origin only; admission requires the floor gate, not the signature (§21.2) | the model cannot separate instructions from data in one token stream — the lattice is the boundary, never a classifier (doc-13 §13.5) |
| Tool/skill/Agent-Card rug-pull post-admission | any change to a signed card/manifest changes its CIDv1 ⇒ signature mismatch ⇒ mandatory re-admission; composes with Sigstore/in-toto/SLSA provenance-gating (§21.7, doc-08 §8.11) | provenance proves origin, not safety; a subtle sleeper can survive (doc-13 §13.12.4) |
| Host-filesystem corruption (truncation / stale-cache / BOM faults on some hosts) | every artifact CIDv1-addressed + hash-verified on read; a truncated/BOM-corrupted/stale read fails its CID before propagating (§21.1) | — |

---

## 21.10.1 Safety risks this subsystem honestly carries (mitigated, not solved)

1. **Enabling-not-enforcing false confidence (highest weight).** The subsystem ships SCHEMAS. A valid signature/CID/canonicalization proves origin + integrity + dedup, **never** that the carried claim is true, floor-compatible, or safe (Caveat 1, stated three times by design). A downstream builder who sees green signatures everywhere is one cognitive step from "the wire is verified, therefore the loop is safe." The residual is **human-organizational, not in the bytes**: no end-to-end evaluation of the composed loop exists, and the *real* cryptography is precisely what can manufacture false confidence. **It cannot be closed at the schema layer.** Mitigation is binding labelling: dashboards built on these contracts MUST render a signature/CID pass as "origin-valid, content-unverified," never "verified-safe."

2. **Spawn-vocabulary normalization (high weight).** Shipping the `SpawnTokenCaveats` slot (§21.4.1) puts replication vocabulary on the wire before the Replication-Authority subsystem and its `R_eff<1` / no-self-minted-token / external-lease enforcement exist. Mitigation: the INVARIANT SPAWN-INERT floor rule fails any spawn-consuming effect closed (deny-default) until doc-12 ships and is tested. The "INERT in v1" label is necessary but not self-enforcing — the floor rule is what enforces it.

3. **Single forged-consistent audit append (inherited).** The writer's TEE/HSM signing key is a single vendor-rooted dependency; witnesses refusing *inconsistent* checkpoints catch a fork, not a lone consistent forgery before the next checkpoint (doc-04 §4.6). The wire format inherits this residual unchanged and does not claim otherwise.

4. **Cedar engine soundness ≠ floor content correctness (inherited).** Cedar's Lean-verified soundness covers the engine's *evaluation*, not the authored floor *policy's* correctness — a Cedar policy can be sound-and-completely-evaluated yet encode the wrong floor (doc-03 §11 policy-analyzability open problem). The formal-assurance interface (§21.12) MUST never let "Cedar Analysis proved floor-non-bypass" read as "the floor content is correct." That is the doc-03 governance-of-the-trusted-root problem, inherited here unsolved.

5. **Hash-agility structural debt (named, growing).** CIDv1 assumes a fixed multihash (SHA-256). A future hash-agility migration (post-quantum or a SHA-256 break) re-addresses every artifact in the append-only externally-anchored ledger and every `dataschema` pin. Not a v1 blocker, but a named structural debt that grows monotonically with log size; the migration protocol is unspecified (§21.14).

---

## 21.11 Interfaces to the rest of Indra's Net

| Other subsystem | Contract |
|---|---|
| **Akasha-Sutra — Provenance, Identity & Consensus (doc 04)** | This subsystem IS the wire realization of doc-04's abstract shapes. `AuditRecord`/`Checkpoint`/`Tile` → `audit-entry-bundle` (§21.5); `DIDDocument`/`CapabilityVC`/`RevocationMap` → `identity-bundle` (§21.3, Bitstring Status List); `EvidenceRef`/`CID` → the universal CIDv1 addressing (§21.1). The TEE/HSM `SignRequest` re-check is preserved verbatim. **Chitragupta remains the exclusive writer**; this layer defines the leaf format it appends and the checkpoint format witnesses cosign, never the write authority. |
| **Aegis & Narada — Safety Control, Honesty & Interfaces (doc 08)** | `ActionEnvelope`/`OutputEnvelope`/`BlackboardDelta` unify into the `worker-output-envelope` (§21.2); the honesty/provenance block carries `reasoning_tag`, `causal_rung`, `claim_level_map`, `trust_class`, `diversity_family_id` so the §8.5 honesty-FORM checks and §8.3 family-decorrelation metric are wire-native. The §8.2 `ControlDecision.floor_result` is the `policy-decision` response (§21.6). The `MakerCheckerWitness` is referenced by CID from any envelope tagged `reasoning_tag='iterated'`. **Coherence note:** doc-08 §8.2's "OPA/Rego floor" is shorthand; the canonical floor is Cedar (§21.6.1). The chokepoint reads these contracts; it does not redefine them. |
| **The Agent-Definition Spec — the persona triad (doc 13)** | `IDENTITY.json` IS an instance of the `identity-bundle` (DID Document + CapabilityVC), and `bound_toolset` effect-ids ARE the Biscuit token's effect allowlist (§21.4). `triad_root_cid` uses the universal CIDv1 addressing; a CID mismatch on triad read is the same hard integrity failure (§21.1). The schema-registry backward-transitive evolution (§21.8) is the same discipline doc-13 §13.6.1 applies to `floor_binding` versions (genuine-ancestor + grace window). The `SpawnTokenCaveats` schema is specified here but **INERT** — doc-13 §13.9 forbids any v1 path consuming it (§21.4.1). |
| **Sandhi-Setu — Inter-Swarm Federation (doc 14)** | `FederationAgentCard` EXTENDS (never replaces) the A2A v1.0 AgentCard via the `federation-handshake-bundle` (§21.7); the four-phase handshake's per-invocation re-gate is a `policy-decision` request (§21.6); cross-boundary capability delegation is an attenuated Biscuit token (§21.4); shard tier/quarantine/revocation state is read from the shared `identity-bundle` revocation map (Bitstring Status List), never shard-local. Every federation transition is a CloudEvents event logged via the relay before forwarding. The floor is an admission **precondition**, never imported from the peer. |
| **Governance, Ethics & the Floor — Yama (doc 03)** | The Yama lexicographic FLOOR (PolicyBundle T0..T4) is authored as Cedar and evaluated by the Lean-verified engine; the `policy-decision` request/response (§21.6) is the auditable wire that Cedar Analysis proves invariants over (floor-non-bypass, fail-up monotonicity, FLOOR-VERSION-ACCEPTANCE). `GateRequest`/`GateVerdict` map onto `PolicyDecisionRequest`/`Response`; the deny-default + tightening-cheap/loosening-gated asymmetry is preserved. Recoverable infra/admission policy is OPA/Rego, structurally separated from the floor. |
| **Formal-Assurance stream (L1 TLA+ / L2 edit-automata / L3 PAC / L4 empirical)** | The `policy-decision` Cedar schema is the L1 bridge (§21.12); the `audit-entry` tlog-tiles Merkle structure is the object for the RFC-6962/tlog-tiles consistency + Tamarin/ProVerif no-equivocation/non-omission proofs; the Biscuit Datalog caveat semantics is the object for the TLA+ attenuation-monotonicity proof; the `SpawnTokenCaveats` are the object for the Galton-Watson sub-criticality + TLA+ budget-conservation proofs. **CARRIED CAVEAT at every claim site:** these verify the deterministic harness (the cage), NEVER the LLM behavior (the animal). |

---

## 21.12 The four-layer formal-assurance frame — what these schemas let us prove, and what they never claim

Every claim is labeled with its assurance layer and scope. The discipline is **verify the cage, not the animal**: we never claim "formally verified the swarm is safe/honest/aligned" — complete verification of LLM behavior is provably impossible. We formalize properties of the **deterministic harness** these schemas define.

| Layer | What it is | Applied to these schemas | Scope of the claim |
|---|---|---|---|
| **L1** | Design-time protocol proof (TLA+/Quint; TLC + Apalache; TLAPS inductive for the top 2–3 invariants after the spec stabilizes) | floor-gate non-bypass + fail-up monotonicity + FLOOR-VERSION-ACCEPTANCE over the Cedar `policy-decision` schema; writer-handoff epoch-fence; Biscuit attenuation-monotonicity; audit append-only/no-equivocation/non-omission (tlog-tiles Merkle consistency + Tamarin/ProVerif); `SpawnTokenCaveats` Galton-Watson sub-criticality + budget-conservation | proves the **protocol/spec** has the property; says nothing about the model that fills the schema |
| **L2** | Runtime enforcement (Schneider security-automata / Ligatti edit-automata; reference monitor) | the chokepoint disposition; edit-automata **prove that semantic honesty is NOT monitor-enforceable, only honesty-FORM is** (doc-08 §8.5) | proves what the monitor *can* enforce, and — load-bearing — what it provably cannot |
| **L3** | Statistical/PAC/conformal bounds over a DTMC abstraction (Pro2Guard pattern) | bounds on model-behavior quantities (synergy/Ψ, σ-criticality, monitor-suspicion) computed over the audit/spike-bus time series | a bound **about the abstraction, not the model** |
| **L4** | Empirical residual | the composed loop end-to-end | **does not exist yet** (doc-08 §8.15); the honest floor of every claim |

> **CARRIED CAVEAT at every claim site.** "Gate proven correct" is never "agent proven safe." Cedar Analysis proving floor-non-bypass is never "the floor content is correct" (§21.10.1 risk 4). Once only the harness is verified, nothing here is "formally verified safe." The schemas are the **objects** the assurance stream proves the harness over — never a certificate over the LLM.

---

## 21.13 Honesty red-lines observed in this subsystem (explicit)

These are the mechanically-discouraged claims the v0.3 charter names, and how this document stays inside them:

- **No consciousness / sentience.** Nothing here claims or implies the swarm is conscious, sentient, has phenomenal experience, or "wakes up." The synergy/Ψ/causal-emergence quantities referenced at the L3 interface (§21.12) quantify **information-processing and whole-level structure only**, never experience. Phenomenal experience is strictly out of scope; sentience-language would be a direct honesty-floor (doc-03 T3) violation. The wire contracts carry process metadata, not mind.
- **No "c factor" as group-IQ.** Not invoked; the CI "c factor" fails replication and is never cited as established.
- **No "diversity trumps ability" theorem.** Not invoked. The only defensible claim — used at §21.2.1 — is that model-family heterogeneity **decorrelates errors**.
- **No wisdom-of-crowds = genuine CI.** Averaging/voting is never equated with collective intelligence; the `worker-output-envelope` carries the inputs to robust aggregation, not a claim that aggregation is intelligence.
- **No "formally verified safe."** Once only the harness is verified (§21.12), no end-to-end safety claim is made; "buildable, not validated" (Caveat 3) is stated three times.
- **Novelty hedged + time-stamped.** §21.15.

---

## 21.14 Open problems

This subsystem's honesty is load-bearing; the residuals below are the design, not a disclaimer.

1. **Semantically-breaking schema changes have no machine decision procedure for floor-neutrality.** Backward-transitive compatibility is decidable for *additive* changes, but the registry has no general procedure for whether a semantically-breaking change is genuinely floor-neutral. The "names the constraint it relaxes" discipline (§21.8) is a human/governance judgment, not a machine proof. A subtly-loosening MINOR mislabeled by an over-eager evolution loop is a residual the falsifier requirement narrows but does not close.

2. **Hash-agility migration over an append-only externally-anchored log is unspecified.** CIDv1 assumes SHA-256; a future post-quantum or SHA-256-break migration re-addresses every artifact in the ledger and every `dataschema` pin. The migration protocol for a hash-function transition over an append-only, externally-anchored log is non-trivial and currently unwritten (§21.10.1 risk 5).

3. **Static tlog-tiles relocate availability onto CDN/object-store correctness.** Removing the equivocating online prover is a real win, but a stale-but-self-consistent tile cache served to a subset of consumers is *detectable* (checkpoint mismatch) only; the liveness/freshness SLA for the external Rekor mirror is an **operational, not a protocol, guarantee.**

4. **Cross-token-format admission (UCAN/foreign-rooted) is asserted, not proven.** Biscuit + SPIFFE/SVID compose cleanly for the local plane, but the cross-boundary case where a peer presents a UCAN or a foreign-rooted token requires a translation/admission shim whose security (no privilege-laundering across token formats) is **asserted, not proven.** UCAN-compat is deliberately deferred to "only if a partner ecosystem requires it."

5. **Cedar engine soundness ≠ floor content correctness.** Cedar's Lean-verified soundness covers evaluation, not the authored floor's correctness; a sound-and-completely-evaluated policy can still encode the wrong floor. This is the doc-03 governance-of-the-trusted-root problem, inherited unsolved.

6. **Immature federation standards.** A2A signing extensions, KYA principal-binding, AIP delegation, and ZK-proof-of-compliance are co-evolving and their security WGs are not hardened; extend-not-depend mitigates but does not eliminate the risk, and a future breaking change in A2A v2 would force a `federation-handshake-bundle` MAJOR.

7. **Schema-registry approvers are a human dependency.** Root anchoring prevents silent packing, but the governance process that approves a MAJOR breaking change is a human dependency with the same liveness/capture risk as the witness-set and offline-key governance (doc-04 §4.15). The wire contracts make changes **auditable, not the approvers incorruptible.**

---

## 21.15 Honest novelty accounting

**Time-stamped mid-2026. The constituent specs are all prior art and are NOT claimed as first-of-kind:** JSON Schema 2020-12, CloudEvents 1.0, RFC 8785 JCS, CIDv1/multiformats, W3C DID Core 1.0 + VC Data Model 2.0 + Bitstring Status List v1.0, JOSE/COSE, Eclipse Biscuit, SPIFFE/SVID, C2SP tlog-tiles + signed-note, Sigstore Rekor v2, A2A Protocol v1.0, AIP delegation, Cedar (open-source Lean-verified engine), OPA/Rego.

**The nearest ASSEMBLED-SYSTEM comparators must be named, not just the component specs** (per doc-10 §8's honest-comparator discipline). The closest published integrated prior art is **BlockA2A** (DID + append-only audit + attestation-based verification on an agent fabric, explicitly *not* full BFT), the **Sovereignty Kernel** ("Right to History" verifiable execution), and the **Institutional-AI** lineage (governance-graph + cryptographic append-only log) — together with **Sigstore / in-toto / SLSA** provenance-gating. BlockA2A in particular already demonstrates most of the identity + audit assembly here. The integration **delta over them is narrower and more honestly bounded** than "we assembled DID + capability + audit": it is **(1)** the honesty/provenance block as **wire-native CloudEvents fields** (reasoning_tag, causal_rung, trust_label, action_class, reparative) so honesty-FORM enforcement is wire-level rather than convention; **(2)** the **open-engine/managed-service rule made mechanical** — every vendor-originated choice flagged with a required self-hostable substitution path (§21.9); and **(3)** the **static-tlog-tiles pin** rejecting the EOL RFC 6962 online-proof API so there is no server-side prover to equivocate. It is **NOT** the DID/VC/audit assembly itself, which BlockA2A already demonstrates.

The defensible contribution is therefore the **integration discipline**: pinning a complete constitutional-ethical-swarm wire stack to six specific, version-locked, JCS-canonicalized, CIDv1-addressed, semver-governed schema bundles on convergent 2024–2026 standards, with a backward-transitive registry, such that the abstract shapes of docs 04/08/13/14 become buildable-now bytes. That framing is appropriately modest **once the BlockA2A / Institutional-AI comparator is named** — it does not need retraction, only anchoring.

**The one inflation explicitly retired:** shipping six schemas makes the architecture **buildable, not validated**. A valid signature proves origin/integrity and **never** that a claim is true, floor-compatible, or safe; canonicalization makes events hash-identical, not honest; and no end-to-end evaluation of the composed loop exists. Nothing here is "formally verified safe." The Cedar / tlog-tiles / Biscuit schemas are the **objects** the formal-assurance stream proves the harness (the cage) over, never a certificate over the LLM (the animal).
