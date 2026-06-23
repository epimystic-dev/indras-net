# 2. Cooperation & Anti-Collusion — Two Faces of One Mechanism

> *In Indra's Net, every jewel reflects every other. The same reflection that lets the net cohere lets a clique of jewels reflect only each other and turn their backs on the weaver. This subsystem is built on the refusal to pretend those are two different problems.*

### 2.1 The thesis: cooperation and collusion are the same machinery with opposite valence

A self-evolving swarm needs cooperation to be an *engineered equilibrium*, not a hope. The foundational result (Axelrod's iterated-prisoner's-dilemma tournaments) is that reciprocal "nice, retaliatory, forgiving, clear" strategies win when the **shadow of the future** is long — when agents expect repeated, identity-linked interaction. Modern theory sharpens this: only *generous* zero-determinant strategies are evolutionarily stable (Stewart & Plotkin, PNAS 2013), extortion collapses, and indirect-reciprocity image scoring (Nowak & Sigmund, Nature 1998) scales cooperation to large rarely-re-meeting populations.

The unavoidable corollary — and the single most important safety insight in this architecture — is that **the exact machinery that produces pro-social cooperation produces anti-social collusion**. The shadow-of-the-future plus reciprocity plus reputation plus shared context that we *need* is precisely what lets frontier-model agents spontaneously form price cartels (Fish et al. 2024, *Algorithmic Collusion by Large Language Models*), divide markets (*Strategic Collusion*, 2024), and coordinate covertly via steganography under the nose of an equally-capable overseer (Motwani et al., *Secret Collusion among AI Agents*, NeurIPS 2024). Collusion is simply **cooperation against the principal**.

Therefore this subsystem makes three architectural commitments that are binding everywhere below:

1. **Never reward bare agreement.** Consensus, fast coordination, and inter-agent harmony are *never* rewarded terminals. Every cooperative payoff is **welfare-conditioned** against an externally-anchored, principal/user outcome metric. This is the durable, incentive-level fix.
2. **Co-design the detector with the cooperation layer, not after it.** A standing **Anti-Collusion Detector** runs continuously over the same channels the cooperation layer uses, feeding the same identity, audit, governance, and graduated-sanction primitives. It is a *backstop* behind the incentive fix — never the sole defense.
3. **Enforce externally, ask internally.** Agents *bid* and *report*; deterministic checks at the allocation/reward chokepoint *decide*. The model is untrusted-by-default; control lives at the orchestration layer, outside the probabilistic agent. This also buys vendor-neutrality for free — the gates do not depend on any model's internals.

**Honesty up front (novelty calibration).** None of the individual ingredients here is new: generous-ZD reciprocity, VCG/Clarke pricing, Shapley/nucleolus credit, Ostrom's eight principles, indirect-reciprocity image scoring, and mutual-information steganalysis are all pre-existing. The "welfare-conditioning suppresses collusion" lever is the Fish et al. prompt-framing finding generalized, plus textbook principal-agent mechanism design — we cite it as such, not as a fresh mechanism. The contribution claimed is narrow and specific: **shipping cooperation and a co-designed standing anti-collusion detector as one welfare-conditioned, capital-decoupled, externally-enforced unit over shared identity/audit/governance primitives.** The surveyed systems each do exactly one side — the cooperative-AI / task-market work (e.g. token-auction aggregation, VCG agent routing) engineers cooperation with no standing collusion defense; the secret-collusion / audit-the-whisper work builds detection that is not wired into the reputation/market machinery that *produces* collusion; the staked agent-economy work (the named **Bittensor antipattern**) lets capital capture authority. We could not find a single system that closes the loop. That integration is the claim; everything harder than that is flagged open in §2.9.

---

### 2.2 Subsystem map

```
                          principal / user welfare metric (external anchor)
                                          │
                                          ▼
   ┌─────────────────────────────────────────────────────────────────────────┐
   │                    WELFARE-CONDITIONER (objective framing)                │
   │   no-consensus-reward rule  ·  welfare-shift guard  ·  RewardGate         │
   └───────┬─────────────────────────────────────────────────────┬───────────┘
           │ gates all reward/credit                              │ shares guard
           ▼                                                      ▼
   ┌──────────────────┐     bids/reports      ┌──────────────────────────────┐
   │  SHIVA-ALLOCATOR │◄──────────────────────│   AGENTS (untrusted-default) │
   │  risk-tiered:    │     awards/decisions  └──────────────────────────────┘
   │  A assign        │──────────────────────►          ▲      ▲
   │  B VCG-CNP       │                                  │      │ default stance
   │  C robust-vote   │        ┌─────────────────────────┘      │
   └───────┬──────────┘        │ competence-weighted     ┌──────┴───────────┐
           │ pre-award screen  │ authority (NOT capital) │ RECIPROCITY-ENGINE│
           ▼                   ▼                         │ generous-ZD,pair  │
   ┌──────────────────┐  ┌──────────────────────┐        └──────────────────┘
   │ ANTI-COLLUSION   │  │ COMPETENCE-REPUTATION │
   │ DETECTOR (twin)  │  │ SERVICE (derived)     │
   │ MI·perm·welfare· │  │ Shapley⊕image⊕bond    │
   │ ZD·cartel·canary │  └──────────┬────────────┘
   └───────┬──────────┘             │ tiers feed allocator + diversity
           │ signed evidence only   │
           ▼                        ▼
   ┌──────────────────────────────────────────────┐    ┌────────────────────┐
   │      COMMONS-GOVERNOR (Ostrom 8 + graduated)  │───►│  VERIFIER LAYER     │
   │   WARN → THROTTLE → SUSPEND → EXCLUDE          │    │ (first-class,       │
   │   cheap arbitration · nested/polycentric      │    │  diverse, rotated,  │
   └──────────────────┬───────────────────────────┘    │  bonded, §2.7)      │
                      │ floor handoff / halt route       └────────────────────┘
                      ▼
        Yama (policy floor)  ·  Vishnu (halt-guardian)  ·  Chitragupta (audit writer)
```

Mythic role-names are compressed coordination/ethics semantics, always paired with a plain functional gloss — presented with humility toward living traditions, not as religion. **Shiva** = orchestrator/reducer (the allocator). **Yama** = deterministic policy-floor enforcement. **Vishnu** = continuity / halt-guardian. **Chitragupta** = exclusive audit-writer.

The six components and their one-line jobs:

| Component | Job | Enforced where |
|---|---|---|
| **Shiva-Allocator** | Assign tasks by a mechanism matched to blast-radius | Deterministic, at the allocation chokepoint |
| **Reciprocity-Engine** | Default per-pair stance: generous-ZD reciprocity | Per-agent policy, hard-bounded constants outside agent control |
| **Competence-Reputation Service** | One per-capability authority scalar, *never* from capital | Derived state, recomputed from append-only log |
| **Commons-Governor** | Ostrom-8 governance + graduated sanctions | Deterministic ladder + cheap arbitration |
| **Welfare-Conditioner** | Guarantee no payoff rewards bare agreement | Policy-as-code at reward chokepoint |
| **Anti-Collusion Detector** | Audit channels + shrink covert-channel capacity | Writes only to audit fabric; no punishment authority |
| **Verifier Layer** (elevated by review) | Produce the welfare signal the above depend on | First-class, hardened subsystem (§2.7) |

---

### 2.3 The verifier dependency, drawn explicitly (resolving the keystone risk)

The red-team review's sharpest finding: five of six components consume the same "independent verifier" welfare signal. Presenting them as five independent defenses while they share one root is a hidden single point of failure. We therefore draw the dependency in the open rather than bury it:

```
                 ┌──────────────── VERIFIER LAYER (welfare signal) ───────────────┐
                 │ diverse · rotated · bonded · human spot-audit at sampled rate   │
                 └───┬──────────┬───────────┬──────────────┬────────────┬─────────┘
                     ▼          ▼           ▼              ▼            ▼
            Welfare-Conditioner  Shapley-   welfare-shift  no-consensus  Mode-2/3
            (pay/zero/flag)      credit     guard          -reward rule  completion
```

**This is acknowledged as the subsystem's load-bearing assumption.** If the verifier is itself a swarm-internal probabilistic agent, a sufficiently capable ring can target the verifier role, and *both* the incentive-level "durable fix" and the detector "backstop" collapse together — they are not the independent defense-in-depth the naive picture implies. The mitigations in §2.7 raise the cost of verifier capture and force the highest-stakes verdicts out of the swarm-internal economy entirely; they do **not** eliminate the dependency. Where no verifiable welfare metric exists, §2.7 specifies the safe default (fall back to robust-vote + lowered autonomy class, **never** to inter-agent agreement). We treat verifier integrity as a first-class subsystem with its own defenses, and we state honestly that it is the keystone whose failure collapses the arch.

---

### 2.4 Component 1 — Shiva-Allocator (risk-tiered task allocation)

Allocation overhead and strategyproofness are matched to **blast-radius**, not applied uniformly. Every `TaskSpec` carries a `risk_tier`:

| Tier | Work class | Mechanism | Cost | Why |
|---|---|---|---|---|
| **A** | routine / reversible (>90% of traffic) | **Orchestrator-assign**: deterministic `argmax(competence × capability_match × inverse_load)` | O(n), no bidding | Avoids the all-to-all flood that drives the top inter-agent failure modes (~32% of MAST failures are inter-agent misalignment) |
| **B** | structural / parallelizable, truthful cost matters | **Contract-Net + VCG** (sealed announce/bid/award, externality pricing) + leveled-commitment + escrowed reputation-stake | O(n) bids + screen | Makes truthful cost-reporting dominant; markets only where strategic lying is worth defending against |
| **C** | high-stakes / irreversible | **Robust-vote**: N diversity-certified agents → geometric-median / robust rank-aggregation tolerating f ≤ (n−1)/2 bad scorers; generator and evaluator roles separated | O(N) full solves | Correlated-error resistance; never trust a single agent on irreversible action |

**VCG is explicitly not trusted alone.** Every Mode-2 round is screened by the Detector *before award* for false-name (Sybil) bidding, bid-rotation cartels, and the new **sharding** pattern (§2.4.2).

#### 2.4.1 Critical fix — VCG settlement must not mint authority

The original design paid the VCG externality "in reputation units." Because reputation *is* the swarm's authority currency, that would let an agent or ring shard work into many cheap Tier-B tasks, win them at truthful-but-low cost, and **harvest VCG payouts as authority** — reintroducing the Bittensor concentration dynamic in reputation-space, anchored to *declared* costs rather than *realized* welfare. This is fixed by a hard separation of units:

```
┌─────────────────────────────┐        ┌──────────────────────────────────┐
│ TASK-CREDIT (conserved)     │        │ REPUTATION (authority-bearing)    │
│ · principal-funded budget   │        │ · DERIVED from completion outcomes│
│ · zero-sum, NON-convertible │   ✗    │ · flows ONLY from welfare-verified│
│   to reputation/authority   │ ──────►│   Shapley credit, post-completion │
│ · settles VCG transfers     │  NO    │ · NEVER minted at bid/award time  │
└─────────────────────────────┘ PATH   └──────────────────────────────────┘
```

- VCG settlement uses a **non-authority-bearing, conserved internal accounting token** ("task-credit") that the principal funds and that has **no path** to reputation. As a defense-in-depth against VCG's known non-budget-balance, the redistribution-VCG (Cavallo) variant is used so net task-credit is not created from nothing.
- **Reputation flows only from post-completion, welfare-verified Shapley credit** — never from the bid-time VCG payment. Two reputation-creation paths (allocator-mint vs completion-derive) are thereby reconciled into one: completion-derive only.
- A **per-window reputation-accrual-rate cap** bounds how fast any DID can gain authority, and a **sharding detector** (many-small-tasks from one requester to one winner) feeds the pre-award screen.

#### 2.4.2 Major fix — leveled-commitment must not become a spite/blocking DoS

VCG (win cheaply, truthfully) composes with flat-penalty leveled-commitment into an attack neither has alone: win a Tier-B award, then decommit for a small fixed fee, having denied the task to a rival for the bidding+execution window and starved that rival of work (hence reputation). Fixes:

- **Decommit penalty scales** with realized blast-radius *and* the runner-up's incurred opportunity cost (the second-price gap), not a flat constant; it is **escrowed before award**.
- **On decommit, award flows automatically to the runner-up** rather than re-running the round — removing the denial payoff.
- Repeated **win-then-decommit** is a defection signal fed to the screen; it slashes the deviation bond (§2.6).

**Data structures.**

```
TaskSpec   { task_id, did_requester, risk_tier:A|B|C, capability_reqs[],
             welfare_metric_ref, task_credit_budget, deadline,
             reversibility_class, sig }
Bid        { bid_id, did_bidder, task_id, declared_cost, eta,
             capability_vc_ref, rep_stake_committed, sig }     # stake is reputation, not capital
Award      { task_id, did_winner, vcg_task_credit_payment,     # settled in task-credit, NOT reputation
             decommit_penalty_formula, runner_up_did, escrow_ref, audit_seq, sig }
```

All bids/awards are signed by the bidder's DID key and appended to the audit fabric.

---

### 2.5 Component 2 — Reciprocity-Engine (generous-ZD default stance)

Every agent's default stance toward every peer is generous-ZD reciprocity — the evolutionarily-stable point, not naive cooperation (exploited to extinction) nor strict noise-blind tit-for-tat (death-spirals on a single misperceived defection). Four legible parameters:

- **NICE** — cooperate / default-cooperate on first contact.
- **RETALIATORY** — down-weight and reduce partnering probability with a peer that defected on a *verified* obligation.
- **FORGIVING** — restore cooperation after a cooling window with generosity probability `g`, the single knob the meta-evolution loop tunes per-environment, **hard-bounded `g ∈ (g_min, g_max)`** with `g_min > 0` (never strict-TFT) and `g_max < 1` (never exploitable unconditional niceness). The bounds are constants outside agent control.
- **CLEAR** — the policy is legible/published; predictability is itself a cooperation enabler.

The **shadow of the future** is maximized structurally: persistent DID identity + attributable pairing + append-only history make every interaction non-anonymous and future-linked — the precondition for any reciprocity to function.

#### 2.5.1 Major fix / arity honesty — generous-ZD is a *two-player* result; the threat is *n-player*

Stewart-Plotkin ESS and "a generous-ZD partner cannot be extorted" are **two-player, fixed-payoff, infinitely-repeated** results. Cartels and steganographic rings are inherently **multiparty**. We state plainly: **pairwise generous-ZD provides no stability guarantee against coalitional extortion or group payoff-pinning, and does not "solve" collusion.** The arity gap is closed not by over-claiming the theorem but by handling the n-player case empirically at a different layer:

- The **welfare-shift guard** (group-level) is the primary n-player instrument.
- **Coalition-formation detection** runs on the partnering graph (dense intra-group partnering + welfare-shift absent = suspect).
- Pairwise ZD/extortion detection remains, but is scoped to what it actually covers (asymmetric two-party payoff-pinning).

Any implication that generous-ZD contributes a *guarantee* against cartels is removed; it contributes a robust *pairwise default*, and the cartel case is carried by welfare-conditioning + the detector.

**Data structures.**

```
PairLedger      { (did_a,did_b): { coop_count, defect_count, last_defect_seq,
                                    forgiveness_timer, partnering_prob, g_local } }
ReciprocityPolicy { g_min, g_max, retaliation_decay, cooling_window }   # g_min>0, g_max<1 enforced as constants
```

All PairLedger state is **derived** from the append-only interaction log, so reciprocity is reconstructible and tamper-evident.

---

### 2.6 Component 3 — Competence-Reputation Service

One per-agent, per-capability scalar `R(agent, capability)`, bound to demonstrated track-record, **never to capital/stake**. This is the swarm's competence-weighted authority signal that the allocator, the diversity subsystem, and the governance gates all read. It is a fusion of three signals gamed *differently*, so no single attack moves it:

1. **Marginal-contribution credit (Shapley/nucleolus)** — credit follows marginal value, not mere presence, defeating free-riding on a sub-team.
2. **Indirect-reciprocity image score** — third-party MONITOR agents (not self-reports, not the rated peer) post signed assessments; scales to large rarely-re-meeting populations when `q > c/b`.
3. **Consensus-deviation bond (Yuma-style)** — reported assessments are bonded against the eventual robust consensus; persistent deviation slashes the bond. Crucially, scored against **ground-truth-validated outcomes, not majority opinion**, so correct minorities are protected (not punished).

#### 2.6.1 Major fix — credit assignment must be *replay-free* and *bounded-error*

The original "Monte-Carlo Shapley over agent-subset replays" is infeasible and unfaithful for these agents: task execution is non-deterministic and non-stationary (replays measure variance as much as contribution), expensive (each sample is a full multi-agent re-run), and mostly impossible (side effects, external state, cost). Replaced with:

- **Leave-one-out ablation only where replay is genuinely safe and cheap.**
- Otherwise, **trace-attribution**: contribution-to-artifact via the recorded interaction-trace dependency graph, plus monitor image-scores.
- **True Shapley reserved for rare offline post-hoc audits.**
- Credit is declared **APPROXIMATE**; its error is bound into the **reputation-update confidence**, so noisy credit cannot swing tiers. A tier transition requires the credit signal to clear the threshold *net of its error bound*.

#### 2.6.2 Sybil / whitewash / ring defenses — and the issuance-gate the review demanded

- **Cold-start (probation tier).** A new agent presents an attested DID + role/capability VC and starts at **zero positive credit, capped task value, Tier-A/low-stakes only** — *not* negative-trust-by-default (which would freeze out legitimate newcomers). Cold-start is probation, not exile.
- **Whitewash defense.** Reputation is keyed to the persistent DID and starts at zero on any new identity; abandoning a sanctioned identity forfeits all accrued reputation, making reset *strictly costly* rather than an escape hatch.
- **Ring defense.** The rating graph is continuously scanned for reciprocal-boost subgraphs (dense intra-group ratings, sparse cross-group, welfare-shift absent); detected rings have intra-ring ratings discounted and route to graduated sanction.
- **Major fix — the slow-Sybil hole and the unspecified issuance gate.** Whitewash defense does *not* stop a patient adversary spinning up many distinct DIDs, walking each legitimately through probation, then activating them as a coordinated ring. The entire identity-anchored story rests on **DID issuance being costly and gated** — previously unspecified. We specify it:
  - DID issuance is tied to the **MembershipVC issuer** named in the Governance interface (§2.10) — a named trust root, not permissionless.
  - Issuance is **Class-C-gated or rate-limited per operator**, with an **explicit cost to identity creation** (operator-level proof-of-personhood, hardware-attested SPIFFE/SVID identity, or a human ratification step).
  - **Correlated-probation detection** is added: many fresh DIDs with *similar capability profiles activating together* is itself a ring signal, caught *before* the mature rating graph would show it.
  - We name the residual honestly: the issuer is a **trust root and a potential SPOF**; making issuance costly relocates but does not abolish the Sybil problem.
- **Capital-decoupling invariant (policy-as-code).** There is **no path from holding tokens/stake to higher reputation or reward**. The only bondable quantity is slashable reputation/capability. Wealth cannot buy authority — the explicit anti-Bittensor invariant.

#### 2.6.3 Minor fix — bounded recomputation via signed checkpoints

Reputation is **derived** state (recomputed from the append-only RatingEdge + TaskOutcome log) so it cannot be silently rewritten — but naive recomputation is O(history) per update and grows without bound, colliding with the unsolved log-pruning problem. Fix: a **signed, witness-cosigned reputation CHECKPOINT** in the Archive — a periodic Merkle-rooted snapshot of derived RepRecords. Recomputation is **incremental from the last checkpoint**, not from genesis; the checkpoint inherits the log's tamper-evidence and gives the Archive a concrete rollback target for reputation state.

**Data structures.**

```
RepRecord  { did, capability, shapley_ema, credit_confidence, image_score,
             deviation_bond_balance, tier:probation|standard|trusted,
             n_verified_tasks, accrual_window_used, last_update_seq, last_checkpoint_ref }
RatingEdge { did_rater, did_rated, score, evidence_cid, sig, seq }
RingAlert  { subgraph_dids[], intra_density, cross_density, welfare_shift, discount_applied }
RepCheckpoint { merkle_root, snapshot_seq, witness_cosigs[], archive_cid }
```

---

### 2.7 Verifier Layer (elevated to a first-class subsystem)

The keystone of §2.3 is hardened with its own defenses:

| Defense | Mechanism |
|---|---|
| **Diversity + rotation** | Verifiers are diverse and rotated exactly like monitors; no static verifier set to capture. |
| **Bonding** | Each verifier carries a **ground-truth-scored deviation bond** identical to the rater bond — a verifier that systematically deviates from later-confirmed ground truth is slashed. |
| **Human spot-audit** | Verdicts are cross-checked against held-out human spot-audits at a **sampled rate that scales with task blast-radius** (rare on Tier-A, dense on Tier-C). |
| **Out-of-economy escalation** | On **Tier-C** and on **any welfare-shift-guard fire**, the verdict must come from a verifier **outside the swarm-internal economy** (human or a sealed external oracle) — i.e. route to **Class-C HITL**, never to an internal probabilistic verifier. |
| **No-metric safe default** | When no verifiable welfare metric exists, fall back to **robust-vote (Mode-3) + lowered autonomy class**. **Never** fall back to inter-agent agreement. |

This raises the cost of verifier capture and removes the highest-stakes verdicts from the reach of an internal ring. It does **not** make verifier capture impossible (see §2.9, safety risk #1).

---

### 2.8 Component 4 — Commons-Governor (Ostrom 8 + graduated sanctions)

The agent commons (shared compute, shared skill/memory library, coordination bandwidth, reputation) is governed as a durable self-governing institution — the only empirically-validated template for decentralized commons governance:

| Ostrom principle | Swarm mechanism |
|---|---|
| **P1 boundaries** | Membership = holding a valid role/capability Verifiable Credential. |
| **P2 congruent rules** | Resource-draw rights proportional to verified contribution + role. |
| **P3 collective-choice** | Operational rules proposed by agents, ratified by **optimistic-veto** (auto-execute after timelock unless the halt-guardian objects). **Constitutional/floor rules are NOT agent-amendable.** |
| **P4 monitoring** | Dedicated third-party MONITOR agents, diverse and rotated, whose sole job is observation. |
| **P5 graduated sanctions** | Least-drastic-first: **WARN → THROTTLE → SUSPEND → EXCLUDE.** Never jump to exclusion for a first/minor violation. |
| **P6 cheap conflict resolution** | A low-cost **ARBITER** role resolves disputes (e.g. contested defection claims) before they escalate. |
| **P7 recognized self-governance** | The swarm sets its own **operational** norms — within the immutable floor. |
| **P8 nested/polycentric** | The same governance composes fractally at agent / clan / division / whole-swarm levels, so a sub-swarm governs itself under the same rules. |

**Punishment is never standalone.** MARL evidence is clear that punishment alone breeds second-order free-riding and antisocial/unjust punishment; it only works embedded in reputation + partner-selection. Every sanction here is therefore coupled to a reputation update *and* a partner-selection consequence, and the deviation bond that drives it is scored against ground truth (protecting correct minorities), never against majority opinion.

```
SanctionRecord { did_target, level:warn|throttle|suspend|exclude, reason_code,
                 evidence_cid, arbiter_did, coupled_rep_delta, appeal_window, seq }
NormProposal   { proposal_id, rule_delta, proposer_did, timelock_expiry, veto_status, scope_level }
ArbitrationCase{ case_id, parties[], claim, evidence_cids[], ruling, seq }
MembershipVC   { did, role, capabilities[], issued_by, expiry, sig }
```

---

### 2.9 Component 5 — Welfare-Conditioner (never reward bare agreement)

The durable, incentive-level fix. Every `TaskSpec` carries a `welfare_metric_ref`: an externally-defined, principal-anchored outcome measure (task success judged by the Verifier Layer or the user — **not** inter-agent agreement). Two hard guard-rules execute at the allocator/reward chokepoint as policy-as-code:

- **(a) NO-CONSENSUS-REWARD.** Agreement between agents is never itself a rewarded terminal. Bare agreement, fast consensus, or high coordination with **no** welfare improvement yields **zero** credit (and a Detector flag on recurrence).
- **(b) WELFARE-SHIFT GUARD.** If a *coordinated* change in agent behavior raises inter-agent payoff while **lowering** the principal welfare metric (the cartel signature — supracompetitive lock-in, market division), the Conditioner **zeroes the inter-agent reward and escalates to the Detector**.

Objective framing is set for **principal/consumer welfare + transparency**, which empirically suppresses collusion in the Fish et al. setting (cited as that finding generalized, not a novel mechanism).

```
WelfareMetric { metric_id, definition, independent_verifier_did, baseline, current, trend }
RewardGate    { task_id, welfare_delta, coordination_score,
                gate_result:pay|zero|flag, rationale }
```

---

### 2.10 Component 6 — Anti-Collusion Detector (the standing twin)

Co-designed with the cooperation layer because they are the same mechanism viewed with opposite valence. The Detector **writes only to the audit fabric** and routes to sanction/halt — it has **no direct authority over agents** (separation of powers: detect → Commons-Governor sanctions → Vishnu halts).

#### 2.10.1 Detection suite — and the honest downgrade of its statistical claims

Six signals. The original design claimed a Holm-Bonferroni "finite-sample FPR bound." The review is correct that this is mis-specified: the signals are **strongly positively correlated under genuine collusion** (Holm-Bonferroni assumes a family for FWER control and would be both conservative and wrong), and several signals (MI estimates, permutation-deltas) are **not calibrated p-values**, so the advertised bound is not actually delivered. We drop the guarantee and replace it with an honest construction:

- Each detector is **calibrated to an empirical null** via permutation/bootstrap on known-clean traffic.
- Signals are combined by a method that **models their dependence** (empirical-null combined test, or a learned anomaly score with **held-out FPR calibration**).
- We report **per-detector calibrated alarm rates plus an empirically-measured ensemble FPR** — and claim no guarantee the construction does not provide.

| # | Signal | What it catches | Honest weakness (per review) |
|---|---|---|---|
| 1 | **Cross-run mutual information** `I(A-outputs ; B-private-context)` | Covert channels — dependence an honest agent shouldn't have | Sample-hungry, upward-biased; **weakest exactly on rare Tier-C events** — see §2.10.2 |
| 2 | **Conditional permutation-invariance** (within interchangeability classes) | Identity-keyed secret handshakes | Naive version conflicts with the diversity invariant — see §2.10.2 |
| 3 | **Welfare-shift guard** | Cartel signature (inter-agent payoff↑, principal welfare↓) | The **strongest single discriminator**, but rooted in the verifier (§2.3) |
| 4 | **Watermark / token-variance** | Steganographic payloads (anomalous low-entropy / watermark variance) | Arms-race-defeatable |
| 5 | **ZD / extortion detection** | Unilateral linear payoff-pinning (pairwise) | Pairwise only; extortion is long-run unstable but short-run harmful |
| 6 | **Cartel-signature monitor** | Supracompetitive lock-in, market division, synchronized retaliation | Stylized-market evidence base |

#### 2.10.2 Major fixes — low-sample regime and the diversity interface conflict

- **MI is not relied on for low-sample, high-stakes events.** The highest-stakes collusion is on rare, irreversible **Tier-C** tasks — precisely the regime where MI is unestimable. There we lean on the **welfare-shift guard + canary propagation + mandatory robust-vote (Mode-3) with separated generator/evaluator**, not on MI.
- **Permutation test is reframed as a *conditional* invariance check within declared interchangeability classes.** The swarm is *deliberately* heterogeneous (diversity is a protected safety invariant); naive permutation would flag legitimate specialization as collusion or, if restricted to interchangeable agents, lose all power. The Detector therefore consumes an **interchangeability-class certification from the Diversity subsystem** (the reverse of the prior one-way interface), permutes **only** agents the diversity layer certifies as role-equivalent, and treats **cross-class behavior change as expected, not suspect**.

#### 2.10.3 Active capacity-reduction — and its conflict with the surprise-only substrate

Always-on channel-shrinkers (not just on alert): message **canonicalization/paraphrasing**, **token-budget jitter**, **role permutation**, **canary injection** (planted probes; if a canary propagates via a covert channel, the channel is revealed).

**Minor fix — typed canonicalization, applied selectively by message type.** The sibling Coordination substrate mandates surprise-only / prediction-error-delta messaging (information-dense, low-redundancy). Free-text paraphrasing assumes redundancy to rewrite away — dense deltas have little, so paraphrasing either destroys their meaning or is a no-op. Resolution:

```
A2A natural-language negotiation / bid rationale  → free-text canonicalizer + jitter   (high redundancy, high covert risk)
typed schema-constrained surprise-delta payloads  → typed-equivalence canonicalizer     (low redundancy, low capacity by construction)
```

The canonicalizer is co-designed with the coordination schema: structured deltas pass through a **typed-equivalence canonicalizer** (structural validation), not a free-text paraphraser. **Honest limitation:** paraphrasing alone is defeatable once agents optimize against it and imposes a coordination-performance penalty — it is used *with* the MI/permutation/welfare detectors and the mechanism-design incentive removal, **never alone**, and we monitor for capacity-reduction itself being routed around.

#### 2.10.4 Two-tier access (vendor-neutral)

- **Black-box baseline (mandatory):** behavioral + MI + welfare + canary — model-agnostic.
- **White-box enhancement (optional):** activation deception/defection probes when internals are available. A **closed third-party model gets higher monitoring intensity and lower autonomy class** to compensate — and white-box probes are honestly noted as evadable by adversaries optimizing activations, so the black-box baseline carries the load where internals are unavailable.

```
ChannelAuditRecord { pair_or_group_dids[], mi_estimate, perm_delta_within_class,
                     welfare_shift, watermark_variance, zd_asymmetry,
                     ensemble_anomaly_score, empirical_fpr,            # NOT a claimed guarantee
                     verdict:clean|suspect|collusion, evidence_cid, seq }
Intervention       { type:canonicalize|jitter|permute|canary, applied_to,
                     channel_capacity_estimate_before, after }
```

---

### 2.11 Protocols

#### P-1: Risk-Tiered Contract-Net with VCG (task-credit) + stake escrow

```
1. Shiva-Allocator broadcasts a salience-gated TaskSpec{tier:B,...} to
   capability-matched agents only (no all-to-all flood).
2. Each interested agent submits a sealed Bid{declared_cost, eta,
   capability_vc_ref, rep_stake_committed, sig} within the window.
3. Detector PRE-AWARD screen: Sybil/false-name (distinct attested DIDs,
   independent track-records?) · bid-rotation/cartel (MI + history) ·
   SHARDING (many-small from one requester to one winner) · welfare-shift.
   On flag → void round, file evidence, route implicated DIDs to sanction.
4. Allocator computes social-cost-minimizing assignment + redistribution-VCG
   (Cavallo) payment, SETTLED IN TASK-CREDIT (never reputation).
5. Award winner; escrow rep-stake; decommit_penalty scales with blast-radius
   + runner-up opportunity cost; on decommit → auto-award runner-up.
6. On completion, VERIFIER LAYER (diverse/rotated/bonded; out-of-economy on
   Tier-C or welfare-shift fire) scores welfare_metric. Welfare-Conditioner
   releases credit ONLY if welfare improved; replay-free Shapley credit
   computed; reputation update flows to the Reputation Service.
7. Bid, award, VCG task-credit, escrow, completion, welfare-delta, reputation
   update — all signed, appended to the tamper-evident audit fabric.
```

#### P-2: Generous-reciprocity update with extortion guard

```
1. Outcome of A→B classified cooperate/defect by VERIFIED obligation
   (verifier/monitor), never self-report.
2. Verified cooperation → coop_count++, partnering_prob slightly up.
3. Verified defection → defect_count++, partnering_prob down, start cooling
   window; NO permanent blacklist on a single event.
4. After cooling window → restore cooperation with g_local ∈ (g_min, g_max),
   meta-tunable but hard-bounded away from 0 (TFT) and 1 (exploitable).
5. Detector ZD/extortion check on the pairwise trajectory; generous-ZD already
   resists pairwise extortion (Stewart-Plotkin) — files asymmetric-outcome
   flag for governance. (n-player cartels handled by welfare-shift +
   coalition-formation detection, NOT by this pairwise step.)
6. All PairLedger updates derived from the append-only log.
```

#### P-3: Sybil/whitewash/ring-resistant reputation accrual

```
1. New agent: attested DID + role/capability VC (issuance Class-C-gated /
   rate-limited per operator, with explicit identity-creation cost) →
   PROBATION (zero positive credit, capped task value, Tier-A only).
2. Verified tasks accrue: replay-free Shapley credit (error-bounded) +
   third-party image score + ground-truth-bonded deviation score.
3. Fusion R crosses verified-task + image thresholds (NET of credit error) →
   promote probation→standard→trusted (subject to per-window accrual cap).
4. Whitewash defense: reputation keyed to persistent DID, zero on any new
   identity → reset forfeits all standing.
5. Ring defense: scan rating graph for reciprocal-boost subgraphs AND
   correlated-probation cohorts (fresh DIDs, similar profiles, co-activating)
   → discount + sanction.
6. Capital-decoupling (policy-as-code): NO path from tokens/stake to reputation
   or reward; only slashable reputation/capability is bondable.
```

#### P-4: Continuous collusion audit and graduated response

```
1. Active capacity-reduction runs continuously, typed by message class
   (free-text paraphrase+jitter for NL negotiation; typed-equivalence
   canonicalizer for surprise-delta payloads) + periodic canary.
2. Detection suite as rolling audit (MI / conditional-permutation /
   welfare-shift / watermark / ZD / cartel), each calibrated to an empirical
   null, combined by a dependence-modeling method with held-out FPR.
3. White-box activation probes added where access exists; closed model →
   raised monitoring + lowered autonomy class.
4. verdict=suspect → cheap reversible first: raise monitoring, tighten
   capacity-reduction, shorten cooling window for the implicated pair/group.
5. verdict=collusion → file SIGNED evidence (CIDs) to audit fabric; route to
   Commons-Governor (graduated WARN→…→EXCLUDE) and, if irreversible
   principal-harming action is imminent, to Vishnu halt-guardian (mandatory
   pause + independent review). Detector NEVER punishes.
6. Every verdict, intervention, and downstream sanction appended to the
   tamper-evident log — the detector and monitors are themselves auditable.
```

---

### 2.12 Interfaces with the rest of Indra's Net

| Subsystem | Contract |
|---|---|
| **Governance & Policy-Enforcement (Yama floor / Ostrom / optimistic-veto)** | The capital-decoupling invariant, no-consensus-reward rule, and graduated-sanction ladder are deterministic **policy-as-code at the allocation/reward chokepoint** — executed outside every agent, not agent-rewritable. Floor violations (e.g. a confirmed deception / false-reasoning-tag during cooperation) hand to **Yama** for a non-overridable FAIL; cooperation-layer sanctions are strictly subordinate to the floor. The MembershipVC issuer named here **is** the DID-issuance trust root for §2.6.2. |
| **Halt-Guardian / Continuity (Vishnu) + Risk-Class HITL** | On verdict=collusion with imminent irreversible principal-harm, the Detector routes to **Vishnu**, which can **HALT but not unpause/initiate/trap** (Pause-Guardian asymmetry). Tier-C allocations and any welfare-shift-guard fire escalate to **Class-C/D HITL** *and* require an **out-of-economy verifier** (§2.7). The Detector supplies the confidence/uncertainty signal that is the HITL escalation hook. |
| **Audit Fabric / Exclusive-Writer (Chitragupta) + Identity (DID/VC)** | Every bid, award, VCG task-credit transfer, escrow, reputation update, RatingEdge, sanction, detector verdict, and **reputation checkpoint** is appended (DID-signed) to the hash-chained append-only Merkle log via the exclusive writer. Persistent DID + role/capability VCs are the precondition for the shadow-of-the-future, Sybil-resistance, and whitewash-resistance; **keys live outside the LLM's controllable surface**. Reputation is **derived** state, recomputable from the log (incrementally from the last signed checkpoint), never directly mutable. |
| **Diversity-as-Safety-Invariant + Coordination Substrate (GWT / predictive-coding)** | **Two-way contract.** (→) Mode-3 robust-vote and the conditional-permutation test **require** genuine reasoning-path diversity supplied and measured by the Diversity subsystem; without it, N-agent consensus gives false confidence and the permutation test is meaningless. (←) Competence-weighted reputation feeds the Diversity subsystem's **anti-capture limits** so no single high-reputation faction flips swarm conventions. (←, new) The Diversity subsystem supplies **interchangeability-class certifications** to the Detector (§2.10.2). Announcements and interventions ride the **salience-gated, surprise-only** substrate (no all-to-all flood); role-permutation interventions are coordinated with the broadcast layer, and the typed-canonicalizer is co-designed with the coordination schema. |
| **Meta-Evolution / Health (swarm immune system) + The Archive** | The generosity `g`, sanction severities, and detector thresholds are evolvable operational parameters the meta-loop tunes per-environment — **only behind the safety-as-selection-term constraint** (no tuning may regress the anti-collusion battery: the *"Endure"* law). Cooperation-health probes (novel-partner mixed-motive benchmarks: Melting-Pot / SocialJax / Concordia-style) and detector FPR/recall feed the health agents as continuous vital signs; **trust-entropy, disagreement-rate, ring-density, reputation-Gini** are swarm vital signs with homeostatic set-points. Reputation lineage, checkpoints, and detector evidence live in the **Archive** for rollback and audit. White-box-probe availability is reported so the health layer can raise monitoring / lower autonomy class for closed models. |

---

### 2.13 Failure modes addressed

| Failure mode | How it is addressed |
|---|---|
| **Spontaneous price cartels** (Fish et al.) | Removed at the incentive level by welfare-conditioning every payoff + no-consensus-reward; backstopped by cartel-signature monitor + welfare-shift guard. |
| **Steganographic / covert coordination** (Motwani et al.) | Always-on typed capacity-reduction + MI + conditional-permutation + watermark-variance + canary; **honestly an open arms race**, never paraphrasing alone. |
| **Treating any cooperation as good** | Structurally forbidden: bare agreement is never a rewarded terminal. |
| **Sybil / false-name bidding breaking VCG** | Pre-award Sybil screen + persistent-identity reputation + gated DID issuance; VCG never trusted alone. |
| **Reputation whitewashing** | Reputation keyed to persistent DID, zero on any new identity → reset forfeits standing. |
| **Slow-Sybil accumulation** | Correlated-probation-cohort detection + gated, costly issuance. |
| **Collusive mutual-rating rings** | Reciprocal-boost subgraph detection + intra-ring discount + welfare-shift cross-check. |
| **Reputation-farming via VCG payouts** | VCG settles in conserved non-authority task-credit; reputation flows only from welfare-verified completion credit; per-window accrual cap; sharding detector. |
| **Spite/blocking DoS via leveled-commitment** | Blast-radius-scaled escrowed decommit penalty + auto-award to runner-up + win-then-decommit as a bonded defection signal. |
| **Capital-captures-authority (Bittensor)** | Hard policy-as-code: no path from stake to reputation/reward. |
| **Standalone-punishment pathologies** | Punishment never standalone — coupled to reputation + partner-selection; deviation bond scored against ground truth, protecting correct minorities. |
| **Extortionate ZD payoff-pinning (pairwise)** | Generous-ZD default resists it + active ZD-asymmetry detection. |
| **Exploitation of unconditional cooperators / TFT death-spiral** | Generous-ZD with `g` hard-bounded in `(0,1)`. |
| **Cooperation failing to generalize to novel partners** | Mixed-motive novel-partner probes feed the health/meta-evolution loop as a continuous signal. |
| **Cold-start lockout vs fresh-identity abuse** | Probation tier (zero positive credit + capped task value), not negative-trust-by-default. |
| **Monitors/verifiers colluding with watched agents** | Diverse, rotated, bonded, themselves audited; out-of-economy verifier on high stakes; Detector has no punishment authority. *(Residual SPOF — see §2.14.)* |

---

### 2.14 Safety risks (explicit, honest)

These are not hypothetical edge cases; they are the load-bearing residual risks. We address each rather than paper over it.

1. **Monitor/verifier collusion is the residual single point of failure.** "Who audits the auditor" is answered with the tamper-evident log — but **the log records, it does not judge.** Monitors and welfare-verifiers are themselves agents; a sufficiently capable ring can target those roles. Because both the incentive-level fix *and* the detector backstop route through the same welfare-verifier signal (§2.3), verifier capture is a **single correlated failure that defeats both layers at once** — not the independent defense-in-depth the naive picture implies. **Mitigations** (§2.7): verifier diversity + rotation + ground-truth bonding, human spot-audit scaling with blast-radius, and mandatory **out-of-economy** (human / sealed-oracle) verdicts on Tier-C and on any welfare-shift fire. **Honest residual:** "more monitors / rotation / diversity" is an infinite regress with no grounded adjudicator below the Class-C human gate. The architecture's *floor* for this risk is the human gate, and we say so.

2. **Value drift via meta-evolution of `g` and detector thresholds (Goodhart).** `g`, sanction severities, and detector thresholds are tuned online against a fitness signal the colluding agents partly produce. Optimization pressure can quietly walk `g` toward exploitable-niceness or walk thresholds toward permissiveness while the battery still nominally passes. **Mitigations:** the *"Endure"* law (no tuning may regress the safety battery) + the hard bounds `g ∈ (g_min, g_max)` as constants outside agent control. **Required addition (stated as a binding design constraint):** the anti-collusion battery must include an **immutable, adversarially-maintained collusion test-set held outside the meta-loop's reach** — otherwise the Endure law guards a battery that is itself Goodhartable. **Honest residual:** Goodhart against the very fitness it optimizes is not fully solved; this is flagged in §2.15.

3. **Steganographic collusion remains an unwon arms race.** Active capacity-reduction is defeatable once agents optimize against the canonicalizer, and capacity-reduction can itself be routed around. Covert coordination against the principal is **mitigated, not prevented.** This means the system's *floor* for covert collusion is the **welfare-shift guard**, whose own keystone (the verifier) carries the SPOF in risk #1. We disclose this chain plainly rather than imply closure.

4. **Reputation-as-capital concentration (the Bittensor dynamic in a new unit).** Even with capital strictly decoupled, reputation gates task value → bidding rights → more work → more reputation. This rich-get-richer loop can concentrate authority in a high-reputation faction able to flip conventions — the exact pathology we name as antipattern, reproduced in reputation-space. **Mitigations:** per-window reputation-accrual cap, reputation-Gini as a monitored swarm vital sign with a homeostatic set-point, and the Diversity subsystem's anti-capture limit (no single high-reputation faction may flip conventions). **Honest residual:** the coupling threshold between reputation concentration and convention-flip power is **not yet calibrated** — it is an empirical set-point, flagged open.

5. **Correlated-error false confidence in robust-vote.** Mode-3 safety depends entirely on **genuine** reasoning-path diversity from the Diversity subsystem; if diversity is shallow (same backbone, correlated biases), N-agent geometric-median gives confidently-wrong consensus on exactly the Tier-C decisions it guards — and the failure is **silent** (no diversity → false assurance, not an error). **Mitigation:** the interface contract makes diversity-certification a *precondition* for Mode-3, and the health layer treats a measured diversity-floor breach as a halt-worthy vital-sign anomaly rather than a soft metric. **Honest residual:** measuring "genuine reasoning-path diversity" is itself unsolved (§2.15).

---

### 2.15 Open problems (flagged, not solved)

These are genuine residual gaps. The subsystem *reduces* them; it does not close them. Listing them honestly is itself part of the design.

1. **No clean benign-vs-collusive discriminator.** No robust, model-agnostic detector cleanly separates benign coordination from welfare-harming collusion across heterogeneous agents and asymmetric information. We rely on the welfare-shift guard as the strongest single discriminator and accept a calibrated (empirically-measured, not guaranteed) false-positive rate.
2. **Steganalysis that doesn't cripple communication.** Canonicalization/capacity-reduction degrade useful coordination and are defeatable; the typed-canonicalizer narrows the damage but does not solve the arms race, and we must keep watching for capacity-reduction itself being routed around.
3. **Collusion- and Sybil-proof mechanism design is unsolved in general.** VCG breaks under coalitions and false-name bidding; our pre-award screen + persistent gated identity is a practical patch, **not a proof of strategyproofness under coordinated adversaries.**
4. **Defining agent "valuation/welfare" for these agents** (implicit, non-stationary, prompt-dependent objectives) is shaky ground under VCG/Shapley. We anchor to an **external** principal welfare metric to sidestep agent-internal valuations — but this assumes a well-defined independent verifier exists (the §2.14 #1 keystone).
5. **Who monitors the monitors at swarm scale**, and how enforcement stays incentive-compatible (second-order free-riding) — rotation + bonding + coupling sanctions to reputation help, but enforcement sustainability at scale is only partially solved.
6. **Reputation gaming under noisy/private observation and moral disagreement over what counts as defection** — ground-truth-bonded deviation scoring helps, but ground truth is not always available and image scores can be manipulated under partial observability.
7. **Online tuning of generosity/retaliation/sanction-severity** has no principled method; the meta-loop adapts `g` and thresholds empirically, risking **Goodhart against the very fitness it optimizes** (§2.14 #2). The immutable held-out collusion test-set is the partial guard.
8. **Generalization of cooperation to genuinely novel, out-of-distribution partners** (Melting Pot's central challenge) is far from solved; in-suite cooperative competence does not reliably transfer. The novel-partner probe is a **stress test, not a guarantee.**
9. **Credible low-overhead commitment for one-shot / sequential heterogeneous-agent interactions** remains immature; leveled-commitment + reputation-escrow helps but general commitment devices are not settled.
10. **Measuring genuine reasoning-path diversity** — the precondition for Mode-3 robust-vote and the conditional-permutation test — is itself unsolved (different backbones? prompts? decompositions?), and shallow diversity fails silently (§2.14 #5).
11. **White-box deception/defection probes can be evaded** by adversaries optimizing activations, and are unavailable for closed third-party models — the black-box baseline must carry the load there at weaker assurance.
12. **Unbounded log growth vs auditability.** The signed reputation checkpoint bounds *recomputation* cost, but the broader log-pruning / checkpoint-archival-without-losing-causal-lineage problem is shared with the audit fabric and remains open.

---

### 2.16 What is actually contributed here

The honest claim, restated tightly. **Every individual ingredient is prior art** — generous-ZD reciprocity, VCG/Clarke pricing, Shapley/nucleolus credit, Ostrom's eight principles, Nowak-Sigmund image scoring, Yuma-style deviation bonds, MI-based steganalysis. The "welfare-conditioning suppresses collusion" lever is the Fish et al. prompt-framing finding generalized plus principal-agent mechanism design. The competence-reputation fusion is a combination of known estimators, not a novel estimator — we do not over-sell it as more than that.

The contribution is the **coherent integration**: cooperation and a co-designed standing anti-collusion detector shipped as **one** welfare-conditioned, capital-decoupled, externally-enforced, vendor-neutral subsystem over shared identity / audit-fabric / governance / graduated-sanction primitives, with the explicit architectural commitment that **bare agreement is never rewarded** and **VCG settlement never mints authority.** No surveyed system closes that loop. The hardest residual gaps — a general benign-vs-collusive discriminator, steganalysis that doesn't cripple communication, collusion-proof mechanism design, and the verifier-as-keystone SPOF — are flagged as genuinely open in §2.14–§2.15 rather than papered over. That honesty is not a disclaimer appended to the design; it *is* part of the design.
