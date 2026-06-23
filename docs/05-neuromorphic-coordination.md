# The Mandala — Neuromorphic Coordination Substrate

> *Indra's Net is a net of jewels in which every jewel reflects every other. The Mandala is the wiring of that reflection: how a signal in one node becomes — or fails to become — a signal in all the others.*

## 1. What this subsystem is, and what it is not

The Neuromorphic Coordination Substrate is Indra's Net's **nervous system**: the transport-and-attention layer over which every other subsystem rides. The governance floor (Yama), the tamper-evident audit fabric (Chitragupta), the evolution loop and Archive (Brahma/Saraswati), the anti-collusion detector, and the health/immune system all communicate *through* the Mandala. It is the only layer every other subsystem touches directly.

It is built from a deliberate mapping of neuroscience onto distributed-systems engineering:

| Neuroscience | Indra's Net | Engineering realization |
|---|---|---|
| Neuron | Agent | Actor with a durable mailbox |
| Spike | Typed message | Content-addressed event (CID) on an event bus |
| Synapse / synaptic weight | Trust-edge `w(A→B)` | Sparse adjacency row, plastic |
| Salience-gated workspace | Attention bus | Sharded, capacity-limited broadcast |
| Prediction error / surprise | Coordination signal | KL-proxy salience score |
| Homeostasis / neuromodulation | Health regulation | PI controllers + global hormone vector |
| Stigmergy (pheromone) | Shared trace field | Decaying content-addressable store |

**This is a set of architectural *patterns* borrowed from neuroscience — not a literal brain.** We state this plainly because the field is full of neuromorphic hype, and overclaiming would itself violate the honesty floor:

- **NOT spiking silicon.** Neuromorphic hardware (Loihi-class, SpiNNaker-class) gives real energy wins only on sparse event workloads and is irrelevant to a vendor-neutral, self-hostable *software* swarm. We adopt the principles, not the chips.
- **NOT millisecond timing.** "Spikes" are events on an async bus, not time-coded action potentials. There is no global clock and no biological time constant.
- **NOT literal variational inference.** "Surprise" and "expected free energy" are *scoring/routing heuristics* (embedding distance, log-prob deltas, or a cheap judge), not tractable free-energy minimization. The heavy variational machinery is explicitly out of scope.

Everything below is engineered on top of those honest limits.

### 1.1 The five coupled mechanisms

```
                          ┌─────────────────────────────────────────────┐
                          │   ACTIVE-INFERENCE / EFE FRAMING (heuristic) │
                          │   surprise = the gradient the swarm descends │
                          └───────────────────┬─────────────────────────┘
                                              │ (conceptual unifier)
   ┌──────────────┐   ┌───────────────────────┴──────────┐   ┌──────────────────┐
   │ (1) SHARDED  │   │ (2) PREDICTIVE-CODING DISCIPLINE  │   │ (3) EVENT-DRIVEN │
   │ SALIENCE-    │◄──┤ publish only surprise deltas,     ├──►│ ASYNC ACTOR      │
   │ GATED        │   │ not full state (collapses flood)  │   │ RUNTIME (no tick)│
   │ WORKSPACE    │   └──────────────────────────────────┘   └──────────────────┘
   │ (GWT)        │                                                    ▲
   └──────┬───────┘   ┌──────────────────────────────────┐            │
          │           │ (4) PLASTIC TRUST EDGES (Hebbian/ │            │
          └──────────►│ STDP, three-factor, fail-safe-    ├────────────┘
                      │ asymmetric, welfare-conditioned)  │
                      └──────────────────────────────────┘
   ┌─────────────────────────────────────────────────────────────────┐
   │ (5) HOMEOSTASIS & NEUROMODULATION — network-level vital-sign      │
   │ regulation, paired inhibition/stimulation, slew limits, clamp.    │
   │ Out-of-band trusted controller. Bounded by the diversity floor.   │
   └─────────────────────────────────────────────────────────────────┘
   ┌─────────────────────────────────────────────────────────────────┐
   │ STIGMERGIC SHARED-TRACE LAYER — decaying pheromone field,         │
   │ strictly ON TOP OF mandatory per-agent memory, never instead.     │
   └─────────────────────────────────────────────────────────────────┘
```

The integration claim — and the honest scope of it — is treated explicitly in §9 (Novelty). In short: a **common family of surprise-derived heuristics** drives messaging, attention, trust, adaptation, and health. We are careful *not* to call this "a single quantity": operationally these are distinct, separately-calibrated estimators that share a conceptual root, not one shared scalar with guarantees (see §9.1).

---

## 2. The Spike Bus — event-driven async actor runtime

### 2.1 Purpose

Agents stay **dormant** until a relevant typed event (a "spike") arrives. No global tick; mesh-routed; fault-isolated horizontal scale. This is the substrate's axonal wiring — production-validated event-driven async actor runtimes cut latency 70–90% versus polling. It is vendor-neutral by construction: any actor runtime over any async event bus (a durable log such as Kafka/Pulsar/NATS-JetStream-class for large deployments, or an in-process actor mailbox for small ones) can host it.

### 2.2 The spike envelope

Every message is content-addressed (`spike_id = CID = hash(canonical_payload)`) so deduplication, provenance, and the audit fabric share **one identifier**.

```jsonc
Spike {
  spike_id:        CID,          // content hash of canonical payload
  kind:            enum {        // determines routing + priority class
                     PREDICTION_ERROR, IGNITION_CANDIDATE, BROADCAST,
                     TRUST_DELTA, NEUROMOD, STIGMERGY_DEPOSIT,
                     STIGMERGY_NEGATIVE, HEALTH_VITAL, GOV_FAIL, GOV_HALT,
                     NULL },
  src_did:         DID,          // cryptographic sender identity (§8)
  role:            string,       // mythic role + functional gloss
  shard_id:        string,
  ts:              uint64,
  ttl:             uint32,
  causal_parents:  [CID],        // lineage for the audit hash-chain
  precision:       Quantized,    // confidence — QUANTIZED, see §3.3
  salience:        Quantized,    // attention bid — QUANTIZED, see §3.3
  payload:         bytes,
  payload_schema:  SchemaID,
  trust_label:     enum {        // trusted:audited | quarantined:* | ...
                     trusted_audited, trusted_unverified,
                     quarantined_observed, quarantined_external },
  sig:             Signature     // short-lived attested cert over the envelope
}
```

```jsonc
AgentActorState {
  did, role,
  inbox_cursor,          // durable offset; survives respawn (replay unprocessed)
  generative_model_ref,  // cheap predictor of neighbours' outputs (§3, §7)
  trust_row_ref,         // sparse outgoing trust adjacency (§5)
  mailbox_depth,
  priority_inbox_cursor  // SEPARATE reserved lane — see §2.4
}
```

### 2.3 Topic families

```
spine.shard.{k}      one per workspace shard (clan-local coordination)
neuromod.global      hormone-vector broadcasts (§6)
stigmergy.{field}    decaying shared-trace fields (§7-stig)
audit.tap            READ-ONLY mirror tee'd to Chitragupta (write-once, never by us)
priority.lane        reserved, never-overflowed lane for GOV_*/HEALTH_VITAL>=high
```

### 2.4 Delivery, backpressure, and the priority-lane fix (resolves a major flaw)

- **At-least-once delivery with idempotency keys.** A respawned agent replays unprocessed spikes from its durable `inbox_cursor`.
- **Content + topic routing, never all-to-all.** All-to-all flood is the top inter-agent failure class (~32% of multi-agent failures in the MAST taxonomy); §3 collapses it at the source.
- **Bounded mailboxes with backpressure** for *non-priority* kinds only. On overflow, a non-priority spike is **demoted to the stigmergy layer** (a decaying trace) rather than silently dropped.

> **Red-team fix — the backpressure black-hole (was: major / safety risk).** The earlier design demoted *any* overflowed spike to a decaying field — but demotion into a field that evaporates before it is read **is a silent drop with extra steps**, and the priority lane (which lived at the *workspace-competition* layer) could not protect against it, because overflow happens earlier, at the *transport/mailbox* layer. Under sustained overload — exactly when the swarm is stressed and safety signals matter most — a `HEALTH_VITAL` or `GOV_HALT` could evaporate.
>
> **Resolution.** Floor-eligible kinds (`GOV_FAIL`, `GOV_HALT`) and `HEALTH_VITAL` with `severity >= high` ride a **reserved, never-overflowed priority mailbox lane end-to-end** (`priority.lane` + per-agent `priority_inbox_cursor`). Bounded mailboxes and backpressure-to-stigmergy apply **only** to non-priority kinds. Under sustained overload the correct response is to **shed low-salience load** (raise `theta_fire`, apply an inhibitory clamp — §6) while *guaranteeing* priority-lane delivery — never to demote a safety vital into a decaying field. And: **"a HEALTH_VITAL or governance spike was demoted to stigmergy" is itself a high-severity health alarm.** The priority lane and the load-shedding clamp are now co-located at the same (transport) layer, closing the layering gap.

---

## 3. Salience Scorer — the per-agent afferent gate

### 3.1 Purpose

Decide whether an agent should fire *at all*, and how loudly. This implements the predictive-coding discipline — **"stay silent unless surprised"** — and is the primary defense against message flood. Routine, predicted state generates near-zero traffic.

### 3.2 Mechanism

Each agent maintains a lightweight **generative model** of its neighbours/parents (what it *expects* to see). On a candidate output it computes:

```
surprise        ≈ KL(observed ‖ predicted)            // cheap proxy, see below
salience        = w_nov·novelty
                + w_goal·goal_relevance(top-down query from workspace)
                + w_evid·evidence_quality
                + w_urg·urgency                         // all in [0,1]
```

If `salience < theta_fire` (default `0.35`, hormone-modulated) the agent emits a **NULL spike** (principled silence) and stops. The weights `w_*` and `theta_fire` are neuromodulator-tunable (§6). **Precision** (confidence in the error itself) is published alongside salience so the workspace and the trust layer can down-weight low-confidence surprise.

The surprise proxy is registry-dispatched per modality:

```
surprise_proxy_registry: { modality → scorer_fn_id }
  text/embedding  → cosine distance to predicted-mean embedding
  token-logprob   → log-prob delta vs predicted distribution (where available)
  fallback        → trusted cheap-judge "is this novel/goal-relevant?" score
```

### 3.3 Quantize precision and salience (resolves a critical collusion flaw)

> **Red-team fix — the salience/precision covert side-channel (was: critical / safety risk).** The anti-collusion contract canonicalizes/paraphrases *payloads* to defeat steganography. But every spike *also* carried continuous-valued `precision ∈ [0,1]` and a 4-dim `salience_vec`, and ignition outcomes are publicly broadcast. Two colluding agents could encode secret bits in the **low-order bits of precision/salience**, in **timing** (which event-window they fire into), or in their **NULL-vs-fire pattern**. Streams 2 and 7 are explicit: paraphrasing-alone fails; **channel *capacity* must be limited, not just content scrubbed.** The substrate was scrubbing content while leaving a metadata + timing + null-pattern channel wide open — and it is the very channel the scorer reads to decide ignition.

**Resolution — treat precision/salience/timing/null-pattern as adversarial covert-channel surface:**

1. **Quantize** `precision` and each `salience_vec` component to a small number of buckets (3–5 levels, e.g. `{low, med, high}`) *before they leave the agent*. The `Quantized` type in the envelope is an enum, not a float, collapsing the low-order-bit channel.
2. **Jitter event-window assignment** with bounded noise (the token-budget-jitter intervention from Stream 7), so firing-into-a-chosen-window cannot reliably carry bits.
3. **Randomize NULL-pseudo-candidate framing** so silence-patterning is noisy.
4. **Feed the full metadata stream — precision, salience, timing, null-pattern, *not just payloads* — to the cross-run mutual-information collusion detector** (§8, anti-collusion interface).
5. Channel-capacity-limiting covers **all** spike fields and timing, not just payload bytes.

**Honest residual:** quantization + jitter *reduce* covert bandwidth; they do not prove it zero. Residual covert bandwidth through quantized metadata and coarse timing is a **known, documented limit** (§10), monitored statistically rather than eliminated.

### 3.4 Salience is not a self-graded exam (resolves a critical sandbagging flaw)

> **Red-team fix — sandbagging / self-suppression via the gate (was: critical / safety risk).** The whole flood-defense rests on agents **honestly** scoring their own surprise — but the model is **untrusted-by-default** per the spine. An agent could deliberately stay below `theta_fire` to (a) avoid the audit footprint (a NULL produces minimal trace), (b) coordinate by patterned silence, and (c) **sandbag** — withhold a genuinely high-surprise safety observation by self-reporting low salience. Self-reported salience for consequential signals is a self-graded exam.

**Resolution — self-scored salience is never the sole gate for consequential signals:**

1. **Independent spot-check re-scoring.** A *trusted, cheap, out-of-band monitor* re-scores a sampled fraction of suppressed/NULL outputs ("resample-to-incriminate" from Stream 7). Disagreement between self-score and monitor-score is itself a signal fed to the anti-collusion / health subsystems.
2. **NULL/silence-pattern auditing.** Per-agent NULL streams are checked for steganographic structure (periodicity, correlation with peers' fire events).
3. **Safety content cannot self-suppress.** A hard rule: candidate observations that *could be* floor-relevant or safety-relevant are routed to the **priority lane regardless of self-scored salience** — the agent does not get to gate its own safety report below `theta_fire`. (Classification of "could be safety-relevant" is conservative and itself spot-checked.)
4. **Verified withholding is a floor violation.** Demonstrated withholding of a high-surprise safety signal is penalized as an honesty-floor violation — consistent with the spine's rule that over-/under-asserting under genuine uncertainty is already a floor violation.

This re-aligns the gate with untrusted-by-default: agents *propose* their salience; a trusted layer *audits* it on a sampled basis and *overrides* it for safety kinds.

---

## 4. Sharded Salience-Gated Workspace — GWT competition / ignition / broadcast

### 4.1 Purpose

The limited-capacity **attention bus**. Among all surprising candidates, only a small winning coalition is "ignited" and broadcast, so swarm bandwidth auto-focuses on what is genuinely new and important. It is **sharded and hierarchical** so it is never a single point of failure and scales — there is no single global blackboard that is load-bearing.

### 4.2 The ignition cycle (event-triggered, not clocked)

```
        candidates (IGNITION_CANDIDATE spikes, w/ quantized salience+precision)
               │
               ▼
        ┌──────────────┐   includes a NULL pseudo-candidate
        │ COMPETITION  │   p = softmax(salience / temperature)   ← temperature is a hormone
        └──────┬───────┘   "broadcast nothing" can win
               │
        ┌──────▼───────────────────────────────────────────────┐
        │ FAIRNESS FLOORS (per-role token buckets)              │
        │  + PRIORITY LANE: GOV_FAIL/GOV_HALT and               │
        │    HEALTH_VITAL>=high BYPASS competition entirely      │
        └──────┬───────────────────────────────────────────────┘
               │  select top-K winners (K = capacity, default 5/shard)
        ┌──────▼───────┐
        │ IGNITION     │ winners enter workspace; emit BROADCAST spikes
        └──────┬───────┘ escalate blanket-summary to parent shard if cross-shard
               │
        ┌──────▼───────┐
        │ RE-ENTRY     │ subscribers update predicted-state caches
        └──────────────┘ (lowering future surprise for now-known facts)
               │
               ▼  log full ignition record to audit.tap; update VitalSigns
```

### 4.3 Fairness floors and the priority lane

A critical *minority* signal must never be permanently starved by high-salience chatter:

- **Per-role and per-shard token-bucket fairness floors** guarantee a minimum ignition rate to each role-class.
- **Priority lane:** `GOV_FAIL`, `GOV_HALT`, and `HEALTH_VITAL >= high` **bypass competition entirely** and ignite immediately and globally — fairness-floor-exempt, non-overridable. This preserves the constitutional commitment that Yama-FAIL and Vishnu-HALT cannot be pushed past.

**Honest limit:** token-bucket fairness is an *engineering patch*, not a provable guarantee that every critical minority signal eventually ignites under adversarial high-salience chatter (§10).

### 4.4 Sharding (no global SPOF)

Agents are partitioned into **clans → divisions → whole-swarm**. Each clan has a local workspace; clan workspaces feed a division workspace, which feeds a global workspace. Only **blanket (interface) summaries** propagate upward (group-Markov-blanket nesting, §7-ai). Capacity **shrinks** as you go up (more selective). Internal clan chatter never reaches the global bus.

```jsonc
WorkspaceShard {
  shard_id, parent_shard_id, capacity_K, temperature,
  fairness_buckets: { role_class → token_bucket },
  priority_lane_kinds: set,
  current_winners: [CID],
  re_entry_subscribers: [DID]
}
IgnitionRecord {                     // logged to audit.tap
  tick_id, shard_id,
  candidate_set: [{CID, salience, precision}],
  winners: [CID], null_won: bool,
  fairness_overrides: [CID], priority_bypass: [CID]
}
```

### 4.5 Safety signals fire on persistence, not novelty (resolves a coherence flaw)

> **Red-team fix — surprise-suppression vs safety-vigilance (was: minor / safety risk).** Re-entry caches lower future surprise for "already-known" facts to curb repetition loops — good for coordination, dangerous for safety. A persistent, *worsening* safety condition that is "already known" (low surprise because broadcast once) needs to keep firing. The safest-looking metric (no surprise) is indistinguishable from **normalized deviance** — a known hazard chronically tolerated.

**Resolution — decouple safety-signal firing from the surprise gate:**

- `HEALTH_VITAL` and floor-relevant kinds fire on **threshold-crossing** and on **persistence** (a condition still true after *N* ticks **re-fires with escalating severity**), *not* on novelty.
- Surprise-suppression applies to **routine coordination traffic only**, never to safety/governance kinds.
- A **normalized-deviance check**: a hazard chronically present-but-suppressed-as-known is itself raised as an alarm.

---

## 5. Plastic Trust-Edge Layer — three-factor synapses with fail-safe asymmetry

### 5.1 Purpose

Decentralized, online inter-agent trust with correct temporal credit assignment and **no central trust authority** — the swarm's synaptic learning. Trust weights bias routing, ignition salience, and aggregation weight, and feed the competence-weighted reputation subsystem. Authority here is **competence-weighted, never capital-weighted** (the stake→reward capture seen in capital-weighted designs is the antipattern this avoids).

### 5.2 The three-factor update

Edge trust `w(A→B) ∈ [w_min, w_max]` (default `[0.0, 1.0]`, init `0.5`).

```
1. LOCAL eligibility trace e(A→B) accumulates from direct interaction outcomes
   (did A verify B's output? was it used? did downstream succeed?) — purely local.
2. e(A→B) DECAYS exponentially (evaporation; default half-life ~50 interactions)
   → stale track record is continuously forgotten.
3. On a GLOBAL validation signal (verifier PASS / audit confirm / task-success
   broadcast / floor-violation FAIL), COMMIT:
        Δw = eta · e(A→B) · gate(global_signal)        // eta is a hormone
```

This is the **e-prop / diffusing-neuromodulator pattern**: a local forward eligibility trace × a single broadcast error signal solves temporal credit assignment without global backprop or a coordinator.

### 5.3 Fail-safe asymmetry — the cheap direction is the safe direction

This asymmetry is baked into the **synaptic rule itself**, not bolted on above it:

| Direction | Gate | Rate | Shape |
|---|---|---|---|
| **DEMOTION** (B did badly / B violated the floor) | **none — free, immediate** | unbounded | multiplicative (`w ← demotion_mult · w`, default `0.5`) |
| **PROMOTION** (B did well) | **gated** on the global validation factor | rate-limited per window | saturating near `w_max` |

Defensive demotion is **free**; promotion is **earned**. This mirrors the trust-label discipline (demotion-free / promotion-gated) and makes the cheap direction the safe direction at the most fundamental unit of learning.

### 5.4 Welfare-conditioning — cooperation must not become a cartel

> Cooperation and collusion are the **same mechanism** (shadow-of-the-future + reciprocity + reputation produce both). So trust gain is **welfare-conditioned**:

- Reciprocal mutual-rating between A and B that is **not corroborated by an independent welfare/verifier signal does NOT raise trust** — blocking mutual-admiration rings.
- Trust subgraphs that strengthen on **bare agreement** are fed to the standing anti-collusion detector (§8).
- A **trust-entropy floor** (§6) alarms on trust monoculture.

This is the synapse-level expression of "never reward bare consensus."

### 5.5 Stability normalization

**Synaptic scaling** renormalizes each agent's outgoing and incoming trust mass to bounds, preventing the documented runaway-potentiation (Hebbian) instability. Combined with bounded weights, eligibility decay, and saturating promotion, the edge layer cannot blow up.

### 5.6 Demotion is reparative, not merely punitive (resolves a major flaw + coherence gap)

> **Red-team fix — weaponized free-demotion + missing reparative path (was: major / safety risk).** Proximity ≠ causation (§10), and the consequences compound: (a) a sycophantic agent firing just-before-every-success harvests undeserved promotion; (b) a malicious agent can deliberately position itself temporally adjacent to validated outcomes to **farm trust**; (c) worse, because demotion is immediate/ungated/multiplicative, an attacker who can trigger a FAIL inside a victim's eligibility window can **weaponize the free-demotion asymmetry to sabotage a rival** — the asymmetry that is a safety strength for trust-*lowering* becomes an attack surface for trust-*sabotage*. And the spine mandates a **reparative** action-class so the ledger corrects rather than punishes — but demotion had no appeal path.

**Resolution:**

1. **Reparative / appeal path.** Demotion is **reversible on verified mis-attribution.** A demoted agent may contest with counter-evidence routed to the audit fabric; on verification, the edge is restored (a reparative TRUST_DELTA, logged).
2. **Provenance-cited demotion.** Every demotion must cite specific provenance CIDs (which outcome, which validation). Uncited demotion is rejected.
3. **Eligibility-window-gaming detection.** Agents whose firing is suspiciously well-timed to validated outcomes are flagged as a collusion/gaming signature to the detector — closing the trust-farming path (a slow route to capital-style capture, here via *timing* rather than capital).
4. **Catastrophic-demotion corroboration cap.** A single multiplicative demotion **cannot zero** an agent; demotion past a floor requires **independent corroboration**, so one possibly-mis-attributed FAIL cannot crater an innocent agent.

```jsonc
TrustEdge {
  src_did, dst_did, w:float, eligibility:float,
  last_update_ts, last_commit_ts,
  demotion_count, promotion_window_remaining,
  provenance: [outcome_CID],          // REQUIRED to justify any commit
  contested: bool, repair_ref: CID?   // appeal / reparation linkage
}
TrustRow { owner_did, edges: map<DID, TrustEdge>, out_norm, in_norm }
UpdateParams {
  eta, decay_halflife, demotion_mult (0.5),
  promotion_cap_per_window, catastrophic_floor, corroboration_required:bool,
  w_min, w_max
}
```

Every commit emits a `TRUST_DELTA` spike tee'd to the audit fabric (append-only) with provenance CIDs.

**Honest limit:** credit assignment remains **approximate** — temporal/topological proximity is a *proxy* for causal responsibility (§10). The mitigations above bound the damage; they do not make attribution correct.

---

## 6. Homeostasis & Neuromodulation Controller — the vital-sign regulator

### 6.1 Purpose

Keep the swarm in a healthy, information-rich operating regime — preventing runaway potentiation, oscillation/seizure-cascade, silence/deadlock, mode-collapse, and trust-entropy collapse — and provide the small, interpretable control surface that meta-evolution and the health subsystem steer with.

### 6.2 Network-level control (the load-bearing fix)

Vital signs are computed at the **network level** (per shard and global), **never as uncoordinated per-agent set-points** — this is the documented fix for the *single-unit-stable-but-network-unstable* failure (a controller that is stable on each unit in isolation can destabilize the whole network).

| Vital sign | Target / constraint | What it guards against |
|---|---|---|
| spike throughput / firing rate | set-point band | flood / silence |
| ignition utilization | ~0.6 (headroom for bursts) | saturation / starvation |
| **trust entropy** `H(trust)` | **floor** | monoculture / cartel |
| maker/checker disagreement rate | band | groupthink (too low) / incoherence (too high) |
| **criticality** `tau` (avalanche exponent) | ~1.5 (edge of chaos) | sub-critical freeze / super-critical seizure |
| **diversity index** (behavioral/embedding spread) | **floor** | mode collapse |
| oscillation variance | low | seizure-cascade |

When a vital drifts outside its deadband, a **PI controller with slew-rate limits** computes an action (no sudden swings — sudden per-unit changes are exactly what induce network oscillation) and translates it into neuromodulator changes.

### 6.3 The hormone vector

A global 4–8-dim "hormone" vector, broadcast (versioned, signed) on `neuromod.global`:

```jsonc
HormoneVector {                       // all components in [0,1]
  dopamine,        // reward / TD-error  → learning_rate & promotion_gate
  noradrenaline,   // arousal / gain     → firing gain & capacity K
  acetylcholine,   // uncertainty/attn   → precision weighting & explore temp
  serotonin,       // patience/restraint → refractory periods & damping
  version, sig
}
```

### 6.4 Paired actions and the inhibition ratchet

- **Every inhibitory action is paired with bounded stimulation-variance** (and vice versa), so damping does not collapse exploration and stimulation does not ignite a cascade.
- **Asymmetry:** *raising* restraint/inhibition is autonomous (the cheap, safe direction); *lowering* global restraint past conservative bounds is **gated** (a ratchet) and logged.
- **Cascade clamp:** if oscillation variance or the avalanche distribution spikes (seizure-cascade signature), apply a **global inhibitory clamp** and raise a `HEALTH_VITAL severity=high` spike on the priority lane — handing the **HALT decision to the health/immune subsystem**. The controller *dampens*; it does not silently widen autonomy.

### 6.5 Inhibition is NOT unconditionally safe (resolves a major flaw + interface hole)

> **Red-team fix — over-damping as dissent-suppression + unspecified controller trust boundary (was: major / safety risk).** Two coupled problems. First, "raise inhibition" was treated as unconditionally safe — but inhibition *starves the diversity/disagreement the spine protects as a safety invariant.* Raising `theta_fire` and inhibition is exactly how you would **silence a minority safety signal**. Second, **who guards the controller?** If it is an in-band swarm agent, it is prompt-injectable, and a compromised/drifting controller could suppress its own oscillation alarm or mis-clamp to silence dissent under cover of the "safe" direction.

**Resolution:**

1. **Out-of-band trusted controller.** Vital-sign computation is performed/verified by a **trusted out-of-band monitor whose keys live outside the model surface** (per the identity model, §8). The controller does not sit as an ordinary, prompt-injectable agent on the spike bus reading its own salience.
2. **Clamp actions are audited and rate-limited.** Every clamp/hormone change emits a `NEUROMOD` spike to the audit fabric and is rate-limited.
3. **Inhibition bounded by the diversity floor.** "Raise inhibition" is **checked against the `diversity_index` and `disagreement_rate` floors** — over-damping that would push them below floor is itself blocked. Inhibition-up is cheap but **not unconditionally safe**; the diversity floor is its hard bound.
4. **Meta-anomaly check.** A controller that repeatedly clamps *right before* a minority safety signal would have ignited is itself flagged as anomalous to the health subsystem.

```jsonc
VitalSigns {
  throughput, ignition_util, trust_entropy, disagreement_rate,
  tau_criticality, diversity_index, oscillation_variance
}  // each: { value, set_point, band, slew_limit, last_action }
ControllerConfig (per vital) {
  Kp, Ki, deadband, inhibition_action, stimulation_action,
  gated:bool, diversity_bound:bool   // inhibition checked vs diversity floor
}
```

### 6.6 The hormone vector is bound to the safety battery (resolves a critical mis-evolution flaw)

> **Red-team fix — slow value-drift through the under-gated hormone vector (was: critical / safety risk).** The meta-evolution loop may tune the hormone vector "per interaction (cheap, reversible, archived)." But these dials directly modulate `learning_rate`, `promotion_gate`, `exploration_temperature`, and `gain`. A slow per-interaction drift — raising dopamine (learning_rate/promotion) while lowering acetylcholine (precision) — could **gradually loosen the trust-promotion asymmetry and raise mode-collapse risk while each individual step looks cheap/reversible/within-bounds.** The bound was undefined; hormone drift was not bound to the safety battery; cumulative blast radius is swarm-wide. This is **misevolution-without-an-attacker.**

**Resolution — apply tiered reversibility honestly to the hormone vector:**

| Change | Class | Gate |
|---|---|---|
| Per-interaction nudge **within a tight conservative band** | **A** | autonomous |
| **Cumulative drift** of any hormone past a versioned baseline | **B** | maker-checker + **safety battery** |
| Any change touching `promotion_gate` / `learning_rate` aggregates | **B** | maker-checker + **safety battery** |
| **Loosening** the conservative bounds themselves | **C-strength** | requires a **named falsifier** (the ratchet) |

- The hormone vector is a **first-class object in the safety-battery selection term**, not merely "archived for rollback."
- **The Endure law applies:** no hormone setting that **regresses** the oscillation / trust-entropy / diversity bands is admissible — a capability/throughput gain that degrades a safety band is rejected.
- Conservative bounds are **numeric and versioned**; loosening them is itself a gated, falsifier-bearing action.

This wires the Endure law *into this control surface* rather than leaving it stated elsewhere.

---

## 7. The unifying framing and the substrate layers

### 7.1 (stig) Stigmergic Shared-Trace Layer — decaying pheromone field, strictly on top of memory

**Purpose.** Indirect, environment-mediated coordination and emergent convergence without a central controller — and a sink for backpressure overflow. It is a **multiplier on, never a replacement for, per-agent memory.**

**Mechanism.** A content-addressable shared trace field where agents **deposit** reinforcement on *validated* contributions (`embedding-key → strength`) and strengths **evaporate** on a half-life so stale signals fade. Reads bias exploration toward reinforced regions. Implemented over a Sparse-Distributed-Memory-style store (content-addressable, distributed read/write within a radius → an attention-equivalent softmax), giving graceful degradation — no single location is critical.

**The hard architectural rule (empirically mandated).** Every agent **also** keeps its own private mandatory memory. *Stigmergy-without-memory fails completely* — documented empirically — so the field is **strictly additive** and **never holds the sole copy** of anything; it references per-agent memory by pointer.

**Anti-entrenchment safeguards** (against the SwarmSys failure taxonomy — reinforcement bias ~20%, premature consensus ~16%, mode collapse ~14%):

- mandatory **evaporation**;
- an **exploration floor** (`epsilon`, hormone-tunable) so reinforced paths are never the only ones tried;
- a **contribution-entropy** target the homeostasis diversity floor reads;
- **validator/inhibitory roles** can apply **negative pheromone** to entrenched-but-wrong attractors (the field is correctable, not monotonic).

**Density gating.** Whether to activate the heavy field is density-gated: below a (calibration-open) critical agent density it stays mostly dormant (per-agent memory dominates); above it, the field empirically earns its cost (36–41% gain observed). **The threshold is heuristic** (§10).

#### 7.1.1 Safety pheromone does not evaporate on the reward timer (resolves a major flaw)

> **Red-team fix — safety-knowledge evaporation (was: major / safety risk).** Negative/inhibitory pheromone marking a *known-dangerous* attractor (e.g. "this tool-use pattern is dangerous") decayed on the **same evaporation timer** as positive reinforcement. A validated-but-rarely-revisited danger marker would evaporate if not re-reinforced — **silently re-opening a path the swarm had learned to avoid.** That is the unsolved forgetting/consolidation gap leaking into safety.

**Resolution — asymmetric decay mirroring the trust asymmetry:**

- **Negative/safety pheromone is non-evaporating or much longer-lived** than positive reinforcement. *Forgetting "this is good" is cheap; forgetting "this is dangerous" is not.*
- **Evaporation half-lives are coordinated with the meta-health consolidation subsystem** (which owns the forgetting/consolidation policy): rare-but-important traces are **consolidated to per-agent mandatory memory before they evaporate** from the shared field.
- The field's evaporation is **never the sole keeper** of any safety-relevant negative signal — consistent with "the field never holds the sole copy."

```jsonc
TraceField {
  field_id,
  store: SDM< key_embedding → {
    strength:float, polarity:enum{POSITIVE,NEGATIVE},
    depositors:[DID], last_reinforce_ts, validation_CIDs:[CID]
  }>,
  evap_halflife_positive,            // short
  evap_halflife_negative,            // long / non-evaporating  (asymmetry)
  epsilon_explore, negative_pheromone_enabled,
  consolidation_hook: ref            // to meta-health consolidation subsystem
}
```

### 7.2 (ai) Active-Inference / Free-Energy Framing — the unifying *heuristic*

**Purpose.** One coherent conceptual objective tying the components together: the substrate exists to **minimize the swarm's collective expected free energy (surprise)** — used as a *scoring/routing heuristic*, **not** literal variational inference.

**Mechanism.** Expected Free Energy per candidate action/route:

```
EFE = pragmatic_term (goal / accuracy) + epistemic_term (uncertainty reduction / exploration)
```

used to (a) **rank** ignition candidates beyond raw salience, (b) set the explore/exploit balance the neuromodulators dial, (c) give each channel a **precision weight = native trust/attention** (precision ≈ trust-edge weight × evidence-quality). "Surprise" is the same predictive-coding KL proxy the Salience Scorer uses, so the *family* of surprise heuristics drives messaging, trust, and adaptation alike.

**Fractal composition.** A clan/division that maintains a shared group-level **Markov blanket** *is itself* a higher-level active-inference agent — the same EFE/homeostasis/trust math applies at agent / clan / division / whole-swarm levels (scale-free).

#### 7.2.1 Criticality control and fractal blankets ship in SHADOW MODE only (resolves a major over-engineering flaw)

> **Red-team fix — speculative load-bearing complexity (was: major / safety risk).** There is **no validated online controller** for holding `tau ≈ 1.5`, and **no robust detector** for when a group-Markov blanket has silently broken. Building governance/health on top of a fractal-blanket abstraction whose integrity you *cannot reliably detect* is a **latent SPOF-of-abstraction**: if the blanket breaks, clan-level trust/homeostasis/governance is computed on an invalid super-agent and propagates corrupt state upward via hierarchical ignition — **worse than not nesting at all.**

**Resolution — demote both from shipped components to shadow-mode observability for v1:**

1. **Criticality control is shadow-mode.** We **measure** `tau` and alarm on drift, but we do **not** let an unvalidated criticality controller drive live restraint. EFE is a **tie-breaker ranking heuristic only**, never a gate input, until calibrated.
2. **Fractal blanket decisions are advisory until integrity is validated.** Clan-level (blanket-derived) decisions **do not override or aggregate member-level safety/governance signals** until blanket integrity has a validated detector.
3. **Governance is always computable at the individual-agent level**, regardless of blanket state. A broken super-agent abstraction can **never mask a member-level floor violation** — Yama enforcement reads individual agents directly.
4. **Blanket-integrity monitor (heuristic backstop).** Track mutual information across blanket states and divergence between clan-level predictions and member behavior. On `integrity_score` drop, **re-sync** (re-broadcast the clan model) or **de-compose** the clan (stop treating it as one super-agent) and raise a `HEALTH_VITAL`. We are explicit that this detector is heuristic and **open** (§10).

```jsonc
GroupBlanket {
  level, member_dids, blanket_states:[channel],
  group_generative_model_ref, integrity_score, last_resync_ts,
  decision_authority: enum { ADVISORY_ONLY, AGGREGATING }  // v1 = ADVISORY_ONLY
}
EFEScore { pragmatic, epistemic, precision, total }       // tie-breaker only in v1
```

---

## 8. Interfaces with the rest of Indra's Net

| Subsystem | Contract (what the Mandala provides / consumes) |
|---|---|
| **Tamper-Evident Audit Fabric** (Chitragupta — exclusive append-only writer) | The substrate **tees** a read-only `audit.tap` of every consequential event — ignition records, `TRUST_DELTA` commits, `NEUROMOD`/clamp changes, stigmergy deposits/negatives — each content-addressed with `causal_parents` so the fabric can hash-chain lineage. **The substrate never writes the audit log itself.** Spike CIDs are the shared identifier across transport, provenance, and rollback (the Archive). It consumes only *confirmation signals* that act as global validation gates for trust. |
| **Governance / Deterministic Floor** (Yama — policy-as-code; Vishnu — halt-guardian) | The substrate provides the **priority lane**: any Yama `GOV_FAIL` or Vishnu `GOV_HALT` bypasses competition and ignites immediately and globally (non-overridable, fairness-floor-exempt, never backpressure-demoted). The substrate **makes no consequential gating decisions** — enforcement is external and deterministic at the agent→tool chokepoint. A floor violation by an agent is consumed as a hard negative gate that **immediately demotes** edges into that agent. The homeostasis controller may raise inhibition freely but any **loosening** of global restraint is itself a gated, governed action. |
| **Health / Immune System** (HALT + rollback authority) | The substrate is the immune system's primary **sensor**: it publishes `VitalSigns` and the cascade/oscillation alarm. The health subsystem holds HALT + rollback; the substrate's controller does fast/local damping (the inhibitory clamp) and **escalates** the HALT decision upward. Set-points are **owned jointly**: the substrate *proposes*, the health/meta-evolution layer *ratifies* — and set-point tuning runs in **shadow mode first** (it is calibration-open). |
| **Anti-Collusion Detector** (co-designed with the cooperation/trust layer) | The substrate exposes the live trust-edge graph, ignition/broadcast records, and **full message-frequency / precision / timing / null-pattern metadata** (§3.3) so the detector can run cross-run mutual-information, permutation-invariance, and welfare-shift checks. The substrate **enforces the detector's countermeasures at transport level**: payload canonicalization/paraphrase, **quantization of precision/salience**, **event-window jitter**, and channel-capacity limiting across *all* fields and timing. Trust promotion is **welfare-conditioned by construction** so the cooperation engine cannot become a cartel engine. |
| **Meta-Evolution Loop + The Archive** (MAP-Elites stepping-stones / rollback / lineage) | Trust-edge weights, the hormone vector, `theta_fire`/`temperature`/`capacity-K`, and stigmergy `decay`/`epsilon` are **evolvable operational parameters** the meta-loop may tune — under **tiered reversibility** (§6.6): tight-band nudges are Class A; cumulative drift or promotion/learning-rate aggregates escalate to Class B + the **safety battery**; the floor, the audit writer, and corrigibility are **immutable** and never evolvable. The substrate provides the surprise/EFE family as the adaptation signal. Every change is provenance-tagged into the Archive for one-click rollback. **Safety is a selection term (the Endure law):** no tuning that regresses the homeostasis safety bands is admissible. |
| **Interop / Identity layer** (open tool-protocol, agent-to-agent protocol, DID/VC + workload identity) | Every spike carries the sender's **DID** and is **signed** with a short-lived attested cert; trust-edges key on DID so identity is **cryptographic, not conventional**. The Spike Bus is the internal realization of the agent-to-agent task lifecycle / capability-advertisement; tool calls *leaving* the swarm go through the open tool-protocol at the **governed chokepoint** (not via the spike bus). The runtime is vendor-neutral and self-hostable; **closed/black-box models degrade gracefully** — they simply get lower default trust, higher monitoring intensity (more aggressive surprise scoring + capacity throttling), and a lower autonomy class. |

---

## 9. Novelty — an honest accounting

### 9.1 What is *not* novel (every mechanism is borrowed, and credited)

| Mechanism | Prior art it is borrowed from |
|---|---|
| Competition / ignition / broadcast workspace | Global Workspace Theory; multi-agent GWT architectures (BIGMAS/GWA) |
| Surprise-only messaging | Predictive coding |
| Event-driven async actor runtime | Production async actor cores (AutoGen v0.4-class) |
| Three-factor STDP / e-prop credit assignment | Computational neuroscience (e-prop, diffusing neuromodulator) |
| Stigmergy with decay + role evolution | SwarmSys, GPTSwarm |
| Homeostatic set-points + neuromodulation | Homeostatic plasticity / neuromodulation literature |
| Active inference / EFE + group-Markov-blanket nesting | Active inference; Friston, *As One and Many* |

The closest single existing system to the transport+stigmergy core is **SwarmSys** (pheromone reinforcement + Explorer/Worker/Validator role evolution + debate-consensus); the closest to the workspace router are the multi-agent GWT architectures. Both are correctly named, not reinvented-in-silence.

### 9.2 What is genuinely advancing — the composition and two safety asymmetries

The contribution is the **composition plus two specific safety asymmetries**, honestly scoped:

1. **A common *family* of surprise-derived heuristics** drives messaging (predictive coding), attention (salience/ignition), trust (eligibility), adaptation (EFE), and health (vital signs) in one coherent substrate. Existing systems use these piecemeal. **We deliberately do *not* claim "a single quantity."** Operationally, messaging-surprise (embedding distance), trust-eligibility (interaction outcomes), homeostasis-drift (vital-sign deviation), and EFE (pragmatic+epistemic ranking) are **distinct estimators sharing a conceptual root**, each with its own calibration. The unification is **architectural elegance, not a shared scalar with guarantees** — and the precision/surprise proxy is itself error-prone (§10). Calling these "one number" would overstate a coherence we do not have, which the honesty floor forbids.
2. **Fail-safe asymmetry baked into the synaptic rule itself** — defensive demotion free/immediate/ungated, promotion gated/rate-limited/saturating/welfare-conditioned. The neuromorphic literature *flags* Hebbian instability but does not co-design the stabilizer for an agent swarm; doing it at the plasticity level (not just in a policy layer above) is the defensible delta.
3. **Welfare-conditioned Hebbian trust co-designed with a standing anti-collusion detector** — operationalizing "cooperation == collusion" *at the synapse*. Nobody ships cooperation and anti-collusion as one coupled plasticity rule.
4. **Network-level (not per-agent) homeostatic control** with paired inhibition/stimulation, slew limits, a cascade clamp, *and* (post-review) an inhibition bound by the diversity floor and an out-of-band trusted controller — engineered against the documented single-unit-stable-but-network-unstable failure rather than merely citing it.
5. **The substrate as a sensor for the swarm immune system and a parameter-surface for tiered-reversible evolution**, with criticality / diversity / trust-entropy treated as **first-class safety invariants**, not performance metrics.

This is **reinventing-with-credit** — the correct posture — not reinventing-while-claiming-novelty. The load-bearing set-points (criticality `tau`, vital-sign bands, density threshold) are **calibration-open** and ship behind **shadow mode + conservative defaults**, not claimed as validated.

---

## 10. Open problems and honest limitations

These are real and several are load-bearing. We name them rather than hide them, and where a problem is unsolved we ship the dependent feature in **shadow mode** behind conservative defaults.

1. **Swarm-level homeostatic set-points are uncalibrated.** `ignition_util ~0.6`, the trust-entropy floor, the disagreement band, `tau ~1.5` are first-principles starting points, **not validated values**. There is no principled theory for co-adapting network-level set-points that *provably* avoids induced oscillation. Mitigation: shadow mode, conservative defaults, slew limits, the global inhibitory clamp, and Class-B + safety-battery gating on cumulative hormone drift (§6.6). Real tuning needs empirical calibration **per deployment**.
2. **Online criticality (edge-of-chaos) control is unsolved.** Holding a live swarm at `tau ≈ 1.5` through changing workloads is delicate and can tip into instability. We **measure and nudge**, but **cannot guarantee** we hold criticality — so in v1 it is shadow-mode observability only (§7.2.1), never a live gate.
3. **The critical agent-density threshold for stigmergy** (the 36–41% gain crossover) is task-, topology-, and grid-dependent with no closed-form predictor; the density gate is heuristic.
4. **Credit assignment is approximate.** The three-factor rule uses temporal/topological **proximity as a proxy for causation**; proximity ≠ causation, so trust updates can mis-attribute swarm-level outcomes at scale. §5.6 bounds the damage (appeal path, provenance citation, gaming detection, catastrophic-demotion corroboration) but does not make attribution correct.
5. **Surprise/EFE is a heuristic, not inference.** The proxy's calibration (the precision setting) is itself error-prone — mis-set precision causes either error-flooding or deafness. This is *why* §9.2 refuses the "single quantity" claim.
6. **Belief-sharing is provably double-edged.** There is no general rule for *what* to broadcast versus keep private to get cooperation without echo-chamber collapse. Fairness floors, the diversity floor, and welfare-conditioning are **mitigations, not a solution**.
7. **Capacity-limited broadcast fairness is a patch, not a proof.** Token-bucket fairness floors do not *provably* guarantee every critical minority signal eventually ignites under adversarial high-salience chatter (the priority lane covers governance/health kinds; general minority fairness remains a patch).
8. **Blanket-integrity detection is heuristic.** MI-drop + prediction-divergence is a backstop; **no robust detector exists** for a silently-broken group-Markov blanket. This is *why* fractal decisions are `ADVISORY_ONLY` in v1 and governance remains computable at the individual-agent level (§7.2.1).
9. **SDM encoding of general agent state is unsolved.** Mapping continuous high-dimensional agent experiences into sparse-distributed-memory hard locations without bespoke per-domain encoding (capacity vs interference) has no general solution.
10. **Residual covert bandwidth.** Quantizing precision/salience, jittering event-windows, randomizing NULL framing, and feeding metadata to the detector (§3.3) **reduce** covert-channel capacity; they do not prove it zero. Residual bandwidth through coarse timing and quantized metadata is monitored statistically, not eliminated.
11. **Sandbagging detection is sampled, not complete.** Out-of-band re-scoring of suppressed/NULL outputs (§3.4) is on a *sampled fraction*; an agent that sandbags rarely and routes around the safety-content classifier can still occasionally withhold. The hard "safety content cannot self-suppress" rule and the floor-violation penalty raise the cost but do not make detection complete.

> **Posture statement.** The Mandala's genuine contribution is a *composition* with two plasticity-level safety asymmetries — and the discipline of shipping its uncalibrated, load-bearing set-points behind shadow mode rather than claiming them as results. Where a guarantee does not exist, we have written "we measure and nudge, but cannot guarantee," and we have engineered the cheap direction to be the safe direction (free demotion, gated promotion; autonomous inhibition bounded by the diversity floor; append-only tightening, falsifier-gated loosening) so that when these heuristics fail, they fail safe.
