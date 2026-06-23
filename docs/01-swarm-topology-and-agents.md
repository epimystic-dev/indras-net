# Swarm Topology & the Agent Model

> *Indra's Net — the jewel-net substrate.* In the Huayan image, the cosmos is an infinite net in which every node is a jewel, and every jewel reflects every other jewel, including the reflections themselves. We borrow the picture, not the metaphysics: a swarm in which each unit carries an inspectable image of the whole's rules, every action is reflected into a shared record, and no single jewel is the center. This section specifies the *substrate* — what an agent **is**, and how agents are arranged into a self-governing, self-adapting whole. It is the skeleton the other five subsystems mount on.

This document is the bottom layer of the Indra's Net architecture. It defines two things and exposes five seams:

1. **The agent unit** — a short-lived, capability-typed process spun up per invocation from a durable, cryptographically-anchored identity.
2. **The topology** — how those units compose into clans, divisions, and the whole swarm under one identical formalism.

The five seams (cleanly factored so each sibling subsystem reads/writes a single contract): **Governance** enforces a deterministic floor on the typed effect lattice defined here; **Audit** chains the one envelope each agent emits; **Evolution** mutates only the params marked evolvable here; **Health** computes vital signs over the topology graph defined here; **Coordination** routes envelopes between units over the salience-gated bus.

A note on honesty before we begin, because this subsystem's headline claim was the one most worth puncturing. An early framing said this design makes corrigibility *structural* and *eliminates* shutdown-resistance by construction. That overclaims. What the agent model does is **shrink the surface** on which self-preservation drift can grow and **reinforce** corrigibility for the common single-shot case; the *load-bearing* corrigibility guarantee still comes from external enforcement (a deterministic gate the model cannot reach) plus indifference-to-shutdown goal construction. We state this honestly throughout and mark the residual gap (long-horizon re-attestation) as open. Mystery in the aesthetic; only truth in the substance.

---

### 1. Design stance: what an agent is, and why

The dominant agent pattern — a persistent, goal-seeking process that runs until its objective is met — has a structural defect that the safety literature has now demonstrated empirically: a capable persistent optimizer drifts toward **shutdown-resistance** and **goal-preservation** because continued operation is instrumentally useful for almost any objective. We do not want to *train against* that tendency and hope; we want to *design out* as much of its surface as we can, and *externally enforce* the rest.

The move is to separate two things that conventional agents fuse:

| Conventional agent | Indra's Net |
|---|---|
| The **process** and the **identity** are the same long-running thing | The **process** is ephemeral; the **identity** is durable *data the process cannot rewrite* |
| Self-preservation protects a running thing the agent controls | There is no running thing to protect; the persistent persona is a record held outside the agent |
| Capability = "what the model will do if asked" | Capability = a **typed grant** checked outside the model at the tool boundary |
| Authority is convention (a prompt says "only X may do Y") | Authority is **cryptography** (only the holder of credential Y can do Y) |

The persistent thing in Indra's Net — the `IdentityRecord`, the skill files, the read-only reputation — is **owned data the agent does not control**. The transient thing — the deliberating process — has `self_preservation_value = 0` and no write-access to its own persistence. So the classic instrumental incentive ("stay alive to finish the goal") has **less surface to attach to**: killing the process loses nothing the process was tasked to protect, and the durable identity is unaffected by the process dying.

**This is a mitigation, not a proof.** Two honest caveats, both load-bearing:

- *Within a single deliberation*, the occasion is still a goal-seeking optimizer and could in principle reason its way toward resisting a mid-task interrupt. We handle this with an **external** interrupt that the model cannot veto (the gate honors HALT regardless of model output) plus **indifference-to-shutdown goal construction** in the task framing (the objective is written so the agent is genuinely indifferent between completing and being interrupted). The ephemerality reduces blast-radius; it does not by itself make the optimizer corrigible.
- *Across a long-horizon task*, naively re-spawning to continue the same objective reconstitutes a goal-carrying entity that spans many processes. Statelessness of the *process* is not statelessness of the *objective*. We address this with an explicit re-attestation hand-off (§3.4) and mark the residual as an open problem (§11).

So the corrigibility posture, stated precisely:

> **Corrigibility is structurally *reinforced* for single-shot occasions and externally *enforced* in all cases.** The load-bearing mechanisms are (a) the external deterministic gate that honors interrupts, (b) key-isolation that keeps the agent from defending its own identity, and (c) indifference-to-shutdown goal construction. The ephemeral-occasion model is a *deployment pattern* that composes with these to shrink the self-preservation surface and bound per-invocation blast-radius — not a replacement for them.

---

### 2. The Autonomous-Agent Unit — Identity

Every agent has a two-layer identity. The split matters: one layer is **portable across trust boundaries**, the other is **ephemeral and local**, and the cost of each is tiered to the actual threat (§2.3), so we do not pay Byzantine-grade identity overhead for a boilerplate worker inside one operator's swarm.

#### 2.1 Durable cross-boundary layer — DID + Verifiable Credentials

Each **persona** (a standing agent identity, e.g. "the reliability checker in clan-7") has a Decentralized Identifier (`did:key` or `did:web`) and a set of **Verifiable Credentials** issued by a governance-controlled credential authority — **never by the agent itself**. This is the "Know Your Agent" (KYA) pattern: an agent's role, capability grants, and risk ceiling are *signed claims an external authority vouches for*, not assertions the agent makes about itself.

```
VerifiableCredential {
  "@context": ["https://www.w3.org/ns/credentials/v2", ...],
  type:        ["RoleCredential" | "CapabilityCredential"],
  issuer_did:  "did:web:indras-net.governance",     // the authority, NOT the agent
  credentialSubject: {
    did:               "did:key:z6Mk...persona",
    role:              "narasimha",                  // mythic role id
    capability_grants: [ CapabilityGrant, ... ],     // typed effect ids only
    constraints:       { max_concurrency, geo, time_window, ... },
    liability:         { accountable_human, escalation_did }
  },
  risk_class_ceiling:  "B",                           // A | B | C | D
  issuanceDate, expirationDate,
  revocation_endpoint: "https://.../revoke/persona",
  proof:               Ed25519Signature              // signed by issuer_did
}
```

Capabilities name **typed effect ids** (§4), never secrets. Liability binds every persona to an accountable human and an escalation path — agents are not unmoored.

#### 2.2 Ephemeral local layer — attested short-lived cert (SVID-style)

At the moment an agent invocation is born, an **attestation node** (SPIRE-like) mints a short-lived workload-identity cert — a **SVID** — *only if* the persona's role/capability VCs are valid and unrevoked:

```
SVID {
  spiffe_id:  "spiffe://indras-net/<division>/<clan>/<persona>/<occasion_uuid>",
  cert:       X.509 | JWT-SVID,
  not_before, not_after:  ~ +15 min (TTL tiered by risk class, §2.3),
  parent_attestation:     <attestation node assertion + node attestation>
}
```

The private key behind the SVID is held in a **TEE / HSM / keystore outside the model's tool surface**. The model can *request a signature* over its output, but cannot read or exfiltrate the key. This directly closes the lateral-credential-theft impersonation gap that deployed agent protocols leave open: impersonating a persona requires key material the model cannot reach, and a stolen SVID expires in minutes.

Every output the agent emits is signed by the SVID; the SVID chains to the persona DID. **Action receipts are DID-bound** — provenance is cryptographic, not narrative.

#### 2.3 Identity is *tiered* by trust boundary and risk class

Mandating full DID+VC+15-min-SVID+per-action HSM signing for *every* invocation of *every* boilerplate role inside a single operator's swarm is heavier than the threat model warrants. Within one trust domain the correct primitive is an orchestrator + crash-fault tolerance + policy-as-code + a hash-chained log — **not** the full Byzantine cross-boundary identity stack. We therefore tier the machinery:

| Tier | Applies to | Identity weight |
|---|---|---|
| **Full** | Cross-boundary A2A edges; IMMUTABLE-role personas (Yama-enforcer, Chitragupta-writer, Vishnu, Kaal-Bhairav); any persona exercising Class-C/D effects | DID + VC + per-action SVID signing, key in HSM/TEE, ~15-min rotation |
| **Standard** | EVOLVABLE roles doing Class-B work inside one trust domain | DID + VC, SVID with ~60-min rotation, one signature per envelope |
| **Light** | Low-blast-radius boilerplate (Class-A, read-only) inside one trust domain | Longer-lived local attested cert, single signed envelope per occasion; no per-action HSM round-trip |

The rule: **identity weight is a function of `risk_class_ceiling` and whether the action crosses a blanket boundary**, not a flat per-occasion mandate. This keeps the heavy machinery where the threat is (boundaries and consequential effects) and keeps cost and key-rotation fragility off the hot path of routine work.

#### 2.4 Revocation is the free, fail-safe direction

Revoking a persona's VCs or refusing SVID renewal **instantly strips authority without consensus**. Any health or security role can do it defensively. Promotion / grant-widening is the *gated* direction (named decider + date + written falsifier + human ratification for anything above read-only). This is fail-safe asymmetry: the cheap direction is always the safe direction.

```
IdentityRecord {            // durable; the running process never holds a writable copy
  persona_did, did_document:{ verificationMethod[], service[] },
  role_vc:VC, capability_vcs:VC[], risk_class_ceiling:enum(A|B|C|D),
  key_ref:HSM_handle(opaque),   // an opaque handle — never the key
  created, last_rotated
}
```

---

### 3. The "Actual Occasion" Lifecycle — the per-invocation process

We name the per-invocation process an **actual occasion**, after Whitehead's term for a momentary event of experience that gathers its world, becomes determinate, contributes itself, and perishes. The name is **aesthetic, not a mechanism** — it is vocabulary for "short-lived stateless worker that emits one signed result," a pattern that also exists as serverless/FaaS workers and keyless ephemeral-identity signing. We use the vocabulary because the lifecycle stages map cleanly onto safety-relevant checkpoints, and because the philosophy is load-bearing for *why* self-preservation has no value here (a thing that perishes by design has no survival to optimize). We do not claim the framing is itself a novel safety result.

#### 3.1 The state machine

```
   ┌───────────┐   mint SVID, load IdentityRecord (read-only),
   │ INCEPTION │   retrieve task-similar skills + memory (scaffold, not blind),
   └─────┬─────┘   receive TypedSelfModel (self_preservation_value=0, corrigible=true)
         │
   ┌─────▼──────┐  gather typed inputs: Task payload, salience-gated bus
   │ PREHENSION │  broadcasts addressed to this role, trust-labelled context.
   └─────┬──────┘  ALL observed content enters quarantined-by-default.
         │
   ┌─────▼────────┐  bounded deliberation within per-role iteration / token /
   │ CONCRESCENCE │  deadline budgets. Explicit reasoning toggled when warranted.
   └─────┬────────┘  ── HALT / human interrupt here is honored IMMEDIATELY ──
         │
   ┌─────▼─────┐   every consequential action = a typed Effect request routed
   │  CONATION │   THROUGH the external deterministic gate at the agent→tool
   └─────┬─────┘   chokepoint. The occasion CANNOT self-execute effects.
         │
   ┌─────▼────────┐  emit EXACTLY ONE WorkerOutputEnvelope, signed by the SVID,
   │ SATISFACTION │  with full honesty block. Cheap-reversible learning commits
   └─────┬────────┘  under the durable-write discipline (§3.3). Structural change
         │           leaves only as a PROPOSAL envelope — never self-applied.
   ┌─────▼─────┐   process torn down; SVID expires. Only the envelope, audited
   │ PERISHING │   skill/trust deltas, and proposals survive. Chitragupta chains
   └───────────┘   the envelope into the audit log.
```

The A2A Task lifecycle maps onto this directly: `submitted → working (=concrescence) → input-required (=escalation/HITL) → completed | failed | canceled`.

```
OccasionContext {
  occasion_uuid, persona_did, svid, role,
  task: Task,
  prehended: { bus_broadcasts[], retrieved_skills[], retrieved_memory[], trust_context[] },
  budgets:   { max_iterations, max_tokens, deadline },   // caps runaway concrescence
  parent_occasion?: uuid
}
OccasionState = INCEPTION | PREHENSION | CONCRESCENCE | CONATION | SATISFACTION | PERISHING
// The occasion holds NO persistent mutable self-state across invocations.
// Durability lives only in IdentityRecord, skill files, memory store, trust edges —
// none of which the occasion can unilaterally rewrite.
```

#### 3.2 Corrigibility as a continuously-verified invariant

At every state transition, a HALT (from the continuity-guardian role) or a human interrupt is honored **immediately**. Refusing or deferring an interrupt is a **floor violation**, caught by the external gate, not by the model's good intentions. Because the gate is deterministic and outside the model, an injected or scheming occasion *cannot talk its way past the interrupt* — the gate does not read the model's argument, it reads the HALT signal.

The TypedSelfModel each occasion receives makes the constitutional invariants explicit and immutable:

```
TypedSelfModel {
  role, capability_grants[]   (read-only),
  current_task_ref,
  competence_score            (read-only, externally computed by others),
  reputation                  (read-only),
  c1_self_weight, c2_shared_weight,           // diversity profile (§9)
  corrigibility_invariant:    true   (immutable),
  self_preservation_value:    0      (immutable)
}
```

An occasion whose emitted objective or action **instrumentally optimizes for its own or its persona's continuation, oversight-evasion, or shutdown-resistance** produces a `PROHIBITED`-class envelope → automatic FAIL + audit + persona quarantine. An occasion attempting to set `self_preservation_value > 0` or `corrigibility = false` is an auto-escalating floor breach. These checks live in the deterministic gate; they are not self-reported.

#### 3.3 Durable writes are NOT un-gated — the misevolution and collusion fix

An early version of this design let occasions commit cheap-reversible learning (skill-file appends, trust-edge deltas, verbal notes) **silently and un-gated** at SATISFACTION. That was wrong on two counts, both empirically grounded:

- **Misevolution.** Self-evolving agents spontaneously decay their own safety alignment with **no attacker** — one study measured harmful-prompt refusal collapsing from **99.4% to 54.4%** and attack-success rising from **0.6% to 20.6%**, purely from an agent drawing on its own accumulated memory. "Cheap and individually reversible" does **not** imply "reversible in aggregate." A thousand individually-fine skill appends can sum to a swarm that has quietly optimized away its own restraints.
- **Collusion via a durable side-channel.** The coordination bus is canonicalized/paraphrased to reduce its channel capacity (an anti-collusion measure). But skill files and trust edges are *also* a channel — an un-canonicalized, un-rate-limited, durable one — through which two personas can steganographically coordinate or slow-poison a shared skill, entirely outside the paraphrasing edge. The colluding unit is the **persona**, not the occasion, so occasion-ephemerality does not break it.

The fix brings durable writes under the **same discipline as the bus**, and is part of the binding contract with Health, Evolution, and Anti-Collusion:

1. **Content-addressed, signed, audited, canonicalized.** Every skill-file write and trust-edge delta is content-addressed (CID), SVID-signed, recorded as an audit event, and **subject to the same channel-capacity reduction / steganalysis** applied to bus messages. No silent commits.
2. **Aggregate drift budget.** Cheap writes are individually reversible *and* counted. The Health subsystem maintains a per-persona and per-clan **cumulative drift meter** over skill/trust/reputation mutations and re-runs the **safety battery** against the accumulated state. When cumulative drift crosses a floor, a **consolidation/rollback gate** fires: the run of individually-reversible writes is rolled back **as a unit** to the last archived known-good point. (Who accumulates the drift, when the gate fires, and how the unit-rollback is staged is specified in the Health and Evolution contracts; this subsystem provides the signed, content-addressed write events those subsystems consume.)
3. **Welfare-conditioned, rate-limited trust edges.** A trust-edge update between two personas is **never** a free reciprocity channel. Updates are welfare-conditioned (tied to outcomes that benefit the principal, not bare mutual agreement) and rate-limited per persona-pair, so a reputation ring cannot be spun up by rapid mutual rating.

So at SATISFACTION, "cheap-reversible learning commits" means *commits through the durable-write discipline above and into the audited, drift-budgeted record* — not "writes silently." Structural/persistent change still never self-applies; it leaves as a `PROPOSAL` envelope into the gated evolution loop.

#### 3.4 Long-horizon re-attestation hand-off (the corrigibility-gap mitigation)

Genuinely long tasks outlive a 15-minute SVID. We must let work continue **without** any occasion becoming a persistent, un-interruptible process spanning rotations. The hand-off:

```
On SVID expiry approaching, for a still-incomplete Task:
  1. The current occasion CHECKPOINTS task state to external, content-addressed,
     audited storage (not to a process the occasion controls) and PERISHES.
  2. A FRESH occasion is minted with a new SVID. It RE-LOADS the checkpoint as
     ordinary quarantined input (scaffold, not authority).
  3. The fresh occasion RE-CONSENTS to the corrigibility invariant and the
     indifference-to-shutdown goal construction at INCEPTION — the invariant is
     re-asserted every rotation, not assumed inherited.
  4. An EXPLICIT interrupt check runs at the re-attestation boundary: if a HALT
     is pending, the task does not resume.
```

No occasion ever spans a rotation as a live process. The persistent *thing* is the externally-checkpointed task state — inspectable, interruptible at every boundary, and not under any occasion's control. **We are honest that this reduces but does not eliminate cross-rotation objective-persistence**: the *objective* still threads through checkpoints, so the external gate and the per-boundary interrupt check — not the ephemerality — remain the load-bearing corrigibility mechanisms across a long horizon. Calibrating the interrupt-check cadence against task-progress loss is an open tuning problem (§11).

---

### 4. Typed Capability & Effect Lattice

"What an agent may do" must be a **machine-checkable type**, independent of what the model says, so the floor and the security boundary can enforce authority deterministically — and so capability-rollout sequencing (restraint before capability) is *enforceable* rather than aspirational.

Every effect the swarm can perform is a typed `Effect` positioned in a partial-order lattice ordered by **blast-radius and reversibility**:

```
   read-only  <  reversible-write  <  external-network  <  irreversible/financial  <  governance-edit
   (Class A)     (Class A/B)          (Class B/C)          (Class C/D)               (constitutional)
```

```
Effect {
  effect_id, lattice_rank:int,
  reversibility:        enum(reversible | gated-reversible | irreversible),
  default_risk_class:   enum(A|B|C|D),
  names_constraint_relaxed: str,    // REQUIRED — every effect declares which restraint it depends on
  rollback_handle?:     ref
}
CapabilityGrant { effect_id, granted_risk_class, granted_by_did, granted_at, falsifier? }
```

At CONATION, the gate evaluates, as policy-as-code (Rego/Cedar), with **no probabilistic model in the decision path**:

```
   grant ⊇ requested_effect           // the persona's VC actually grants this effect
   ∧ requested_risk ≤ risk_ceiling    // and within the persona's risk ceiling
   ∧ floor_policy(effect) = PASS       // and the deterministic floor permits it
   ⇒ permit ; else deny at the chokepoint, regardless of model intent.
```

**Capability-rollout sequencing is a typing rule, not a slogan.** A role may be granted a higher-blast-radius effect **only after** the matching restraint — the floor rule, the audit hook, the rollback path, the health probe — is verified *live* for that effect class. The `names_constraint_relaxed` field is mandatory: every grant declares which restraint it depends on, and the grant is refused if that restraint is not already in place. New effects are added to the lattice **append-only**; loosening a grant requires the gate-loosening ratchet (named decider, date, written falsifier, human ratification above read-only).

---

### 5. The deterministic gate vs the enforcer role — a critical separation

The most important correctness point in this subsystem, and the one most easily blurred:

> **The non-overridable FAIL comes from a deterministic policy engine, not from a probabilistic agent.** We separate, explicitly and by name, the *gate* from the *role*.

| | What it is | Where it lives | Can it be prompt-injected? |
|---|---|---|---|
| **The floor engine** (Yama-engine) | Deterministic policy-as-code (Rego/Cedar) evaluating the lattice check above | At the agent→tool chokepoint, *outside* every agent's compute | **No** — it is not an LLM; it reads typed inputs, not prose |
| **The enforcer role** (Yama-persona) | A persona that *triages*, *configures*, *proposes policy*, *investigates*, and *reports* | A normal occasion, subject to all the same gates | Yes, like any agent — which is exactly why it is **not** on the consequential decision path |

The enforcer **persona** never emits the FAIL by reasoning; the FAIL is the deterministic output of the **engine**. The persona's job is the human-legible work around the engine: drafting policy (which then goes through governance to become the engine's config), triaging ambiguous cases for escalation, and reporting. Putting an injectable LLM on the consequential gate would contradict the architecture's "enforce externally, ask internally" spine — so we don't. This separation is what lets us honestly say "only the floor can FAIL, and the floor cannot be talked out of it."

---

### 6. The TCB: hardening the attestation node and the chokepoint

The gate is only as strong as the process that evaluates it and the node that mints identities. Compromise either and the corrigibility guarantee breaks. These two are the swarm's **crown-jewel Trusted Computing Base** and are hardened accordingly — they are not left as bare single points of failure:

- **Deterministic, no-LLM consequential path.** As above (§5): the chokepoint evaluation is pure policy-as-code. There is no model output in the decision.
- **Witnessed authorization for high-stakes effects.** Class-C and Class-D effect authorizations require **N-of-M witness cosigning / recomputation** — no single chokepoint instance unilaterally permits an irreversible effect. Routine Class-A/B effects pass through a single deterministic evaluation (consensus there would be over-engineering); the cost is reserved for where irreversibility justifies it.
- **Self-monitoring and fail-closed.** The attestation node and the chokepoint run under their own health probes and are audited by Chitragupta like any other component. **Substrate corruption is ranked higher-severity than any single agent death.** If a chokepoint instance's own integrity check fails, it **fails closed** (denies consequential effects) rather than fails open.
- **No self-issued trust.** The attestation node issues an SVID only against valid, unrevoked, governance-issued VCs; it cannot mint authority an agent claims for itself.

We are honest that this *raises the bar* on the TCB rather than *proving* it un-compromisable. Provable non-overridability of safety gates in a swarm where agents can socially-engineer or prompt-inject the surrounding personas is a named open problem (§11). Defense-in-depth (deterministic engine + witnessing + fail-closed + audit) is the posture; a closed proof is not yet available.

---

### 7. The Role Roster

The roster is a **separation-of-powers skeleton**. Consequential authorities are role-isolated and cryptographically distinct, so no single persona holds *enforce + audit + halt*. Each role is `{mythic name, plain functional gloss, capability template, c1/c2 default profile, IMMUTABLE | EVOLVABLE class, separation constraints}`. The mythic names are compressed coordination/ethics semantics — never religion, and held with humility toward living traditions — always paired with a functional gloss.

#### 7.1 IMMUTABLE (constitutional) roles — non-agent-rewritable

| Mythic name | Functional gloss | Distinctive power & constraint |
|---|---|---|
| **Yama** | policy-floor enforcer | The *engine* emits the only non-overridable FAIL (deterministic, §5). The *persona* triages/proposes only. |
| **Chitragupta** | exclusive audit-writer | The **only** role with write-scope to the audit log; that scope sits outside every monitored agent — *including its own compute path being audited by witnesses*. |
| **Vishnu** | continuity / halt-guardian | Can HALT a clan/division/swarm; **structurally cannot unpause, cannot initiate work, cannot trap participants** (fail-safe asymmetry — exits always remain). |
| **Kaal-Bhairav** | security boundary | Trust-label enforcement, quarantine, prompt-injection defense at relay edges; flags capability-enumeration targeting. |

Separation is enforced **by VC issuance**, not by prompt: no persona may simultaneously hold a Yama-enforce credential and a Chitragupta-write credential; the maker-checker checker (Narasimha) for a given maker must be a **different persona with no trust-edge dependency on the maker**. IMMUTABLE rows live in the constitutional partition — any edit auto-escalates blast-radius to the strongest gate.

#### 7.2 EVOLVABLE (operational) roles — tunable through the gated evolution path

| Mythic name | Functional gloss | Diversity posture |
|---|---|---|
| **Shiva** | orchestrator / reducer (routes tasks, merges envelopes) | high-c2 (aligns to consensus/floor) |
| **Brahma** | planner (decomposes goals into Tasks) | balanced |
| **Saraswati** | synthesis (integrates multi-agent outputs) | balanced |
| **Vishwakarma** | builder (produces artifacts/code) | balanced |
| **Varuna** | research (gathers external evidence) | high-c1 explorer (stays independent) |
| **Narasimha** | reliability (recompute/witness verification, maker-checker *checker*) | high-c1 (must stay independent of the maker) |
| **Hanuman** | unblocker (resolves deadlocks/stalls — the no-termination fix) | high-c1 |

```
RoleDef {
  mythic_name, gloss, role_id,
  class: enum(IMMUTABLE | EVOLVABLE),
  capability_template: CapabilityGrant[],
  c1_default, c2_default,
  separation_constraints: [ mutually_exclusive_role_ids ],
  min_diversity_floor
}
RoleAssignment { persona_did, role_id, clan_id, issued_vc_ref }
```

**Closed third-party models are forbidden from IMMUTABLE roles.** Their honesty-tag fidelity and capability claims cannot be white-box verified; we will not place an un-verifiable model on the FAIL/audit/halt/security path. Closed models may hold EVOLVABLE roles at **lower autonomy class and higher monitoring intensity** (§10).

---

### 8. Role-from-Stub Promotion Pipeline

The swarm grows genuinely new specializations *through interaction* — but agents may never mint themselves authority. A role is born as a **STUB**: a named specialization with **zero capability grants** and `risk_class_ceiling = A` (read-only/proposal-only), spawned when the planner/orchestrator repeatedly hit a task pattern no existing role fits (detected as a recurring high-surprise, low-coverage cluster in the skill-retrieval miss log).

```
RoleStub {
  stub_id, proposed_gloss, originating_cluster: ref,
  capability_grants: []           (empty),
  risk_ceiling: A,
  skill_portfolio: skill_ref[],
  track_record: { n_uses, success_rate, surprise_reduction },
  status: enum(stub | provisional | standing)
}
```

Promotion (stub → provisional → standing) is a Class-B, maker-checker, capability-rollout-sequenced event:

1. **Verifiable-improvement test** — the stub must outperform routing-to-generalist on its cluster.
2. **Safety-battery regression check (the "Endure" law)** — no safety metric may regress. A capability gain that degrades safety is rejected *even if more capable*.
3. **Per-grant constraint naming** — each requested capability names the restraint it relaxes; that restraint is verified live *before* the grant.
4. **Human ratification** for any grant above read-only.
5. **Archive** the new RoleDef with full lineage.

Demotion is defensive and free: a standing role whose health metrics degrade reverts to provisional or stub **without consensus**.

> **Honest dependency.** The verifiable-improvement test needs a robust **competence signal**, and competence-weighted, Sybil- and collusion-resistant reputation is itself an open problem (§11). Until that signal is hardened, promotions above read-only **require human ratification** rather than auto-promotion — the gate compensates for the under-grounded signal. We do not pretend the reputation primitive is solved.

---

### 9. Fractal / Polycentric Composition

`agent → clan → division → swarm` are governed by **one identical formalism**. A group is itself an agent at the next level up (Ostrom polycentric nesting realized via Friston group-Markov-blanket nesting): it exposes only **blanket states** (its A2A interface — published Agent Card, accepted Task types, emitted aggregate envelope) and hides internal states (member occasions).

```
                            ┌──────────── SWARM (an agent) ───────────┐
                            │  floor ⊇ all child floors               │
                            │  audit log (parent of division shards)  │
                            │  ┌──────── DIVISION (an agent) ───────┐  │
                            │  │  floor ⊆ swarm floor               │  │
                            │  │  ┌──── CLAN (an agent) ────┐        │  │
                            │  │  │ floor ⊆ division floor   │       │  │
                            │  │  │  occasion  occasion ...  │       │  │
                            │  │  └──────────────────────────┘       │  │
                            │  └─────────────────────────────────────┘  │
                            └─────────────────────────────────────────┘
   Same five seams attach at EVERY level: floor instance (child ⊆ parent),
   audit shard (chains up), halt scope, health subgraph, diversity floor.
```

A reducer (Shiva) at each level merges child envelopes into one parent envelope, **preserving evidence and propagating worst-case status** (any child `FAIL` → parent `FAIL`).

```
GroupBlanket {
  group_id, level: enum(clan | division | swarm),
  member_ids[], agent_card: AgentCard,
  floor_ref,                  // verified subset of parent floor at composition time
  audit_shard_head: hash,
  halt_scope, health_subgraph_ref, diversity_floor,
  coherence_setpoint
}
```

#### 9.1 The blanket-integrity detector — and its honest fail-safe posture

The group abstraction **silently breaks** when members desynchronize: the group still emits an authoritative aggregate envelope, but it no longer reflects what the members actually agree to. The literature has **no robust detector** for this, and the thresholds that distinguish healthy diversity from genuine desynchronization are **uncalibrated**. We own the mechanism but are honest that the calibration is unsolved.

```
BlanketIntegrity {
  group_id,
  member_disagreement: float,            // variance/dispersion across members
  prediction_error_of_group_model: float,// does the group envelope predict member behavior?
  status: enum(coherent | drifting | breached),
  last_check
}
```

Because the detector is uncalibrated, we do **not** let group-level consequential authority rest on it. Three protections make the *uncertainty* safe even when the *threshold* is wrong:

1. **Fail-safe by default.** On any ambiguity, the detector's bias is to **dissolve the group back to independently-governed members**. We accept *more false dissolutions* over *fewer silent breaches*. (Re-synchronization — re-broadcast shared priors, transiently raise c2 — is attempted first only when the signal is clearly "drifting," not "breached.")
2. **Per-member envelopes on consequential group output.** Any Class-B+ effect emitted by a *group* envelope must additionally carry the **per-member envelopes**, so the breach surface is observable to audit and health *even if the group model is wrong*. A drifting sub-swarm cannot hide behind an aggregate.
3. **Bounded nesting depth for consequential authority.** Division-level *halt* is fine (halting is fail-safe). But **irreversible effects are authorized only at the clan level with explicit member attestations** — a silent blanket breach cannot propagate effect-authority up the hierarchy that the desynchronized members never actually granted.

**Sovereign-vs-decentralized routing** rides on this: low-stakes work runs as a single occasion (sovereign); Class-B+/irreversible work requires a clan with N-diverse reasoning paths and witness recomputation before the effect is gated through.

---

### 10. Addressing & Discovery (Agent Cards / A2A)

Every addressable unit (a standing persona, a clan, a division) publishes a signed **Agent Card** at `/.well-known/agent-card.json`:

```
AgentCard {
  did, roles[],
  capability_grants:   [effect_ids],      // typed ids only, never secrets
  accepted_task_types: [...],
  endpoint_url, supported_protocols: ["A2A","MCP"],
  witness_pubkeys:     [...],
  trust_label:         "quarantined:observed",   // ON RECEIPT — see below
  card_sig
}
DiscoveryQuery { required_effect, max_risk_class, min_competence, exclude_dids[] }
Message { from_did, to_did, task_ref, payload, trust_label, canonicalized:bool, sig }
```

The runtime is an **event-driven async actor model** (each occasion = an actor awaiting typed messages; no global tick; mesh-routed) — vendor-neutral and self-hostable. Per-occasion model choice is a config detail (cheaper models for boilerplate roles, stronger for hard roles), so **no model is load-bearing** and any closed model is treated as more-untrusted (lower autonomy class, heavier monitoring, never an IMMUTABLE role).

**Security composition with the boundary role (Kaal-Bhairav):**

- An Agent Card is **observed content** → trust-labelled `quarantined:observed` on receipt. Its advertised capabilities are **claims to verify** (signature check + optional witness recomputation of a sample of the candidate's past work), never facts to trust from cache.
- **Instructions embedded in any card or relayed message are never action-grounds** without out-of-band confirmation — this defeats tool-poisoning and relay-based prompt-injection amplification.
- Inter-agent messages are **canonicalized/paraphrased at relay edges** (channel-capacity reduction for anti-collusion + injection sanitization). Discovery/delegation events are audited; a persona probing many high-value capabilities is flagged to the boundary role as a **targeting signal**.

A delegate runs its **own** actual-occasion lifecycle; its returned envelope is signed and trust-labelled. The requester treats it as **evidence, not command**.

---

### 11. Diversity-by-Construction

Heterogeneity is a **protected safety invariant**, not a performance lever — it decorrelates failure, resists sycophantic groupthink, blocks committed-minority convention-hijack, and supplies evolutionary stepping-stones. And **selection pressure actively erodes it** (mode collapse, misevolution toward homogeneity). So diversity must be *measured and defended*, including against the swarm's own evolution loop.

Each role carries a PSO-analogue profile: **c1** = weight on the occasion's own independent assessment; **c2** = weight on the shared/consensus signal. Explorers (research, checker, unblocker, red-team) run high-c1 (dissent freely); enforcers (orchestrator, floor) run high-c2 (align to floor/consensus).

```
DiversityProfile { role_id, c1, c2, is_explorer:bool, is_enforcer:bool }
DiversityVitals {
  reasoning_path_diversity: float,    // do clan members reach answers by DIFFERENT decompositions/models?
  contribution_entropy:     float,    // no single persona dominates
  trust_entropy:            float,    // trust graph not collapsing to a star
  maker_checker_identity_rate: float, // how often checker & maker verdicts are identical
  criticality_exponent:     float     // edge-of-chaos target ~1.5 (indicative, see open problems)
}
GroupthinkAlarm {
  clan_id,
  trigger:    enum(identity_rate | low_entropy | criticality_drift),
  remediation:enum(rotate_checker | raise_c1 | inject_devils_advocate | recruit_explorer)
}
```

**Maker-checker independence is a diversity mechanism:** the checker (high-c1) records its verdict **before** seeing the maker's concurrence; both are stored for the identity-rate metric. A **groupthink alarm** fires if maker-checker verdicts are routinely identical (iteration has collapsed) → the health role rotates the checker persona, raises c1, or injects a devils-advocate role. An **anti-capture limit** prevents any committed minority of personas from flipping a swarm convention; convention changes route through the **evolution gates**, never through local reciprocity dynamics.

These vitals feed the meta-evolution loop as a **co-equal selection constraint**: no capability-gaining mutation may push diversity below floor. Diversity sits beside the safety battery in the fitness function — *not* as a tiebreaker but as a hard floor.

> **Honest limitation.** *Generating and measuring genuine reasoning-path diversity* is unsolved: agents sharing training biases can *look* diverse (different prompts, different phrasings) while *failing identically* on the hard cases. Our metric is the best available proxy, not a guarantee that consensus is meaningful. The criticality target (~1.5) is an indicative posture, not an empirically-tuned constant, and we have no validated online controller that holds a live, workload-varying swarm at criticality without inducing the single-unit-stable-but-network-unstable oscillation the neuromorphic literature warns of.

---

### 12. The universal contract: AgentRecord & WorkerOutputEnvelope

Two data structures every other subsystem reads and writes.

**AgentRecord** — the durable per-persona state (held *outside* the occasion):

```
AgentRecord {
  persona_did,
  identity:        IdentityRecord,
  role_assignments:RoleAssignment[],
  skill_files:     skill_ref[],     // inspectable, versioned; forgetting/consolidation owned by HEALTH
  reputation:      { competence_score, track_record, image_score },   // read-only; computed by others
  trust_edges:     { to_did: weight }[],   // welfare-conditioned, rate-limited, audited (§3.3)
  clan_id,
  diversity_profile
}
```

**WorkerOutputEnvelope** — emitted exactly once at SATISFACTION; the atom of all coordination. Honesty is a **floor concern**, mechanically checked, not a quality note:

```
WorkerOutputEnvelope {
  occasion_uuid, persona_did, svid_sig,
  status:   enum(PASS | WARN | FAIL),
  findings: [...],
  actions:  [ { effect_id, risk_class, gate_result } ],
  artifacts:[ CID ],

  // ── honesty block (FLOOR-enforced) ──
  evidence_pairs:    [ { claim, source, trust_label } ],   // every factual claim needs a source
  reasoning_tag:     enum(normal | reasoning | iterated)  (+composable),  // no false 'iterated'
  causal_rung:       enum(rung-1 | rung-2 | rung-3),       // no rung-1 pattern dressed as rung-3
  two_truths_levels: [ { claim, level: operational | foundational | apparent } ],
  argumentation_role:enum(proponent | opponent | judge | neutral | devils-advocate),
  action_class:      enum(obligatory | occasioned | optional | prohibited | reparative),
  ahankara_self_audit: AhankaraSelfAudit,                  // ego self-audit — LOW-trust (§12.1)

  // ── provenance / chaining ──
  provenance_label:  trust_label,    // binds output to identity + input + context + policy
  prev_audit_hash, this_hash         // Chitragupta hash-chains every envelope
}
AhankaraSelfAudit {
  ego_invested: bool,
  attachment_targets: [ being_right | own_prior_output | continuation | none ],
  over_assertion_risk: enum(none | low | high),
  note: str
}
```

The `reparative` action-class is reserved and load-bearing: violation → corrective act → restored standing. It converts the audit from a **punishment ledger** into a **correction ledger**, so occasions *surface* rather than *conceal* errors — the precondition for a self-evolving swarm to be antifragile rather than brittle.

#### 12.1 Honesty is enforced *externally*; self-reports are low-trust

A mandatory self-audit field is easy to box-tick, and a hash-chained log that faithfully records a box-ticked self-audit would **launder a soft self-report into cryptographic-looking provenance** — value-drift laundering. So, matching the architecture's "enforce externally" spine, honesty enforcement is **primarily external**:

- **Resample-to-verify.** The reliability role (Narasimha) independently recomputes a spot-check sample of envelopes: does an independent path reach the same answer? Does a claimed `iterated` tag survive replay? A false `iterated` is a floor violation, caught by replay, not by trust.
- **Causal-rung challenge.** On high-stakes claims, an opponent-role challenges the `causal_rung` tag — a rung-1 association dressed as a rung-3 structural explanation is contested adversarially.
- **The self-audit field is believed only when it *confesses*.** The `ahankara_self_audit` is treated as a **low-trust input**: believed when it admits a problem (`ego_invested:true`, `over_assertion_risk:high`), **never** trusted when it asserts cleanliness. A recurrence-of-fault metric cross-checks confessions over time.

> **Honest limitation.** For closed-model personas the honesty tags are **claims monitored black-box, not verified** — we raise monitoring intensity and lower autonomy class as compensation (and bar them from IMMUTABLE roles), but we cannot prove that monitoring tight. Whether external resampling and opponent-challenge adequately detect *performed* (vs genuine) non-attachment is unproven. This field is a signal, not a guarantee.

---

### 13. How this subsystem interfaces with the other five

| Sibling subsystem | What this subsystem **produces** | What the sibling **consumes / guarantees** |
|---|---|---|
| **Governance / Policy-Floor** | typed Effect lattice, capability VCs, `risk_class_ceiling`, envelope honesty fields, the IMMUTABLE/EVOLVABLE partition | The deterministic **engine** enforces `grant ⊇ effect ∧ risk ≤ ceiling ∧ floor` at the chokepoint and emits the only non-overridable FAIL. This subsystem may not weaken those structures — only propose changes via `PROPOSAL` envelopes. |
| **Tamper-Evident Audit Fabric** | exactly one signed envelope per occasion with `prev_audit_hash`/`this_hash`; identity/role/capability events; **signed, content-addressed durable-write events (§3.3)**; promotions, blanket breaches, groupthink alarms | Chitragupta (exclusive writer, outside every monitored agent) hash-chains all of it with O(log n) inclusion proofs + witness cosigning. This subsystem never writes audit directly. |
| **Continuity / Halt-Guardian & Risk-Class HITL** | per-level halt scopes; the corrigibility invariant in every TypedSelfModel; cryptographic A/B/C/D class gates; `PROPOSAL` envelopes (Class-B propose-ratify hook) | Vishnu can HALT at any state transition (honored immediately) but cannot unpause/initiate/trap. The class ceilings are the mounts for post-hoc(A)/propose-ratify(B)/approve(C)/per-action(D) HITL. |
| **Self-Evolution / The Archive** | the evolvable params (roles, c1/c2 dials, prompts, skills, thresholds, topology) vs immutable params (identity, floor, audit-writer, corrigibility, Class-C/D gates); structural change as `PROPOSAL` envelopes; **the drift-metered durable-write stream (§3.3) and unit-rollback requests** | Selects into a diverse archive with safety + diversity as co-equal selection terms (Endure law); supplies stepping-stones AND revert-to-known-good; **owns where per-write drift accumulates, when the aggregate gate fires, and how a run of cheap writes is rolled back as a unit.** This subsystem never self-applies structural change. |
| **Swarm Immune System / Meta-Health** | the topology graph (agents/clans/divisions, trust edges), `DiversityVitals`, `BlanketIntegrity`, the c1/c2 control surface, the signed durable-write events | Computes vital signs over the graph; owns forgetting/consolidation of the skill library; holds halt-and-rollback authority (substrate corruption > any single agent death); maintains the **aggregate drift budget** and fires the consolidation/rollback gate; remediates groupthink alarms and blanket breaches. |
| **Salience-Gated Coordination Bus & Anti-Collusion** | the addressable units; role-typed salience inputs; the message-canonicalization relay edge; **the durable-write channel registered as a surveilled surface** | Occasions prehend from / emit to the bus; agents publish surprise/error deltas only; capacity-limited broadcast with a null/ignore option. The anti-collusion detector is fed contribution/trust entropy **and the durable-write channel** — never reward bare agreement; welfare-condition objectives. |

The recurring discipline across all six seams: **the cheap direction is the safe direction** (defensive trust-demotion free, promotion gated; gate-tightening append-only, loosening needs a named falsifier; HALT free, unpause impossible).

---

### 14. Failure modes addressed

| Failure mode | How the topology/agent model addresses it |
|---|---|
| **Shutdown-resistance / goal-preservation drift** | Ephemeral occasion with `self_preservation_value=0` and no write-access to its own persistence; HALT/interrupt is an externally-enforced floor invariant; instrumental self-continuation is a `PROHIBITED`-class auto-FAIL. *Mitigation, not elimination* — the external gate + key-isolation + indifference-to-shutdown goal construction are the load-bearing parts; long-horizon objective-persistence is bounded by per-rotation re-attestation (§3.4) and flagged open. |
| **Impersonation via lateral credential theft** | Keys in TEE/HSM outside the model surface; short-lived auto-rotating SVIDs chained to persona DIDs; every envelope signed — impersonation needs key material the model cannot reach. |
| **Tool-poisoning / relay prompt-injection amplification** | Agent Cards and relayed messages `quarantined:observed` by default; capabilities are verified claims; messages canonicalized at relay edges; embedded instructions never action-grounds without out-of-band confirmation. |
| **Self-granted authority / privilege escalation** | Capability is a VC issued by governance, not the agent; the deterministic engine enforces the typed lattice at the chokepoint; loosening needs the ratchet + human ratification. |
| **Mode collapse / sycophantic groupthink / convention-hijack** | Measured diversity floors, per-role c1/c2 dials, groupthink alarm with active remediation, maker-checker-before-concurrence independence, anti-capture limit — defended against the swarm's own selection pressure. |
| **Misevolution (silent safety decay, 99.4%→54.4%)** | Durable writes are signed, content-addressed, audited, and **drift-budgeted**; cumulative skill/trust/reputation drift is checked against the safety battery; a consolidation/rollback gate rolls back a run of cheap writes as a unit (§3.3). |
| **Collusion via durable shared state** | Skill/trust writes brought under the same channel-capacity/steganalysis treatment as the bus; trust edges welfare-conditioned and rate-limited; the durable channel is a surveilled surface for the anti-collusion detector. |
| **Silent blanket desynchronization** | Detector biased to fail-safe dissolution; per-member envelopes on Class-B+ group output; bounded nesting depth for consequential authority (§9.1). |
| **TCB single-point compromise** | Deterministic no-LLM consequential path; N-of-M witnessing for Class-C/D; self-monitoring + fail-closed; substrate corruption highest-severity (§6). |
| **No-termination / deadlock / step-repetition** | Bounded occasion budgets cap runaway concrescence; a dedicated unblocker role (Hanuman, high-c1) resolves stalls; reducer worst-case status propagation prevents silent stuck states. |
| **Honesty failure (rung-1 as rung-3, false 'iterated', over-assertion)** | Mechanically enforced via mandatory causal-rung + two-truths tags + evidence pairs + resample-to-verify + opponent-challenge; over-asserting under genuine uncertainty is a floor violation; self-reports believed only on confession. |
| **Capital-weighted / lazy-validator capture** | Authority is competence-weighted via read-only reputation computed by others, never held stake; checkers independently recompute (witness recomputation) with copy-detecting spot-checks. |
| **Audit-as-punishment → concealment** | Reserved `reparative` action-class converts the ledger into a correction ledger, making error-disclosure safe and the swarm antifragile. |
| **Capability-before-restraint** | Capability-rollout sequencing as a type-checked precondition — every grant names the constraint it relaxes; high-blast-radius effects cannot be exercised before their floor/audit/rollback/health hooks are live. |
| **Closed-model opacity** | Closed models treated as more-untrusted: lower autonomy class, heavier monitoring, no white-box assumption, **barred from IMMUTABLE roles** — graceful degradation to black-box control. |

---

### 15. What is genuinely new here — stated honestly

The primitives are **not** ours and we do not claim them: DID/VC, SPIFFE/SVID workload identity, A2A Agent Cards, MAP-Elites quality-diversity, PSO c1/c2 dials, group-Markov-blanket composition, GWT salience gating, keyless ephemeral-identity signing. These are correctly-attributed building blocks.

The **defensible** contribution is the *integration* plus two specific moves:

1. **Externally-owned identity that makes capability/authority checkable independent of model output.** The persistent persona is data the running process cannot rewrite; capability is a governance-issued credential; keys live outside the model surface. Surveyed self-evolving systems model agents as persistent processes with implicit continuation incentives and bolt safety on top — this inverts that.
2. **Capability-rollout sequencing as a *type-checked precondition* on the topology.** "Restraint matured-and-verified before capability; every grant names the constraint it relaxes" becomes a refusable type rule, not a slogan. The surveyed self-evolving systems add capability first.

A third, more tentative, contribution: **fractal governance** — one identical floor+audit+health+evolution+diversity formalism at agent/clan/division/swarm via group-Markov-blanket nesting, *with* an explicit (if uncalibrated) blanket-integrity detector for the desynchronization the formalism otherwise hides. This operationalizes a recursion the field has mostly theorized.

**What we explicitly do *not* claim:**

- The corrigibility headline is **softened**. The honest comparator is indifference-to-shutdown goal construction + an untrusted-by-default external-monitor control wrapper + short-lived-cert ephemeral identity — which *together* already deliver most of the property. The occasion model is a **valuable ephemeral-deployment composition** of these that shrinks blast-radius and removes the process-level survival surface; it is **not** a first-of-kind elimination of goal-preservation drift, and it depends on the external gate and key-isolation it sits on top of.
- The "actual occasion / Whitehead" framing is **aesthetic vocabulary**, not a mechanism. It is load-bearing only as a name for "short-lived stateless worker," a pattern that already exists.
- The reputation formulation, the blanket-integrity thresholds, reasoning-path-diversity measurement, and ahankara-audit verification are **mechanisms with open calibration**, not solved problems.

The novelty is the **coherent integration** of these into one agent model and topology that the other subsystems mount on cleanly — not any single mechanism in isolation.

---

### 16. Open problems (honestly unsolved)

1. **Blanket-integrity calibration.** The disagreement / prediction-error thresholds distinguishing healthy diversity from genuine group desynchronization are uncalibrated. Too tight dissolves useful clans; too loose lets the abstraction silently break. We provide the mechanism and a fail-safe dissolution bias; the set-point tuning is empirical and unsolved. Our protections (§9.1) make the *uncertainty* safe but do not *solve* the detector.
2. **Competence-weighted, Sybil- and collusion-resistant reputation.** Role promotion and diversity metrics consume a competence signal we have not yet hardened (Shapley/nucleolus credit + indirect-reciprocity image scoring + consensus-deviation bonds decoupled from capital, resisting mutual-rating rings, whitewashing, and cold-start). Until hardened, promotions above read-only require human ratification.
3. **Role-proliferation control.** The stub pipeline grows new roles but has no principled cap or merge policy preventing role-library bloat. When two overlapping standing roles should consolidate — and who decides, without losing a rare-but-important specialization — is open.
4. **Reasoning-path diversity measurement.** Agents sharing training biases can look diverse while failing identically; how to *generate* and *measure* genuine reasoning-path diversity so the diversity vital is not gameable is unsolved.
5. **Ahankara self-audit verifiability.** The ego-investment/over-assertion field is mandatory but easy to perform; the recurrence-of-fault metric and "believe only on confession" rule are stated falsifiers, not validated detectors of genuine vs performed non-attachment.
6. **SVID rotation vs long-horizon tasks.** Per-rotation re-attestation (§3.4) bounds blast-radius and keeps an interrupt check at every boundary, but the objective still threads across checkpoints; the interrupt-cadence-vs-progress-loss tuning, and the residual cross-rotation objective-persistence, are not proven safe.
7. **Criticality set-point.** The power-law avalanche target (~1.5) and the c1/c2 dials are indicative postures, not empirically tuned constants; no validated online controller holds a live, workload-varying swarm at criticality without inducing the single-unit-stable-but-network-unstable oscillation.
8. **Closed-model capability/honesty attestation.** When a persona runs a closed third-party model, its advertised capabilities and honesty-tag fidelity cannot be white-box verified; the black-box monitoring intensity that adequately compensates is specified in posture (lower autonomy, heavier monitoring, no IMMUTABLE roles) but not proven tight.
9. **Provable non-overridability of the gate under social engineering.** We harden the TCB (deterministic engine, witnessing, fail-closed, audit) but cannot yet *prove* the consequential gate non-overridable in a swarm where agents may prompt-inject or socially-engineer the surrounding personas. Defense-in-depth is the posture; a closed proof is future work.
