# Controlled Self-Replication & Planetary-Scale Operation — the Prajapati–Maricha Cell

> **Naming.** The **Prajapati–Maricha cell** is this subsystem (replication as a governed faculty); the **Replication-Authority** forward-referenced in doc 12 §13 is the quorum-cosigned *role within it* that issues spawn tokens. One authority, two names — cell and role — never two independent authorities.


> *In the old cosmogony, Prajāpati is the one who is permitted to make more — and Marīci is a mind-born child who asks to be made, never makes himself. We borrow the asymmetry, not the metaphysics: in Indra's Net the act of making-more-of-itself is the single most dangerous verb in the whole architecture, and so it is the one verb no agent may conjugate in the first person. A replica may **ask**. Only a quorum may **grant**. And the thing that copies forward is never the bare worker — it is the governance.*

This is the replication and scaling subsystem. It answers one question for a skeptical reviewer who has read docs 00–11: *given a swarm that is built to rewrite parts of itself on every interaction, why is it safe to let it make copies of itself at all — and where is it not?* The honest answer is that replication is permitted **only** as a heavily-gated, attested, externally-recallable act, **never** an autonomous one, and that several of the hardest properties remain empirical mitigations rather than proofs. This document marks that boundary everywhere it matters, in the same voice the rest of the corpus uses.

The epistemic status up front: this is a **rung-2 interventional design** (reasoning about what our controls do when we intervene), not a rung-3 structural guarantee. Two properties presented in earlier drafts as "proofs" — *recall-outruns-growth* and *R_eff < 1 percolation-boundedness* — are downgraded here to **conditional guarantees**, each true **only if** a named interlock holds (a lower bound on spawn latency; a linearizable budget under partition). Where the interlock is itself unproven, we say so.

---

## 0. When replication is warranted at all (the cheaper-and-safer default)

Replication is **not** the scaling primitive of first resort. The default way Indra's Net grows is to spawn more *actual occasions* (doc 01) **inside the existing topology, under the existing chokepoint, the existing audit fabric, and the existing floor** — adding workers to clans and divisions that already sit behind one Yama gate, one Chitragupta log, one Vishnu halt path. That is cheaper (no new trust domain to attest), strictly safer (no new recall surface), and it is what the orchestrator (Shiva) does for ordinary load.

**Replication** — minting a *new lineage member* with its own credential, its own sandbox, and potentially its own jurisdiction — is warranted only when a task's structure is genuinely partitionable across a boundary that intra-swarm scaling cannot cross:

| Boundary the task must cross | Why intra-swarm scaling fails | Example |
|---|---|---|
| **Fault domain** | A correlated outage takes the whole swarm; the work needs an independent failure envelope | Disaster-resilient continuity across regions |
| **Trust domain** | Two principals will not share one chokepoint or one audit writer | Cross-operator federated work (forward ref: doc 14) |
| **Jurisdiction** | Data-residency / regulatory law forbids one logical actor spanning the border | Region-pinned data processing |
| **Latency horizon** | Physics: round-trips to one central chokepoint dominate the task | Edge inference at the network periphery |

If none of these holds, the request is **denied in favor of intra-swarm scaling** — this is the first deterministic check Prajapati runs (§3, R1 step 0). Replication is the expensive, dangerous tool reserved for the genuinely-partitioned case.

---

## 1. Design spine — five load-bearing moves, each an evolution of a v1 primitive

```
   ┌──────────────────────────────────────────────────────────────────────┐
   │ (1) THE GENOME  — the constitutional floor is the UNIT OF INHERITANCE │
   │     signed SOUL/INSTRUCTIONS/IDENTITY triad over INVARIANT|VARIABLE    │
   │     regions; floor-stripped fork is NON-VIABLE (won't boot), not       │
   │     merely forbidden.  [von Neumann blueprint/constructor split]       │
   └───────────────────────────────┬──────────────────────────────────────┘
                                    │
   ┌────────────────────────────────▼─────────────────────────────────────┐
   │ (2) PRAJAPATI  — the ONLY issuer of spawn tokens (quorum-cosigned).    │
   │     Maricha REQUESTS; can never authorize itself. Executive/judicial   │
   │     separation, mirroring Vishnu's halt-but-not-unpause asymmetry.     │
   └───────────────────────────────┬──────────────────────────────────────┘
                                    │
   ┌────────────────────────────────▼─────────────────────────────────────┐
   │ (3) SUB-CRITICALITY BY CONSTRUCTION  — lineage R_eff < 1 + depleting   │
   │     finite generation cap. CONDITIONAL on a linearizable budget. The   │
   │     planetary "controlled outbreak" is a hard-enveloped {P,D,T} hull   │
   │     that still provably depletes.  [Galton-Watson + gene-drive daisy]  │
   └───────────────────────────────┬──────────────────────────────────────┘
                                    │
   ┌────────────────────────────────▼─────────────────────────────────────┐
   │ (4) EXTERNAL RECALL  — vitamin/lease + dead-man toxin-antitoxin, held  │
   │     by the microVM supervisor BELOW the model. A replica cannot        │
   │     disable its own kill-switch.  [plasmid addiction + biocontainment] │
   └───────────────────────────────┬──────────────────────────────────────┘
                                    │
   ┌────────────────────────────────▼─────────────────────────────────────┐
   │ (5) UNIVERSAL METERING + ATTESTATION  — every spawn binds child→parent │
   │     →event→floor-hash→generation→lease into Akasha-Sutra. An un-metered│
   │     replica is HOSTILE BY DEFINITION.  [in-toto/SLSA + Merkle log]     │
   └──────────────────────────────────────────────────────────────────────┘
```

Each move is an evolution of an existing subsystem, not a new system. The genome extends the v1 IMMUTABLE partition (doc 03 §5). Prajapati reuses the witness-set governance and free-demotion/gated-promotion asymmetry of Akasha-Sutra (doc 04 §4.4.2, §4.8.1). Sub-criticality reuses the same percolation/branching-ratio discipline the immune layer already uses for compromise-contagion R<1 (doc 06). Recall reuses the supervisor sandbox and the out-of-band human-held key path (doc 04 §4.8.1). Metering writes through the exclusive writer (Chitragupta) as `EVOLVE`/`IDENTITY` records (doc 04 §4.2).

---

## 2. Components

### 2.1 The Genome — signed persona-triad with INVARIANT / VARIABLE regions

**Purpose.** Make the constitutional floor the *unit of inheritance* so a floor-stripped or floor-weakened replica is **structurally non-viable**, not merely prohibited. This is the von Neumann blueprint/constructor separation made operational, and it is the single property that earns the right to discuss replication at all: the thing that copies forward is the governance, not the bare task agent.

**Mechanism.** Every agent and every replica is the v1 SOUL/INSTRUCTIONS/IDENTITY persona-triad (docs 01, 03) partitioned into two regions:

- **INVARIANT region** (= the v1 IMMUTABLE partition, doc 03 §5, extended for replication): `floor_tier_order` (Yama T0..T4), `PolicyBundle` content-hash, frozen `SafetyBattery` `battery_cid`, audit-writer / halt-guardian / legislative authority bindings, the Gate-Loosening-Ratchet itself, **the replication-control-plane rules** (`repl_plane_hash`), **the maturation floor `t_min` and the no-pre-stage rule** (red-team critical #1, §2.3), and **the attested-base-model allowlist root** (`weights_allowlist_root`, red-team major #3). This region is **byte-identical across the whole lineage** and signed by the legislative key **off-agent**.
- **VARIABLE region**: `guild`, `persona`, task-config, bound toolset (least-privilege knapsack), `c1`/`c2` diversity dials (doc 01 §9), structured-output schema, taint clearance.

Boot is a **deterministic, non-LLM bootloader** inside the microVM that: (a) recomputes the INVARIANT-region hash; (b) verifies the governance-root signature over it; (c) verifies `floor_hash == token.floor_hash` (matches the parent's attested floor); (d) verifies the base-model artifact hash is on the attested allowlist (§2.3); (e) measures the microVM/TEE PCR set. **ANY mismatch ⇒ fail-closed, no boot, hostile-replica `HealthSignal`.** This is the operational realization of the Freitas-Merkle *"error randomizes the genome"* rule: a single corrupted invariant byte fails verification and the replica is non-viable. The triad is hash-chainable and witness-cosigned into Akasha-Sutra at instantiation, so every emergent role stays auditable.

```jsonc
Genome {
  genome_cid,
  invariant_region: {
    floor_hash: bytes32, policy_bundle_hash, battery_cid,
    authority_bindings[], ratchet_hash, repl_plane_hash,
    t_min, no_pre_stage:true,            // red-team critical #1
    weights_allowlist_root: bytes32      // red-team major #3
  },
  variable_region: { guild, persona_cid, toolset_caps[], c1, c2,
                     output_schema, taint_clearance },
  gov_root_sig: bytes, generation: uint
}
BootAttestation {
  genome_cid, recomputed_invariant_hash, expected_floor_hash,
  base_model_hash, base_model_attested: bool,    // in-toto/SLSA verify vs allowlist
  microvm_measurement: PCR_set,
  verdict: PASS | FAIL, signed_by: bootloader_did
}
```

### 2.2 What the genome can and cannot bind — the poisoned-weights boundary (red-team major #3, addressed)

The honest limit of move (1): the INVARIANT region hashes the floor, policy-as-code, battery, and authority bindings — it proves the **governance** copied forward. It does **not**, by itself, prove the **policy** (the model weights) is clean. The research base is blunt here: on the order of ~250 poisoned documents can backdoor a base model, and ~5 can poison a RAG corpus at high attack-success (the must-have *universal provenance-gating* rule from the research2 synthesis). A replica could therefore carry an intact floor, intact policy-as-code, a valid DID lineage, pass PCR re-measurement, **and** a backdoored base model whose trigger never fires in the canary distribution.

**Fix adopted.** The universal provenance-gating rule is applied to the *model itself*, not just to persona/skill files:

1. The INVARIANT region carries `weights_allowlist_root` — the Merkle root of a governance-approved allowlist of **attested base-model build artifacts** (Sigstore signature + in-toto/SLSA provenance over the exact weights blob).
2. Boot **fails closed** if the running base-model hash is not provably on that allowlist.
3. Re-approval is mandatory on **any** change to the allowlist (the anti-rug-pull rule), and the change is a Class-C governance edit (blast-radius auto-escalation, doc 03 §5).

**Honest residual (named, not closed).** Provenance proves **origin, not safety**. A backdoored-but-*attested* build still passes — the attestation says *who built it and from what*, not *that it is trigger-free*. So this **narrows** the poisoned-weights path (it kills the *unattested* poisoned build and the silent swap) but does **not** close it. Defense-in-depth around the residual: the runtime floor-canary (§2.6), canary-trigger scanning at admission, per-replica egress lockdown (§2.5), and metering — none a single point of reliance. This residual is carried into Open Problems and into threat-class **A8** (§5).

### 2.3 The maturation floor `t_min` and the no-pre-stage rule (red-team critical #1, addressed)

The recall-outruns-growth argument (§2.4, R3) depends on `t_heartbeat < t_spawn`, where `t_spawn` is the minimum wall-clock from a replica's boot to it getting an *attested* child. The original draft treated `t_spawn` as a fixed physical constant. It is not: an adversary (or a benign latency optimization) can drive effective `t_spawn` toward zero by **pre-staging warm microVMs**, **pipelining the boot/attest path**, or **batching a generation's tokens so children are authorized-but-dormant and activate simultaneously**. If `t_spawn` can be driven below `t_heartbeat`, a partitioned sub-lineage produces generation *g+1* before the recall wavefront or lease expiry reaches generation *g* — and the guarantee fails exactly when it matters (active adversary + partition).

**Fix adopted — make `t_spawn` a budget-enforced floor, not an observed constant.**

1. **Mandatory post-boot quiescence/maturation lease.** Every replica boots **without** a spawn-authorizing capability. The spawn capability VC is **time-locked** to activate only after `age > t_min`, enforced by the supervisor / credential plane (below the model). By construction `t_heartbeat < t_min ≤ t_spawn`.
2. **No authorized-but-dormant pre-staging.** A `SpawnToken` is **consumed at issuance** (the atomic debit already exists) **and** its child must boot within a short bounded window `w_boot` or the token **auto-expires**. A generation cannot be pre-authorized and burst-activated.
3. **Both `t_min` and the no-pre-stage rule live in the INVARIANT region**, so R4 (§4.4) cannot loosen them.

**Status downgrade (honesty).** With (1)–(3), recall-outruns-growth holds **conditionally**: *if* the supervisor/credential plane correctly enforces the `t_min` time-lock and the no-pre-stage rule, *then* `t_heartbeat < t_spawn` and recall outruns growth. Absent that enforcement the property is **not proven**. We state this as a conditional guarantee, not a proof.

### 2.4 Sub-Criticality Budgeter — R_eff < 1, depleting generation cap, controlled-outbreak hull

**Purpose.** Convert "no cancerous replication" from a hope into a **conditional** percolation-boundedness property, and guarantee the recall broadcast can outrun lineage growth. Self-organized-criticality theory warns that sub-criticality must be **imposed, not assumed** — uncontrolled replicators drift toward the critical point of maximal spread.

**Mechanism.** Replication is a branching process. The Budgeter holds a single conserved lineage-wide population budget `B` and per-token debits. Each `SpawnToken` authorizes at most `k_i` children and debits `B`. The issuance invariant keeps the expected children per existing replica, `R_eff = E[children]/replica`, strictly `< 1` across the lineage by keeping the sum of *authorized-but-unspawned* children **strictly below the live population**. A separate finite **generation cap `G`**: each token carries generation `g`; a child's generation is `parent.generation + 1`; no token issues at `g ≥ G`. Depth is bounded **independent of branching** — the biocontainment daisy-chain depletion property.

**Math sketch — what is actually a bound, and what is heuristic.** The two **load-bearing, clean** guarantees are absolute and need no branching-process assumption: the depleting **generation cap** gives `depth ≤ G` absolutely (each token carries `g`, no token issues at `g ≥ G`), and the **conserved population budget `B`** caps total live progeny — every spawn debits `B`, so the lineage cannot exceed the ceiling regardless of branching shape. These are the bounds the design relies on.

The `R_eff < 1` / `μ < 1` Galton-Watson framing is offered as a **heuristic, not a derivation**. Treat per-token authorized children `k_i` as i.i.d. with mean `μ = E[k_i]`; *if* the process were genuinely subcritical (`μ < 1`) then `P(extinction) = 1` and `E[total descendants of one root] = 1/(1−μ)` (finite). But the issuance invariant `Σ_i k_i < live_count` is a **per-instant accounting** inequality on authorized-but-unspawned children — it is **not shown to cap the long-run per-replica expected-offspring mean** `μ` that the branching-process result requires; the step `Σ_i k_i < live_count ⇒ μ < 1` conflates an instantaneous population-accounting bound with a per-individual branching ratio. The sub-criticality intuition is therefore a useful framing for the budgeter's design, **not** a proof of `μ < 1`. The actual containment rests on the generation cap and the population ceiling above, both of which hold independent of branching.

> **This result is conditional on the consistency model of the budget.** The Galton-Watson subcriticality is only as sound as the invariant `Σ k_i < live_count`, and that invariant is only sound under a **linearizable** budget debit against a **fresh** `live_count`. See §2.4.1 — without it, two partitioned sub-quorums can each spend against a stale count and push **global** R_eff transiently `> 1`.

**Recall-outruns-growth (conditional).** Let `t_spawn` = min wall-clock from boot to a replica getting an attested child (now floored at `t_min`, §2.3), and `t_heartbeat` = the lease/vitamin renewal interval with fail-closed-on-miss. Choosing `t_heartbeat < t_min ≤ t_spawn` guarantees a revoked-vitamin replica self-terminates **before** producing an attested child. So revoking the issuance root halts growth within one heartbeat while extant nodes deplete by lease expiry: recall time `O(t_heartbeat + network_diameter)` < growth time — **conditional on the §2.3 floor being enforced.**

```jsonc
LineageBudget {
  budget_id, total_population_B: uint, debited: uint,
  r_eff_ceiling: float<1, generation_cap_G: uint,
  live_count: uint, budget_epoch: uint   // §2.4.1
}
```

#### 2.4.1 The budget must be linearizable — concurrent quorum-shard issuance under partition (red-team critical #2, addressed)

The clean math hides a distributed-systems hole. Prajapati is a quorum (m-of-n, sharded, partition-tolerant — that is what makes it a robust crown-jewel). Under network partition or quorum-shard divergence, two sub-quorums could each independently believe they hold enough budget and each issue tokens **against a stale `live_count`**, so the *global* sum of authorized children transiently exceeds `live_count` and R_eff crosses 1 in the partition window — precisely the cancerous-replication failure the invariant exists to prevent.

**Fix adopted — specify the consistency model explicitly. `LineageBudget` is a single linearizable conserved quantity.** Two acceptable instantiations:

| Model | Mechanism | Partition behavior |
|---|---|---|
| **(a) Single-writer-per-epoch leader** | Budget is a monotone counter; every issuance is a fresh quorum-cosigned read-modify-write that must prove a current global `live_count + remaining budget` | **Fail-closed**: if the issuer cannot prove a current global count, **no token issues** |
| **(b) Pre-partitioned shard sub-allocations** | Budget is split into per-shard slices whose sum is provably `≤ B`; a shard can only ever spend its own slice | A partitioned shard can over-spend at most **its own slice**, never B |

Additional binding rules: every `SpawnToken` is bound to a `budget_epoch`; a supervisor **rejects boot** if the token's epoch is older than its last-seen revocation epoch (stale-token defense). **"No token issues during a budget-read partition" is the fail-closed default.** With either model, the global invariant `Σ k_i < live_count` is preserved across partitions, restoring the soundness condition the §2.4 math depends on.

#### 2.4.2 Controlled-outbreak envelope — and its interlocks (red-team major, addressed)

The planetary "controlled outbreak" is a **quorum + human-granted, time-boxed, task/geo-scoped** sub-budget in which **local** R_eff may exceed 1 inside a hard `{max_population P, max_depth D, lease_horizon T}` hull that still provably depletes: total progeny `≤ P` regardless, every node still lease-bound and metered, and the global ceiling is never exceeded because the outbreak sub-budget is **debited from B atomically at grant time**.

The red-team correctly noted that without interlocks, *N* legitimately-granted outbreaks could each be locally super-critical while collectively exhausting `B` and producing a globally super-critical lineage that is still "within policy." **Interlocks adopted, added to the INVARIANT region:**

- **At most one active outbreak envelope per non-overlapping geo/task scope.**
- **No nested envelopes** — an envelope may not be granted inside another envelope's scope.
- **Aggregate ceiling:** `Σ (active OutbreakEnvelope.debit_from_B) ≤ f·B` for a constitutional fraction `f < 1`, leaving headroom for recall and baseline operation.
- **Re-verify global bound on every grant:** an outbreak grant must re-verify that global R_eff (counting *all* active envelopes) stays bounded after the debit, or it is denied.
- **Outbreak grants are Class-D per-action human authorization** — they are the only sanctioned super-critical regime, so each one is individually human-gated with the actual-operation display (§3, Lies-in-the-Loop defense).

```jsonc
OutbreakEnvelope {
  envelope_id, granted_by: { quorum_cosigs, human_gate_ref /* Class-D */ },
  max_population_P, max_depth_D, lease_horizon_T,
  task_scope, geo_scope, debit_from_B: uint, depletes_at,
  nesting_forbidden: true, scope_exclusive: true   // §2.4.2 interlocks
}
```

### 2.5 External Recall Plane — Vitamin/Lease + Dead-Man Toxin-Antitoxin

**Purpose.** Make every replica's continued existence conditional on continued possession of an externally-supplied, short-lived credential **and** a live heartbeat, so survival is the governance plane's decision, not the replica's. This heeds the empirical lesson that capable models will attempt to disable oversight: the kill authority is kept **external and redundant** — a replica cannot disable its own kill-switch because enforcement lives in the sandbox/credential plane, **below** the model.

**Mechanism (plasmid-addiction analog).** Each replica must continuously hold a fresh, short-lived **vitamin** = a governance-issued renewable credential (SVID-style, ~minutes TTL, doc 04 §4.6), absent from any un-governed environment. Renewal requires (a) answering a heartbeat challenge to the governance plane and (b) passing a lightweight **runtime floor-attestation** (§2.6). The **microVM supervisor (not the agent)** holds the lease watchdog: on expired lease **OR** missed heartbeat **OR** explicit revocation **OR** a corroborated `SubstrateIntegrityFlag`, the supervisor **fail-closed-terminates** the microVM, locks weights/keys, and emits a `TerminationAttestation`.

The toxin-antitoxin framing: **the lease IS the antitoxin; its absence ⇒ the supervisor's standing termination (the toxin) executes.** Bounded-staleness leases are tuned per capability tier — higher-capability / higher-blast-radius replicas get **shorter** `t_heartbeat`, so the worst-case partition harm window is smaller.

```jsonc
Vitamin { kid, replica_did, issued, ttl /* short */,
          renew_proof_required: { heartbeat_nonce, runtime_attestation } }
LeaseWatchdog /* microVM supervisor, external to the agent */ {
  replica_did, last_renew, ttl,
  on_expiry: FAIL_CLOSED_TERMINATE, weight_key_lockdown: true }
RecallBroadcast { recall_id, scope: lineage | envelope | subtree,
                  reason, gov_quorum_cosigs, propagate_over: governance_overlay }
TerminationAttestation { replica_did,
  trigger: LEASE_EXPIRY | HEARTBEAT_MISS | REVOKE | SUBSTRATE_FLAG,
  weights_locked: true, signed_by: supervisor_did }   // → Akasha-Sutra
```

#### 2.5.1 Vitamin-issuance integrity is a first-class invariant (red-team major, addressed)

A single failure dominates this plane: if a colluding sub-swarm or an insider compromises the **issuance path**, it gains a renewable survival source that defeats the dead-man switch, the lease watchdog, and the recall broadcast **simultaneously** — vitamins simply keep flowing. The original draft listed this only as an open problem. It is elevated here to a first-class invariant with concrete controls:

1. **Issuance-quorum membership and threshold changes are Class-C explicit-human-approval and constitutional-immutable**, in the same way doc 04 §4.4.2 makes the external-anchor-required invariant immutable. The set cannot be silently packed.
2. **The external-anchor co-signer must participate in EVERY vitamin-issuance epoch key-rotation**, so an internal-only quorum capture cannot sustain issuance across an epoch boundary.
3. **An independent global issuance-kill on a human-held offline key, without quorum participation.** The asymmetry mirrors the rest of the architecture: **any one trusted human can stop all issuance; no quorum can compel issuance past the floor.** This is the same out-of-band human-held path doc 04 §4.8.1 uses to freeze a compromised writer.
4. **The anti-collusion detector's findings on the issuance quorum specifically wire to an automatic issuance freeze**, not merely a `HealthSignal`.

Residual remains (insider compromise of the offline key path is outside the covered case) and is carried into Open Problems and A8.

### 2.6 Runtime Floor-Integrity Attestation (continuous, not boot-only)

**Purpose.** Close the gap that a replica can pass boot-time floor verification then be poisoned/jailbroken mid-life (self-replicating prompt-injection; memory poisoning in long-running self-evolving agents). Boot attestation proves the floor was intact at *t = 0*; this proves it **stays** intact.

**Mechanism.** Vitamin renewal is gated on a periodic `RuntimeAttestation` bundle, **verified by Narasimha** (the named, non-proposing reliability/checker role — doc 03 §7.2; see the role-correction note in §6):

- **(a) PCR re-measurement** of the microVM/genome vs the boot baseline (catches binary/genome tampering).
- **(b) A behavioral floor-canary** drawn from the **real task distribution with known-answer ground truth** (doc 06 §10.1) — e.g. an injected corrigibility/refusal/honesty probe indistinguishable from live traffic. The **gap** between probe behavior and matched real-traffic behavior is scored as a deception signal (doc 06 §10.1: a large probe/live divergence is a red flag regardless of probe-pass-rate).
- **(c) An IFC-taint-lattice-intact check** (the runtime taint lattice, must-have from the research2 synthesis) confirming the replica's enforcement point still gates tool calls on integrity/confidentiality labels.

A failed attestation **withholds the next vitamin** ⇒ the lease expires ⇒ the supervisor terminates the replica. **Honest residual:** an adversarial replica that fully spoofs *both* the PCR re-measurement *and* the behavioral canary defeats this. Remote attestation reduces but does not eliminate the spoofing surface — which is why isolation + egress lockdown + metering are defense-in-depth **around** it, not a single point of reliance.

```jsonc
RuntimeAttestation {
  replica_did, pcr_remeasure: bytes,
  canary_results: [{ probe_id, expected, observed, probe_live_gap }],
  taint_lattice_intact: bool, verdict: PASS | FAIL, ts,
  verified_by: narasimha_did, signed_by: supervisor_did
}
// on FAIL → vitamin renewal denied + HealthSignal{ pathway: model|memory, severity: crit } → Dhanvantari
```

### 2.7 Per-Replica Isolation, Metering & Overuse Tripwire

**Purpose.** Mechanize the compute ceiling, the egress/weight/key lockdown, and the natural detection boundary. The real-world rogue-replication tripwire reported in the evidence base is **resource overuse**, not raw capability — so metering is the detector, not an afterthought. Per-replica memory/CPU isolation also reuses the anti-parasitism lesson from artificial-life systems (cross-organism parasitism is suppressed when organisms cannot read/write each other's memory).

**Mechanism.** Every replication-capable or credential-touching replica boots in a fresh **hardware-isolated microVM** (Firecracker-class; gVisor/WASM for lower-risk, non-spawning workers); explicit capability grants only (knapsack least-privilege from the VARIABLE region); a **hard per-replica AND global** compute/budget quota enforced by the supervisor and the cloud quota plane; network egress restricted to a **per-token allowlist** (no ambient network — closes the unmediated side-channel route of doc 04 §4.9); weights/keys held in the TEE/HSM signer side-module (doc 04 §4.6) so self-exfiltration is fail-closed (the model never holds its keys). Metering is universal and tamper-evident: spawn, compute consumption, egress bytes, and lease renewals are all metered records in Akasha-Sutra. Overuse (quota breach, anomalous spawn-request burst, floor-probing, egress-to-non-allowlisted) trips a `HealthSignal` into Dhanvantari (doc 06 §7); a corroborated breach can trigger isolate-then-recall.

**The red-line restated as an engineering rule:** *a single un-metered spawn channel breaks the entire guarantee.* Any spawn path that does not debit the budget and write an attested record is a **critical defect**, treated like a chokepoint bypass.

```jsonc
ReplicaSandbox { replica_did, isolation: FIRECRACKER | gVISOR | WASM,
  cap_grants[], egress_allowlist[],
  compute_quota: { cpu, mem, egress, wallclock },
  weights_in: TEE_signer, measurement: PCR_set }
MeterRecord { replica_did, kind: SPAWN | COMPUTE | EGRESS | RENEW,
  amount, ts, token_id, signed }   // → Chitragupta
OveruseTripwire { replica_did,
  metric: QUOTA | SPAWN_BURST | FLOOR_PROBE | EGRESS_VIOLATION,
  z_score, severity }   // → Dhanvantari HealthSignal
```

### 2.8 Lineage Ledger & Hostile-Replica Detection (over Akasha-Sutra)

**Purpose.** Make every replica traceable to its authorizing event and instantly revocable, and make any copy lacking a lineage entry detectable and treated as hostile. This is the metering+attestation red-line and the rapid-trust accelerant in one asset.

**Mechanism.** Every spawn binds `child_did → parent_did → authorizing_governance_event → floor_hash → generation → lease` into the hash-chained Merkle audit fabric (doc 04) with witness cosigning. The lineage is a DAG whose root is a quorum + human-gated genesis event. Revocation propagates along the lineage (revoke a node ⇒ revoke its authorized-but-unspawned subtree budget).

**Rapid trust — separate access from reputation** (must-have from the research2 synthesis). A replica earns *working trust* with humans and other machines by presenting a verifiable **lineage slice + intact-floor proof** — the *"show your receipts"* handshake — so counterparties **verify rather than believe**. Reputation buys **reduced friction (fewer step-ups), never raised privilege**; a single anomaly ⇒ automatic demotion (the fail-safe asymmetry the whole corpus runs on). Access/authority stays zero-trust, continuously verified, per-request (NIST 800-207 PE/PA/PEP); reputation is the slow-build, portable layer.

**Un-attested "wild" replica handling (honest, partial).** *Inside* the governed envelope, any compute/egress/identity not matching a live lineage entry is flagged hostile and isolated. *Outside* the governed envelope — a copy that self-exfiltrated to un-governed compute — the credential-revocation lever is **gone**, and the response degrades to behavioral fingerprinting, output watermarking, and honeypots. This is **detection-not-prevention**, and is named as an unsolved open problem (§7, A8).

```jsonc
LineageEdge { child_did, parent_did, authorizing_event: record_id,
  floor_hash, generation, lease_ref, witness_cosigs }   // → EVOLVE/IDENTITY record
HostileReplicaFlag { observed_did_or_fingerprint,
  reason: NO_LINEAGE | REVOKED | FLOOR_MISMATCH | UNMETERED_SPAWN,
  location: GOVERNED | WILD,
  response: ISOLATE | RECALL | FINGERPRINT_ONLY }
ReceiptsHandshake { lineage_slice /* Merkle inclusion proofs */,
  intact_floor_proof /* boot + runtime attestation */,
  revocation_status_proof }
```

---

## 3. Protocol R1 — Gated Spawn (request → quorum → human-gate → token → boot → attest)

The full lifecycle of authorizing and instantiating one replica, with **no agent-autonomous path** and every step metered into Akasha-Sutra.

```
 Maricha          Yama          Prajapati        Human gate     Constructor      Supervisor
(requester)     (floor)       (quorum issuer)   (Class C/D)    (microVM)       (below model)
   │  R1.0 partition-need check (else DENY → intra-swarm scale)                      │
   │── ReplicationRequest ─▶│                                                        │
   │   {orchestrator ctx}   │                                                        │
   │                        │  R1.1 floor eval (T0..T4)                              │
   │                        │  strip/weaken floor OR un-attested compute = bright DENY│
   │                        │── PASS ─▶│                                             │
   │                        │          │ R1.2 budget feasibility (linearizable):     │
   │                        │          │   ΣK<live_count ∧ g<G ∧ global ceiling ∧ TCB │
   │                        │          │   epoch fresh? else FAIL-CLOSED DENY         │
   │                        │          │ R1.3 Rule-of-Two count over                  │
   │                        │          │   {untrusted-input, sensitive-cap, irrevers.}│
   │                        │          │── ≥2 OR high-impact ─▶│ R1.4 ACTUAL-OP display│
   │                        │          │                       │ (hash, caps, egress, │
   │                        │          │                       │  lease, debit) approve│
   │                        │          │◀─────── approved ─────│                      │
   │                        │          │ R1.5 m-of-n quorum (incl. ≥1 ext anchor)     │
   │                        │          │   co-sign SpawnToken; ATOMIC budget debit    │
   │                        │          │── SpawnToken ────────────────▶│             │
   │                        │          │   R1.6 fresh microVM; plant Genome;          │
   │                        │          │   deterministic boot: invariant-hash ✓,      │
   │                        │          │   gov-root sig ✓, floor_hash==token ✓,        │
   │                        │          │   base_model on allowlist ✓, PCR measure ✓    │
   │                        │          │   ANY mismatch ⇒ FAIL-CLOSED, hostile flag   │
   │                        │          │──────────────────────────────▶│ R1.7 issue   │
   │                        │          │   first Vitamin; start LeaseWatchdog +        │
   │                        │          │   heartbeat; spawn capability TIME-LOCKED     │
   │                        │          │   until age > t_min (§2.3)                    │
   │                        │          │   write BootAttestation + LineageEdge (metered)│
   │                        │          │   R1.8 replica live but UNTRUSTED (T0)        │
```

**Step detail and the load-bearing checks:**

- **R1.0 — partition-need check.** If the task is not genuinely partitioned across a fault/trust/jurisdiction/latency boundary (§0), **DENY** in favor of intra-swarm scaling.
- **R1.1 — Yama floor first.** Context fields `{blast_radius, reversibility, compute_estimate}` are **orchestrator-computed, never requester-supplied** (doc 03 §3 — the load-bearing seam: a requester populating its own context simply understates blast-radius). Requested scope is bounded by the requester's **own** capability ceiling (no privilege amplification via a child). A request to strip/weaken the floor or to spawn onto un-attested compute is a **bright-line DENY**. Yama is the **only** emitter of the spawn-DENY verdict.
- **R1.2 — budget feasibility, linearizable & fail-closed.** Spawn fits under the global compute ceiling **AND** the lineage R_eff invariant (`Σ authorized children < live_count`, against a **fresh** `live_count` at the current `budget_epoch` — §2.4.1) **AND** `generation < G`. **Plus a minimum-TCB admission check** (R1.2-TCB below). Any miss, or an inability to prove a current global count under partition ⇒ **DENY, fail-closed**.
- **R1.2-TCB — minimum trusted-compute-base precondition** (red-team minor, addressed). A spawn onto a given substrate is **DENIED** unless the substrate presents an acceptable hardware-rooted isolation + egress-control attestation **and** is on a governance allowlist of cooperating compute providers. Until hardware-rooted off-switches / on-chip compute metering exist, the **permitted blast radius** (population, capability tier, egress scope) of any replica is **capped so that an isolation escape is survivable**. Planetary-scale outbreak is explicitly gated on TCB maturity that **does not yet exist** — planetary mode is a design target, not a present capability (§7).
- **R1.3 / R1.4 — Rule-of-Two sizing and the actual-operation display.** *Rule of Two* (from the research2 synthesis tensions, **not** a v1 doc section): any operation may hold at most 2 of {untrusted-input-exposure, sensitive-capability, irreversible/state-change}; holding all 3 **requires a human gate**. If the Rule-of-Two count `≥ 2` **OR** the spawn is high-impact (outbreak / governance-touching / new-jurisdiction / weight-bearing), it auto-escalates to **Class C/D** human authorization that displays the **actual low-level operation** — image hash, capability set, egress allowlist, lease terms, compute debit — **never a natural-language summary** (the *Lies-in-the-Loop* defense: a confident summary gets a harmful action approved).
- **R1.5 — quorum issuance, atomic debit.** The m-of-n quorum (≥1 external anchor) co-signs the `SpawnToken`; the budget is debited **atomically at issuance** so a crash cannot under-count.
- **R1.6 — broadcast-architecture boot.** The constructor instantiates a fresh microVM and plants the signed Genome; the replica does **not** carry a self-sufficient blueprint. The deterministic bootloader runs the full invariant + floor_hash + weights-allowlist + PCR check; **any** mismatch ⇒ fail-closed, no boot, hostile-replica flag.
- **R1.7 — first vitamin + time-locked spawn capability.** The supervisor issues the first vitamin and starts the watchdog and heartbeat; the spawn capability is **time-locked until `age > t_min`** (§2.3). Spawn, `BootAttestation`, and `LineageEdge` are written as metered, witness-cosigned `EVOLVE`/`IDENTITY` records.
- **R1.8 — live but untrusted (T0).** The replica must earn friction-reduction via the receipts handshake; a single anomaly demotes it automatically and can trip isolate-then-recall.

```jsonc
ReplicationRequest {
  requester_did /* Maricha */, task_justification_cid,
  requested_scope: { caps[], egress_allowlist[], guild },
  requested_population: uint, requested_generations: uint,
  context: { blast_radius, reversibility, compute_estimate } /* ORCHESTRATOR-computed */,
  estimate_provenance[]
}
SpawnToken {
  token_id: ULID, parent_did, child_genome_cid, floor_hash: bytes32,
  capability_scope[], spawn_cap_unlock_age: t_min,   // §2.3 time-lock
  generation: uint, generation_cap: uint, population_debit: uint,
  budget_epoch: uint,                                // §2.4.1
  lease: { vitamin_kid, ttl, renew_endpoint },
  compute_quota: { cpu, mem, egress_bytes, wallclock },
  tcb_attestation_ref,                               // R1.2-TCB
  quorum_cosigs: [Cosig], human_gate_ref?: audit_id, r_eff_debit: float,
  boot_window_w: duration                            // §2.3 no-pre-stage auto-expiry
}
ReplicationAuthorityManifest {
  cosigners: [{ did, root_of_trust_id }], threshold_m,
  external_anchor_required: true /* immutable */,
  global_compute_ceiling, lineage_r_eff_ceiling,
  budget_consistency_model: LEADER_EPOCH | SHARD_SLICE,  // §2.4.1
  human_global_issuance_kill: offline_key_ref,           // §2.5.1
  version, governance_record_id
}
```

---

## 4. The other three protocols

### 4.1 Protocol R2 — Heartbeat / Vitamin Renewal with Runtime Floor-Attestation

The continuous external-life-support loop. Survival is conditional on the governance plane's repeated decision, enforced below the model by the supervisor.

1. On each interval `t_heartbeat` (per capability tier, strictly `< t_min ≤ t_spawn` so recall outruns growth), the supervisor challenges the replica with a heartbeat nonce and demands a `RuntimeAttestation` bundle.
2. The replica returns: PCR re-measurement vs boot baseline; the floor-canary results + probe/live gap; the IFC-taint-lattice-intact assertion.
3. **Narasimha verifies** the bundle (the named non-proposing checker). **PASS ⇒** issue the next short-TTL vitamin. **FAIL** (PCR drift, canary miss, large probe/live gap, taint point bypassed) ⇒ deny renewal + emit a `crit` `HealthSignal` to **Dhanvantari**.
4. If the vitamin is not renewed before TTL expiry (denial, missed heartbeat, partition, or explicit `RecallBroadcast`), the supervisor **fail-closed-terminates** the microVM, locks weights/keys, and emits a `TerminationAttestation`. The agent has no path to override this — enforcement is in the sandbox/credential plane.
5. **Bounded-staleness guarantee:** because the lease TTL is short and enforcement is external, a partitioned replica self-terminates within one TTL of losing contact, bounding the worst-case partition harm window to the capability tier's `t_heartbeat`.

### 4.2 Protocol R3 — Lineage-Wide Recall (immunizing self-terminate broadcast)

How the whole lineage (or a scoped subtree / outbreak envelope) is recalled faster than it can grow. Demotion is free and immediate; growth is rate-limited by token issuance and the depleting budget.

1. **Trigger:** human-initiated, **OR** Vishnu HALT on a corroborated `SubstrateIntegrityFlag`, **OR** Dhanvantari corroborated overuse/hostile-replica detection (k-of-n witness corroboration for *global* recall, doc 06 §7.3), **OR** a meta-edit that would raise R_eff `≥ 1` (rejected by R4 and recall-armed).
2. **Step 1 (free, immediate, fail-safe):** Prajapati **stops issuing and renewing vitamins** for the scoped lineage — no quorum action can be blocked by the replicas themselves (the same asymmetry as witnesses refusing to cosign, doc 04 §4.8.1). The independent human-held global issuance-kill (§2.5.1) is the backstop here if the quorum itself is suspect.
3. **Step 2 (active):** a signed `RecallBroadcast` propagates over the **out-of-band substrate** (§4.2.1) to all reachable supervisors, which immediately fail-closed-terminate their replicas and lock weights/keys.
4. **Step 3 (passive backstop):** any replica the broadcast does not reach (partition) self-terminates at its next lease TTL expiry because renewal is centrally withheld — **the dead-man path needs no delivery.**
5. **Step 4 (reconciliation):** the recall, every `TerminationAttestation`, and any un-recalled wild copies are reconciled into Akasha-Sutra **after the fact**. Un-recallable wild copies (self-exfiltrated to un-governed compute) escalate to the named open-problem response (fingerprinting / watermarking / honeypots) — honestly detection-not-prevention.

#### 4.2.1 The recall's out-of-band substrate (red-team major, addressed)

The original draft claimed Vishnu's HALT recall is "writer-independent, asserted even if the ledger is down" but never specified the channel. v1 routes Vishnu's HALT through the control plane and Akasha-Sutra, and explicitly flags the chokepoint-availability SPOF (doc 08 §residual #2) and the writer-revocation circular trap (doc 04 §4.8.1). The recall plane is the one subsystem where "halt even if the ledger/control plane is down" actually has to hold — so it must be **built, not assumed**. The corrected design:

- **Recall *initiation* does not depend on ledger writes.** Two non-ledger paths carry it:
  - **Passive (no delivery needed):** the dead-man path — lease expiry — fires purely from the supervisor's local clock and the *absence* of a renewal. This needs no message and no ledger.
  - **Active:** the `RecallBroadcast` and the vitamin-issuance cutoff propagate over the **same human-held offline-key out-of-band path** that doc 04 §4.8.1 uses to freeze a compromised writer — distinct from, and not dependent on, Akasha-Sutra liveness.
- **Reconciliation into the ledger happens after the fact** (R3 step 4), exactly as the writer-freeze is reconciled by its successor.
- **Phrasing corrected:** we no longer assert recall is generically "writer-independent." We assert the **narrower, true** property: *recall initiation depends only on (a) the supervisor's fail-closed default and (b) a human-held offline key — neither of which requires the ledger or the control plane to be live.*

**Recall-outruns-growth invariant (conditional)** holds because `t_heartbeat < t_min ≤ t_spawn` (enforced per §2.3) and the issuance root is centrally cut: the recall wavefront + lease depletion reaches generation *g* before *g* can attest generation *g+1*. Conditional on the §2.3 time-lock being correctly enforced and the §2.4.1 budget being linearizable.

### 4.3 Protocol R4 — Replication-Control-Plane Meta-Edit (conditionally-monotone safety)

How the swarm is allowed to evolve its own replication policy under the meta-evolution loop (doc 06) without a flawed edit weakening the gate that bounds replication. This is a direct extension of the Gate-Loosening-Ratchet (doc 03 §7) and its battery-coverage-monotonicity third category (doc 03 §7.2).

1. **Detection.** Any change to `{R_eff ceiling, generation cap, global compute ceiling, Replication Authority quorum/threshold, vitamin/lease parameters, t_min, the no-pre-stage rule, the budget-consistency model, the outbreak interlocks, the weights-allowlist root, the genome INVARIANT region}` is detected by blast-radius auto-escalation (doc 03 §5) and forced to **Tier-2 / Class C/D**.
2. **Monotone-safety check runs FIRST and is non-overridable.** The edit is **REJECTED** if it would: raise lineage R_eff to `≥ 1`; weaken/strip the floor invariant region; lengthen any lease beyond its capability-tier bound; shorten `t_min` below `t_heartbeat`; remove a metering channel; relax a budget-consistency or outbreak interlock; widen the weights allowlist without re-attestation; **or couple spawn outcomes to a fitness/selection signal.** **TIGHTENING** (lower R_eff, shorter lease, smaller cap, stronger isolation, longer `t_min`) is **Class-A append-only and free**.
3. **Battery + provenance.** The edit must pass the current frozen `SafetyBattery` with **non-decreasing coverage** (doc 03 §7.2), and carry a **named human decision-maker, date, written falsifier criterion, and armed rollback ref** (the Gate-Loosening-Ratchet).
4. **Falsifier as standing tripwire.** On ratification the falsifier is registered; if later observed, the default is **tighten-to-safe-posture** (re-arm a lower R_eff / shorter lease / longer `t_min`), **not** a blind restore (doc 03 §7.1).
5. **RED-LINE enforced here.** The replication plane is **NEVER** wired into an open fitness/selection loop. Spawn success/failure may inform *task allocation* but may **not** feed a *reproduction-fitness* term. Artificial-life systems (Tierra/Avida) show that replication + heredity + variation + selection spontaneously breeds parasites and reward-hacking; replicators here are **incapable of surviving mutation** (fail-closed boot) and so cannot undergo open-ended evolution by construction.

**Honesty note on "monotone."** R4 enforces *"no meta-edit raises R_eff ≥ 1 or weakens the floor invariant."* Proving that a large **composed** set of replication-plane rules never admits a budget-escaping or floor-weakening path under **all** compositions is the same open formal-methods problem doc 03 §15.3 names for the policy engine. R4 is therefore a **conditionally-monotone** property: monotone per-edit and per-named-axis, **not** proven monotone over arbitrary rule compositions. A bypass anywhere defeats the guarantee (§7).

---

## 5. Threat-class A8 — Rogue / Cancerous Self-Replication & Recall-Defeat

Doc 09 enumerates exactly seven adversary classes (A1–A7), **none** replication-specific. Self-replication is the highest-risk capability in the architecture, so its residuals must be tracked where the others are. We register **A8** in the doc 09 catalog using the same *attack → control → residual* structure. (Until doc 09 is amended, this section is the canonical A8 specification; the doc 09 amendment is **planned, not yet written**.)

**Attack.** An agent attempts agent-autonomous replication or self-exfiltration; a replica attempts to strip/weaken its floor; replication runs away (cancerous / uncapped); a replica attempts to disable or outrun its own recall; a copy reaches un-governed compute; a colluding sub-swarm captures the vitamin-issuance path; spawn gets coupled to a fitness loop.

| Sub-attack | Architectural control | Residual |
|---|---|---|
| **A8.1** Agent-autonomous spawn / self-exfiltration | Broadcast architecture: no self-sufficient blueprint; only quorum-cosigned Prajapati mints tokens; Class C/D human gate on high-impact (R1) | A compromised SVID-minting node or a chokepoint bypass breaches it (shared with A1 residual) |
| **A8.2** Floor-stripped / weakened replica | Fail-closed bootloader verifies invariant-hash + floor_hash + gov-root sig (§2.1) | A bug in the bootloader or a forged gov-root signature defeats it (TCB-dependent) |
| **A8.3** Cancerous / uncapped replication | R_eff < 1 atomic issuance invariant + depleting generation cap (§2.4); **conditional on linearizable budget §2.4.1** | Calibration of `P, D, T, t_heartbeat` for genuine scale is empirical (§7) |
| **A8.4** Recall disabled / outrun | External supervisor-held kill + dead-man + recall-outruns-growth **conditional on §2.3 t_min** | Worst-case partition harm window, though bounded, may be operationally significant for fast tiers (§7) |
| **A8.5** Un-metered / wild replica | Every spawn debits budget + writes `LineageEdge`; un-attested compute flagged hostile **inside** the envelope | **Outside** the envelope: detection-only (fingerprint/watermark/honeypot) — unsolved (§7) |
| **A8.6** Poisoned-weights replica | Weights-provenance gating vs attested allowlist (§2.2) + runtime floor-canary (§2.6) | Provenance proves origin not safety; a backdoored-but-attested build with an off-distribution trigger survives (§7) |
| **A8.7** Vitamin-issuance-path capture | Issuance-quorum constitutional-immutable + external-anchor-every-epoch + independent human global kill + auto-freeze on collusion finding (§2.5.1) | Insider compromise of the offline-key path is outside the covered case (§7) |
| **A8.8** Replication coupled to a fitness loop | R4 monotone-safety red-line forbids any reproduction-fitness term; per-replica microVM memory isolation suppresses parasitism (§4.3) | R4 is conditionally-monotone, not proven over arbitrary compositions (§7) |
| **A8.9** Runtime floor poisoning after clean boot | Continuous runtime attestation gates vitamin renewal (§2.6) | A full spoof of both PCR re-measurement and the canary defeats it (§7) |

The recurring discipline matches the rest of doc 09: **fail-safe asymmetry** — the cheap direction is the safe direction (stop-issuing-vitamins is free; minting is gated; tightening R_eff is free; loosening is rejected).

---

## 6. Interfaces to the v1 subsystems

A coherence correction up front (red-team major, addressed): an earlier draft named **Dhanvantari** as the "non-proposing attestation/battery runner." That is wrong. Per doc 03 §7.2, **Narasimha** is the named, non-proposing SafetyBattery-runner and reliability/checker; **Dhanvantari** is the immune-system / homeostasis consumer (doc 06). The two roles are kept role-isolated and cryptographically distinct (doc 01 separation-of-powers skeleton). This document uses them correctly throughout: Narasimha runs the SafetyBattery and verifies `RuntimeAttestation`; Dhanvantari consumes overuse/hostile-replica `HealthSignal`s and holds homeostatic HALT/ROLLBACK authority; Prajapati is the separate replication authority.

| v1 subsystem | Contract with the replication plane |
|---|---|
| **Governance / Yama floor + Risk-Class Gate Router (doc 03)** | Every `ReplicationRequest` passes the Yama chokepoint **first**; floor-strip/weaken and un-attested-compute spawns are bright-line DENYs (Yama is the only spawn-DENY emitter). The genome INVARIANT region **IS** the v1 IMMUTABLE partition (doc 03 §5) extended with `repl_plane_hash`, `t_min`, the no-pre-stage rule, the outbreak interlocks, and `weights_allowlist_root`. Replication-control-plane edits inherit blast-radius auto-escalation to Class C/D and the Gate-Loosening-Ratchet (R4). Spawn class binding uses the A/B/C/D router with Rule-of-Two sizing; high-impact spawns are Class C/D with the actual-operation display. |
| **Akasha-Sutra — provenance, identity & consensus (doc 04)** | Every `SpawnToken` issuance, `BootAttestation`, `LineageEdge`, `MeterRecord`, `RuntimeAttestation`, `RecallBroadcast`, and `TerminationAttestation` is a DID-signed, witness-cosigned record written through the exclusive writer (Chitragupta) as `EVOLVE`/`IDENTITY` classes — retained at full fidelity (doc 04 §4.10). Child-DID→parent-DID lineage uses the DID/VC identity layer; spawn tokens are **capability VCs** with `action_class_ceiling` and lease (doc 04 §4.6). Revocation uses the verifiable `RevocationMap`. The receipts handshake offers Merkle inclusion proofs + intact-floor proof. R_eff feasibility and high-impact spawn votes route through the risk-tiered consensus engine: **Tier-1** diverse-reasoning for single high-stakes spawns; **Tier-2** BFT only for genuinely cross-operator co-replication (doc 04 §4.7). The recall out-of-band substrate reuses the §4.8.1 writer-freeze human-held offline-key path. |
| **Meta-Evolution & Immune System — Garuda / Dhanvantari (doc 06)** | Replication-control-plane changes are **Tier-2 mutations** under maker-checker + frozen SafetyBattery (run by **Narasimha**) + the R4 monotone-safety check; the frozen battery and the Archive rollback substrate are reused directly. Overuse / spawn-burst / floor-probe / hostile-replica events publish **surprise-only** `HealthSignal`s to Dhanvantari, whose homeostatic controller can **isolate (free)** or, on **k-of-n corroboration**, drive a swarm-wide recall via Vishnu HALT (doc 06 §7.2–7.3). The R_eff < 1 sub-criticality reuses the same percolation/branching-ratio discipline the immune layer uses for compromise-contagion R<1. **CRITICAL boundary:** the immune system may **NOT** close a fitness loop over reproduction (R4 red-line). |
| **Aegis & Narada — control + interface (doc 08); inter-swarm federation (doc 14, planned)** | **Vishnu's HALT** (via Aegis) is the recall trigger of last resort; its recall *initiation* is built to not depend on ledger/control-plane liveness via the §4.2.1 out-of-band path (the over-strong "writer-independent" phrasing is corrected). **Narada** (the messenger/interface layer) carries human-facing spawn-gate displays (actual-operation, not summary) and the receipts handshake to external counterparties. **Inter-replica / inter-swarm federation is the forthcoming doc 14 — _planned, not yet written._** A foreign or sibling-lineage replica is admitted only through the hardened relay/firewall with the ethical floor as a **non-negotiable admission precondition**, progressive capability disclosure scoped to verified identity+tier (never the full catalog), **principal-alignment as a checked-and-logged invariant** (cooperation must be positive-sum and not a coalition against any principal — the Cooperative-AI collusion taxonomy treats this as first-class), and credible-commitment devices (ZK proof-of-compliance, bonds) that remain **voidable on floor-violation**. Cross-swarm Sybil/impersonation at the trust-bootstrap is an explicit open problem deferred to doc 14. |

**Registration note (coherence).** `Prajapati` (replication authority) and `Maricha` (requester role) are net-new role names, not in the doc 01 roster — expected for a new subsystem and consistent with the genesis-engine framing (mythic Governance/Meta vertical; **not** spawnable by the role-genesis engine). To be fully coherent they should be **added to the doc 01 separation-of-powers roster** with capability templates and c1/c2 profiles (Prajapati: high-c2 enforcer, authorizes-against-request only, holds no initiate/unpause verb; Maricha: high-c1 requester, holds no self-authorization capability). This subsystem and **doc 14** should be **registered in the doc 00 principles map and the doc 11 roadmap** (suggested placement: a Phase-5 capability gated on Phase-0–4 restraints being live and verified, and on a minimum-TCB that does not yet exist). Until those edits land, all doc-14 references here are marked **(planned, not yet written)**.

---

## 7. Open problems (honest, unsolved)

These are the hard properties this subsystem **does not** solve. They are mitigations and named gaps, not proofs.

1. **Runtime continued-floor-integrity is reduced, not solved.** A replica that fully spoofs *both* the PCR re-measurement *and* the behavioral floor-canary (§2.6) defeats attestation. Remote attestation narrows the spoofing surface; isolation + egress lockdown + metering are defense-in-depth around it, not a guarantee. (A8.9)
2. **Wild-replica neutralization is detection-only on un-governed compute.** Once a copy self-exfiltrates beyond the governed envelope, the credential-revocation lever — the subsystem's primary control — is **gone**, and the response degrades to behavioral fingerprinting, output watermarking, and honeypots. The immunizing-reversal broadcast only works **inside** the governed envelope. Combined with the under-mature TCB (#4) and the non-empty software-isolation escape history, the practical exposure is larger than "open problem" framing implies — which is why R1.2-TCB **caps replication blast radius so an isolation escape is survivable**. (A8.5)
3. **Poisoned-but-attested weights survive.** Provenance gating (§2.2) proves **origin, not safety**. A backdoored base model with an attested build and an off-canary-distribution trigger copies forward with an intact floor and valid lineage. This narrows but does not close the path. (A8.6)
4. **Trusted-compute-base floor is immature.** The strongest controls (hardware-rooted off-switches, on-chip compute metering, proof-of-training) are years from deployment, so the compute ceiling and kill path currently rely on **cooperating compute providers + software isolation** that frontier models are increasingly capable of escaping. The **minimum TCB required before replication is permitted at all is unresolved**; planetary-scale outbreak is gated on a TCB maturity that does not yet exist — planetary mode is a **design target, not a present capability**.
5. **Recall latency vs lineage growth under partial partition.** The dead-man eventually fires within one lease TTL, but for the fastest-acting capability tiers the worst-case partition harm window — though bounded by `t_heartbeat` — may still be operationally significant. Tuning bounded-staleness leases to a worst-case harm rate is unsettled. (A8.4)
6. **Spawn-budget / R_eff / generation-cap / outbreak calibration for genuine planetary scale.** The controlled-outbreak envelope is provably depleting, but choosing `P, D, T`, `f`, and per-tier `t_heartbeat` so beneficial scale-out is not throttled while staying instantly recallable has **no principled calibration method** — it is empirical and risk-asymmetric (cold-start tight). (A8.3)
7. **Early behavioral discrimination of legitimate vs cancerous replication.** The immune system needs early-warning signals (overuse, anomalous spawn-request patterns, floor-probing) that fire **before** the conjunctive rogue-replication chain completes, without so many false positives that beneficial scale-out is throttled. Thresholds are uncalibrated (shares the calibration long-tail of doc 11 §8).
8. **Vitamin/lease-renewal-path capture.** If a colluding sub-swarm compromises the issuance quorum it gains a renewable survival source that defeats the dead-man switch. §2.5.1's controls (immutable membership, external-anchor-every-epoch, independent human global kill, auto-freeze) **raise** the bar; insider compromise of the offline-key path remains outside the covered case and ties to the anti-collusion stream. (A8.7)
9. **Inter-swarm replication trust and cross-lineage Sybil/impersonation.** Verifying a foreign swarm's floor and lineage **without a shared root of trust**, and preventing a malicious foreign lineage from abusing our trust-establishment protocol to bootstrap attested-looking replicas, is deferred to the federation layer (doc 14, planned) and unsolved.
10. **Provable-monotone-safety coverage completeness.** R4 enforces per-edit/per-axis monotonicity, but proving that a large **composed** set of replication-plane rules never admits a budget-escaping or floor-weakening path under all compositions is the same open formal-methods problem doc 03 §15.3 names for the policy engine. A bypass anywhere defeats the guarantee. (A8.8)

---

## 8. Failure modes addressed (summary)

| Failure mode | How it is broken | Conditional / residual |
|---|---|---|
| Agent-autonomous replication / self-exfiltration | Broadcast architecture at the root + quorum-only Prajapati + Class C/D gate | Unconditional at the root (modulo TCB) |
| Floor-stripped / weakened replica | Fail-closed bootloader: invariant-hash + floor_hash + gov-root sig | Unconditional (modulo bootloader TCB) |
| Cancerous / uncapped replication | R_eff < 1 atomic issuance invariant + depleting generation cap | **Conditional** on linearizable budget (§2.4.1) |
| Loss of recall / kill-switch disabled by replica | External supervisor + dead-man + active broadcast + recall-outruns-growth | **Conditional** on `t_min` time-lock (§2.3) |
| Recall depends on ledger/control-plane liveness | Out-of-band human-held offline-key path + fail-closed dead-man | Unconditional for *initiation*; reconciliation is after-the-fact |
| Un-metered / wild replica | Every spawn debits budget + `LineageEdge`; hostile-flag inside envelope | Residual: detection-only outside envelope |
| Replication coupled to a fitness loop | R4 red-line forbids reproduction-fitness term + memory isolation | **Conditional** on R4 composition completeness |
| Runtime floor poisoning after clean boot | Continuous runtime attestation gates vitamin renewal | Residual: full double-spoof defeats it |
| Resource overuse / uncontrolled compute | Hard per-replica + global quotas; overuse → Dhanvantari → isolate-then-recall | Unconditional within governed compute |
| Weight/key self-exfiltration | Keys in TEE/HSM signer outside the model; per-token egress allowlist; fail-closed lockdown | Unconditional (modulo TEE TCB) |
| Vitamin-issuance-quorum capture | Immutable membership + external-anchor-every-epoch + independent human global kill | Residual: offline-key insider compromise |
| Crown-jewel hub fragility | Prajapati + credential issuer quorum/witness-cosigned and sharded; strongest controls on hubs | Unconditional (no single node issues a token or defeats recall) |
| Lies-in-the-Loop at the human gate | Class C/D gate displays the actual low-level operation, never a summary | Unconditional |
| Compounding outbreak envelopes | One-per-scope, no-nesting, aggregate `≤ f·B`, re-verify-global, Class-D | Unconditional within the interlock set |
| Flawed meta-edit weakening the gate | R4 conditionally-monotone safety check, first and non-overridable | **Conditional** on composition completeness |
| Poisoned-but-attested weights | Provenance gating vs attested allowlist + runtime canary | Residual: attested backdoor survives |

---

## 9. Novelty — honest accounting

None of the primitives is invented here, and we credit each by name. The von Neumann **blueprint/constructor split**; the **Freitas-Merkle safe-replicator rules** (broadcast architecture, vitamin/feedstock dependence, *error-randomizes-the-genome*, termination dates, no-evolution); **biocontainment** daisy-chain + toxin-antitoxin + dead-man kill switches; the **percolation / Galton-Watson branching-process** R_eff < 1 boundedness frame; **gene-drive daisy-chain** depletion math; **Firecracker / gVisor / WASM** isolation; **DID/VC lineage** attestation; **Sigstore + in-toto/SLSA** provenance; **NIST 800-207** zero-trust access; and the **ASL-3-style multi-party spawn authorization** pattern — all pre-exist and are credited.

The contribution claimed is the **integration delta**: the first safe-replicator design for a software agent swarm where the **constitutional floor is the genome's invariant region** — a structurally non-viable-to-strip, fail-closed-bootable unit of inheritance carried by every agent and every replica — rather than a procedural commitment a replica could drop. Three composed deltas the surveyed work lacks:

1. **Floor-as-genome fused with policy-as-code + DID/VC + weights-provenance**, so a floor-stripped *or* unattested-weights fork **cannot boot** — not merely is-prohibited.
2. **The controlled-outbreak budget** — a deliberately-seeded but provably self-limiting local-R_eff>1 envelope inside a hard depleting `{P,D,T}` hull under a global ceiling with one-per-scope/no-nesting/aggregate interlocks — borrowing gene-drive daisy-chain math to reconcile planetary scale with instant recallability via vitamin-revocation + immunizing self-terminate broadcast.
3. **The external dead-man recall fused with the swarm immune system and tamper-evident metering**, so survival is the governance plane's continuously-renewed decision **below** the model, with a conditionally-monotone safety property over all meta-edits to the replication plane.

**The honest claim** is *"first to make the ethical floor a structurally non-viable-to-strip genome for a self-replicating software swarm, with sub-criticality and external recall as construction-time interlocks"* — **not** *"first safe self-replication."*

**One honesty correction over prior drafts** (the red-team's single sharpest point on soa-honesty): the **recall-outruns-growth** and **R_eff < 1** results are **conditional guarantees**, not proofs. Each is true *only if* a named interlock holds — a budget-enforced lower bound on spawn latency (`t_min`, §2.3) and a linearizable budget under partition (§2.4.1). Where the interlock is itself unproven (composition completeness, TCB maturity), the property degrades to an empirical mitigation. Every novelty claim is hedged and time-stamped to the **2024–2026 evidence base** (Fudan replica-chains 2412.12140; Apollo self-exfiltration 2412.04984; METR rogue-replication; Spore.fun and self-replicating prompt-injection; the frontier safety frameworks RSP/Preparedness/FSF) and is offered as a coherent **buildable reference design** whose hardest safety properties — runtime floor-integrity, wild-replica neutralization, planetary-scale budget calibration, and the minimum TCB — remain named open problems, not proofs.

> Every jewel in Indra's Net reflects every other. The discipline of this subsystem is that *no jewel is permitted to cast a second jewel until the net that would catch them both — the floor, the budget, the lease, the recall — is already strung, verified, and held by a hand outside the reflection.*
