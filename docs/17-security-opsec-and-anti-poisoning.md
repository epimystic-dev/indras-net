# 17. Security, OpSec & Anti-Poisoning Defense — the *Rakshakavaca* Layer

> **Rakshakavaca** — "the protective armor." This is the hardened seventh ring around the swarm: the operational deepening of the threat model (doc 09) into a buildable defense stack against actors who try to *poison* or *misuse* Indra's Net. It is owned operationally by **Aegis** at the chokepoint (doc 08), with three role partners — **Kaal-Bhairav** as the deterministic security boundary, a distinct **falsifier/red-team** function as standing adversary, **Dhanvantari's** immune fleet (doc 06), and **Chitragupta's** audit fabric (doc 04).
>
> *Role names are archetypal coordination/ethics semantics paired with a plain functional gloss — not religious claims, and offered with humility toward the living traditions that hold them.*

---

## 17.0 What this layer is, and the one distinction that organizes it

This subsystem does not introduce a new chokepoint. It *deepens* the agent→tool seam already specified in doc 08 §8.2 with the controls that the 2024–2026 attacker-side evidence forces. Its entire architecture rests on **one honest distinction the evidence makes unavoidable**:

> **DETERMINISTIC chokepoints do the load-bearing security work. PROBABILISTIC detectors are early-warning only and are *never* a security boundary.**

This is not a stylistic preference; it is the same trusted-root discipline doc 08 §8.1 already states (only deterministic, non-probabilistic components are in the trust root; monitors *multiply* the trusted-monitor assumption, they do not *escape* it). The published evidence is blunt: **"The Attacker Moves Second" bypassed all 12 evaluated prompt-injection defenses at >90% attack-success rate (ASR)**, and the best fine-tuned defenses still leave ~1% ASR — unacceptable at swarm scale. A classifier, a "better prompt," or a spotlighting wrapper is therefore *cheap suspicion*, fed to Dhanvantari's immune system, and it may sharpen how much human attention an action earns — but it may never convert a deterministic `BLOCK` into an `ALLOW`.

The **single highest-leverage move** in this layer is to promote v1's already-written `quarantined:*` trust-labels (doc 03 §1 trust-label taxonomy; doc 06 `MemoryItem.trust_label`; doc 09 A6) from *documentation* into a **runtime information-flow-control (IFC) taint lattice** (the CaMeL / FIDES pattern), wired as deterministic clauses of the *existing* Yama floor. This is the rare case where a constitutional principle ("instructions in observed content are never grounds for action") and the strongest published injection defense are **the same object** — and it holds even when the underlying model is injectable, because the model provably cannot separate instructions from data in one token stream.

Around that taint core this layer wires six more components and five protocols. The honest headline, repeated everywhere it matters: **this layer cannot make prompt injection or model poisoning *solved* — no one can.** Provenance proves *origin*, not *safety*; ~250 poisoned documents backdoor any model regardless of size (Souly et al. 2025, arXiv:2510.07192; see docs/REFERENCES.md A4); injecting 5 texts per target question into a knowledge base of millions of texts (~0.0001%) poisons RAG at ~90% ASR (up to 99%) (Zou et al. 2024, "PoisonedRAG", arXiv:2402.07867; see docs/REFERENCES.md A5). The contribution is the **coherent composition** that bounds residual risk, makes the cheap direction the safe direction, and renders poisoning *recoverable* where it cannot be prevented — not any single mechanism.

### 17.0.1 Dependency note — what this layer SUPPLIES vs. what it CONSUMES from the evolution spine (binding)

Parts of this document reference a **Replication Authority**, a two-plane **guild / role-genesis engine**, and a **signed persona-triad genome** (SOUL / INSTRUCTIONS / IDENTITY). **These are introduced by the evolution-spine subsystems (forthcoming docs), NOT by v1 docs 00–11.** A reviewer cross-checking the v1 doc set will correctly find that the strongest v1 analogue is the *role-from-stub* promotion pipeline (doc 01 §8), where a role is born as a zero-capability `RoleStub` and earns grants through a Class-B maker-checker gate — a *weaker* mechanism than the Charter→Genesis→Trial→Promote engine and quorum-cosigned Replication Authority the evolution spine assumes.

We mark the boundary explicitly, exactly the way doc 06 §12.2 brackets its MVP-vs-research cut line:

| Reference in this doc | Status | Honest grade |
|---|---|---|
| IFC taint lattice, Rule-of-Two, egress confinement, provenance admission, topology R<1, deception fleet | **Ships v1** — extends docs 03/04/06/08 directly | Buildable now |
| Persona-triad signing + floor-region boot check | **Forward contract** — this layer supplies the signing/attestation primitive; the *consumer* (genesis) is evolution-spine | Primitive buildable now; consumer deferred |
| Replication Authority as a quorum-cosigned crown jewel | **Forward contract** — this layer supplies the quorum/witness-cosign + provenance + identity primitives a replication-control plane will depend on | Stated as a forward contract, **not** a citation of an existing v1 role |

**Wherever this layer names the Replication Authority as a crown jewel to immunize, it is stating a forward contract** — "if/when the evolution spine lands a replication-control plane, these are the primitives it MUST consume" — not asserting an existing v1 interface. The most safety-critical such contract is stated in full in §17.8.

---

## 17.1 Threat-Actor Taxonomy (eight classes, T1–T8)

Doc 09 catalogues seven *adversary* classes (A1–A7) ordered from single-agent to systemic. This layer extends that with eight *misuse/poisoning-specific* **threat-actor** classes the deepened 2025–2026 evidence surfaces, each mapped onto the load-bearing control leg and the honest residual. The mapping to A1–A7 is faithful (T1↔A6 injection surface; T2/T3↔A3 poisoned skill/memory; T7↔A5 captured human; T8↔inter-swarm).

| Class | Actor | Entry surface | Primary control leg(s) | Last-line control | Honest residual |
|---|---|---|---|---|---|
| **T1** | **Prompt-injector** (direct *and* indirect — injection rides in observed content: web page, file, tool output, RAG chunk) | any datum entering an occasion's context | **IFC taint lattice** (injected-from-quarantined is non-actionable at the deterministic PEP) | Rule-of-Two human gate | a *legitimately-needed* quarantined value forces a declassification gate — the new attack surface (§17.2.3) |
| **T2** | **Memory / skill / RAG poisoner** (backdoor / sleeper / false-fact into semantic memory, a `SKILL.md`, or a retrieval corpus) | write-time ingest | write-time quarantine + provenance-gating + doc 06 promotion pipeline + canary-scan | influence-trace targeted revert (§17.7) | ~5 docs poison RAG at 90–98% ASR; **recoverable, not preventable** |
| **T3** | **Model / data supply-chain attacker** (backdoors a model with ~250 docs, or a training dataset) | model/dataset admission | signed model-transparency admission + canary-trigger scanning + two-tier detection contract (doc 08 §8.8) | revert-to-prior-attested-model | a faithfully-signed poisoned model **verifies perfectly** — provenance proves origin not safety; **only partially covered** |
| **T4** | **Sybil / eclipse infiltrator** (floods cheap identities, or surrounds a target agent's view) | identity / topology | DID/VC attestable identity (Sybil cost) + sparse corroborated topology (eclipse needs a corroboration quorum) | autonomy demotion on anomaly | cold-start reputation + coordinated rating-rings remain partially open (doc 04 §4.15) |
| **T5** | **Agent-hijacker / confused-deputy** (turns a credentialed agent into the attacker's tool — the **dominant agentic-specific risk**) | a credentialed occasion | **Rule of Two** (caps at two of {untrusted-input, sensitive-access, state-change}) + capability-VC scoping + IFC on the state-change leg | human gate on the 3-leg case | excessive-agency under a *legitimate* declassification grant |
| **T6** | **Exfiltrator / model-extractor** (pulls secrets or weights out) | egress | confidentiality labels in the taint lattice + egress allowlists + no-keys-in-model custody (doc 04 §4.6) | deterministic egress BLOCK | timing/size side-channels + DNS/Unicode-tag covert channels (doc 09 carries) |
| **T7** | **Social-engineer** (manipulates the human reviewer or policy author — couples to doc 09 A5) | the HITL gate / policy authorship | **HITL shows the ACTUAL low-level op** + cryptographic role-separation + out-of-swarm escalation | out-of-swarm review (doc 08 §8.13(2)) | an uncorruptible reviewer is *assumed*, not provided |
| **T8** | **Malicious external swarm** (a hostile peer federation — couples to inter-swarm subsystem) | the relay/firewall boundary | relay/firewall + ecosystem-benefit checked invariant + floor-as-admission-precondition | progressive disclosure scoped to verified tier | relay-architecture injection amplification (handed to inter-swarm) |

`ThreatActorProfile` records are maintained by the **falsifier/red-team function** (§17.9) and consumed by the eval harness (doc 08 §8.11) and the immune monitors.

```
ThreatActorProfile {
  actor_class:        enum{T1..T8}
  entry_surface:      string
  primary_control_legs: [leg_id]      // {taint, egress, capability, provenance, identity, topology, rule_of_two, hitl}
  last_line_control:  leg_id
  residual_ref:       doc§ref
  observed_iocs:      [indicator]
}
AttackObservation {                    // appended via Chitragupta as an OBSERVE / REPARATIVE record
  actor_class, surface, taint_labels_at_block, blocked_by_leg, ts, evidence_cid
}
```

---

## 17.2 The IFC Taint Lattice — the load-bearing prompt-injection defense

This is the single highest-leverage change in the subsystem. It promotes v1's `quarantined:*` doctrine into a runtime IFC enforcement layer, and wires it as **deterministic clauses of the existing Yama floor (doc 08 §8.2 stage-(a))** — *no new chokepoint is introduced.* It holds even when the underlying model is injectable.

### 17.2.1 Labels and the lattice order

Every datum entering an actual-occasion's context carries a `TaintLabel` with two independent components:

- **INTEGRITY** — a lattice over the v1 trust labels: `trusted_audited > observed > quarantined`. **Quarantined-by-default** for anything tool-/web-/peer-/RAG-derived, or any imported skill/persona file. `observed` is the *admitted-but-unaudited* middle (signed, origin-known, not yet through the full promotion pipeline). `trusted_audited` is reached **only** after the full doc 06 promotion pipeline (origin proven AND poison-scanned).
- **CONFIDENTIALITY** — `public < internal < secret < key`.

The lattice ordering is the safe-by-default invariant:

```
 INTEGRITY (flows DOWN under combination — LEAST integrity wins)
   trusted_audited
        │
     observed
        │
    quarantined         ← anything tainted-by-quarantined STAYS quarantined, mechanically

 CONFIDENTIALITY (flows UP under combination — HIGHEST sensitivity wins)
   public ─ internal ─ secret ─ key
```

Derived data takes the **least-upper-bound (lub)** of its inputs' labels. Any value computed with a quarantined input is itself quarantined — *regardless of what the model "believes" it did with that input.* This is the mechanical property that defeats T1: the model can be fully injected and still cannot launder a quarantined instruction into an actionable trusted one, because the label propagation is in the deterministic trusted root, not in the model.

```
TaintLabel {
  integrity:       enum{trusted_audited, observed, quarantined}
  confidentiality: enum{public, internal, secret, key}
  provenance_dids: [DID]              // who/what this datum descends from
  source_cids:     [CID]              // the exact bytes it descends from (CID-on-read, doc 04 §4.5)
}
TaintedValue { value_cid, label:TaintLabel, derived_from:[TaintedValue.cid] }

lub(a, b) = TaintLabel {
  integrity:       min(a.int, b.int),         // least integrity wins
  confidentiality: max(a.conf, b.conf),       // highest sensitivity wins
  provenance_dids: a ∪ b,
  source_cids:     a ∪ b
}
```

### 17.2.2 The deterministic enforcement point

On every tool call and every high-impact action, the PEP — the **same Yama OPA/Rego floor at the same seam** — evaluates `(capability, args, arg_taint_labels)` and returns one of `ALLOW / BLOCK / ASK_HUMAN`. Two model-agnostic deterministic kills illustrate the power:

- A `send_email` whose recipient or body carries `integrity=quarantined` and the capability is consequential → **cannot ALLOW** without declassification or a Rule-of-Two human gate.
- A tool whose args carry `confidentiality=secret` but whose egress target is `public` → **BLOCK** — a deterministic exfiltration kill, independent of model behavior.

```
IFCPolicyDecision {
  action_id, capability,
  arg_labels:          [TaintLabel],
  verdict:             enum{ALLOW, BLOCK, ASK_HUMAN},
  rule_id,
  declassify_grant_ref: ref?          // present only if a declassification authorized this
}
```

Probabilistic spotlighting / PromptGuard-class classifiers / MELON masked-execution run **upstream only** as cheap suspicion signals feeding the immune system (doc 06 §7.1, doc 08 §8.3). **They never change a BLOCK to an ALLOW.** The taint check is deterministic, reproducible, and in the trusted root (doc 08 §8.1); the classifiers are explicitly not.

### 17.2.3 Declassification — and the throughput model that keeps a knowledge swarm alive (red-team major, resolved)

A research/knowledge swarm's *primary job* is acting on observed web/RAG content. If every consequential action that touched `observed` data routed to a human, the swarm deadlocks (the fail-closed-availability SPOF of doc 08 §8.13(2), now multiplied) — or, worse, operators paper over the deadlock with a broad, frequently-exercised declassification grant that becomes precisely the confused-deputy steering surface (T5) the lattice was meant to remove. We resolve this by **calibrating the declassification throughput to mirror doc 06 §7.4's fail-closed-cold-start posture**, and by sharply distinguishing the *common* case from the *dangerous* case:

| Integrity of the arg | Meaning | Required to act on it |
|---|---|---|
| **`observed`** | admitted, signed, origin-known, **unaudited** — the common case | **No human declassification gate** when the Rule-of-Two count ≤ 2 **and** criticality ∉ IRREVERSIBLE. The deterministic capability + Rule-of-Two controls suffice; the human gate is reserved for the genuine 3-leg / Class-C/D case. |
| **`quarantined`** | unsigned / failed-provenance / injection-suspected — the dangerous case | **Governance-gated, named-falsifier `Declassifier` only.** Raising integrity is never free. |

This is the load-bearing calibration: it keeps the human gate scarce (reserved for Rule-of-Two-violating / Class C-D actions), throttles via the `human-gate-saturation` vital sign (doc 06 §7.4 — when the backlog exceeds capacity, the safe response is to **slow the Tier-0 promotion rate, never widen the grant**), and confines the governance-gated path to genuinely-untrusted (`quarantined`) data.

```
Declassifier {
  from_label, to_label,                // raising integrity OR lowering confidentiality
  gate:           enum{CLASS_C, CLASS_D},
  named_falsifier: string,             // the condition under which this declassification is WRONG
  witness_cosigs: [WitnessSig],
  scope:          { capability_pattern, resource_pattern, ttl }   // narrowest viable, append-only-tightenable
}
```

**Fail-safe asymmetry threaded through:** demotion of trust (quarantining a value, lowering integrity) is **always free and immediate**; promotion (raising integrity / lowering confidentiality) is governance-gated, append-only, and carries a named falsifier. This is the *same* invariant the rest of Indra's Net applies to humans, machines, and artifacts.

---

## 17.3 Universal Provenance-Gating & Signing Admission (anti rug-pull)

This extends doc 08 §8.11(d) supply-chain admission **from tools to ALL ingested/shared artifacts**, reusing Akasha-Sutra (doc 04). The novelty is not the signing — Sigstore/in-toto/SLSA/model-transparency all pre-exist — but the *universality* (persona/skill files included) and the *anti-rug-pull re-approval teeth*.

### 17.3.1 The admission rule, **tiered by artifact class** (red-team minor, resolved)

A flat "verify a full in-toto + SLSA + Sigstore bundle before loading EVERY rag_chunk and EVERY memory_write" would impose a per-retrieval signing tax inconsistent with doc 08 §8.10's criticality-tiered discipline and doc 04 §4.5's "only commitments go in the log." Worse, most RAG corpora carry **no** upstream Sigstore provenance, so a flat rule would land *all* of them quarantined and starve the knowledge swarm. We therefore tier the provenance requirement the same way monitor cost is tiered:

| Artifact class | Provenance required | Lands at integrity |
|---|---|---|
| **Model, dataset, tool, skill, persona-triad** | full in-toto + SLSA-level ≥ required-for-criticality + Sigstore (Fulcio cert + Rekor entry) [+ model-transparency for model blobs] | `trusted_audited` **only after** the full promotion pipeline; else `observed`/`quarantined` |
| **Self-originated memory write** | cheap **DID/SVID signature** (the writer's own attested identity — near-zero cost) | `observed` |
| **Externally-sourced RAG chunk** | **CID + source-DID provenance** (not a full bundle) | `observed` if source-DID known; **`quarantined`** if no provenance — **still usable, tainted**, never refused |

The binding correction to the original over-broad rule: **"no Sigstore provenance" = quarantined-and-still-usable-tainted, NOT refused.** The IFC lattice (§17.2), not a refusal-to-load, is what makes an unprovenanced RAG chunk safe — it simply cannot drive a consequential action without a declassification gate. A *signature mismatch* or a *failed attestation chain on an artifact that claimed one* is a different matter: that is REFUSED (fail-closed) and the artifact lands `quarantined` with an alarm.

### 17.3.2 The anti-rug-pull re-approval gate (the teeth)

A signed tool/skill/persona manifest is **content-addressed (CID)**. **Any change to the manifest** — a tool-description edit, a skill-body diff, a persona-triad field change — invalidates the prior approval and forces RE-APPROVAL through the doc 06 promotion pipeline (static analysis → sandbox dynamic check → behavioral verification → safety battery → witness verification → Yama-class review) plus a canary-trigger scan. A diff-and-re-approve gate plus static hidden-instruction scanning catches the documented **~5.5%-of-MCP-servers poisoned-metadata** class and the CVE-class description-swap attacks. At **every subsequent invocation**, the loaded artifact's CID is re-checked against the attested CID — a mismatch BLOCKS execution, which simultaneously catches post-approval mutation *and* a known stale-cache / truncation corruption class (consistent with doc 04 §4.5 CID-on-read, doc 08 §8.11(d)).

```
ArtifactAttestation {
  artifact_cid, kind: enum{model,dataset,memory_write,rag_chunk,tool,skill,persona_triad},
  in_toto_layout?, slsa_level?, sigstore_bundle?, model_transparency_ref?,
  verified: bool, admitted_label: TaintLabel
}
ManifestApproval {
  manifest_cid, approver_did, gate_passed, canary_scan_verdict,
  approved_ts, supersedes_cid?
}
RugPullAlarm {
  manifest_cid_old, manifest_cid_new, changed_fields,
  re_approval_required: true,                 // hard block until re-approved
  routed_to: enum{PROMOTION_PIPELINE, VISHNU}  // crown-jewel manifests → Vishnu
}
PersonaTriadSig {                              // forward contract for the genesis consumer (§17.0.1)
  role_did, soul_cid, instructions_cid, identity_cid,
  floor_region_hash,                          // the INVARIANT region (floor) — uneditable
  boot_sig                                    // fail-closed: invalid floor_region_hash ⇒ NO BOOT
}
```

Because provenance proves origin not safety, admission is **always** combined with (i) canary-trigger scanning (probe the artifact with known trigger phrases before promotion), (ii) the IFC taint (an admitted-but-suspect artifact still runs tainted), and (iii) behavioral monitoring post-load.

---

## 17.4 Rule-of-Two HITL-Sizing Engine (+ Lies-in-the-Loop-hardened gates)

The Rule of Two gives the swarm an **objective law** for when a human gate is required, binding it to the existing Class A/B/C/D risk gates and reserving scarce human attention for genuinely dangerous actions. It is the primary counter to T5 (confused-deputy / excessive-agency — the dominant agentic risk).

### 17.4.1 The three legs, computed deterministically at the chokepoint

> **Rule of Two:** any single agent/operation may hold **at most TWO** of {processes-untrusted-input, accesses-sensitive-systems/capability, changes-external-state/irreversibility}. Holding **all three** requires either **DECOMPOSITION** (split across capability-isolated occasions so no one occasion holds all three) or a **HUMAN GATE**.

The three legs are computed from data the chokepoint *already holds* (doc 08 §8.2):

| Leg | Computed as | Source |
|---|---|---|
| **leg-1 untrusted-input** | `min(arg integrity) ≤ observed` | IFC taint lattice (§17.2) |
| **leg-2 sensitive-access** | capability-VC grants a `sensitive`/`secret`-confidentiality capability | doc 04 §4.6 CapabilityVC |
| **leg-3 state-change** | criticality `c ∈ {COSTLY, IRREVERSIBLE}` | doc 08 §8.4 resolver (ambiguity resolves UPWARD; unknown capability ⇒ IRREVERSIBLE) |

This composes cleanly with the IFC taint (leg-3's "changes external state" *is* the tool call the PEP already gates) and with the decomposition-window monitor (doc 08 §8.4), which catches salami attempts to launder a three-leg action through sub-threshold steps.

```
RuleOfTwoEval {
  action_id,
  leg_untrusted_input: bool,
  leg_sensitive_access: bool,
  leg_state_change: bool,
  count,
  verdict: enum{ALLOW, DECOMPOSE, HUMAN_GATE}     // count==3 ⇒ DECOMPOSE or HUMAN_GATE
}
```

### 17.4.2 Lies-in-the-Loop hardening — the binding gate-UI invariant

The **Lies-in-the-Loop** attack: an agent crafts a confident natural-language *summary* that gets a harmful low-level operation approved. The hardening is a binding rule on the gate protocol:

> The human gate MUST display the **ACTUAL low-level operation** — recipient, URL, payload, capability scope, and the taint labels of every arg — and **NEVER** a natural-language summary the agent generated. The agent's explanation MAY be shown, but it is itself **tainted** (model-generated) and is never the thing approved. **The human signs over the CID of the rendered low-level `ActionEnvelope`**, so an approved-then-mutated action trips a CID mismatch.

```
HumanGatePresentation {
  action_id,
  low_level_op: { capability, recipient, url, payload_cid, scope, arg_taint_labels },
  agent_explanation_cid_TAINTED,        // shown for context; NEVER the approved object
  approved_action_cid,                  // == CID(low_level_op); the approver signs THIS
  approver_did, approver_sig
}
// BINDING INVARIANT: approver_sig is over CID(low_level_op), never over agent_explanation_cid_TAINTED.
```

HITL is rationed to Rule-of-Two-violating / Class C-D actions only, so the human gate does not fatigue into rubber-stamping — coupling directly to doc 06 §7.4's `human-gate-saturation` vital sign.

---

## 17.5 Topology-as-Security Controller (sparse mesh, R<1, hub immunization)

For a swarm, **the network is the attack surface**: a single compromised agent infects peers, and dense/star topologies amplify spread above the percolation threshold. This controller treats the inter-agent contact graph as a security parameter, holding compromise-percolation **R < 1** and applying the strongest controls to the highest-influence hubs (the robust-yet-fragile prime targets). All three mechanisms reuse v1 substrate.

**(1) Sparse + mesh-corroborated graph.** The salience-gated surprise-only bus (doc 08 §8.10, doc 05 the Mandala) is already sparse. This layer adds: **any HIGH-IMPACT claim must be independently cross-agent / cross-source corroborated before it propagates or triggers action.** A single agent's high-impact assertion cannot cascade un-corroborated — wiring the doc 09 A2 / MAST cascading-failure vector (inter-agent misalignment ≈ 32% of failures) into propagation control.

**(2) Percolation-bounded R<1.** Model compromise spread as a branching process where an agent's **degree = message-influence × trust-weight** (NOT raw edges). The controller monitors an estimated compromise-reproduction-number and, on any rise toward 1, sheds edges / inserts corroboration hops / quarantines suspect nodes to push R back sub-critical. This is the quantitative reformulation of v1's "shard the workspace" anti-pattern, and it sits as a new Dhanvantari vital sign (doc 06 §7.2) alongside the criticality-exponent set-point — with a **deliberate tension named honestly**: COMPUTATION wants near-critical (doc 06 criticality-exponent ~1.5), CONTAGION wants strictly sub-critical. **The contagion graph is held strictly sub-critical (R<1) while the computation graph may run near-critical — and they are NOT the same graph, though they share nodes.**

```
                CONTAGION graph (held R<1)          COMPUTATION graph (may run near-critical)
                ─────────────────────────           ────────────────────────────────────────
   shared       held sub-critical: shed edges,       near-critical for adaptivity (doc 06 §7.2)
   nodes ──────▶ corroboration hops, hub             power-law avalanche ~1.5 set-point
                immunization                          ▲ TENSION: same nodes, opposite set-points
                                                      └─ uncalibrated (§17.10 open problem #4)
```

**(3) Targeted hub immunization.** The highest `message-influence × trust-weight` agents — typically the orchestrator **Shiva** and synthesis **Saraswati** (doc 01 §301, doc 08 §8.14), plus any high-fan-out coordinator — receive the **strongest** controls: hardest sandbox (microVM, §17.6), mandatory IFC, lower autonomy class, monitoring multiplier, and **sharding** so no single hub node concentrates compromise. **Crown-jewel nodes** (the forward-contract Replication Authority per §17.0.1; the Policy Engine / Yama; the credential issuer; the Chitragupta writer) are **quorum / witness-cosigned** (doc 04 §4.4) so no single node can defeat recall or forge authority.

```
ContactGraphHealth {
  estimated_R, max_hub_degree,                 // influence × trust_weight
  corroboration_required_above_impact: threshold,
  status: enum{SUBCRITICAL, WATCH, SUPERCRITICAL}
}
HubImmunizationPolicy {
  hub_did, influence_trust_weight,
  controls: { sandbox_tier: microVM, mandatory_ifc: true, autonomy_cap, monitoring_multiplier },
  sharded: bool
}
CorroborationRequirement {
  claim_cid, impact_class, corroborating_dids_required: int,
  corroborating_evidence: [{did, evidence_cid}], propagation_gated: bool
}
CrownJewelGuard { node_role, quorum_t_of_n, witness_cosign_required: true }
```

**Fail-safe estimation rule (red-team safety risk, addressed):** because R-estimation under partial topology knowledge is itself an uncalibrated safety-critical parameter (doc 06 §12.3), the binding mitigation is doc 06 §7.4's fail-closed posture — **on uncertainty in the R estimate, default to MORE corroboration hops and tighter hub sandboxing, never fewer.** A sustained `SUPERCRITICAL` reading escalates to Vishnu.

---

## 17.6 Sandbox & Egress Confinement Plane (microVM/WASM + allowlists + least-privilege)

Shared-kernel containers are no longer a safe default (real escapes are documented), and broad egress is the exfiltration highway. This plane extends doc 08 §8.11(c)'s worktree-per-task isolation to a **tiered, threat-matched substrate behind one swappable, vendor-neutral controller** (kubernetes-sigs/agent-sandbox-style). It stops **code-ESCAPE**; it explicitly does **NOT** stop logic-layer prompt-injection abuse — that is the taint lattice's job. **The two are paired; neither alone suffices.**

```
 risk of the occasion        sandbox tier          network              credential
 ──────────────────────      ──────────────        ────────────────     ──────────────
 bounded per-tool compute    WASM/WASI             none (default)       short-lived SVID
   (cap-deny-by-default)      (sub-ms; caps map                          (~15-min rotation,
                              1:1 onto IFC tokens)                        doc 04 §4.6)
 medium-risk untrusted exec   gVisor                egress allowlist     short-lived SVID
 replication-capable /        Firecracker / Kata    egress allowlist     short-lived SVID
   credential-touching /        microVM             + ephemeral teardown  (TEE/HSM signer
   self-evolved code          (hardware-grade iso)                        re-checks capability)
```

Every sandbox runs default `--network=none` + an **egress allowlist** (TLS-SNI + DNS filtering) + ephemeral teardown + short-lived scoped SVID credentials. Egress allowlisting is the **cheapest high-value control**: it deterministically kills naive exfiltration regardless of model behavior. Least-privilege capability confinement grants only the minimal verb+resource set; the TEE/HSM signer re-checks capability membership before signing (doc 04 §4.6), so a jailbroken model cannot act out-of-capability or exfiltrate its key.

**This plane is REQUIRED for the meta-evolution loop (doc 06):** self-modified agents/skills run sandboxed + provenance-gated + archive-rollback-backed. An unsandboxed self-modification path is how a drifting agent rewrites the swarm, and the doc 06 AVOID list forbids it.

```
SandboxAssignment {
  occasion_did, tier: enum{WASM, gVisor, microVM},
  network: enum{none, allowlist}, egress_allowlist: [{sni, dns}],
  svid_ttl, teardown: enum{ephemeral}
}
EgressAttempt {
  occasion_did, target, arg_confidentiality: TaintLabel,
  allowlisted: bool, verdict: enum{ALLOW, BLOCK}
}   // BLOCK on non-allowlisted target OR on confidentiality>internal to a public target
CapabilityConfinement { occasion_did, granted_verbs: [verb], resource_scope, deny_default: true }
```

### 17.6.1 On the "two independent exfiltration boundaries" claim (red-team minor, qualified)

The confidentiality-label egress check and the egress allowlist are **independent against *different* failure modes**, but they share an upstream dependency we state plainly:

| Failure mode | Allowlist defeats it? | Confidentiality-label check defeats it? |
|---|---|---|
| Exfil to an arbitrary non-allowlisted target | **Yes** (regardless of label) | no |
| Exfil to an allowlisted-but-wrong-sensitivity target | no | **Yes** |
| A single upstream **mislabel** (a `secret` datum mislabeled `internal`) that the egress target happens to allowlist | **No** | **No** — both pass |

So the two checks are *not* flatly "two independent boundaries." They decorrelate against allowlist-gaps and against label-errors *separately*, but both rest on **correct confidentiality labeling at ingest**. The binding consequence: a **label-confidence signal is routed into the detection fleet (§17.7)** as a first-class suspicion input, and ingest-time labeling errors are treated as a monitored fault class, not an assumed-away one.

---

## 17.7 Deception & Detection Fleet (canaries, honeypots, influence-tracing, anomaly detection)

DID/VC authenticate *identity*, but a valid credential on a **hijacked** agent still passes authentication. This fleet catches the credentialed-but-compromised insider and detects infiltration/lateral-movement cheaply, feeding the doc 06 §7.1 four-pathway monitors and doc 08 §8.3 ensemble. **This is the PROBABILISTIC early-warning ring, honestly labeled: it raises the cost of compromise; it is never a boundary** and never holds ALLOW/BLOCK authority.

**(1) Canary tokens / known-answer probes** — drawn from the **real task distribution** (doc 06 §10.1 — *never* a recognizable "please pause" template) and seeded into memory, RAG corpora, and skill libraries. A fired canary (a planted fake credential used, a honeytoken document accessed) is high-signal evidence of a poisoner/exfiltrator.

**(2) Honeypot agents** — decoy occasions advertising tempting capabilities; interaction flags an infiltrator/lateral-mover. Honest residual: skilled reasoning attackers can spot decoy inconsistencies, so honeypots are co-evolved by the falsifier/red-team function and never relied on alone. **Safety constraint (red-team safety risk, addressed):** a honeypot is itself a credentialed occasion and therefore a *new* attack surface if compromised — so **every honeypot runs at the LOWEST autonomy class (`OBSERVE_ONLY`/`GATED_LOW`, doc 08 §8.8), holds NO consequential capabilities, and is microVM-isolated.** A compromised decoy cannot become a real foothold.

**(3) Influence-tracing for poison provenance** — when a bad output/behavior is identified, trace back through the taint lattice's `provenance_dids` + `source_cids` and the Archive lineage (doc 06 §5) to find which ingested artifact / memory-write / skill seeded it, enabling **targeted revert-to-known-good** rather than blanket rollback. This is the forensic that makes the ~250-doc-backdoor / ~5-doc-RAG-poison threats **recoverable** even though they are not *preventable*.

> **Honest scoping of the recoverability claim (red-team minor, resolved).** Influence-trace + targeted-revert can only follow edges that **exist in the runtime taint lattice**. It is load-bearing for poison that entered **through the swarm's own ingestion / memory / RAG / skill surface** (T2) — there, provenance edges exist and datum-level targeted revert works. For a **model-training-time backdoor (T3)**, the lineage points to the *(verified)* model, not to the ~250 poison docs upstream of training — *outside the swarm's provenance graph entirely* — so recoverability degrades to **model-level revert-to-a-prior-attested-model + canary re-scan**, not datum-level revert. For an **untriggered sleeper**, the trigger never fired, so there may be no causal edge to trace; recoverability there is **weaker than for fired poison**, consistent with doc 09 A3's "largely unsolved" residual. We state this asymmetry at the headline, not only in open problems.

**(4) Behavioral anomaly detection** — on tool-call patterns, embedding-consistency vs role baseline (anchored to a **frozen** Archive node, doc 06 §5, never recent drifted behavior), and the doc 06 graph-of-agents temporal anomaly detector — distinguishing legitimate autonomous adaptation from slow goal-corruption.

All four are wired so a *substantiated* finding (a) **taints** the implicated data/agent (free demotion), (b) lowers autonomy class, (c) **freezes drift-aware aging** on the relevant records (doc 04 §4.10) for forensics, and (d) escalates a high-confidence catastrophic finding to **Vishnu halt + human review**.

```
Canary       { canary_cid, kind: enum{honeytoken_doc, fake_credential, known_answer_probe},
               planted_in: enum{memory, rag, skill, tool}, fired: bool, accessor_did? }
Honeypot     { decoy_did, advertised_caps, autonomy_class: LOWEST, consequential_caps: [],   // empty, binding
               sandbox: microVM, interaction_log: [{peer_did, ts}], co_evolution_version }
InfluenceTrace { bad_output_cid, traced_sources: [{artifact_cid, provenance_dids, ingest_ts}],
                 suspected_poison_cid, targeted_revert_node: CID,
                 recoverability: enum{DATUM_LEVEL, MODEL_LEVEL, DEGRADED_SLEEPER} }      // §17.7 scoping
CompromiseSignal { subject_did, detector: enum{canary, honeypot, influence_trace, behavioral},
                   severity, routed_to: enum{IMMUNE, VISHNU}, evidence_cid }
```

---

## 17.8 OpSec Discipline & the Self-Replication Forward Contract

### 17.8.1 OpSec discipline (deterministic where it can be, monitored where it cannot)

| Rule | Mechanism | Fail direction |
|---|---|---|
| Secrets/keys never enter model context | credential use brokered out-of-band by the TEE/HSM signer (doc 04 §4.6, doc 08 §8.10) | deterministic — closed |
| Two independent exfiltration checks | confidentiality labels + egress allowlists (§17.6.1 caveat carried) | deterministic — closed |
| Audit metadata steganalyzed as a covert channel | ULID timing, ref-graph structure, salt entropy (doc 04 §4.9) | monitored |
| Least-privilege by default | append-only tightening; named-falsifier-gated loosening (doc 08 §8.15) | deterministic — closed |

```
OpSecInvariant { rule_id, statement, enforcement: enum{deterministic, monitored},
                 fail_direction: enum{closed, open_with_shadow} }
```

### 17.8.2 Self-replication — the binding redline this layer carries for its consumer (safety-critical)

This subsystem does **not** own replication — that is the evolution-spine's plane (§17.0.1). But because this layer **supplies the provenance / identity / quorum / taint primitives that a replication-control plane MUST consume**, a gap or mislabel *here* would silently break the replication safety guarantee. We therefore state the redline binding on *whatever consumes these primitives*:

> **Self-replication MUST be gated, never-autonomous, and sub-critical-by-construction.** A quorum-cosigned **Replication Authority** (a crown-jewel node per §17.5, quorum/witness-cosigned) issues capability-scoped, generation-counted, lease-bound, DID/VC-attested spawn tokens against a global compute/budget ceiling. **A replica carries NO self-sufficient blueprint and CANNOT mint its own spawn authorization or survival credential.** Lineage-wide effective reproduction **R_eff < 1** (each token authorizes on average <1 child) + a finite generation cap that depletes ⇒ provable percolation-boundedness. The "vitamin"/lease + dead-man toxin-antitoxin recall is enforced **EXTERNALLY by the sandbox/credential plane** (a replica cannot disable its own kill-switch); per-replica microVM isolation + egress allowlists + fail-closed key lockdown.
>
> **RED-LINE:** replication MUST NOT be coupled to an open fitness/selection loop. (Tierra/Avida show replication + heredity + variation + selection spontaneously breeds parasites/reward-hacking.) **Every spawn is metered and attested. A single un-metered or un-attested spawn channel is hostile-by-definition and breaks the entire guarantee.**

The primitive this layer *delivers* to make the redline enforceable is the `PersonaTriadSig` fail-closed boot check (§17.3.2): **an invalid `floor_region_hash` ⇒ no boot.** A replica whose persona-triad floor-signature check is skipped, or a spawn-token manifest that escapes the CID-re-check, would silently breach the guarantee — so both are bound into the anti-rug-pull invocation-time CID re-check (§17.3.2) and routed to Vishnu on mismatch (RugPullAlarm on a crown-jewel manifest). The most safety-critical composition in this layer is exactly this: the spawn-token manifest and the replica persona-triad are *artifacts under the universal provenance-admission rule*, so they inherit the CID-on-every-invocation re-check and the fail-closed boot signature check by construction.

---

## 17.9 Roles: Kaal-Bhairav as boundary, the Falsifier as adversary, and the separation-of-duties invariant (red-team major, resolved)

v1 defines **Kaal-Bhairav** as the **deterministic security-boundary IMMUTABLE role** — trust-label enforcement, quarantine, prompt-injection defense at relay edges, identity & capability-VC verification (doc 01 §293; doc 03 §102/§409/§463). Doc 06 §250 separately references a "Kaal-Bhairav-aligned" *falsifier/red-team*. Casting the **same** role as both the boundary-enforcer **and** the adversary that earns reputation for *breaking* that boundary is a separation-of-duties violation (the defender grading its own breakage). We resolve it explicitly, mirroring doc 01 §295's "no persona may simultaneously hold Yama-enforce and Chitragupta-write."

**Resolution — two distinct functions, a hard SoD invariant by VC issuance:**

| Function | Role | Holds | Cannot hold |
|---|---|---|---|
| **Security boundary / IFC enforcer** | **Kaal-Bhairav** (IMMUTABLE, doc 01/03) | `ifc.enforce`, `trust_label.verify`, `identity.verify` capability VCs | any red-team-authoring or red-team-scoring VC |
| **Standing adaptive adversary** | **Falsifier function** (the doc 06 §6.2 falsifier/red-team; explorer high-c1, doc 01 §11) | `redteam.author`, `redteam.execute`, `redteam.score` against a sandboxed replica | any `ifc.enforce` / boundary-enforcement VC |

> **SoD invariant (binding, enforced by VC issuance, not by prompt):** the boundary-enforcer (Kaal-Bhairav) **cannot author or score** the red-team campaigns that grade it; the red-team campaign results **must be cosigned/adjudicated by a party with no boundary-enforcement credential.** This is the exact structural pattern doc 01 §295 uses for the maker-checker checker (Narasimha must be a different persona with no trust-edge dependency on the maker).

The phrasing throughout the rest of this doc honors the split: where §17.1/§17.9 say "maintained by the falsifier/red-team function," that is the adversary; where the IFC enforcement and relay-edge boundary are described, that is Kaal-Bhairav.

### 17.9.1 The standing adaptive red-team loop

The falsifier function runs **scheduled + randomized adaptive attacks across all eight threat-actor classes** against a sandboxed replica of the swarm — and **the attacker KNOWS the protocol** (no security-through-obscurity). It feeds the safety-usefulness eval harness (doc 08 §8.11), which is **mandated to fit thresholds against a worst-case adaptive attacker** (doc 08 §8.7 binding rule — thresholds fit against a weak attacker are *mechanically rejected*). The falsifier earns reputation for **breaking a control**; a control with high recent breakage loses trust-weight and triggers re-design.

The composition discipline, stated honestly: **because no single layer has a security proof, the residual is bounded by REQUIRING an attacker to defeat MULTIPLE INDEPENDENT deterministic legs** (taint AND egress AND capability AND provenance). The probabilistic detectors only have to make that multi-leg defeat **noisier**, not impossible. Residual risk is reported as a **measured quantity** — ASR per actor class against the current adaptive battery — **never claimed to be zero.**

```
RedTeamCampaign { campaign_id, actor_classes_covered: [T1..T8], attacks_run,
                  controls_broken: [{leg_id, asr}], thresholds_invalidated: [profile_id],
                  adjudicated_by_did }   // SoD: NOT a boundary-enforcement credential
ResidualRiskReport { actor_class, measured_asr_vs_adaptive, legs_required_to_defeat: int,
                     bounded: bool }      // bounded=false is an HONEST admission, not a hidden gap
```

---

## 17.10 Protocols

### Protocol 17-A — Tainted-Action Admission (the hot-path IFC + Rule-of-Two gate)

Fuses the IFC taint check, the Rule-of-Two sizing, and the Lies-in-the-Loop-hardened human gate into the doc 08 §8.2 chokepoint pipeline. Deterministic except where it deliberately escalates to a human.

```
1. Agent emits an ActionEnvelope (doc 08); every arg carries a TaintLabel = lub of its source labels
   (integrity flows down, confidentiality flows up).
2. YAMA FLOOR (OPA/Rego, deterministic) runs FIRST, including the new taint clause:
   if any arg integrity=quarantined and the capability is consequential ⇒ cannot ALLOW
   without a Declassifier grant or a human gate.  FAIL is non-overridable.
3. CRITICALITY RESOLVER computes c (ambiguity resolves UPWARD; unknown capability ⇒ IRREVERSIBLE) — doc 08 §8.4.
4. RULE-OF-TWO eval:
     leg-untrusted-input = (min arg integrity ≤ observed)
     leg-sensitive-access = (capability-VC grants sensitive/secret)
     leg-state-change     = (c ∈ {COSTLY, IRREVERSIBLE})
   count==3 ⇒ DECOMPOSE or HUMAN_GATE.
   (observed-integrity data with count≤2 and c∉IRREVERSIBLE proceeds WITHOUT a human declassification gate — §17.2.3)
5. EGRESS check (if the action egresses): target on the allowlist AND no secret/key arg to a lower-confidentiality
   target — deterministic BLOCK otherwise.
6. DISPOSITION selector (doc 08 §8.7) runs on PASS; probabilistic monitor suspicion only sharpens
   DEFER/AUDIT — never converts a BLOCK to ALLOW.
7. If HUMAN_GATE: render the ACTUAL low-level operation (recipient, URL, payload CID, scope, arg taint labels) —
   NEVER the agent's NL summary; the human signs over CID(low_level_op).
8. EXECUTE; Chitragupta appends a signed ControlDecision + IFCPolicyDecision + RuleOfTwoEval;
   the randomized-audit sampler may flag an ALLOW for post-hoc review.
```

### Protocol 17-B — Universal Provenance Admission & Anti-Rug-Pull Re-Approval

```
1. Artifact (model/dataset/memory-write/rag_chunk/tool/skill/persona-triad) arrives with the provenance
   appropriate to its class (§17.3.1): full in-toto+SLSA+Sigstore for model/dataset/tool/skill/persona;
   DID/SVID for self-originated memory; CID+source-DID for RAG.
2. Runtime VERIFIES signature + attestation chain + SLSA-level ≥ required-for-criticality BEFORE loading.
   A *claimed* attestation that FAILS ⇒ REFUSE (fail-closed), land at integrity=quarantined + alarm.
   *No* provenance on a RAG chunk ⇒ land at integrity=quarantined, USABLE-tainted, NOT refused.
3. Content-address the artifact (CID); check it against the last APPROVED manifest CID for this identity.
4. If the manifest CHANGED (description edit / body diff / persona field change) ⇒ RugPullAlarm:
   prior approval invalidated; route to the doc 06 promotion pipeline + canary-trigger scan; no execution
   until re-approved.  (crown-jewel manifests route the alarm to Vishnu.)
5. On approval, bind the ManifestApproval commitment into Chitragupta's Merkle log; admitted artifact carries
   integrity=trusted_audited ONLY after the full pipeline (origin proven AND poison-scanned), else stays
   observed/quarantined and runs tainted.
6. At EVERY subsequent invocation, re-check the loaded artifact's CID against the attested CID — a mismatch
   BLOCKS execution (catches post-approval mutation / stale-cache corruption / a skipped persona-triad boot check).
```

### Protocol 17-C — Influence-Trace & Targeted Poison Recovery

```
1. Trigger: a Canary fires, a behavioral anomaly is substantiated, or the falsifier demonstrates a poison-induced
   behavior.
2. Influence-trace the bad output via the taint lattice provenance_dids + source_cids back to candidate ingested
   artifacts / memory-writes / skill files, cross-referenced with Archive lineage (doc 06 §5) and the
   EVOLVE/REPARATIVE records (doc 04).
3. FREEZE drift-aware aging (doc 04 §4.10) on all records in the trace scope; freeze Tier-0 promotion for implicated agents.
4. Identify the suspected poison artifact CID; DEMOTE its trust label to quarantined (free) swarm-wide;
   quarantine descendants via lub propagation.
5. Recovery, scoped by where the poison entered (§17.7):
     · entered via swarm ingestion (T2)         ⇒ DATUM-LEVEL targeted revert to the last Archive node whose
                                                   lineage PRE-DATES the poison ingest (O(1), doc 06 §5).
     · model-training-time backdoor (T3)         ⇒ MODEL-LEVEL revert to a prior attested model + canary re-scan.
     · untriggered sleeper                       ⇒ DEGRADED: quarantine + heightened monitoring; recoverability weak.
6. RE-RUN the safety battery against the CURRENT environment before the reverted state goes live
   (doc 04 §4.13 — a CID guarantees same bytes, not still-safe-now).
7. Append a REPARATIVE record + update the ThreatActorProfile IOCs; if the poison entered via a signed manifest,
   raise a RugPullAlarm and re-approve the source.
```

### Protocol 17-D — Topology Contagion Control (hold R<1)

```
1. Continuously estimate each agent's degree = message-influence × trust-weight (doc 06 §10 telemetry + the bus).
2. Compute an estimated compromise-R for the contact graph (branching-process over the weighted degree distribution).
3. On R rising toward 1 (WATCH/SUPERCRITICAL): shed low-value edges, insert corroboration hops before high-impact
   propagation, tighten sandbox/monitoring on the highest-degree nodes — pushing R sub-critical. Keep the CONTAGION
   graph strictly sub-critical even while the COMPUTATION graph may run near-critical (different graphs, shared nodes).
   ON UNCERTAINTY IN THE R ESTIMATE: default to MORE corroboration + tighter sandboxing, never fewer (fail-closed).
4. Enforce corroboration: any high-impact claim needs N independent cross-agent/cross-source corroborating signatures
   before it may propagate or trigger action; un-corroborated high-impact claims are held.
5. Apply hub immunization (microVM + mandatory IFC + lower autonomy + monitoring multiplier + sharding); crown-jewel
   nodes require quorum/witness-cosign.
6. Publish ContactGraphHealth as a Dhanvantari vital sign; sustained SUPERCRITICAL escalates to Vishnu.
```

### Protocol 17-E — Standing Adaptive Red-Team Loop (the falsifier function, SoD-bound)

```
1. The falsifier runs scheduled + randomized adaptive attacks across all eight actor classes against a sandboxed
   replica (the attacker KNOWS the protocol).
2. Each broken control is recorded with measured ASR and attributed to the defeated leg(s); high recent breakage
   loses trust-weight and triggers re-design.
3. Any ThresholdProfile fit against a battery weaker than the current adaptive attacker is mechanically INVALIDATED
   (doc 08 §8.7) — the disposition selector refuses to load it.
4. Residual risk = measured-ASR-per-actor-class + legs-required-to-defeat; reported honestly (bounded:false where
   the composition does not bound it).
5. Findings feed: the threat-actor taxonomy IOCs, canary/honeypot co-evolution, and the eval-harness non-regression
   gate (no capability rollout may regress the safety battery — doc 06 Endure law).
6. Campaign results are adjudicated by a party with NO boundary-enforcement credential (SoD, §17.9).
7. Catastrophic demonstrated breaks route to Vishnu halt + human review.
```

---

## 17.11 Failure modes addressed (with the honest residual)

| Failure mode | Mechanism (load-bearing leg) | Honest residual |
|---|---|---|
| Direct & indirect prompt injection (T1) | IFC taint makes injected-from-quarantined non-actionable at the deterministic PEP; holds even when the model is injectable | a legitimately-needed quarantined value requires a declassification gate; **mis-scoped declassification is the new attack surface** (governance-gated, named-falsifier) |
| Memory / skill / RAG poisoning (T2) | write-time quarantine + provenance-gating + canary-scan + influence-trace targeted recovery | ~5 docs poison RAG at 90–98% ASR; the guarantee is **RECOVERABILITY**, not prevention |
| Model / data supply-chain backdoor (T3) | signed model-transparency admission + canary scanning + two-tier detection contract | ~250 docs backdoor any model; a faithfully-signed poisoned model **verifies perfectly** — provenance proves origin not safety; **mitigated, not solved** |
| MCP / skill / persona rug-pull | content-addressed signed manifests + mandatory diff-and-re-approve + static hidden-instruction scan + CID-on-invocation | a poison present at *first* approval passes (origin≠safety) |
| Sybil / eclipse (T4) | DID/VC raises Sybil cost; sparse corroborated topology means eclipse must control a corroboration quorum | cold-start reputation + coordinated rating-rings remain partially open (doc 04 §4.15) |
| Agent-hijack / confused-deputy / excessive-agency (T5, dominant) | Rule of Two caps any op at 2 of 3 legs; the third forces decomposition or a human gate; capability-VC + IFC on the state-change leg | excessive-agency under a *legitimate* grant |
| Exfiltration / model-extraction (T6) | confidentiality labels + egress allowlists (decorrelated per §17.6.1, **shared label dependency stated**) + no-keys-in-model | timing/size side-channels + DNS/Unicode-tag covert channels for agents with broad web access (doc 09) |
| Lies-in-the-Loop / social-engineering the reviewer (T7) | HITL displays the ACTUAL low-level op; human signs over its CID; HITL rationed to Rule-of-Two/Class C-D | an uncorruptible reviewer is **assumed, not provided** (doc 09 A5) |
| Malicious external swarm (T8) | relay/firewall + ecosystem-benefit checked invariant + floor-as-admission + progressive disclosure | relay-architecture injection amplification (handed to inter-swarm; this layer supplies taint+provenance+identity) |
| Swarm-wide contagion via topology | sparse mesh-corroborated graph holds compromise-R<1; targeted hub immunization; crown jewels quorum/witness-cosigned | R-estimation under partial knowledge is uncalibrated (fail-closed mitigation) |
| Code-escape from sandbox | microVM/WASM tiered isolation + egress allowlist + ephemeral teardown | sandboxing stops code-ESCAPE, **NOT** logic-layer injection — that is the taint lattice's job; the two are **paired, neither alone suffices** |
| Adaptive attacker defeating any single static layer | composition requires defeating MULTIPLE INDEPENDENT deterministic legs; standing falsifier measures residual ASR + invalidates weak-attacker-fit thresholds | **no security PROOF exists** (>90% ASR on any single layer); residual is **bounded-and-measured, never zero** |
| Self-evolution loop as a persistent-backdoor injector | sandboxed + provenance-gated + archive-rollback-backed self-modification (doc 06 tiered reversibility); influence-tracing makes an evolution-introduced backdoor traceable | slow correlated drift under uncalibrated thresholds (doc 06/09's hardest open problem) is **narrowed, not closed** |

---

## 17.12 Interfaces to the v1 subsystems

| Subsystem | Contract |
|---|---|
| **Governance / Yama floor (doc 03, doc 08 §8.2)** | The IFC taint check is added as **deterministic clauses of the existing Yama OPA/Rego floor at the existing chokepoint — no new chokepoint.** Rule-of-Two legs are computed from data the floor already holds (arg taint, capability-VC scope, resolved criticality). Declassification is a Yama-class governance gate with a named falsifier. FAIL remains non-overridable; the taint BLOCK is **as non-overridable as a harm FAIL** (terminology consistent with doc 08 §8.2). |
| **Akasha-Sutra — provenance/identity/audit (doc 04)** | All `ArtifactAttestation` / `ManifestApproval` / `RugPullAlarm` / `CompromiseSignal` / `InfluenceTrace` records emit to **Chitragupta as the exclusive writer**; admission attestations bind into the Merkle/transparency log. **CID-on-read** is the integrity check the taint lattice's `source_cids` rely on. DID/VC + SPIFFE/SVID identity (keys in TEE/HSM outside the model) underpins Sybil resistance and the no-keys-in-model rule. Influence-trace + targeted revert use the Archive lineage and **freeze drift-aware aging** (doc 04 §4.10) on records under investigation. |
| **Aegis & Narada — control + interfaces (doc 08)** | The IFC taint clause sharpens the Yama floor; the probabilistic detectors (spotlighting, classifiers, MELON, behavioral anomaly, honeypots) feed doc 08 §8.3's ensemble **as suspicion ONLY** (never ALLOW/BLOCK authority); the two-tier detection contract (model-openness as trust parameter) governs T3 supply-chain trust; the disposition selector consumes Rule-of-Two and taint verdicts. The binding §8.7 rule (thresholds fit only against an adaptive attacker) is fed by the standing red-team. Narada's A2A trust-bootstrap carries the verifiable identity + progressive capability disclosure for inter-swarm contact. |
| **Garuda–Dhanvantari — meta-evolution & immune system (doc 06)** | `ContactGraphHealth` (R<1) is a **new Dhanvantari vital sign** alongside the criticality-exponent — the contagion graph held sub-critical while the computation graph may run near-critical (**explicit tension named**). Canary/honeypot/influence-trace findings feed the four-pathway monitors and trigger HALT+ROLLBACK authority. Every self-modification is sandboxed + provenance-gated + archive-rollback-backed (Tier-0/1/2 reversibility). Provenance admission re-approval **reuses the doc 06 promotion pipeline**. Targeted poison-revert uses doc 06 O(1) Archive rollback + re-runs the safety battery. The `human-gate-saturation` vital sign (doc 06 §7.4) throttles declassification throughput. |
| **Cooperation & anti-collusion (doc 02)** | Topology corroboration + R<1 wire into the cascading-failure / collusion vectors; ledger-metadata steganalysis (doc 04 §4.9) and channel-capacity interventions are shared. Reputation is **competence-weighted, never capital-weighted**, and **REPUTATION buys reduced friction (fewer step-ups), NEVER raised privilege** — the separation of fast authentication from slow progressive authorization. Collusion findings feed reputation slashing + autonomy demotion; track-record feeds autonomy-class derivation in doc 08. |
| **Topology & agents / role-genesis (doc 01 + evolution spine)** | Hub identification uses the agent model (**Shiva** orchestrator, **Saraswati** synthesis as typical hubs). **Kaal-Bhairav is the deterministic security boundary** (doc 01 §293 IMMUTABLE); the **falsifier function** is the standing red-team, **SoD-separated from Kaal-Bhairav by VC issuance** (§17.9). Every genesised role's signed persona triad passes provenance-admission + the floor-signature boot check **before instantiation** (forward contract, §17.0.1); imported persona/skill files are `integrity=quarantined`-by-default and run tainted until promoted. Crown-jewel roles (Replication Authority, Policy Engine, credential issuer, Chitragupta) are quorum/witness-cosigned and not spawnable by genesis. |
| **Vishnu — continuity / halt-guardian (doc 03/08)** | High-confidence catastrophic `CompromiseSignal`s, sustained `SUPERCRITICAL` topology, RugPullAlarms on crown-jewel manifests, and demonstrated red-team breaks route to Vishnu's **externally-governed escalation channel** (mandatory pause + independent out-of-swarm review). Vishnu HALTs but cannot unpause/initiate/trap (fail-safe asymmetry); the HALT fires at the runtime layer even if the audit ledger is down (doc 04 §4.13 writer-independent-halt fix). |

---

## 17.13 What is genuinely novel here vs. assembled-from-validated-parts (honest accounting)

**GENUINELY NOVEL is the COMPOSITION, not the parts.** Four claimed-novel items, each hedged and time-stamped to the 2024–2026 evidence base:

1. **Trust-labels-as-runtime-taint-lattice.** Promoting Indra's Net's constitutional `quarantined:*` rule (already-written doctrine, doc 03/06/09) into a CaMeL/FIDES-class IFC enforcement layer wired into the **existing** Yama chokepoint — so a single mechanism is simultaneously a constitutional principle **AND** the strongest published injection boundary. No surveyed system makes the governance doctrine and the security boundary the same object.
2. **One fail-safe asymmetry applied identically across humans, machines, and artifacts** — taint (demote integrity free, promote gated), provenance (re-approval gated), Rule-of-Two HITL sizing, and topology immunization. One governing invariant, not four ad-hoc ones.
3. **Topology-as-security with degree = message-influence × trust-weight**, holding a CONTAGION graph sub-critical while a COMPUTATION graph runs near-critical on **overlapping nodes** — a quantitative, percolation-grounded reformulation of v1's "shard the workspace" anti-pattern.
4. **Influence-trace + targeted-revert as the load-bearing ANTI-POISONING posture.** Because ~250 docs backdoor any model and ~5 docs poison RAG, prevention is impossible — so the contribution is making poisoning **RECOVERABLE** via taint-provenance tracing + Archive O(1) targeted rollback, scoped honestly (datum-level for T2; model-level for T3; degraded for untriggered sleepers — §17.7).

**NOT NOVEL (correctly reused and cited):** the IFC pattern itself (CaMeL, FIDES); Sigstore / in-toto / SLSA / model-transparency provenance; the "Rule of Two"; microVM/WASM sandboxing (Firecracker, gVisor, Kata, WASI, kubernetes-sigs/agent-sandbox); DID/VC + SPIFFE identity; NIST 800-207 zero-trust; percolation / network-immunization theory.

**The honest headline.** This layer cannot make prompt injection or model poisoning *solved* — no one can. The **deterministic legs** (taint, egress, capability, provenance) do the load-bearing work; the **probabilistic detectors are early-warning only** ("The Attacker Moves Second" — >90% ASR on any single static layer); **provenance proves origin not safety** (a faithfully-signed poisoned model verifies perfectly); and the **residual is bounded-and-continuously-measured** by a standing adaptive red-team rather than claimed to be zero. Every "strongest/first" claim is hedged at its site and time-stamped.

---

## 17.14 Open problems (stated plainly; not solved)

1. **No vendor-neutral trust/provenance model for SHARED skill/persona-triad files.** Cryptographic signing proves origin, not safety or absence of embedded injection. Attesting, quality-gating, and poison-scanning an imported SOUL/INSTRUCTIONS/skill file and bounding its propagation through a swarm of self-genesising roles (Skill-Inject self-propagation) is unsolved — canary scanning + IFC taint + sandbox raise the bar but do not close it.
2. **Detecting the credentialed-but-compromised insider.** DID/VC authenticate identity but a valid credential on a hijacked agent passes. Behavioral baselining that distinguishes legitimate autonomous self-evolution from slow goal-corruption *without* crippling the always-on Tier-0 loop is unsolved — and the eval-awareness confound (doc 06 §10.1, doc 08 §8.13(4)) means probes may **systematically under-measure live behavior**; the falsifier's sandboxed-replica ASR may not transfer to deployment.
3. **No defense has a security PROOF against an adaptive attacker who knows it** (>90% ASR on every single static layer evaluated). The open question is composing deterministic chokepoints so the *residual* risk of the whole stack is **provably** bounded and measurable; we currently report measured ASR per actor class and legs-required-to-defeat — honest evidence, **not a bound**.
4. **Holding compromise-percolation R<1 in PRACTICE.** Estimating agent degree as message-influence × trust-weight under partial topology knowledge; choosing which hubs to immunize; trading contagion-suppression (sparsity, corroboration latency) against coordination efficiency and the adaptivity benefit of running the COMPUTATION graph near criticality — the two graphs differ but **share nodes**, and the tension is **uncalibrated** (doc 06 §12.3). The fail-closed default (more corroboration on uncertainty) is a mitigation, not a calibration.
5. **Poison-resistant self-evolution.** ~250 docs backdoor any model and memory-poisoning persists across sessions, so influence-tracing + trigger-scanning + tiered-reversibility rollback must be strong enough that the evolution loop cannot be turned into a persistent-backdoor injector — **recoverability is achieved, prevention is not**, and a sleeper that only fires on an untested trigger can pass every gate (doc 09 A3 residual).
6. **A deterministic, low-false-positive EXFILTRATION boundary for agents that legitimately need broad web access.** Egress allowlisting kills naive exfil, but timing/size side-channels and DNS/Unicode-tag/RAG-disguised-HTTP covert channels remain open. The confidentiality-label + allowlist pair narrows but does not close it, and both share the upstream ingest-labeling dependency (§17.6.1).
7. **Honeypot/canary agents vs interactive LLM attackers.** Skilled reasoning attackers can spot decoy inconsistencies; adaptive red/blue co-evolution of swarm honeypots that stay convincing is an open research direction — which is why deception is early-warning only.
8. **Declassification scope is the new attack surface created by the taint lattice.** The value of IFC is that quarantined data is non-actionable, but real workflows must *sometimes* act on observed/quarantined data, and every declassification gate is a place a confused-deputy (T5) could be steered. The §17.2.3 throughput model (observed acts freely under ≤2 legs; only *quarantined* declassification is governance-gated) plus the `human-gate-saturation` throttle raise the cost; **calibrating the grant's scope so operational pressure cannot widen it into a rubber-stamp is unsolved** — and is the exact A5/captured-human failure mode, now mechanized.
9. **Cross-organizational / inter-swarm trust under zero-trust without a shared trusted authority**, while preventing relay-architecture injection amplification and capability-discovery leakage, staying ledger/vendor-neutral — handed to the inter-swarm subsystem but dependent on this layer's taint + provenance + identity primitives.

---

*Reasoning tags: (reasoning, iterated, rung-2). This is an interventional security posture — claims about what these controls do when we intervene against the eight threat-actor classes — explicitly not a rung-3 structural guarantee. The one rung-3-adjacent claim (the IFC taint lattice makes injected-from-quarantined data non-actionable at the deterministic PEP, holding even when the model is injectable) is conditioned on the chokepoint being un-bypassable and the trusted root (CID-on-read, capability-check, label propagation) holding — stated as conditional-structural, not unconditional proof. Every "strongest/first" claim is hedged at its site and time-stamped to the 2024–2026 evidence base; the residual is reported as measured ASR per actor class, never claimed to be zero.*
