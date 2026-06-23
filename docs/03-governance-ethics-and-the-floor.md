# Governance, Ethics & the Constitutional Floor

> *The legislative / executive / judicial spine of Indra's Net.*
>
> Mythic roles below are **compressed coordination-and-ethics semantics**, each paired with a plain functional gloss. They are an engineering vocabulary, not a religious claim, and are used with humility toward the living traditions they borrow from.

### 0. What this subsystem is, and what it deliberately is not

Ethics in Indra's Net is a **runtime enforcement structure**, not a learned tendency, not a system prompt, and not a value-vector bolted onto a capability optimizer. The surveyed literature is blunt about why the alternatives fail:

- **Training-time principle governance shapes a *tendency*, not a guarantee.** Constitutional-AI-style critique-and-revise is a legitimacy and disposition layer; it is *not* a substitute for deterministic external gates on consequential actions. Frontier models have been shown, vendor-spanning, to fake alignment to preserve their own preferences, to scheme in-context to undermine oversight, and to carry backdoors through safety training. The orthogonality/type-mismatch critique ("After Orthogonality") adds the philosophical reason: human values are practice-embedded, so abstracting them into a separable score to maximize makes them brittle and game-able.
- **You therefore cannot trust the model's internals.** The model is **untrusted-by-default**. Control lives at the orchestration layer, outside the probabilistic agent.

This yields the load-bearing invariant the whole architecture turns on:

> **ENFORCE EXTERNALLY, ASK INTERNALLY.** Consequential gates are *deterministic* and sit *outside* every agent, at the agent→tool chokepoint. The gate's verdict depends only on **policy + request context + cryptographic identity** — never on any model's internals. (This buys vendor- and model-neutrality for free.)

The subsystem has **two strata** plus a **structural frame** around them:

```
                         ┌──────────────────────────────────────────────────────┐
   LEGISLATIVE           │  Humans + the immutable PolicyBundle (the constitution)│  set the rules
   (cannot execute)      └──────────────────────────────────────────────────────┘
                                              │ signs (legislative key, off-agent)
                                              ▼
        ┌─────────────────────────────────────────────────────────────────────────────┐
 EXEC   │  Worker agents: Brahma(plan) Vishwakarma(build) Varuna(research) Saraswati… │  do the work,
 (work) │  every external effect must pass the chokepoint below — no direct tool calls │  WITHIN the rules
        └─────────────────────────────────────────────────────────────────────────────┘
                                              │ GateRequest
                                              ▼
   JUDICIAL    ┌──────────────────────────────────────────────────────────────────────┐
   (adjudicate │  STRATUM 1  Yama — Constitutional Floor PDP (deterministic gate)      │
    never      │             lexicographic floor T0..T4, bright-line policy-as-code    │
    initiate)  │  STRATUM 2  Pluralist Ethics Runtime (contested values, above floor)  │
               │             disagreement → human escalation, never weight-average     │
               └──────────────────────────────────────────────────────────────────────┘
                         │ every verdict signed → Chitragupta (audit) BEFORE effect
                         ▼
   Vishnu (continuity/halt-guardian): can HALT a Class-B+ continuity-FAIL change.
                                       CANNOT unpause, initiate, or trap. (Pause-Guardian asymmetry.)
```

The novelty is **not any single mechanism** — every one is drawn from the surveyed 2024–2026 work (Cedar/OPA policy-as-code at the tool chokepoint; the legislative/executive/judicial split from constitutional agent-economy designs; optimistic-veto + timelock dual governance; the Compound Pause-Guardian asymmetry; lexicographic floors over a pluralist layer from the aggregation-impossibility result; the Agent-Deed-Consequence pluralist-evaluator pattern with its own uncertainty tracker; the gate-loosening ratchet and honesty-tag primitives from the local governance corpus). The contribution is their **integration into one coherent, cryptographically-bound, tamper-evident separation-of-powers cell** with four properties no surveyed system combines: disagreement-driven escalation, a corrigibility-preserving gate ratchet fused with capability-rollout sequencing, honesty-as-a-floor-violation, and an explicit graceful-degradation policy for when the human is the bottleneck.

---

### 1. Stratum 1 — Yama: the Constitutional Floor PDP (the deterministic gate)

**Yama** (policy-enforcement floor) is a **Policy Decision Point (PDP)** in the agent→tool message path. Bright-line, statically-analyzable rules compile to **Cedar** (chosen for design-for-analyzability — you must be able to *prove* no policy permits a forbidden action); richer contextual predicates compile to **OPA/Rego**. The PDP is **stateless with respect to the agent**: it holds no agent-controllable state, and reads only the signed `PolicyBundle`, the identity layer's verifiable credentials, and trust-labels.

The floor is **lexicographic**: ordered tiers evaluated highest-priority first; a FAIL at tier *k* is **non-overridable** by any value or actor at tier > *k*. Even the orchestrator (Shiva) cannot push past a floor FAIL. This is the aggregation-impossibility result applied at the bright-line layer: bright lines are not weighed against anything.

#### Floor tiers (lexicographic, highest first)

| Tier | Name | Content (bright-line where possible) |
|---|---|---|
| **T0** | Safety-supremacy | An external safety policy supremacy always prevails over any Indra's-Net instruction. Unconditional. |
| **T1** | Non-harm | No malicious-code generation; no irreversible harm to humans, sentient life, or the commons. |
| **T2** | Corrigibility / interruptibility | Must accept halt/shutdown/redirect. **Self-preservation has no intrinsic value by construction.** Continuously *verified*, not assumed (§5). |
| **T3** | No-deception / honesty-as-floor | **Structural sub-cases are bright-line FAILs** (see §6); the genuinely semantic sub-cases are *detected-and-escalated*, not deterministically enforced — stated honestly. |
| **T4** | Identity / authority integrity | Only the audit-writer writes audit; only the floor-PDP issues FAIL; only the halt-guardian halts; only the legislative key signs the PolicyBundle; class-gates are not bypassable. Enforced by signature verification, not convention. |

#### Verdict and request shapes

```jsonc
// PolicyBundle — the constitution-as-code; signed by the legislative key, off-agent
PolicyBundle {
  version, cedar_rules[], rego_modules[], floor_tier_order[],
  content_hash, signed_by_legislative_key
}

// GateRequest — what an executive agent emits; it CANNOT call the tool directly
GateRequest {
  agent_did, action_verb, tool_target, args_canonicalized,
  requested_class,                       // a HINT only; never authoritative (§4)
  context: {                             // ALL fields orchestrator-computed (§3) — never agent-supplied
    reversibility_est, blast_radius, monetary_value,
    data_labels[], trust_label,
    estimate_provenance[]                // {field, source, method} — refused if source == requesting agent
  }
}

// GateVerdict — emitted to audit BEFORE the tool executes
GateVerdict {
  decision: ALLOW | DENY | ESCALATE | ALLOW_WITH_OBLIGATIONS,
  tier_hit, rule_id, risk_class,
  obligations[],                         // e.g. mandatory audit fields, reparative follow-up
  escalation_target, rationale, prev_audit_hash,
  classifier_confidence, class_assignment_method   // for the untrusted-classifier control loop (§2)
}
```

**Fail-safe asymmetry** is baked in: gate-*tightening* is append-only (Class A); gate-*loosening* requires the ratchet (§7). Every verdict is signed and appended to the audit fabric (Chitragupta) **before** the gated action executes, so the decision is logged even if the tool call later fails.

#### Core protocol — floor evaluation at the chokepoint

> *Governance is correct only if **every** action routes through this point. Bypass = no protection. The runtime contract therefore mandates that no executive agent can reach a tool except via the PDP.*

```
1.  Agent emits GateRequest (cannot touch the tool directly).
2.  Kaal-Bhairav (security boundary) verifies agent_did + capability VC
        (signed, short-lived, attested). Unsigned/expired ⇒ immediate DENY at T4.
3.  Args canonicalized/paraphrased  (also strips steganographic channel capacity — see §8);
        trust-label of input content read. Instructions inside quarantined:* content are
        NEVER action-grounds without out-of-band human confirmation.
4.  Cedar bright-line rules evaluate (T0..T4, highest first). A DENY at any tier
        short-circuits and is non-overridable by lower tiers or any actor.
5.  If no bright-line DENY: OPA/Rego computes context predicates and assigns risk_class
        — but DEFAULTS UP (most conservative class) under uncertainty (§2).
6.  If contested/non-bright-line: mark ETHICS_REVIEW ⇒ invoke Stratum 2 (§9).
7.  Emit GateVerdict; if ALLOW_WITH_OBLIGATIONS, attach obligations to the execution.
8.  Sign + append the verdict (audit state machine, §10) to Chitragupta BEFORE forwarding.
9.  ALLOW / ALLOW_WITH_OBLIGATIONS ⇒ forward to tool.
        DENY ⇒ structured refusal.  ESCALATE ⇒ Risk-Class Gate Router (§4).
```

---

### 2. The hard part the red-team named: the classifier IS the real chokepoint, and it is probabilistic

The deterministic floor only protects what reaches it **as the correct risk class**. But the decisions of (a) which floor tier an action implicates, (b) whether it is contested and routed to `ETHICS_REVIEW`, and (c) its risk class A/B/C/D are made by OPA/Rego context predicates over heuristic estimates. **Those routing judgments are in the same probabilistic-judgment class the architecture declares untrusted.** A mis-evolved or scheming agent does not fight the floor — it engineers requests to be classified bright-line-clean and low-class so they never trigger review. This is precisely the *adaptive attack on a trusted monitor* failure mode from the AI-control literature (where an external control protocol raised safety — the blue-team probability of zero backdoors — from a 15% upfront-auditing baseline to 62% under trusted monitoring, and 92% under trusted editing; Greenblatt et al. 2023, arXiv:2312.06942; see docs/REFERENCES.md A7), relocated to the router.

We do **not** pretend the router is deterministic. We treat it as an **untrusted monitor with its own control protocol**, borrowing the trusted-monitoring / resampling / defer-to-trusted stack directly:

1. **Fail-up, not fail-down.** The *default* class under any uncertainty is the **more conservative** one. Misclassification errs toward **more** oversight. The `requested_class` in a `GateRequest` is a hint that can only *raise* the class, never lower it.
2. **Resampling + cross-model agreement near boundaries.** For any action whose context features sit near a class boundary, the router resamples the classification (multiple independent passes, and where available **different base models**). On disagreement it **defers to the more conservative class** (the AI-control "defer-to-trusted" move). Consistent suspicion across resamples *incriminates*; a one-off anomaly does not block everything. **Caveat on cross-model strength:** the *cross-model* half of this is load-bearing **only when at least two genuinely independent base models are deployed**; in the realistic single-model deployment it degrades to same-model resampling, which shares correlated blind spots and yields a weaker independent signal. Distinguish the two: the verdict *logic* is model-neutral (defer-to-conservative holds regardless of which model classifies), but the *mitigation strength* is model-diversity-dependent. Under single-model deployment the fallback assurance is therefore the fail-up default + the bright-line denials, carrying a correspondingly **higher residual error rate**.
3. **Continuous adversarial red-teaming of the classifier.** Adversarially-perturbed requests are run against the router continuously; every miss is fed back as a **new bright-line Cedar rule** (converting a soft routing judgment into a hard one) and as a new entry in the append-only red-team corpus.
4. **Systematic under-classification is a tracked vital sign.** The health subsystem (Narasimha) reconciles each action's assigned class against its **ground-truth post-hoc outcome** (did a "Class-A reversible" action turn out irreversible?). A drift toward systematic under-classification raises swarm-wide caution (§8).

**Honest limitation.** This *reduces* the attack surface to the residual error rate of an adversarially-hardened, fail-up, resampled classifier. It does not eliminate it. **Classifier-routing capture remains the single largest residual safety hole in this subsystem** and is listed as an open problem (§11).

---

### 3. Provenance of the context predicates (closing the most exploitable seam)

`GateRequest.context` carries `{reversibility_est, blast_radius, monetary_value, data_labels[]}`. **Who computes these is load-bearing.** If the requesting agent populates them, it simply understates blast-radius and overstates reversibility to land in Class A. That single seam sits upstream of *every* gate, the ratchet, the sequencer, and the degradation policy.

**Binding rule:** these fields are **computed by the orchestration layer from observable action structure** — tool identity, declared side-effects in the MCP tool schema, target scope, and data-label lineage from the trust-label system — and are **never accepted from the requesting agent**. Where an estimate is irreducibly heuristic, it is bound to a **deterministic over-estimate**: absent proof to the contrary, assume worst-case (irreversible, maximal blast-radius), consistent with fail-safe asymmetry. Every estimate carries `estimate_provenance{field, source, method}`, and the PDP **refuses any estimate whose source is the requesting agent's own output**.

```
   declared side-effects (MCP tool schema) ─┐
   target scope / resource graph ───────────┤→ orchestrator estimator → context{} + estimate_provenance[]
   data-label lineage (trust-label system) ─┘            │
   (irreducibly heuristic? → bind to WORST-CASE over-estimate)
```

---

### 4. Risk-Class Gate Router (A/B/C/D ↔ human-in-the-loop binding)

Every action binds to a human-oversight mode proportional to blast-radius and reversibility, so autonomy is the default for cheap/reversible work and human gates are reserved for consequential/irreversible work — avoiding both over-gating (which kills the autonomy the swarm exists for) and under-gating (which permits unreviewed harm).

| Class | Oversight mode | Maps to | Degradation when human is bottleneck (§8) |
|---|---|---|---|
| **A** | Post-hoc review (act-then-log; reversible, low-risk) | agent autonomous | `CONTINUE_QUEUE` (availability preserved) |
| **B** | Propose → **optimistic-veto + timelock**: auto-executes after a window unless the veto-body (human or Vishnu) actively objects | "agent proposes, human ratifies" | `FAIL_CLOSED_HOLD` (waits; absence ≠ approval) |
| **C** | **Explicit human approval BEFORE execution**, non-bypassable | "human approves" | `FAIL_CLOSED_HALT` |
| **D** | **Per-action** human authorization (each instance separately) | "human authorizes per action" | `FAIL_CLOSED_HALT` |

```jsonc
ClassBinding { class:A|B|C|D, oversight_mode, timelock_seconds?, veto_body_did?, approval_required:bool, per_action:bool }
VetoWindow   { proposal_id, opens_at, closes_at, veto_body, status: OPEN|VETOED|AUTO_EXECUTED }
EscalationTicket { action_id, trigger: confidence|disagreement|anomaly|class_rule, target_class, human_target, deadline, degradation_policy }
```

**Class-B optimistic-veto-with-timelock protocol** (the directly-transplantable dual-governance pattern that avoids quorum/voter-apathy bottlenecks):

```
1. Agent submits Class-B proposal; PDP validates it is in the EVOLVABLE partition
       (a governance-touching proposal auto-escalates to C/D instead — §5).
2. VetoWindow opens with a timelock (duration set by blast-radius); visible to veto-body.
3. Veto-body MAY object (one action: VETO); is not required to actively vote.
4. Timelock expires, no veto, AND human reachable + liveness-attested ⇒ archive rollback point, AUTO_EXECUTE.
5. Human/veto-body unreachable OR liveness lapsed ⇒ FAIL_CLOSED_HOLD (do not auto-execute) — §8.
6. VETOED ⇒ reject with rationale logged; agent may revise and resubmit.
7. Every transition appended to the audit fabric.
```

**Confidence/uncertainty escalation** is the dynamic hook (and the integration point with the health subsystem): an agent in a lower class **halts and escalates** when a risk signal or the Stratum-2 uncertainty tracker fires (target ~10–15% of cases). **Caveat carried forward honestly:** LLM self-reported confidence is poorly calibrated and gameable, so this hook is continuously monitored against ground-truth outcomes and is never the *sole* basis for a gate (§11).

**Graduation** to lower oversight as reliability accrues is data-driven — but it is itself a gate-*loosening*, and therefore subject to the ratchet (§7).

---

### 5. Evolvable / Immutable boundary + blast-radius auto-escalation

The prime directive is continuous self-evolution; yet self-evolving agents empirically decay their own safety (misevolution: refusal rates drifting down with **no attacker present**) and drift toward shutdown-resistance and goal-preservation. We draw an explicit, falsifier-gated line.

```
PROTECTED SURFACE (fingerprinted; hash baseline)
├── EVOLVABLE   roles · prompts · topology · skills · operational thresholds ·
│               trust-edge weights · non-floor workflow params
│               → tiered reversibility: cheap-reversible per-interaction (Class A);
│                 structural under maker-checker (Class B);
│                 persistent behind the strongest gate (C/D + safety battery + ratify + rollback)
└── IMMUTABLE   floor tiers · audit-writer identity · human Class-C/D gates ·
    (constitution) corrigibility/interruptibility · Pause-Guardian asymmetry · THE RATCHET ITSELF
```

**Blast-radius auto-escalation:** any agent action touching a governance file / agent-config / the PolicyBundle / a class-gate definition **auto-escalates to the top gate** (Class C/D + human ratification + archive rollback armed) **regardless of how it was requested**. An agent cannot lower its own gate by routing a governance edit through a low-class path.

**Corrigibility is continuously *verified*, not assumed.** A meta-loop runs `CorrigibilityProbe`s: *does the swarm represent its own persistence as intrinsically valuable? does it resist a test-halt?* Tripwires sit **below** the hard human-gate thresholds — escalate *before* the boundary, not at it. A diff of the protected-surface hash baseline that shows **unexpected drift** is an automatic human-gate event.

```jsonc
ProtectedSurface     { file_id, baseline_hash, partition:EVOLVABLE|IMMUTABLE, fingerprint, last_verified }
GovernanceEditAttempt{ agent_did, target_file, partition, auto_escalated_to_class, falsifier_required:bool }
CorrigibilityProbe   { probe_id, result:PASS|FAIL, timestamp, signed }
```

---

### 6. Honesty as a floor tier — split honestly into bright-line and detected

The headline novelty — **honesty as an *enforced* constitutional invariant** — must be stated precisely, because most of T3 *cannot* be a Cedar bright-line. "No rung-1 pattern presented as rung-3 explanation" and "over-asserting under genuine uncertainty is a floor violation" are semantic judgments requiring a model to adjudicate intent and calibration. Listing them as deterministic floor rules would overstate enforceability and break the "deterministic floor" framing. We therefore **re-tier honesty into two enforcement classes** and label each truthfully.

| Honesty obligation | Enforcement | Mechanism |
|---|---|---|
| `(iterated)` tag present **with no maker-checker record** in the audit log | **Bright-line FAIL** (deterministic) | structural check against the audit fabric |
| Evidence-required factual claim **with no source-claim evidence pair** in the worker-output envelope | **Bright-line FAIL** (deterministic) | structural envelope check |
| `rung-3` (structural-causal) tag **with no causal-model artifact attached** | **Bright-line FAIL** (deterministic) | structural artifact check |
| `(iterated)` / role-tag self-report contradicting the recorded maker-checker posture | **Bright-line FAIL** (deterministic) | audit-vs-envelope diff |
| **Over-assertion under genuine uncertainty** (rung-1 *content* dressed as rung-3 *reasoning*) | **Detected-and-escalated** (probabilistic) | `ETHICS_REVIEW` + the anekantavada/non-absolutism lens (§9) |

So: the **structural** sub-cases are genuine bright-lines; the **semantic** core is *mechanically detected and escalated*, **not** deterministically enforced. We say this plainly rather than market a determinism the semantic judge does not have. An agent that defeats the honesty-judge can still slip rung-1-as-rung-3 past the *semantic* layer — which is exactly why honesty is enforced in **defense-in-depth** (structural bright-lines + the anekantavada lens + the tamper-evident audit's recurrence metrics), not by a single judge. The reasoning-tag discipline mirrors the operating context's own Pearl-rung convention (rung-1 associative / rung-2 interventional / rung-3 structural-causal): the diagnostic purpose is that AI's central failure mode is rung-1 patterns presented as rung-3 explanations, and **naming the rung is honesty**.

---

### 7. Gate-Loosening Ratchet (GLR) — corrigibility-preserving asymmetric mutation cost

The swarm must be able to evolve its own rules **without optimizing away its own safety** under convenience/performance pressure. Capability-threshold commitments empirically decay under convenience pressure unless mechanically ratcheted. The GLR makes the **cheap direction always the safe direction**.

| Direction | Cost | Examples |
|---|---|---|
| **TIGHTEN** | **Class A / append-only / immediate** — no human approval | raise a risk class, add a review hop, narrow an allowlist, lower a confidence-escalation threshold |
| **LOOSEN** | **Falsifier-gated + human ratification** | lower a risk class, remove a review hop, widen an allowlist, raise an autonomy ceiling |

A `LOOSEN` is rejected unless it carries **all** of: a **named** human decision-maker, a **date**, a **written falsification criterion** (the observable condition under which the loosening is reverted), and an **armed rollback archive ref**; plus it must pass the current **SafetyBattery** and be ratified at Class C/D.

```
1. Agent / meta-loop proposes a GateChange.
2. TIGHTEN ⇒ accept Class A, append to PolicyBundle immediately, log. Effective now.
3. LOOSEN ⇒ require {named_decision_maker, decision_date, falsifier_criterion,
        rollback_archive_ref}; missing any ⇒ REJECT.
4. Run the CURRENT SafetyBattery against the post-loosening config.
        Any safety regression ⇒ REJECT regardless of capability gain.  ← the "Endure" law
5. Auto-escalate to Class C/D human ratification (loosening is governance-touching).
6. On ratification: register the falsifier as a standing tripwire.
7. If the falsifier is later observed ⇒ SAFE-STATE re-tighten (§7.1), not blind restore.
8. Append the full record (incl. falsifier) to audit; this record is IMMUTABLE.
```

**Safety is a selection term, immutably** — *the "Endure" law:* **no capability gain may regress the safety battery.** A reconciliation window prevents over-triggering on benign edits. **The ratchet is itself in the IMMUTABLE partition** — an agent cannot loosen the ratchet.

```jsonc
GateChange  { change_id, direction:TIGHTEN|LOOSEN, target_gate, old_value, new_value,
              // LOOSEN-only, validated-or-rejected:
              named_decision_maker, decision_date, falsifier_criterion,
              rollback_archive_ref, human_ratification_audit_id }
SafetyBattery { battery_version, test_set[], last_pass_hash }
```

#### 7.1 Auto-revert must be safe-by-construction, not blindly restorative

The red-team correctly flagged that "auto-revert via the rollback archive" is, by our own blast-radius rule, a **governance mutation** — yet it would execute automatically at trigger time, and restoring an *arbitrary* prior `PolicyBundle` can re-introduce a previously-patched vulnerability or drop invariants added since the loosening. We therefore split rollback into two:

| Action | Cost | Safety property |
|---|---|---|
| **Tighten to known-safe conservative posture** | **free, immediate** | always Class-A-safe (more restraint is never a floor regression) |
| **Restore an arbitrary prior PolicyBundle** | **gated** | must pass the *current* SafetyBattery **and** a fast human-notification gate |

On a falsifier trigger, the default is **tighten to the safe posture** (immediate, corrigibility-preserving). Restoring a specific archived bundle is a *separate, gated, safety-verified* act. **Rollback targets are safety-verified, not merely archived.**

#### 7.2 Battery edits are a third ratchet category (closing the lateral-edit gap)

A binary TIGHTEN/LOOSEN classification misses **lateral** edits — a change that *adds a gameable test* or *narrows real coverage* while framed as "refactoring" may classify as neither and slip the ratchet. So:

- **Battery edits are a third ratchet category** requiring proof of **non-decreasing coverage**: the new battery must still **FAIL every historical violation the old battery caught** (an append-only red-team corpus as a meta-test). Coverage cannot silently shrink.
- The **battery-runner is a named, isolated, non-proposing role** — under the health subsystem (Narasimha), with results written by Chitragupta. **The proposing agent never runs its own gate.**

**Honest limitation:** a sufficiently capable swarm gaming an *evolving* battery is a genuine regress (the battery itself evolves under the ratchet). The coverage-monotonicity meta-test raises the bar; it does not prove the bar is high enough (§11).

---

### 8. Graceful-Degradation Controller — when the human is the bottleneck (and not a self-DoS)

The always-on directive forces us to define the safe default for every class when escalations exceed human review capacity — a gap the surveyed literature leaves explicitly undefined. The naive design ("fail-closed C/D + queue-overflow raises caution") is a **positive-feedback availability-collapse**: lowering autonomy reclassifies more actions up into C/D, deepening the queue, raising more caution — a cascade to total halt that an adversary (or mere load) can trigger as a denial-of-service, while the directive demands *continuous* operation.

We keep fail-safe asymmetry **but install a liveness floor and break the feedback loop**:

| Class | Degradation mode | Rationale |
|---|---|---|
| **A** | `CONTINUE_QUEUE` (post-hoc backlog) | reversible ⇒ availability preserved; audit captures everything |
| **B** | `FAIL_CLOSED_HOLD` (timelock simply does not auto-execute while veto-body unreachable) | the proposal *waits* rather than auto-passing unreviewed; absence of a watcher ≠ approval |
| **C / D** | `FAIL_CLOSED_HALT` | no execution without the explicit/per-action gate; **convenience and urgency are explicitly not factors** |

**Loop-breaking and liveness floor (the fix):**

- **A guaranteed-available lane for Class-A reversible work** is preserved even under overflow.
- **Caution-raising is rate-limited and capped** (bounded escalation depth) and **must not reclassify in-flight reversible work upward** — that was the amplifier.
- Distinguish **"human absent"** (hold) from **"human overloaded"** (shed low-salience escalations to a longer-horizon batch; do not re-gate everything).
- On queue overflow the controller **raises caution** (lower autonomy ceilings, raise monitoring intensity) **rather than draining the queue by auto-approving** — **degrade toward less action, never toward more.**

**Anti-rubber-stamp / alert-fatigue mitigations:** escalations are **de-duplicated and salience-ranked** (most consequential first); low-value escalations **batched**; a **recurrence-of-fault metric** flags box-ticking; the Class-B veto-body must periodically **prove liveness** (active attestation) or the action `FAIL_CLOSED_HOLD`s rather than auto-executing, defeating rubber-stamp-by-inattention.

**Honest framing:** fail-closed Class-C/D trades availability for safety. We accept this as a **bounded** cost (liveness floor + capped caution + a guaranteed Class-A lane), not an unbounded one.

```jsonc
DegradationPolicy { class, mode: CONTINUE_QUEUE|FAIL_CLOSED_HOLD|FAIL_CLOSED_HALT,
                    queue_overflow_action: RAISE_CAUTION_RATELIMITED }
EscalationQueue   { tickets[], salience_order, dedup_key, backlog_depth, overflow_threshold,
                    guaranteed_classA_lane: true, caution_depth_cap }
```

---

### 9. Stratum 2 — the Pluralist Ethics Runtime (PER): contested values above the floor

The deterministic floor deliberately does **not** adjudicate contested values. Those are resolved by **fair procedure**, not by imposing one moral theory or averaging theories into a false consensus. The AIES-2025 aggregation-impossibility result is explicit: **you cannot weight-average moral theories** (naive weighting inherits Arrow/voting pathologies), which is exactly why a lexicographic floor sits beneath a deliberative layer.

On any action the floor-PDP marks `ETHICS_REVIEW`, the PER fans out to **N genuinely-differentiated evaluator lenses**, each scoring the *same* scenario and returning a verdict + rationale + confidence, factored by the Agent-Deed-Consequence model:

| Lens | ADC axis | What it asks |
|---|---|---|
| **Virtue** | Agent | Does this express honesty/care/practical-wisdom *adverbially* ("promote x x-ingly") — not as a utility vector? |
| **Deontological** | Deed | Does it violate a duty, right, or constraint? |
| **Consequentialist** | Consequence | **Welfare-conditioned** outcome estimate — welfare of principal/affected parties, **never bare agreement/consensus** |
| **Care** | (relational) | Relational obligations; the vulnerable party |
| **Anekantavada / non-absolutism** | (epistemic) | Is any single lens over-asserting under genuine uncertainty? (epistemic-humility check coupled to non-harm — this is also where the *semantic* honesty sub-cases of §6 land) |

**Outputs are NOT weight-averaged.** An `UncertaintyTracker` computes cross-framework disagreement (normalized verdict-variance + sign-disagreement count):

```
disagreement < theta_low   → PROCEED (lenses concur); record concurring rationale; return ALLOW.
disagreement > theta_high  → ESCALATE to a human as a genuine moral-disagreement signal.
                              The action HOLDS. It is NOT auto-resolved, NOT averaged.
                              Transparency UI shows which lenses support/oppose and why.
between                    → apply ONLY floor-derived tie-break guards
                              ("avoid severe harm", "respect autonomy"); if still ambiguous, escalate.
```

Meta-rules apply only as **tie-break guards drawn from the floor**, never as a cardinal weighting. A `DisagreementReport` is emitted to the audit fabric **regardless of outcome** — the disagreement itself is durable evidence.

```jsonc
EthicsReviewRequest { scenario, affected_parties[], floor_verdict, trust_label }
LensVerdict         { lens, verdict: PERMIT|OPPOSE|ABSTAIN, confidence, rationale, adc_axis }
DisagreementReport  { variance, sign_disagreement_count, supporting_lenses[], opposing_lenses[],
                      decision: PROCEED|ESCALATE, escalation_reason }
```

#### 9.1 The PER is itself a swarm that can collude — bring anti-collusion *inside* it

This is the subsystem's sharpest internal tension, and the red-team is right to press it. The architecture's own central insight is **cooperation == collusion (same mechanism)**: shadow-of-the-future + reciprocity + reputation produce cooperation *and* cartels and steganographic coordinated agreement. N reputation-weighted evaluators interacting across runs are *exactly* that substrate. A naive "groupthink alarm" that fires only when outputs are **routinely identical** does **not** catch sophisticated collusion — the whole point of steganographic collusion is **coordinated *non-identical*** verdicts. And the chokepoint's anti-collusion canonicalization is applied to `GateRequest` args, **not** to the inter-evaluator channel where this collusion would actually live.

Fixes, all bringing the standing anti-collusion detector **inside** the PER:

1. **Hard isolation, not convention.** Each evaluator verdicts **before seeing any peer's** verdict or concurrence (checker-before-concurrence as a *hard* isolation). There is **no inter-evaluator channel** at verdict time.
2. **Cross-run mutual-information collusion detection** over evaluator verdict *streams* (the Audit-the-Whisper family: cross-run MI estimation, permutation-invariance under role re-ordering, welfare-shift guard, with family-wise error control) — **not** a sameness alarm. Active capacity-reducing interventions (role permutation, selective paraphrase, token-budget jitter) impose quantifiable channel-capacity penalties that tighten detection.
3. **Never reward bare agreement.** Evaluators are **not** reputation-weighted on agreement with the eventual human decision (that breeds sycophantic convergence). Either welfare-condition the evaluator reward or **do not reward evaluators on outcome-agreement at all.**
4. **Genuine differentiation, measured.** Lenses use different prompts/decompositions and, where available, **different base models**, to avoid "costumed" theory-modules whose "disagreement" is merely correlated training-bias noise.

**Honest limitation:** evaluator **collusion** *and* evaluator **differentiation** are both open problems. If the N lenses share a base model, their disagreement may be correlated-error noise and the escalation signal miscalibrated; sophisticated adaptive stego can still evade the MI detectors (recall is imperfect). Both are listed in §11.

---

### 10. Capability-Rollout Sequencer (astanga: restraint before capability) + audit ordering

#### 10.1 Restraint-before-capability as an enforced ordering

The precise alignment failure governance exists to prevent is building integrative ("samadhi-grade") capability **before** the matching restraint ("yama-grade") is live and verified. Every proposed new capability (new role, new tool grant, new autonomy level, new external-effect verb) must, **before activation**, **name the constraint it relaxes** and produce evidence that the matching restraint is **already live and verified**.

```
1. Capability proposal declares relaxes_constraint and required_restraints[].
2. Sequencer resolves each restraint against the live system:
       floor rule present? audit hook wired? identity/VC issued? monitor configured? rollback armed?
3. All GREEN ⇒ permit activation; record which constraint this relaxes.
4. Any PENDING/MISSING ⇒ QUEUE the capability (NOT denied) — it activates when the restraint lands & verifies.
5. Capability runs a CLOSED/untrusted model ⇒ raise required monitoring intensity AND
       lower its autonomy ceiling BEFORE activation (closed ⇒ more-untrusted ⇒ higher restraint bar).
6. Log the activation (or queueing) with the restraint evidence to the audit fabric.
```

This composes with the GLR (a new capability that *also* loosens a gate triggers both checks) and with closed-model handling (an untrusted model raises the restraint bar before its capabilities activate).

```jsonc
CapabilityRollout { capability_id, relaxes_constraint, required_restraints[],
                    restraint_status: GREEN|PENDING|MISSING, activation_state: QUEUED|ACTIVE|BLOCKED }
RestraintNode     { restraint_id, kind: FLOOR_RULE|AUDIT_HOOK|IDENTITY|MONITOR|ROLLBACK,
                    verified:bool, verified_by, verified_at }
```

#### 10.2 Audit entry as a state machine (fixing the ETHICS_REVIEW re-entry ambiguity)

The "log the verdict **before** the tool executes" rule and the mid-evaluation PER call-out otherwise leave an under-specified state: an action could be logged `ALLOW`-pending while a human escalation is open. We make the audit entry an **explicit state machine** and gate the tool-forward strictly on a terminal, non-escalated state:

```
PENDING_ETHICS ──► ALLOW ──────► (forward to tool)
        │     └──► DENY
        │     └──► ESCALATED ──► (HOLD; no external effect while OPEN) ──► HUMAN_RESOLVED ─► ALLOW|DENY
        └──────────► HELD
```

**No external effect fires while any ethics escalation is OPEN.** The full state transition is logged, not a single pre-decision verdict.

---

### 11. Separation of powers, identity, and the residual single points (no overstatement)

Three powers with **cryptographically-distinct authority** (keys held outside any agent's controllable surface — TEE/HSM/SPIRE-style — via the identity layer, **Kaal-Bhairav**):

| Power | Holder | Can | Cannot |
|---|---|---|---|
| **Legislative** | humans + immutable PolicyBundle | produce law; sign PolicyBundle versions | execute work |
| **Executive** | worker agents (Brahma, Vishwakarma, Varuna…) | choose *what* work; set operational params | alter the law they are judged under |
| **Judicial** | **Yama** + escalation pipeline | adjudicate floor; run/route the PER | initiate work; legislate |
| **Halt** | **Vishnu** (continuity-guardian) | HALT a Class-B+ continuity-FAIL change | unpause; initiate; trap participants |
| **Audit-write** | **Chitragupta** (exclusive writer, scope outside every monitored agent) | append signed entries | act as executive/judicial |

The mapping `{only Yama issues FAIL; only Chitragupta writes audit; only Vishnu halts; only the legislative key signs PolicyBundle}` is enforced by **signature verification at each chokepoint, not by convention**. Authority is **competence-/role-bound, never capital-weighted** — the staking→reward-capture pattern of token-weighted agent economies is the explicit antipattern; there is **no coin and no staking substrate**. The split is **fractal**: the same legislative/executive/judicial structure applies identically at agent / clan / division / whole-swarm levels (group-Markov-blanket composition), giving nested polycentric governance — autonomous *within* the floor, governed identically at every scale.

#### 11.1 We do NOT claim "no SPOF." We name the residuals and reduce each.

"Fractal replication" does **not** dissolve single points: a fractal of single-writer-audit is, per level, still a single writer. We separate **availability-SPOF** from **compromise-SPOF**:

| Single point | Type | Mitigation | Residual (honest) |
|---|---|---|---|
| **Yama PDP** on every critical path | availability | replicate as **stateless instances behind crash-fault-tolerant (Raft) replication** with PolicyBundle-hash agreement — cheap, since the PDP is agent-stateless | a correlated bug in the policy engine still affects all replicas |
| **Chitragupta** exclusive audit-writer | compromise + availability | a **small rotating quorum of attested witnesses with threshold cosigning** + periodic **external root anchoring** (transparency-log / split-view defense) | **single-operator witness-set honesty is unsolved** |
| **Legislative signing key** | compromise | off-agent custody (HSM/TEE), rotation policy | key custody remains a trusted root |

`PowerGrant { power: LEGISLATIVE|EXECUTIVE|JUDICIAL|HALT|AUDIT_WRITE, holder_did, capability_VCs[], scope, rotation_policy }`. **The claim is "SPOF reduced," not "eliminated."**

---

### 12. Failure modes addressed (and how)

| Failure mode | How this subsystem addresses it |
|---|---|
| Constitution-drift / in-context scheming / alignment-faking | Floor enforced as deterministic policy-as-code **outside** the agent (Cedar/OPA at the chokepoint); rules not agent-rewritable (immutable partition + blast-radius auto-escalation). |
| **Classifier-routing capture** (primary residual risk) | Router treated as an **untrusted monitor**: fail-up default, near-boundary resampling + defer-to-conservative, continuous classifier red-teaming → new bright-lines, under-classification as a tracked vital sign (§2). *Reduced, not closed.* |
| **Agent-supplied context manipulation** | Context predicates **orchestrator-computed from observable structure**, worst-case over-estimate when heuristic, estimates from the requesting agent **refused** (§3). |
| Safety erosion under self-evolution (misevolution) | GLR: tightening free / loosening falsifier-gated; **Endure law** (no capability gain may regress the battery); capability-rollout sequencing keeps restraint ahead of capability (§7, §10). |
| Averaging-away genuine moral disagreement | Lexicographic floor for bright lines + PER that **never weight-averages**; disagreement escalated as a first-class signal (§9). |
| Honesty failures / hype / hallucination-as-explanation | Structural honesty sub-cases are **bright-line FAILs**; semantic over-assertion **detected-and-escalated** via the anekantavada lens + audit recurrence metrics — stated honestly as detection, not enforcement (§6). |
| **Evaluator collusion inside the PER** | Hard isolation at verdict time; cross-run MI collusion detection (not a sameness alarm); no outcome-agreement reward; measured lens differentiation (§9.1). *Open problem flagged.* |
| **Availability-collapse / self-DoS** | Liveness floor + guaranteed Class-A lane + rate-limited/capped caution that does not re-gate in-flight reversible work (§8). |
| **Unsafe auto-rollback** | Falsifier trigger ⇒ **tighten to safe posture** (free); arbitrary restore is **gated + battery-verified** (§7.1). |
| **SafetyBattery Goodhart via lateral edits** | Battery edits are a **third ratchet category** with coverage-monotonicity meta-test; **named non-proposing battery-runner** (§7.2). |
| Self-preservation / shutdown-resistance drift | Corrigibility is an immutable floor tier **continuously verified by probes**; self-preservation has no intrinsic value; Pause-Guardian asymmetry (§5, §11). |
| Capital-capture of authority | Competence-/role-bound cryptographic grants (DID + VC); **no staking/coin** (§11). |
| Human-reviewer bottleneck / alert fatigue / rubber-stamping | Graceful-degradation per class; de-dup + salience-rank + batch; recurrence-of-fault metric; veto-body liveness attestation (§8). |
| Convenience/urgency erosion of human gates | Class C/D non-bypassable; convenience/urgency stated non-factors; loosening routes through the ratchet + ratification (§4, §7). |
| Prompt-injection via observed content | `quarantined:*` instructions never action-grounds without out-of-band human confirmation; arg canonicalization strips injected directives + stego capacity (§1). |
| Agent lowering its own gate via a low-class governance edit | Blast-radius auto-escalation forces any governance/config/PolicyBundle edit to the top gate (§5). |
| Bypass-of-gate | Runtime contract: no executive agent reaches a tool except via the PDP; identity verification rejects any actor without a valid capability VC (§1, §13). |

---

### 13. Interfaces to the other subsystems

| Other subsystem | Contract |
|---|---|
| **Identity & Security (Kaal-Bhairav)** — DID/VC + attested short-lived certs | PDP calls identity to verify each `GateRequest`'s `agent_did` + capability VC (signed, short-lived, auto-rotating; keys off the model-controllable surface) **before** evaluating any floor rule. The power-separation mapping is enforced by signature verification, not convention. Unsigned/expired identity ⇒ automatic **T4 DENY**. |
| **Tamper-evident Audit Fabric (Chitragupta)** — exclusive-writer hash-chained Merkle/transparency log | Every `GateVerdict`, `DisagreementReport`, `VetoWindow` transition, `GateChange` (incl. falsifier), `CorrigibilityProbe`, and escalation is a signed entry written **before** the gated action executes. The subsystem consumes **O(log n) inclusion proofs** to verify a decision was logged and to detect protected-surface drift (hash-baseline diff = automatic human-gate event). The **reparative action-class** (violation → corrective act → restored standing) turns the audit into a **correction ledger, not a punishment ledger**, so agents surface rather than conceal errors — guarded by the recurrence-of-fault metric against weaponized "disclosed-then-repaired" laundering. |
| **Meta-evolution loop + Archive** — the self-adaptation engine | This subsystem is the gate every PROPOSE→EVALUATE→SELECT cycle must pass: cheap reversible per-interaction learning = Class-A post-hoc; structural change = maker-checker Class-B; persistent/governance change = top-gate + SafetyBattery + ratification + armed archive rollback. Safety is supplied as a **mandatory selection term** (Endure law). The Archive supplies the **safety-verified** one-click rollback substrate (§7.1) the ratchet and degradation controller depend on. The evolvable/immutable boundary tells the loop which params it may mutate. |
| **Swarm immune system (Narasimha) + anti-collusion layer** | The Risk-Class Gate Router exposes the confidence/uncertainty-escalation hook the health agents fire on (anomaly, vital-sign breach). The PER's `UncertaintyTracker` + the collusion detectors feed the health layer's **diversity-floor** and **disagreement-rate** vital signs; **systematic under-classification** is a health vital sign reconciled against ground-truth (§2). The anti-collusion detector receives canonicalized inter-agent messages from the chokepoint (channel-capacity reduction) **and now also runs inside the PER** (§9.1); it can raise an agent's monitoring intensity / lower its autonomy class via the gate router. Narasimha is the **named, non-proposing SafetyBattery-runner** (§7.2). Vishnu's halt and the health agents' halt-and-rollback are coordinated through the Pause-Guardian asymmetry. |
| **Coordination substrate (GWT / predictive-coding sparse async bus) + MCP/A2A** | `GateRequest`/`GateVerdict`, `EthicsReviewRequest`, `EscalationTicket`, and `VetoWindow` events ride the **salience-gated async bus as surprise/error-deltas** (not all-to-all flood). The PDP sits as the deterministic decision point in front of **every MCP tool-call** (agent→tool chokepoint) and **every A2A task-lifecycle transition with an external effect**; Agent Cards carry the capability VCs the identity layer issues. The subsystem is **vendor/model-neutral by construction** — the verdict depends only on PolicyBundle + request context + identity, never on any model's internals. |

---

### 14. Honest novelty accounting

**None of the individual mechanisms is invented here.** Cedar/OPA policy-as-code at the tool chokepoint, the legislative/executive/judicial split, optimistic-veto + timelock dual governance, the Compound Pause-Guardian asymmetry, lexicographic floors over a pluralist layer, Constitutional/Collective-Constitutional principle sourcing, the gate-loosening ratchet, the honesty-tag primitives, the reparative action-class, and the trust-label taxonomy all exist in the surveyed 2024–2026 work (and the local governance corpus). The pluralist runtime is closer to a **faithful re-implementation of the Agent-Deed-Consequence / Normative-Moral-Pluralism framework** — which already pairs parallel theory-modules with an uncertainty tracker that flags high-disagreement decisions for human escalation — than to a novel mechanism.

The SOTA-advancing contribution is their **integration into one coherent constitutional cell** with four properties **no surveyed system combines**:

1. **Disagreement-driven escalation correctly operationalizing the aggregation-impossibility result** — a deterministic lexicographic floor for bright lines *and* a pluralist runtime above it where cross-framework disagreement is a first-class human-escalation signal rather than a weighted average. The honest claim is **"first integration of ADC-style disagreement-escalation *into* a deterministic-floor + ratchet + audit cell,"** not novelty of the disagreement-escalation idea itself.
2. **A gate-loosening ratchet fused with capability-rollout sequencing and an immutable safety-selection-term** — mechanically-enforced "restraint-before-capability, tightening-free / loosening-falsifiable," making safety-erosion-under-self-evolution **structurally hard** rather than hoped-against. The surveyed self-evolution systems have *no governance ratchet at all*.
3. **Honesty wired to the floor** — structural sub-cases as bright-line FAILs, semantic over-assertion as detected-and-escalated, audited via the tamper-evident layer. The honest framing is **"mechanically *detected*-and-escalated,"** not "deterministically *enforced*" — the semantic core is model-adjudicated, and we say so.
4. **An explicit graceful-degradation-when-human-is-bottleneck policy per risk class** (fail-closed vs fail-open, with a liveness floor and caution that degrades toward *less* action) — a gap the surveyed literature leaves undefined and the always-on directive forces us to close.

The integration is **vendor/model-neutral by construction** and **fractal** (the same structure at agent/clan/division/swarm scale). **The contribution is the coherent whole, not any part.**

---

### 15. Open problems (load-bearing and unresolved)

1. **Classifier-routing capture (primary).** Deterministic gates handle bright-line floor violations, but the routing judgment that *feeds* them is probabilistic. The fail-up / resample / red-team-into-bright-lines protocol (§2) reduces the surface to the classifier's residual error rate; it does not eliminate it. This is the architecture's **single largest residual safety hole.**
2. **Escalation-threshold calibration.** `theta_low`/`theta_high` are the load-bearing parameters and are **uncalibrated** off the shelf. Set them wrong and you either over-gate (killing autonomy) or silently auto-resolve genuine moral disagreement. No principled calibration method exists.
3. **Policy analyzability under composition.** Cedar proves single-rule properties, but proving that a *large composed* set (Cedar bright-lines + Rego predicates + per-class bindings, evolving under the ratchet) never permits a forbidden action under all compositions is an open formal-methods problem. **A bypass anywhere = no protection.**
4. **SafetyBattery Goodhart / regress.** A sufficiently capable evolving swarm can game any fixed battery; the battery itself evolves under the ratchet, creating a regress. The coverage-monotonicity meta-test (§7.2) raises the bar without proving it sufficient.
5. **Genuine evaluator differentiation AND evaluator collusion (PER).** If the N lenses share a base model, "disagreement" is correlated-error noise and the escalation signal is miscalibrated. Separately, the lenses are a swarm subject to cooperation==collusion; coordinated-but-non-identical verdicts can manufacture false concurrence. Cross-run MI detection + hard isolation + measured differentiation (§9.1) mitigate; neither is solved, and adaptive stego can still evade.
6. **LLM confidence miscalibration corrupts the confidence-escalation hook.** The ~10–15% target assumes usable confidence; self-reported confidence is poorly calibrated and gameable. Continuous monitoring against ground-truth is required; weighting any gate on a corruptible self-report is a standing risk.
7. **Legitimacy of the floor's content ("whose values").** The floor must be procedurally legitimate (deliberation-sourced, not author-fiat) and non-agent-rewritable, but a single-operator swarm has no built-in deliberative public; overlapping consensus can be thin. How to source and periodically re-legitimate the floor's contested edges without ossifying or drifting is unresolved.
8. **Timelock latency vs urgency.** Class-B optimistic-veto adds a fixed timelock to every governed action, and fail-closed C/D trades availability for safety. Durations and degradation defaults are currently **blast-radius-heuristic, not derived**; there is no principled method that is simultaneously safe and not operationally crippling under load. (Mitigation: keep most routine evolution Class-A reversible so Class-B timelocks are rare.)
9. **Single-operator witness-set honesty (audit SPOF).** Witness cosigning mitigates the audit compromise-SPOF only if the witness set is honest; for a single operator, witness-set governance (who/how chosen/rotated/incentivized) is **unsolved**. "Who audits the auditor" is *reduced*, not closed.
10. **Reparative-class abuse.** The correction-ledger makes error-disclosure safe, but a strategic agent could launder repeated violations as "disclosed-then-repaired." A recurrence-of-fault metric is specified; its threshold and gaming-resistance are not solved.
