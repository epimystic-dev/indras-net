# Reference Schemas — Indra's Net wire contracts

> Machine-readable contract schemas for the protocols in [`../../docs/21-protocols-and-wire-contracts.md`](../../docs/21-protocols-and-wire-contracts.md). JSON Schema draft 2020-12, vendor-neutral, semver-tagged. These make the architecture buildable: implement against these and the floor / audit / identity / capability contracts are fixed.

| Schema | Purpose |
|---|---|
| [`worker-output-envelope.schema.json`](worker-output-envelope.schema.json) | Standard: JSON Schema draft 2020-12, designed as the `data` payload of a CloudEvents 1.0 structured-mode event (outer event supplies id=ULID, source=producing DID, type=reverse-DNS verb e.g. net.indras.enforce.fail, subject=subject_cid, dat |
| [`identity-bundle.schema.json`](identity-bundle.schema.json) | Standard stack: W3C DID Core 1.0 (did:key for ephemeral occasions, did:web for durable personas/governance root) + W3C VC 2.0 (validFrom/validUntil, credentialSubject, DataIntegrityProof/eddsa-jcs-2022) + W3C Bitstring Status List v1.0 (Bit |
| [`capability-token.schema.json`](capability-token.schema.json) | Standard: JSON Schema draft 2020-12, modeled on Eclipse Biscuit token semantics (an issuer-signed `authority_block` plus an ordered, holder-appendable `attenuation_blocks[]` chain of Datalog-style `caveats`) with a SPIFFE/SVID sender-constr |
| [`audit-entry.schema.json`](audit-entry.schema.json) | Standard: the bundle realizes doc-04 §4.2 AuditRecord + Checkpoint over the C2SP tlog-tiles / Static-CT leaf-and-checkpoint format with C2SP signed-note checkpoints (origin / tree_size / base64(root_hash) note body) and an optional Sigstore |
| [`federation-handshake.schema.json`](federation-handshake.schema.json) | Standard & addressing: JSON Schema draft 2020-12. Every object is canonicalized with RFC 8785 JCS, content-addressed as CIDv1 = multibase(multicodec, multihash(SHA-256, JCS_bytes)), and signed with DETACHED JOSE/JWS (alt COSE_Sign1) — the d |
| [`policy-decision.schema.json`](policy-decision.schema.json) | Standard & shape: JSON Schema draft 2020-12, modeling the doc-21 wire-contract #6 (policy-decision) as a request/response pair that realizes doc-03's GateRequest/GateVerdict (the Yama floor PDP) and doc-08 §8.2's ControlDecision. It is deny |

_See doc 21 for field-level detail and worked JSON examples. `$id` values are placeholders to be rehomed to a resolvable `epimystic.dev`/`epimystic.com` URL before publication._
