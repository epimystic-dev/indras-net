# Evolution Overview — the Functional, Federation, Replication & Defense Layers

> *Look at one jewel and you see all the others reflected in it. The first eleven sections cut the facets of a single jewel and arranged the net so each reflects the rules of the whole. This addendum does not re-cut the jewels. It grows the net outward — more jewels (the working specialists), a treaty-bridge to other nets (federation), a strictly-gated way to make more of the net (replication), the trust that lets a new jewel be admitted quickly, the hardening that keeps a poisoned jewel from spreading, and the physics that says which clusters of jewels may be governed as one. Every new facet still reflects the same three spines: the **Floor** (Yama), the **Audit fabric** (Chitragupta), the **Halt authority** (Vishnu). Nothing here weakens them; everything here hangs off them.*

This document is the **front door to the v2 evolution** of Indra's Net. Doc 00 introduced the integrated cell — eight subsystems composing safe self-evolution, a homeostatic health layer, cryptographically-bound governance, and standing anti-collusion. That cell is the **substrate this addendum builds on and does not modify.** The seven new sections (docs 12–18) are **strictly additive**: each consumes v1 mechanisms by exact citation, introduces **no new chokepoint, no new write-path, and no new identity primitive**, and hard-codes a fail-closed default for any dependency that is not yet built.

The honest framing, stated once and binding on everything below. The v1 posture in doc 00 §7 — *coherent buildable reference design, not a validated system; reasoning is rung-2 interventional, not rung-3 structural-causal guarantee* — **applies in full to the v2 layers, and is sharper where the topic is more dangerous.** Two of these layers (inter-swarm federation, doc 14; controlled self-replication, doc 15) cross the architecture's highest-risk boundaries. For those, we do not soften the caveats; we name the red-lines as construction-time invariants and name the residual risk as residual. *The aesthetic carries the mystery; the substance carries only truth.*

The same role-vocabulary discipline from doc 00 §intro holds throughout: archetypal mythic names are compressed coordination-and-ethics semantics, **always** paired with a plain functional gloss, **never** a religious claim, offered with humility toward the living traditions that gave the names meaning. If the names distract, read only the glosses — the architecture is fully specified by the functional contracts alone. New substrate names introduced by the evolution layers are listed in §6.

---

## 1. What the evolution adds (and what it deliberately does not)

The v1 cell answers *what an agent is, how it coordinates, how it is governed, how its history is kept incorruptible, how it evolves and heals, how it remembers, and how it meets reality.* It leaves six questions for a swarm that must do **real, open-ended, multi-organization, scalable work** — and answers them in the seven new sections.

| # | The question v1 left open | The v2 answer | Doc |
|---|---|---|---|
| Q1 | *How does the net grow the specialists that actually do the work — and new specialists for tasks no role fits — without an ungoverned bag of personas?* | The **two-plane functional layer**: a stable signed Guild + seed-role catalog over an open-ended `Charter→Genesis→Trial→Score→Promote` role-genesis engine. | 12 |
| Q2 | *What is the canonical on-disk definition of an agent, such that emergent roles stay auditable and floors stay non-strippable?* | The **agent-definition spec**: every agent is a signed `SOUL / INSTRUCTIONS / IDENTITY` triad (the von-Neumann genome) split into an INVARIANT region (floor) and a VARIABLE region (persona). | 13 |
| Q3 | *How does Indra's Net cooperate with OTHER swarms across trust boundaries, ethically and positive-sum, without being exploited or drawn into collusion?* | **Inter-swarm federation & diplomacy** — the **Sandhi-Setu** treaty-bridge: a hardened relay/firewall, floor-as-admission-precondition, ecosystem-benefit as a checked-and-logged invariant. | 14 |
| Q4 | *When (if ever) may the swarm make more of itself, and how is that the single highest-risk capability gated so it can never run away?* | **Controlled self-replication** — the **Prajapati–Maricha cell**: quorum-cosigned spawn tokens, sub-criticality by construction (R_eff < 1), external dead-man recall, the floor as a non-strippable genome region. | 15 |
| Q5 | *How is trust established rapidly with humans and machines without letting reputation buy privilege?* | **Rapid trust establishment** — the **Pratyaya trust plane**: structurally unconflate ACCESS (zero-trust, per-request) from REPUTATION (slow, portable, friction-only); audit-fabric-as-trust-accelerant. | 16 |
| Q6 | *How does the swarm survive an adversary who poisons or hijacks it, when ~250 docs backdoor any model and no defense has a proof?* | **Security, OpSec & anti-poisoning** — the **Rakshakavaca layer**: promote the `quarantined:*` trust-labels into a runtime IFC taint lattice; deterministic chokepoints load-bear, probabilistic detectors are early-warning only. | 17 |
| Q7 | *Which physics claims in the v1 docs actually load-bear, and which are aesthetic that must be barred from control paths?* | **First-principles physics & mathematics**: closure-gated fractal governance, causal-discipline-as-audit-admission, σ/Lyapunov certified homeostasis — each with a blunt **load-bearing-vs-framing** verdict. | 18 |

**What the evolution does not add.** It adds no new authority. Docs 16, 17, and 18 are *lenses and instruments* over the existing floor/audit/identity/health spine — a friction lens (16), a taint clause inside the existing Yama chokepoint and percolation instrumentation (17), and a measurement-and-certification spine that *measures and constrains but issues no verdict it does not earn* (18). Docs 12 and 13 are a disciplined generalization of doc 01 §8's `RoleStub` pipeline. Only docs 14 and 15 add genuinely new operational surfaces (an external trust boundary; a replication authority) — and both are built so that the surface is reachable **only via single audited chokepoints; non-bypass is an enforced obligation of the harness, not a proven theorem**, mounted on the v1 spine, with their hardest properties named open.

---

## 2. The layered map, with v2 in place

Read this top-to-bottom as "where work flows," exactly as doc 00 §4. The three vertical spines are unchanged: **Yama (Floor)** to the left (deterministic gate before every consequential action), **Chitragupta (Audit)** to the right (exclusive-writer of the one append-only log), **Vishnu (Halt)** beneath (HALT-only, no `unpause`/`initiate`/`trap`). The v2 layers are shown as additions that **hang off these spines, never beside or above them.**

```
                          ┌───────────────────────────────────────────────────────────┐
   HUMAN PRINCIPAL ◄─────►│  Risk-Class HITL gates  A / B / C / D                      │
   (welfare anchor)       │  Rule-of-Two sizing (doc 17) · actual-operation display    │
                          │  (Lies-in-the-Loop-resistant; never a NL summary)          │
                          └───────────────────────────────┬───────────────────────────┘
                                                          │ escalation = disagreement / uncertainty /
                                                          │             blast-radius / Rule-of-Two violation
 ════════════════════════════════════════════════════════════════════════════════════════════════════
  │ F │   ┌────────────────────────────────────────────────────────────────────────────────────┐  │ A │
  │ L │   │ (14) INTER-SWARM FEDERATION & DIPLOMACY — "Sandhi-Setu"          ◄── external peers  │  │ U │
  │ O │   │   hardened relay/firewall · DECLARE→ADMIT→CONTRACT→OPERATE · floor-as-admission ·    │  │ D │
  │ O │   │   ecosystem-benefit CHECKED invariant · voidable-on-floor treaties · KYA principal   │  │ I │
  │ R │   │   ▲ Inter-Swarm-Envoy is a Governance/Meta seed-role — NOT genesis-spawnable         │  │ T │
  │   │   └────────────────────────────────────────────────────────────────────────────────────┘  │   │
  │ Y │   ┌────────────────────────────────────────────────────────────────────────────────────┐  │ F │
  │ A │   │ (08) INTERFACES & DevSecOps — "Aegis & Narada"                                       │  │ A │
  │ M │   │   chokepoint interceptor (federation-facing extension = the doc-14 relay) ·          │  │ B │
  │ A │   │   trusted-monitor ensemble · model-adapter (trust-class) · Narada = HITL messenger   │  │ R │
  │   │   └────────────────────────────────────────────────────────────────────────────────────┘  │ I │
  │det│   ┌────────────────────────────────────────────────────────────────────────────────────┐  │ C │
  │erm│   │ (16) RAPID TRUST — "Pratyaya"   [a FRICTION LENS over the floor, not a new gate]      │  │   │
  │in-│   │   ACCESS (zero-trust PE/PA/PEP, per-request)  ⟂  REPUTATION (slow, portable,          │  │ Ch│
  │is-│   │   friction-only) · T0→T3 ladder ↔ A/B/C/D · gated-promote / free-instant-demote ·    │  │ it│
  │tic│   │   show-your-receipts handshake (audit-fabric-as-trust-accelerant)                    │  │ ra│
  │pol│   └────────────────────────────────────────────────────────────────────────────────────┘  │ gu│
  │icy│   ┌────────────────────────────────────────────────────────────────────────────────────┐  │ pt│
  │ at│   │ (12) FUNCTIONAL AGENTS, GUILDS & ROLE-GENESIS — the two-plane functional layer       │  │ a │
  │the│   │   PLANE 1 guilds + signed seed-roles (anchor) ── OVER ──► PLANE 2 Charter→Genesis→    │  │   │
  │too│   │   Trial→Score→Promote (emergent, signed-at-instantiation, least-privilege)           │  │ ex│
  │l  │   │   (13) AGENT-DEFINITION SPEC: every role = signed SOUL/INSTRUCTIONS/IDENTITY triad    │  │ cl│
  │cho│   │        INVARIANT region = floor (fail-closed boot)  ·  VARIABLE region = persona      │  │ us│
  │ke-│   └────────────────────────────────────────────────────────────────────────────────────┘  │ iv│
  │poi│   ┌────────────────────────────────────────────────────────────────────────────────────┐  │ e │
  │nt │   │ (01) SWARM TOPOLOGY & AGENT MODEL · (05) "the Mandala" coordination                  │  │   │
  │   │   │   actual-occasion agents · DID/VC identity · typed Effect lattice · GroupBlanket ·   │  │ wr│
  │ ◄─┼───│   salience-gated surprise-only bus · plastic trust-edges · homeostasis              │  │ it│
  │   │   └────────────────────────────────────────────────────────────────────────────────────┘  │ er│
  │(08│   ┌────────────────────────────────────────────────────────────────────────────────────┐  │   │
  │ + │   │ (02) COOPERATION ⇄ ANTI-COLLUSION · (03) GOVERNANCE, ETHICS & THE FLOOR              │  │ ◄─┼─┐
  │ 17│   │   welfare-conditioning · capital-decoupling · collusion detector ·                   │  │   │ │
  │)  │   │   lexicographic floor (policy-as-code) · pluralist runtime · gate-loosening ratchet  │  │   │ │
  │   │   └────────────────────────────────────────────────────────────────────────────────────┘  │   │ │
  │(17│   ┌────────────────────────────────────────────────────────────────────────────────────┐  │   │ │
  │)  │   │ (04) PROVENANCE, IDENTITY & CONSENSUS — "Akasha-Sutra"                               │  │   │ │
  │IFC│   │   exclusive-writer Merkle/tile log · witness cosigning · CID · DID/VC + SPIFFE ·      │  │   │ │
  │ta-│   │   ▲ (17) adds: trust-labels → RUNTIME TAINT LATTICE (CaMeL/FIDES) gating every call   │  │   │ │
  │int│   │   ▲ universal provenance-gating (Sigstore/in-toto/SLSA) admission for EVERYTHING      │  │   │ │
  │la-│   └────────────────────────────────────────────────────────────────────────────────────┘  │   │ │
  │tt-│   ┌────────────────────────────────────────────────────────────────────────────────────┐  │   │ │
  │ice│   │ (06) META-EVOLUTION + HEALTH "Garuda–Dhanvantari" · (07) MEMORY & ADAPTATION          │  │   │ │
  │ ◄─┼───│   PROPOSE→EVALUATE→SELECT→ARCHIVE · tiered reversibility · Endure law · immune system │  │   │ │
  │   │   │   ▲ (18) feeds σ-criticality + Lyapunov-margin + shift-triage as new VITAL SIGNS      │  │   │ │
  │   │   └─────────────────────────────────────────┬──────────────────────────────────────────┘  │   │ │
  └───┘                                            │                                               └───┘ │
       ▲                                           ▼                                                     │
       │  ┌──────────────────────────────────────────────────────────┐    ┌──────────────────────────┐ │
       │  │ (15) CONTROLLED SELF-REPLICATION — "Prajapati–Maricha"     │    │      THE ARCHIVE         │ │
       │  │   quorum-cosigned Replication Authority (Prajapati) ·      │    │  append-only · CID ·     │ │
   HALT│  │   R_eff<1 by construction · generation-capped · lease/     │◄───│  MAP-Elites elites ·     │ │
  (one-│  │   vitamin + dead-man toxin-antitoxin recall (EXTERNAL) ·   │    │  role-genomes (doc 12) · │ │
  way) │  │   microVM isolation · floor = non-strippable genome region │    │  revert-to-known-good    │ │
       │  │   ▲ NEVER agent-autonomous · NEVER coupled to a fitness    │    │                          │ │
       └──┤      loop · NEVER un-metered · NEVER loses recall          │    │  one structure serves    │ │
   Vishnu │   (18) supplies the lineage-wide R_eff<1 budget check      │    │  evolution+health+audit  │ │
  continuity└────────────────────────────────────────────────────────┘    │  + role-genome lineage   │ │
  /halt-guardian                                                            └──────────────────────────┘ │
  (HALT yes; unpause no) ◄─── lineage / rollback ────────────────────────────────────────────────────────┘
```

**How to read the v2 additions against the spines.**

- **The relay (doc 14) is the federation-facing extension of the doc-08 chokepoint, not a new gate.** An external peer reaches a worker *only* through it; OUR Yama floor gates every internal action a federation step triggers, unchanged. The peer's declared floor is never trusted as ours — it only bounds `max_cooperation_class`.
- **The taint lattice (doc 17) is a set of deterministic clauses *inside* the existing Yama chokepoint.** It introduces no second enforcement point. Promoting `quarantined:*` from doctrine (doc 00 §3, doc 09) to a runtime CaMeL/FIDES label that gates every tool call by least-upper-bound is the load-bearing security move — and it works even when the model is injectable, because the model provably cannot separate instructions from data in one token stream.
- **The Replication Authority (doc 15) sits beside Vishnu's halt line, not above it.** Vishnu's HALT is the recall trigger of last resort and is writer-independent. Prajapati only *authorizes against an already-floor-cleared request*; Yama is still the only emitter of the spawn-DENY. A replica carries the floor in its INVARIANT genome region and **cannot mint its own spawn token or survival lease** — recall is enforced externally by the credential/sandbox plane.
- **The physics layer (doc 18) writes nothing and gates nothing on its own.** It produces content-addressed certificates (`ClosureCertificate`, `CausalAttestation`, `CriticalityState`, `LyapunovCertificate`) that *let* doc 05 graduate a `GroupBlanket` from advisory to aggregating, *let* Chitragupta admit a Pearl-rung tag, and feed Dhanvantari new vital signs. Every controller ships **shadow-mode-first**.
- **The functional layer (docs 12–13) populates the topology; it is not a new topology.** A guild *is* a doc-01 `GroupBlanket`. A genesis-promoted role-genome *is* a doc-06 Archive node. The triad's `IDENTITY` file *is* the doc-01 `IdentityRecord`, structured on disk. No new identity primitive exists.

---

## 3. How each new layer hangs off the v1 spine

Each evolution layer binds to the same four anchors — **Floor (doc 03), Audit (doc 04), Identity (doc 01/04), Health (doc 06)** — plus the control chokepoint (doc 08). The table is the contract index; the per-doc `interfaces` sections carry the exact section-level bindings.

| New layer | Floor (Yama, 03) | Audit (Chitragupta, 04) | Identity (01/04) | Health (Dhanvantari, 06) |
|---|---|---|---|---|
| **12 Functional / Role-Genesis** | Every triad binds INSTRUCTIONS risk-gates + INVARIANT-region floor-hash to the Yama PDP; charters declare each capability's `relaxes_constraint` for the §10 rollout sequencer; Observer-Trio consumes the frozen safety battery as a **veto**. | Charter, Genesis composition, Trial run, `GenesisScore`, `PromotionTicket`, triad signature — each a signed event hash-chained in; skill/tool provenance bound into the Merkle log. | Triads instantiate as doc-01 personas/occasions; guilds **are** clans/divisions; bound toolset entries **are** §4 Effect-lattice ids; c1/c2 dials reused. | Promoted role-genomes **are** Archive nodes (reuse + O(1) rollback + lineage as one structure); genesis MUST NOT close an open fitness loop (Tierra/Avida red-line). |
| **13 Agent-Definition Spec** | `SOUL.floor_binding` references the doc-03 PolicyBundle by `content_hash`; the Boot Integrity Verifier enforces `floor_content_hash == live bundle`; VARIABLE edits route through tiered-reversibility, the GLR, and the §10 capability sequencer. | 3-stage attestation (genesis-author sig → governance VC → hash-chained provenance record); `triad_root_cid` is a doc-04 CID; CID-mismatch on read is the hard integrity failure that catches mount/truncation/BOM corruption. | `IDENTITY.json` **is** the on-disk `IdentityRecord`; the triad **is** the durable per-persona data; the occasion loads it **read-only** and projects `self_preservation_value=0`. | The Charter→Trial→Score→Promote path is the doc-06 MAP-Elites-fed genesis path; `Score` consumes the frozen safety battery (Endure law); VARIABLE-edit drift + unit-rollback owned by the Health drift budget. |
| **14 Federation / Sandhi-Setu** | The peer's floor is **never** our floor; a Yama `ENFORCE_FAIL` on any federation-derived action is non-overridable and trips the treaty floor-void clause; F0–F3 federation tiers map onto A/B/C/D. | Every `InboundEnvelope`, `FederationSession` transition, `FloorCompatVerdict`, `EcosystemBenefitCheck`, `Treaty`, `DisputeRecord` appended by the exclusive writer with selective-disclosure for sensitive terms. | Cross-boundary DID/VC + Know-Your-Agent principal-binding; `FederationAgentCard` **extends** the doc-08 AgentCard, not replaces it; the Envoy is a non-spawnable Governance/Meta seed-role. | Circuit-breaker trips, channel quarantine, cascade isolation feed Dhanvantari's vital signs (per-partner trust, channel-capacity, corroboration-failure rate, reputation-Gini); Vishnu is the only HALT emitter. |
| **15 Replication / Prajapati–Maricha** | Every `ReplicationRequest` passes Yama **first**; floor-strip/weaken and un-attested-compute spawns are bright-line DENYs; control-plane edits inherit blast-radius auto-escalation to C/D + the GLR ratchet. | Every `SpawnToken`, `BootAttestation`, `LineageEdge`, `MeterRecord`, `RuntimeAttestation`, `RecallBroadcast`, `TerminationAttestation` is DID-signed, witness-cosigned, written through the exclusive writer. | child-DID → parent-DID lineage on the DID/VC layer; spawn tokens are capability VCs with `action_class_ceiling` + lease; the floor is the INVARIANT genome region verified at fail-closed boot. | Replication-control-plane changes are Tier-2 mutations under maker-checker + frozen battery + a **monotone-safety** check (no meta-edit raises R_eff≥1 or weakens the floor); overuse/spawn-burst events publish surprise-only HealthSignals; immune system may **not** close a fitness loop over reproduction. |
| **16 Rapid Trust / Pratyaya** | The Progressive Authorizer's policy engine is co-located with and **subordinate to** Yama: FAIL is evaluated first and non-overridable; a floor near-miss is a free-demotion trigger; A/B/C/D **are** the ladder's eligibility targets. | Reputation records + receipts-handshake slices **are** tile-Merkle inclusion proofs; promotion/demotion events and PE-decisions emitted to Chitragupta **before** action; the Reputation Ledger is a cache of inclusion proofs, never a free-floating score. | Consumes the v1 identity layer verbatim (DID/VC cross-boundary; SPIFFE/SVID local; keys in TEE/HSM); replicas inherit a lineage-capped rung (parent−1). | Immune-system behavioral-anomaly baselines are a demotion-trigger source; baselines re-set only on ratified evolution steps; collusion verdicts feed reputation slashes + demotion. |
| **17 Security / Rakshakavaca** | The IFC taint check is added as **deterministic clauses of the Yama floor at the existing chokepoint** — no new chokepoint; declassification is a Yama-class gate with a named falsifier; a taint BLOCK is as non-overridable as a harm FAIL. | All `ArtifactAttestation` / `ManifestApproval` / `RugPullAlarm` / `CompromiseSignal` / `InfluenceTrace` records emitted to Chitragupta; admission attestations bound into the Merkle log; CID-on-read is the integrity check the taint lattice's `source_cids` rely on. | DID/VC + SPIFFE/SVID (keys outside the model) underpin Sybil resistance + the no-keys-in-model rule; every genesised triad passes provenance-admission + floor-signature boot check before instantiation. | `ContactGraphHealth (R<1)` is a new Dhanvantari vital sign alongside the criticality exponent; canary/honeypot/influence-trace findings trigger HALT+ROLLBACK; targeted poison-revert uses doc-06 O(1) Archive rollback + re-runs the safety battery. |
| **18 First-Principles Physics** | A `DOWNTAGGED` verdict on a bright-line causal over-claim is surfaced to Yama as a floor-honesty event (§6 honesty tier) with the REPARATIVE path available; Yama's floor verdict is always supreme and read at the individual-agent level. | ALL certificates are content-addressed and tee'd **read-only**; this subsystem **never writes the log** — Chitragupta exclusive-writer preserved; the Causal-Discipline Gate decides at which rung a claim enters the chain; GroupBlanketUpgrades require k-of-n witness cosign. | Reads/writes `WorkerOutputEnvelope.causal_rung`; closure-test graduates `GroupBlanket.decision_authority` (doc 05 §7.2.1) ADVISORY→AGGREGATING on a witnessed certificate, auto-demote on margin loss. | σ supercritical-storm early-warning + Lyapunov margin-to-boundary are first-class vital signs; First-Line Shift-Triage feeds the four-pathway monitors; AdaptationStabilityCheck is an admissibility **input** to the tiered-reversibility gate, not the floor verdict. |

---

## 4. The replication red-lines, stated up front

Self-replication (doc 15) is the **single highest-risk capability in the architecture.** Per the doc-00 honesty floor applied to itself, the red-lines are stated here, in the front door, as **construction-time invariants** — not as policies someone must remember to enforce. Each is a property of how the mechanism is built; the per-doc treatment specifies the enforcement and names the residual.

| Red-line | Why it is a construction fact, not a policy | Residual risk (named) |
|---|---|---|
| **NO agent-autonomous spawn.** | The only issuer of a spawn token is the quorum-cosigned Replication Authority (Prajapati). The requester role (Maricha) can *ask* but holds no minting verb. A single un-metered spawn channel would break this — so every spawn is metered + attested or it is hostile by definition. | Vitamin/lease-renewal-path capture: a colluding sub-swarm that compromises the issuance quorum gains a renewable survival source. Hardening the quorum against insider/collusion attack is open (ties to the anti-collusion stream). |
| **NO floor-stripping replica.** | The constitutional floor is the INVARIANT region of the genome, verified by a fail-closed boot signature check against the governance root. A floor-stripped fork's invariant-region hash diverges → it **refuses to boot.** Non-viability is structural (von-Neumann blueprint/constructor split + Freitas-Merkle "error randomizes the genome"). | Runtime continued-floor-integrity: a replica that fully spoofs both PCR re-measurement *and* the behavioral floor-canary defeats attestation. Isolation + egress lockdown + metering are defense-in-depth around it, not a guarantee. |
| **NO self-sufficient blueprint / self-minted survival credential.** | Replicas carry no blueprint that reconstructs the spawn authority; the vitamin/lease + dead-man toxin-antitoxin heartbeat is enforced **externally** by the sandbox/credential plane. A replica cannot disable its own kill-switch. | Wild-replica detection on un-governed compute: once a copy self-exfiltrates beyond the governed envelope, credential-revocation is gone and response degrades to behavioral fingerprinting + honeypots — detection, not prevention. |
| **NO replication coupled to an open fitness/selection loop.** | Replication + heredity + variation + selection spontaneously breeds parasites and reward-hacking (Tierra/Avida). The immune system (doc 06) may isolate and rollback but is structurally barred (R4 red-line) from closing a fitness loop over reproduction. | Early behavioral discrimination of legitimate vs cancerous replication needs early-warning signals that fire *before* the conjunctive rogue chain completes, without throttling beneficial scale-out. Thresholds uncalibrated. |
| **NO loss of recall.** | Lineage-wide effective reproduction R_eff < 1 + a finite, depleting generation cap ⇒ provable percolation-boundedness and the **recall-outruns-growth** property (t_heartbeat < t_spawn). The planetary "controlled outbreak" is a hard-enveloped, still-provably-depleting, instantly-recallable region. | Recall latency vs lineage growth under partial network partition; spawn-budget/R_eff/generation-cap calibration for genuine scale; and the **trusted-compute-base floor** — hardware-rooted off-switches are years out, so the ceiling currently rests on cooperating compute providers + software isolation. |

The honest headline, repeated because it matters: **this layer makes sub-criticality and external recall construction-time guarantees rather than hopes — but its three hardest safety properties (runtime floor-integrity, wild-replica neutralization, planetary-scale budget calibration) remain empirical mitigations and named open problems, not proofs.** The claim is *"first to make the ethical floor a structurally non-viable-to-strip genome for a self-replicating software swarm, with sub-criticality and external recall as construction-time guarantees"* — time-stamped mid-2026, hedged — **not** *"first safe self-replication."*

A parallel honest note for **federation** (doc 14): you cannot white-box-verify a foreign swarm's ethical floor. This is *not* solved; it is **substituted-for** by a ranked, fail-closed assurance ladder (declaration < behavioral honeypot-probe < ZK proof-of-compliance < receipts-handshake < cross-corroboration) whose residual is named, bounded, and escalated to a Lies-in-the-Loop-resistant human gate that displays the **actual** treaty terms. A sophisticated peer can pass behavioral probes while harboring an incompatible floor; that is the load-bearing residual of the whole subsystem, and we say so.

---

## 5. The unifying invariants the v2 layers share

Four invariants recur across the seven new sections. They are the reason the evolution composes into the v1 cell rather than bolting onto it. Each is a v1 principle (doc 00 §3) extended to new surfaces.

**5.1 — Genome = Floor (the non-strippable unit of inheritance).** Docs 12, 13, and 15 share one object: the signed `SOUL/INSTRUCTIONS/IDENTITY` triad with the floor in an INVARIANT, fail-closed-bootable region. This is what makes "a role cannot strip its floor" (12), "a triad cannot be forked floor-free" (13), and "a replica cannot mutate its own floor" (15) the **same construction fact**, not three separate promises. It extends doc 03's redline ("impossible by construction, not merely prohibited") into the unit of reproduction.

**5.2 — Fail-safe asymmetry, applied identically across humans / machines / artifacts / replicas / peers.** The cheap direction is always the safe direction (doc 00 §3.8). Trust *promotion* is gated, multi-fresh-signal, rate-limited; *demotion* is free, instant, single-anomaly (doc 16). Gate *tightening* is append-only; *loosening* needs a named decision-maker + date + falsifier (doc 03 GLR). Integrity-label *demotion* is free; *promotion* (declassification) is a gated governance act (doc 17). Provenance *re-approval* is mandatory on any signed-manifest change (doc 17). One governing invariant, five surfaces.

**5.3 — Separate access from reputation (and never let cooperation mint authority).** Doc 16 makes this a **type-level guarantee**: REPUTATION has, by construction, no interface method that returns a privilege grant — only a capped friction discount. Doc 14 enforces the cross-boundary corollary: treaty bonds settle in conserved task-credit so no bond can mint authority, and every credible-commitment device is **voidable-on-floor-violation** (no commitment unbreakable by Yama-FAIL / Vishnu-HALT). Doc 15 enforces the replication corollary: a replica inherits a lineage-capped rung (parent−1) and must re-earn standing, just as it cannot mint its own spawn token. This is doc 00 §3.9 (competence-weighted, never capital-weighted) carried to every new boundary.

**5.4 — Ecosystem-benefit and cooperation==collusion as checked-and-logged invariants.** Doc 02's "cooperation == collusion, same mechanism, opposite valence" is the design fulcrum of doc 14: before any inter-swarm cooperation commits, the Ecosystem-Benefit Invariant Checker verifies-and-logs that it is positive-sum for declared principals and **not a coalition against any party's principal** — treating collusion as first-class across the trust boundary exactly as the cooperation layer does internally. "For the benefit of all intelligences" becomes an enforced, logged invariant rather than an assumption that "both swarms are nice."

**5.5 — Deterministic chokepoints load-bear; probabilistic layers are early-warning only.** This is the spine of doc 17 and the security posture of all seven. The taint lattice, egress allowlists, capability confinement, and provenance admission do the load-bearing work; spotlighting, injection classifiers, masked re-execution, anomaly detection, and honeypots are cheap early-warning feeding the immune system, **never a boundary** — because the published evidence (*"The Attacker Moves Second"*) indicates that adaptive attack on these probabilistic layers is intractable in practice: every evaluated defense was bypassed at >90% ASR, consistent with the observation that a model has no reliable means to separate instructions from data in one token stream. Provenance proves **origin, not safety**; a faithfully-signed poisoned artifact verifies perfectly.

---

## 6. New substrate names introduced by the evolution

Consistent with doc 00 and the existing substrate names (Akasha-Sutra = the provenance/audit thread, doc 04; the Mandala = neuromorphic coordination, doc 05; Aegis & Narada = control + interface, doc 08; Alaya-vijnana = memory, doc 07; Garuda–Dhanvantari = meta-evolution + immune system, doc 06), the evolution layers introduce:

| Name (gloss) | Functional contract | Doc |
|---|---|---|
| **Guild-Steward** | owner of a functional guild's signed skill-library, seed-role catalog, and TIGHTEN-only local norms; named requester for promotion, never its own judge | 12 |
| **Role-Charterer** | drafts a candidate persona-triad from a task (Governance/Meta; not genesis-spawnable) | 12 |
| **Genesis-Observer-Trio** | three independent maker-checker observers scoring role-completeness, plan-vs-capability, and safety+differentiation; holds the lexicographic safety veto on promote | 12 |
| **Sandhi-Setu** (the treaty-bridge) | the inter-swarm federation relay/firewall, structurally outside the worker mesh and inside the Aegis control plane | 14 |
| **Inter-Swarm-Envoy** | the federation-facing seed-role operating the relay (Governance/Meta; not genesis-spawnable) | 14 |
| **Prajapati** (the progenitor) | the quorum-cosigned Replication Authority — the only issuer of spawn tokens | 15 |
| **Maricha** (the requester) | the role that may *request* replication but can never authorize its own | 15 |
| **Pratyaya** (the ground of trust) | the rapid-trust plane that unconflates access from reputation | 16 |
| **Rakshakavaca** (the protective armor) | the deepened security / OpSec / anti-poisoning layer (the runtime taint lattice + provenance admission + topology-as-security) | 17 |
| **Narasimha** (the immune response) | the federation/security arm of the immune system — circuit-breaker trips, channel quarantine, cascade isolation, hostile-replica response | 15, 17 |

`Kaal-Bhairav` (doc 01 §10 / the security-IFC and standing red-team/falsifier role) is reused, not re-introduced. All Governance/Meta vertical roles — including Prajapati, Maricha, the Inter-Swarm-Envoy, the Role-Charterer, and the Genesis-Observer-Trio — are **NOT spawnable by the role-genesis engine** (doc 12 §1).

---

## 7. Reader's guide to the seven evolution sections

The seven sections can be read in any order, but this path tells the cleanest story — and **doc 13 should be read close after doc 12**, because the triad it specifies is the object docs 12, 14, and 15 all consume.

1. **`12-functional-agents-and-guilds.md` — populate the net.** Start here. The two-plane functional layer: stable guilds + signed seed-roles over the open-ended `Charter→Genesis→Trial→Score→Promote` engine. *Read this to understand how the swarm grows auditable, least-privilege specialists and resolves the endogeneity paradox's governance horn.*
2. **`13-agent-definition-spec.md` — the genome.** The canonical on-disk `SOUL/INSTRUCTIONS/IDENTITY` triad, the INVARIANT/VARIABLE split, the three-stage signing chain, the import-quarantine model. *Read this to understand why the floor is non-strippable by construction and how every emergent role stays signed.*
3. **`16-trust-establishment.md` — admit fast, safely.** The Pratyaya plane: unconflate access from reputation, the T0→T3 ladder, gated-promote / free-instant-demote, the show-your-receipts handshake. *Read this to understand why reputation buys friction, never privilege.*
4. **`17-security-opsec-and-anti-poisoning.md` — survive the adversary.** The Rakshakavaca layer: trust-labels as a runtime taint lattice, universal provenance-gating, Rule-of-Two HITL sizing, topology-as-security, poison-as-recoverable-not-preventable. *Read this to understand why deterministic chokepoints load-bear and probabilistic detectors only warn.*
5. **`14-inter-swarm-federation-and-diplomacy.md` — cooperate across boundaries.** The Sandhi-Setu treaty-bridge: the four-phase handshake, floor-as-admission, the ecosystem-benefit checked invariant, voidable-on-floor treaties, the honest assurance ladder for the unverifiable-foreign-floor problem. *Read this to understand ethical positive-sum federation without exploitation or collusion.*
6. **`15-self-replication-and-scaling.md` — make more of the net, gated.** The Prajapati–Maricha cell: the genome, the Replication Authority, sub-criticality by construction, external dead-man recall, universal metering. *Read this to understand the highest-risk capability and why it can never run away or strip its floor.* **Read §4 above first.**
7. **`18-first-principles-physics-and-mathematics.md` — the measurement spine.** Closure-gated fractal governance, the causal-discipline audit-admission gate, σ/Lyapunov certified homeostasis — every quantity carrying a blunt load-bearing-vs-framing verdict. *Read this to understand which physics actually load-bears and why framing metaphors are structurally barred from control paths.*

Each evolution section carries the same four parts as the v1 docs: a **summary**, an honest **novelty** accounting (what is genuinely new vs. assembled-from-credited-parts), its **interfaces** (the exact contracts to the v1 subsystems and the sibling evolution layers), and its **open problems** (stated as problems, not glossed).

---

## 8. Honest posture for the evolution (the limitations, carried into the details)

We close the way every section closes — by naming what the evolution has *not* solved, so the reader carries the caveats into the per-doc detail rather than discovering them late. These compose with, and do not replace, the doc-00 §7 limitations.

- **Every novelty claim is integration, time-stamped 2026-06, hedged.** None of the primitives is invented here — MetaGPT `Code=SOP(Team)`, CrewAI role/goal/backstory, von-Neumann blueprint/constructor split, DID/VC + SPIFFE, Sigstore/in-toto/SLSA, CaMeL/FIDES IFC, A2A Agent Cards, Know-Your-Agent, ZK proof-of-compliance, NIST 800-207, the Freitas-Merkle safe-replicator rules, percolation/branching-process theory, ε-machine/computational-mechanics, do-calculus/DoWhy, neural-Lyapunov, MorphAgent differentiation metrics — all are prior art, credited at their sites. The contribution is the **safe, auditable, vendor-neutral composition** mounted on the v1 contracts, never any single mechanism.

- **Evaluation of synthesized specialists is unsolved** (doc 12). We can keep every emergent role signed, attested, and gated (the governance horn), but there is no accepted benchmark for whether a swarm-generated role is genuinely competent, differentiated, AND safe (the evaluation horn). The Genesis-Observer-Trio's scores are best-available proxies, not validated measures.

- **Provenance proves origin, never safety** (doc 17). Cryptographic signing of a skill/persona file proves where it came from, not that it is poison-free; ~250 docs backdoor any model and ~5 docs poison RAG at 90–98% ASR. The contribution is making poisoning **recoverable** (taint-provenance tracing + Archive O(1) targeted rollback), not prevented. A sleeper that only fires on an untested trigger can pass every gate.

- **The unverifiable foreign floor is substituted-for, not solved** (doc 14), and **the three hardest replication safety properties remain empirical mitigations** (doc 15, §4 above): runtime floor-integrity against a fully-spoofing replica, wild-replica neutralization on un-governed compute, and planetary-scale budget calibration. We name the residual, fail closed to a human gate, and do not claim a proof.

- **Set-points across the evolution are uncalibrated** (docs 14, 15, 16, 18): the capability-threshold for fixed-vs-emergent instantiation, the federation transitive-trust cap, R_eff / generation-cap / per-tier heartbeat, the trust-ladder `k_promote` and friction-discount cap, the approximate-closure threshold, the σ set-point and Lyapunov margin. These are first-principles starting values that ship behind shadow-mode and conservative defaults; real tuning is per-deployment empirical work.

- **No defense has a security proof against an adaptive attacker who knows it** (doc 17): >90% ASR on every single static layer evaluated. We compose deterministic chokepoints so the **residual is bounded-and-continuously-measured by a standing adaptive red-team** (Kaal-Bhairav), and report measured ASR per actor class and legs-required-to-defeat — honest evidence, not a bound.

- **The physics layer guards against the architecture's own named failure** (doc 18): presenting rung-1 pattern dynamics (avalanches, attractors, "emergence") as rung-3 structural explanations. Closure is the only legitimate cash value of "downward causation"; Landauer/thermodynamics and strong-emergence are **demoted to framing and structurally barred from control paths**. Every controller ships shadow-mode-first with a blunt load-bearing-vs-framing verdict — measuring and certifying before it is allowed to gate.

These are not apologies; they are the design's honesty floor applied to itself, extended to the evolution. The v2 layers grow the net outward — more working jewels, a bridge to other nets, a gated way to make more, the trust to admit a new jewel fast, the armor to keep a poisoned one from spreading, and the physics that says which clusters may be governed as one — **with the seams designed so each can improve without the others, the spines, or the floor having to be rebuilt.** Whether the reflection holds under load, especially at the federation and replication boundaries, is the empirical question the seven sections, and the work after them, exist to answer.

---

## Open problems (cross-cutting, for the evolution as a whole)

Beyond the per-doc open problems, four concerns belong to the **integration of the evolution layers** and are owned by no single section:

1. **Governance UX at emergent-role scale.** Signing every emergent triad keeps roles auditable, but the human-legibility and capability-attestation management of thousands of ephemeral signed roles per task — VC issuance throughput, provenance-record volume, the human-ratification path for above-read-only grants — is an operational open problem (doc 12 OP1, doc 13 OP6). We have the mechanism (sign-at-instantiation) and a cost-bound (stubs stay Class-A, no ratification); we do not have the steady-state operational model for a high-genesis-rate swarm.

2. **The genesis ↔ replication ↔ federation interaction surface.** A genesis-spawned role that requests replication routes to Prajapati and can never mint its own token (doc 12 ↔ 15); a treaty that requires a worker role has the Inter-Swarm-Envoy request it through the internal allocator under scoped tokens, never a direct federation egress (doc 14 ↔ 12); revocation/quarantine propagation across a **federated AND self-replicated** peer population, and preventing reputation/identity inheritance from laundering trust to unaudited replicas of a partner swarm, is only sketched (doc 15 OP8, doc 14 OP7). The three-way interaction is the least-specified region of the evolution.

3. **Anti-collusion among synthesized (not pre-vetted) roles.** Cooperation-vs-collusion separation for emergently-bred agents that may share latent failure modes is an Indra's-Net-specific open problem (doc 12 OP9). The cross-run mutual-information check over observer streams and the diversity metric mitigate but do not close it — roles built on the same base model can look differentiated while failing identically (the doc-01 §16.4 residual, inherited).

4. **Provable-monotone-safety coverage across composed meta-edits.** The replication plane's R4 ("no meta-edit raises R_eff≥1 or weakens the floor invariant") and the genome's INVARIANT-region boot check both reduce to the same open formal-methods problem doc 03 §15.3 names for the policy engine: proving that a *large composed set* of rules admits no budget-escaping or floor-weakening path under **all** compositions. A bypass anywhere defeats the guarantee. We enforce per-edit checks and a fail-closed boot verifier; we do not have a whole-composition proof.
