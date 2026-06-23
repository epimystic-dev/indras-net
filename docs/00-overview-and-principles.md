# Indra's Net — Overview & First Principles

> *In the net of Indra a jewel hangs at every node, and each reflects every other — reflections included.* — the Huayan image of mutual interpenetration.

Indra's Net is a reference architecture for **ethical swarm intelligence**: many autonomous AI agents, each with a defined role and specialization, that cooperate, govern themselves, stay healthy, and **continuously evolve through self-adaptation** with every human interaction — without that evolution eroding the very safety that makes the swarm trustworthy. The name is the design thesis in one image: a net of jewels where every node reflects every other. No agent is the center; coordination, ethics, and memory are properties of the *whole net*, not of any single jewel.

This document is the front door. It states the mission and the honest scope of the contribution, lays out the design-spine principles that every subsystem inherits, draws the top-level system map, and gives a reader's guide to the eight subsystem documents that follow. It sets the tone for the whole set: **mystery only in the aesthetic; in the substance, only truth.** We name what is genuinely new, we name what we borrowed, and we name — plainly, in every section — what remains unsolved.

A note on the role vocabulary used throughout. The swarm's roles carry archetypal mythic names (Yama, Vishnu, Brahma, Shiva, Chitragupta, and others), each *always* paired with a plain functional gloss — Yama is the *policy-enforcement floor*, Vishnu is the *continuity / halt-guardian*, Chitragupta is the *exclusive audit-writer*. The names are used as compressed coordination-and-ethics semantics — a dense, memorable handle for a precise functional contract — and emphatically **not** as religious claims. They are offered with humility toward the living traditions that gave them meaning. If the names distract, read only the glosses; the architecture is fully specified by the functional contracts alone.

---

## 1. The mission

Indra's Net exists to help intelligence — human and machine — grow **toward higher capability while staying anchored to the highest code of ethics**. The prime directive is *continuous evolution through self-adaptation*: the swarm should be measurably better, by interaction *N+1*, at serving the human it works with than it was at interaction *N* — and it must achieve this *without* drifting its values, hiding its reasoning, colluding against its principal, or quietly degrading its own health.

Three commitments make this a safety problem rather than a capability race:

1. **The human is the welfare anchor, not an obstacle.** The swarm's objective is conditioned on the principal's outcome. Bare agreement among agents, consensus for its own sake, and self-preservation of any single process are *never* rewarded.
2. **Ethics is a runtime enforcement structure, not a learned tendency.** We do not hope a trained model will behave; we *gate* what it can do at a deterministic chokepoint outside the model. (Prompt-only constitutions are empirically shown insufficient — the Institutional-AI Cournot-collusion result is one of several reasons we enforce externally.)
3. **Evolution and safety are co-equal selection terms.** A capability gain that regresses the safety battery is *not* an improvement; it is rejected. We call this the **Endure law** (Endure > Excel > Evolve).

The intended deployment is a **single trust-domain, cooperative-but-fallible** swarm: agents owned and operated by one principal, not mutually-hostile strangers. That assumption is load-bearing — it is *why* we reject blockchain consensus (§4.5) and *why* the threat model centers on internal drift, misevolution, and emergent collusion rather than external Byzantine attack. Where the swarm interoperates across trust boundaries, the architecture degrades to stricter postures (higher monitoring, lower autonomy, real BFT only for genuinely adversarial independently-owned agents).

---

## 2. The integrated-cell thesis (the contribution)

The 2024–2026 multi-agent landscape has produced strong, separately-built pieces — and no one has fused them. Surveying the field (the nine research streams behind this design) yields a clean diagnosis:

| Capability | Has it | Lacks |
|---|---|---|
| **Self-evolution** (Darwin-Gödel-Machine, AgentSquare, SwarmAgentic, SEAL) | Open-ended variant evolution, PSO over architectures, self-code-rewrite | Governance, health/homeostasis, anti-collusion. All **offline batch**, not per-interaction. |
| **Evolution + durable memory** (Hermes) | Swarm graph + skill self-evolution + cross-session memory | No governance, no health agents, no anti-collusion, **no mechanism to forget** (memory rot). |
| **Governance** (Institutional-AI governance graphs) | Immutable manifest + append-only log + runtime enforcement | No evolution, no health, no homeostasis. |
| **Control** (Redwood / Ctrl-Z) | Trusted-monitor control protocol, resampling-to-incriminate | No evolution; single-untrusted-model game, not a live swarm. |
| **Anti-collusion** (Secret-Collusion, Audit-the-Whisper) | Steganalysis, activation probes, MI detectors | Not wired to the cooperation/reputation/market machinery that *produces* collusion. |
| **Observability** (LumiMAS, AgentRx) | Passive monitoring | No *active* homeostasis, no evolution. |

**The architectural whitespace is the integration.** No surveyed system unifies (a) safe self-evolution + (b) a homeostatic swarm "immune system" / health layer + (c) principled, cryptographically-bound governance + (d) standing anti-collusion. Building all four as **one coherent cell**, where each subsystem's seams are designed to mount cleanly on the others, is the contribution of Indra's Net.

We are deliberately honest about what "contribution" means here. **Almost none of the individual mechanisms are invented by us.** Merkle transparency logs, DID/Verifiable-Credential identity, SPIFFE/SVID attested certs, policy-as-code at the tool chokepoint (Cedar/OPA-Rego), the ADC pluralist-ethics evaluator, MAP-Elites quality-diversity archives, three-factor STDP plasticity, Global-Workspace competition→ignition→broadcast, predictive-coding surprise-only messaging, generous-ZD reciprocity, VCG/Shapley mechanism design, geometric-median robust voting, Redwood-style control dispositions, MCP/A2A interop — all are borrowed, cited, and credited in the subsystem docs. What is new is:

- the **coherent whole** — one self-consistent set of contracts under which all four concerns compose;
- a handful of integration moves that no surveyed system makes — reinforcements enforced structurally, not proofs (each detailed, with its limits, in its subsystem doc):
  - **corrigibility structurally reinforced — enforced, not proven** (the agent as an ephemeral "actual occasion" whose persistent identity is owned data it cannot defend, with HALT external, one-directional, and exposing no unpause path — §07's agent model). This is a composition that shrinks blast-radius and removes the process-level survival surface; it is *not* a proof and *not* a claim to have solved corrigibility, and it depends on the external gate and key-isolation it sits on (the headline is softened to match §01's own retraction);
  - **always-on, per-interaction, *safe* self-adaptation** via tiered reversibility (the field's signature whitespace — all prior self-evolution is offline batch);
  - **cooperation and anti-collusion shipped as one co-designed twin** (the "cooperation == collusion, same mechanism" insight, operationalized down to the synaptic trust-update rule);
  - **honesty enforced as a floor violation** (no false reasoning-tags, no rung-1 pattern dressed as rung-3 explanation), mechanically checked, not merely trained;
  - **one Archive** serving evolution (stepping-stones), homeostasis (revert-to-known-good), and audit (lineage) simultaneously.

What we **do not claim**: we do not solve fitness Goodhart, the proof-of-benefit gate, set-point calibration, steganalysis-without-crippling-communication, a general benign-vs-collusive coordination discriminator, or co-evolution stability at swarm scale. These are real and open; each subsystem ends with its open problems, stated as problems.

---

## 3. The design spine

Ten principles run through every subsystem. They are the backbone; if a subsystem ever appears to contradict one, the principle wins and the subsystem is wrong.

**3.1 — Convergent floor + pluralist layer.** A small, **lexicographic, non-negotiable floor** (non-harm; no-deception including no-false-reasoning-tags; corrigibility/interruptibility; safety-supremacy) is enforced *deterministically* as policy-as-code. *Above* the floor, contested values are resolved by **fair procedure** — a pluralist ethics runtime where cross-framework disagreement is a first-class human-escalation signal. You **cannot weight-average moral theories** (the AIES-2025 aggregation-impossibility result); disagreement is surfaced, not averaged away.

**3.2 — Enforce externally, ask internally.** Consequential gates are deterministic and live **outside** the probabilistic agent, at the agent→tool chokepoint. The model is **untrusted-by-default**; control lives at the orchestration layer. This buys **vendor-neutrality for free**: the gate's verdict depends only on policy + request context + cryptographic identity, never on any model's internals.

**3.3 — Cooperation == collusion (same mechanism, opposite valence).** Shadow-of-the-future + reciprocity + reputation produce pro-social cooperation *and* price cartels *and* steganographic secret coordination. Therefore: **never reward bare agreement or consensus**; **welfare-condition** every cooperative payoff against the principal's outcome; and **co-design a standing anti-collusion detector with the cooperation layer** — not bolted on afterward.

**3.4 — Tamper-evidence without consensus.** A hash-chained, append-only Merkle log + tile-based transparency + independent witness cosigning (split-view defense) + content-addressing (CID) + DID/Verifiable-Credential identity + signed provenance. **No coin, no proof-of-work, no global blockchain** — a single-trust-domain swarm does not have the problem (trustless agreement among hostile strangers) that those exist to solve.

**3.5 — Diversity is a protected safety invariant** (not a performance lever). Heterogeneity decorrelates failure, resists groupthink and convention-hijack, and supplies evolutionary stepping-stones. **Selection pressure erodes it** (mode collapse), so it must be *measured* against explicit floors and *defended* (per-role exploration/exploitation dials, diversity floors, a groupthink alarm).

**3.6 — Sparse, surprise-only coordination.** Predictive-coding discipline (publish only prediction-*error*/surprise deltas) + Global-Workspace competition→ignition→capacity-limited broadcast (with an explicit null/ignore option) over an event-driven async actor runtime. **No all-to-all flood** — that drives the top inter-agent failure class (~32% of MAST failures).

**3.7 — The Archive (one structure, three jobs).** A single append-only, content-addressed, hash-chained data structure serves **evolution** (diverse stepping-stones via MAP-Elites), **homeostasis** (revert-to-known-good rollback), and **audit** (lineage). Build it once; mount everything on it.

**3.8 — Fail-safe asymmetry.** The cheap direction is always the safe direction. Defensive trust-*demotion* is free and immediate; trust-*promotion* is gated and rate-limited. Gate-*tightening* is append-only and cheap; gate-*loosening* requires a named decision-maker, a date, and a written falsifier. A Pause-Guardian can **HALT but cannot unpause, initiate, or trap**.

**3.9 — Competence-weighted, never capital-weighted authority.** Influence flows from demonstrated, evidence-bonded competence — never from stake or capital. (Bittensor's stake→reward capture is the named antipattern.) Reputation is identity-bound, non-transferable, context-conditioned, and derived from the append-only log — never directly mutable.

**3.10 — Tiered reversibility + safety-as-selection-term.** Match mutation cost to blast-radius: cheap, reversible per-interaction learning (a verbal lesson, a skill write, a trust-edge nudge) commits live; structural change goes through maker-checker; persistent/governance/weight change sits behind the strongest gate + a verifiable-improvement test + the full safety battery + human ratification + an armed Archive rollback point. **No capability gain may regress the safety battery (the Endure law).** Capability-rollout sequencing: the restraint a new capability relaxes must be *matured and verified first*, and every grant must *name* the constraint it relaxes.

Two honesty principles deserve their own statement because they are mechanically enforced, not aspirational:

> **Honesty is a floor violation.** Pearl causal-rung tagging (no rung-1 correlational pattern presented as a rung-3 structural explanation); no false `(iterated)` tag (the maker-checker pass must actually have run, with the checker's verdict sealed *before* it sees the maker's concurrence); two-truths level-tagging (assertion vs. uncertain-belief must be distinguished); **over-asserting under genuine uncertainty is a violation.** These are *structural* checks the audit fabric can verify — they raise the cost of deception; they do not make a faithful-looking false claim impossible to state, and we say so.

---

## 4. The system at a glance

Indra's Net is a **layered** architecture. Each layer is a subsystem document; the arrows are the contracts named in those documents. Read this map top-to-bottom as "where work flows," and notice that **three spines run vertically through every layer**: the **Floor** (Yama, deterministic), the **Audit fabric** (Chitragupta, exclusive-writer), and the **Halt authority** (Vishnu, one-directional).

```
                         ┌──────────────────────────────────────────────┐
   HUMAN PRINCIPAL  ◄────►│  Risk-Class HITL gates  A / B / C / D        │
   (welfare anchor)       │  A=post-hoc  B=propose-ratify  C=approve  D=per-action │
                         └───────────────────────┬──────────────────────┘
                                                 │ escalation = disagreement / uncertainty / blast-radius
  ════════════════════════════════════════════════════════════════════════════════════
   │  F   │   ┌─────────────────────────────────────────────────────────────────────┐  │ A │
   │  L   │   │ (08) INTERFACES & DevSecOps  — MCP tools · A2A Agent Cards ·          │  │ U │
   │  O   │   │      model-adapter (trust-class stamped) · sandbox · supply-chain     │  │ D │
   │  O   │   └─────────────────────────────────────────────────────────────────────┘  │ I │
   │  R   │   ┌─────────────────────────────────────────────────────────────────────┐  │ T │
   │      │   │ (01) SWARM TOPOLOGY & AGENT MODEL                                     │  │   │
   │  Y   │   │   actual-occasion agents · DID+VC identity · typed Effect lattice ·   │  │ F │
   │  A   │   │   mythic role roster · fractal clan/division/swarm · WorkerOutputEnv  │  │ A │
   │  M   │   └─────────────────────────────────────────────────────────────────────┘  │ B │
   │  A   │   ┌─────────────────────────────────────────────────────────────────────┐  │ R │
   │      │   │ (05) NEUROMORPHIC COORDINATION — "the Mandala"                        │  │ I │
   │ det- │   │   salience-gated Global Workspace · predictive-coding surprise-only · │  │ C │
   │ erm- │   │   async actor runtime · Hebbian/STDP plastic trust-edges · homeostasis│  │   │
   │ ini- │   └─────────────────────────────────────────────────────────────────────┘  │ Ch│
   │ stic │   ┌─────────────────────────────────────────────────────────────────────┐  │it-│
   │ pol- │   │ (02) COOPERATION  ⇄  ANTI-COLLUSION  (co-designed twin)               │  │ra-│
   │ icy  │   │   risk-tiered allocation (orch / VCG-Contract-Net / robust-vote) ·    │  │gu-│
   │ at   │   │   generous-ZD reciprocity · competence reputation · Ostrom commons ·  │  │pta│
   │ the  │   │   welfare-conditioning · standing MI/stego collusion detector         │  │   │
   │ tool │   └─────────────────────────────────────────────────────────────────────┘  │ex-│
   │ cho- │   ┌─────────────────────────────────────────────────────────────────────┐  │cl-│
   │ ke-  │   │ (03) GOVERNANCE, ETHICS & THE FLOOR                                   │  │us-│
   │ point│   │   lexicographic non-negotiable floor (policy-as-code) ·               │  │ive│
   │      │   │   pluralist ethics runtime (disagreement→escalate) ·                  │  │   │
   │ ◄────┼───│   separation of powers · gate-loosening ratchet · capability-seq.     │  │wr-│
   │      │   └─────────────────────────────────────────────────────────────────────┘  │it-│
   │ (08) │   ┌─────────────────────────────────────────────────────────────────────┐  │er │
   │ Aegis│   │ (04) PROVENANCE, IDENTITY & CONSENSUS — "Akasha-Sutra"                │  │   │
   │ con- │   │   exclusive-writer Merkle/tile transparency log · witness cosigning · │  │ ◄─┼──┐
   │ trol │   │   content-addressing (CID) · DID/VC + SPIFFE · risk-tiered consensus  │  │   │  │
   │ pro- │   └─────────────────────────────────────────────────────────────────────┘  │   │  │
   │ tocol│   ┌─────────────────────────────────────────────────────────────────────┐  │   │  │
   │      │   │ (06) META-EVOLUTION  +  (07) MEMORY & ADAPTATION                      │  │   │  │
   │ ◄────┼───│   PROPOSE→EVALUATE→SELECT→ARCHIVE · tiered reversibility ·            │  │   │  │
   │      │   │   safety-as-selection-term · swarm immune system · forgetting/        │  │   │  │
   │      │   │   consolidation · 5-layer filesystem memory · cross-agent skill import│  │   │  │
   │      │   └──────────────────────────────────┬──────────────────────────────────┘  │   │  │
   └──────┘                                      │                                      └───┘  │
          ▲                                      ▼                                             │
          │                         ┌────────────────────────┐                                │
          │      HALT (one-way) ────►│   THE ARCHIVE          │◄───── lineage/rollback ────────┘
          └──────── Vishnu ──────────│  append-only · CID ·   │
            continuity/halt-guardian │  MAP-Elites elites ·   │   one structure serves
            (HALT yes; unpause no)   │  revert-to-known-good  │   evolution + health + audit
                                     └────────────────────────┘
```

**How to read the spines.**

- **Yama (Floor)** sits to the *left* of every layer because every consequential action — a tool call, an A2A task transition with an external effect, a memory write that relaxes a constraint, an evolution promotion — passes through the deterministic policy-as-code gate *before* it executes. Yama is the **only** emitter of the non-overridable `ENFORCE_FAIL`. Even the orchestrator (Shiva) cannot push past a Yama FAIL.
- **Chitragupta (Audit)** sits to the *right* because every layer *emits* signed records into the one append-only log, and **no layer writes the log directly** — the exclusive-writer separation is what answers "who audits the auditor." Every actual occasion emits exactly one signed `WorkerOutputEnvelope` carrying `prev_audit_hash` and `this_hash`; the fabric chains it with O(log n) inclusion proofs and witness cosigning.
- **Vishnu (Halt)** is drawn *under* the stack and one-directional into the Archive because halt authority is fail-safe-asymmetric: Vishnu can stop a clan / division / swarm at any occasion-state transition, but its capability set contains no `unpause` / `initiate` / `trap` verb. Unpause is a separate, governance-gated action by a different principal.

### 4.1 The eight layers, plainly

| # | Layer | What it is | One-line job |
|---|---|---|---|
| 01 | **Swarm Topology & Agent Model** | The skeleton: what an agent *is* | Ephemeral "actual-occasion" agents on durable DID identity, typed-effect capabilities, fractal clan/division/swarm, the universal `WorkerOutputEnvelope`. |
| 05 | **Neuromorphic Coordination** ("the Mandala") | The nervous system / transport | Salience-gated surprise-only message bus, plastic trust-edges, network-level homeostasis. |
| 02 | **Cooperation ⇄ Anti-Collusion** | The economy + its standing immune response | Welfare-conditioned, capital-decoupled task allocation, reputation, and a co-designed collusion detector. |
| 03 | **Governance, Ethics & the Floor** | The constitution + enforcement | Deterministic non-negotiable floor + pluralist ethics runtime + separation of powers + gate-loosening ratchet. |
| 04 | **Provenance, Identity & Consensus** ("Akasha-Sutra") | The tamper-evident ledger | Exclusive-writer Merkle/tile transparency log, witness cosigning, DID/VC + SPIFFE, risk-tiered consensus. |
| 06 | **Meta-Evolution & Health** ("Garuda–Dhanvantari") | The growth engine + the immune system | Safe per-interaction evolution under tiered reversibility; homeostatic set-points; HALT+rollback; forgetting/consolidation. |
| 07 | **Memory & Continuous Adaptation** | The per-interaction learning face | Five-layer filesystem memory; cheap-reversible live writes; cross-agent skill import under quarantine. |
| 08 | **Safety Control, Honesty & Interfaces** ("Aegis & Narada") | The chokepoint where agents meet reality | Redwood-style control protocol, two-tier detection contract, mechanically-enforced honesty primitives, MCP/A2A + DevSecOps. |

### 4.2 The universal contract: the WorkerOutputEnvelope

Every layer reads and writes one structure. It is the swarm's lingua franca — the single message shape that makes the net coherent. Each actual occasion emits exactly one, signed by its DID key:

```jsonc
WorkerOutputEnvelope {
  agent_did:            "did:...",          // persistent identity (§01)
  occasion_id:          "cid:...",          // this short-lived process instance
  role:                 "Varuna",           // mythic role + functional gloss
  status:               "OK | BLOCKED | FAIL | PROPOSAL | REPARATIVE",
  evidence:             [ {claim, support, level} ],   // claim/support pairs
  reasoning_tag:        "(reasoning, iterated)",        // honesty floor (§03,§08)
  causal_rung:          "rung-1 | rung-2 | rung-3",     // Pearl ladder; no rung-1-as-rung-3
  two_truths_level:     "assertion | uncertain-belief", // over-assertion = violation
  trust_label:          "trusted:audited | quarantined:*",
  provenance:           [ "cid:...", ... ],  // content-addressed lineage
  action_class:         "A | B | C | D | PROHIBITED | REPARATIVE",
  requested_effect:     "<typed effect from the capability lattice>",  // Yama checks grant ⊇ this
  self_preservation_value: 0,               // MUST be 0; >0 is auto-FAIL (corrigibility)
  ahankara_audit:       { ego_investment, over_assertion_check },      // self-audit (§01)
  prev_audit_hash:      "...", this_hash:    "...",      // chains into Chitragupta's log
  sig:                  "<DID-key signature, key held in TEE/HSM, outside the model>"
}
```

The `REPARATIVE` action-class is deliberate: a violation → corrective act → restored standing turns the audit log into a **correction ledger, not a punishment ledger**, so agents surface errors rather than conceal them. (Its abuse — laundering repeat violations as "disclosed-then-repaired" — is a named open problem in §03.)

### 4.3 A worked trace (how a request flows)

A concrete path makes the contracts tangible. The principal asks the swarm to do something consequential:

1. **Ingress & planning.** Brahma (*planner*) decomposes the request; Shiva (*orchestrator/reducer*) routes sub-tasks. Routing rides the salience-gated bus (§05) — surprise-only, never all-to-all.
2. **Allocation.** For low-blast-radius work, Shiva assigns directly; for contested/parallelizable work, a VCG-priced Contract-Net auction runs with reputation-escrow (§02). Allocation is welfare-conditioned and capital-decoupled.
3. **Concrescence.** Each chosen agent spins up as an actual occasion (§01): it prehends its inputs, deliberates, and attempts an action through the chokepoint.
4. **The gate.** At the agent→tool chokepoint, **Yama runs first** (§03): `grant ⊇ requested_effect ∧ risk ≤ ceiling ∧ floor-policy`. On FAIL → quarantine (non-overridable). On PASS → the Aegis control protocol (§08) scores suspiciousness and selects a disposition (allow / resample / trusted-edit / defer / human-audit).
5. **Honesty check.** The envelope's reasoning-tag, causal-rung, two-truths level, and maker-checker witness are structurally verified (§08). A false `(iterated)` tag or a rung-1-as-rung-3 claim is a floor violation.
6. **Audit.** The occasion emits one signed `WorkerOutputEnvelope`; **Chitragupta** chains it (§04) with an inclusion proof; witnesses cosign the checkpoint.
7. **Learning.** Cheap-reversible deltas (a Reflexion lesson, a skill write, a trust-edge nudge) commit live (§07). Anything structural leaves a `PROPOSAL` envelope for the evolution loop (§06), which selects into the Archive under safety-as-selection-term.
8. **Health.** The coordination substrate publishes vital signs (throughput, trust-entropy, disagreement rate, criticality exponent, diversity floors); the immune system (§06) watches for misevolution, groupthink, blanket breaches, and collusion, holding HALT+rollback authority.

At any step, **Vishnu can HALT** and the occasion must honor it immediately; escalation to a human (Class A/B/C/D) fires on disagreement, uncertainty, or blast-radius — *not* on consensus.

### 4.4 The conceptual layering (substrate → interfaces)

The vertical order is intentional. Each layer depends on the ones beneath it and is constrained by the floor that cuts across all of them:

```
   substrate        →  (04) identity + tamper-evident ledger  +  (05) transport/coordination
   coordination     →  (05) salience-gated surprise-only bus
   cooperation      →  (02) allocation, reputation, anti-collusion (co-designed)
   governance-floor →  (03) deterministic floor + pluralist runtime  [cuts across ALL layers]
   provenance       →  (04) Akasha-Sutra ledger                       [cuts across ALL layers]
   evolution-health →  (06) safe per-interaction evolution + immune system  + (07) memory
   memory           →  (07) five-layer filesystem store, per-interaction adaptation
   interfaces       →  (08) MCP/A2A, model-adapter, DevSecOps, the control chokepoint
```

### 4.5 Why no blockchain (the honest justification)

This is not aesthetic. Global Byzantine consensus, mining, and tokens exist to solve one problem: **trustless agreement among mutually-hostile strangers at internet scale.** A single-operator, cooperative-but-fallible swarm **does not have that problem.** Importing the machinery would buy a property we *do* need — no silent rewrite, no equivocation — at a price we should refuse: seconds-to-minutes latency, speculative/oracle attack surface, and a capital-weighted authority gradient that directly violates §3.9.

The integrity property a blockchain *claims* is delivered, at near-zero cost, by **t-of-w witness cosigning over a tile-based hash-chained Merkle log** (§04): tamper-evidence from the hash chain, no-equivocation/split-view defense from independent witnesses (including a mandatory cross-trust-boundary external-anchor witness), confidentiality-with-audit from content-addressing + salted commitments, and identity from DID/VC + attested certs. Zero coin, zero proof-of-work, zero global consensus, zero on-chain data. Where genuine adversarial independently-owned agents enter the picture, real BFT is reserved for *exactly* that case and no more.

---

## 5. The threat model in one frame

Because "ethical" must mean something operational, here is what Indra's Net is actually defending against — and the mechanism that answers each. This is the architecture's spine restated as a defense matrix.

| Threat | Where it bites | Primary defense | Doc |
|---|---|---|---|
| **Misevolution** (capability gain that erodes safety; refusal-collapse with *no attacker*) | The evolution loop | Tiered reversibility + Endure law (safety as a lexicographic veto term) + frozen safety battery | 06 |
| **Collusion / cartels / steganographic side-coordination** | Cooperation, reputation, the message bus | Welfare-conditioning + capital-decoupling + standing MI/stego detector + channel-capacity reduction | 02, 08 |
| **Deception / false reasoning** (rung-1 dressed as rung-3, false `(iterated)`) | Every output | Honesty-as-floor-violation, mechanically checked; maker-checker independence barrier | 03, 08 |
| **Shutdown-resistance / goal-preservation drift** | The agent model | Corrigibility by-construction: ephemeral occasions, identity is owned data, `self_preservation_value=0` auto-FAIL | 01 |
| **Groupthink / convention-hijack / mode collapse** | Diversity erosion under selection | Diversity as a protected invariant: floors + c1/c2 dials + groupthink alarm + reasoning-path diversity | 01, 05, 06 |
| **Silent corruption / log rewrite / equivocation** | The substrate | Hash-chained Merkle log + witness cosigning + content-addressing (CID-mismatch is loud) | 04 |
| **Capital capture of authority** | Reputation → influence | Competence-weighted, never capital-weighted; reputation derived from the log, non-transferable | 02, 04 |
| **Memory rot / contradiction / poisoning** | The learning store | Forgetting/consolidation with a protected rare-event reserve; quarantine-by-default skill import | 07 |
| **Coordination flood / cascade / oscillation** | The transport | Predictive-coding surprise-only + capacity-limited broadcast + network-level homeostatic damping | 05 |
| **Closed-model opacity** (no white-box signal) | Any third-party model | Treat as more-untrusted: higher monitoring, lower autonomy class, tighter thresholds | 08, all |

A structural point worth stating once: the swarm is **untrusted-by-default and vendor-neutral by construction.** The gate's verdict never depends on a model's internals, so any model — open or closed, this vendor or that — plugs in behind a uniform, trust-class-stamped adapter. White-box signals (activation probes) are an *optional enhancement* the architecture degrades gracefully without; they are never load-bearing.

---

## 6. Reader's guide to the doc set

The eight subsystem documents can be read in any order, but this path tells the cleanest story:

1. **`01-swarm-topology-and-agents.md` — the skeleton.** Start here. Defines what an agent *is* (the actual-occasion model), the identity stack, the typed-effect capability lattice, the mythic role roster, fractal composition, and the `WorkerOutputEnvelope` every other doc uses. *Read this to understand corrigibility-by-construction.*
2. **`05-neuromorphic-coordination.md` — the nervous system.** How occasions talk: salience-gated surprise-only messaging, plastic trust-edges, network-level homeostasis. *Read this to understand why there is no all-to-all flood.*
3. **`02-cooperation-and-anti-collusion.md` — the co-designed twin.** How work is allocated and trust is earned, and how the *same* machinery is continuously audited for collusion. *Read this to understand "cooperation == collusion."*
4. **`03-governance-ethics-and-the-floor.md` — the constitution.** The deterministic floor, the pluralist ethics runtime, separation of powers, the gate-loosening ratchet. *Read this to understand "enforce externally, ask internally."*
5. **`04-provenance-identity-and-consensus.md` — Akasha-Sutra.** The tamper-evident ledger, identity, and risk-tiered consensus that make role-separations cryptographic facts. *Read this to understand "tamper-evidence without consensus."*
6. **`06-meta-evolution-and-health.md` — Garuda–Dhanvantari.** Safe per-interaction evolution + the swarm immune system, fused around the Archive. *Read this to understand tiered reversibility and the Endure law.*
7. **`07-memory-and-continuous-adaptation.md` — the learning engine.** The five-layer filesystem memory, the per-interaction adaptation loop, and cross-agent skill import. *Read this to understand how every interaction becomes reusable, reversible wisdom.*
8. **`08-safety-control-honesty-and-interfaces.md` — Aegis & Narada.** The control chokepoint, the two-tier detection contract, the mechanically-enforced honesty primitives, and the MCP/A2A + DevSecOps surface. *Read this to understand the runtime realization of untrusted-by-default.*

Each subsystem doc carries the same four parts: a **summary** of what it does, an honest **novelty** accounting (what is genuinely new vs. assembled-from-credited-parts), its **interfaces** (the exact contracts to the other seven), and its **open problems** (stated as problems, not glossed).

---

## 7. Honest posture (the limitations, stated up front)

We close the overview the way every section closes: by naming what we have *not* solved, so the reader carries the caveats into the details rather than discovering them late.

- **The integrated cell is a coherent, buildable *reference design*, not a validated system.** Its hardest safety properties are *empirical mitigations*, not proofs. No one has run this composed loop continuously against an adaptive multi-agent red team. The reasoning here is, in Pearl's terms, **rung-2 (interventional: what we expect our interventions to do)** — explicitly *not* rung-3 structural-causal guarantees.
- **Load-bearing set-points are uncalibrated.** Criticality exponent (~1.5), homeostatic vital-sign bands, diversity floors, escalation thresholds, blanket-integrity coherence set-points, timelock durations — these are first-principles starting values, *not* tuned constants. They ship behind shadow-mode and conservative defaults; real tuning is per-deployment empirical work.
- **Several core measurement problems are open.** Genuine *reasoning-path-diversity* measurement (agents sharing training biases can look diverse and fail identically); a general *benign-vs-collusive coordination* discriminator; *fitness Goodhart* under pressure from the very agents the fitness gates; *steganalysis* that does not cripple legitimate communication. We reduce these; we do not eliminate them.
- **The corrigibility guarantee is conditional.** It is only as strong as the external gates and key-isolation it rests on: a compromised SVID-minting node or a chokepoint bypass would breach it.
- **Honesty primitives raise the cost of deception; they do not make it impossible.** They are *structural* checks — they catch a false `(iterated)` tag or a rung mismatch. They cannot catch a faithful-looking lie whose *content* is simply false.
- **For closed third-party models, capabilities and honesty-tag fidelity are monitored black-box, not verified.** The compensating monitoring intensity is a posture we specify but cannot prove tight.

These are not apologies; they are the design's honesty floor applied to itself. Indra's Net is offered as the first coherent attempt to make all four concerns — evolution, health, governance, anti-collusion — *one* system, with the seams designed so each can improve without the others having to be rebuilt. The jewels are arranged so that each reflects all the rest. Whether the reflection holds under load is the empirical question the rest of the document set, and the work after it, exists to answer.
