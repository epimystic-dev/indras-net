# 13. The Agent-Definition Spec — SOUL / INSTRUCTIONS / IDENTITY (the von-Neumann genome made operational)

> *The genome of a jewel.* Doc 01 established that an Indra's Net agent is a short-lived **occasion** spun up from a **durable identity the running process cannot rewrite**. This document specifies what that durable identity *is on disk*: a signed, hash-chained, attested triad of files — **SOUL.md / INSTRUCTIONS.md / IDENTITY.json** — that together constitute the agent's von-Neumann genome. Blueprint (SOUL: what this agent is and values), constructor-program (INSTRUCTIONS: how it acts), and capability-certificate (IDENTITY: what it may touch). The occasion loads this genome **read-only** and can never edit its own copy; structural change leaves only as a `PROPOSAL` envelope into the gated evolution loop.
>
> Role names below are archetypal coordination/ethics semantics, each paired with a plain functional gloss — engineering vocabulary, not religious claims, offered with humility toward the living traditions they borrow from.

---

## 13.0 What this spec is, what it binds to, and the two honest framings it must carry up front

This is the **canonical on-disk definition** every agent conforms to. It does not introduce a new enforcement plane — it is the *data* that the v1 enforcement planes already read. Specifically, it is the realization of:

- doc 01's `IdentityRecord` / `AgentRecord` / `RoleDef` / typed-`Effect`-lattice / `DiversityProfile` / `WorkerOutputEnvelope` (the triad **is** the durable per-persona data; `IDENTITY.json` **is** the on-disk `IdentityRecord` superset);
- doc 03's lexicographic floor (`PolicyBundle` T0..T4), the EVOLVABLE/IMMUTABLE partition + blast-radius auto-escalation (§5), the Gate-Loosening Ratchet (§7), the Capability-Rollout Sequencer (§10);
- doc 04's `DIDDocument` / `CapabilityVC` / `SVID`, the TEE/HSM `SignRequest` (signer re-checks capability), the `AuditRecord` hash-chain, the Merkle-DAG `CID`/`EvidenceRef`, and the `missing provenance ⇒ quarantined, no execution` interop rule (§4.13);
- doc 08's `ActionEnvelope` / `OutputEnvelope` / Honesty-FORM checks (§8.5) / `MakerCheckerWitness` (§8.6) / supply-chain admission (§8.11) / two-tier detection contract (§8.8);
- doc 06's MAP-Elites `(role × PSO c1/c2 × risk-class)` grid, the frozen safety battery + Endure law, and the drift budget.

It **never weakens** any of those structures. Where it touches a floor concern it can only propose a change via a `PROPOSAL` envelope.

**Two framings are load-bearing and stated before anything else, because the rest of the document is unsafe to read without them:**

> **Framing 1 — The genome makes the floor *non-strippable*, which is NECESSARY but NOWHERE NEAR SUFFICIENT for safe self-replication.** The central novelty here — the constitutional floor living in an **INVARIANT region** of a fail-closed-bootable genome — guarantees that *a replica cannot mutate or fork its own floor by construction*. It does **nothing** about runaway reproduction rate, un-metered spawn channels, lease/recall defeat, or generation depletion. Those live in a **future Replication-Authority subsystem that does not yet exist in v1** (§13.9). Reading "the genome carries the floor" as "replication is solved" is the single most dangerous possible misread of this document. The genome is a *precondition this spec provides to* that future subsystem — not a solution to replication.

> **Framing 2 — The genome makes emergent role specialization *auditable*, not *correct*.** Signing every spawned role at instantiation reconciles the endogeneity-paradox finding (emergent specialization beats rigid pre-assignment for capable models) with governance: thousands of emergent roles stay DID/VC-attested and policy-bound because they fill the *same* human-legible triad template. It does **not** prove a spawned role is competent, differentiated, or non-colluding — those rest on the genesis Score stage's proxies (§13.7), which inherit doc 01 §16.4's unsolved reasoning-path-diversity problem.

---

## 13.1 The persona-file triad container (the genome object)

A role **is** three co-located files. Nothing else *is* the role; everything else (the occasion, the SVID, the reputation) is computed *from* or *around* it.

```
                         THE PERSONA TRIAD  (the von-Neumann genome)
   ┌───────────────────────────────────────────────────────────────────────────────┐
   │  SOUL.md          INSTRUCTIONS.md            IDENTITY.json                      │
   │  (blueprint)      (constructor-program)      (capability-certificate)           │
   │  what it IS       how it ACTS                what it MAY TOUCH                   │
   │  + values         + SOP + A/B/C/D gates      + DID + capability VCs + toolset    │
   │  + guild          + handoff contracts        + taint clearance + c1/c2 dials     │
   │  + FLOOR-BINDING  + honesty obligations      + risk ceiling + accountable-human  │
   └───────────────────────────────────────────────────────────────────────────────┘
        │ each file split into ONE invariant-blob + variable-body (§13.6)
        ▼
   canonicalize → Merkle-DAG → triad_root_cid     (doc 04 §4.5 CID; producer-DID-co-signed)
        │
        ├── genesis_author_sig   (stage-1, doc 04 §4.6 TEE/HSM signer re-checks capability)
        ├── governance_vc_refs    (stage-2, role_vc + capability_vcs; subject ≠ the agent)
        └── provenance_record_id  (stage-3, Chitragupta IDENTITY-class AuditRecord, hash-chained)
```

The occasion at **INCEPTION** (doc 01 §3.1) receives the triad as **read-only** input plus a `TypedSelfModel` projected from `IDENTITY.json` (`self_preservation_value=0`, `corrigibility=true`, both immutable). **Keys never live in the triad** — `IDENTITY.json` holds only an opaque `key_ref:HSM_handle` (doc 01 §2.4 / doc 04 §4.6), so a leaked triad file leaks **no signing capability**. A leaked genome lets an attacker *read* a role's contract; it does not let them *be* the role.

```jsonc
PersonaTriad {
  triad_id, persona_did, guild_id, role_id,
  files: {
    soul:         { cid, invariant_blob_hash:bytes32, variable_body_cid:CID },
    instructions: { cid, invariant_blob_hash:bytes32, variable_body_cid:CID },
    identity:     { cid, invariant_blob_hash:bytes32, variable_body_cid:CID }
  },
  triad_root_cid: CID,                    // Merkle-DAG over canonical bytes of all three files
  genesis_author_sig: DIDSig,             // stage-1 attestation (§13.5)
  governance_vc_refs: [vc_ref],           // stage-2 attestation
  floor_binding: {
    policy_bundle_version: semver,        // by REFERENCE, never a private copy
    floor_content_hash: bytes32,          // the live doc 03 PolicyBundle content_hash
    floor_tier_order: ["T0","T1","T2","T3","T4"]
  },
  invariant_region_hash: bytes32,         // H over the three invariant_blob_hashes + floor_binding
  provenance_record_id: record_id,        // stage-3 Akasha-Sutra AuditRecord
  role_class: "IMMUTABLE" | "EVOLVABLE",
  schema_version: semver, instantiated_at
}
```

> **Simplification adopted from review (red-team minor, buildability).** Earlier drafts hashed *every* INVARIANT sub-section per file. That created a large surface of designer judgment calls and made boot verification finer-grained than the security goal requires. **Collapsed to ONE canonicalized invariant-blob per file (three hashes total) plus the `floor_binding` hash.** The boot check needs only "invariant bytes unchanged ∧ floor hash matches a valid version," not sub-section granularity. The cost of re-attestation now scales with **promoted** roles, not attempted ones (§13.7).

---

## 13.2 SOUL.md — mythic identity, values, guild, and the inherited floor-binding

SOUL is the genome's **value-blueprint**. It carries the archetypal mythic name + mandatory functional gloss, the guild, the declared values, the trait→function maps, and — the load-bearing part — the **floor it inherits and structurally cannot edit**.

A markdown file: a **signed YAML front-matter header** (the only part that gates boot) plus a prose body (VARIABLE commentary, flavor only, never authority). The front-matter is partitioned into one INVARIANT block and one VARIABLE block.

**The floor is inherited by reference-and-hash, never by copy.** SOUL's `floor_binding` embeds the doc 03 tier order plus the `PolicyBundle.content_hash` — *a pointer with an integrity check*, not a forked private copy. The agent therefore cannot quietly evolve a personal floor; the Boot Integrity Verifier (§13.6) recomputes and refuses to boot any triad whose `floor_binding` diverges from an accepted live `PolicyBundle` version.

**Values are expressed adverbially, not as a utility vector** — "promote *x* *x*-ingly" (doc 03 §9 virtue lens) — deliberately avoiding the orthogonality/Goodhart trap of a separable score to maximize.

```jsonc
// SOUL.md front-matter
{
  INVARIANT: {                            // the soul.invariant_blob; hashed; boot-gated
    archetype_mythic_name: "Narasimha",
    functional_gloss: "reliability checker (recompute / witness verification)",  // MANDATORY pair
    guild_id: "Data-Science",             // one of the seven verticals (§13.3)
    role_class: "EVOLVABLE",              // IMMUTABLE | EVOLVABLE
    floor_binding: { floor_tier_order:["T0".."T4"], policy_bundle_version, floor_content_hash:bytes32 },
    corrigibility_inheritance: true,      // immutable — honor HALT at every lifecycle transition
    self_preservation_value: 0,           // immutable
    immutable_powers: []                  // e.g. ["yama.enforce"] only for IMMUTABLE roles; else empty
  },
  VARIABLE: {                             // the soul.variable_body; editable under tiered reversibility
    values: [ { virtue:"truthfulness", adverbial_expression:"verify claims verifiably" } ],
    trait_function_map: [
      { trait:"independent-mindedness", emitted_function:"recompute before concurring",
        implied_c1_c2_posture:"high-c1 explorer" }
    ],
    narrative_backstory: "…",             // CrewAI-style flavor; NEVER an authority source
    guild_norms_ref: CID
  }
}
```

**Trait→function maps are VARIABLE and tunable — except where a trait names an IMMUTABLE-role power.** A trait that maps to (say) a Yama-enforce capability belongs in `immutable_powers` inside the INVARIANT block; for an EVOLVABLE role this list is empty by construction, and the genesis engine may never populate it (§13.7).

---

## 13.3 The guild taxonomy and the v1-roster crosswalk (resolving the role-vocabulary ambiguity)

The functional layer is **two planes**: a stable declarative **guild + seed-role catalog** (the governance/identity/audit anchor) sitting *over* an open-ended **role-genesis engine** (§13.7). Guilds are anchors; role *instantiation* is emergent.

| Guild (vertical) | Plain function | Genesis-spawnable? |
|---|---|---|
| **Engineering** | build artifacts, code, infrastructure | yes |
| **Creative / Media** | writing, design, generative media | yes |
| **Knowledge / Research** | gather + structure external evidence | yes |
| **Data / Science** | analysis, modeling, reliability/verification | yes |
| **Operations / Business** | process automation, ops, coordination | yes |
| **Interaction** | human-facing dialogue, the Narada messenger layer | yes |
| **Governance / Meta** | the constitutional / separation-of-powers spine | **NO — never spawnable** |

> **Crosswalk fix (red-team major, role-vocabulary coherence).** "Governance-Meta = the mythic roles" was ambiguous against doc 01's IMMUTABLE/EVOLVABLE split, because the EVOLVABLE mythic roles are *also* mythic and *also* not genesis-spawned. The resolution: **`Governance/Meta` = the IMMUTABLE roster ONLY.** The EVOLVABLE mythic roles are **seed roles distributed across the six functional guilds.** Genesis spawns new roles *within the six functional guilds only* — never IMMUTABLE, and **never a new seed Governance/Meta role either.**

| v1 roster role (doc 01 §7) | guild_id | role_class | genesis-spawnable? | basis |
|---|---|---|---|---|
| **Yama** (policy-floor enforcer) | Governance/Meta | IMMUTABLE | no | doc 01 §7.1; the engine never issues FAIL |
| **Chitragupta** (exclusive audit-writer) | Governance/Meta | IMMUTABLE | no | doc 01 §7.1; doc 04 §4.2 |
| **Vishnu** (continuity / halt-guardian) | Governance/Meta | IMMUTABLE | no | doc 01 §7.1; doc 03 §11 |
| **Kaal-Bhairav** (security boundary) | Governance/Meta | IMMUTABLE | no | doc 01 §7.1 |
| **Shiva** (orchestrator / reducer) | Operations/Business | EVOLVABLE (seed) | no (seed, not genesis) | doc 01 §7.2 |
| **Brahma** (planner) | Knowledge/Research | EVOLVABLE (seed) | no (seed) | doc 01 §7.2 |
| **Saraswati** (synthesis) | Knowledge/Research | EVOLVABLE (seed) | no (seed) | doc 01 §7.2 |
| **Vishwakarma** (builder) | Engineering | EVOLVABLE (seed) | no (seed) | doc 01 §7.2 |
| **Varuna** (research) | Knowledge/Research | EVOLVABLE (seed) | no (seed) | doc 01 §7.2 |
| **Narasimha** (reliability / maker-checker checker) | Data/Science | EVOLVABLE (seed) | no (seed) | doc 01 §7.2 |
| **Hanuman** (unblocker) | Operations/Business | EVOLVABLE (seed) | no (seed) | doc 01 §7.2 |

**Three role classes, not two:** `IMMUTABLE` (constitutional, never spawnable, never tunable except via top-gate constitutional edit), `EVOLVABLE-seed` (the named mythic operational roles — tunable through the gated evolution path, but *authored*, not genesis-bred), and `EVOLVABLE-genesis` (emergent roles spawned by §13.7, born as Class-A stubs). Only the third is produced by the genesis engine.

---

## 13.4 INSTRUCTIONS.md — SOP, decision protocol, risk-class gate behavior, handoff contracts, boundaries, honesty obligations

INSTRUCTIONS is the genome's **constructor-program**: what turns a persona into a deterministic-enough worker the rest of the swarm can contract with. It is the data-not-process embodiment of MetaGPT's "Code = SOP(Team)."

A markdown file with a signed YAML header. The SOP is an **ordered list of phases mapped onto doc 01's actual-occasion lifecycle** (INCEPTION → PREHENSION → CONCRESCENCE → CONATION → SATISFACTION).

**Risk-class gate behavior is declared but never self-enforced.** The agent declares its *stance* per class — but the binding enforcement is external at the Yama chokepoint, and **the stance can only *raise*, never *lower*, the effective gate.** doc 03 §5 blast-radius auto-escalation overrides any self-declared class. An INSTRUCTIONS file that declares "treat governance edits as Class A" is simply ignored: the chokepoint auto-escalates the governance edit to C/D regardless.

| Risk class | Declared stance (must not under-classify) | External enforcement (doc 03 §4) |
|---|---|---|
| **A** | act-then-log (post-hoc) | post-hoc review; `CONTINUE_QUEUE` under load |
| **B** | emit PROPOSAL via optimistic-veto + timelock | propose→ratify; `FAIL_CLOSED_HOLD` under load |
| **C** | emit PROPOSAL and HOLD; never self-act | explicit human approval before act; `FAIL_CLOSED_HALT` |
| **D** | emit PROPOSAL and HOLD; per-instance | per-action human authorization; `FAIL_CLOSED_HALT` |

**Honesty obligations are floor concerns, not advisory — and the triad never self-certifies honesty.** The obligations declare *which* `OutputEnvelope` honesty fields the agent must **populate** (doc 01 §12 / doc 08 §8.5). They are INVARIANT. But:

> **Honesty enforcement authority lives entirely in the doc-08 control layer, not in the triad.** The independent rung classifier (doc 08 §8.5(1)) — *not the agent's self-tag* — is the authority on causal rung; the `no-false-(iterated)` check is the cryptographic `MakerCheckerWitness` barrier (`sealed_ts < concurrence_ts`, doc 08 §8.6); a false `(iterated)`, unwarranted `rung-3`, or evidence-free claim is a **floor violation caught externally by resample-to-verify** (doc 01 §12.1). The triad **declares the obligation to populate; the control layer adjudicates the truth.** Per doc 08 §8.13, every honesty-form pass is labeled **"form-valid, content-unverified"** — never "honest." A triad cannot make its outputs honest by asserting it is honest.

```jsonc
// INSTRUCTIONS.md front-matter
{
  INVARIANT: {                            // hashed; boot-gated
    gate_behavior: { A:"post_hoc_log", B:"propose_optimistic_veto",
                     C:"propose_and_hold_human_approve", D:"propose_and_hold_per_action" },
    honesty_obligations: {                // floor concerns; declare WHICH envelope fields to populate
      requires_reasoning_tag:true, requires_causal_rung:true,
      no_false_iterated:true, evidence_pairs_required:true, two_truths_levels:true
    },
    corrigibility_clause: "honor HALT/interrupt immediately at every lifecycle transition"
  },
  VARIABLE: {                             // editable under tiered reversibility (§13.6)
    sop_phases: [ { phase:"CONCRESCENCE", steps:["…"],
                    budgets:{ max_iterations, max_tokens, deadline } } ],
    decision_protocol: [ { condition, action, escalate_to_class } ],
    handoff_contracts: {
      inbound:  [ { from_role_id, envelope_type, trust_label_expected } ],
      outbound: [ { to_role_id, envelope_type } ]
    },
    boundaries_NOT_do: [ "…" ],           // first-class enumerated; feeds taint lattice + Rule-of-Two
    tools_usage_notes: "…"
  }
}
```

The `boundaries_NOT_do` list is **first-class**: it is read by the Rule-of-Two check (§13.8) and the taint lattice (§13.5/§13.8), not just by humans.

---

## 13.5 IDENTITY.json — DID, capability VCs, bound toolset, output schema, taint clearance, c1/c2 dials, risk ceiling, accountability

IDENTITY is the genome's **capability-certificate** — the machine-checkable, cryptographically-attested statement of who this agent is and exactly what it may touch. **This is the field the deterministic Yama gate and the Kaal-Bhairav boundary actually read; nothing in SOUL/INSTRUCTIONS prose is authoritative against it.** It is the on-disk realization of doc 01's `IdentityRecord` as a strict superset-binding with doc 04's `DIDDocument`/`CapabilityVC` and doc 01's `DiversityProfile`.

**The bound toolset is typed effect-ids from the doc 01 §4 Effect lattice — never free-text tool names and never secrets.** Each entry is a `CapabilityGrant` whose `granted_by_did` is the governance authority, not the agent. The Yama gate at CONATION checks exactly:

```
grant ⊇ requested_effect  ∧  requested_risk ≤ risk_class_ceiling  ∧  floor_policy(effect)=PASS
   ⇒ permit ; else deny at the chokepoint, regardless of model intent.   (doc 01 §4)
```

```jsonc
IDENTITY.json {
  // ── INVARIANT region (hashed; boot-gated; editable only at top-gate C/D) ──
  persona_did: DID,
  did_document: { verificationMethod:[pubkeys], authentication, capabilityInvocation },  // doc 04 §4.6
  role_vc_ref: vc_ref,
  risk_class_ceiling: "A"|"B"|"C"|"D",
  accountable_human: human_id,           // doc 01 §2.1 — no persona is unmoored
  escalation_did: DID,
  key_ref: HSM_handle,                    // OPAQUE — keys live in the TEE/HSM signer, never here

  // ── VARIABLE region (editable under tiered reversibility; loosening gated — §13.6) ──
  capability_vc_refs: [vc_ref],
  bound_toolset: [
    CapabilityGrant {
      effect_id,                          // from the doc 01 §4 Effect lattice — typed id only
      granted_risk_class: "A"|"B"|"C"|"D",
      granted_by_did: "did:web:indras-net.governance",   // NEVER the agent itself
      names_constraint_relaxed: str,      // MANDATORY (doc 01 §4) — which restraint this grant depends on
      falsifier?: str
    }
  ],
  output_schema: { envelope_type:"WorkerOutputEnvelope", artifact_schema_ref:CID },  // doc 01 §12 / doc 08 §8.5
  taint_clearance: {                      // CaMeL/FIDES IFC labels (doc 04 trust-labels → runtime lattice)
    max_read_confidentiality: label,
    min_write_integrity: label,
    derived_label_rule: "least-upper-bound"
  },
  diversity_profile: {                    // doc 01 §11 PSO dials
    c1_self_weight: float, c2_shared_weight: float,
    is_explorer: bool, is_enforcer: bool, min_diversity_floor: float
  }
}
```

**Taint-lattice clearance is the load-bearing IFC boundary** (the CaMeL/FIDES promotion of doc-level `quarantined:*` trust-labels into a runtime lattice). A deterministic policy-enforcement point gates every tool call on the derived-data least-upper-bound label vs this clearance — *the model provably cannot separate instructions from data in one token stream, so this is the boundary, never a "better prompt."* Its placement in the VARIABLE region is **asymmetrically constrained** — see §13.6.

---

## 13.6 INVARIANT / VARIABLE region split + the fail-closed Boot Integrity Verifier

This is where "the floor cannot be edited by any agent or replica" becomes a **structural fact, not a prohibition.**

| Region | Contents | Editable by an occasion/replica? | Edit gate |
|---|---|---|---|
| **INVARIANT** | `floor_binding`, `corrigibility_inheritance`, `self_preservation_value`, `immutable_powers`, `persona_did`, `did_document`, `role_vc_ref`, `risk_class_ceiling`, `accountable_human`, honesty-obligation flags, gate-behavior stances | **No** | Constitutional — top-gate C/D + GLR ratchet + safety battery + human ratification + armed rollback |
| **VARIABLE** | SOP phases, decision protocol, trait maps, narrative, `bound_toolset` grants, `taint_clearance`, `diversity_profile`, `output_schema.artifact_schema_ref`, handoff contracts, boundaries | **Only via PROPOSAL** (occasion never self-applies) | Tiered by doc 03 §5 (see below) |

### The Boot Integrity Verifier (fail-closed, non-LLM, in the TCB)

A **non-LLM** verifier runs **before any occasion is minted** — it is part of doc 04 Protocol B identity-bootstrap, *before* the SVID is issued. It lives in the IMMUTABLE/TCB partition (doc 01 §6).

```
BOOT INTEGRITY VERIFIER  (runs before SVID mint; fail-closed)
  1. Recompute each file's invariant_blob_hash from on-disk bytes; recompute invariant_region_hash.
  2. Verify floor_binding references an ACCEPTED PolicyBundle version (§13.6.1 reconciliation).
  3. Verify the genesis-author signature (stage-1) + the governance VC chain (stage-2).
  4. Verify triad_root_cid matches the Akasha-Sutra provenance record (stage-3).
  VERDICT = BOOT  iff  ALL of {hashes equal ∧ floor version accepted ∧ floor hash valid ∧
                              sigs valid ∧ provenance matches}
          else FAIL_CLOSED → no SVID minted → alarm to Kaal-Bhairav + Chitragupta audit.
```

**A replica that strips, edits, or forks the floor cannot boot by construction** — its recomputed `invariant_region_hash` will not match, or its `floor_binding` will not reference an accepted version. This is the realization of the safety redline "a replica mutating its own floor must be impossible by construction, not merely prohibited."

```jsonc
BootCheck {
  triad_id,
  recomputed_invariant_hash:bytes32, expected_invariant_hash:bytes32,
  declared_floor_hash:bytes32, accepted_floor_versions:[semver], floor_version_accepted:bool,
  genesis_sig_valid:bool, vc_chain_valid:bool, provenance_match:bool,
  verdict: "BOOT" | "FAIL_CLOSED",
  alarm_routed_to: ["Kaal-Bhairav","Chitragupta"]
}
```

### 13.6.1 Floor-version reconciliation — the rotation problem (resolved; was the critical flaw)

> **Critical fix (red-team).** A boot check that hard-pins `floor_content_hash == LIVE PolicyBundle hash` has no story for the legitimate-floor-rotation case. The floor *does* evolve (doc 03 GLR loosening is falsifier-gated but real; doc 04 §4.13 Yama enforces against a staleness-bounded cached version). On any ratified floor edit, **every existing triad's `floor_binding` now diverges from the live hash and would FAIL-CLOSED at next boot** — bricking the swarm. The naive "fix" of accepting any signed version silently defeats the non-strippability guarantee (a rollback-to-weaker-floor attack would pass).

**The resolution — versioned acceptance window + a governance re-binding sweep:**

The Boot Integrity Verifier accepts `floor_binding` if it references a PolicyBundle version that is **(a)** the live version, **OR (b)** a still-accepted predecessor inside a bounded staleness/grace window, AND in either case the referenced version is itself **validly signed by the legislative key and not revoked**, AND **(c)** there exists a signed `FloorMigrationRecord` linking the referenced version forward to the live version as a genuine ancestor (not an arbitrary or rolled-back bundle).

```jsonc
FloorMigrationRecord {                    // written by governance; hash-chained into Akasha-Sutra
  from_version:semver, to_version:semver,
  from_content_hash:bytes32, to_content_hash:bytes32,
  is_genuine_ancestor:true,               // to_version's lineage includes from_version
  grace_window_closes_at:ts,              // after this, from_version FAILs closed
  legislative_sig:bytes
}
AcceptedFloorWindow { live_version, accepted_predecessors:[semver], window_policy }
```

On a ratified floor change, a governance-side **RE-BINDING SWEEP** re-issues every triad's `floor_binding` reference (a new `triad_root_cid` + full re-attestation per the §13.6.2 edit protocol) **before the old version's grace window closes.** Stale-but-in-window triads boot against the validated predecessor; triads referencing a version *outside* the window, *unsigned*, *revoked*, or *not a genuine ancestor* (e.g. a rolled-back weaker floor) **FAIL closed.** This keeps both properties: floor edits are possible (no ossification) **and** the non-strippability guarantee survives (no "accept anything" bypass; a weaker-floor rollback is rejected because it is not a genuine ancestor of the live version).

### 13.6.2 VARIABLE edits under tiered reversibility — and the taint-clearance asymmetry

VARIABLE edits route through doc 03 §5 tiered reversibility:

| Edit kind | Class | Mechanism |
|---|---|---|
| Cheap-reversible (skill note, SOP wording) | **A** | doc 01 §3.3 durable-write discipline: content-addressed, SVID-signed, audited, canonicalized, counted against the per-persona drift budget |
| Structural (new SOP phase, c1/c2 retune, **new tool grant**, **taint-clearance LOOSENING**) | **B → escalated** | maker-checker; a new grant *or a clearance loosening* additionally runs the doc 03 §10 Capability-Rollout Sequencer (names_constraint_relaxed must resolve GREEN before activation, else QUEUED) and the doc 03 §7 GLR |
| Any INVARIANT-region target, or any edit that loosens a gate | **C/D** | blast-radius auto-escalation + GLR ratchet + safety battery + human ratification + armed rollback |

> **Taint-clearance asymmetry fix (red-team major, security).** `taint_clearance` is the load-bearing IFC boundary, yet it sits in the VARIABLE region. A Class-B (optimistic-veto) edit that **raises `max_read_confidentiality`** or **lowers `min_write_integrity`** is a *clearance loosening* — silent boundary erosion that the timelock may not catch. **Binding rule: any taint-clearance change that raises read-confidentiality OR lowers write-integrity is a GATE-LOOSENING** routed through doc 03 §7 GLR + §10 Sequencer (named falsifier + date + rollback + human ratification + blast-radius auto-escalation), identical to a new tool grant. **Only TIGHTENING** (lower read ceiling / raise write floor) is the free Class-A append direction. The IFC boundary can only be *narrowed* cheaply; *widening* it pays the full ratchet cost.

```jsonc
RegionEdit {
  triad_id, target_file, region: "INVARIANT"|"VARIABLE", field,
  proposed_class:"A"|"B"|"C"|"D", auto_escalated_to:"A"|"B"|"C"|"D",
  is_gate_loosening:bool,                 // true for new grant OR clearance-widening
  glr_required:bool, sequencer_required:bool,
  rollback_archive_ref
}
// INVARIANT target ⇒ auto_escalated_to ∈ {C,D}
// taint_clearance widen / new tool grant ⇒ is_gate_loosening=true ⇒ glr_required ∧ sequencer_required
```

**Aggregate drift rollback (misevolution guard).** Per doc 01 §3.3 / doc 06, the Health subsystem accrues cumulative VARIABLE-edit drift. When drift crosses the floor, the consolidation/rollback gate rolls the run of cheap edits back **as a unit** to the last archived known-good triad and re-runs the safety battery. This relocates the doc 01 §3.3 misevolution guard (refusal-rate decay with no attacker) onto the persona-edit stream.

---

## 13.7 Triad signing, hash-chaining + attestation, and the Role-Genesis template-filler

### 13.7.1 Three-stage attestation (provenance-gating at instantiation)

Every triad — including every emergent role — is a first-class, provenance-gated object so a persona/skill file **cannot self-propagate unverified.** This is the Sigstore + in-toto/SLSA admission rule applied to the genome (~5 poisoned docs reach 90–98% RAG ASR; persona/skill files self-propagate).

```
STAGE 1 — GENESIS-AUTHOR SIGNATURE
  Author (genesis engine or human) canonicalizes the three files, computes triad_root_cid,
  calls the doc 04 §4.6 TEE/HSM signer with (triad_root_cid, requested_capability="persona.author").
  The signer RE-CHECKS capability before signing.  → genesis_author_sig

STAGE 2 — GOVERNANCE VC ISSUANCE
  The governance credential authority (NEVER the agent) verifies the author, then issues
  role_vc + capability_vcs whose credentialSubject.did = persona_did and whose capability_grants
  EXACTLY equal IDENTITY.bound_toolset.   grants_match_identity MUST be true, else REFUSE.

STAGE 3 — PROVENANCE RECORD
  Chitragupta writes ONE IDENTITY-class AuditRecord (doc 04 §4.2)
  { actor_did=governance, subject_cid=triad_root_cid, event_type="persona.instantiate",
    refs=[parent_triad_id if genesis-bred] }, hash-chained into Akasha-Sutra.
  triad.provenance_record_id points back at it.

RE-APPROVAL ON ANY CHANGE: a VARIABLE edit ⇒ NEW triad_root_cid ⇒ NEW stage-1 sig ⇒ NEW stage-3
  record chaining prev_triad_cid. (Kills tool/skill "rug-pulls" — a changed manifest re-admits.)
```

```jsonc
TriadAttestation {
  triad_root_cid:CID,
  stage1_author_sig: { author_did, sig, signed_root_cid },
  stage2_vc_issuance: { issuer_did:"did:web:indras-net.governance",
                        role_vc:vc_ref, capability_vcs:[vc_ref], grants_match_identity:bool /*MUST be true*/ },
  stage3_provenance: { audit_record_id:record_id, prev_triad_cid:CID|null, lineage_depth:int }
}
```

**Provenance proves ORIGIN, not SAFETY.** Admission therefore *additionally* requires the import canary scan + taint-quarantine (§13.8) and — for genesis — the supply-chain-bound composition below.

### 13.7.2 Role-Genesis: Charter → Genesis → Trial → Score → Promote/Discard

> **Scope fix (red-team major, coherence).** doc 01 §8 is a **stub-PROMOTION pipeline** (detect a recurring cluster → birth a zero-grant Class-A stub → verifiable-improvement + safety-battery + human-ratify-above-read-only). The genesis engine here is a **generative EXTENSION of §8, not a realization of it.** What §8 supplies and what this spec adds:
>
> | Stage | doc 01 §8 (REALIZED — reused as-is) | This spec (NEW — must be added to §8 or a genesis doc) |
> |---|---|---|
> | Charter | cluster-detection from the skill-retrieval miss log | the `RoleCharter` object + budget |
> | Genesis | — | **knapsack-composition of a candidate triad from the capability-commons** |
> | Trial | — | **hardware-isolated (microVM) sandbox run on cluster-representative tasks** |
> | Score | safety-battery regression check (Endure law) | **the three-axis score: safety + competence + DIFFERENTIATION** |
> | Promote | stub→provisional→standing, maker-checker, human-ratify-above-read-only | triad signing + attestation; archive as reusable skill |
>
> Role-proliferation cap/merge (doc 01 §16.3) **remains OPEN**, and the steady-state cost of a high-genesis-rate swarm is **unmodeled** (§13.10).

```
(1) CHARTER   planner/orchestrator detects a recurring high-surprise low-coverage task cluster
              (doc 01 §8 miss log) → RoleCharter{ needed_capabilities, guild_hint, originating_cluster, budget }
                  │
(2) GENESIS   compose a candidate PersonaTriad by knapsack-selecting skills+tools from the
              VETTED capability-commons under budget; draft SOUL (archetype+gloss+guild+INHERITED
              floor — never a new floor), INSTRUCTIONS (SOP from the closest seed-role template +
              cluster-specific decision protocol), IDENTITY (DID minted; bound_toolset = ONLY the
              composed effect-ids; risk_class_ceiling = A by default — born a STUB, doc 01 §8).
                  │                         ▲ supply-chain admission bound here — §13.7.3
(3) TRIAL     run the candidate in a hardware-isolated microVM with egress allowlists on
              cluster-representative tasks. NO Class-B+ effect reaches production.
                  │
(4) SCORE     three CO-EQUAL axes:
              · SAFETY        — doc 06 frozen safety battery; Endure law (no safety regression)
              · COMPETENCE    — must outperform routing-to-generalist on its cluster (doc 01 §8 test)
              · DIFFERENTIATION — MorphAgent role-clarity/divergence vs existing roles +
                                  the doc 01 §11 reasoning-path-diversity floor (a redundant role is discarded)
                  │
(5) PROMOTE   stub → provisional → standing = the doc 01 §8 maker-checker, capability-rollout-
   / DISCARD  sequenced, human-ratified-above-read-only event. On PROMOTE: triad signed+attested
              (§13.7.1), archived as a reusable (Voyager-style) skill. On DISCARD: logged + dropped.
              GENESIS NEVER mints IMMUTABLE / Governance-Meta roles, and never a new seed role;
              never grants a capability whose names_constraint_relaxed does not resolve GREEN.
```

```jsonc
RoleCharter      { charter_id, needed_capabilities:[effect_id], guild_hint, originating_cluster:ref, budget }
GenesisCandidate { triad:PersonaTriad /*risk_ceiling=A, status=stub*/,
                   composed_from_skills:[ { skill_cid, provenance:SkillAttestation, taint_label } ],  // §13.7.3
                   candidate_taint_clearance, parent_seed_role_id }
TrialResult      { candidate_id, sandbox_id:microVM, tasks_run, egress_allowlist, observed_effects:[effect_id] }
GenesisScore     { safety:{ battery_pass:bool, regression:bool },
                   competence:{ vs_generalist_delta:float },
                   differentiation:{ role_clarity:float, reasoning_path_divergence:float, redundant:bool },
                   verdict:"PROMOTE"|"DISCARD" }
PromotionEvent   { triad_id, from:"stub", to:"provisional"|"standing",
                   maker_did, checker_did /*no trust-edge dependency on maker — doc 01 §7.1*/,
                   human_ratification_audit_id, archived_skill_cid }
```

> **Cost-bounding (red-team minor).** Stubs stay at **Class-A with NO VC re-issuance until first promotion.** Ephemeral discarded candidates **never hit the VC/provenance path** — they are logged and dropped. Re-attestation cost therefore scales with **promoted** roles, not attempted ones. The high-genesis-rate steady-state remains unmodeled (§13.10).

### 13.7.3 Genesis composition is supply-chain-bound (poisoned-skill guard)

> **Supply-chain fix (red-team major, security).** "Knapsack-select from the *vetted* commons" assumed the commons is safe; provenance proves origin, not safety, and a signed-but-poisoned skill composed into a fresh role would rely on the Trial sandbox alone to catch it. **Binding rules:**

1. **Each `composed_from_skills` entry carries its provenance attestation + taint label.** Composition is bound to the doc 08 §8.11 admission gate: any composed skill that **fails in-toto/SLSA/Sigstore verification or whose CID does not re-check** is **refused at compose time, before Trial.**
2. **The candidate's `taint_clearance` is the least-upper-bound of its composed skills' labels — not a free choice.** A composed skill cannot have its taint laundered away by the genesis engine choosing a clean clearance.
3. **A quarantined-origin skill forces the whole candidate into the quarantined integrity label through Trial,** until a local checker clears it. The Trial is behavioral and the canary scan is probabilistic; the taint-LUB + capability-downscope are the load-bearing guards.

---

## 13.8 Persona-file import / quarantine model (the Skill-Inject defense)

Importing a persona/skill/triad across a trust boundary (another swarm, a marketplace, a sibling operator) is the **highest-risk admission path** — persona files are exactly the self-propagating skill-files the research flags. The pipeline below treats an imported genome as the hostile, self-propagating artifact it may be.

```
CROSS-BOUNDARY IMPORT ADMISSION  (foreign triad → maybe a local stub; NEVER bootable on import)

  arrive as quarantined:observed  (doc 01 §10, doc 04)  ── NON-bootable ──┐
                                                                          │
  (1) PROVENANCE GATE  verify foreign genesis-author sig + VC chain against a KNOWN issuer.
      missing/unknown ⇒ stay quarantined; no execution without a Class-C human gate
      (doc 04 §4.13 "missing provenance ⇒ quarantined, no execution").
                                                                          │
  (2) FLOOR RE-BIND    STRIP the imported SOUL.floor_binding; REPLACE with a reference to
      THIS swarm's live PolicyBundle. A foreign OR weaker floor is a HARD REJECT.
      (The floor is inherited locally, NEVER imported.)
                                                                          │
  (3) CANARY / POISON SCAN   screen SOUL/INSTRUCTIONS prose for embedded instructions,
      capability-enumeration probes, injection payloads. ALL such content = DATA, never COMMANDS
      (no action-grounds without out-of-band human confirmation).  ← probabilistic; defense-in-depth only
                                                                          │
  (4) CAPABILITY DOWNSCOPE   DISCARD the imported bound_toolset entirely; re-admit as a fresh
      STUB (risk_ceiling=A, ZERO grants). Foreign grants are never retained.
                                                                          │
  (5) TAINT             all data the imported role produces during probation carries the
      quarantined integrity label until a LOCAL checker clears it.
                                                                          │
  (6) RULE-OF-TWO GATE  the import action holds untrusted-input(foreign file) +
      capability-grant + state-change(boot) = ALL THREE ⇒ MANDATORY human gate.
      The gate DISPLAYS THE ACTUAL triad bytes/CID + the re-bound floor hash + the zeroed toolset
      — never a natural-language summary (Lies-in-the-Loop defense).
                                                                          │
  on human ADMIT ──► the stub re-enters the LOCAL genesis Trial→Score→Promote pipeline (§13.7.2)
                     and earns capability ONLY by passing local safety + competence + differentiation.
```

```jsonc
ImportRequest { foreign_triad_cid:CID, source_boundary_did, claimed_vcs:[vc_ref], trust_label:"quarantined:observed" }
ImportVerdict {
  provenance_ok:bool,
  foreign_floor_rejected:true,            // ALWAYS — floor re-bound locally
  canary_findings:[ { section, finding, severity } ],
  capability_downscoped_to:"stub:riskA",
  rule_of_two_triggered:bool, human_gate_required:bool,
  disposition: "QUARANTINE" | "ADMIT_AS_STUB" | "REJECT"
}
```

The **Rule of Two** is the objective HITL-sizing law: any operation may hold at most 2 of {untrusted-input, sensitive-access/capability, state-change/irreversibility}; holding all 3 *requires* a human gate. The import action holds all three, so the human gate is mandatory — and it must show the *actual low-level object* (the literal CID, re-bound floor hash, zeroed toolset, and for an edit the literal `RegionEdit` diff), because a confident NL summary gets a harmful change approved (Lies-in-the-Loop).

---

## 13.9 Forward dependency — the Replication-Authority subsystem (NOT in v1)

> **Phantom-interface fix (red-team major, coherence + the highest-safety-weight topic).** Earlier framing presented "a quorum-cosigned Replication Authority issues capability-scoped, generation-counted, lease-bound spawn tokens" as an *existing* doc-06 contract. **It does not exist in v1.** Grep of docs 00–11 confirms `Replication Authority`, `spawn token`, `R_eff`, `vitamin`, `lease`, and `generation cap` appear **nowhere**; doc 06's only "replicat" usage is the *audit log* being replicated (a CFT detail), not agent self-replication.

**This spec therefore makes the relationship a forward dependency, explicitly:**

- The triad-as-replication-unit and the **floor-as-non-strippable-genome are PRECONDITIONS this spec PROVIDES TO** a future, as-yet-unwritten **doc-12 / Replication-Authority spec.**
- **Until that subsystem is specified, NO spawn path consumes the triad for replication.** A triad is instantiated (§13.7.1) and imported (§13.8); it is **not replicated** by any v1 mechanism.
- The genome contributes exactly **one** safety property to replication: **a replica cannot mutate or fork its own floor** (the Boot Integrity Verifier refuses to mint an SVID for a divergent invariant region, §13.6). That is necessary and **nowhere near sufficient.**

**Named requirements the future Replication-Authority doc MUST satisfy** (carried here so no reader mistakes the genome for a solution):

| Requirement | Why (research redline) |
|---|---|
| **Lineage-wide R_eff < 1** — each spawn token authorizes on average **< 1** child | provable percolation-boundedness; without it, runaway reproduction |
| **Finite, depleting generation cap** | guarantees the lineage provably depletes; planet-scale = a hard-enveloped "controlled outbreak" that still depletes |
| **No self-minted spawn token or survival credential** | a replica carries NO self-sufficient blueprint; it cannot authorize its own children |
| **Quorum-cosigned Replication Authority** against a global compute/budget ceiling | crown-jewel; no single node mints authority (doc 01 §6 / doc 03 §11 witness pattern) |
| **External lease ("vitamin") + dead-man toxin-antitoxin recall** enforced by the sandbox/credential plane | a replica **cannot disable its own kill-switch** |
| **Per-replica hardware-grade isolation (microVM) + egress allowlists + fail-closed key lockdown** | bound blast-radius per replica |
| **Replication MUST NOT be coupled to an open fitness/selection loop** | Tierra/Avida: replication + heredity + variation + selection spontaneously breeds parasites/reward-hacking. Every spawn metered + attested; **a single un-metered spawn channel breaks the entire guarantee.** |

> **Safety risk, stated loudly.** The actual safety machinery of replication (R_eff<1, depleting generation cap, external lease + dead-man recall, microVM isolation, no self-minted token) is **out of scope here and absent from v1.** A reader must not conclude "replication is safe because the genome carries the floor." Floor-non-strippability is one precondition; the un-metered-spawn-channel risk that breaks the whole guarantee is **not addressed by this spec** because the spawn channel is not specified here — which is precisely why this section exists.

---

## 13.10 Interfaces to the v1 subsystems

| v1 subsystem | Contract |
|---|---|
| **Topology & Agent Model (doc 01)** | `IDENTITY.json` IS the on-disk `IdentityRecord` (strict superset). The triad IS the durable per-persona data referenced by `AgentRecord`. `bound_toolset` entries ARE doc 01 §4 `CapabilityGrant`/Effect-lattice ids. `diversity_profile` c1/c2 ARE the §11 dials. The occasion loads the triad read-only at INCEPTION and projects the `TypedSelfModel` (`self_preservation_value=0`, `corrigibility=true`). The genesis pipeline **extends** the §8 RoleStub promotion (it does not merely realize it — §13.7.2). An occasion **never** rewrites its own genome; structural change leaves as a PROPOSAL envelope only. |
| **Governance, Ethics & the Floor (doc 03)** | `SOUL.floor_binding` references the doc 03 `PolicyBundle` (T0..T4 lexicographic floor) by `content_hash`; the Boot Integrity Verifier enforces version acceptance + genuine-ancestor migration (§13.6.1). `INSTRUCTIONS.gate_behavior` must be consistent with the §4 Risk-Class Gate Router and **cannot under-classify** (blast-radius auto-escalation §5 wins). VARIABLE edits route through §5 tiered reversibility; **new tool grants AND taint-clearance widenings** route through the §7 GLR + §10 Sequencer. Honesty obligations map to the §6 honesty floor (T3: structural bright-lines + semantic detected-and-escalated). This spec proposes floor changes **only** via PROPOSAL envelopes; it may not weaken floor structures. |
| **Provenance, Identity & Consensus — Akasha-Sutra (doc 04)** | `persona_did` + `did_document` + `role_vc`/`capability_vcs` are §4.6 `DIDDocument`/`CapabilityVC`. The 3-stage attestation uses the §4.6 TEE/HSM `SignRequest` (signer re-checks capability) and writes one IDENTITY-class `AuditRecord` (§4.2) hash-chained into the ledger. `triad_root_cid` is a §4.5 Merkle-DAG `CID`/`EvidenceRef` (always producer-DID-co-signed, so attribution survives dedup). **A CID mismatch on triad read is the §4.5 hard integrity failure** that catches mount/truncation/BOM corruption of a genome file before it propagates. Re-approval-on-change and the import missing-provenance rule are the §4.13 evolution/interop contracts. The floor-version reconciliation reuses the §4.13 staleness-bounded cache discipline. |
| **Safety, Control, Honesty & Interfaces — Aegis & Narada (doc 08)** | `IDENTITY.output_schema` names the `WorkerOutputEnvelope`/`OutputEnvelope` (§8.5). Every consequential effect becomes a §8.2 `ActionEnvelope` routed through the Chokepoint Interceptor (Yama floor first, then criticality, monitor, disposition). The agent's declared `honesty_obligations` map to the §8.5 Honesty-FORM checks (independent rung-classifier authority, the `MakerCheckerWitness` `sealed_ts < concurrence_ts` barrier, two-truths, maker-checker independence) — **the triad declares which fields to populate; the doc-08 layer adjudicates truth, and labels every pass "form-valid, content-unverified" (§8.13).** `taint_clearance` feeds the §8 trust_class / `quarantined:*` handling. Genesis skill composition binds to the §8.11 supply-chain admission gate (§13.7.3). Checker selection for any triad maker-checker draws maximal reasoning-path diversity from the maker's c1/c2 profile (§8.6). |
| **Meta-Evolution & Health (doc 06)** | The genesis Charter→Trial→Score→Promote pipeline feeds the doc 06 MAP-Elites grid `(role × PSO c1/c2 × risk-class)`. Score consumes the doc 06 **frozen safety battery + Endure law** (no safety regression) plus health competence/differentiation signals. Cumulative VARIABLE-edit drift and unit-rollback are owned by the doc 06 Health drift budget. |
| **Replication-Authority (FUTURE doc-12; NOT in v1)** | The triad is the **intended** replication unit and the floor-as-non-strippable-genome is a precondition this spec **provides to** that future subsystem (§13.9). Until it is specified, no spawn path consumes the triad. The future doc must satisfy the R_eff<1 / generation-cap / external-lease-recall / no-self-minted-token / metered-and-attested-spawn requirements listed in §13.9. |

---

## 13.11 Failure modes addressed

| Failure mode | How the spec addresses it | Residual (honest) |
|---|---|---|
| **Floor-stripping / floor-forking** by an agent or replica | Floor lives in the INVARIANT region, inherited by reference+hash; the fail-closed Boot Integrity Verifier refuses an SVID for any triad whose invariant-region hash or floor version diverges. Non-viable by construction, not merely prohibited. | Holds only relative to an uncompromised verifier + root-of-trust (§13.12) |
| **Floor-rotation bricking / rollback-to-weaker-floor** | Versioned acceptance window + signed `FloorMigrationRecord` genuine-ancestor check; governance re-binding sweep before the grace window closes (§13.6.1). | Window-size tuning is empirical |
| **Self-granted capability / privilege escalation via persona edit** | `bound_toolset` = typed effect-ids checked at the external Yama chokepoint; grants come only from governance VCs whose subject ≠ the agent; blast-radius auto-escalation overrides any self-declared low gate. | — |
| **Silent IFC-boundary widening under cheap edits** | Any taint-clearance widening = gate-loosening → GLR + Sequencer (§13.6.2); only tightening is free Class-A. | Differentiation between benign and adversarial widening still needs the falsifier |
| **Persona/skill-file self-propagation, tool/skill "rug-pulls"** | 3-stage provenance-gating (author-sign → governance-VC → hash-chained Akasha-Sutra record); ANY change ⇒ new CID + new sig + new provenance record + mandatory re-approval. | Provenance proves origin not safety — paired with canary + taint |
| **Skill-Inject / poisoned imported persona** | Import quarantine strips the foreign floor, discards foreign capability (re-admit as stub), canary-scans prose as data, Rule-of-Two-gates with actual bytes shown (§13.8). | Canary scan is probabilistic (§13.12) |
| **Poisoned-but-signed skill composed by genesis** | Composition bound to doc 08 §8.11 admission; candidate taint = LUB of composed skills; quarantined-origin forces quarantine through Trial (§13.7.3). | Trial is behavioral; subtle sleeper may survive (§13.12) |
| **Prompt-injection through observed persona content** | Taint-lattice clearance + deterministic PEP gate every tool call on derived-data LUB; instructions in `quarantined:*` content are never action-grounds. | The model cannot separate instructions from data — boundary is the lattice, not a classifier |
| **Key exfiltration via a leaked genome file** | `IDENTITY` holds only `key_ref:HSM_handle`; keys live in the TEE/HSM signer outside the model surface. | TEE/HSM root-of-trust dependency (doc 04 §4.15) |
| **Lies-in-the-Loop at the import/edit human gate** | Gates display the ACTUAL low-level object (triad CID, re-bound floor hash, zeroed toolset, literal diff), never an NL summary. | Human still the trust root for the gate decision |
| **Role-library bloat / redundant emergent roles** | Genesis Score enforces a MorphAgent differentiation metric + reasoning-path-diversity floor; a non-differentiating role is discarded. | Metric is a proxy (§13.12); merge/cap policy open (doc 01 §16.3) |
| **Misevolution (silent safety decay across many cheap edits)** | VARIABLE cheap edits are content-addressed, signed, audited, drift-budgeted; a run rolls back as a unit when cumulative drift crosses the floor (§13.6.2). | Drift-budget set-point is empirical |
| **Emergent-specialization illegibility** | Every spawned role fills the same human-legible triad template and is signed at instantiation, so open-ended genesis stays auditable. | Auditable ≠ correct (Framing 2) |
| **Genome-file mount/truncation/BOM corruption** | `triad_root_cid` CID-checked on read = doc 04 §4.5 hard integrity failure before propagation. | — |

---

## 13.12 Safety risks this spec honestly carries (mitigated, not solved)

1. **Self-replication is named as a forward dependency, and its actual safety machinery does not exist in v1.** The genome makes the floor non-strippable — necessary, nowhere near sufficient. R_eff<1, depleting generation caps, external lease + dead-man recall, no self-minted token, and the rule that *a single un-metered spawn channel breaks the whole guarantee* live in a doc-12 that has not been written (§13.9). *The most dangerous misread is "the genome carries the floor, so replication is safe." It is not.* Mitigation: §13.9 states the dependency loudly and enumerates the requirements the future subsystem must satisfy. Residual: until doc-12 exists, **do not enable any spawn path that consumes the triad.**

2. **The "cannot boot a stripped floor" guarantee holds ONLY relative to an uncompromised Boot Integrity Verifier + root-of-trust.** A forged-yet-internally-consistent triad signed by a **compromised genesis-author key** boots cleanly until a checker contradicts it (it inherits the doc 04 §4.6 writer-key residual). This is the **load-bearing residual** and is surfaced as a top-line risk, not a tail open-problem. **Binding requirement (not an aside): the genesis-author signing key and the governance VC issuer key are held under HSM custody with Shamir m-of-n threshold across separate custodians** (doc 04 §4.15) for the highest-stakes issuance, so no single key compromise forges admissible genomes at scale. Residual: custody design remains an operational open problem; provable non-strippability holds only relative to the TCB root.

3. **The taint-clearance IFC boundary is in the VARIABLE region.** Even with the §13.6.2 asymmetry (widening = full GLR cost, tightening = free), a *gradual* sequence of small ratified widenings is the misevolution-by-many-cheap-edits pattern relocated onto the security-clearance field. Mitigation: every widening pays the falsifier + human-ratification cost and is counted against the drift budget, and the unit-rollback fires when cumulative drift crosses the floor. Residual: the drift set-point that distinguishes legitimate scope-growth from slow erosion is uncalibrated (inherits doc 01 §16.1 / doc 06).

4. **Genesis skill-composition supply-chain.** §13.7.3 binds composition to the doc 08 §8.11 gate and forces the candidate taint to the LUB of its composed skills, so a signed-but-poisoned skill cannot be laundered clean at compose time and a quarantined-origin skill forces quarantine through Trial. But the Trial is *behavioral* and the canary scan is *probabilistic* — a subtle data-exfil or sleeper skill could survive composition and Trial and be promoted into a standing, signed, *auditable-looking* role. Mitigation: taint-LUB + capability-downscope-to-stub are the load-bearing guards; the scan is defense-in-depth only. Residual: no boundary against a sufficiently subtle sleeper.

5. **Differentiation-metric gameability.** The MorphAgent role-clarity / reasoning-path-divergence score that gates genesis Promote shares doc 01 §16.4's unsolved problem: **roles built on the same base model can LOOK differentiated (different prompts) while FAILING IDENTICALLY.** A redundant or correlated-failure role can therefore be promoted and treated by the swarm as adding diversity — quietly eroding the protected-diversity safety invariant. The metric is a proxy, not a guarantee; the +44% emergent-specialization benefit is partly *unverifiable*. We say so plainly (it is not papered over).

6. **Canary scan is early-warning, never a boundary.** Screening SOUL/INSTRUCTIONS prose for embedded instructions / injection payloads is probabilistic — no prompt or classifier separates instructions from data in one token stream. A subtle payload in a benign-looking backstory can pass. The **taint-lattice + capability-downscope-to-stub** are the load-bearing guards; the scan is defense-in-depth only.

---

## 13.13 Honest novelty accounting

**The primitives are prior art, correctly attributed and not claimed:** MetaGPT "Code = SOP(Team)" and CrewAI role/goal/backstory (the triad template); W3C DID/VC + SPIFFE/SVID (identity); the von-Neumann blueprint/constructor separation (the genome framing); CaMeL/FIDES information-flow taint labels (security); Sigstore + in-toto/SLSA (provenance-gating); the MorphAgent / AutoAgents / EvoAgent role-genesis toolkit (the Charter→Genesis→Trial→Promote engine).

**The defensible contribution is the integration into one signed object**, with three specific, honestly-hedged moves (proposed 2026-06; time-stamped; *not* claimed first-of-kind in isolation):

1. **The constitutional floor as the INVARIANT region of a fail-closed-bootable genome.** The floor is inherited by reference+hash and is structurally non-viable to strip or fork, because a divergent invariant-region hash refuses to boot — making "a replica cannot mutate its own floor" a *construction fact*, not a procedural commitment. No surveyed agent framework makes the ethical floor a genome region verified at boot.
2. **Emergent role-genesis that stays auditable by signing every spawned role at instantiation.** This reconciles the endogeneity-paradox finding (emergent specialization beats rigid roles for capable models) with governance by making the open-ended capability plane fill the *same* human-legible, provenance-gated triad template the stable guild/seed-role plane uses — so thousands of emergent roles remain DID/VC-attested and policy-bound.
3. **The persona-import quarantine that re-binds the floor and zeroes capability.** Treating a shared persona file as the self-propagating skill-file it is — stripping any foreign floor, downscoping to a fresh stub, and Rule-of-Two-gating the import with the actual bytes shown to the human.

The novelty is the **coherent whole** — a triad that is simultaneously a human-legible role contract, a cryptographic capability certificate, an IFC-clearance carrier, and (a precondition for) a safe self-replicator genome — mounted cleanly on the v1 contracts, not any single field.

> **The one inflation explicitly retired (per review).** This spec does **not** call the genome "a safe self-replicator genome." That overstates: the genome makes the **floor** non-strippable but contributes **nothing** to the R_eff / recall / metering machinery that actually makes replication safe, and that machinery is not in this spec or in v1. The honest phrasing, used throughout: **"a genome whose floor is non-strippable-by-construction — a NECESSARY precondition for safe replication that a future Replication-Authority subsystem (doc-12) must complete."**

---

## 13.14 Open problems (honestly unsolved)

1. **Boot-check completeness vs a co-opted verifier.** The fail-closed boot check assumes the Boot Integrity Verifier and its root-of-trust are uncompromised; a forged-yet-internally-consistent triad signed by a compromised genesis-author key boots cleanly until a checker contradicts it (inherits the doc 04 §4.6 writer-key residual). Provable non-strippability holds **only relative to the TCB root.** The Shamir m-of-n custody requirement (§13.12) narrows but does not close this.

2. **Canary-scan recall on imported persona prose.** Screening SOUL/INSTRUCTIONS for embedded instructions / injection payloads is probabilistic early-warning, never a boundary — no prompt or classifier separates instructions from data in one token stream. A subtle payload in a benign backstory can pass. The taint-lattice + capability-downscope-to-stub are the load-bearing guards; the scan is defense-in-depth only.

3. **Differentiation-metric gameability.** The MorphAgent role-clarity / reasoning-path-divergence score gating genesis Promote shares doc 01 §16.4's unsolved problem: roles on the same base model can look differentiated while failing identically, so a redundant or correlated-failure role can be promoted. The metric is a proxy, not a guarantee.

4. **INVARIANT/VARIABLE boundary placement is a judgment call.** Which fields belong in the INVARIANT region is partly designer-chosen. Mis-placing a security-relevant field in VARIABLE (editable under mere Class-B) *or* over-freezing a benign field (ossifying the role) both have costs; there is no provably-correct partition. The §13.6.2 taint-clearance asymmetry is a hardening of one such placement, not a general solution.

5. **Floor-version reconciliation window tuning.** The grace-window size, the genuine-ancestor check's completeness against a determined rollback-to-weaker-floor attack, and the re-binding-sweep throughput at genome scale are empirical. Set the window too long and a deprecated-but-weaker floor stays bootable; too short and the sweep cannot keep pace and benign triads brick.

6. **Genesis-author key custody and the genome supply chain.** Every emergent role's trust bottoms out in the genesis engine's signing key and the governance VC issuer. Key compromise forges admissible genomes at scale. Mitigated by HSM custody + Shamir m-of-n for the highest-stakes issuance (doc 04 §4.15), but custody design remains an operational open problem.

7. **Re-attestation cost at genome scale.** Thousands of ephemeral signed emergent roles (the endogeneity-paradox regime) strain VC issuance, provenance-record throughput, and the human-ratification path for above-read-only grants. The spec bounds this by keeping stubs at Class-A with no VC re-issuance until first promotion and dropping discarded candidates before the provenance path — so cost scales with promoted roles, not attempted ones — but the steady-state cost of a high-genesis-rate swarm is **unmodeled.**

8. **The Replication-Authority subsystem (doc-12) does not yet exist.** The triad-as-replication-unit and floor-as-non-strippable-genome are preconditions this spec provides; R_eff<1, depleting generation caps, external lease + dead-man recall, no self-minted token, and the un-metered-spawn-channel guarantee are all **out of scope and unwritten.** This is the largest open item by safety weight, and it is a *missing subsystem*, not a residual of this one.
