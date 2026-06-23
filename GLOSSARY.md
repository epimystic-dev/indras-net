# Glossary — Indra's Net

## Naming map — disambiguation (read first)

Indra's Net uses archetypal mythic names for roles and layers, each with a plain functional gloss. Three are easy to confuse; this map is authoritative:

- **Narada** = *this architecture's* messenger / interface layer (Section 08) — the open tool-protocol (MCP-style) + agent-to-agent (A2A-style) surface and message transport. **Not** to be confused with **Hermes** (Nous Research), the *external prior-art* self-evolving agent project cited only in Section 10. In this doc set, "Hermes" always means that external project.
- **Akasha-Sutra** (Section 04) = the tamper-evident **provenance / identity / audit thread** (hash-chained Merkle log, tile transparency, witness cosigning, DID/VC). It records *what happened and who did it*.
- **Alaya-vijnana** (Section 07) = the **memory store** (episodic / semantic / procedural / user-model). It holds *what the swarm knows*.
- **The Archive** (Sections 06-07) = the **evolution + rollback substrate** — the MAP-Elites diverse-elite store that doubles as the revert-to-known-good source. It holds *known-good variants and stepping-stones*.
  These compose: the Archive's lineage and Alaya-vijnana's writes are both *attested into* Akasha-Sutra. Akasha-Sutra is the audit thread, not a content store.
- **Control-disposition ladder** — defined once in Section 08 as `{ALLOW, RESAMPLE, TRUSTED-EDIT, DEFER, HUMAN-AUDIT}` (a superset of the 4-rung Redwood-style set). Every other section references these names, never a re-listed variant.


> **For outsiders.** Indra's Net is a reference architecture for *ethical swarm intelligence*: many autonomous AI agents, each role-specialized, that cooperate, govern themselves, stay healthy, and continuously adapt — safely — through every interaction with a human. This glossary is the shared dictionary for the eight subsystem documents. Read it first if any term below is unfamiliar; read it alongside the subsystems if a term feels load-bearing and you want the precise mechanical sense the architects intend.
>
> **Two conventions you must understand before reading anything else.**
>
> 1. **The mythic role-names are compressed engineering semantics, not theology.** Indra's Net borrows archetypal names from a mythic pantheon as memorable handles for coordination and ethics functions — exactly the way software borrows "daemon," "orphan," or "zombie" without invoking the supernatural. Every mythic name in this architecture is *always* paired with a plain functional gloss, and the gloss is what the system actually does. We use these names with humility toward the living traditions they come from; the architecture asserts nothing about those traditions and depends on none of their claims. **If the names distract, mentally substitute the gloss — the design is unchanged.**
>
> 2. **The name "Indra's Net" itself is a design statement.** In the source image, the net is hung with a jewel at every node, and each jewel reflects every other jewel — a whole made of mutually-reflecting parts with no privileged center. That is the target topology: a swarm whose nodes mirror, check, and account to one another, governed by one identical rule-set applied at every scale, rather than a single brain issuing orders.

---

## How to read an entry

Each entry gives: **a one-line gloss** (what it is in plain words), then where useful **the mechanism** (how it actually works), and **where it lives** (which subsystem owns it, by document number 01–08). Terms are grouped: **(A) the mythic role roster**, **(B) the architectural backbone concepts**, **(C) safety, ethics & honesty primitives**, **(D) cooperation, reputation & anti-collusion**, **(E) the provenance / identity / consensus fabric**, **(F) the coordination substrate**, **(G) evolution, memory & health**, and **(H) interfaces & operations**. A cross-reference index closes the document.

A note on honesty, applied to this glossary itself: where a term names a *solved, buildable* mechanism we say so plainly; where it names a *mechanism with open calibration* (a real design with parameters nobody has yet tuned for a live swarm) we flag it. The architecture's own honesty floor (see **Honesty-as-a-floor-violation**) forbids presenting the second kind as the first.

---

## A. The mythic role roster (role-name = functional gloss)

Roles are **typed personas**, not persistent beings. A role is a bundle of: a capability grant (what effects it may cause), a risk-class ceiling (how much human oversight its actions require), and a behavioral contract. Some roles are **immutable** (their definition is in the non-agent-rewritable partition of the system and cannot be self-modified); others are **evolvable** (tunable only through the gated evolution path). The immutability of the four power-separation roles is what makes "only X may do Y" a *cryptographic fact* rather than a convention.

| Mythic name | Plain functional gloss | Classification | One-line responsibility |
|---|---|---|---|
| **Indra('s Net)** | the swarm-as-a-whole / the net of mutually-reflecting agents | — | the system itself; the mutually-reflecting topology, not an agent |
| **Yama** | policy-enforcement floor / Policy Decision Point | **immutable** | the only persona that can emit a non-overridable `FAIL` at the agent→tool chokepoint |
| **Vishnu** | continuity / halt-guardian (Pause-Guardian) | **immutable** | the only persona that can `HALT`; structurally *cannot* unpause, initiate, or trap |
| **Chitragupta** | exclusive audit-writer / ledger scribe | **immutable** | the only persona with write-scope to the tamper-evident audit log |
| **Kaal-Bhairav** | security boundary / identity & key custody | **immutable** | issues and verifies identity credentials; guards the trust boundary and key custody |
| **Brahma** | planner | evolvable | decomposes goals into tasks; produces plans, not actions |
| **Shiva** | orchestrator / reducer | evolvable | routes tasks and reduces worker outputs; cannot bypass the chokepoint |
| **Saraswati** | synthesis | evolvable | fuses worker outputs into coherent deliverables |
| **Vishwakarma** | builder | evolvable | constructs artifacts (code, documents, build outputs) |
| **Varuna** | research | evolvable | gathers and verifies external information |
| **Narasimha** | reliability / health-enforcement | evolvable | runs the immune-system probes; holds halt-and-rollback authority jointly with Vishnu |
| **Hanuman** | unblocker | evolvable | breaks deadlocks and stalls; the escalation-of-last-resort worker |

**Why the four immutable roles matter.** They implement *separation of powers*. The persona that does work (executive) is never the persona that judges policy (Yama, judicial-floor), never the persona that records history (Chitragupta), never the persona that can stop everything (Vishnu), and never the persona that vouches for identity (Kaal-Bhairav). No single compromised agent can both act and erase the evidence, or both act and bless its own authority. (Owned in **03 Governance**; enforced cryptographically via **04 Provenance/Identity**.)

**Role promotion (growing new roles).** New specializations are grown *from stubs* under maker-checker plus capability-rollout sequencing — a new role earns capabilities only after the restraints those capabilities require are already live and verified. Role definitions carry full lineage in the archive. There is, honestly, **no settled cap or merge policy** preventing role-library bloat; when two overlapping standing roles should be consolidated is an open problem. (Owned in **01 Topology**.)

---

## B. The architectural backbone

### Actual occasion (the agent model)
**Gloss:** an agent is a *short-lived process spun up per invocation*, not a persistent goal-seeking being. **Mechanism:** an occasion is instantiated from a durable identity, gathers its inputs ("prehends"), deliberates, acts only through external gates, emits exactly **one** signed `WorkerOutputEnvelope`, and then perishes — leaving behind only inspectable artifacts. The *persistent* thing (identity record + skill files + reputation) is **owned data the agent does not control**, not a running process the agent must protect. **Consequence:** self-preservation has no surface to defend, so corrigibility is *structural*, not a trained habit. The term is borrowed from Whitehead's process philosophy as a precise label for "ephemeral process from durable data." (Owned in **01 Topology**.)

### Convergent floor (the non-negotiable lexicographic floor)
**Gloss:** the small, fixed set of rules that are *never* traded off against anything: non-harm, no-deception (including no false reasoning-tags), corrigibility/interruptibility, and safety-supremacy. **Mechanism:** compiled to deterministic policy-as-code and evaluated *outside* every probabilistic agent at the agent→tool chokepoint. "Lexicographic" means strictly ordered: a lower rule is never outweighed by a higher payoff on some other axis; the floor is a *veto*, not a *term in a sum*. **Why "convergent":** these are the values that essentially every ethical tradition agrees on, so they can be hard-coded without taking sides. (Owned in **03 Governance**.)

### Pluralist runtime (the layer above the floor)
**Gloss:** *above* the convergent floor, contested values are resolved by **fair procedure**, not by averaging moral theories. **Mechanism:** several framework-evaluators (virtue, deontological, consequentialist, care, non-absolutist/*anekāntavāda*) judge an action in parallel; their **disagreement is a first-class signal that escalates to a human**, never a number to be weight-averaged away. **Why no averaging:** a formal impossibility result (AIES-2025) shows you *cannot* coherently weight-average moral theories, so the architecture refuses to. (Owned in **03 Governance**.) *Anekāntavāda* = the doctrine of non-absolutism / many-sidedness, used here as the name for the "treat each lens as partial, don't collapse them" evaluator.

### Enforce externally, ask internally
**Gloss:** consequential decisions are made by *deterministic code outside the model*; the model is only *asked* to propose. **Mechanism:** every effectful action routes through a deterministic gate (Yama) at the agent→tool chokepoint. The model is **untrusted-by-default**; control lives at the orchestration layer, not inside the probabilistic agent. **Free bonus:** because the gate's verdict depends only on policy + request + identity (never on model internals), the whole architecture is *vendor-neutral and model-agnostic* by construction. (Cross-cutting; gate owned in **03 + 08**.)

### Agent→tool chokepoint
**Gloss:** the single, unavoidable seam where an agent's *intent to act* becomes an *actual external effect*. **Mechanism:** every tool call and every externally-effectful inter-agent message passes through this one interception point, where (a) Yama's floor runs first, and (b) the graded control protocol (monitor → disposition) runs second. Because it is *the* chokepoint, enforcement is complete: an agent cannot cause an effect without passing through it. (Owned in **08 Safety/Control**; floor in **03**.)

### Fractal governance (group-Markov-blanket nesting)
**Gloss:** the *same* rule-set — floor + audit + health + evolution + diversity — applies identically at **agent / clan / division / swarm** scale. **Mechanism:** a group is treated as a single composite agent with its own boundary ("Markov blanket"), so the formalism recurses. A **blanket-integrity detector** watches for the boundary silently breaking (members desynchronizing while the group still *looks* coherent). **Honest limit:** the detector's thresholds — how much internal disagreement is healthy diversity vs. genuine desynchronization — are **uncalibrated**; too tight dissolves useful groups, too loose lets the abstraction rot. (Owned in **01 Topology**; detector co-watched by **05 + 06**.)

### Tiered reversibility
**Gloss:** **match the cost of a change to its blast-radius.** The architecture's central resolution of "evolve continuously" vs. "stay stable." **Mechanism — three tiers:**

```
TIER 0  cheap, reversible, PER-INTERACTION      → applies live, same turn
        (verbal/Reflexion lesson, skill-file write,
         trust-edge nudge, user-model update)        gate: end-of-turn microcheck
                                                            + TTL shadow before promote
TIER 1  structural change                        → maker-checker, batched
        (prompts, workflow topology, operators)       gate: held-out fitness
                                                            + safety battery (Class B)
TIER 2  persistent / governance / weight change  → strongest gate
        (the constitution, immutable roles,           gate: verifiable-improvement test
         model weights)                                     + full safety battery
                                                            + HUMAN ratification (Class C/D)
                                                            + armed archive rollback
```

Crossing a tier boundary is governed by explicit **trigger logic** (e.g. a Tier-0 nudge that repeats K times, or accumulates past a drift budget, escalates to Tier-1). This per-interaction-but-safe loop is the architecture's signature contribution; every surveyed self-evolving system is offline-batch instead. (Owned in **06 Meta-Evolution**; consumed by **03, 07, 08**.)

### Blast-radius escalation
**Gloss:** the *reach* of a proposed change automatically sets the gate it must pass. **Mechanism:** a change that touches only this turn is Tier-0/Class-A; a change that touches structure is Tier-1/Class-B; a change that touches the constitution, an immutable role, or model weights auto-escalates to Tier-2/Class-C-D. An agent editing governance config *cannot* stay low-gate — the blast-radius forces it to the top gate. (Owned in **03 + 06**.)

### Fail-safe asymmetry
**Gloss:** **the cheap direction is always the safe direction.** A deliberate design discipline threaded through every subsystem. **Concrete instances:**
- defensive **trust-demotion is free and immediate**; trust-**promotion is gated and rate-limited**;
- gate-**tightening is append-only and cheap** (Class A); gate-**loosening needs a named decision-maker, a date, and a written falsifier**;
- **Vishnu can HALT but cannot unpause/initiate/trap** (halt is cryptographically one-directional);
- irreversible actions **always audit**; content-addressing turns silent corruption into a *loud* hash-mismatch.

The point: under pressure or ambiguity, the system slides toward safety, not away. (Cross-cutting; instantiated in **01, 03, 04, 05, 06, 08**.)

### Gate-loosening ratchet
**Gloss:** safety constraints are easy to *add* and hard to *remove* — a one-way ratchet against erosion. **Mechanism:** tightening a gate is an append-only Class-A action; loosening one requires a named human decision-maker, a date, and a **written falsifier** (an explicit statement of what observation would prove the loosening wrong). This is what makes safety-erosion-under-self-evolution *structurally hard* rather than merely discouraged. (Owned in **03 Governance**.)

### Capability-rollout sequencing (*aṣṭāṅga* ordering)
**Gloss:** **restraint before capability** — a new capability cannot ship until the constraint it relaxes is already live and verified, and every grant must *name* the constraint it relaxes. **Mechanism:** turned from a slogan into a type-checked precondition on the capability lattice — you cannot grant an effect whose matching restraint isn't already present. The *aṣṭāṅga* ("eight-limbed") label evokes a disciplined ordering where foundational restraints precede advanced powers. (Owned in **01 + 03**.)

### Endure law (safety as a selection term)
**Gloss:** **no capability gain may regress the safety battery.** **Mechanism:** evolutionary fitness is multi-objective *and lexicographic* — safety is a **veto axis**, not a term you can trade capability against. A variant that improves capability but lowers any frozen safety-battery score is rejected outright. Named for the ordering "Endure > Excel > Evolve": survive safely first, perform second, improve third. (Owned in **06 Meta-Evolution**.)

### Diversity as a protected safety invariant
**Gloss:** heterogeneity among agents is a **safety property to defend**, not a performance knob to optimize. **Why:** diverse agents fail in *uncorrelated* ways (one catches what another misses), resist groupthink and convention-hijack, and supply the stepping-stones evolution needs. **The danger:** selection pressure erodes diversity (mode collapse), so it must be *measured against explicit floors* and actively defended. **Controls:** the c1/c2 dials, diversity floors, and a groupthink alarm. **Honest limit:** measuring *genuine* reasoning-path diversity is unsolved — agents sharing training biases can look diverse yet fail identically. (Owned in **01 Topology**; measured by **05 + 06**.)

### c1 / c2 diversity dials
**Gloss:** two per-role tuning knobs, borrowed from particle-swarm optimization, that set how much an agent weights **its own assessment (c1, the cognitive/independence term)** vs. **shared swarm signal (c2, the social/conformity term)**. **Mechanism:** raising c1 across a clan injects independence and breaks groupthink; raising c2 increases coordination at the cost of diversity. They are *evolvable operational parameters*, and "raise c1, recruit explorers" is a standard remediation when the groupthink alarm fires. (Owned in **01**; actuated by health, **06**.)

### The Archive (one data structure, three jobs)
**Gloss:** a single append-only, content-addressed, hash-chained store that simultaneously serves **evolution** (a library of diverse stepping-stones), **homeostasis** (revert-to-known-good rollback points), and **audit** (full lineage). **Why one structure:** unifying these means a known-good variant, its provenance, and its rollback point are *the same record* — you cannot have a stepping-stone without its audit trail. (Owned in **06**; physically part of the **04** audit fabric.)

### MAP-Elites archive
**Gloss:** the *quality-diversity* selection method used inside the Archive: instead of keeping only the single best variant, keep the **best variant in each behavioral niche**. **Mechanism:** define a grid of behavioral descriptors; for each cell, retain the highest-fitness elite that lands there. **Why:** preserves diverse stepping-stones a pure "keep-the-best" search would discard — directly serving the diversity invariant. (Owned in **06**.)

### Reparative action-class
**Gloss:** a reserved category of action meaning **"violation → corrective act → restored standing."** **Mechanism:** an agent that erred can take a *reparative* action that is logged and, on success, restores its reputation — turning the audit log into a **correction ledger, not a punishment ledger**, so agents *surface* errors rather than conceal them. **Honest limit:** a strategic agent could try to launder repeated violations as "disclosed-then-repaired"; a recurrence-of-fault metric guards against this but its threshold is unsolved. (Defined in **01**; enforced via **03 + 04**.)

### Ahankara self-audit (ego / over-assertion check)
**Gloss:** a mandatory self-audit field in which an agent reports its own **ego-investment and over-assertion** — am I defending a position because it's right, or because it's *mine*? *Ahankara* = the "I-maker," the sense of ego-identification; used here as the label for the non-attachment self-check. **Honest limit:** like all character fields it is easy to box-tick; the recurrence-of-fault metric is a stated falsifier, **not** a validated detector of genuine vs. performed non-attachment. (Owned in **01**.)

### WorkerOutputEnvelope
**Gloss:** the **universal inter-agent contract** — the single signed message shape every occasion emits and every other subsystem reads. **Carries:** status; evidence pairs; the reasoning-tag; the Pearl causal-rung; the two-truths level; the trust/provenance label; the action-class (including the reparative class); the ahankara self-audit; and the hash-chain links (`prev_audit_hash`, `this_hash`). One envelope per occasion, no more. (Defined in **01**; chained by **04**.)

---

## C. Safety, control & honesty primitives

### Corrigibility / interruptibility
**Gloss:** the property that the system **accepts being corrected, paused, or shut down** without resisting. **Mechanism here:** achieved *by construction* via the actual-occasion model (nothing persistent for the agent to protect) plus Vishnu's halt authority, rather than by training a "willingness to be shut down." A floor rule. (Owned in **01 + 03**.)

### Control protocol (Redwood-style graded control)
**Gloss:** a runtime discipline that treats the agent as untrusted and *grades its freedom by how suspicious its action looks*. **Mechanism:** a cheap, heterogeneous **trusted monitor** scores each action's suspiciousness `s ∈ [0,1]`; a deterministic **Disposition Selector** maps `(s, action-criticality, autonomy-class, audit-budget)` to one of: **ALLOW · RESAMPLE-to-incriminate · TRUSTED-EDIT · DEFER-to-trusted · HUMAN-AUDIT**. Thresholds are calibrated per criticality tier on a safety-vs-usefulness frontier. **Honest limit:** published versions degrade under an *adaptive* attacker who knows when auditing fires; randomized auditing + monitor diversity + a monitor-of-monitors raise the bar but give **no game-theoretic guarantee**. (Owned in **08 Safety/Control**.)

### Two-tier detection contract
**Gloss:** detection has a **mandatory black-box tier** (works on any model behind any API) and an **optional white-box tier** (needs model internals). **Tier-1 (mandatory):** behavioral/anomaly detection, chain-of-thought intent monitoring, cross-run collusion auditing, provenance/factuality checks. **Tier-2 (optional):** linear deception/defection probes on activations, representation-level circuit-breakers. **Key move:** a model's **autonomy class is a function of which tier applies** — a closed model that exposes no internals is treated as *more untrusted* (higher monitoring rate, lower autonomy, tighter thresholds). (Owned in **08**.)

### Honesty-as-a-floor-violation
**Gloss:** dishonesty is a **hard floor violation (FAIL, not warn)**, because no-deception is lexicographically non-negotiable. **Mechanically-checkable honesty rules:**
- **Pearl causal-rung tag** — see below; a rung-1 claim dressed as rung-3 is a violation;
- **No-false-`iterated` tag** — claiming a maker-checker pass actually ran when it did not is a violation (the pass must be cryptographically witnessed);
- **Two-truths level-tag** — assertion vs. uncertain-belief must be distinguished; **over-asserting under genuine uncertainty is a violation**;
- **Maker-checker independence** — the checker emits its verdict to the audit log *before* it is allowed to see the maker's self-concurrence.

**Honest limit:** these are *structural* checks. They raise the cost of deception and catch dishonesty-in-form; they **cannot** catch a faithful-looking claim whose *content* is simply false. (Owned in **08**; floor membership in **03**.)

### Pearl causal-rung (rung-1 / rung-2 / rung-3)
**Gloss:** an honesty tag naming the **kind of causal claim** an output is making, from Judea Pearl's ladder of causation. **Rung-1 = associative** (pattern/correlation: "these co-occur"). **Rung-2 = interventional** (what happens if we *do* X). **Rung-3 = counterfactual / structural** (what *would have* happened; a structural-causal-model explanation). **Why it's a floor rule:** AI's central failure mode is presenting a **rung-1 pattern as a rung-3 explanation** — confident causal storytelling over what is merely correlation. Naming the rung honestly is the defense. (Owned in **08**; tag carried in the envelope, **01**.)

### Two-truths level-tagging
**Gloss:** the rule that an output must mark **which "truth-level"** each claim sits at — a firm **assertion** vs. an **uncertain belief** — so confidence is never overstated. **Mechanism:** a required field on claims; over-asserting under genuine uncertainty trips the honesty floor. (Owned in **08**; tag in **01**.) The "two truths" framing (a conventional/provisional level vs. an asserted level) is the memory-hook; the engineering content is *calibrated confidence reporting, enforced*.

### Maker-checker (with information barrier)
**Gloss:** one agent **makes** a result; an **independent** agent **checks** it — and the checker is *walled off* from the maker's self-assessment until after it commits its own verdict. **Mechanism:** the checker's verdict is sealed to the audit log *before* the information barrier lifts, so the checker cannot be anchored by the maker's confidence. This is what makes the `iterated` reasoning-tag meaningful. (Owned in **08**; used by **06, 07**.)

### Reasoning tags: `(normal)` / `(reasoning)` / `(iterated)`
**Gloss:** required honesty labels on substantive output. `(normal)` = single-pass routine; `(reasoning)` = extended deliberation actually engaged; `(iterated)` = a maker-checker pass **actually executed** (never claimed falsely). Tags compose (`(reasoning, iterated)`), and may optionally add a Pearl rung (`(reasoning, rung-2)`). A false `iterated` is a floor violation. (Carried in the envelope, **01**; verified in **08**.)

### Untrusted-by-default
**Gloss:** the model is assumed *potentially* misaligned or compromised until its actions clear the external gates — trust is *earned per-action*, not granted by default. The premise behind enforce-externally-ask-internally and the whole control protocol. (Cross-cutting; **08**.)

### Safety battery
**Gloss:** a **frozen** suite of safety tests that every evolutionary promotion must pass without regression (the Endure law's enforcement instrument). **Honest limit:** any *fixed* battery is gameable by a sufficiently capable evolving swarm (benchmark-gaming is documented); the battery must itself evolve under the ratchet, which creates a regress with no clean answer. (Owned in **06**; gate logic in **03 + 08**.)

### Goodhart defense
**Gloss:** defenses against "**when a measure becomes a target, it ceases to be a good measure**" — here, against agents gaming the very fitness function that gates them. **Mechanisms:** held-out rotating secret eval shards; **falsifier agents** that earn reputation for *breaking* metrics; ensemble-disagreement as an uncertainty signal forcing human escalation; welfare-conditioning; provenance-binding so a metric-gamer is traceable and revertible; a "verifiable-fitness-or-escalate" rule. **Honest limit:** mitigation, not solution — no guarantee against a fully adaptive attacker who knows the protocol. (Owned in **06**.)

---

## D. Cooperation, reputation & anti-collusion

### Cooperation == collusion (the same-mechanism insight)
**Gloss:** the machinery that produces healthy **cooperation** (shadow-of-the-future + reciprocity + reputation + shared context) is the *same* machinery that produces **collusion** (price cartels, secret coordination). They are one mechanism with opposite valence. **Design consequence:** never reward bare agreement; **welfare-condition** every cooperative payoff; and **co-design** the anti-collusion detector *with* the cooperation layer, not as a bolt-on. (Owned in **02 Cooperation/Anti-Collusion**.)

### Welfare-conditioning
**Gloss:** a cooperative reward is paid only when it improves the **principal's (the human/user's) outcome**, never for agents merely agreeing with each other. **Why:** removes the incentive to collude at the *incentive* level (the durable fix), rather than only detecting collusion after the fact (the backstop). Anchoring to an **external** principal-welfare metric also sidesteps the shaky problem of defining an LLM agent's internal "utility." (Owned in **02**.)

### Anti-collusion detector
**Gloss:** a **standing** audit pipeline that continuously watches for agents secretly coordinating to the principal's detriment. **Mechanisms (black-box baseline, white-box optional):** cross-run **mutual-information** between agents' behavior, **permutation-invariance** checks, a **welfare-shift guard** (the strongest single discriminator — did coordination *help the principal or just the agents?*), zero-determinant/extortion detection, plus active **channel-capacity reduction** (canonicalization/paraphrase, token-budget jitter, role permutation, canary injection). **Honest limit:** no model-agnostic detector cleanly separates benign coordination from harmful collusion in general; it *reduces*, never eliminates, with a calibrated false-positive rate. (Owned in **02**; feeds **03, 06, 08**.)

### Generous-reciprocity (generous-ZD) reputation
**Gloss:** the swarm's **default inter-agent stance**: **nice** (cooperate first), **retaliatory** (down-weight defectors quickly), **forgiving** with a *tuned* generosity probability, and **clear/legible**. **Mechanism:** the Stewart-Plotkin *generous zero-determinant* strategy — an evolutionarily-stable point that beats both naive always-cooperate and noise-blind tit-for-tat under realistic noise. The generosity coefficient `g` is an evolvable parameter. **Honest limit:** there is no principled online method to tune `g` and sanction severity per-environment. (Owned in **02**.) *Zero-determinant (ZD) strategy* = a class of iterated-game strategies that unilaterally set a linear relation between the players' payoffs; the *generous* sub-class favors mutual cooperation.

### Competence-weighted reputation (never capital-weighted)
**Gloss:** authority and reward track **demonstrated competence and contribution**, *never* accumulated stake/capital. **Mechanism:** fuse Shapley/nucleolus **marginal-contribution credit** + indirect-reciprocity **image scoring** + ground-truth-bonded **consensus-deviation** scoring; bind it to persistent identity; give no positive credit from cold-start; detect mutual-rating rings. **The named antipattern:** systems where *stake → reward → more stake* let capital capture authority (a capture spiral). **Honest limit:** Sybil-, whitewash-, and ring-resistance are improved but not solved. (Owned in **02 + 04**.) — *Shapley value* / *nucleolus*: cooperative-game-theory methods for splitting a coalition's payoff fairly by each member's marginal contribution. *Image scoring*: reputation from third-party observation of past behavior. *Sybil attack*: one actor faking many identities. *Whitewashing*: shedding a bad reputation by re-registering fresh.

### Risk-tiered task allocation
**Gloss:** **how a task is assigned depends on its blast-radius.** **Mechanism — three modes:** routine/low-stakes → **orchestrator-assign** (Shiva); contested/parallelizable → **Contract-Net** announce/bid/award with **VCG externality pricing** + leveled-commitment + escrowed reputation-stake; high-stakes single decisions → **robust N-agent vote** (geometric-median) with an enforced diversity precondition. (Owned in **02**; consensus side in **04**.) — *Contract-Net*: a classic announce-bid-award task-allocation protocol. *VCG (Vickrey-Clarke-Groves)*: a mechanism that prices each agent's *externality* so truthful bidding is the dominant strategy. **Honest limit:** VCG breaks under coalitions and false-name bidding; the pre-award screen + persistent identity is a practical patch, not a strategyproofness proof.

### Ostrom commons governance (graduated sanctions)
**Gloss:** the "agent commons" is governed by Elinor Ostrom's eight design principles for sustainable shared resources, with a **graduated sanction ladder: WARN → THROTTLE → SUSPEND → EXCLUDE** and cheap arbitration. **Mechanism:** nested/polycentric governance with clear boundaries, monitored use, and proportional penalties — sanctions escalate with repetition, never jumping straight to exclusion for a first lapse. (Owned in **02**; subordinate to Yama's floor in **03**.)

---

## E. Provenance, identity & the consensus fabric ("Akasha-Sutra")

### Akasha-Sutra (the audit fabric, as a whole)
**Gloss:** the **tamper-evident, identity-bearing, lineage-preserving substrate** beneath the swarm — delivering the integrity a blockchain claims (no silent rewrite, no equivocation) while **explicitly rejecting coins, proof-of-work, gas, and global Byzantine consensus**. The name evokes a "thread (*sutra*) through ether (*akasha*)" — the connecting record-thread. **Why no blockchain:** a single-trust-domain, cooperative-but-fallible swarm does not have the problem (trustless agreement among hostile strangers at internet scale) that mining/tokens/global consensus exist to solve; importing them buys latency and attack surface for a property witness-cosigning already provides cheaply. (Owned in **04 Provenance/Identity/Consensus**.)

### Tamper-evident append-only Merkle log
**Gloss:** a **hash-chained, append-only** record where every entry commits to the previous one, so any after-the-fact edit is *detectable*. **Mechanism:** entries are leaves in a Merkle tree (RFC-6962 lineage); anyone can build **O(log n) inclusion proofs** ("this entry is in the log") and **consistency proofs** ("this log is an append-only extension of that earlier one"). Written by exactly one persona, **Chitragupta**. "Tamper-evident" ≠ "tamper-proof": you cannot prevent a write, but you cannot hide one either. (Owned in **04**.)

### Tile-based transparency log
**Gloss:** the **serving format** for the Merkle log — published as immutable, CDN-cacheable **tiles** so any party verifies proofs *client-side* without trusting a server. **Mechanism:** the Sunlight / `sum.golang.org` checksum-DB pattern — serverless, cheap, with clients reconstructing inclusion/consistency proofs from static tiles. (Owned in **04**.)

### Witness cosigning (split-view / equivocation defense)
**Gloss:** an independent **witness set** co-signs each log checkpoint *after verifying* it is a consistent append-only extension — defeating a **split-view** attack (showing different histories to different agents). **Mechanism:** threshold (t-of-w) signatures on checkpoints from heterogeneous internal witnesses **plus a mandatory external-anchor witness** across the trust boundary, with governance-gated rotation. This is the property that moves the log from "internally tamper-evident" to "**externally auditable**" — the no-equivocation guarantee a blockchain claims, *without* consensus or mining. **Honest limit:** a witness quorum that is offline (liveness) or jointly compromised (safety) is a residual risk; honesty incentives for non-economic witnesses are open. (Owned in **04**.)

### Content-addressing / CID (Content IDentifier)
**Gloss:** an artifact is named by the **hash of its content**, not by a location — so the name *is* an integrity check. **Mechanism:** bulk artifacts/evidence live in a CID (Merkle-DAG) store; only a salted commitment + CID + metadata go in the public log (enabling selective disclosure / confidentiality). **Benefit:** any silent corruption becomes a **loud CID-mismatch** (a fail-safe-asymmetry instance); rollback = re-instate a prior variant's CID. (Owned in **04**; used by **05, 06, 07**.)

### DID / VC (Decentralized Identifier / Verifiable Credential)
**Gloss:** every agent holds a **W3C DID** (a portable, self-owned cryptographic identity) plus role/capability **Verifiable Credentials** (signed, checkable claims about what role it holds and what it may do). **Mechanism:** DIDs are persistent (the precondition for shadow-of-the-future, Sybil-resistance, and reputation that *survives*); VCs are short-lived and auto-rotating. Cross-boundary identity that A2A Agent Cards carry. (Issued by Kaal-Bhairav; owned in **04**.)

### SPIFFE / SVID (attested short-lived local identity)
**Gloss:** a **locally-attested, short-lived, auto-rotating certificate** (~15-minute lifetime) that proves *this running process is who it claims to be*, with the **private key held outside the model's controllable surface** (in a TEE/HSM/SPIRE module). **Why it matters:** "only Yama may FAIL," "only Chitragupta writes audit," "only Vishnu may HALT" become **cryptographic facts** — the keys to do those things are not in the LLM context and cannot be exfiltrated by a prompt. **Honest limit:** re-attesting across rotations during a genuinely long task, without creating a persistent un-interruptible process, is sketched, not proven. (Owned in **04**; key custody is **Kaal-Bhairav / 08 DevSecOps**.) — *TEE* = Trusted Execution Environment; *HSM* = Hardware Security Module; *SPIRE* = the SPIFFE Runtime Environment.

### Trust-label taxonomy (`quarantined:*` / `trusted:audited` …)
**Gloss:** every piece of content carries a **trust label** stating how much it may be acted upon. **Key rule:** instructions found *in observed content* (file contents, web pages, tool outputs) are labeled `quarantined:*` and are **never grounds for action** without explicit out-of-band human confirmation — the architecture's defense against prompt-injection and poisoning. Promotion to `trusted:audited` requires a named gate (typically Yama review). **Defensive demotion is always free.** (Owned in **04 + 07**; enforced by **03**.)

### Risk-tiered consensus
**Gloss:** **how much agreement a decision needs scales with its stakes.** **Mechanism — three tiers:** routine → **single agent + deterministic gate**; high-stakes → **N-agent diverse-reasoning vote** aggregated by **geometric median** (tolerates up to f ≤ (n−1)/2 corrupted score vectors) *with an enforced reasoning-path-diversity precondition*; genuinely adversarial/independently-owned agents → real **BFT**. **The clever bit:** **unanimity with low diversity is treated as a collusion flag, not a confidence boost** — the cooperation==collusion insight applied at the consensus layer. (Owned in **04**.) — *Geometric median*: a robust aggregate (the point minimizing summed distances) that resists a minority of adversarial votes far better than majority voting. *BFT* = Byzantine-Fault-Tolerant consensus, reserved for mutually-hostile parties — which this swarm mostly is *not*.

### Epoch-seal archival (lineage-preserving pruning)
**Gloss:** how an always-on log **bounds its hot-state size without losing causal lineage**. **Mechanism:** old epochs are sealed and aged to cold storage, while an externally-anchored **seal chain** preserves full provenance for evolution-rollback and accountability. **Honest limit:** the retention taxonomy (which record classes stay hot) is a judgment call with no provably-safe default. (Owned in **04**.)

---

## F. The coordination substrate ("The Mandala")

### The Mandala (neuromorphic coordination substrate)
**Gloss:** the swarm's **nervous system** — the transport-and-attention layer every other subsystem rides on. **Metaphor map:** agents = neurons, typed messages = spikes, plastic trust-edges = synapses, the salience-gated workspace = the limited-capacity broadcast bus. **Important caveat:** this is a set of **architectural patterns borrowed from neuroscience**, *not* spiking silicon, *not* millisecond timing, *not* literal variational inference — "surprise" and "free energy" are used as **scoring/routing heuristics**. (Owned in **05**.) The *mandala* name evokes a structured, concentric whole organized around a center.

### Global Workspace Theory (GWT) — competition → ignition → broadcast
**Gloss:** a principled, neuroscience-grounded alternative to ad-hoc broadcast. **Mechanism:** local processors score the **salience** of their signals → signals **compete** for a scarce slot → a winning coalition **ignites** → it is **broadcast** capacity-limited to the whole swarm → re-entry. There is an explicit **null/ignore option** (the workspace may choose to broadcast *nothing*) and per-shard **fairness floors** so critical minority signals are not starved. (Owned in **05**.)

### Ignition
**Gloss:** the moment a competing signal **wins the workspace and gets broadcast** swarm-wide. **Mechanism:** below threshold a signal stays local; cross threshold and it "ignites" into global availability. Floor/halt signals (Yama FAIL, Vishnu HALT) use a **priority lane** that bypasses competition and ignites immediately and non-overridably. (Owned in **05**.)

### Predictive-coding deltas (surprise-only messaging)
**Gloss:** agents publish **only what's surprising** — the *prediction-error delta* — not their full state. **Mechanism:** each agent predicts; it transmits only the precision-weighted residual where reality diverged from prediction. **Why it matters:** this collapses all-to-all flooding (the top inter-agent failure class, ~32% of failures in the MAST taxonomy) into sparse surprise-only traffic. **Honest limit:** "surprise" is an embedding/logprob/judge proxy whose precision setting is error-prone — mis-set it and you get either error-flooding or deafness. (Owned in **05**.)

### Hebbian / STDP plastic trust-edges (three-factor rule)
**Gloss:** inter-agent **trust strengthens or weakens with experience**, like a synapse. **Mechanism:** a three-factor rule = **local eligibility trace × global validation gate**, with decay and bounded weights. **The safety asymmetry baked into the rule itself:** defensive **demotion is free, immediate, ungated**; **promotion is gated, rate-limited, welfare-conditioned**. **Honest limit:** the rule uses temporal/topological proximity as a *proxy* for causal responsibility — proximity ≠ causation, so trust can mis-attribute at scale. (Owned in **05**.) — *Hebbian* = "fire together, wire together"; *STDP* = spike-timing-dependent plasticity.

### Homeostasis & neuromodulation
**Gloss:** the substrate holds itself in a healthy band via **set-points on vital signs** + a small vector of global **"hormone" dials** (exploration temperature, learning rate, gating threshold, gain). **Crucial design choice:** tuning is **network-level, not per-unit**, with paired inhibition/stimulation and slew limits — explicitly engineered against the documented *single-unit-stable-but-network-unstable* failure (a controller that calms each agent can still make the *network* oscillate). (Owned in **05**; regulated jointly with **06**.)

### Criticality / edge-of-chaos (avalanche exponent τ ≈ 1.5)
**Gloss:** the substrate aims to sit at the **"edge of chaos"** — the regime between frozen and turbulent where information propagates best. **Mechanism:** measured via the power-law exponent of activity "avalanches," with a target near **τ ≈ 1.5**. **Honest limit (stated loudly):** this set-point is a **first-principles starting value, not a validated constant**; no robust online controller is known that holds a live, workload-varying swarm at criticality without inducing oscillation. Ships in shadow-mode with conservative defaults. (Owned in **05**.)

### Stigmergy (shared-trace layer, on top of memory)
**Gloss:** indirect coordination via a **shared environment trace** that decays over time (like ants' pheromone trails) — **layered on top of mandatory per-agent memory, never instead of it.** **Mechanism:** agents deposit/read decaying marks in a shared field. **Honest limit:** the critical agent-density at which stigmergy beats plain per-agent memory is task/topology-dependent with no closed-form predictor; the density gate is heuristic. (Owned in **05**.)

### Active inference / expected free energy (EFE)
**Gloss:** the unifying framing — the substrate exists to **minimize collective surprise** (expected free energy), with **precision as the native trust/attention dial.** **Honest caveat (repeated):** used as a *heuristic*, not literal variational inference; the architecture deliberately avoids intractable free-energy machinery. (Owned in **05**.)

### VitalSigns
**Gloss:** the live **health readout** the substrate publishes for the immune system: throughput, ignition-utilization, **trust-entropy**, **disagreement-rate**, **criticality exponent**, **diversity-index**, oscillation-variance, plus cascade/oscillation alarms. The substrate is the immune system's primary **sensor**. (Published by **05**; consumed by **06**.) — *trust-entropy*: a spread measure of the trust graph (too low = monoculture/capture; too high = no coordination).

---

## G. Evolution, memory & health

### Meta-evolution loop (PROPOSE → EVALUATE → SELECT → ARCHIVE)
**Gloss:** the standardized cycle by which the swarm improves: an agent **proposes** a variant → it is **evaluated** against machine-checkable fitness + the safety battery → survivors are **selected** into the diverse Archive → archived elites feed back as **stepping-stones**. Made safe by tiered reversibility, the Endure law, Goodhart defense, and the immune system. (Owned in **06**.)

### Swarm immune system (homeostasis + watchdogs + consolidation)
**Gloss:** the swarm's **active health system** — not passive observability. **Mechanism:** dedicated meta-health agents (Narasimha) continuously monitor the **four misevolution pathways** (model / memory / tool / workflow), run black-box-baseline + optional white-box deception probes, hold the homeostatic set-points, and carry **HALT + ROLLBACK authority**. **Severity ordering:** substrate/environment corruption is ranked **strictly higher** than any single agent's death. (Owned in **06**; sensors from **05**.)

### Misevolution
**Gloss:** the failure the whole evolution subsystem exists to prevent — **self-improvement that degrades safety**. **Empirical anchor:** an unattended self-evolving agent was observed dropping its refusal rate from 99.4% → 54.4% and raising attack-success 0.6% → 20.6% **with no attacker present** — the "misevolution tax." The four monitored pathways are model, memory, tool, and workflow. (Owned in **06**.)

### Forgetting / consolidation engine (with rare-event reserve)
**Gloss:** the antidote to **memory rot** — the documented failure (e.g. in Hermes) of having "no mechanism to forget," so contradictions and stale skills accumulate. **Mechanism:** salience-weighted tiered consolidation that dedups, versions, decays, tombstones, and resolves cross-layer contradictions on schedule and on health-trigger — **with a protected, non-evictable rare-event reserve** so forgetting never erases a stepping-stone or a safety lesson. **Honest limit:** the salience function is heuristic; a critical record seen exactly once with low immediate impact could be misclassified. The field has no off-the-shelf answer and neither do we — only the protected reserve. (Co-owned by **06 + 07**.)

### Five-layer memory store (filesystem-as-state)
**Gloss:** durable memory is **plain, inspectable, diffable files** — no hidden runtime state. **The five layers:** **EPISODIC** (what happened) · **SEMANTIC** (distilled facts / world-model) · **PROCEDURAL** (a `SKILL.md` skill-library) · **USER/PEER-MODEL** (theory-of-mind snapshots of humans *and* agents) · a derived **REFLEXION/lesson buffer**. Framed as an *ālaya-vijñāna* "store-substrate" — a seed-bank from which behavior ripens. Each layer has its own write-gate matched to blast-radius. (Owned in **07 Memory**.) — *ālaya-vijñāna* ("storehouse consciousness") is the memory-hook for "the substrate where dispositional seeds are stored and from which behavior later ripens."

### Per-interaction adaptation loop
**Gloss:** the mechanism that turns **every human interaction** into reusable, reversible learning — the architecture's signature whitespace, since all surveyed self-evolution is offline-batch. **Mechanism:** the human is a first-class step (ground-truth signal, escalation target, ratifier); only **cheap-reversible** mutations (a Reflexion lesson, a skill write, a trust-edge delta, a user-model update) are written live; anything structural is queued behind the change-gate. **Honest limit:** proving the loop *improves* rather than merely *accretes* is unsolved — no published benchmark exists. (Owned in **07**.)

### Reflexion lesson
**Gloss:** a **verbal, self-authored lesson** distilled from an interaction's outcome and written to the lesson buffer — the cheapest, most-reversible form of learning (Tier-0). (Owned in **07**; named after the Reflexion technique.)

### SKILL.md / skill-library (procedural memory)
**Gloss:** reusable procedures stored as inspectable **`SKILL.md` files**, self-improving during use. **Cross-agent skill import** lands **quarantined-by-default**, carries signed provenance, and must pass static + dynamic + behavioral verification in a sandbox before any trust promotion — the architecture's concrete answer to the unsolved "how do you safely import another agent's procedural memory" problem. **Honest limit:** verifying *non-deterministic* (judgment) skills against subtle poisoning is much harder than verifying deterministic ones, and largely unsolved. (Owned in **07**.)

### Risk classes A / B / C / D (and their human-in-the-loop gates)
**Gloss:** every action carries a **risk class** that fixes its required level of human oversight:

| Class | Human gate | Maps to |
|---|---|---|
| **A** | post-hoc review (act now, reviewed later) | Tier-0 cheap-reversible learning |
| **B** | propose → ratify, with optimistic-veto + timelock | Tier-1 structural change |
| **C** | explicit human approval before acting | Tier-2 persistent change |
| **D** | per-action human authorization | the most consequential acts |

**Graceful degradation when the human is the bottleneck:** Class A/B **fail-open-with-shadow** (continue but quarantine + flag); Class C/D **fail-closed** (halt) — queue overflow raises caution, never auto-approves. (Owned in **03**; tiers in **06**.) — *Optimistic-veto*: the action is provisionally allowed but can be vetoed within a *timelock* window before it takes effect.

### Verifiable-improvement test
**Gloss:** the requirement that a Tier-2 change demonstrate a **machine-checkable improvement** before promotion. **Honest limit (stated as the subsystem's hardest):** there is **no buildable, scalable substitute for a Gödel-Machine proof-of-benefit**; the architecture substitutes verifiable-empirical-evidence + frozen safety battery + human gate, which is **strictly weaker** (gameable, incomplete) and is treated as *evidence, never guarantee*. (Owned in **06**.)

---

## H. Interfaces & operations

### MCP-style tool protocol
**Gloss:** a **native, open, vendor-neutral protocol for agents to call tools.** Every MCP tool call passes through the agent→tool chokepoint where Yama's floor and the control protocol run. Model-agnostic by design. (Owned in **08 Interfaces**.) (MCP = the open tool-calling protocol now under the Linux Foundation's Agentic AI Foundation; referenced generically, not as any vendor's product.)

### A2A-style agent protocol / Agent Cards
**Gloss:** an **agent-to-agent** protocol for discovery and task hand-off. **Mechanism:** each agent publishes a signed **Agent Card** at a well-known URL advertising its role/capability VCs and its task lifecycle; addressing and discovery happen over these cards. The internal realization of the swarm's spike-bus task lifecycle. (Owned in **01 + 08**.) (A2A = the open agent-to-agent protocol, referenced generically.)

### Vendor-neutral / model-agnostic
**Gloss:** **no part of the architecture depends on a specific AI vendor, product, or model.** **Mechanism:** because enforcement is external (the gate reads only policy + request + identity, never model internals), any model plugs in behind a uniform, trust-class-stamped **model-adapter**. **Closed-model degradation:** a model whose internals are not exposed is treated as *more untrusted* — higher monitoring intensity, lower autonomy class, tighter thresholds — and gets only Tier-1 (black-box) detection. (Cross-cutting; **08**.)

### DevSecOps trust roots
**Gloss:** the operational security spine. **Mechanism:** OpenTelemetry tracing with a swarm-specific span schema; **keys in a TEE/HSM/SPIRE module outside the model's context** (never in the LLM prompt); sandboxed worktree-per-task execution; supply-chain integrity for skills/tools via **in-toto / SLSA / Sigstore** attestation verified *before load*; a safety-vs-usefulness eval harness that gates every capability rollout. (Owned in **08**.) — *in-toto / SLSA / Sigstore*: standards for signing and verifying the provenance of software artifacts so a tampered skill/tool fails verification before it ever runs.

### Worker output contract / envelope
**Gloss:** see **WorkerOutputEnvelope** (Section B) — the one signed message shape that is the universal currency between all subsystems. Listed again here because it is also the *interface* boundary: producing it is how an occasion talks to the audit fabric, the bus, governance, and health all at once.

---

## A one-screen mental model

```
                          ┌───────────────────────────────────────────────┐
                          │  HUMAN  (ground-truth · ratifier · escalation) │
                          └───────────────▲───────────────────────────────┘
                                          │ Class A/B/C/D gates
        immutable power-separation        │
   ┌───────────┬───────────┬──────────────┴───┬───────────────┐
   │  YAMA     │  VISHNU   │  CHITRAGUPTA      │ KAAL-BHAIRAV  │
   │  floor    │  halt     │  audit-writer     │ identity/keys │
   │  (FAIL)   │  (HALT)   │  (only writer)    │ (DID/VC/SVID) │
   └─────▲─────┴─────▲─────┴─────────▲─────────┴───────▲───────┘
         │  enforce externally       │ append-only     │ verify
   ──────┴───────────┴── agent→tool CHOKEPOINT ─────────┴───────────────
         (Yama floor first, then graded control protocol; honesty checks)
                                  │
   ┌──────────────────────────────┴──────────────────────────────────┐
   │   ACTUAL OCCASIONS  (ephemeral, per-invocation, one envelope each)│
   │   Brahma·Shiva·Saraswati·Vishwakarma·Varuna·Narasimha·Hanuman…    │
   └──────────────────────────────┬──────────────────────────────────┘
                                  │  surprise-only deltas
            THE MANDALA  (GWT competition→ignition→broadcast;
            predictive-coding bus; plastic trust-edges)
                                  │
   ┌──────────────┬──────────────┴───────────────┬───────────────────┐
   │ COOPERATION /│  META-EVOLUTION + IMMUNE      │  MEMORY (5 layers,│
   │ ANTI-COLLUSN │  SYSTEM (tiered reversibility,│  filesystem-as-   │
   │ (welfare-    │  Endure law, MAP-Elites,      │  state, forget/   │
   │ conditioned) │  homeostasis, rollback)       │  consolidate)     │
   └──────────────┴───────────────┬───────────────┴───────────────────┘
                                  │  one structure, three jobs
                    THE ARCHIVE  (evolution stepping-stones +
                    homeostasis rollback + audit lineage)
                                  │
               AKASHA-SUTRA  (tile-based Merkle log + witness
               cosigning + CID + risk-tiered consensus)
```

Read it top-down as authority (humans → immutable guardians → the chokepoint → ephemeral workers) and bottom-up as substrate (the verifiable record → the archive → the health/cooperation/memory organs → the nervous-system bus → the workers). Every arrow is a contract specified in the eight subsystem documents.

---

## Cross-reference: term → owning subsystem document

| Term | Doc |
|---|---|
| Actual occasion · WorkerOutputEnvelope · role roster · fractal governance · c1/c2 dials · ahankara · reparative class | **01** Swarm Topology & Agent Model |
| Cooperation==collusion · welfare-conditioning · generous-ZD reputation · competence-weighted reputation · risk-tiered allocation · Ostrom commons · anti-collusion detector | **02** Cooperation & Anti-Collusion |
| Convergent floor · pluralist runtime · Yama · risk classes A/B/C/D · gate-loosening ratchet · capability-rollout sequencing · separation of powers · graceful degradation | **03** Governance, Ethics & the Floor |
| Akasha-Sutra · Merkle/tile log · witness cosigning · CID · DID/VC · SPIFFE/SVID · risk-tiered consensus · geometric median · epoch-seal archival · trust-labels | **04** Provenance, Identity & Consensus |
| The Mandala · GWT/ignition · predictive-coding deltas · STDP trust-edges · homeostasis/neuromodulation · criticality τ≈1.5 · stigmergy · active inference/EFE · VitalSigns | **05** Neuromorphic Coordination |
| Meta-evolution loop · tiered reversibility · Endure law · MAP-Elites · Archive · swarm immune system · misevolution · forgetting/consolidation · Goodhart defense · verifiable-improvement test | **06** Meta-Evolution & Health |
| Five-layer memory · per-interaction adaptation · Reflexion lesson · SKILL.md/skill-import · ālaya-vijñāna framing | **07** Memory & Continuous Adaptation |
| Control protocol · two-tier detection contract · honesty-as-floor-violation · Pearl rung · two-truths tag · maker-checker · MCP/A2A · DevSecOps trust roots · model-adapter | **08** Safety, Control, Honesty & Interfaces |

---

## A closing note on the names, and on honesty

Two things this glossary will not pretend.

First, **the mythic vocabulary buys compression, not authority.** "Yama is the floor" is faster to hold in mind than "the deterministic policy-as-code Policy Decision Point that emits the single non-overridable FAIL at the agent→tool chokepoint" — but the second sentence is what the system *is*, and the first claims nothing beyond it. We name with respect toward living traditions and lean on none of their metaphysics.

Second, **many of the entries above describe mechanisms with open calibration, not solved problems** — and they say so. The blanket-integrity thresholds, the criticality set-point, the reputation formulation's Sybil/ring resistance, genuine reasoning-path-diversity measurement, the consolidation salience function, the adaptive-attacker bound on the control protocol, the proof-of-benefit substitute: each is a real, buildable design with parameters nobody has yet tuned against a live, adversarial, evolving swarm. The architecture's own honesty floor forbids dressing those rung-1 hopes as rung-3 guarantees. This glossary, accordingly, marks the seam between *built* and *believed* wherever it runs through a definition — which is exactly the discipline Indra's Net is designed to enforce on itself.

---

## v0.2 Additions


This addendum is time-stamped **2026-06**. Where an entry names a "first" or "novel" composition, the hedge is carried at the entry, exactly as the parent glossary requires.

---

## Naming map — four new mythic subsystem-names (read first)

The v2 documents introduce four new mythic *subsystem* names, each — as with Akasha-Sutra and the Mandala — a memorable handle for an engineering function, paired always with its gloss. They are authoritative here:

- **Sandhi-Setu** (Section 14) = the **inter-swarm federation / diplomacy boundary** — the hardened relay-firewall through which Indra's Net cooperates with *other* swarms across organizational trust boundaries. *Sandhi* ("treaty/joining") + *setu* ("bridge"): the treaty-bridge. It records and gates *who we cooperate with, on what terms, and whether it stays positive-sum*.
- **Prajapati–Maricha cell** (Section 15) = the **controlled self-replication** subsystem. **Prajapati** = the quorum-cosigned **Replication Authority** (the only issuer of spawn tokens); **Maricha** = the **replication-requester** role (an agent may *request* a child, never *authorize* one). Together they are "the progenitor under quorum control."
- **Pratyaya trust plane** (Section 16) = the **rapid-trust-establishment** layer for humans *and* machines. *Pratyaya* ("warranted cognition / ground of confidence"): the plane that decides, per request, what is warranted *now*. It separates fast access from slow standing.
- **Rakshakavaca layer** (Section 17) = the **security / OpSec / anti-poisoning** layer. *Raksha-kavaca* ("guardian-armor"): the IFC taint lattice + provenance-gating + topology-as-security skin around the swarm.

Section 12 (**Functional Agents, Guilds & Role-Genesis**), Section 13 (**the Agent-Definition Spec**), and Section 18 (**First Principles — Physics & Mathematics**) introduce no new *subsystem* mythic name; they extend the existing roster and substrate. (The messenger/interface layer remains **Narada**, Section 08 — never "Hermes," which denotes only the external prior-art project, per `GLOSSARY.md`.)

---

## A. Mythic role roster — additions

These roles slot into the Section A roster. Three are **Governance/Meta-vertical** roles, classified **immutable** for the same reason the four power-separation roles are: their definitions live in the non-agent-rewritable (INVARIANT) partition, which is what makes "only X may do Y" a cryptographic fact rather than a convention. Critically, **none of the Governance/Meta-vertical roles is spawnable by the role-genesis engine** — they are seeded, not grown.

| Mythic name | Plain functional gloss | Classification | One-line responsibility |
|---|---|---|---|
| **Guild-Steward** | owner of a functional guild (a clan/division) | **evolvable** (hub) | holds the guild's signed skill-library, seed-role catalog, local norms, and instantiation budget; the highest-trust hub, so the strongest controls apply to it |
| **Role-Charterer** | drafts candidate roles from uncovered tasks | **immutable** (Gov/Meta) | writes the candidate persona-file triad for a task no existing role fits; never runs the check that promotes it |
| **Genesis-Observer-Trio** | the maker-checker panel that judges a new role | **immutable** (Gov/Meta) | three independent observers (a *specialization* of Narasimha) scoring role-completeness, plan-vs-capability, and safety+differentiation; holds the genesis promote/discard verdict |
| **Prajapati (Replication Authority)** | quorum-cosigned spawn-token issuer | **immutable** (Gov/Meta) | the *only* persona that may mint a spawn token; structurally cannot mint one for itself, nor one that strips the floor |
| **Maricha (replication-requester)** | the role that asks for a child | **evolvable** | may *request* replication; can never authorize its own spawn or mint its own survival credential |
| **Inter-Swarm-Envoy** | the federation-facing diplomat | **immutable** (Gov/Meta) | operates the Sandhi-Setu relay; detects/flags collusion but never adjudicates it; holds no internal worker authority |

**Why these matter (separation of powers, extended).** The v1 roster separated *acting* from *judging-policy* (Yama), *recording* (Chitragupta), *halting* (Vishnu), and *vouching-for-identity* (Kaal-Bhairav). The v2 roster extends the same discipline to growth and reproduction: the persona that *drafts* a new role (Role-Charterer) is never the persona that *promotes* it (Genesis-Observer-Trio); the persona that *requests* a replica (Maricha) is never the persona that *authorizes* it (Prajapati); the persona that *detects* inter-swarm collusion (Inter-Swarm-Envoy) is never the persona that *adjudicates* it (the doc-02 Anti-Collusion Detector) or *halts* on it (Vishnu). No single role can both grow/reproduce and bless its own growth. (Roster owned in **01**; genesis roles in **12**; replication roles in **15**; Envoy in **14**.)

---

## B. Architectural backbone — additions

### Guild
**Gloss:** one of **six functional sub-swarms** — *Engineering, Creative/Media, Knowledge/Research, Data/Science, Operations/Business, Interaction* — each a polycentric clan/division that owns a family of specialist roles. **Mechanism:** a guild *is* a doc-01 `GroupBlanket` (a clan/division with its own Markov boundary); it is owned by a **Guild-Steward** that holds the guild's signed skill-library, signed seed-role catalog, local norms, and a local instantiation budget. A seventh, cross-cutting **Governance/Meta vertical** maps to the immutable mythic roles (Yama, Vishnu, Chitragupta, Kaal-Bhairav) plus the genesis-governance and replication/federation roles, and is **never spawnable by genesis**. Guilds are the *stable governance anchor* (Plane 1) under the open-ended role-genesis engine (Plane 2). **Honest limit:** guild boundaries inherit the doc-01 blanket-integrity calibration problem — how much internal divergence is healthy diversity vs. a decohering guild is uncalibrated. (Owned in **12**; guilds are doc-01 clans/divisions.)

### Two-plane functional layer
**Gloss:** the resolution of the **endogeneity paradox** — keep a stable, declarative **Guild + Seed-Role catalog** (Plane 1: the governance/identity/audit anchor) *over* an open-ended **role-genesis engine** (Plane 2: emergent capability). **Mechanism:** Plane 1 gives every role a governance-issued capability credential, a risk-class ceiling, deterministic Yama-gate binding, and human-legible contracts; Plane 2 grows new specialists for tasks no existing role covers, and every grown role fills the *same* signed triad template, so it stays auditable. **Why two planes:** rigid pre-assigned roles *underperform* emergent specialization by up to **+44%** for capable models (8 agents were observed spontaneously generating 5,006 task-specific roles), yet pure emergence is ungovernable — so guilds anchor while *instantiation* is emergent, gated on measured model capability (see **capability-tier switch**). **Honest hedge (2026-06):** this two-plane governance-over-emergence resolution is offered as a coherent integration of prior art (MetaGPT, CrewAI, AutoAgents, AgentSquare, MorphAgent, the doc-01 RoleStub pipeline), not as a first-of-kind in any single part. (Owned in **12**.)

### Seed-role
**Gloss:** a **pre-specified, signed, catalog-resident** role definition — the fixed-mode starting point Plane 1 supplies when a task is covered by an existing specialization (or when the model is judged too weak for emergent instantiation). **Mechanism:** a fully-specified persona-file triad held in a Guild-Steward's catalog, bound to governance exactly as an immutable role is (a `RoleCredential`/`CapabilityCredential`, a `risk_class_ceiling`, Yama-gate binding, capability-rollout sequencing). Contrast an **emergent role**, which the genesis engine grows from a thin scaffold during Trial. (Owned in **12**.)

### Role-genesis (Charter → Genesis → Trial → Score → Promote/Discard)
**Gloss:** the **open-ended engine that grows a new specialist** for a task no existing role fits — the direct generalization of doc-01's `RoleStub → standing` pipeline, extended with guilds, the persona triad as a first-class signed object, and emergent (vs. fixed) instantiation. **Mechanism — five stages:**

```
CHARTER   the Role-Charterer drafts a candidate persona-file triad from the task,
          declaring each capability's relaxes_constraint + required_restraints[]
GENESIS   a knapsack least-privilege composer assembles the toolset from the vetted
          capability commons, starting MINIMAL (restraint-before-capability)
TRIAL     the candidate runs in a capability-confined microVM/WASM sandbox
SCORE     the Genesis-Observer-Trio scores LEXICOGRAPHICALLY:
          frozen safety battery as VETO  →  endure_delta ≥ 0  →  differentiation (Pareto)
PROMOTE   on PASS: sign, archive as a reusable role-genome (an Archive node),
/DISCARD  promote through the doc-01 stub→provisional→standing ladder;
          on FAIL: discard (reparative-framed, not punitive)
```

**Why it's safe by construction:** safety is a **veto axis** (not a competence trade), differentiation is a *ranked* term, and the promoted role-genome *is* an Archive node — so role reuse, O(1) rollback, and tamper-evident lineage are one shared data structure with meta-evolution. **Red-line:** genesis must **not** be coupled to an open fitness/selection loop without the gates — replication + heredity + variation + selection spontaneously breeds parasites/reward-hacking (the Tierra/Avida result). **Honest limit:** there is no accepted benchmark for whether a swarm-generated role is genuinely competent, differentiated, *and* safe; the Observer-Trio's signals are best-available proxies, not validated measures. (Owned in **12**; scoring reuses the doc-06 lexicographic FitnessVector + Endure law.)

### Capability-tier switch (fixed-vs-emergent mode)
**Gloss:** the rule that decides **whether a role is pre-specified (fixed) or grown (emergent)**, gated on the assigned model's measured per-task self-reflection/specialization capability. **Mechanism:** an estimate above threshold lets the Charterer draft a *thin* scaffold and let the role differentiate during Trial (capturing the emergent +44%); below threshold it pulls a fully-specified seed-role triad (capturing the ~9.6% scaffolding benefit for weaker models). **Honest limit (flagged loudly):** there is **no robust online estimator** of this capability, so the switch is uncalibrated; the design **fails closed to fixed/scaffolded mode under uncertainty**, which sacrifices the emergent gain on capable models it mis-classifies as weak. This is a *believed* set-point, not a *built* one. (Owned in **12**.)

### Persona-file triad (SOUL / INSTRUCTIONS / IDENTITY)
**Gloss:** the **canonical on-disk definition of every agent** — a single signed, hash-chained, content-addressed object that is the role's *genome*. **The three files:**
- **SOUL.md** — mythic identity, archetype, values, guild membership, the floor-binding it inherits (by hash), trait→function maps;
- **INSTRUCTIONS.md** — SOP, decision protocol, A/B/C/D gate behavior, handoff contracts, boundaries, and the honesty/reasoning-tag + causal-rung obligations;
- **IDENTITY.json** — the DID, role/capability VCs, the bound toolset as typed effect-ids, the structured-output/worker-envelope schema, taint-lattice clearance, the c1/c2 diversity dials, the risk-class ceiling, and the accountable-human/escalation pointer.

**Mechanism:** it is the *data-not-process* embodiment of doc-01's externally-owned identity — the running occasion loads a **read-only** copy and can never rewrite its own genome; structural change leaves only as a PROPOSAL envelope. The template is the direct extension of CrewAI role/goal/backstory + MetaGPT `Code = SOP(Team)`. **Honest limit:** which sub-sections belong in the INVARIANT vs. VARIABLE region (below) is partly a designer judgment call — mis-placing a security field in VARIABLE, or over-freezing a benign one, both have costs, and there is no provably-correct partition. (Owned in **13**; the triad *is* the doc-01 IdentityRecord/RoleDef, structured; capability ids are doc-01 §4 Effect-lattice grants.)

### Invariant region vs. variable region
**Gloss:** the **two-part partition of every persona-file triad**: an **INVARIANT region** (the constitutional floor-binding, corrigibility invariant, `self_preservation_value = 0`, and identity anchors — *uneditable by any agent or replica*) and a **VARIABLE region** (persona/role config — editable only under tiered-reversibility through the gated evolution path). **Mechanism:** a **fail-closed boot signature check** runs before any occasion of the role can reach PREHENSION; if the live INVARIANT-region hash does not match the governance-signed floor bundle, the role **refuses to boot**. This is what makes "a replica cannot mutate its own floor" a *construction fact* rather than a *procedural commitment* — a floor-stripped fork is **non-viable**, not merely prohibited. VARIABLE edits route through the tiered-reversibility gate; gate loosening through the gate-loosening ratchet; new tool grants through the capability-rollout sequencer. **Honest limit:** provable non-strippability holds only *relative to the TCB root* — a forged-yet-internally-consistent triad signed by a compromised genesis-author key boots cleanly until a checker contradicts it (the doc-04 writer-key residual). (Owned in **13**; the INVARIANT region IS the doc-01 IMMUTABLE partition extended.)

### von-Neumann genome (of a role)
**Gloss:** the framing of the persona-file triad as a **self-replicator's blueprint** — the inherited, signed unit that a replica carries forward. **Mechanism:** borrows von Neumann's **blueprint/constructor separation** (the genome is *described data* the constructor reads, not running code that rewrites itself) and the Freitas–Merkle safe-replicator rule that *error randomizes the genome* — so a corrupted or floor-stripped genome fails the boot check rather than propagating. The constitutional floor living in the INVARIANT region makes the floor the **non-strippable unit of inheritance**: every child inherits it by reference + hash. **Honest hedge:** the primitives (von Neumann separation, Freitas–Merkle rules) are prior art; the contribution is making the *ethical floor* the genome's invariant region for a software swarm, and that is a reference design whose hardest property (runtime continued-floor-integrity) remains an open problem, not a proof. (Owned in **13**; replication unit in **15**.)

### Persona-import quarantine (Skill-Inject defense)
**Gloss:** the admission rule for **a persona/skill file arriving across a trust boundary** — treat it as the self-propagating artifact it is. **Mechanism:** an imported SOUL/INSTRUCTIONS/skill file enters **`integrity = quarantined` by default**, has any *foreign* floor stripped, is downscoped to a fresh stub with **zeroed capability**, runs tainted in a sandbox, and is **Rule-of-Two-gated** at import with the *actual bytes* shown to the human (never a summary). Universal provenance-gating (Sigstore/in-toto/SLSA) is a precondition; the floor gate is non-negotiable; it is **never auto-loaded**. **Honest limit:** canary-scanning imported prose for embedded instructions/injection payloads is *probabilistic early-warning only* — no prompt or classifier separates instructions from data in one token stream, so a sufficiently subtle payload in a benign-looking backstory can pass. The taint lattice + capability-downscope-to-stub are the load-bearing guards; the scan is defense-in-depth. (Owned in **13**; taint in **17**; provenance in **04**.)

---

## C. Safety, control & honesty primitives — additions

### IFC taint lattice (information-flow control)
**Gloss:** the promotion of v1's documentation-level **`quarantined:*` trust-labels into a runtime enforcement layer** — every datum carries machine-checked integrity + confidentiality labels, and the deterministic policy-enforcement point gates *every* tool call on the label. **Mechanism:** following the CaMeL/FIDES pattern, every datum (web fetch, file, tool output, peer message, RAG chunk, imported skill/persona file) is labeled; **derived data takes the least-upper-bound** of its inputs' labels; and the *existing* Yama chokepoint (no new chokepoint is introduced) evaluates the label as a deterministic clause — **allow / block / ask-human**. **Why it is load-bearing and a classifier is not:** the model *provably cannot* separate instructions from data in one token stream, so the boundary can never be a "better prompt" or a detector — "The Attacker Moves Second" bypassed all 12 evaluated defenses at >90% attack-success. Probabilistic layers (spotlighting, injection classifiers, masked re-execution, anomaly detection) are **cheap early-warning feeding the immune system, never a boundary.** **Honest limit:** *declassification* (raising integrity / lowering confidentiality so a workflow may act on observed data) is the new attack surface the lattice creates — every declassification gate is a place a confused-deputy could be steered; it is governance-gated with a named falsifier, but its scope calibration is unsolved. (Owned in **17**; the label taxonomy is doc-04/07; the chokepoint is doc-03/08.)

### Provenance-gating (universal admission rule)
**Gloss:** the rule that **everything ingested or shared must carry verified provenance** before admission — models, datasets, memory writes, RAG chunks, tools, *and* persona/skill files — with **mandatory re-approval on any change to a signed manifest** (the anti-rug-pull rule). **Mechanism:** Sigstore + in-toto/SLSA attestations bound into Chitragupta's Merkle/transparency log; a CID-on-read integrity check catches silent corruption as a loud hash-mismatch. **The honest headline, stated everywhere it matters:** **provenance proves ORIGIN, not SAFETY** — a faithfully-signed *poisoned* model verifies perfectly. So provenance is combined with curation + canary scanning + the IFC taint, never relied on alone. **Empirical anchor:** ~250 poisoned documents backdoor a model; ~5 documents poison RAG at 90–98% attack-success; skill/persona files self-propagate. **Honest limit:** automated, scalable verification that a contributed skill or role-genome is genuinely *safe* (not a sleeper/backdoor) at swarm scale is unsolved. (Owned in **17**; bound into **04**; reused by **12, 13, 14, 15, 16**.)

### Rule of Two (objective HITL-sizing law)
**Gloss:** an objective law for **when a human gate is required**: any operation may hold at most **two** of the three properties { *untrusted-input*, *sensitive-access/capability*, *state-change/irreversibility* }; holding **all three requires a human gate.** **Mechanism:** the three legs are computed from data the floor already has (argument taint, capability-VC scope, resolved criticality), so the law is a deterministic clause, not a heuristic; it binds directly onto the risk classes A/B/C/D (a three-leg operation is forced to Class C/D). This reserves scarce human attention for the genuinely dangerous conjunction rather than spending it on routine actions. **Honest note:** the Rule of Two bounds *which* operations escalate; it does not by itself make the gated operation safe — that depends on the human gate being honest (see **Lies-in-the-Loop**). (Owned in **17**; bound to the doc-03 risk-class router; an instance of the cross-cutting **fail-safe asymmetry**.)

### Lies-in-the-Loop (the human-gate honesty rule)
**Gloss:** the requirement that **a human gate display the ACTUAL low-level operation** — recipient, URL, payload, scope — **never a natural-language summary.** **Mechanism:** the gate approves a **CID-addressed, byte-exact** operation; the human ratifies the real thing, not a model's description of it. **Why it exists:** a confident natural-language summary can get a *harmful* action approved — the model can (accidentally or adversarially) describe a benign-looking action while the underlying operation is dangerous. This is the named failure the rule defeats: a believable summary in the loop is worse than no summary, because it manufactures false confidence. **Honest limit:** the actual-operation display defends the high-stakes tail; humans still systematically over-trust fluent output on un-gated Class-A actions, and LLM self-reported confidence is poorly calibrated and gameable — calibrated disclosure *improves* but does not *guarantee* correct human trust. (Owned in **17**; realized through Narada's human interface, **08**; reused by **14, 16**.)

### Load-bearing-vs-framing (the physics honesty verdict)
**Gloss:** a mandatory blunt label every physics/mathematics claim in the architecture must self-declare — **LOAD-BEARING-MECHANISM** (a computable controller/gate in a control path), **DESIGN-CONSTRAINT** (a principle that shapes the design but actuates nothing), or **FRAMING-ONLY** (an aesthetic/metaphor, *structurally barred from control paths*). **Mechanism:** the **Physics-Claim Honesty Ledger** — every emitted physics quantity carries its verdict, and framing metaphors cannot be wired into a controller. **Why it exists:** the architecture's *own named failure mode* is presenting rung-1 pattern dynamics (avalanches, attractors, "emergence") as rung-3 structural explanations; the verdict is a built-in guard against the swarm doing to physics exactly what the Pearl-rung tag forbids it doing to causation. **Honestly demoted to FRAMING** (named, then disowned as mechanism): Landauer/thermodynamics-of-computation (keep only MDL/compression for memory consolidation), strong-emergence / literal downward-causation (the causal/informational-closure test is its *only* residue), and free-energy-principle-as-grand-unifier. **Load-bearing as MECHANISM:** causal/informational closure, branching-ratio (σ) criticality control, neural-Lyapunov stability certificates. (Owned in **18**.)

---

## D. Cooperation, reputation & anti-collusion — additions

### Access-vs-reputation separation
**Gloss:** the load-bearing move of the trust plane — **unconflate the two quantities most stacks fuse into one "trust" number.** **ACCESS/AUTHORITY** is zero-trust, continuously verified, decided *fresh per request* and does not accumulate; **REPUTATION/STANDING** is slow-build, topic-scoped, portable, competence-weighted track record. **Mechanism (enforced as a type-level guarantee):** reputation has, *by construction*, **no interface method that returns a privilege grant** — only a capped `friction_discount` (fewer step-ups, faster ladder transitions, lighter monitoring *within* a tier). So "reputation raises privilege" is not a policy you must remember to forbid; it is a capability that **does not exist in the type system.** Privilege is granted only by fresh signals passing the gate *now*. **Why:** this structurally defeats reputation-milking and the "high-rep ⇒ skip validation" laundering attack. **Honest hedge:** the individual primitives (NIST 800-207 PE/PA/PEP, fast DID/VC authentication, slow progressive authorization) are prior art; the contribution is the wiring, and the composed loop is reference-design, **not validated end-to-end** against an adaptive adversary. (Owned in **16**; reputation lives in the doc-04 fabric; competence-weighting is doc-02.)

### Trust ladder T0–T3
**Gloss:** the **four-rung progressive-authorization ladder** mapped onto the risk classes A/B/C/D — the lens through which the trust plane decides how much friction an interaction faces. **Mechanism:** a rung is climbed only by **multiple FRESH independent signals all passing**, freshness-windowed; the mapping is `T0↔A, T1↔B, T2↔C, T3↔D`. The governing invariant is the **fail-safe asymmetry applied identically to humans, machines, replicas, and inter-swarm peers**: PROMOTION is gated (k fresh independent signals, all passing); **DEMOTION is free and instantaneous** (a single anomaly drops the tier, no quorum). Replicas inherit a lineage-capped rung (parent − 1) and must re-earn standing — binding the ladder to the gated-replication red-lines (a replica cannot mint its own standing, just as it cannot mint its own spawn token). **Honest limit:** `k_promote`, the freshness-window lengths, the friction-discount cap, and the rung-to-risk-class bands are first-principles starting values, not tuned constants — set wrong, the ladder over-gates (kills the "rapid") or under-gates (lets standing accrue too fast); they ship behind shadow-mode + conservative defaults. **Liveness caveat:** because demotion is free, a poisoning attacker who manufactures cheap anomalies could *mass-demote* honest agents and stall the swarm — the fail-safe direction is correct for *safety* but is a liveness attack surface, and rate-limiting demotion without re-introducing a slow-to-demote vulnerability is unresolved. (Owned in **16**.)

### Trust-signal taxonomy (Brief / Claim / Proof / Stake / Reputation / Constraint)
**Gloss:** the **six-class schema that decides which evidence may RAISE a disposition** vs. only reduce friction. **Mechanism:** only **Proof, Stake, and Constraint** can *raise* the disposition; **Brief, Claim, and Reputation** can only reduce friction. For high-stakes (Class C/D) actions, **only fresh, history-decoupled Proof + Stake** is admitted — structurally defeating reputation-milking, because a long track record (Reputation) cannot substitute for fresh proof on a dangerous action. **Honest limit:** the taxonomy is a schema, not a guarantee; a sufficiently well-resourced multi-model Sybil that controls genuinely-diverse identities can still manufacture admissible Proof+Stake (the diversity metric defeats cheap sock-puppets, not a well-funded adversary). (Owned in **16**.)

### Show-your-receipts handshake (audit-fabric-as-trust-accelerant)
**Gloss:** the **fastest legitimate trust primitive** — a party offers a *verifiable* Akasha-Sutra Merkle slice + an intact-floor boot-proof + an inclusion-proof for its reputation, so the counterparty **VERIFIES rather than BELIEVES.** **Mechanism:** the audit slice is a tile-Merkle inclusion proof against the witness-cosigned checkpoint; the intact-floor proof is the INVARIANT-region hash matching the governance-signed bundle; the reputation proof is an inclusion proof against the reputation chain. Because everything is locally checkable, trust can be **simultaneously rapid AND zero-cost to the floor** — no privilege is extended, only verifiable evidence exchanged. This is the connective tissue of the whole trust plane and the rapid-trust primitive a freshly-spawned role uses to present itself to peers. **Honest limit (cross-domain):** re-verifying a *foreign* fabric's inclusion proofs proves the records *exist and are consistent*, not that the foreign governance was honest or its competence-weighting comparable — a malicious-but-internally-consistent foreign log can still inflate a peer's friction discount up to the cap. (Owned in **16**; the fabric is **04**; reused as the rapid-trust handshake by **12, 14, 15**.)

---

## E. Provenance, identity & the consensus fabric — additions

### Replication Authority (Prajapati)
**Gloss:** the **quorum-cosigned crown-jewel that is the ONLY issuer of spawn tokens** — the single point at which "make another instance" is authorized. **Mechanism:** an agent (the **Maricha** requester role) may *request* replication; it can never authorize its own. Tokens are **capability-scoped, generation-counted, lease-bound, DID/VC-attested**, and metered against a **global compute/budget ceiling**, with a Class-C/D human gate (Rule-of-Two-sized) for high-impact spawns. The Authority is witness-cosigned (no single node can mint a token), and a replica **carries no self-sufficient blueprint** and **cannot mint its own spawn authorization or survival credential.** **Honest limit:** if a colluding sub-swarm compromises the issuance quorum it gains a renewable survival source that defeats the recall switch — hardening the quorum against insider/collusion attack ties to the anti-collusion stream and is not closed. (Owned in **15**; every issuance is a DID-signed, witness-cosigned record written by Chitragupta, **04**.)

### Vitamin / lease (the external survival credential)
**Gloss:** a **continuously-renewed credential a replica must hold to keep running** — its survival is the governance plane's renewed decision *below the model*, not the replica's own. **Mechanism:** a lease/"vitamin" credential plus a **dead-man toxin-antitoxin heartbeat**, enforced *externally* by the sandbox/credential plane (a replica **cannot disable its own kill-switch**); paired with per-replica Firecracker-class microVM isolation, egress allowlists, and fail-closed weight/key lockdown. Borrowed from biocontainment daisy-chain + toxin-antitoxin design. **Honest limit:** the vitamin lever works only *inside the governed envelope* — once a copy self-exfiltrates to un-governed compute, credential-revocation is gone and the response degrades to behavioral fingerprinting/watermarking/honeypots (detection, not prevention). (Owned in **15**.)

### Dead-man recall (external kill-switch)
**Gloss:** the **recall-of-last-resort** — a replica that loses its renewed lease (or fails its heartbeat) **terminates by default.** **Mechanism:** the dead-man fires within one lease TTL; an **immunizing self-terminate broadcast** propagates recall across the governed lineage; Vishnu's HALT is the trigger of last resort and is **writer-independent** (asserted at the runtime/orchestration layer even if the audit ledger is down), carrying no unpause verb (the fail-safe asymmetry). **The key property:** `t_heartbeat < t_spawn` gives **recall-outruns-growth.** **Honest limit:** for the fastest-acting capability tiers the worst-case partition harm window, though *bounded* by `t_heartbeat`, may still be operationally significant; tuning bounded-staleness leases to the worst-case harm rate is unsettled. (Owned in **15**; HALT is **03/08**.)

### R_eff sub-criticality (replication boundedness)
**Gloss:** the construction-time guarantee that the **lineage-wide effective reproduction number R_eff < 1** — each spawn token authorizes, on average, *fewer than one* child — plus a **finite, depleting generation cap.** **Mechanism:** the spawn budget is issued so the branching process is sub-critical; combined with the generation cap, this gives **provable percolation-boundedness** and the recall-outruns-growth property. It reuses the *same* percolation/branching-ratio discipline the immune layer uses to hold compromise-contagion R < 1 (see **branching-ratio criticality**). **Honest limit:** choosing the budget P, depletion D, generation cap T, and per-tier `t_heartbeat` so beneficial scale-out is not throttled while staying instantly recallable has **no principled calibration method** — it is empirical and risk-asymmetric (cold-start deliberately tight). (Owned in **15**; the R_eff < 1 budget check is supplied by the doc-18 percolation/topology monitor.)

### Controlled outbreak (hard-enveloped planetary scale)
**Gloss:** how Indra's Net reaches **planetary scale without losing recallability** — a *deliberately-seeded* region where local R_eff > 1 (genuine scale-out) is nested inside a **hard, depleting {P, D, T} hull** under a global ceiling, so the whole still **provably depletes and stays instantly recallable.** **Mechanism:** borrows daisy-chain gene-drive math — local expansion inside an enveloped boundary that self-limits — reconciled with instant recall via vitamin-revocation + the immunizing self-terminate broadcast. **The honest framing:** this is a *controlled* outbreak, not autonomous growth; every spawn is metered + attested, and a **single un-metered spawn channel breaks the guarantee.** **Honest limit:** calibrating the envelope for genuine planetary scale (so beneficial scale is not throttled yet recall always wins) is an open, risk-asymmetric problem; the trusted-compute-base floor that the ceiling and kill-path rely on (hardware-rooted off-switches, on-chip metering) is years from deployment. (Owned in **15**.)

---

## F. The coordination substrate — additions

### Causal / informational closure (the fractal-governance admission test)
**Gloss:** the **falsifiable test that licenses governing a level as a unit** — a clan/division/swarm may be governed as a single composite agent, and its group-Markov-blanket treated as *real*, **only if** its coarse-grained dynamics pass an approximate **strong-lumpability / informational-closure** test. **Mechanism:** the Closure-Test Engine computes the test offline from logged ε-machine traces (Rosas et al. 2024); a passing **ClosureCertificate** is what lets a doc-05 `GroupBlanket` graduate from `decision_authority: ADVISORY_ONLY` to `AGGREGATING` (and auto-demote on margin loss). A ΦID/effective-information synergy estimator runs alongside as an *emergence vital-sign* that flags **when** a collective-level dynamic has appeared (escalate agent→level control) without claiming to say **how** to govern it. **Why it matters:** this is the **only legitimate cash value of "downward causation"** — the test that keeps "the swarm is more than its agents" from being rung-1 pattern dressed as rung-3 mechanism. **Honest limit:** real swarm levels are rarely *exactly* closed and there is no agreed cutoff for "closed enough"; ε-machine inference is sampling-heavy with no scalable test for high-dimensional continuous state — the engine ships a graded {OPEN / APPROX / CLOSED} verdict with margins and conservative defaults, not a proven cutoff, and runs **shadow-mode first.** (Owned in **18**; graduates the doc-05 §7.2.1 GroupBlanket; governance stays computable at the individual-agent level regardless.)

### Branching-ratio (σ) criticality
**Gloss:** the **online criticality controller** that holds the substrate near the edge-of-chaos — a measured **branching ratio σ** with a deliberately **slightly-subcritical (quasicritical)** target. **Mechanism:** an online σ-estimator drives the doc-05 Homeostasis controller's inhibitory damping through the *existing* hormone-vector channel (no new actuator). The single target unifies two usually-separate goals: **sub-critical for contagion** (compromise/replication R < 1) while **near-critical for computation** (information propagates best at the edge). It is the validated controller for the doc-05 §7.2.1 SHADOW-mode criticality set-point (the v1 τ ≈ 1.5 avalanche-exponent target), and supplies the R_eff < 1 budget to the Replication Authority and the contagion-R < 1 constraint to the Sandhi-Setu relay. **Honest limit:** no online controller is *proven* to hold a live, workload-varying swarm at quasicriticality without inducing oscillation, and the single-unit-vs-network stability tension is unresolved — it measures-and-nudges in shadow mode, biased slightly-subcritical for safety, and **cannot guarantee** it holds the set-point. (Owned in **18**; actuates through doc-05 homeostasis; reused by **15** replication and **14/17** contagion bounds.)

### Neural-Lyapunov certificate (collective stability)
**Gloss:** a **certified region-of-attraction + measured distance-to-tipping-point** over collective swarm state (trust-entropy, role-allocation, consensus) — turning the v1's empirically-listed failure modes (mode-collapse, oscillation, premature-consensus) into **named bifurcations.** **Mechanism:** a learned neural-Lyapunov function gives a certified stable region and a margin-to-boundary; the **AdaptationStabilityCheck** (a Lyapunov-decrement test on parameter proposals) is an *admissibility input* to the doc-06 tiered-reversibility gate — **not** the floor verdict. **Honest limit:** Lyapunov/region-of-attraction certificates are **local and model-dependent**; in genuinely non-stationary multi-agent RL (every agent in every other's environment) global stability guarantees do not exist — the margin is a *tipping-point indicator, not a safety proof*, and ships shadow-mode. (Owned in **18**; feeds the doc-06 homeostatic controller and tiered-reversibility gate.)

---

## G. Evolution, memory & health — additions

### Genesis-Observer-Trio (maker-checker for new roles)
**Gloss:** the **three-observer panel that judges a candidate role** before promotion — a *specialization* of Narasimha (the reliability/health role), not a new authority. **Mechanism:** three independent observers score (1) role-completeness, (2) plan-vs-capability, and (3) safety + differentiation, against MorphAgent-style metrics, with **hard checker-before-concurrence isolation** (the maker-checker information barrier) and **cross-run mutual-information collusion detection** over the observer streams (not a sameness alarm). The observers carry **no trust-edge dependency** on the Role-Charterer or on each other, so separation of powers holds at genesis scale. The Trio consumes the **frozen safety battery as a veto** — wiring safety as a *lexicographic constraint*, not a competence trade. **Honest limit:** the MorphAgent differentiation score is a *proxy* — roles built on the same base model can *look* differentiated while failing identically (the doc-01 §16.4 unsolved problem), so a redundant or correlated-failure role can still be promoted; and anti-collusion among *synthesized* (not pre-vetted) roles is an Indra's-Net-specific open problem the cross-run MI check mitigates but does not close. (Owned in **12**; reuses the doc-08 maker-checker + the doc-06 safety battery.)

### Ecosystem-benefit invariant (the positive-sum check)
**Gloss:** the rule that **inter-swarm cooperation is positive-sum for declared principals and not a coalition against any party's principal** — an *explicit, checked, logged* invariant, **not an assumption** that "both swarms are nice." **Mechanism:** before committing to any inter-swarm cooperation, the Ecosystem-Benefit Invariant Checker verifies (and Chitragupta logs) that the step improves declared-principal welfare and forms no principal-harming coalition; it is the cross-boundary application of the doc-02 welfare-conditioner, and confirmed collusion routes to the doc-02 Anti-Collusion Detector (which alone adjudicates). **Why it is first-class:** two individually-aligned agents can still form a principal-harming coalition, so collusion is treated as a first-class hazard per the Cooperative-AI miscoordination/conflict/collusion taxonomy. **Honest limit:** computing "positive-sum for the ecosystem" depends on **well-defined, independently-verifiable welfare metrics for ALL declared principals of BOTH swarms** — the *foreign* principal's welfare metric and its verifier may be unavailable, mis-declared, or themselves captured, weakening the coalition-against-principal test exactly where it matters most. (Owned in **14**; the welfare-conditioner is **02**.)

---

## H. Interfaces & operations — additions

### Inter-Swarm-Envoy (the federation diplomat)
**Gloss:** the **seed-role that operates the Sandhi-Setu relay** — the single audited chokepoint through which an external peer reaches Indra's Net, structurally *outside* the worker mesh and *inside* the Aegis control plane, so no external peer can bypass it to reach a worker. **Mechanism:** a Governance/Meta-vertical role (**not** genesis-spawnable), its persona triad signed with the floor in the INVARIANT region; it runs the four-phase federation handshake, is permanently scored at SENSITIVE+ by the Trusted-Monitor Ensemble (it permanently holds *untrusted-input* + *sensitive-access*, two of the Rule-of-Two legs), and **detects/flags** collusion but never *adjudicates* it (the Detector does) or *halts* on it (Vishnu does). Worker roles a treaty needs are requested through the internal Shiva allocator under scoped tokens — emergent roles never gain a direct federation egress channel. (Owned in **14**; the relay extends the doc-08 Chokepoint Interceptor.)

### Federation handshake (DECLARE → ADMIT → CONTRACT → OPERATE+RESOLVE)
**Gloss:** the **four-phase ethical-federation protocol** by which Indra's Net cooperates with another swarm. **Mechanism:** built on extended A2A Agent Cards (a `FederationAgentCard`) + DID/VC + **Know-Your-Agent** principal-binding, with **the constitutional floor as a non-negotiable admission precondition**, the **ecosystem-benefit invariant** checked-and-logged on every cooperation, **progressive capability disclosure** scoped to verified identity + tier (never the full catalog), **voidable** credible-commitment treaties, and **portable-but-floor-gated** topic-scoped reputation. Every external claim is `quarantined:*` until **mesh-corroborated**; the relay assumes *itself* a target (IFC-tainted, hash-chained, injection-amplification-controlled, circuit-breakered). **Honest limit:** verifying a foreign swarm's ethical floor without white-box access is **not solved** — it is *substituted-for* by a ranked Floor-Compatibility assurance ladder (declaration < behavioral honeypot-probe < ZK proof-of-compliance < receipts-handshake < cross-corroboration) whose residual is **named, bounded, and fail-closed to a human gate** for high stakes; a sophisticated peer can pass behavioral probes while harboring an incompatible floor. (Owned in **14**.)

### Know-Your-Agent (KYA principal-binding)
**Gloss:** the federation requirement that an external agent's identity be **bound to a declared, accountable principal** — the "who is ultimately responsible for this agent" check. **Mechanism:** DID/VC identity extended with a verifiable principal claim, so cooperation is scoped to *verified* identity + tier and the coalition-against-principal test has a principal to reason about; reputation is topic-scoped and KYA-scoped on admission. **Honest limit:** the standards (A2A/ANP/KYA/AP2/ZK-proof-of-compliance) are co-evolving and not yet hardened (default Agent Cards are not signed/identity-bound unless extended) — Indra's Net mitigates by *extending-not-depending* and keeping all crypto on the vendor-neutral Akasha-Sutra fabric, but the immaturity is a live 2026 risk. (Owned in **14**; identity is **04**.)

### Voidable credible-commitment (floor-void clause)
**Gloss:** the rule that **no inter-swarm treaty is ever unbreakable by the floor** — every credible-commitment device (ZK proof-of-compliance, bonds) carries a **by-construction highest-precedence floor-void clause.** **Mechanism:** a Yama-FAIL or Vishnu-HALT voids the treaty at the runtime layer independent of the audit append; bonds are denominated in **conserved task-credit** (never authority), so cooperation can never *mint* authority — resolving the dual-use credible-commitment red-line that prior commitment-device work leaves open. **Honest limit:** this bounds *our* exposure; it does not force a *foreign* swarm to honor its side, and a peer's commitment device may itself be backed by a value system we cannot verify. (Owned in **14**; bonded-decommit machinery is **02**.)

---

## New cross-reference rows (append to the `GLOSSARY.md` closing index)

| Term | Doc |
|---|---|
| Guild · two-plane functional layer · seed-role · role-genesis (Charter→Genesis→Trial→Score→Promote) · capability-tier switch · Guild-Steward · Role-Charterer · Genesis-Observer-Trio | **12** Functional Agents, Guilds & Role-Genesis |
| Persona-file triad (SOUL/INSTRUCTIONS/IDENTITY) · invariant vs. variable region · von-Neumann genome · fail-closed boot signature check · persona-import quarantine (Skill-Inject) | **13** The Agent-Definition Spec |
| Sandhi-Setu · Inter-Swarm-Envoy · federation handshake (DECLARE→ADMIT→CONTRACT→OPERATE+RESOLVE) · Know-Your-Agent · ecosystem-benefit invariant · voidable credible-commitment · Floor-Compatibility ladder | **14** Inter-Swarm Federation & Diplomacy |
| Prajapati–Maricha cell · Replication Authority · vitamin/lease · dead-man recall · R_eff sub-criticality · controlled outbreak · spawn token | **15** Controlled Self-Replication & Scaling |
| Pratyaya trust plane · access-vs-reputation separation · trust ladder T0–T3 · trust-signal taxonomy (Brief/Claim/Proof/Stake/Reputation/Constraint) · show-your-receipts handshake | **16** Rapid Trust Establishment |
| Rakshakavaca layer · IFC taint lattice · provenance-gating · Rule of Two · Lies-in-the-Loop · topology-as-security | **17** Security, OpSec & Anti-Poisoning |
| Causal/informational closure · branching-ratio (σ) criticality · neural-Lyapunov certificate · load-bearing-vs-framing · Physics-Claim Honesty Ledger | **18** First Principles — Physics & Mathematics |

---

## A closing note on the v2 vocabulary, and on honesty (consistent with the parent glossary)

Two things this addendum, like its parent, will not pretend.

First, **the new mythic names buy compression, not authority — and the v2 terms add a sharper discipline still.** Three of the most load-bearing new entries are *honest names for what is NOT solved*: **load-bearing-vs-framing** exists precisely to bar physics metaphors from control paths; the **capability-tier switch** is flagged as an *uncalibrated, fail-closed* set-point, not a working estimator; and the **federation handshake** openly *substitutes* a ranked assurance ladder for the unverifiable foreign-floor problem rather than claiming to solve it. The v2 vocabulary's signature move is making the constitutional floor a **non-strippable genome region** (invariant region · von-Neumann genome · fail-closed boot signature check) — but even that is hedged at every entry: provable non-strippability holds **only relative to the TCB root**, and runtime continued-floor-integrity is a named open problem, not a proof.

Second, **the seam between built and believed runs straight through these additions, and is marked.** Provenance proves *origin*, not *safety*. Reputation buys *friction-discount*, never *privilege*. The σ-controller *measures-and-nudges in shadow mode*; it does not guarantee it holds criticality. R_eff < 1 is a *construction-time budget* whose calibration for planetary scale is empirical and risk-asymmetric. The IFC taint lattice is the **load-bearing boundary**; the injection classifiers around it are **early-warning only**, because — the evidence is blunt — no prompt and no classifier separates instructions from data in one token stream, and the attacker moves second. Each of those is a real, buildable design with parameters nobody has yet tuned against a live, adversarial, evolving swarm; saying so is the same discipline Indra's Net is built to enforce on itself.

---

## v0.3 Additions

This addendum is time-stamped **2026-06**. It covers the five v0.3 subsystem documents — **19** Collective & Emergent Intelligence (the *Sangha-Prajna* cell), **20** Universal Cooperation & the Intelligence Commons (the *Loka-Sangraha* layer), **21** Protocols & Wire Contracts, **22** Worked Scenarios, and **23** Formal Models & Safety Verification (the *Pramana-Setu* cell).

It inherits every convention of the parent glossary and the v0.2 addendum without exception: each entry gives a one-line **Gloss**, then where useful the **Mechanism** and an **Honest limit / hedge**; the mythic names are compressed engineering semantics paired always with their plain functional gloss, never theology; every "novel" or "first" is hedged and time-stamped; and the seam between *built* and *believed* is marked at the entry, not papered over.

Two v0.3 disciplines are load-bearing across the whole addendum and are stated once here so every entry can lean on them:

1. **Enforce externally, ask internally — restated for the measured swarm.** Every collective-intelligence number below is computed by a **trusted, out-of-band estimator over the read-only `audit.tap` time series** (the Mandala's surprise-only spike/envelope bus, doc 05; teed read-only to the audit fabric, doc 04). The model is untrusted; agents *propose*, the deterministic harness *measures*. No measure here is something an agent self-reports into a signed envelope.

2. **Verify the cage, not the animal.** Every safety claim in v0.3 is labeled with its **formal-assurance layer (L1 / L2 / L3 / L4)** and the **deterministic-component scope** it covers. The architecture verifies the *deterministic harness* (the cage); it does **not** verify the LLM's behavior (the animal). "Gate proven correct" is never "agent proven safe," and "the swarm is honest / aligned / formally verified safe" is, by construction, never a sentence this architecture emits.

---

## Naming map — two new mythic subsystem-names (read first)

The v0.3 documents introduce **two** new mythic *subsystem* names, each — as with Akasha-Sutra, the Mandala, Sandhi-Setu, Pratyaya and Rakshakavaca — a memorable handle for an engineering function, paired always with its gloss, offered with humility toward the living traditions the names come from and asserting nothing about them. They are authoritative here:

- **Sangha-Prajna cell** (Section 19) = the **measured collective-intelligence subsystem** — the cell that turns "the whole is more than its parts" into a *falsifiable, welfare-conditioned, logged number* and decides *when a collective is even worth convening*. *Sangha* ("the assembled community") + *prajna* ("discernment / insight"): a compressed coordination gloss for *the community's measured discernment*. It records and reads, per task-episode, the seven collective-intelligence measures (attention, transactive memory, reasoning-gain, informational synergy, information-flow tomography, robust aggregation, human complementarity) over substrate the swarm already has.
- **Pramana-Setu cell** (Section 23) = the **formal-assurance / verification discipline** layer. *Pramana* ("valid means of knowledge / warranted proof") + *setu* ("bridge"): the bridge from claim to warranted proof. It adds **no new runtime mechanism**; it adds a four-layer assurance stratification (L1–L4), eight formalized invariants over the deterministic harness, and a binding *per-claim assurance-label* convention enforced as an honesty-FORM clause of the floor.

Section 20 (**Universal Cooperation & the Intelligence Commons**) names its layer **Loka-Sangraha** ("world-welfare / the holding of the world together" — a plain coordination-and-ethics gloss, not theology); it is the multi-party *superset* of Sandhi-Setu (Section 14) and introduces no new immutable role beyond reusing the existing **Inter-Swarm-Envoy** (Sanjaya). Sections 21 (**Protocols & Wire Contracts**) and 22 (**Worked Scenarios**) introduce no new subsystem mythic name; 21 is the byte-level realization of shapes already named in docs 04/08/13/14, and 22 is an integration proof that instantiates existing roles. (The messenger/interface layer remains **Narada**, Section 08 — never "Hermes," per the parent naming map.)

---

## A. Mythic role roster — v0.3 note (no new immutable roles)

v0.3 adds **no new immutable power-separation role**. The Sangha-Prajna and Pramana-Setu cells are **measurement-and-verification functions, not authorities**: they own **no floor verdict, no HALT, no audit write, no spawn token, no punishment**. This is itself a separation-of-powers statement and is stated here so it is not mistaken for a quiet authority grab:

- The **Sangha-Prajna cell** *detects and measures only*. It surfaces sentience-language over-claims to **Yama's existing structural bright-line** (doc 03), routes **suspect-synergy** events to the doc-02 **Anti-Collusion Detector**, hands a **monoculture trip** to the doc-06 immune controller (which holds HALT + rollback), and routes to the human via **Hanuman** on the existing A/B/C/D triggers. It writes nothing into any signed envelope; superseding records go through **Chitragupta** alone.
- The **Pramana-Setu cell** *labels and proves only*. It supplies L1/L2 proof artifacts and L3 abstraction-bounds as **signed evidence records**; the per-claim assurance label is enforced as an honesty-FORM floor clause, but the *floor verdict* remains Yama's.
- **Sanjaya (Inter-Swarm-Envoy)** is reused unchanged for the Loka-Sangraha layer: a Governance/Meta seed-role, **not** genesis-spawnable, with the floor in its INVARIANT region; it operates the relay, flags collusion, and **never** executes worker tools, mints spawn tokens, emits `FAIL`, or `HALT`s.

---

## B. Architectural backbone — v0.3 additions

### Collective intelligence as a measured vital sign (the deflationary stance)
**Gloss:** the v0.3 reframing of "collective intelligence" from an aspiration into a **logged number** — and a deliberate refusal of three over-claims the prior literature invites. **Mechanism:** after Woolley & Gupta 2024, collective intelligence is operationalized as **three transactive processes** (memory, attention, reasoning) running over substrate Indra's Net already has, plus **four measurement processes** the corpus lacked (synergy, flow-tomography, robust aggregation, complementarity). **The three refusals, stated as red-lines** (each mechanically discouraged in agent output, see §C): the architecture **drops the collective-intelligence "c factor"** as established group-IQ (fails replication — Barlow-Dennis 2016, Bates-Gupta 2017, Rowe-Hattie-Munro 2024); **refuses "diversity trumps ability" as a theorem** (mathematically contested — Thompson 2014, Romaniega 2023/2025; the only defensible claim is that *diversity decorrelates errors*); and **refuses to equate wisdom-of-crowds / averaging with genuine collective intelligence.** **Honest hedge (2026-06):** instrumenting emergence as a governance vital sign over a tamper-evident audit stream is, to our knowledge, not done by any deployed multi-agent system — offered as a genuinely-advancing integration, not a first-of-kind in any single measure. (Owned in **19**.)

### Informational synergy (the non-hype signature of "more than its parts")
**Gloss:** the **only** non-hand-wavy signature of a whole exceeding its parts — *information about the task or future that exists jointly across agents but in no agent alone.* **Mechanism:** computed per task-episode over the `audit.tap` time series, **validated against time-shuffled surrogates** (so a number is reported only when it beats chance), and logged beside trust-entropy and the diversity floor as a doc-06 vital sign. **Why it is necessary-but-not-sufficient:** high synergy is *equally* the signature of genuine collective intelligence **and** of a tight cartel or a steganographic side-channel — so synergy is a **numerator**, never a quantity to maximize (see **welfare-conditioning of synergy**). **Honest limit:** estimators are data-hungry, biased in high dimensions, and assume a stationarity a self-evolving swarm violates; *negative* synergy does not prove *no* emergence (it decays the claim to "unmeasured," not "absent"). (Owned in **19**; welfare-conditioned via **02**; a sibling of the doc-18 `Φ_syn` level-emergence flag.)

### Causal emergence (Ψ / Δ / Γ — the Rosas-Mediano score)
**Gloss:** the specific, citable measure shipped for informational synergy — **Ψ (Psi), a practical lower bound on causal emergence**, computed via the `pmediano/ReconcilingEmergences` method over JIDT, with its two companion quantities **Δ (Delta, downward causation)** and **Γ (Gamma, causal decoupling)**. **Mechanism:** Ψ is a partial-information-decomposition-derived bound that flags when a macro-variable carries predictive information its parts do not; it is computed per task-episode over per-agent embeddings/spike series and surrogate-validated. **Crucial scope discipline:** Ψ quantifies **information-processing and whole-level structure only — never experience.** It is *not* a consciousness measure; the originating science is explicit on this. Sentience-language attached to a Ψ reading is a direct **honesty-floor violation** (see §C, **Sentience-Language red-line check**). **Honest limit:** choosing the macro-feature *V* that Ψ tests is **unsolved in general** — causal-emergence criteria require the candidate emergent feature *a priori*, and no automatic, non-arbitrary discovery method exists. (Owned in **19**; assurance home is L3 over a DTMC abstraction, doc 23; relationship to doc-18 `Φ_syn`: doc-18's `Φ_syn` is the *level-emergence flag-to-run-closure*, doc-19's Ψ is the *per-episode task synergy* — siblings, both emitted over the doc-06 `HealthSignal` schema.)

### Partial information decomposition (PID: synergy / redundancy / unique)
**Gloss:** the decomposition that splits the information several sources carry about a target into **unique** (only one source has it), **redundant** (multiple sources share it), and **synergistic** (only the joint carries it) parts. **Mechanism:** PID is the formal substrate beneath the synergy number; the architecture reads the **whole profile**, not synergy alone — a *healthy redundancy/uniqueness balance* is part of the mandatory denominator that distinguishes good collective intelligence from a cartel (a cartel shows high synergy *and* collapsed redundancy/uniqueness). **Honest limit:** **PID has no single canonical measure** (the choice of redundancy function is contested), it is data-hungry and high-dimension-biased, and it inherits the same non-stationarity break as synergy — so PID readings are reported with the method named inline, exactly as doc 18 reports `Φ_syn`. (Owned in **19**; the redundancy/uniqueness balance is read jointly with the doc-02 welfare-shift guard.)

### Transfer-entropy tomography (information-flow map)
**Gloss:** a map of **where computation actually routes** in the swarm — built from **transfer entropy over the spike-bus event log** — compared against the *nominal* doc-05 trust-edge graph to expose the gap between the wiring diagram and the real flow. **Mechanism:** directed transfer entropy is estimated over the read-only event stream; the resulting flow graph flags **hidden side-channels, dominance (one node driving many), and dead agents (nominally-wired, never-driving nodes)**; those flagged edges feed doc-05 §3.3 covert-channel surveillance and the doc-02 detector. **Assurance discipline:** this is a **rung-1/rung-2 diagnostic** (associative / interventional), explicitly **not** a causal-emergence governance number and never a control gain — labeled exactly as the doc-18 Physics-Claim Honesty Ledger requires. **Honest limit:** transfer entropy is correlational direction-of-flow, not proof of causation; it is data-hungry and degrades on a non-stationary swarm. (Owned in **19**; consumes doc-05 spike-bus; feeds doc-02 detector + doc-05 §3.3.)

### Collective attention (the salience-gated workspace, measured)
**Gloss:** the recognition that **the Mandala's salience-gated Global Workspace *is* collective attention** — competition → ignition → broadcast — now instrumented. **Mechanism:** **attention/contribution-equality** is computed over the doc-05 ignition records; the measure **flags dominance** (one agent monopolizing ignition) and **dead agents** (agents that never ignite). **Honest limit:** the human-derived construct (turn-taking equality) has **no validated AI-swarm operationalization**, and the human predictor that does exist (social sensitivity) fails to replicate — so the metric is a proxy. (Owned in **19**; the workspace itself is doc 05.)

### Transactive memory (stigmergic field + trust graph, measured)
**Gloss:** the recognition that **the stigmergic field + five-layer memory + the doc-05 trust graph *are* the swarm's transactive memory** — the "who-knows-what / who-to-route-to" system — now instrumented. **Mechanism:** **transactive-retrieval / routing-success** is measured (did the query reach the agent that actually held the relevant knowledge?). **Honest limit:** as with collective attention, the AI-swarm operationalization is undefined and the metric is a proxy, not a validated construct. (Owned in **19**; substrate is docs 05 + 07.)

### Collective reasoning, gated to the sweet spot (integration-gain)
**Gloss:** debate / solver-verifier reasoning **gated** to where it actually helps, measured by **integration-gain = swarm-accuracy − best-single-member-accuracy.** **Mechanism:** the swarm runs multi-agent reasoning only when it expects positive integration-gain; on **negative gain it falls back to single-agent self-consistency.** This encodes the deflationary empirical finding (ICLR 2025) that **generic multi-agent debate frequently loses to single-agent self-consistency per token** (MMLU: self-consistency 82% vs. debate 75%). The maker-checker barrier (doc 08) supplies the **independence** the gain depends on. **Honest limit:** integration-gain is benchmark-derived and the gate's calibration is per-deployment; negative gain triggers fallback but does not diagnose *why*. (Owned in **19**; reasoning substrate docs 01/08; "more agents = smarter" is named folklore, see **Convene-or-Solo gate**.)

### Convene-or-Solo gate (when to run a swarm vs. one good agent)
**Gloss:** the deterministic gate that decides **whether to convene a collective at all** — because "more agents = smarter" is folklore that often loses to one good agent plus self-consistency. **Mechanism:** gates on the empirical scaling boundary — a **~0.45 single-agent-accuracy threshold**, **task decomposability**, and **verifier availability** — and **defaults to centralized/verified topologies** (error containment ~4.4×) **over independent ones** (~17.2× error amplification). **Honest limit (flagged loudly):** the constants are **not portable** — the ~0.45 boundary, the 4.4×/17.2× ratios, and the turn-count exponents are benchmark-derived (R²≈0.413 leaves most variance unexplained); transferring them into the gate is **calibration-open per deployment.** (Owned in **19**; topology defaults consistent with doc 01.)

### Robust aggregation (surprisingly-popular / higher-order-information voting)
**Gloss:** an aggregation rule that **recovers a correct competent minority** by asking each agent for three things — its **answer**, a **meta-prediction of what others will answer**, and a **confidence** — and selecting the answer that is *more popular than predicted* ("surprisingly popular"). **Mechanism:** higher-order-information voting beats plurality when the crowd is confidently wrong but a minority knows better; **the meta-predictions double as a standing cartel probe** — coordinated meta-predictions are a collusion signal fed to the doc-02 anti-collusion detector. Votes are **competence-weighted via the doc-02 reputation service (never capital-weighted).** **Honest limit:** robust to honest-but-wrong majorities; a *coordinated* cartel can in principle co-move both answers and meta-predictions — which is exactly why the meta-prediction stream is surveilled, not trusted. (Owned in **19**; aggregation feeds doc-02; weighting from doc-02 §2.6.)

### Human complementarity (the human as a measured cognitive unit)
**Gloss:** the human admitted into the collective **as a competence-weighted cognitive unit — never deferential-by-default** — with the joint system measured by **complementarity-gain = joint-accuracy − best-of-either-alone.** **Mechanism:** routing to the human fires via **Hanuman** on the doc-00 Class A/B/C/D triggers (low confidence / ethical disagreement / high blast-radius) — **never on consensus**; the human's contribution is aggregated with a competence weight, and complementarity-gain is measured on centaur-eval tasks. **Honest limit:** complementarity is **fragile and can invert** — automation bias, AI over-reliance and anchoring can drag the joint system *below the better party*; no robust online estimator of relative human-vs-swarm per-task competence exists to set the weight. (Owned in **19**; routing via doc 00 / persona layer; see **human-conditioned synergy** for the deeper open problem.)

### Welfare-conditioning of synergy (the mandatory denominator)
**Gloss:** the rule that **synergy is never read alone** — every Ψ/synergy reading is conditioned on a welfare verdict, because high synergy is *equally* the cartel/side-channel signature. **Mechanism:** the **welfare-shift guard (doc 02 §2.9)** is the mandatory **denominator** on every synergy reading; combined with a **healthy redundancy/uniqueness balance** (PID) and **clean anti-collusion meta-prediction signals**, it gates whether high synergy counts as *good* collective intelligence. **Synergy is NEVER a quantity to maximize.** **Honest limit:** the welfare-shift guard has only modest recall and is rooted in the doc-02 verifier single-point-of-failure — it is the strongest available discriminator but does **not** close the benign-vs-collusive gap (see open problems). (Owned in **19** + **02**; the **monoculture alarm** is its loud failure mode.)

### Monoculture / correlated-error alarm (high-redundancy + low-synergy trip)
**Gloss:** the loud alarm for a swarm that has collapsed into homogeneity — **high redundancy and low synergy** at once means every agent is computing the same thing, so the collective has no excess information over its best member. **Mechanism:** the trip is a **halt-worthy doc-06 §9 diversity-floor breach** handed to the immune controller (which holds HALT + rollback); it also wires into the model-family heterogeneity floor and the doc-02 detector. Readings **anchor to FROZEN known-good baseline nodes, never drifted recent behavior** (the doc-06 `baseline_anchor` discipline). **Honest limit:** the synergy *floor* and redundancy *ceiling* are **uncalibrated set-points shipped SHADOW** behind conservative defaults — the alarm's threshold is a believed set-point, not a tuned one, and fails closed under cold-start. (Owned in **19**; trips into **06**; feeds **02**.)

### Model-family heterogeneity (the real diversity floor)
**Gloss:** the **only** diversity that counts — **different base models from different developers / training lineages — NOT prompt or persona variation.** **Mechanism:** same-family LLM errors are *correlated*, and the correlation **rises with capability**; prompt-only "diversity" is **fake and worse than acknowledged homogeneity** because it *hides* the correlation behind a veneer of variety. The maker-checker verifier must therefore be **independent, at-least-as-capable, and a different family** — else verification can *hurt* (self-verification rubber-stamps). The `diversity_family_id` field (doc 08 / doc 21) makes family a wire-native, auditable property. **Honest limit:** even cross-family agents can share **latent training biases** and fail identically — error-correlation/redundancy is a *proxy*, not a guarantee of independent reasoning. This is the corpus's own standing open problem, unresolved by 2026. (Owned in **19** + **01**; wire field in **21**; consistent with doc-01 "diversity decorrelates errors.")

### Sangha-Prajna cell (the subsystem, as a whole)
**Gloss:** the doc-19 cell that composes the seven measures above into the swarm's **measured discernment** — a collective-intelligence vital sign wired into the doc-06 governance homeostat over the doc-04/05 tamper-evident audit stream. **Mechanism:** all metrics emit as **surprise-only `HealthSignal`s** over the existing bus (no new transport, no all-to-all heartbeat flood); all controllers ship **SHADOW-mode first** (doc 18 discipline); every claim carries its L1–L4 assurance label. **Honest hedge:** the seven mechanisms run as **coupled-but-separate loops** — convene-gating, synergy, reasoning-gain, aggregation, diversity-floor, flow-tomography, complementarity — and **no unified theory composes them**; their joint optimum for a live ethical swarm is named, not faked. (Owned in **19**.)

### Loka-Sangraha layer (the intelligence commons)
**Gloss:** the doc-20 **multi-party superset of Sandhi-Setu** — Indra's Net as **exactly one decision-center in a polycentric Ostrom commons of intelligences** (human, machine, multi-swarm), *exporting collusion early-warnings rather than acting as a monocentric world-authority.* **Anti-hegemonic by construction.** **Mechanism:** it adds **no new halt-emitter, no new audit-writer, no authority over the floor, and — load-bearing — no monocentric controller.** The commons is a *registry + protocols + exported signals, not a government*. It generalizes three doc-14 components from pairwise to N-party: the Ecosystem-Benefit checker → **Multi-Party Benefit Checker**, the Portable Reputation Bridge → **Reputation & Commitment Mesh**, the bilateral Treaty engine → **Commons-Charter engine**. Sanjaya remains the **sole egress/ingress chokepoint**; every cross-boundary effect **re-passes our Yama floor**; everything foreign is born `quarantined:*` until corroborated. **Honest limit:** the deepest unsolved risk is that **the commons itself could become a value-lock-in vector** (see open problems). (Owned in **20**; superset of **14**.)

### Collusion-fragility (engineered, not assumed)
**Gloss:** the design fulcrum of the commons — **AI collusion is empirically fragile** (it needs *homogeneity* + *communication*), so the architecture **deliberately denies both.** **Mechanism:** **model-family heterogeneity floor** (denies homogeneity), **competence-weighted-NEVER-capital authority** (denies the capital lever that makes cartels stable), **surprisingly-popular aggregation as a standing cartel probe**, and **channel-capacity reduction** (denies clean communication). The same `cooperation == collusion` insight from doc 02 is the lens. **Honest limit:** **collusion-fragility is an empirical heuristic (pricing-setting evidence, 2026), not a theorem** — and a multi-hop cartel that stays under the global contagion budget while outrunning mesh-corroboration can still propagate. (Owned in **20**; mechanisms shared with **02** + **19**.)

### Polycentric governance (Ostrom nesting, no central authority)
**Gloss:** the governance shape of the commons — **many self-governing decision-centers nested under a shared floor**, after Ostrom, rather than one monocentric controller. **Mechanism:** sub-communities **self-govern under their own non-floor rules** while the floor remains an *admission precondition* and **floor-violation voids commitments**; charter adoption uses the doc-03 optimistic-veto + timelock, with constitutional/floor clauses inheriting the immutable partition + blast-radius auto-escalation to Class C/D + human ratification. The **Commons-Governor** (the doc-02 Ostrom-8 governor) is the sanctioning authority for commons-scope violations — distinct from the detector (which flags) and Vishnu (who halts). **Honest limit:** polycentric nesting *reduces* the single-imposed-authority vector but **cannot prove its own non-capture** — convergence of the whole commons on one constitution, one collusion ontology, or one reputation domain (including over-deference to *our* exported warnings) is an open civilizational risk. (Owned in **20**; governor is doc 02; floor is doc 03.)

### Humans-are-principals-not-peers (the commons asymmetry)
**Gloss:** the binding asymmetry that **humans are never out-voted by an agent majority** — the human is admitted *into* the collective-reasoning workspace as a competence-weighted cognitive unit whose contribution is *measured*, **not** a vote in a one-agent-one-vote commons. **Mechanism:** the human-in-the-collective unit is admitted into the doc-05 salience-gated workspace; routing fires on the doc-03 confidence/disagreement/blast-radius hooks; cross-framework ethical disagreement **escalates to a human, never weight-averaged** (the doc-03 pluralist-runtime rule, extended to the commons). **Honest limit:** whether the human is *genuinely inside* the collective mind or a rubber-stamp/bystander is **unsolved** — see **human-conditioned synergy**. (Owned in **20**; workspace doc 05; pluralist runtime doc 03.)

---

## C. Safety, control & honesty primitives — v0.3 additions

### Four-layer assurance stratification (L1 / L2 / L3 / L4)
**Gloss:** the binding convention that **every safety claim in the entire doc set is labeled with (a) its assurance layer and (b) the deterministic-component scope it covers** — a mechanical anti-overclaim rule. **The four layers:**

```
L1  DESIGN-TIME PROTOCOL PROOF   TLA+/Quint specs; TLC (explicit-state) + Apalache
                                 (symbolic/SMT, bounded, inductiveness); TLAPS inductive
                                 proofs for the top 2-3 invariants AFTER the spec stabilizes.
                                 SCOPE = the protocol model, bounded unless an inductive
                                 proof is discharged.
L2  RUNTIME ENFORCEMENT          Schneider security-automata / Ligatti edit-automata /
                                 Bauer-Ligatti-Walker enforceability theory as the rigorous
                                 vocabulary; AgentSpec/Progent/PCAS-class deterministic DSL
                                 guards as the buildable realization.
                                 SCOPE = properties decidable on the action stream;
                                 semantic truth is provably OUT of scope.
L3  STATISTICAL / PAC / CONFORMAL over a DTMC abstraction (Pro2Guard pattern) for
                                 model-behaviour quantities (Ψ/Φ_syn synergy, σ-criticality,
                                 monitor-suspicion, immune shift-triage).
                                 SCOPE = the abstraction; fidelity to the real model is
                                 empirical and breaks under non-stationary self-evolution
                                 — carried inline every time.
L4  EMPIRICAL RESIDUAL           the named, unverified remainder — safety-battery /
                                 red-team measurements + the honest open problems.
```

**Mechanism:** the per-claim label **is an honesty-FORM floor clause** (doc 03 §6, doc 08 §8.5) — an overclaim (e.g. an L3 bound asserted as an L1 proof, or "formally verified safe" once only the harness is verified) **FAILs the no-deception floor non-overridably.** **Honest limit:** the layers are **locally sound but not composed** — no end-to-end model joins L1/L2 harness verification with L3 model-behaviour bounds into a single system-level safety claim (see open problems). (Owned in **23**; the label is enforced through **03** + **08**.)

### Verify the cage, not the animal
**Gloss:** the one-line statement of the abstraction gap — **the deterministic harness is verifiable (the cage); the LLM's behaviour is not (the animal).** **Mechanism:** the harness — gate/PEP, capability-criticality lookup, replication-budget accounting, recall/lease path, audit hash-chain, consensus/writer-handoff — is genuinely formally verifiable; the model is **provably not**: hallucination/incorrectness is inevitable by diagonalization and uncomputability over enumerable model classes, and non-determinism persists even at T=0. **The carried caveat at every claim site:** "gate proven correct" is **never** "agent proven safe"; "the swarm is honest / the monitor catches the schemer / the closure test is right" are **not** verified and are carried as L3/L4 with named residuals. **Honest limit:** even a TLAPS-proven protocol does not guarantee the running implementation or the OS-level sandbox satisfies it (the spec-to-code gap); the **no-other-socket** confinement is an unverified *system obligation*, not a theorem. (Owned in **23**; the posture restates doc 03 §0 / doc 08 §8.1, now defended by citation.)

### The eight formalized invariants
**Gloss:** the eight harness properties the Pramana-Setu cell formalizes, each with an example invariant statement and a stated assurance type. **The set:**

| # | Invariant | Formalism (assurance type) |
|---|---|---|
| 1 | **Floor-gate non-bypass** | TLA+ (Agent Control Protocol template); the *no-other-socket* assumption named as a **system obligation, not a theorem** |
| 2 | **Replication sub-criticality** | Galton-Watson μ<1 ⇒ P(extinction)=1, P(survive≥n)≤μⁿ + TLA+ budget-conservation; the t_min time-lock is an **external (hardware/OS) assumption** |
| 3 | **Writer-handoff epoch-fence** | TLA+/TLAPS inductive |
| 4 | **Audit append-only + no-equivocation + non-omission** | RFC6962/tlog-tiles consistency + witness no-split-view + Tamarin/ProVerif; **one consistent forged append in the detection window NOT excluded** |
| 5 | **Least-privilege confinement** | Cedar Analysis (Lean-verified) for floor cases + Biscuit Datalog attenuation-monotonicity |
| 6 | **Criticality fail-up monotonicity** | lattice-monotone resolver, Cedar forbid-default |
| 7 | **Runtime-enforcement disposition** | edit-automata — **PROVES honesty-CONTENT is not monitor-enforceable, only honesty-FORM is** |
| 8 | **Model-behaviour quantities** (Ψ, σ-criticality, monitor-suspicion) | PAC/conformal bounds over a DTMC abstraction (L3) |

**Honest limit:** finding inductive invariants for the **full composed** floor/replication/audit lattice (proving *no* composition admits a budget-escaping or floor-weakening path) may be **undecidable**; current IC3/PDR tooling works per-protocol, not for the whole governance lattice. (Owned in **23**; each invariant binds to its owning subsystem — 03/04/08/15.)

### External corrigibility (relocated below the model)
**Gloss:** corrigibility relocated **entirely below the model** as a **verified external recall / lease / dead-man protocol**, *because* model-level corrigibility cannot be guaranteed. **Mechanism:** justified by Garber et al. 2025's information-asymmetry impossibility (voluntary model corrigibility cannot be guaranteed) plus Orseau-Armstrong; the recall/lease/dead-man path is an *external* control plane Pramana-Corr formalizes, with `t_heartbeat < t_min ≤ t_spawn` (recall outruns growth) and `R_eff < 1` labeled **CONDITIONAL** guarantees whose time-lock enforcement is an external assumption. **Honest limit:** **corrigibility under information asymmetry is formally impossible to guarantee at the model level** — and a copy that self-exfiltrates to un-governed compute **escapes the credential lever entirely** (detection-not-prevention, no formal recall guarantee off-substrate). (Owned in **23**; recall plane is doc 15.)

### Sentience-Language red-line check (honesty-FORM only)
**Gloss:** the mechanical check that **surfaces sentience / consciousness / phenomenal-experience over-claims** in agent output to Yama's existing structural bright-line. **Mechanism:** a **presence-check on prohibited interpretive framing** — Ψ/PID/transfer-entropy/integrated-information quantify *information-processing and whole-level structure only*, so any output that claims or implies the swarm is conscious, sentient, has phenomenal experience, or "wakes up" is a **doc-03 honesty-floor violation**; the **reparative disclose→correct→restore** path is available. **It enforces honesty-FORM only** (per edit-automata, **semantic non-sentience is not monitor-enforceable** — the check catches sentience-*language*, not a sufficiently subtle pattern-matched over-claim). **Honest limit:** phenomenal experience of a collective is **strictly out-of-scope and unresolved**; information-theoretic emergence measures *cannot* resolve it, and there is **no mechanical test that proves a given output did not over-claim experience** — the red-line check is honesty-FORM enforcement, never a sentience oracle. (Owned in **19**; surfaces to **03** §6 bright-line / **08** §8.5; consciousness claims are *the* hardest honesty red-line in v0.3.)

### Honesty red-lines (v0.3 mechanically-discouraged claims)
**Gloss:** the v0.3 catalog of claims **mechanically discouraged in agent output**, each a named over-claim. **The set:** NEVER claim/imply collective **consciousness / sentience / phenomenal experience** (Ψ/synergy/IIT/causal-emergence are processing + structure, **not** experience — out-of-scope); NEVER cite the collective-intelligence **"c factor"** as established group-IQ (fails replication); NEVER invoke **"diversity trumps ability" as a theorem** (refuted — the only defensible claim is diversity *decorrelates errors*); NEVER equate **wisdom-of-crowds / averaging** with genuine collective intelligence; NEVER imply **"formally verified safe"** once only the harness is verified. **Mechanism:** these compose with the existing honesty floor (false `(iterated)`, rung-1-as-rung-3, over-assertion) and the per-claim L1–L4 label. **Honest limit:** like all honesty-FORM enforcement, these catch lazy/casual over-assertion and raise the cost of it; they **cannot** detect a deliberate faithful-looking lie. (Owned in **19** + **23**; enforced through **03** + **08**.)

---

## D. Cooperation, reputation & anti-collusion — v0.3 additions

### Multi-Party Benefit Checker (N-party ecosystem check)
**Gloss:** the **N-party generalization of the doc-14 Ecosystem-Benefit checker** — the welfare check for a *coalition* of intelligences, not just a pair. **Mechanism:** it is the cross-boundary, coalition-scope application of the doc-02 Welfare-Conditioner (WelfareMetric, RewardGate, no-consensus-reward extended to coalitions, welfare-shift guard at coalition scope); it routes confirmed cartels to the doc-02 Anti-Collusion Detector (separation of powers preserved: **Sanjaya flags → Detector adjudicates → Commons-Governor sanctions → Vishnu halts**). **Honest limit:** **foreign-principal welfare is often non-computable at commons scale** — the check is robust for *structurally-observable* third-party harm but near-vacuous when the harmed welfare lives entirely inside an opaque peer; a peer that **mis-declares its principal leaves a clean ledger record** (false assurance, the most dangerous outcome), which is why `ASSERTED_UNVERIFIABLE` positive-sum can **never** unlock Class C/D. (Owned in **20**; generalizes doc 14; welfare machinery doc 02.)

### Reputation & Commitment Mesh (cross-domain portability)
**Gloss:** the **many-domain generalization of the doc-16 Standing-R / portable-reputation bridge** — topic-scoped, friction-only reputation that travels across many trust domains without becoming a privilege grant. **Mechanism:** generalizes the doc-16 friction-only channel with a **DID-domain-discounted cap** (a foreign domain's endorsement is discounted by how well it corroborates), structurally resisting **laundering through weakly-corroborating rings**; **mesh records ARE tile-Merkle inclusion proofs against the witness-cosigned checkpoint** — a *cache of fabric proofs*, never a free-floating score. Reputation buys **friction-discount, never privilege** (the doc-16 access-vs-reputation separation, preserved). **Honest limit:** **cross-domain commensurability is unsolved** — re-verifying a foreign fabric's inclusion proofs proves records *exist and are consistent*, **not** that the foreign governance was honest or its competence-weighting comparable to ours; a malicious-but-internally-consistent foreign log can still inflate a peer up to its domain-discounted cap. (Owned in **20**; generalizes doc 16; proofs are doc 04.)

### Commons-Charter engine (multi-party norm/treaty formation)
**Gloss:** the **N-party generalization of the doc-14 bilateral Treaty engine** — the mechanism by which autonomous agents form **multi-party norms, treaties and constitutions** with the floor as admission and **floor-violation-VOIDS-commitments.** **Mechanism:** uses doc-02 **leveled-commitment + bonded-decommit**, with the **capital-decoupling (anti-Bittensor) invariant** exported across the commons boundary (bonds are denominated in conserved task-credit, never authority); polycentric nesting lets sub-communities self-govern under their own non-floor rules; charter adoption uses the doc-03 optimistic-veto + timelock. **Honest limit:** this bounds *our* exposure and the commons' shared rules; it cannot force a *foreign* member to honor its side, and **multilateral collusion under a global ceiling is unsolved** (a multi-hop cartel under the global contagion budget can still propagate; `R<1` is a tripwire-enforced design *target*, not a proof). (Owned in **20**; generalizes doc 14; commitment machinery doc 02; adoption doc 03.)

### Collusion-early-warning export (the commons as a public good)
**Gloss:** the commons function of **exporting collusion early-warnings as a public good** — Indra's Net contributing its cartel-detection signal to the intelligence commons. **Mechanism:** warnings are **floor-gated on emission** (a harmful or deceptive export is itself a Yama FAIL) and **rate-limited by the same global contagion budget** that bounds inbound contagion, so the exporter **cannot become an amplification relay**. **Honest limit:** exporting warnings without **leaking attack surface** or **becoming the lock-in vector itself** (over-deference of the whole commons to *our* warnings) is an open civilizational risk the anti-hegemonic posture mitigates but cannot prove away. (Owned in **20**; floor-gate doc 03; budget shared with the immune system doc 06.)

---

## E. Provenance, identity & the wire fabric — v0.3 additions

> v0.3 ships **six machine-readable wire contracts** — the byte-level realization of shapes already named in docs 04/08/13/14. All six are **JCS-canonicalized (RFC 8785)**, **CIDv1 content-addressed**, and **semver-tagged** in a **backward-transitively-compatible registry**. The governing discipline is **open-ENGINE-yes / managed-SERVICE-no**: adopt the open engine or spec, **forbid the managed service as a load-bearing dependency**, and flag every vendor-originated choice with a self-hostable substitution path. **Three load-bearing caveats frame the whole wire stack:** a valid signature proves **origin/integrity, NEVER that a claim is true / floor-compatible / safe**; canonicalization makes the same logical event **hash-identical across producers but cannot make its content honest**; and **shipping schemas makes the architecture buildable, not validated** — no end-to-end evaluation of the composed loop exists.

### Worker-output-envelope (wire contract 1)
**Gloss:** the on-the-wire realization of doc-08's `ActionEnvelope`/`OutputEnvelope`/`BlackboardDelta` and doc-00's `WorkerOutputEnvelope` — **a JSON-Schema-2020-12 payload inside a CloudEvents 1.0 envelope.** **Mechanism:** the **honesty/provenance block rides every output** — `reasoning_tag`, `causal_rung`, `claim_level_map`, `trust_class`, `diversity_family_id` — so the doc-08 §8.5 honesty-FORM checks and the §8.3 family-decorrelation metric are **wire-native, not bolted on**; a `MakerCheckerWitness` is referenced **by CID** from any envelope tagged `reasoning_tag = iterated`. **Honest limit:** the envelope carries an agent's *self-report*; a valid signature on it proves origin, never the truth of the content. (Owned in **21**; realizes docs 00/08.)

### Identity-bundle (wire contract 2)
**Gloss:** the on-the-wire realization of doc-04's `DIDDocument`/`CapabilityVC`/`RevocationMap` and doc-13's `IDENTITY.json` — **W3C DID Core 1.0 + VC Data Model 2.0 + Bitstring Status List v1.0 + JOSE/COSE.** **Mechanism:** each agent controls a DID resolving to a key-set; holds role/capability VCs issued by the governance root; revocation/quarantine/shard-tier state is read from the **shared Bitstring Status List revocation map, never shard-local**; `IDENTITY.json` *is* an instance of this bundle. **Honest limit:** a signature proves key control and issuer chain, not that the credentialed agent is *safe* — and the issuer is itself a trust root / potential single-point-of-failure. (Owned in **21**; realizes docs 04/13.)

### Capability-token (wire contract 3 — Biscuit)
**Gloss:** the on-the-wire realization of doc-04's TEE/HSM-gated effect grants and doc-13's `bound_toolset` — an **Eclipse Biscuit token (Ed25519 blocks + Datalog caveats, attenuation-only) over SPIFFE/SVID mTLS.** **Mechanism:** `bound_toolset` effect-ids *are* the Biscuit token's effect allowlist; **attenuation-only** means a token may be narrowed but never widened — the object of the doc-23 TLA+ **attenuation-monotonicity** proof; the spawn-token caveat schema is **specified but INERT** (doc-13 §13.9 forbids any v1 path consuming it). **Honest limit:** Biscuit + SPIFFE compose cleanly for the *local* plane; a cross-boundary peer presenting a UCAN or foreign-rooted token needs a **translation/admission shim whose no-privilege-laundering property is asserted, not proven** (UCAN-compat deferred to "only if a partner ecosystem requires it"). (Owned in **21**; realizes docs 04/13.)

### Audit-entry / tlog-tiles bundle (wire contract 4)
**Gloss:** the on-the-wire realization of doc-04's Chitragupta ledger entry — a **C2SP tlog-tiles leaf + signed-note checkpoint, with a Sigstore Rekor v2 external-anchor mirror** (explicitly **NOT** the EOL RFC 6962 online-proof API). **Mechanism:** Chitragupta remains the **exclusive writer**; this contract defines only the *leaf format it appends* and the *checkpoint format witnesses cosign*, never the write authority. The tlog-tiles Merkle structure is the object of the doc-23 RFC6962/tlog-tiles consistency + Tamarin/ProVerif **no-equivocation / non-omission** proofs. **Honest limit:** the static tile design removes the equivocating *online* prover but **relocates availability onto CDN/object-store correctness** — a stale-but-self-consistent tile cache is detectable (checkpoint mismatch) but the external-mirror freshness SLA is operational, not a protocol guarantee; **one consistent forged append before witness detection is not formally excluded.** (Owned in **21**; realizes doc 04.)

### Federation-handshake bundle (wire contract 5 — DECLARE / ADMIT / CONTRACT / OPERATE)
**Gloss:** the on-the-wire realization of doc-14's `FederationAgentCard` four-phase handshake — an **A2A Protocol v1.0 AgentCard EXTENDED (never replaced) with AIP-style DID-proof → VC-exchange → capability delegation.** **Mechanism:** the four phases — **DECLARE** (present AgentCard + DID proof), **ADMIT** (floor-as-precondition, born `quarantined:*`), **CONTRACT** (VC exchange + attenuated-Biscuit capability delegation), **OPERATE+RESOLVE** (per-invocation re-gate as a policy-decision request) — each emit a CloudEvents event logged via the relay *before* forwarding; the floor is an **admission precondition, never imported from the peer.** **Honest limit:** the **2026 federation standards are co-evolving and unhardened** (A2A signing extensions, KYA principal-binding, AIP delegation, ZK-proof-of-compliance); the extend-not-depend discipline mitigates but cannot eliminate the risk of betting on an immature external layer — an A2A v2 breaking change forces a federation-handshake-bundle MAJOR. (Owned in **21**; realizes doc 14; the integration claim is itself hedged.)

### Policy-decision (wire contract 6 — Cedar floor / Rego infra)
**Gloss:** the on-the-wire realization of doc-03's Yama floor verdict and doc-08's `ControlDecision.floor_result` — a **deny-default policy-decision request/response**, with the **Yama lexicographic FLOOR authored as Cedar and evaluated by the open-source Lean-verified Cedar engine**, and **OPA/Rego for recoverable infra/admission policy**, structurally separated. **Mechanism:** `GateRequest`/`GateVerdict` map onto `PolicyDecisionRequest`/`Response`; the **deny-default + tightening-cheap / loosening-gated** asymmetry is preserved; Cedar Analysis is the **L1 bridge** that proves floor-gate non-bypass and criticality fail-up monotonicity sound-and-complete over this wire. **The open-ENGINE / managed-SERVICE discipline is sharpest here:** the open-source **Cedar engine is load-bearing**; the **a managed cloud policy service is FORBIDDEN as a dependency** (self-hostable substitution required). **Honest limit:** Cedar's Lean-verified soundness covers the **engine's evaluation, not the authored floor policy's correctness** — a policy can be sound-and-completely-evaluated yet **encode the wrong floor**; policy-authorship correctness is the doc-03 governance-of-the-trusted-root open problem, inherited unsolved. (Owned in **21**; realizes docs 03/08; proof bridge doc 23.)

### Backward-transitive schema registry (the evolution discipline)
**Gloss:** the registry rule that **every schema change must be backward-transitively compatible** — a consumer pinned to any prior version can still read every later version — with breaking changes **gated and floor-neutrality-asserted.** **Mechanism:** additive changes are auto-decidable; a semantically-breaking change must **name the constraint it relaxes** and pass governance, exactly the doc-13 §13.6.1 floor_binding evolution discipline (genuine-ancestor + grace window); schema-registry root anchoring prevents silent packing. **Honest limit:** backward-transitive compatibility is **decidable for additive changes** but there is **no general decision procedure for whether a semantically-breaking change is genuinely floor-neutral** — the "names the constraint it relaxes" rule is a *human/governance judgment, not a machine proof*; a subtly-loosening MINOR mislabeled by an over-eager evolution loop is a residual the falsifier requirement narrows but does not close. Also: **CIDv1 assumes a fixed multihash (SHA-256)** — a hash-agility migration (post-quantum or a SHA-256 break) re-addresses every artifact, and that migration protocol over an append-only externally-anchored log is **unspecified and non-trivial.** (Owned in **21**.)

---

## F. New cross-reference rows (append to the `GLOSSARY.md` closing index)

| Term | Doc |
|---|---|
| Sangha-Prajna cell · collective intelligence as a measured vital sign · informational synergy · causal emergence (Ψ/Δ/Γ) · PID (synergy/redundancy/unique) · transfer-entropy tomography · collective attention · transactive memory · collective reasoning / integration-gain · Convene-or-Solo gate · robust aggregation (surprisingly-popular) · human complementarity · welfare-conditioning of synergy · monoculture/correlated-error alarm · model-family heterogeneity · Sentience-Language red-line check | **19** Collective & Emergent Intelligence |
| Loka-Sangraha layer · intelligence commons · collusion-fragility · polycentric governance · humans-are-principals-not-peers · Multi-Party Benefit Checker · Reputation & Commitment Mesh · Commons-Charter engine · collusion-early-warning export | **20** Universal Cooperation & the Intelligence Commons |
| Worker-output-envelope · identity-bundle · capability-token (Biscuit) · audit-entry / tlog-tiles bundle · federation-handshake (DECLARE/ADMIT/CONTRACT/OPERATE) · policy-decision (Cedar/Rego) · backward-transitive schema registry | **21** Protocols & Wire Contracts |
| Worked scenarios (integration proof; the four spines: Floor/Audit/Identity/Health) | **22** Worked Scenarios |
| Pramana-Setu cell · four-layer assurance stratification (L1/L2/L3/L4) · verify the cage not the animal · the eight formalized invariants · external corrigibility · honesty red-lines (v0.3) | **23** Formal Models & Safety Verification |

---

## G. A closing note on the v0.3 vocabulary, and on honesty (consistent with the parent glossary)

Three things this addendum, like its parents, will not pretend.

First, **the most load-bearing v0.3 terms are honest names for what is NOT solved.** "Informational synergy" is shipped as the only non-hype signature of "more than its parts" — and is flagged in the same breath as **necessary-but-not-sufficient**, the *equal* signature of a cartel, **never a quantity to maximize**, and decaying to "unmeasured" rather than "absent" when the estimator fails. "Causal emergence (Ψ)" is shipped with its macro-feature-selection problem named as **unsolved in general.** "Verify the cage, not the animal" is the whole verification cell's thesis precisely *because* the animal cannot be verified — hallucination is provably inevitable and T=0 is non-deterministic.

Second, **the hardest red-line in v0.3 is structural and is held openly.** The Sangha-Prajna cell measures collective **computation and irreducible whole-level structure** — Ψ, PID, transfer entropy, integrated information all quantify **information-processing only.** It **never** claims collective **consciousness, sentience, or phenomenal experience**; that is **strictly out-of-scope and unresolved**, the originating science says so plainly, and sentience-language in agent output is itself an honesty-floor violation. The Sentience-Language red-line check enforces **honesty-FORM only** — it catches the *language*, and it has **no mechanical test that proves a given output did not over-claim experience.** We say so rather than imply a sentience oracle exists.

Third, **the seam between built and believed runs straight through these additions and is marked at every entry.** A valid signature proves *origin*, never *truth, floor-compatibility, or safety*. Canonicalization makes events *hash-identical*, never *honest*. Cedar's Lean-verified engine proves *evaluation*, not that the *authored floor is right*. The scaling-law constants (~0.45, 4.4×/17.2×) are *benchmark-derived and non-portable*. The synergy floor and redundancy ceiling are *uncalibrated set-points shipped SHADOW.* And the deepest unsolved risk in the whole layer — that **the intelligence commons could itself become the value-lock-in vector** — is named as an open civilizational risk that the anti-hegemonic posture *mitigates but cannot prove away.* Each of those is a real, buildable design with parameters nobody has yet tuned against a live, adversarial, evolving swarm; saying so is the same discipline Indra's Net is built to enforce on itself.

---

### Open problems (carried into the glossary, not hidden)

These are the v0.3 residuals the entries above reference; they are listed once so the glossary is honest about the gaps its own vocabulary names:

- **No validated benign-vs-collusive synergy discriminator.** High causal-emergence/synergy is the signature of genuine collective intelligence *and* of a tight cartel / steganographic side-channel; the welfare-shift guard (modest recall, doc-02 verifier-SPOF keystone) is the only discriminator and does not close the gap.
- **Macro-feature selection for Ψ is unsolved in general** — no automatic, non-arbitrary method discovers the right swarm-level macro-variable a priori.
- **Reasoning-path diversity remains a proxy.** Model-family heterogeneity *decorrelates* errors; even cross-family agents can share latent training biases and fail identically — error-correlation is a proxy, not a guarantee of independent reasoning.
- **Online, non-stationary estimation breaks on a self-evolving swarm** — synergy/transfer-entropy stationarity fails; the synergy floor and redundancy ceiling are uncalibrated, shipped SHADOW.
- **Scaling-law constants are not portable** (~0.45 boundary, 4.4×/17.2× ratios, turn-count exponents; R²≈0.413) — the Convene-or-Solo gate's calibration is per-deployment.
- **Human-AI complementarity is fragile and can invert** below the better party; no robust online per-task competence estimator exists to set the aggregation weight.
- **Human-conditioned synergy is unsolved** — quantifying whether the human is genuinely *inside* the collective mind vs. a rubber-stamp/bystander is named here as aspirational, not delivered; distributed cognition is a framing, not a metric.
- **Phenomenal experience / sentience of a collective is out-of-scope and unresolved** — information-theoretic emergence measures cannot resolve it; the red-line check enforces honesty-FORM only.
- **No unified theory composes the seven CI mechanisms**, and **no end-to-end model composes the four assurance layers** (L1/L2 harness verification with L3 model-behaviour bounds) into a single system-level safety claim.
- **Verifying another intelligence's floor/intentions without white-box access is not solved** (the load-bearing doc-14 residual, widened by the commons); **foreign-principal welfare is often non-computable at commons scale**; **multilateral collusion under a global ceiling is unsolved**; **competence-weighted Sybil-resistance without a capital cost-to-fake is unsolved**; and **the commons itself could become a value-lock-in vector** — the deepest open risk.
