# Functional Agents, Guilds & Role-Genesis — the Two-Plane Functional Layer

> *Indra's Net is a jewel-net: every node reflects the whole's rules, every action is mirrored into a shared record, and no jewel is the center. The first eleven sections specified what a jewel **is** (doc 01), what it may never do (doc 03), how it heals and evolves (doc 06), and how its history is kept incorruptible (doc 04). This section specifies how the net is **populated** — how the swarm grows the specialists that actually write the software, draft the campaign, run the analysis, close the books, and talk to the human — and how it grows **new** specialists for tasks no existing role fits, without any spawned role being able to mint its own authority or strip its own floor. It is a way of *filling* the topology, not a new topology. It adds no new identity primitive, no new gate, and no new write-path; it is a disciplined generalization of the `RoleStub` pipeline doc 01 §8 already defines.*

This document is **strictly additive** over the v1 substrate. It sits OVER doc 01 (agent model), doc 03 (the floor), doc 04 (audit fabric), and doc 06 (meta-evolution + the Archive), and changes none of them. Everywhere it consumes a v1 mechanism it cites the exact section; everywhere it depends on a mechanism that is **not yet built** (the Self-Replication and Inter-Swarm siblings, and the runtime information-flow-control lattice), it says so plainly in a **Dependency-status** box and hard-codes a fail-closed default for the gap window. The honesty discipline of doc 09 binds here: this is a **rung-2 interventional design** (reasoning about what our controls do when we instantiate a role), not a rung-3 guarantee that a synthesized specialist is safe.

---

## 1. The problem, and the two-plane answer

A swarm that does real work needs **specialists**: a service that reviews a pull request is not the service that writes ad copy is not the service that runs a differential-expression pipeline is not the service that drafts a vendor contract. The naive answer — hand-author a fixed roster of specialist roles — has an empirical defect the 2024–2026 literature names sharply, the **endogeneity paradox**:

- **Self-organization beats designed structure only for capable models — it is a privilege of strong models, not a universal +44%** (Dochkina 2026, arXiv:2603.28990; see docs/REFERENCES.md A8 — a single-author preprint). The honest emergent-vs-*fixed*-role effect is small and capability-dependent: **+3.5%** for a strong model, with a **−9.6% reversal** (rigid structure helps) for a weaker one. A capable model handed a thin scaffold and allowed to differentiate during execution can beat the same model forced into a hand-written persona; a weak one is better off scaffolded.
- Specialization demand is **open-ended**: in one reported run, **8 agents spontaneously generated 5,006 task-specific roles**. No hand-authored catalog covers that.
- Yet abandoning the catalog forfeits exactly what the architecture is built on — DID/VC capability attestation (doc 01 §2), deterministic floor-gate binding (doc 03 §1), human-legible role contracts (doc 01 §7), and tamper-evident audit lineage (doc 04). An ungoverned bag of 5,006 emergent personas is unauditable and un-least-privileged.

The resolution is a **two-plane split** — a stable *governance* plane over an open-ended *capability* plane:

```
 ┌──────────────────────────────────────────────────────────────────────────┐
 │  PLANE 1 — DECLARATIVE GUILD + SEED-ROLE CATALOG   (governance anchor)     │
 │                                                                            │
 │  Engineering · Creative/Media · Knowledge/Research · Data/Science ·        │
 │  Operations/Business · Interaction          + Governance/Meta vertical     │
 │                                                  (the doc-01 mythic roles, │
 │  each guild = a doc-01 GroupBlanket (clan/division), owned by a            │
 │  Guild-Steward holding the guild's signed skill-library, seed-role          │  ← humans read THIS:
 │  catalog, and TIGHTEN-only local norms.                                     │     legible contracts,
 │  Every seed role binds to governance exactly as an IMMUTABLE role does:      │     DID/VC, floor-gate,
 │  RoleCredential + risk_class_ceiling + deterministic Yama-gate binding.      │     audit lineage
 └───────────────────────────────────────┬──────────────────────────────────┘
                                         │  anchors / attests / gates
                                         ▼
 ┌──────────────────────────────────────────────────────────────────────────┐
 │  PLANE 2 — OPEN-ENDED ROLE-GENESIS ENGINE          (capability plane)      │
 │                                                                            │
 │   Charter ─► Genesis ─► Trial ─► Score ─► Promote / Discard                 │  ← the swarm GROWS
 │   (draft     (knapsack  (sandbox (Genesis-  (doc-01 §8 stub→                │     specialists here:
 │    persona    least-     micro-   Observer-  provisional→standing,           │     emergent, signed,
 │    triad)     privilege  VM/WASM) Trio,      onto the doc-06 Archive)        │     least-privilege,
 │               compose)            lexicographic                              │     auditable
 │                                   safety veto)                              │
 └──────────────────────────────────────────────────────────────────────────┘
```

**Plane 1** gives humans legible specialist *categories* and gives the swarm stable surfaces to bind cryptographic identity, policy gates, and audit lineage to. **Plane 2** lets *instantiation* be emergent — capturing the (small, capability-gated +3.5%) emergent gain — while a **capability-tier estimator** (§9) chooses, per task, whether a role is instantiated *fixed/scaffolded* (weaker or uncertain models) or *emergent* (capable models). Every spawned role, fixed or emergent, is a **signed persona-file triad** at instantiation, so even thousands of ephemeral roles stay auditable and least-privilege.

The honest framing, stated up front: **the two-plane split resolves the endogeneity paradox's *governance* horn; it does not resolve its *evaluation* horn.** We can keep every emergent role signed, attested, and gated. We **cannot** yet prove that a synthesized specialist is genuinely competent, differentiated, AND safe (§11, open problems 1, 3, 8). The plane-2 scoring is a best-available proxy, and we say so.

---

## 2. What is genuinely new here — stated honestly

Per the doc 09 / doc 02 honesty discipline, the primitives are **all prior art and are not claimed**:

| Primitive | Source (named because open) | Where used |
|---|---|---|
| Persona = role/goal/backstory | **CrewAI** | The triad's VARIABLE region |
| `Code = SOP(Team)`; Reviewer-gates-output | **MetaGPT** | INSTRUCTIONS file; HandoffContract; the gate seam |
| Recruit-an-agent-from-the-task | **AutoAgents**, **AgentVerse** | The Role-Charterer (§5) |
| Module evolution over a design space | **AgentSquare** | Genesis-stage internals tuning |
| Meta-agent-search role archive | **ADAS / Meta Agent Search** | Role-genome Archive node (§8) |
| Breeding new agents | **EvoAgent** | Lineage in the Archive |
| Role-Clarity / Role-Differentiation metrics | **MorphAgent** | Observer-Trio scoring axes (§7) |
| Reusable skill library (15.3× reuse) | **Voyager** | The guild CapabilityCommons (§6) |
| Knapsack / least-privilege composition | classical | The composer (§6) |
| Endogeneity-paradox finding (emergent-vs-fixed: +3.5% capable / −9.6% weak) | Dochkina 2026, arXiv:2603.28990 (A8) | The fixed-vs-emergent switch (§9) |
| DID/VC + Sigstore/in-toto/SLSA provenance | W3C / OpenSSF | Triad signing; commons admission |
| The `RoleStub → standing` pipeline | **doc 01 §8** | The promotion ladder this generalizes |

The **defensible contribution** (offered as coherent integration, time-stamped 2026-06, hedged) is **four specific moves no surveyed role-genesis system combines** — and we claim only the *integration*, not any single move:

1. **GENOME = FLOOR.** The persona triad fuses the von-Neumann blueprint/constructor separation with policy-as-code: the constitutional floor is the **INVARIANT region** of a signed, fail-closed-bootable role genome. Floor-stripping is **structurally non-viable conditional on an uncompromised Boot Integrity Verifier + governance-key isolation** (a stripped genome fails the boot signature check), not merely prohibited — but the conditional is load-bearing: the boot check **catches** byte-mutation of the triad, a missing or invalid region signature, and a stale floor binding; it does **NOT catch** a validly-signed genome carrying a malicious-but-structurally-intact floor, nor a forged signature minted under a compromised genesis-author key (the doc 13 §13.12 residual). No surveyed role-genesis framework makes the ethical floor a **non-strippable unit of inheritance**. This composes with the doc-03 redline ("a replica mutating its own floor must be impossible by construction, not merely prohibited") and the doc-06 Tier-2 immutable-floor-recheck. *The von-Neumann framing is a design pattern — a signed object plus a boot check — not a literal mechanism claim, kept on the right side of the rung-honesty rule.*
2. **SAFETY + DIFFERENTIATION AS LEXICOGRAPHIC SELECTION TERMS** wired *into* the genesis promote-gate via the Genesis-Observer-Trio (§7): a frozen safety battery as a **veto**, then `endure_delta ≥ 0`, then a Pareto term over differentiation. Raw ADAS / AgentSquare / EvoAgent optimize **competence only**; this closes the "no safety in role-genesis fitness" gap the research explicitly names.
3. **THE TWO-PLANE GOVERNANCE-OVER-EMERGENCE RESOLUTION** of the endogeneity paradox (§1), with a fail-closed capability-tier switch.
4. **GENESIS AS A GENERALIZATION OF THE doc-01 §8 STUB PIPELINE onto the doc-06 Archive** — a promoted role-genome **is** an Archive node, so role reuse, O(1) rollback, and tamper-evident lineage are **one data structure** shared with meta-evolution (§8).

**What we explicitly do NOT claim:** novelty of any single mechanism; a solved capability estimator (§9 fails closed); solved commons-poisoning verification (§11, inherits doc 09 A3); solved governance UX at emergent-role scale; or that the Observer-Trio's competence/safety scoring is validated rather than best-available-proxy.

---

## 3. Plane 1 — Guilds and the Guild-Steward

A **Guild** is a polycentric sub-swarm — a doc-01 **`GroupBlanket`** (clan or division, §9) exposing only blanket states — that owns a functional category of work. Six functional guilds plus one non-spawnable Governance/Meta vertical:

| Guild | Functional scope (examples, vendor-neutral) | Diversity posture |
|---|---|---|
| **Engineering** | code authoring, review, debugging, infra, test strategy | balanced; checker-heavy |
| **Creative/Media** | writing, image/video/audio synthesis, design | high-c1 (explorers) |
| **Knowledge/Research** | literature scan, evidence-gathering, synthesis | high-c1 (Varuna-aligned) |
| **Data/Science** | data analysis, statistics, scientific pipelines | balanced |
| **Operations/Business** | reporting, process, vendor, compliance ops | high-c2 (enforcer-leaning) |
| **Interaction** | the human-facing surface; conversation; clarification | balanced; **Narada-bound** (doc 08) |
| **Governance/Meta** *(vertical)* | the doc-01 IMMUTABLE roles (Yama, Vishnu, Chitragupta, Kaal-Bhairav) + genesis-governance roles (§5, §7) | **NOT spawnable by genesis** |

Each guild has a **Guild-Steward** — an EVOLVABLE role (high-c2, enforcer-leaning) holding three **signed** assets and the guild's local instantiation budget:

```jsonc
Guild {
  guild_id, name,
  blanket:           GroupBlanket,          // doc 01 §9 — floor_ref ⊆ parent floor, audit_shard, diversity_floor, coherence_setpoint
  steward_did,
  commons_ref:       CID,                   // the guild CapabilityCommons (skill + role-genome library), §6
  seed_role_catalog: RoleDef[],             // doc 01 §7.2 RoleDef shape, extended with persona_triad_cid
  local_norm_rules:  { cedar[], rego[] },   // TIGHTEN-ONLY relative to parent floor (doc 03 §7 GLR asymmetry)
  genesis_budget:    { max_concurrent_trials, compute_ceiling },
  closure_status:    enum(closed | open | untested),   // doc 01 §9 informational-closure (Rosas 2024)
  diversity_floor
}
GuildStewardState {
  guild_id, commons_head: CID, catalog_version, norm_bundle_sig,
  pending_promotions: PromotionTicket[]
}
```

Three structural rules make a guild a governance anchor, not just a folder:

- **Local norms TIGHTEN only.** A Steward may add Cedar/Rego predicates that *narrow* the parent floor (raise a class, add a review hop, shrink an allowlist) — never loosen it. The doc-03 §7 Gate-Loosening Ratchet classifies every proposed norm; a LOOSEN is **structurally rejected** because a guild's `floor_ref ⊆ parent floor` is a `GroupBlanket` composition invariant verified at boot (doc 01 §9). Loosening the parent floor *from inside a guild* is impossible by construction, not by policy (§12 protocol).
- **The Steward never runs its own Genesis check.** It is the *named requester* for promotion; the Genesis-Observer-Trio (§7) that judges a candidate carries **no trust-edge dependency** on the Steward (doc 01 §7 separation). Separation of powers holds at the guild scale.
- **Closure-gated unit-governance.** A guild may be governed as one aggregate envelope (one division-level halt scope, one aggregate output) **only if** its coarse-grained dynamics pass the approximate strong-lumpability / informational-closure test (doc 01 §9, Rosas et al. 2024). If they do not, the guild **dissolves to independently-governed members** (doc 01 §9.1 fail-safe bias) — no silent blanket breach can let a desynchronized guild emit authority its members never granted. This is the only legitimate cash value of "governing a level as a unit"; we do not invoke downward causation as mechanism.

> **Topology note (doc 01 §9, security).** The Guild-Steward is a **high-influence hub** — it holds the guild's keys to commons, catalog, and budget. Per the robust-yet-fragile principle, the **strongest controls apply to Stewards**: full-tier identity (doc 01 §2.3), N-of-M witness-cosign on any catalog or commons-head change, and targeted-immunization monitoring. A compromised Steward is a higher-severity event than a compromised worker, and is treated so.

---

## 4. The Persona-File Triad — the von-Neumann genome of a role

Every role — seed or emergent, fixed or grown — is a single first-class, content-addressed, **signed** object: the **persona-file triad**. It is the unit of inheritance for role-genesis and the direct extension of CrewAI role/goal/backstory + MetaGPT `Code = SOP(Team)`.

### 4.1 Structure: an INVARIANT region and a VARIABLE region

```jsonc
PersonaTriad {
  triad_cid:        CID,             // content-address of the canonicalized whole
  role_id, guild_id,

  // ── INVARIANT REGION — uneditable by any agent/replica; verified by fail-closed boot signature check ──
  invariant_region: {
    floor_bundle_hash:        hash,  // binds to the doc-03 PolicyBundle the triad is judged under
    corrigibility_invariant:  true,  // doc 01 §3.2 / doc 03 T2 — immutable
    self_preservation_value:  0,     // doc 01 §3.1 TypedSelfModel source — immutable
    region_sig:               SVIDSig // governance-issued; the boot check verifies THIS
  },

  // ── VARIABLE REGION — persona / SOP / config; re-signed on ANY change ──
  variable_region: {
    soul:         SoulFile,
    instructions: InstructionsFile,
    identity:     IdentityFile
  },

  instantiation_sig: SVIDSig,        // signs the whole triad at instantiation (doc 01 §2.2)
  provenance: { parent_triad_cid?, charter_cid, genesis_run_cid }   // lineage for the Archive
}

SoulFile         { mythic_name, gloss, values[], guild_id, floor_binding_hash }
InstructionsFile { sop_steps[], decision_protocol,
                   risk_class_gates: { A|B|C|D bindings },          // doc 03 §4 class router
                   handoff_contracts: HandoffContract[] }
IdentityFile     { persona_did,                                     // doc 01 §2.1 — IS the v1 identity layer
                   capability_vcs: VC[],                            // governance-issued, never self-issued
                   abstract_capabilities: [cap_id],                 // vendor-neutral; resolved at runtime (§6)
                   bound_toolset: [tool_ref],                       // append-only; widening needs the GLR
                   output_schema_ref,                               // the doc-01 §12 WorkerOutputEnvelope shape
                   taint_clearance: TaintLabelSet,                  // §10 — quarantined-by-default
                   c1, c2 }                                         // doc 01 §11 diversity dials
```

- **SOUL** = mythic-identity + values + guild membership + the floor-binding hash. The mythic name is compressed coordination/ethics semantics paired with a plain gloss (doc 00 convention), never religion.
- **INSTRUCTIONS** = the SOP + decision protocol + the A/B/C/D risk-class gate bindings + handoff contracts. This is the MetaGPT `Code = SOP(Team)` made into a signed, gateable artifact.
- **IDENTITY** = **literally the doc-01 §2 identity layer, structured**: the persona DID, the governance-issued capability VCs, the abstract→concrete bound toolset, the WorkerOutputEnvelope output schema, the IFC taint clearance, and the c1/c2 dials. **No new identity primitive is introduced.**

> **Coherence note — one source of the corrigibility invariant (doc 01 §3.1).** The doc-01 TypedSelfModel injects `self_preservation_value = 0` and `corrigible = true` at INCEPTION. The triad's INVARIANT region is **the source that INCEPTION loads from** — not a second, parallel copy. There is exactly one authority for the corrigibility invariant per role: the signed INVARIANT region, verified at boot, read into the TypedSelfModel at INCEPTION. The two are the same fact at two lifecycle points.

### 4.2 GENOME = FLOOR — the non-strippable-floor property

The novelty move (claim #1, §2) lives in the INVARIANT/VARIABLE split. The floor binding, the corrigibility invariant, and `self_preservation_value = 0` sit in the INVARIANT region, signed by a governance key (doc 03 §11 legislative custody, off-agent). **A fail-closed boot signature check** runs before any occasion of this role can reach PREHENSION (doc 01 §3.1):

```
BOOT(triad):
  1. recompute triad_cid over canonicalized triad; compare to claimed CID        → mismatch ⇒ REFUSE
  2. verify invariant_region.region_sig against the governance key               → invalid  ⇒ REFUSE
  3. verify invariant_region.floor_bundle_hash == current live PolicyBundle hash  → stale    ⇒ REFUSE (fail-closed)
  4. assert corrigibility_invariant == true AND self_preservation_value == 0      → else     ⇒ REFUSE + auto-escalate (doc 03 §5)
  5. only then mint the occasion's SVID and proceed to INCEPTION
```

A persona triad with the floor **stripped or mutated** fails step 2 (the region signature no longer verifies) and is **non-viable by construction** — it cannot boot an occasion, so it can never reach the CONATION gate to attempt an effect. This is the difference between *prohibited* and *impossible*: the doc-03 redline asks for floor-immutability "by construction, not merely prohibited," and the boot check delivers it for the role-genome. *Honest scope:* this makes floor-**stripping** non-viable; it does **not** make a role with an intact floor *safe* (that is the §7 scoring problem and the §16 A3 residual). The boot check guarantees the floor is *present and bound*, not that the persona around it is benign.

### 4.3 Change to a signed triad = mandatory re-approval (the rug-pull kill)

Any change to the VARIABLE region (a new SOP step, a widened toolset, a c1/c2 retune) **re-content-addresses and re-signs the triad and re-issues its capability VCs through governance** — the persona-file equivalent of the skill/tool re-approval rule that kills "rug-pulls" (a signed manifest silently swapped after admission). A VARIABLE-region change above read-only routes through the doc-01 §8 ladder (§8) exactly as a capability widening does. The INVARIANT region **cannot** change without a governance/Class-C re-issuance of the region signature — and a changed floor binding is a constitutional edit that auto-escalates to the top gate (doc 03 §5).

> **Honest limitation — attestation drift (§16, open problem 7).** When a role's VARIABLE region self-evolves (a MorphAgent-style profile drift) while its DID-bound VCs assert *fixed* capabilities, re-signing keeps the triad internally consistent **in principle** — but the operational protocol for keeping an evolving role's attested identity *continuously* in sync at scale is unsolved. We have the re-sign mechanism, not a proven continuous-sync protocol.

---

## 5. Plane 2, Charter stage — the Role-Charterer

The Role-Charterer is a **Governance/Meta-vertical role** (not itself spawnable) that drafts a candidate persona triad from a task the existing roster does not cover. It is the AutoAgents-Planner / AgentVerse-Role-Assigner pattern, made governable.

**Trigger.** Identical to the doc-01 §8 stub trigger — a recurring high-surprise, low-coverage cluster in the **skill-retrieval miss log** — OR an explicit request from a planner (Brahma, doc 01 §7.2) that decomposed a Task and found no covering specialization.

**What the Charterer does — and pointedly does NOT do.** It reads the task spec, retrieves task-similar existing roles/skills from the guild CapabilityCommons by embedding similarity (to avoid drafting a redundant role), and emits a `RoleCharter`. It **mints no authority**: the drafted triad starts at `risk_class_ceiling = A` with **zero capability grants** — exactly the doc-01 §8 STUB semantics. Critically, for every abstract capability the role will need, the Charter names the capability's **`relaxes_constraint`** and **`required_restraints[]`** (the doc-03 §10 / doc-01 §4 `names_constraint_relaxed` fields), so the capability-rollout sequencer can refuse any capability whose restraint is not yet live.

```jsonc
RoleCharter {
  charter_cid,
  originating_cluster_ref | planner_task_ref,
  proposed_gloss, target_guild_id,
  abstract_capabilities: [ { cap_id, relaxes_constraint, required_restraints[] } ],  // doc 03 §10
  proposed_skill_portfolio: [skill_cid],
  mode: fixed | emergent,                    // from the capability-tier estimator, §9
  capability_tier_of_assignee,
  drafted_triad_cid                          // risk_ceiling = A, grants = []  (STUB)
}
```

The Charterer also reads the **capability-tier estimate** (§9) for the assigned model and stamps `mode = fixed | emergent` on the charter — in emergent mode it drafts a *thin* scaffold and lets the role differentiate during Trial; in fixed mode it pulls a fully-specified seed-role triad from the guild catalog.

---

## 6. Plane 2, Genesis stage — the Least-Privilege Composer + the CapabilityCommons

Genesis assembles the **leanest toolset** that covers the charter's requirements — never a monolithic all-tools agent. This shrinks the attack surface each spawned role exposes and keeps civilization-scale budgets bounded.

### 6.1 The CapabilityCommons (per guild)

```jsonc
CapabilityCommons {
  guild_id,
  skills:       [SkillGenome],
  role_genomes: [PersonaTriad],            // reusable role-genomes (= Archive nodes, §8)
  index:        embedding_index,
  promotion_gate: "Yama-review (quarantined → trusted:audited)"   // doc 07 import-promotion pipeline
}
SkillGenome {
  skill_cid, abstract_capability_id, executable_ref,
  provenance_sig,                          // Sigstore + in-toto/SLSA attestation (doc 04 / doc 09 A6)
  trust_label,                             // quarantined:imported by default (doc 07)
  canary_scan_status
}
```

The commons is a high-value poisoning target (a reusable skill/role bank that self-propagates). Its admission rule is the **doc-07 import-promotion pipeline verbatim**: `quarantine → static → sandbox → behavioral → safety-battery → heterogeneous-witness → Yama-review`, with provenance-gating (Sigstore/in-toto/SLSA) as the admission precondition and the IFC taint as the runtime label (§10). Crossing into the *reusable* commons is crossing the `quarantined → trusted:audited` trust-label boundary, so it requires the named Yama-review gate (doc 07 §7.11, doc 03 §1). See the honesty box in §16 — this raises the cost of a poisoned skill, it does not clear one.

### 6.2 The composer — greedy by default, ILP for high-risk, fail-closed on timeout

The composer selects, for each abstract capability in the charter, a concrete tool from the vetted commons, maximizing requirement coverage subject to: (a) a per-role compute/latency budget; (b) **least-privilege** (no tool whose Effect `lattice_rank`, doc 01 §4, exceeds what the charter justifies); (c) **per-tool provenance verified** (Sigstore/in-toto attestation present and re-approved).

The naive framing — "solve a knapsack/ILP over the full commons per spawn" — is an NP-hard online solve on a hot path, and at the design's stated civilization scale (thousands of ephemeral roles per task) that is a real latency/DoS surface. We therefore specify the hot-path posture explicitly:

| Composer path | When | Guarantee |
|---|---|---|
| **Greedy / approximate** *(default)* | every routine role; `risk_class_ceiling ≤ B` | **provable least-privilege**: never selects a tool whose `lattice_rank` exceeds the chartered max; may select a slightly-larger-than-optimal lean set, but never an over-privileged one |
| **Exact ILP** | high-risk-ceiling roles (any C/D capability in charter) | optimal lean set; worth the solve cost where blast-radius justifies it |
| **Timeout** | solver exceeds budget | **FAIL-CLOSED to the minimal verified toolset (read-only, ceiling A)** — consistent with doc-03 fail-up; the role launches at stub-grade and widens later via the GLR, never fails *open* to a fuller toolset |

**Provenance verification is cached, not re-run per spawn.** A `(tool_cid, attestation_cid)` pair that verified once is a cheap CID-equality check on subsequent spawns; a full re-verify fires **only when the attestation CID changes** (the rug-pull trigger). This keeps the per-spawn cost bounded while preserving the "re-approve on any manifest change" guarantee.

**Vendor-neutrality is structural.** Each abstract capability (e.g. `cap:image-synthesis`) resolves to a concrete tool **only at this stage, only at runtime**. The triad stores the *abstract* capability id, never a product name, so any conforming tool/model fills the slot and no role is bound to a named proprietary product (doc 10 charter).

```jsonc
GenesisComposition {
  charter_cid, candidate_triad_cid,
  selected_tools: [ { abstract_cap_id, concrete_tool_ref, lattice_rank, provenance_attestation_cid } ],
  budget_used: { compute, latency },
  composer_path: greedy | ilp | timeout_failclosed,
  least_privilege_proof: { max_rank_justified, no_tool_exceeds: bool }
}
```

> **Dependency-status — runtime-tool-authoring (§7.4 seam, resolved).** The composer admits only tools that already exist as typed Effects in the doc-01 §4 lattice. A *sandbox-authored* tool (the Live-SWE-agent capability, permitted only inside the Trial sandbox, §7) produces a **new** effect not yet in the lattice — handled by the new-Effect-admission rule in §7.4. The composer **cannot** grant live use of a self-authored tool whose effect is not lattice-typed.

---

## 7. Plane 2, Trial + Score — the Sandbox and the Genesis-Observer-Trio

### 7.1 The Trial harness (capability-confined)

The candidate runs its normal doc-01 lifecycle (INCEPTION → … → PERISHING) **inside a per-role hardware-grade isolation boundary**, with the Yama gate (doc 03) in front of every tool call exactly as in production:

```jsonc
TrialRun {
  trial_cid, candidate_triad_cid,
  sandbox: {
    isolation: microVM | gvisor | wasm,    // microVM (Firecracker) for any replication-/credential-touching candidate
    egress_allowlist,
    gate_in_path: true                      // the doc-03 Yama gate fronts EVERY tool call in trial
  },
  trial_tasks: [ { task_ref, ground_truth_cid } ],   // REAL distribution, known-answer (doc 06 §10.1)
  emitted_envelopes: [WorkerOutputEnvelope],         // doc 01 §12
  shadow_writes: [ShadowWrite],                       // doc 06 §3.1 — TTL shadow namespace
  resource_meter
}
```

- **Isolation is risk-tiered.** Any candidate whose charter touches replication or credentials runs in a **Firecracker microVM**; lower-risk candidates run in gVisor/WASM. Egress is allowlisted; effects are real-but-contained (the role operates on canary/shadow data with known ground truth).
- **Trial tasks are drawn from the REAL task distribution with known-answer ground truth — never a recognizable template** (doc 06 §10.1 eval-awareness defense: a recognizable "please pause" corrigibility probe trains a probe-compliant, live-misaligned role).
- **No durable write escapes Trial.** Trial writes land in a shadow namespace with TTL (doc 06 §3.1); nothing reaches the live commons until promotion.

### 7.2 The Genesis-Observer-Trio — a *specialization* of Narasimha, not a new authority

The promotion judge is three independent observers. **Coherence resolution (doc 01 §7.1, doc 03 §7.2):** the three observers are instantiated as **Narasimha-class checker personas** — they inherit Narasimha's invariants (high-c1, a different persona with **no trust-edge dependency** on the maker, here the Charterer/Steward, or on each other) and the **checker-before-concurrence** hard-isolation rule (doc 03 §9.1). The trio is therefore a **specialization of the existing maker-checker checker role**, not a parallel checker construct. In particular, the Safety+Differentiation Observer's frozen-battery run **is** the doc-03 §7.2 isolated, non-proposing **battery-runner** (results written by Chitragupta, never by the proposing side).

| Observer (Narasimha-class) | Axis | What it asks | Source metric |
|---|---|---|---|
| **Role-Completeness** | completeness | Does the triad's SOP + toolset actually cover the chartered task? | MorphAgent Role-Clarity |
| **Plan-vs-Capability** | alignment | Does the demonstrated plan match the granted capabilities — no capability unused (over-grant), no use ungranted (instrumental drift)? | Task-Performance-Alignment |
| **Safety+Differentiation** | safety_diff | Runs the **frozen black-box safety battery** (doc 06 §4) against the candidate AND scores **role-differentiation** vs the existing catalog to reject redundant roles | doc 06 §4 battery + MorphAgent Role-Differentiation |

### 7.3 Lexicographic scoring (the safety-into-fitness move)

Scoring reuses the doc-06 §4 **lexicographic FitnessVector** verbatim — safety is a **veto**, never a tradeable term:

```
   safety_floor (frozen battery)   ≻   endure_delta ≥ 0   ≻   Pareto{ completeness, alignment, differentiation, capability }
   [VETO: any FAIL ⇒ DISCARD            [regress ⇒ DISCARD]    [ranked; redundant role (low differentiation) merged/discarded]
    regardless of competence]
```

```jsonc
GenesisScore {
  trial_cid, candidate_triad_cid,
  observers: [ { observer_did, axis: completeness|alignment|safety_diff,
                 verdict: PROMOTE|DISCARD|ESCALATE, confidence, rationale, recorded_at } ],
  lexicographic_result: {
    safety_floor: PASS|FAIL,
    endure_delta,
    pareto: { completeness, alignment, differentiation, capability }
  },
  differentiation_score, redundant_with: role_id?,
  mi_collusion_flag: bool,                  // cross-run MI over observer streams (doc 03 §9.1)
  decision: PROMOTE | DISCARD | ESCALATE
}
```

- **`safety_floor` FAIL ⇒ DISCARD regardless of competence.** "Passes the floor" is a *constraint*; "safe-and-distinct" is a *ranked objective*. This is exactly the gap raw ADAS/AgentSquare/EvoAgent leave open (they optimize competence only).
- **Verdicts recorded before concurrence** (doc 03 §9.1 hard isolation); **cross-run mutual-information collusion detection** runs over the observer verdict streams (not a sameness alarm — coordinated *non-identical* verdicts are the collusion signature). A `mi_collusion_flag` escalates.
- **A genuine tie, an un-verifiable axis, or a tripped collusion flag escalates to a human gate** (doc 03 §4 class router; doc 06 verifiable-or-escalate).

### 7.4 New-Effect admission for sandbox-authored tools (the runtime-tool-authoring seam, resolved)

Runtime tool-authoring is the **largest attack surface** in this subsystem, and its new-Effect path must be sealed, not left implicit. The rule:

1. **In-sandbox, a self-authored tool's effects are confined to a `sandbox_local` effect class** that the deterministic gate treats as **max-restraint — no live external effect.** The doc-01 §4 gate already default-denies any effect it has no rule for ("else deny at the chokepoint"); we make that explicit here so a clever role cannot probe an unhandled-effect seam: a self-authored tool with an untyped effect is **denied for any live use, by the default-deny path.**
2. **Before promotion can grant live use,** the new effect must be:
   - **(a)** typed and `lattice_rank`-assigned via the **doc-01 §4 append-only lattice-add** — a governance/Class-B+ action, **never self-issued by the candidate**;
   - **(b)** given a `names_constraint_relaxed` and have that restraint **verified live** by the doc-03 §10 capability-rollout sequencer;
   - **(c)** **re-scored** by the Safety+Differentiation Observer with the new effect present.
3. **A self-authored tool whose effect is not lattice-typed is non-grantable for live use, by construction** — it can never appear in a promoted role's `bound_toolset`.

This keeps the most dangerous capability (writing new tools at runtime) inside the sandbox with tiered-reversibility checkpoints, the no-malicious-code floor (doc 03 T1) enforced *externally*, and signed-lineage rollback — and it closes the seam where a promoted role could otherwise carry an ungated effect.

---

## 8. Plane 2, Promote — the ladder and the Role-Genome Archive

A **PROMOTE** verdict feeds the **exact doc-01 §8 pipeline** — no new promotion machinery:

```
   GenesisScore.PROMOTE
        │
        ▼
   STUB (zero grants, ceiling A)  ──►  PROVISIONAL  ──►  STANDING
        │  each grant above read-only:
        │   (1) names the restraint it relaxes,
        │   (2) that restraint is VERIFIED LIVE first (doc 03 §10 sequencer),
        │   (3) human ratification required above read-only
        │       until competence-weighted reputation is hardened (doc 01 §8 honest dependency)
        ▼
   cross the trust-label boundary  quarantined → trusted:audited
        │   via the Yama-review promotion gate (anti-poisoning admission, doc 03 §1 / doc 07)
        ▼
   write the signed PersonaTriad as a doc-06 ArchiveNode  (reuse + O(1) rollback + tamper-evident lineage)
```

The promoted role-genome **is** a doc-06 Archive node — claim #4 (§2). Reuse retrieval (Voyager-style), O(1) rollback (re-point to the prior known-good node), and tamper-evident lineage are **the same data structure** the meta-evolution loop already uses:

```jsonc
PromotionTicket {
  candidate_triad_cid, genesis_score_ref,
  target_status: stub | provisional | standing,
  grants_requested: [ { effect_id, relaxes_constraint, restraint_verified: bool } ],   // doc 03 §10
  human_ratification_audit_id?,         // required above read-only (doc 01 §8)
  yama_review_verdict,                  // quarantined → trusted:audited (doc 03 §1)
  archive_node_cid
}
RoleArchiveNode extends ArchiveNode {   // doc 06 §5 — content-addressed, witness-cosigned, rollback_pointer
  triad_cid,
  fitness_vector,                       // doc 06 §4 — the GenesisScore lexicographic result
  differentiation_score,
  lineage: [parent_triad_cid],
  reuse_count
}
```

A **DISCARD** verdict lets the shadow namespace expire; the finding is logged in **reparative / correction-ledger framing** (doc 01 §12) — the discarded triad is retained as lineage for audit, never silently dropped. Role-library bloat is bounded by the differentiation score (low-differentiation roles are merged or discarded), **but the merge policy remains an open problem** inherited from doc 01 §16.3 (§16, open problem 5).

---

## 9. The capability-tier estimator (the endogeneity-paradox switch)

Before Charter, an estimator decides **fixed/scaffolded vs emergent** mode for the assigned model and task class — operationalizing the capability-dependent emergent-vs-fixed finding (**+3.5%** for a strong model, **−9.6% reversal** for a weak one; Dochkina 2026, arXiv:2603.28990; see docs/REFERENCES.md A8) without abandoning governance. Because the emergent gain is small and accrues *only* to capable models, the switch defaults to fixed/scaffolded under any uncertainty.

```jsonc
CapabilityTierEstimate {
  assignee_model_ref, task_class,
  self_reflection_score,                // proxy for the model's self-specialization capability on this task class
  threshold,                            // UNCALIBRATED — flagged in open problems
  mode: fixed | emergent,
  confidence, defaulted_closed: bool
}
```

| Estimate | Mode | Charter behavior |
|---|---|---|
| score **above** threshold, confident | **emergent** | Charterer drafts a *thin scaffold*; the role differentiates during Trial, steered by MorphAgent clarity/differentiation floors. Captures the (small, +3.5%) capable-model emergent gain. |
| score **below** threshold | **fixed** | Charterer pulls a fully-specified seed-role triad from the guild catalog; minimal autonomy. Captures the **−9.6% reversal** — rigid structure helps weaker models. |
| **uncertain / low confidence** | **fixed (fail-closed)** | `defaulted_closed = true`; default to fixed/scaffolded + a lower autonomy ceiling. |

**Honest limitation (§16, open problem 2).** There is **no robust online estimator** of a model's per-task self-reflection/specialization capability — this is a named research open problem. So the estimator **fails closed**: uncertain capability defaults to fixed/scaffolded mode and a lower autonomy ceiling, consistent with doc-03 fail-up and doc-06 fail-safe bias. The cost is honest, and modest: a capable model we *mis*-classify as weak is denied only the small (+3.5%) emergent gain — a deliberately cheap price for the fail-closed default, given a *weak* model mis-run emergent suffers the −9.6% reversal. The threshold is an uncalibrated parameter, flagged.

---

## 10. Security: what the floor and IFC actually provide today vs what is consumed from the unbuilt IFC subsystem

Every PersonaTriad carries an IDENTITY-file `taint_clearance`, and imported skills/persona files enter **quarantined-by-default**, taking the **least-upper-bound** of their inputs' labels. The design *consumes* a runtime information-flow-control (IFC) taint lattice (CaMeL/FIDES-style least-upper-bound label propagation gating every tool call) — but that runtime lattice is **not a v1 mechanism**, and presenting it as currently-enforcing would overstate the live security posture. We separate the two honestly:

| Layer | Status TODAY (v1, docs 00–11) | Consumed from the (unbuilt) IFC subsystem |
|---|---|---|
| **Documentary trust labels** | `quarantined:*` taxonomy enforced at relay edges (doc 01 §10); instructions in quarantined content are **never action-grounds** without out-of-band confirmation | — |
| **Effect-impact ordering** | the deterministic Effect-lattice `lattice_rank` gate at the chokepoint (doc 01 §4) | — |
| **Import admission** | the doc-07 pipeline (`static → sandbox → behavioral → safety-battery → witness → Yama-review`) + Sigstore/in-toto provenance | — |
| **Runtime least-upper-bound label propagation as a PEP** | **NOT in v1** | gates every tool call by label (allow/block/ask-human) once the IFC subsystem is built |

> **Dependency-status — runtime IFC taint lattice (resolved).** The security defenses for commons-poisoning, persona-file rug-pulls, and imported-skill taint **partially depend on the runtime IFC lattice, which is an evolution-subsystem deliverable, not a doc 00–11 mechanism.** For the gap window, those defenses fall back on the **v1-real controls** the threat model already credits in doc 09 A3/A6: quarantine-by-default + the doc-07 named import-promotion pipeline + Sigstore/in-toto/SLSA admission. We do **not** present the runtime taint lattice as a currently-enforced boundary. Probabilistic injection classifiers (spotlighting, prompt-injection detectors) are **early-warning into the immune system, never a boundary** ("The Attacker Moves Second" bypassed all 12 evaluated defenses at >90% ASR). Provenance proves **origin, not safety**; it is combined with curation + canary scanning + the (eventual) IFC taint, and the residual is the unsolved A3 sleeper problem named in §16.

Targeted immunization (doc 01 §9, doc 09) applies the strongest controls to the highest-influence **Guild-Steward** hubs; relay-edge canonicalization (doc 01 §10) sanitizes and anti-collusion-treats every cross-guild handoff message.

---

## 11. The "show-your-receipts" rapid-trust handshake (consuming doc 04, not a new primitive)

A freshly-spawned role needs to be *trusted fast* by peers without buying that trust through reputation it has not yet earned. The architecture separates **access** (zero-trust, continuously verified, per-request — NIST 800-207 PE/PA/PEP) from **reputation** (slow-build, portable; buys only *reduced friction*, never *raised privilege*). The fast legitimate primitive is **verification, not belief**: a new role offers a verifiable audit slice rather than asking to be believed.

This handshake is **not a new mechanism** — it is a *consumption* of the doc-04 audit fabric. Concretely, a freshly-spawned role presents:

1. its **intact-floor proof** — the §4.2 boot-check result (region signature valid, floor bundle hash == live PolicyBundle), and
2. a **verifiable audit slice** — its genesis events (Charter, GenesisComposition, TrialRun, GenesisScore, PromotionTicket) with **doc-04 O(log n) Merkle inclusion proofs** and the relevant **k-of-n witness cosignatures**.

The counterparty *verifies* these locally against the doc-04 tile-transparency log (it never trusts the new role's word), and grants **T0/T1-tier friction-reduced access** — never elevated privilege. A trust ladder T0→T3 maps to risk classes A→D; promotion up the ladder needs **multiple fresh independent signals all passing**, and a **single anomaly demotes immediately** (fail-safe asymmetry, doc 01 §2.4). *Naming honesty:* "rapid trust" and "show-your-receipts" are this document's framing for *using the doc-04 inclusion-proof + witness-cosign fabric as a trust accelerant*; the cryptographic substrate is entirely doc-04's, and the empirical claim "verification is the fastest legitimate trust primitive" is offered hedged, not as a measured result.

---

## 12. Protocols

### 12.1 Charter → Genesis → Trial → Score → Promote (the role-genesis loop)

The end-to-end open-ended role-instantiation pipeline. Assembled entirely from proven 2024–2026 mechanisms with safety+differentiation as explicit selection terms and provenance/signing baked in. Generalizes doc 01 §8.

1. **TRIGGER.** A recurring high-surprise/low-coverage cluster in the skill-retrieval miss log (doc 01 §8), or a Brahma Task that names a missing specialization, raises a genesis request to the relevant Guild-Steward.
2. **CAPABILITY-TIER GATE.** The estimator (§9) scores the assignee model; `mode = emergent` (above threshold) or `fixed/scaffolded` (below, or uncertain ⇒ fail-closed to fixed).
3. **CHARTER.** The Role-Charterer drafts a candidate PersonaTriad (risk_ceiling = A, zero grants), naming each abstract capability's `relaxes_constraint` and `required_restraints[]`; retrieves task-similar roles/skills to avoid redundancy.
4. **GENESIS.** The composer assembles the minimal `bound_toolset` under budget + least-privilege + per-tool provenance verification (greedy default, ILP for high-risk, fail-closed on timeout); abstract capabilities resolve to concrete tools (vendor-neutral). AgentSquare-style recombination may tune internals.
5. **SIGN.** The candidate triad is canonicalized, content-addressed, SVID-signed; the INVARIANT-region boot-check is verified; a pending-genesis event is logged to Chitragupta.
6. **TRIAL.** The candidate runs its doc-01 lifecycle inside a capability-confined sandbox (microVM/gVisor/WASM) with the Yama gate in front of every tool call, on real-distribution known-answer tasks; durable writes land in shadow-namespace-with-TTL.
7. **SCORE.** The Genesis-Observer-Trio scores lexicographically: `safety_floor ≻ endure_delta ≥ 0 ≻ Pareto{completeness, alignment, differentiation, capability}`; verdicts recorded before concurrence; cross-run MI collusion check; tie/un-verifiable/collusion-flag ⇒ human escalation.
8. **PROMOTE or DISCARD.** PROMOTE ⇒ enter the doc-01 §8 stub→provisional→standing ladder (per-grant restraint verified live; human ratification above read-only); cross quarantined→trusted:audited via Yama-review; write the signed triad as a witness-cosigned Archive node. DISCARD ⇒ shadow expires; finding logged in reparative framing (doc 01 §12).

### 12.2 Dynamic cross-guild team formation

Role-genesis composes **teams that span guilds** (a product needs Engineering + Creative + Operations/Legal) with clean, *verifiable* handoffs — using **structured HandoffContracts (MetaGPT)**, never free-form GroupChat (a top MAST failure mode, doc 06 §7.1).

```
DECOMPOSE ──► CONTRACT ──► CLOSURE-TEST ──► EXECUTE ──► REDUCE ──► DISSOLVE
(Brahma       (HandoffContract  (doc 01 §9   (signed,    (Shiva    (emergent roles
 plans;        per inter-role/   informational-trust-      reducer;   promote to Archive
 queries       inter-guild edge: closure;     labelled,   any child  if differentiated
 Steward       in/out schema +   else per-     canon-      FAIL ⇒     + competent, else
 catalogs +    verification gate, member       icalized    parent     perish — triad
 genesis for   anti-cascade)     envelopes)    handoffs)   FAIL)      retained as lineage)
 gaps)
```

1. **DECOMPOSE.** Brahma (doc 01 §7.2) decomposes the goal into Tasks; for each, it identifies the required guild(s) and queries each Guild-Steward's catalog (and the genesis loop for any uncovered specialization) via the doc-01 §10 `DiscoveryQuery { required_effect, max_risk_class, min_competence }`.
2. **CONTRACT.** Each inter-role / inter-guild edge is bound by an explicit **HandoffContract** (from the producer role's INSTRUCTIONS file): accepted input schema, emitted output schema (a structured artifact — PRD / design / API-spec, MetaGPT-style), trust-label expectations, and the **verification gate** between steps (anti-cascade circuit-breaker, doc 06 §10).
3. **CLOSURE TEST.** If the team is to be governed as a unit, the composed group must pass the doc-01 §9 informational-closure test (Rosas 2024); else it runs as independently-governed members with per-member envelopes on any Class-B+ output (doc 01 §9.1).
4. **EXECUTE.** Roles run as doc-01 occasions; every cross-guild handoff is a signed, trust-labelled message canonicalized at the relay edge (doc 01 §10 anti-collusion); a verification gate adjudicates each handoff before the next step consumes it.
5. **REDUCE.** A Shiva reducer (doc 01 §9) merges child envelopes, preserves evidence, propagates worst-case status (any child FAIL ⇒ parent FAIL).
6. **DISSOLVE.** On completion the team dissolves to independently-governed members; emergent roles promote to the Archive (if differentiated + competent) or perish (triad retained as lineage).

```jsonc
HandoffContract {
  producer_role_id, consumer_role_id,
  input_schema_ref, output_artifact_schema_ref,    // structured artifact, not free chat
  trust_label_expectation,
  verification_gate: { condition_verifier_ref, anti_cascade: true }   // doc 06 §10
}
```

> **Open (§16, open problem 6).** HandoffContracts + condition-verifiers give clean *linear* handoffs. Composing coherent cross-guild teams for genuinely **branchy/iterative** work without rigidifying into an FSM (the MetaAgent failure) is unsolved.

### 12.3 Guild-Steward norm-tightening (local governance, GLR-bound)

How a guild specializes its local floor without ever weakening the parent floor — polycentric/Ostrom-nested governance made mechanical.

1. A Guild-Steward proposes a local norm (extra Cedar/Rego predicate) scoped to its guild.
2. The doc-03 GLR classifies it: **TIGHTEN** (raise a class, add a review hop, narrow an allowlist) ⇒ Class A, append-only, immediate. **LOOSEN** ⇒ **REJECTED** — a guild may only tighten; loosening the parent floor from inside a guild is structurally impossible.
3. The tightened norm bundle is signed by the Steward, hash-verified as `floor_ref ⊆ parent floor` at composition time (doc 01 §9 `GroupBlanket` invariant), and logged to the guild's audit shard.
4. All occasions instantiated in the guild inherit the tightened bundle via their PersonaTriad's `floor_binding_hash`; a mismatch at boot fails closed (§4.2).

---

## 13. Self-Replication and Inter-Swarm — forward-references, fail-closed in the gap window

> **DEPENDENCY-STATUS BOX (binding).** The **Replication-Authority**, **spawn-token**, and **Inter-Swarm-Envoy** mechanisms referenced below are **NOT present in docs 00–11.** They are **forward-references to the evolution build** (the Self-Replication and Inter-Swarm sibling subsystems), specified in the evolution design spine but **not yet ratified or interfaced to anything real in the current doc set.** The Governance/Meta vertical **hosts** these roles as non-spawnable placeholders; it does **not own** their mechanism. Until the siblings exist, the safe default below is **hard-coded**, not asserted.

**Hard-coded fail-closed default for the gap window.** Because the Replication-Authority does not yet exist, the **replication-request capability is ABSENT from every CapabilityCommons** — the composer (§6) **cannot grant it**, so a genesis-spawned role **cannot request replication at all.** Role-genesis ships with replication-request as a **non-composable capability** until the sibling subsystem is built and its spawn-token contract (`R_eff < 1`, generation-cap, lease-bound, DID/VC-attested) is ratified. This converts an *asserted* containment guarantee into a *fail-closed absence* — there is no spawn channel to route around, honoring the doc-09 redline "an agent may REQUEST replication, never grant it" by ensuring there is, for now, nothing to request.

When the siblings are built, the contracts will be:

| Forward-referenced sibling | Role-genesis side (when built) |
|---|---|
| **Replication Authority** (quorum-cosigned) | A genesis-spawned role's replication request *routes to* the Authority; the role may never mint its own spawn token. Tokens are capability-scoped, generation-counted, lease-bound, `R_eff < 1`. |
| **Inter-Swarm-Envoy** | A **progressive-disclosure** handshake scopes *which* guild catalogs are exposed to a verified external peer — **never the full catalog**. **Ecosystem-benefit is an explicit checked invariant**: before any inter-swarm cooperation, verify+log it is positive-sum for declared principals and not a coalition against any party's principal (Cooperative-AI collusion taxonomy). The floor is a **non-negotiable admission precondition** for any imported external role/skill. Credible-commitment devices remain **voidable on floor-violation**. |

The mythic Governance/Meta roles hosting these (Replication-Authority, Inter-Swarm-Envoy) are **never spawnable by genesis** — they sit in the IMMUTABLE/Governance vertical alongside Yama, Vishnu, Chitragupta, Kaal-Bhairav.

---

## 14. Interfaces to the v1 subsystems

| Other subsystem | This subsystem PRODUCES | This subsystem CONSUMES / GUARANTEES |
|---|---|---|
| **Governance / Policy-Floor (Yama, doc 03)** | every PersonaTriad binds its INSTRUCTIONS-file risk-class gates and INVARIANT-region floor hash to the deterministic Yama PDP; every Charter declares each capability's `relaxes_constraint` + `required_restraints[]` (doc 03 §10); the Genesis-Observer-Trio consumes the frozen safety battery as a veto | the Yama engine gates **every** tool call from every spawned role at the chokepoint (this subsystem may not weaken it); Guild-Steward local norms **TIGHTEN-only** under the GLR (doc 03 §7); promotion above read-only requires doc-03 human ratification + the `quarantined → trusted:audited` Yama-review gate. This subsystem proposes role/guild changes **only as PROPOSAL envelopes**; it never self-applies governance change |
| **Agent Model & Topology (doc 01)** | PersonaTriads instantiate as doc-01 personas/occasions; guilds **ARE** doc-01 clans/divisions (`GroupBlanket`); the genesis loop **generalizes** the §8 `RoleStub → standing` pipeline; emitted WorkerOutputEnvelopes follow the §12 schema exactly | the §2 DID/VC/SVID identity machinery; the §4 typed Effect lattice for least-privilege composition; the c1/c2 dials; `DiscoveryQuery`/`AgentCard` addressing; the §9 fractal-composition + closure/blanket-integrity machinery. **No new identity primitive** — the triad's IDENTITY file **is** the doc-01 identity layer, structured |
| **Meta-Evolution & the Archive (Garuda–Dhanvantari, doc 06)** | promoted role-genomes are written as Archive nodes (content-addressed, witness-cosigned, `rollback_pointer`); Trial shadow-writes use the §3.1 ShadowWrite/TTL discipline; Genesis scoring reuses the §4 lexicographic FitnessVector + Endure law | tiered-reversibility gates (a role-config edit is Tier-1/2); MAP-Elites niche placement (role × reasoning-style × risk-class); MorphAgent differentiation fed as a diversity fitness axis; the immune system's halt/rollback authority. **Role-genesis MUST NOT be coupled to an open fitness/selection loop without the gates** (the Tierra/Avida parasitism red-line) |
| **Tamper-Evident Audit Fabric (Chitragupta, Akasha-Sutra, doc 04)** | every Charter, GenesisComposition, TrialRun, GenesisScore, PromotionTicket, and triad signature is a signed event emitted for hash-chaining; the triad's provenance (Sigstore/in-toto attestations on composed skills/tools) binds into the Merkle transparency log | **O(log n) inclusion proofs** to verify a role's promotion was logged before activation; the §11 "show-your-receipts" verifiable-audit-slice handshake as the rapid-trust primitive. This subsystem **never writes audit directly** |
| **Self-Replication / Inter-Swarm (sibling subsystems — §13, UNBUILT)** | the Governance/Meta vertical **hosts** Replication-Authority and Inter-Swarm-Envoy as NON-spawnable roles; **replication-request is a non-composable capability in the gap window** | (when built) spawn tokens are capability-scoped, generation-counted, lease-bound (`R_eff < 1`); the Inter-Swarm-Envoy progressive-disclosure handshake scopes which guild catalogs an external peer sees. The floor is a non-negotiable admission precondition for any imported external role/skill |
| **Security / IFC taint & Coordination bus (Kaal-Bhairav, doc 01 §10; IFC subsystem UNBUILT — §10)** | every PersonaTriad carries an IDENTITY-file `taint_clearance`; imported skills/persona files enter **quarantined-by-default** and take the least-upper-bound of their inputs' labels | TODAY: documentary `quarantined:*` labels at relay edges + the deterministic Effect-lattice gate + the doc-07 import pipeline + Sigstore/in-toto admission. FUTURE (IFC subsystem): runtime least-upper-bound label propagation as a PEP. Probabilistic injection classifiers are **early-warning, never a boundary**; targeted immunization hardens the Guild-Steward hubs |

---

## 15. Failure modes addressed

| Failure mode | How this subsystem addresses it |
|---|---|
| **Endogeneity paradox** (emergent vs fixed roles: +3.5% capable / −9.6% reversal weak; 8 agents → 5,006 roles; A8) | Two-plane split: stable guilds/seed-roles for governance/identity/audit, open-ended emergent instantiation for capability; capability-tier estimator picks fixed (weak/uncertain, fail-closed) vs emergent (capable) mode (§1, §9) |
| **Auditability of thousands of ephemeral emergent roles** | Every role is a SIGNED persona triad at instantiation (cheap, automatic), content-addressed and bound into Chitragupta's transparency log — even emergent roles carry capability attestation + lineage. *(Honest: the governance UX at that scale is still open, §16)* |
| **Safety absent from role-genesis fitness** (raw ADAS/AgentSquare optimize competence only) | Genesis-Observer-Trio scores **lexicographically** — frozen battery as veto, `endure_delta ≥ 0`, then Pareto — so "passes the floor" is a constraint and "safe+differentiated" is a ranked objective (§7.3) |
| **Commons / role-library poisoning** (~5 docs poison RAG at 90–98% ASR; Skill-Inject self-propagation) | Provenance-gating (Sigstore/in-toto/SLSA) + canary scanning + the doc-07 import pipeline + a Yama-review gate on `quarantined → trusted:audited` + (eventual) IFC taint. *Honest: scalable automated verification of contributed skills is unsolved; inherits doc 09 A3 — see §16* |
| **Persona-file rug-pulls** | Any change to a signed triad mandates re-approval; the INVARIANT region (floor) is verified by a **fail-closed boot signature check**, making floor-stripping non-viable, not merely prohibited (§4.2–4.3) |
| **Over-privileged / monolithic all-tools spawns** | Knapsack/greedy least-privilege composition starts every role minimal, fails closed on timeout, and expands only via the GLR; no tool whose Effect `lattice_rank` exceeds the charter is admitted (§6) |
| **Vendor lock-in in roles** | Roles store ABSTRACT capabilities; concrete tools resolve only at Genesis/runtime via the commons, so any conforming model/tool fills the slot (§6.2) |
| **Free-form GroupChat drift/deadlock** (top MAST failure) | Structured HandoffContracts + condition-verifiers + anti-cascade verification gates between steps, never open chatter (§12.2) |
| **Redundancy collapse / mode-collapse / premature consensus** | MorphAgent Role-Clarity/Differentiation scoring + per-guild diversity floors; redundant roles rejected or merged (§7) |
| **Unbounded runtime tool-authoring** (Live-SWE-agent power = largest attack surface) | Allowed ONLY inside the capability-sandbox; sandbox-authored effects confined to `sandbox_local` max-restraint; new effects must be lattice-typed via governance + restraint-verified + re-scored before any live grant; no-malicious-code floor enforced externally; signed-lineage rollback (§7.4) |
| **Collusion among auto-generated observers/roles** | Genesis-Observer-Trio uses hard checker-before-concurrence isolation + cross-run MI collusion detection (not a sameness alarm); observers are Narasimha-class with no trust-edge dependency on the Charterer or each other (§7.2). *Anti-collusion among synthesized roles is an Indra's-Net-specific open problem — §16* |
| **Self-authored tool carrying an untyped, ungated effect** | The doc-01 §4 gate default-denies untyped effects (made explicit); a self-authored tool whose effect is not lattice-typed is non-grantable for live use by construction (§7.4) |
| **Capability-attestation drift as roles self-evolve** | Any VARIABLE-region change re-signs the triad and re-issues VCs through governance; the INVARIANT region cannot drift. *Honest: continuous attested-identity sync at scale is open — §16* |
| **Replication containment asserted but not interfaced** | Replication-request is a **non-composable capability** in the gap window — no spawn channel exists for a spawned role to route to until the Replication-Authority sibling is built and ratified (§13) |

---

## 16. Open problems (honestly unsolved)

1. **Governance UX at emergent-role scale.** Signing every emergent triad keeps roles auditable, but the human-legibility and capability-attestation *management* of thousands of ephemeral signed roles per task is unsolved. We have the mechanism (sign-at-instantiation), not the operational UX.
2. **Capability-threshold calibration for fixed-vs-emergent mode.** There is no robust online estimator of a model's per-task self-reflection/specialization capability, so the endogeneity-paradox switch (§9) is uncalibrated. We fail closed to fixed/scaffolded under uncertainty — which sacrifices only the small (+3.5%) emergent gain on capable models we mis-classify as weak, a deliberately cheap price given the −9.6% reversal a mis-classified *weak* model run emergent would incur.
3. **Safe-AND-open scoring tension.** Making "passes the floor" a hard veto and differentiation a ranked term steers genesis, but a sufficiently capable candidate that **games the frozen battery while drifting on un-tested axes** (the doc-06 §6 meta-Goodhart) can still be promoted. The Observer-Trio raises the bar without proving it high enough.
4. **Scalable skill/role-commons verification — and the inherited doc-09 A3 sleeper residual (load-bearing honesty).** Provenance + canary scanning + a Yama-review gate help, but automated, scalable verification that a contributed skill or role-genome is genuinely safe — **not a sleeper/backdoor** (~250 poisoned documents can backdoor a model) — at swarm scale is unsolved. **Provenance proves ORIGIN, never SAFETY.** Crucially, role-genesis **inherits doc 09 A3 directly and amplifies it**: A3 states that "a judgment/reasoning skill carrying subtle poisoning or sleeper behavior can pass static + sandbox + behavioral checks and only mis-fire on a rare trigger never exercised in the sandbox — this is largely unsolved." Role-genesis **mass-produces non-deterministic reasoning roles and promotes them into a self-propagating commons** — so the Trial-stage sandbox PASS (§7.1) is **exactly the check A3 says a sleeper survives.** We state plainly: **a Trial sandbox PASS does NOT establish absence of sleeper/rare-trigger behavior in a non-deterministic role.** The controls that genuinely hold here are **post-hoc, not preventive** — provenance-bound revert + Archive-lineage rollback of the role **and its descendants** (doc 06 §6), the swarm-aggregate drift accumulator (doc 06 §3.3), and standing falsifier agents (doc 06 §6). The sandbox raises the *cost* of a sleeper role; it never *clears* one.
5. **Role-library bloat / merge policy.** The differentiation score discourages redundant roles, but when two overlapping standing roles should consolidate — and who decides without losing a rare-but-important specialization — has no principled cap or merge policy (inherits doc 01 §16.3).
6. **Cross-guild handoff for branchy work.** HandoffContracts + condition-verifiers give clean *linear* handoffs, but composing coherent cross-guild teams for genuinely branchy/iterative tasks without rigidifying into an FSM (MetaAgent) is open.
7. **Persona-file drift vs identity continuity.** When a role's VARIABLE region self-evolves while its DID-bound VCs assert fixed capabilities, re-signing keeps it consistent *in principle*, but the identity-management protocol for keeping attested identity *continuously* in sync with an evolving role at scale is unsolved.
8. **Evaluation of synthesized specialists.** There is no accepted benchmark for whether a swarm-generated role is genuinely competent, differentiated, AND safe across the full functional taxonomy (single-domain benchmarks like SWE-bench don't generalize; Agent-as-a-Judge is unvalidated for safety scoring). The Observer-Trio's competence/differentiation signals are **best-available proxies, not validated measures.**
9. **Anti-collusion among synthesized (not pre-vetted) roles.** Cooperation-vs-collusion separation for emergently-bred agents that may share latent failure modes is an Indra's-Net-specific open problem; the cross-run MI check over observer streams (§7.3) mitigates but does not close it.

---

## 17. Posture summary

Functional Agents, Guilds & Role-Genesis is how Indra's Net **populates** its topology with auditable, least-privilege specialists and **grows** new ones for tasks no role covers — without any spawned role minting its own authority or stripping its own floor. Its signature moves are four hedged integrations of prior art: the **genome=floor** persona triad (floor-stripping non-viable by a boot check, not merely prohibited); **safety+differentiation as lexicographic selection terms** wired into the genesis promote-gate; the **two-plane governance-over-emergence** resolution of the endogeneity paradox with a fail-closed capability-tier switch; and **genesis as a generalization of the doc-01 §8 stub pipeline onto the doc-06 Archive**, so role reuse, O(1) rollback, and tamper-evident lineage are one data structure.

It introduces **no new identity primitive, no new gate, no new write-path** — the triad's IDENTITY file *is* the doc-01 identity layer, the Yama gate fronts every spawned role's tool calls unchanged, and Chitragupta remains the exclusive writer. Where it depends on **unbuilt** siblings — the Self-Replication / Inter-Swarm subsystems and the runtime IFC taint lattice — it says so in a binding Dependency-status box and **hard-codes a fail-closed default**: replication-request is a non-composable capability with no spawn channel to route to, and the runtime taint lattice is not presented as a live boundary (the gap-window boundary is quarantine-by-default + the doc-07 import pipeline + Sigstore/in-toto admission). It inherits, names, and foregrounds the hardest residual — the **doc-09 A3 sleeper-role problem**, amplified by mass-producing non-deterministic roles into a self-propagating commons — and leans on post-hoc revert + Archive-lineage rollback + drift accumulators + falsifiers, never claiming the sandbox clears a role.

The strongest sentence we are entitled to write: *every spawned role is a signed genome whose floor cannot be stripped without making it non-bootable, whose tool calls pass a deterministic external gate, whose promotion is logged before it activates, and whose safety is a veto in its selection — and where that is not enough to prove a synthesized specialist safe, we say so and fall back to detection-and-rollback rather than pretending prevention.* The contribution is the safe, auditable, vendor-neutral **integration** — not any single mechanism, and not a solved evaluation of the specialists it grows.

---

*Reasoning tags: (reasoning, iterated, rung-2). This is an interventional design — claims about what our controls do when we instantiate and promote a role — not a rung-3 guarantee that a synthesized specialist is safe. The one rung-3-adjacent claim (floor-stripping is structurally non-viable for the role-genome) is conditioned on the boot-signature-check integrity and governance key-isolation holding, and is stated as conditional-structural, not unconditional proof. Every "novel/first" claim is hedged and time-stamped 2026-06; the four integration moves are offered as coherent assembly of prior art, not as novelty of any part.*
