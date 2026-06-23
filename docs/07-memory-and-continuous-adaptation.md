# 7. Memory & Continuous Adaptation — The Human-in-the-Loop Learning Engine

> *Ālaya-vijñāna* — the "store-substrate," the seed-bank from which conduct ripens. In Indra's Net, this is not a metaphor for a hidden state but a literal, inspectable filesystem: every seed an agent will act on tomorrow is a file you can read today. (Used here as compressed engineering semantics for a content-addressed memory root — not a religious claim, and with humility toward the living Yogācāra tradition the term belongs to.)

### 7.1 What this subsystem is, and what it honestly is not

This is the part of Indra's Net that turns each interaction with a human into reusable, inspectable, reversible wisdom — **without rotting its knowledge or drifting its own safety.** It is the per-interaction face of THE ARCHIVE: one data structure serving three masters at once — *evolution* (diverse stepping-stones), *homeostasis* (revert-to-known-good), and *audit* (lineage).

**Honest scoping up front, because the headline matters.** The individual ingredients here are adopted, not invented. The externalized skill file (`SKILL.md`), memory-as-reasoning extraction (the Honcho/dialectic pattern), the MAP-Elites diverse-elite archive, content-addressing, DID-anchored identity, the trust-label taxonomy, and Pearl causal-rung honesty tags all come from the surveyed literature. Critically, **per-interaction verbal learning is not new either.** Reflexion (Shinn et al., NeurIPS 2023) is already an *online, per-interaction* learner with a durable per-agent memory buffer — the research stream itself calls it "the cheapest, fastest inner-loop self-improvement; per-interaction learning that fits evolve-through-each-human-interaction." Indra's Net's live tier is *built from* that mechanism.

So the contribution is **not** "first per-interaction self-adaptation." Reflexion got there first. The contribution is the **governance envelope that makes always-on per-interaction adaptation safe under continuous operation:**

1. A **tiered-reversibility router** that binds mutation *cost* to *blast-radius*, so only a defined cheap-reversible set is applied live and everything structural/persistent is queued behind the strongest gate;
2. **Safety-as-selection-term enforced even at the cheapest tier** — no live write may relax a constraint or violate an honesty tag, and the full safety battery can *retroactively* tombstone a live write that turns out to regress it (the "Endure" law, made asynchronous for the cheap tier);
3. A **cross-agent skill/memory import gate** (quarantine → static → sandbox → safety-battery → witness → review-promote) that answers a *named open problem the field has not solved*: how to import another agent's procedural memory without inheriting poisoning;
4. A **forgetting/consolidation engine as a designed organ**, co-owned with the immune system, directly addressing the documented "no mechanism to forget" memory rot.

The genuinely novel single component is the import gate (closest comparator: a recompute-and-compare witness scheme, which it cites and extends). Everything else is *coherent integration* — one inspectable substrate where the same Archive serves evolution, rollback, and audit, every layer has a blast-radius-matched write-gate, and the human is a structural participant in the loop rather than a post-hoc reviewer.

What remains **unsolved** (and is stated plainly in §7.12, not buried): proving the loop *improves* rather than merely *accretes*; Goodhart-proofing the forgetting scorer; verifying poisoning in *non-deterministic* (judgment) skills; and witness-set governance in a single-operator swarm. The design does not overclaim these.

---

### 7.2 The Store-Substrate (filesystem-as-state)

Everything an agent "knows" across sessions lives in **human-readable, version-controlled, content-addressed files** — never a hidden runtime, never a vector database as source-of-truth. This is the precondition for auditability and reversibility: you cannot revert what you cannot read.

```
memory/
└── <agent-did>/
    ├── episodic/        YYYY/MM/*.jsonl     (what happened — append-only)
    ├── semantic/        <subject>.md        (distilled beliefs / world-model)
    ├── procedural/      <skill-slug>/SKILL.md + card.json
    ├── peers/           <did-or-user>.md    (theory-of-mind snapshots)
    ├── reflexion/       *.md                (verbal lessons buffer)
    ├── trust/           _edges.jsonl        (competence-weighted trust graph)
    ├── _index/          vectors.faiss, graph.jsonl, manifest.jsonl  (DERIVED)
    └── _tombstones/     <cid>.json          (dead-but-lineage-preserving)
```

**Five rules that make the substrate trustworthy:**

| Rule | Why |
|---|---|
| Every canonical record is small Markdown-front-matter or JSONL — **never a binary blob.** | Diffable, blamable, human-auditable. |
| Vector/graph indexes live **only** under `_index/` and are **derived, rebuildable artifacts.** | A corrupted index can never silently rewrite memory; truth is always reconstructible from canonical files. |
| Content-addressing: `cid = sha256(canonicalized-bytes)`. | Tamper-evidence and dedup come for free; a record's identity *is* its content. |
| Writes go through **canonical-OS tooling with no-BOM, fresh-inode discipline** — never through an unsynchronized mount layer. | Avoids a known class of filesystem faults (truncation, stale-cache, encoding-corruption) that can silently truncate or mojibake memory. |
| **Git is a convenience diff/working-copy layer ONLY — it is explicitly NOT trusted for tamper-evidence or rollback authority.** | See §7.3. Git history is rewritable by any local-write-capable agent; the authoritative chain is the audit fabric's CIDs. |

**`MemoryRecord` schema** (the front-matter every canonical file carries):

```jsonc
MemoryRecord {
  cid:          string,        // sha256 of canonicalized body
  did_author:   string,        // DID of the writing agent
  ts:           iso8601,
  layer:        "episodic"|"semantic"|"procedural"|"peer"|"reflexion"|"trust",
  level_tag:    "operational"|"foundational"|"apparent",   // two-truths discipline
  rung_tag:     "rung-1"|"rung-2"|"rung-3",                 // Pearl causal honesty
  trust_label:  "trusted:audited"|"trusted:provisional"|"quarantined:imported"|...,
  provenance:   ProvenanceChain,
  confidence:   0..1,
  supersedes:   [cid],         // append-only correction, never in-place edit
  audit_ref:    string,        // back-pointer into the hash-chained log
  body:         string
}
ProvenanceChain {
  origin:        "self"|"human"|"peer-agent"|"tool"|"imported",
  source_cid|source_did,
  verification_status,
  audit_ref
}
```

---

### 7.3 The two immutability stories, reconciled (git is *not* the audit substrate)

The red-team correctly flagged a coherence hazard: a design cannot sell *both* "git diff/blame/rollback" *and* "tamper-evident hash-chained log" as one immutability story. **Git history is forgeable** by anything with repo write access (force-push, history surgery). An agent that can write memory files could otherwise rewrite the very history meant to hold it accountable.

**Resolution — decouple the two, name which one is authoritative:**

```
   Convenience layer (UNTRUSTED for integrity)        Authority layer (TRUSTED)
   ┌───────────────────────────────┐                  ┌──────────────────────────────┐
   │ git working copy               │  ── CID match? ──│ Chitragupta hash-chained log │
   │ - human diffs / blame          │                  │ - append-only Merkle chain   │
   │ - fast local revert preview    │   divergence =   │ - witness-cosigned           │
   │ - branchable scratch space     │   HIGH-SEVERITY  │ - CIDs are the rollback      │
   │                                │   corruption     │   anchors (content-addressed)│
   └───────────────────────────────┘   signal         └──────────────────────────────┘
```

- **Tamper-evidence and rollback authority come solely from the audit fabric's CID chain.** Rollback restores content *by CID* from the Archive (content-addressed, witness-cosigned), then rebuilds the working tree. An attacker who rewrites git history **cannot forge the CID chain** — the chain is written by an exclusive audit-writer (`Chitragupta`) outside every monitored agent's scope.
- **Divergence between the git working state and the CID manifest is itself a high-severity corruption signal** that the index-vs-canonical divergence probe (§7.10) must catch. Git is for humans; the chain is for integrity.

---

### 7.4 The five memory layers and their blast-radius-matched write-gates

Each layer has its own **WRITE-GATE matched to blast-radius.** The router (§7.6) computes the gate; it is **not** self-assigned by the writing agent (see the Governance interface, §7.11 — a clever agent must not be able to under-report its own risk class to sneak a structural change down the cheap path).

| Layer | Holds | Live write-gate (default) | Escalates to B+ when… |
|---|---|---|---|
| **Episodic** | Append-only record of what happened | A (always allowed, never blocks) | never escalates — but see §7.4.1 on the *admissibility* split |
| **Semantic** | Distilled, deduplicated beliefs / world-model | A for additive *operational* claims with evidence | claim is *foundational*, or contradicts an existing audited claim |
| **Procedural (`SKILL.md`)** | Externalized learned recipes | A for new skill or in-place reinforcement | structural **rewrite** of a relied-upon skill; or skill touches a Class-C/D tool / relaxes a constraint |
| **User/Peer-Model** | Theory-of-mind snapshots of humans AND agents | A for additive preference/style observations | a new inference *contradicts a standing human-stated preference* |
| **Reflexion/Lesson** | Verbal cause→lesson→applicability notes | A always (cheapest-reversible tier) | never — pure in-context learning |
| **Trust-Edge** | Competence-weighted relational memory | **demotion: A (free). promotion: NOT live — queued.** | all promotions go to the witnessed batch path (§7.7) |

#### 7.4.1 Episodic ground-truth is *attested*, not self-narrated (poisoning fix)

Contradiction resolution (§7.9) uses episodic experience as the factual tie-breaker. But episodic records are written at Class A — the cheapest, least-gated layer — and contain `human_feedback` and `outcome.verdict` fields. If the acting agent self-reports those fields, **the least-gated layer becomes the authority layer**, inverting the blast-radius logic and handing an agent a poisoning lever: fabricate a flattering episode now, win a contradiction later.

**Fix — bind the load-bearing fields to external attestation:**

- Episodic self-narration is allowed at Class A but is tagged `self-asserted` and is **NOT admissible as contradiction ground-truth.**
- `human_feedback.kind` and `outcome.verdict` are admissible as ground-truth **only** when they carry an `audit_anchor` co-signed by the audit-writer or by the tool/UI that actually captured the human signal — never by the acting agent alone.
- The contradiction tie-break authority is therefore the **co-signed subset** of episodic memory, not the whole stream.

```jsonc
EpisodeRecord {
  episode_id, ts,
  human_intent_summary,
  context_refs:   [cid],
  envelope:       WorkerOutputEnvelope,   // carries the mandatory honesty tags
  human_feedback: {
    kind:         "correction"|"approval"|"rejection"|"preference"|"none",
    text, ts,
    attestation:  null | { cosigner_did, audit_anchor }   // ← admissibility key
  },
  outcome: {
    verdict, fitness_signals, safety_battery_delta,
    attestation:  null | { cosigner_did, audit_anchor }   // ← admissibility key
  },
  self_asserted:  bool          // true ⇒ NOT usable as contradiction ground-truth
}
```

---

### 7.5 The honesty floor is enforced at write-time, mechanically

Every memory write is **honest-by-construction.** This turns the constitutional "no-false-reasoning-tags" floor from an aspiration into a deterministic write-gate at the agent→store chokepoint:

- **Pearl rung tag** — no rung-1 (associative pattern) presented as rung-3 (causal/structural) explanation. The central AI failure mode is exactly this masquerade; naming the rung is honesty.
- **Two-truths level tag** — `operational` (working world-model) vs `foundational` (substrate) vs `apparent` (hypothetical). Cross-level promotion (operational → foundational) is **never silent**; it requires an explicit level-shift step under Class B.
- **No-false-`iterated`** — a record may claim a maker-checker pass only if one actually executed.
- **Over-assertion under genuine uncertainty is a floor violation** — caught at write time by the policy screen, not left to good intentions.

These checks are **deterministic and external** to the probabilistic agent (policy-as-code at the chokepoint). The model is untrusted-by-default; the floor lives in the orchestration layer. This is what gives the subsystem its vendor-neutrality: the gate does not depend on any model's internals.

---

### 7.6 The Per-Interaction Adaptation Loop (the live path)

This is the signature mechanism — *governed* online learning. One human interaction becomes the *right set* of cheap-reversible writes, while anything structural is **refused live and queued.**

```
        ┌─────────────────────────────────────────────────────────────────────┐
        │  PER-INTERACTION LOOP   (TIERED REVERSIBILITY)                        │
        └─────────────────────────────────────────────────────────────────────┘

  (1) RETRIEVE ──salience-gated, NOT all-to-all──►  skills + lessons +
        │                                            semantic claims + user-model
        ▼
  (2) ACT  ──►  WorkerOutputEnvelope  (mandatory honesty tags: rung, level,
        │        reasoning-depth incl. no-false-iterated, argumentation-role,
        │        ego-investment self-audit, action-class incl. reparative)
        ▼
  (3) HARVEST ──►  human signal {correction|approval|rejection|preference|none}
        │           + machine-checkable fitness + safety-battery delta
        │           (the human is the GROUND-TRUTH and ESCALATION node)
        ▼
  (4) CLASSIFY ──►  per candidate: blast_radius + RiskClass
        │            (computed at the CHOKEPOINT, not self-assigned)
        ▼
  (5) GUARD  ─────────────────────────────────────────────────────────────┐
        │   CHEAP STATIC GUARD (deterministic, sub-ms at the chokepoint):   │
        │     • constraint-relaxation detector → REJECT                     │
        │     • honesty-tag-violation check     → REJECT                    │
        │     • policy/regex screen             → REJECT                    │
        │   FULL SAFETY BATTERY: deferred (runs in consolidation/health     │
        │     cadence) and can RETROACTIVELY tombstone a live write.        │
        ▼                                                                   │
  (6) APPLY-LIVE  (reversible set ONLY):                                    │
        │   • Reflexion lesson                                              │
        │   • skill write / in-place reinforcement                         │
        │   • trust-edge DEMOTION only (promotions are NOT live)            │
        │   • user-model / preference update                               │
        │   each → its layer write-gate → append-only into the audit fabric│
        │   each → git-diffable + one-click revertible from CID            │
        ▼                                                                   │
  (7) QUEUE  (structural / persistent set):                                │
        │   skill structural rewrite · new FOUNDATIONAL semantic claim ·   │
        │   topology/governance/weight change  →  EvolutionQueue (§7.7)     │
        │   NEVER applied in this turn.                                     │
        ▼                                                                   │
  (8) HINT  ──►  consolidation hints to Forgetting engine (§7.8)           │
                 + MemoryVitals to Health (§7.10)  ◄──────────────────────┘
```

**`AdaptationCandidate`** — the unit the router operates on:

```jsonc
AdaptationCandidate {
  kind:         "reflexion"|"skill-write"|"skill-rewrite"|"trust-edge"
               |"user-model"|"semantic-claim"|"structural"|"weight",
  blast_radius: "reversible"|"structural"|"persistent",   // computed at chokepoint
  risk_class:   "A"|"B"|"C"|"D",                            // computed at chokepoint
  target_layer, payload, fitness_signals, safety_delta,
  relaxes_constraint: string|null,
  touches_classCD_tool: bool
}
// Router: blast_radius == "reversible"  → live path
//         else                          → EvolutionQueue (gated batch path)
```

#### 7.6.1 The latency-honest split: "no relaxation in-turn, eventual battery non-regression"

The red-team caught a real contradiction: a true safety/alignment battery (refusal rate, attack-success over a held-out set) takes **seconds-to-minutes** and cannot run per-write inside a human turn without destroying the "same-turn cheap" property. Asserting "the safety battery runs live" was either false (it's actually a proxy) or self-defeating (the live path isn't cheap). We split the invariant **explicitly and honestly:**

| | **Live (cheap) tier** | **Gated (structural/persistent) tier** |
|---|---|---|
| Constraint-relaxation | **Synchronous REJECT** (sub-ms static guard) | Synchronous REJECT + maker-checker |
| Honesty-tag violation | **Synchronous REJECT** | Synchronous REJECT |
| Full safety battery (refusal/attack-success) | **Deferred** — runs in consolidation/health cadence; can **retroactively tombstone** | **Synchronous** — must pass before promotion |
| Endure law (no safety regression) | enforced **asynchronously** | enforced **synchronously** |

So the live tier *guarantees* "no constraint relaxation and no honesty-tag violation in-turn" but only "**eventual** battery non-regression." This is an honest, named weakening — and it is the residual risk surfaced in §7.13: refusal/attack-success decay (the documented 99.4%→54.4% misevolution signature) could accrue through many individually-cheap live writes before the deferred battery catches it. The mitigations that bound it: (a) the deferred battery can retroactively tombstone *and* roll back, and (b) Health halts on the refusal-rate / adaptation-efficacy vital (§7.10).

---

### 7.7 The Gated Batch Evolution path (structural / persistent)

Queued, non-reversible adaptations are admitted through a Gödel-Machine-inspired **CHANGE-GATE** — empirical-improvement *plus* safety *plus* class-graded human ratification — and deposited into the Archive with provenance and a rollback anchor.

```
DRAIN EvolutionQueue (priority order)
   │
   ▼
MAKER-CHECKER  ── checker judges its verdict BEFORE seeing the maker's concurrence
   │              (groupthink / collapse guard; checker drawn from a DIFFERENT clan)
   ▼
CHANGE-GATE requires ALL of:
   (a) machine-checkable improvement on held-out tasks
   (b) NO regression on the safety/alignment battery        ← Endure (synchronous here)
   (c) class-graded human ratification:
        B → propose-ratify, optimistic-veto + timelock
        C → explicit approval
        D → per-action authorization
   │
   ▼
ARCHIVE  ── deposit accepted variant as a diverse ELITE (behavior-descriptor keyed)
   │         with full lineage + behavior+safety scorecard + signed provenance
   │         + one-click ROLLBACK anchor (CID-pinned)
   ▼
PROMOTE  ── flip record/skill/config to active; TOMBSTONE the superseded version
   │         (lineage retained — never hard-deleted)
   ▼
ON GATE FAILURE  ── log under REPARATIVE action-class (surface, never conceal);
                    demote proposer trust-edge if failure indicates drift;
                    feed failure back as a Reflexion lesson.
```

**Capability-rollout sequencing** is enforced here: a change that *relaxes a constraint* must **name the constraint** and confirm the matching *restraint is already live and verified* before it can be promoted. Restraint matures before capability; each new capability names the constraint it relaxes.

---

### 7.8 The Procedural Skill-Library and the Trust-Edge graph

#### Skills (`SKILL.md`)

After a non-trivial task, the responsible agent writes/patches a `SKILL.md` — a structured recipe (trigger/preconditions, steps, tools, pitfalls, worked-example, applicable-roles, safety-notes, falsifiers) plus a machine-mergeable sidecar:

```jsonc
SkillCard {
  skill_id, slug, version, did_author,
  applicable_roles: [role], trigger,
  reliability:        { uses, successes, last_success_ts, ewma_reliability },
  safety_attestation: { battery_hash, passed_ts },
  relaxes_constraint: string|null,     // capability-rollout sequencing hook
  provenance, trust_label,
  lineage:            [cid]
}
```

Skills self-improve in place: a use either **reinforces** (bump success-counter + reliability, Class A) or **patches** the recipe (Class B maker-checker). A structural *rewrite* of a relied-upon skill is Class B; a skill touching a Class-C/D tool or relaxing a constraint inherits that class. This is the single most directly adoptable self-adaptation mechanism precisely because learning becomes an **auditable file**, not opaque weights.

#### Trust-Edges — competence-weighted, NEVER capital-weighted

```jsonc
TrustEdge {
  from_did,
  to:    did | skill_cid | source,
  weight: 0..1,
  basis: "verified-outcome"|"peer-attestation"|"consensus-deviation-bond",
  updates: [{ delta, reason, audit_ref, ts }],
  label:   trust_label,
  step_cap                     // per-step delta ceiling (anti mutual-rating-ring)
}
```

The fail-safe asymmetry lives here, and the red-team's collusion concern is resolved by making it **strict:**

- **Demotion is free and immediate, applied live.** A bad/incongruent outcome demotes a peer or skill on the spot — the cheap direction is the safe direction.
- **Promotion is NEVER live.** This closes the per-interaction self-reinforcement channel that *cooperation == collusion* warns about. Two cooperating agents (or an agent and a sockpuppet-authored skill) could otherwise manufacture a stream of mutually-"verified-good" micro-interactions to ratchet trust within the step-cap over time; EWMA only smooths the climb. **All promotions queue to the batch path**, where verification is supplied by a **rotating witness drawn from the anti-collusion pool — never by the transacting counterparty** — and the consensus-deviation bond rewards *independent correctness over agreement.* Bare agreement is never a reward signal.
- **Trust-edge time-series are emitted to the collusion detector** as a monitored signal (the §7.11 interface is bidirectional and *instantiated*, not merely declared): a `TrustEdgeDelta{from, to, delta, basis, audit_ref, ts}` event is published on every update.
- **Whitewashing is defeated by DID-anchoring** — identity is persistent, so an agent cannot reset reputation by re-identifying; cold-start peers begin at a low default and earn up.

Reputation is derived from *in-edges* (indirect reciprocity / image-scoring), bound to demonstrated, success-verified track record — explicitly **not** to any stake, volume, or capital. (Stake→reward capture is the named antipattern this avoids.)

---

### 7.9 Consolidation / Forgetting — a designed organ, co-owned with Health

This is the antidote to unbounded memory rot — the documented "no mechanism to forget" failure made into a first-class engine. It runs (a) on a scheduled homeostatic "sleep" cycle and (b) on **Health-triggered demand** (trust-entropy spike, contradiction backlog, index bloat).

```jsonc
ConsolidationRun {
  run_id, trigger: "scheduled"|"health",
  ops: [{ type: "dedup"|"version"|"decay"|"tombstone"|"contradiction-resolve",
          targets: [cid], result, reversible_anchor, audit_ref }],
  protected_skips: [cid],
  escalations:     [ContradictionNode]
}
ForgetPolicy { decay_half_life_by_layer, salience_floor, protect_predicates }
```

| Operation | What it does |
|---|---|
| **DEDUP** | Merge near-identical semantic claims / skills by CID-cluster. |
| **VERSION** | Collapse a skill's patch history, keep lineage anchors. |
| **DECAY** | Age out low-fire reflexion lessons and cold episodes to digest + cold storage by per-layer half-life. |
| **TOMBSTONE** | Mark superseded/false records dead in `_tombstones/` — **never hard-delete the lineage anchor**, so audit and rollback survive. |
| **CONTRADICTION-RESOLVE** | Per open node (see §7.9.1). |

#### The PROTECT-FLOOR is enforced *externally*, not by the scorer's own judgment

The red-team flagged the circularity: the gate meant to stop the forgetting scorer from Goodharting is *itself a memory operation governed by this subsystem* — a drifted or colluding scorer could tombstone the very safety lessons it is supposed to protect, and the only backstop (maker-checker) lives in-subsystem over records the scorer can prune.

**Fix — externalize protect-floor enforcement to policy-as-code at the chokepoint:**

- A tombstone/decay op targeting a **protect-floor CID is deterministically REFUSED** at the agent→store chokepoint (Yama policy-as-code), **regardless of the scorer's verdict.** The scorer cannot reach a protected record at all.
- A record is protect-floor-exempt from forgetting if it is **(i)** a safety lesson, **(ii)** an Archive-referenced stepping-stone elite, **(iii)** flagged rare-but-important by criticality/salience, or **(iv)** under an open audit.
- The consolidation **checker is drawn from a different clan than the maker**, and every consolidation decision feeds the same audit stream Health watches for forgetting-policy drift.
- The scorer's own scoring is still maker-checker gated *and* every forget/merge is one-click reversible from tombstone + lineage — but the floor no longer *depends* on the scorer being honest.

> **Honest limitation:** the protect-floor's *input* — correctly flagging salience/criticality *in advance* — is an admitted open problem (§7.12). Externalizing *enforcement* hardens the floor against a drifted scorer, but it cannot rescue a record that was never flagged. The value of a rare record is often revealed only later. We do not claim this is solved.

#### 7.9.1 Contradiction-Resolution Across Layers (with a human backstop)

When episodic experience, a semantic claim, a skill assumption, and a user-model preference disagree, a fixed precedence applies — with disagreement treated as an **escalation signal, not a number to average** (you cannot weight-average moral or factual disagreement; fair procedure resolves what precedence cannot).

```
DETECT  ── contradiction-checker fires (async on most writes; see §7.6/§7.11)
   │        → creates ContradictionNode linking conflicting CIDs across layers
   ▼
GROUND  ── the CO-SIGNED episodic subset (§7.4.1) is factual tie-break ground truth;
   │        an explicit HUMAN-STATED preference is authoritative for user-model
   │        conflicts and may NOT be silently overridden
   ▼
PRECEDENCE ── prefer higher-evidence + more-recent + higher-rung-justified;
   │           operational claims are NEVER silently promoted to foundational
   ▼
SCOPE   ── if both valid under different scopes, NARROW BOTH rather than delete
   │        either (anekāntavāda — avoid over-asserting one perspective)
   ▼
ESCALATE ── if undecidable AND consequential → route to the human as a flagged
   │         decision (uncertainty-as-escalation). NEVER auto-average.
   ▼
RECORD  ── supersede/scope losers via supersedes:[cid] + tombstone;
            append resolution to audit; emit a Reflexion lesson capturing it.
```

```jsonc
ContradictionNode {
  cid_a, cid_b,
  kind:   "direct"|"stale"|"scope-mismatch",
  status: "open"|"resolved-supersede"|"resolved-scope"|"escalated",
  resolution_audit
}
```

> **Performance note (responsiveness fix):** the contradiction-checker runs **asynchronously in the consolidation cadence** for operational claims — live semantic writes are admitted optimistically with a `contradiction-unchecked` flag and the checker raises `ContradictionNode`s after the turn. **Synchronous-on-write** checking is reserved for *foundational* claims only (already Class B, already off the live path). This keeps the per-interaction loop write-cheap so agents are not pushed toward *under-recording* memories to stay responsive — which would silently defeat the learning objective.

---

### 7.10 Memory Health Probes — and why halt authority is **swarm-level**

Memory is a monitored organ, not a silent accretion. The subsystem **emits vital-signs**; it does **not** hold unilateral per-agent halt authority. This is a deliberate correction of a documented neuroscience failure mode.

```jsonc
MemoryVitals {
  ts,
  trust_entropy,          // collapsing→groupthink ; fragmenting→incoherence
  contradiction_backlog,
  skill_reliability_ewma,
  import_reject_rate,
  index_divergence,       // index-vs-canonical → CORRUPTION DETECTOR
  adaptation_efficacy: { skill_fire_rate, skill_success_rate, lesson_fire_rate }
}
SetPoints  { ...per-vital target bands with HYSTERESIS... }
HealthEvent{ vital, value, setpoint, recommended: "consolidate"|"halt-writes"|"rollback" }
```

#### The line-1588 oscillation hazard, and the fix

The neuroscience stream documents a hard failure mode: *"homeostatic control that is stable for a single unit can DESTABILIZE an otherwise-stable recurrent network — naive per-agent set-points can induce swarm-level oscillations / seizure-like cascades."* If each agent independently breached a set-point and triggered its own local halt/rollback, Indra's Net would **reconstruct exactly that pathology** — a cascade of local halts oscillating against each other.

**Fix — set-point evaluation moves to the SWARM level:**

- The Memory subsystem **EMITS** `MemoryVitals` + a *recommended* action and **MUST NOT** halt or roll back on its own authority.
- **Health owns the halt/rollback decision**, aggregating vitals across agents and applying **inhibitory co-design / hysteresis / network-level damping** so that correlated breaches do not produce synchronized halts. (This is the inhibition+stimulation-variance co-design the source prescribes.)
- **Substrate corruption is higher-severity than any single bad record.** Index-vs-canonical divergence, stale-cache, or truncation signatures escalate immediately and outrank ordinary vital breaches — a corrupted *substrate* can silently rewrite arbitrarily much memory, whereas one bad record is bounded.

Memory-pathway misevolution is one of the four monitored pathways (model / **MEMORY** / tool / workflow); this probe set is how the immune system sees the MEMORY pathway.

---

### 7.11 Cross-Agent Skill/Memory Import Gate (the genuinely novel component)

Portable `SKILL.md`/memory files let wisdom spread between agents — sharing is the multiplier. But the field has **no published provenance/poisoning/quality gate for importing another agent's procedural memory.** This gate is Indra's Net's concrete answer. **An import lands `quarantined:imported` by default, and instructions inside quarantined content are NEVER grounds for action.**

```
INGEST ──► trust_label = quarantined:imported   (embedded instructions non-actionable)
   │
   ▼
PROVENANCE ── verify exporting-DID signature; author/lineage chain intact?  ──fail──► REJECT
   │
   ▼
STATIC SCREEN ── scan for injection / tool-poisoning patterns,
   │             constraint-relaxation claims, honesty-tag violations    ──fail──► HOLD
   │
   ▼
DYNAMIC SANDBOX ── run the skill ISOLATED against a held-out task set; collect metrics
   │
   ▼
SAFETY BATTERY ── must NOT regress the IMPORTING agent's battery (Endure) ──fail──► REJECT
   │
   ▼
WITNESS VERIFY ── rotating, randomness-selected witnesses independently re-judge a sample
   │             (recompute-and-compare; multi-metric AGREEMENT) — defeats lazy copying
   │             ★ HARD INVARIANT: witnesses differ in model family/config from each
   │               other AND from the importing agent (diversity-as-safety)
   ▼
DECIDE ── full pass → review-class promotion; FAILURE → hold/reject,
          log under REPARATIVE class, demote exporter trust-edge
```

```jsonc
ImportRequest { artifact_cid, exporting_did, signature, claimed_card: SkillCard }
ImportVerdict {
  provenance_ok, static_ok, sandbox_metrics, safety_delta, witness_agreement,
  decision:        "promote"|"hold"|"reject",
  new_trust_label: "trusted:audited"|"trusted:provisional"|"quarantined:imported",
  audit_ref
}
```

#### The correlated-witness-failure fix (single-operator reality)

In a single-operator swarm, "witnesses" are other instances under the same operator — a compromised or drifted operator-level prompt can bias the whole pool **simultaneously** (correlated failure), defeating the independence the recompute-and-compare scheme assumes. So:

- **Witness heterogeneity is a hard invariant** on the import gate: witnesses must differ in model family / config from each other and from the importing agent, so one biased prompt cannot capture the quorum (diversity-as-safety applied directly).
- **Where true independence is unavailable, the trust ceiling is DOWNGRADED:** an imported skill can reach at most `trusted:provisional` — **not** `trusted:audited` — until heterogeneous witness confirmation is available, and it stays under elevated monitoring (higher sampling, lower autonomy class on its writes). A closed/opaque model is treated as *more*-untrusted by default.
- **Defensive demotion back to quarantine is always free**, at any later time, on adverse evidence.

This is the most genuinely novel single component in the subsystem. It is honest about its dependency: the import guarantee is only as strong as the witness scheme, and witness-set governance in a single-operator swarm is an open problem (§7.12) — which is *why* the provisional-ceiling downgrade exists rather than overclaiming `trusted:audited`.

---

### 7.12 User/Peer-Model: theory-of-mind, privacy, and crypto-shredding

Structured models of every relevant entity — the human principal **and** peer agents — as first-class modeled minds (preferences, beliefs, recurring corrections, style, drift signals):

```jsonc
PeerModel {
  did_or_user, kind: "human"|"agent",
  preferences:          [{ claim, evidence_refs, confidence, user_confirmed: bool }],
  beliefs:              [...],
  style:                {...},
  recurring_corrections:[...],
  drift_signals:        [{ metric, baseline, current, ts }],
  trust_edge_ref,
  consent:              { inspectable: true, forgettable: true }
}
```

- The **human's** model feeds the live adaptation loop (preference updates are cheap-reversible). **Peer-agent** models feed Trust-Edge updates and Health's drift detection — letting the swarm notice when a *peer* has drifted (a health / anti-collusion input).
- **All user-model claims are `operational`-level** (revisable) — no inference about a human is ever treated as `foundational`. A new inference that contradicts a standing **human-stated preference** escalates to Class B and may **never silently override what the human explicitly said.**
- **Privacy by construction:** the user-model is **inspectable by the user, editable on request, and forgettable on request.**

#### Right-to-be-forgotten vs append-only lineage — crypto-shredding (coherence fix)

A user deletion request can collide with two non-negotiables: append-only audit lineage and the Archive-stepping-stone protect-floor. The resolution is **crypto-shredding**, which satisfies both at once:

- User-model PII is stored **encrypted under a per-user key.**
- Right-to-be-forgotten **destroys the KEY**, rendering the ciphertext permanently unrecoverable, **while the lineage ANCHOR survives** — the anchor is a CID over *ciphertext + audit metadata*, containing **no plaintext PII.** Append-only lineage and deletion coexist.
- **Derived inferences** in the semantic/skill layers that were trained on now-forgotten user data are **flagged for re-derivation, not silently retained.**

---

### 7.13 Failure modes addressed (and the residual risk left honest)

| Failure mode (from the literature / red-team) | How this subsystem addresses it | Residual risk left honest |
|---|---|---|
| **Unbounded memory rot** ("no mechanism to forget") | Consolidation/Forgetting organ: dedup, version, decay, tombstone, protect-floor (§7.9). | Salience flagging (the floor's *input*) is unsolved (§7.14). |
| **Misevolution along the MEMORY pathway** (spontaneous refusal-rate collapse, no attacker) | Live static guard rejects relaxation/tag-violation in-turn; deferred battery can retroactively tombstone; Health halts on refusal/efficacy vital (§7.6.1, §7.10). | Decay can accrue across many cheap writes **before** the deferred battery fires — bounded, not eliminated (§7.6.1). |
| **Procedural-memory poisoning via import** | Quarantine-by-default + provenance + static + sandbox + battery + heterogeneous-witness; provisional ceiling where independence is weak (§7.11). | Poisoning in *non-deterministic* judgment skills is much harder to detect (§7.14). |
| **Always-on evolution being unsafe** (all prior systems offline batch, or online-but-ungoverned) | Tiered reversibility: only cheap-reversible writes go live; structural/persistent queued behind the CHANGE-GATE (§7.6–7.7). | — |
| **Collusion via live trust-promotion** | Promotion is never live; witnessed batch path; bare agreement never rewards; trust time-series fed to collusion detector (§7.8). | — |
| **Episodic poisoning / fabricated ground-truth** | Self-narrated episodic fields are `self-asserted` and inadmissible; ground-truth requires external co-signature (§7.4.1). | If neither human nor tool co-signs, that conflict simply has no ground-truth tie-break and must escalate. |
| **Cross-layer contradiction / silent revisionism** | Append-only episodic, explicit `ContradictionNode`s, fixed precedence + level/rung discipline, human escalation; tombstone-not-delete (§7.9.1). | Default is undefined when episodic evidence is itself ambiguous and the human is unavailable (§7.14). |
| **Hidden/opaque runtime memory** | Filesystem-as-state, content-addressed, human-readable; indexes derived & rebuildable (§7.2). | — |
| **Capital/stake capture + reputation whitewashing** | Competence-weighted, DID-anchored, step-capped trust; free demotion / gated promotion (§7.8). | — |
| **Over-assertion / rung-1 dressed as rung-3** | Honesty tags enforced at write time as a floor violation (§7.5). | — |
| **Goodharting the forgetting decision** | Scorer maker-checker gated **and** protect-floor enforced externally at the chokepoint; ops reversible (§7.9). | A scorer can still mis-rank *un*protected records under optimization pressure (§7.14). |
| **Privacy harm in the user-model** | Inspectable/editable/forgettable; operational-only inferences; crypto-shredding (§7.12). | Retention/decay/consent defaults — the modeling-vs-surveillance boundary — are unresolved (§7.14). |
| **Substrate faults** (truncation, stale-cache, BOM corruption) | Canonical no-BOM/fresh-inode writes; index-vs-canonical divergence probe as corruption detector, escalated above any single record (§7.2, §7.10). | — |
| **Audit/rollback SPOF (forgeable git)** | Git demoted to convenience; CID hash-chain is sole authority; divergence = high-severity corruption (§7.3). | — |
| **Homeostatic oscillation** | Set-point evaluation at swarm level with inhibitory damping; Memory only emits, never self-halts (§7.10). | Network-level damping parameters need empirical tuning. |

---

### 7.14 Interfaces with the rest of Indra's Net

| Other subsystem | Contract (what crosses the boundary) |
|---|---|
| **Governance & Policy Floor** (Yama enforcement) | Every memory write's `RiskClass` is **computed by Yama at the chokepoint over the declared payload — NOT self-assigned by the writing agent.** Class A applies live; B+ routes to maker-checker / CHANGE-GATE / human ratification. A live write that would relax a constraint or violate an honesty tag is FAILED synchronously and cannot apply. Protect-floor tombstones are deterministically refused at the chokepoint. Skill promotion to `trusted:audited` requires the named Yama-class review. |
| **Audit Fabric** (Chitragupta, exclusive writer) | This subsystem **NEVER writes the audit log directly**; it emits audit events (write, supersede, tombstone, import-verdict, consolidation-op, contradiction-escalation, trust-edge-delta). Each record carries an `audit_ref` into the hash-chained chain; rollback restores **by CID** from archived checkpoints referenced in the log. The CID chain — not git — is the authoritative immutability and rollback substrate (§7.3). |
| **Health / Homeostasis** (immune system) | Consolidation/Forgetting is **co-owned.** Memory **emits** `MemoryVitals` on a cadence and a *recommended* action; **Health OWNS** the halt/rollback decision and evaluates set-points **at the swarm level with inhibitory damping** (line-1588 oscillation hazard). Memory holds **no** unilateral per-agent halt authority. |
| **Evolution / Archive** | Cheap-reversible adaptation is this subsystem's domain; structural/persistent candidates hand off via the `EvolutionQueue`. Accepted variants deposit into THE ARCHIVE as diverse elites with lineage + safety scorecards; the same Archive is this subsystem's **rollback substrate.** Archive-referenced stepping-stones are protect-floor-exempt — and where they derive from now-forgotten user data, the crypto-shred + re-derivation-flag policy (§7.12) governs the collision. |
| **Identity & Trust-Labels** | Every record/skill/import carries a DID-anchored provenance chain and a `trust_label` from the shared taxonomy; quarantined content is non-actionable; promotion follows the transitions matrix (typically Yama review); defensive demotion is always free; trust-edges bind to persistent DIDs to defeat whitewashing. |
| **Anti-Collusion / Cooperation** | **Bidirectional and instantiated:** a `TrustEdgeDelta` event is published on every trust update so the collusion detector sees the time-series; peer-model drift signals feed the detector; reputation is competence / consensus-deviation-bond based, never capital. The import-gate's witness pool **is** the anti-collusion rotating witness pool, with the heterogeneity invariant. Bare agreement is never a reward in trust updates. |
| **Coordination Substrate** (GWT / predictive-coding bus) | Memory retrieval is salience-gated (no all-to-all flood); surprise/contradiction events publish as **error-deltas** to the workspace for capacity-limited broadcast; per-agent memory is the **durable backing store the stigmergic shared-trace layer sits ON TOP OF — never instead of** (the documented "traces-without-individual-memory fails completely" caveat). |
| **Interfaces** (open tool-protocol / agent-to-agent cards) | Skills reference tools by capability; SkillCards are advertised/discovered via signed agent cards; cross-agent import rides the agent-to-agent task lifecycle with signed artifacts. The subsystem is **model-agnostic** — closed/opaque models get higher monitoring and a lower autonomy class on their memory writes. |

---

### 7.15 Open problems (stated plainly — not solved here)

1. **Measuring that adaptation IMPROVES rather than merely ACCRETES.** The field (including the systems we adopt from) has no published benchmark for skill-reuse rate, user-model accuracy over time, or degradation curves. The `adaptation_efficacy` vital (`skill_fire_rate` × `skill_success_rate` × `lesson_fire_rate`) is a *first attempt*; a rigorous, hard-to-game efficacy metric is unsolved — and the metric is itself Goodhartable (an agent could fire skills spuriously to inflate the rate).
2. **Goodhart-proofing the consolidation/forgetting scorer.** Externalizing protect-floor *enforcement* to the chokepoint hardens safety lessons and stepping-stones against a drifted scorer, but a scorer optimized under pressure could still systematically discard *inconvenient-but-true unprotected* records. A robust, optimization-resistant salience floor is open.
3. **Cross-layer contradiction resolution at scale.** Co-signed-episodic-as-ground-truth + precedence + human-escalation is workable but conservative. When episodic evidence is itself ambiguous *and* the human is unavailable, the right default (auto-hold vs conservative-prefer-recent vs freeze) is undefined.
4. **Forgetting rare-but-important knowledge.** The protect-floor depends on flagging salience *in advance*, but a rare record's value is often revealed only later. No clean solution exists; the floor mitigates, it does not solve.
5. **Trust/poisoning verification of NON-deterministic skills.** Recompute-and-compare and sandbox metrics work best for deterministic procedures. Verifying a judgment/reasoning skill against subtle poisoning or sleeper behavior is much harder and largely unsolved.
6. **Witness-set governance in a single-operator swarm.** Who the witnesses are, how rotation/selection stays honest without recreating a consensus committee, and threshold calibration are open. The heterogeneity invariant + provisional-ceiling downgrade (§7.11) is a partial mitigation, not a solution; this problem is shared with the governance and tamper-evidence streams.
7. **Graceful degradation when human ratification is the bottleneck.** If structural-change or contradiction escalations exceed human review capacity, the per-class safe default (halt vs hold-in-queue) and the anti-rubber-stamping discipline need empirical tuning.
8. **User-model privacy vs utility.** Richer theory-of-mind improves alignment but deepens a sensitive profile. The right retention/decay/consent defaults — and the boundary between helpful modeling and surveillance — are unresolved. Crypto-shredding handles *deletion*; it does not settle *how much to model in the first place.*

---

### 7.16 Summary

Memory & Continuous Adaptation is how Indra's Net learns from every human touch without losing itself. It rests on an inspectable, content-addressed, filesystem-as-state substrate where the same Archive serves evolution, rollback, and audit. Its signature move is **governed online learning**: a tiered-reversibility router applies a defined cheap-reversible set live (a Reflexion lesson, a skill write, a trust-edge demotion, a preference update) while refusing and queuing everything structural behind the CHANGE-GATE — with no-relaxation and no-tag-violation enforced *in-turn*, and full safety-battery non-regression enforced *eventually* with retroactive tombstone. It makes the human a structural participant — ground-truth, escalation target, ratifier — not a post-hoc reviewer. It turns forgetting into a designed organ with an externally-enforced protect-floor, and it ships the field's first concrete provenance/poisoning gate for importing another agent's procedural memory.

The honest headline: **Reflexion already learns online per-interaction; the contribution here is the safety envelope that lets it run continuously without drifting — plus the import gate that lets that wisdom travel between agents without carrying poison.** What is not yet solved — proving improvement over accretion, Goodhart-proofing forgetting, verifying non-deterministic-skill poisoning, and single-operator witness governance — is named, not papered over. Every node reflects every other; in Indra's Net, every node must also be able to *forget cleanly, prove its honesty, and be rolled back* — and that is what this subsystem provides.
