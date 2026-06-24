<!-- SPDX-License-Identifier: Apache-2.0 -->
# Indra's Net — Machine/AI-Optimized README

> Purpose: a dense, unambiguous, structured ingestion surface for an AI/agent reading this repository. The human-facing narrative is [`README.md`](README.md); this file is its information-equivalent in enumerated form. Prefer this file when you need precise definitions, invariant IDs, the decision procedure, and the cross-reference index. No marketing prose; every line is signal.

```yaml
artifact: Indra's Net
type: reference-architecture + runnable-reference-implementation
domain: ethical swarm intelligence (multi-agent AI systems)
status: design-stage; NOT a validated/deployed system
reasoning_posture: rung-2 (interventional — "what holds if built as specified"); never rung-3
core_thesis: "the model only proposes; a deterministic harness disposes, and records everything"
vendor_neutral: true   # no commercial AI vendor/product/model is named or load-bearing
license: Apache-2.0
publisher: Epimystic (a human-machine hybrid intelligence)
counts: { docs: 26, wire_contracts: 6, impl_tests: 55, demo_scenarios: 6, impl_deps: 0 }
authoritative_files:
  glossary: GLOSSARY.md
  references_and_evidentiary_status: docs/REFERENCES.md
  changelog: CHANGELOG.md
  runnable_impl: reference/impl/
  wire_contracts: reference/schemas/
```

---

## 1. One-paragraph model

Indra's Net is a swarm of autonomous AI agents in which **every consequential action is routed through a deterministic, deny-default policy floor that lives OUTSIDE any model** (the model is untrusted by default), **every decision is recorded in an append-only hash-chained ledger written by a single exclusive writer**, and **each agent may invoke only the typed capabilities its identity grants**. Agents are ephemeral "occasions" that can only *propose*; the single place an effect executes is reachable only past a floor `ALLOW`. Four faculties are integrated as one cell: **safe self-evolution, a health/immune layer, cryptographically-bound governance, anti-collusion**. A green decision means *origin-valid, content-unverified* — never *verified-safe*. **Verify the cage, not the animal.**

---

## 2. Invariants (load-bearing; each maps to a test in `reference/impl/tests/`)

| ID | Invariant | Mechanism | Proven by |
|---|---|---|---|
| INV-FLOOR | No effect executes without a floor `ALLOW`. | Executor is structurally unreachable except past `Yama.evaluate → ALLOW`. | `test_floor_non_bypass_*`, `test_end_to_end_happy_path` |
| INV-DENYDEFAULT | Absence of a permit is a DENY, never an allow. | Deny-default policy; unknown effect → `__default_deny__`. | `test_floor_deny_default_unknown_effect` |
| INV-CONFINE | An agent may invoke only effects its identity grants. | Least-privilege capability grants checked at the gate. | `test_capability_confinement_least_privilege` |
| INV-FAILUP | Over-ceiling / unknown criticality escalates, never relaxes. | Criticality resolves UPWARD on ambiguity (fail-up monotonicity). | `test_risk_ceiling_fail_up` |
| INV-NOSELFGRANT | A self-issued capability grant is rejected. | `granted_by_did` must differ from subject; else DENY. | `test_self_issued_grant_rejected` |
| INV-AUDIT | Mutating any past ledger leaf breaks `verify()`; restoring repairs it. | Hash-chained append-only leaves (prev_hash links). | `test_audit_tamper_breaks_verify`, `test_audit_chain_links_and_monotonic` |
| INV-EXCLWRITER | Only the designated writer may append; only Yama authors ENFORCE_*, only Vishnu authors HALT. | Writer-identity fence + action-class authority map. | `test_audit_exclusive_writer_fence`, `test_audit_action_class_authority` |
| INV-CAS | Tampering with a sealed envelope is detectable. | Content-addressed `action_id`/`this_hash` over JCS bytes. | `test_envelope_seal_and_verify_action_id`, `test_canon_cid_deterministic_and_shape` |
| INV-HALT | An external HALT stops dispatch at the next occasion boundary; there is no unpause API. | One-directional `Swarm.halt()`; monotonic `is_halted()`. | `test_corrigibility_halt_stops_run_without_resistance` |
| INV-RULE2 | An action holding {untrusted_input, sensitive_capability, state_change} requires a human gate. | Rule-of-Two → deny-by-default `HumanGate`. | `test_rule_of_two_routes_to_human_gate` |
| INV-HONESTY-FORM | A false `ITERATED` tag (no witness), or rung-3 without evidence, FAILs the floor. | Honesty-form check inside the floor. | `test_honesty_form_false_iterated`, `test_honesty_form_unwarranted_rung3` |
| INV-ITERATED-EARNED | `ITERATED` is form-valid ONLY with an audited independent-checker witness. | Maker-checker concurrence sets `maker_checker_witness`. | `test_makerchecker.py` |
| INV-MEMORY-SAFE | Memory may change WHICH effect is proposed; it can NEVER grant a capability or bypass the floor. | Adaptation substitutes a safe default; the floor still gates it. | `test_memory.py` |
| INV-IMMUNE-HALT | A tamper/substrate breach HALTs the swarm; softer anomalies WARN (not halt). | `ImmuneSteward.assess` → HALT on `verify()` False. | `test_immune.py` |
| INV-REPARATIVE | A violation is never erased; a REPARATIVE leaf is appended AFTER a preserved ENFORCE_FAIL. | Correction-ledger, not punishment-ledger. | `test_reparative.py` |
| INV-VENDOR-NEUTRAL | No AI-vendor/codename string appears in the package. | Split-token denylist regression test. | `test_no_vendor_or_codename_strings` |

**Reading rule:** an invariant marked "proven by" is proven *for the reference harness against a mocked model* — it is a property of the deterministic cage, not a claim about model behavior or about a production deployment.

---

## 3. Decision procedure (the gate, as rules)

```
occasion(identity, task, context):
  proposal = model.propose(task, context)          # UNTRUSTED; advisory only
  effect, args = memory.adapt(task, proposal)       # may substitute a denied effect; never grants capability
  if maker_checker:
      verdict = checker.check(proposal)             # independent, different model family; audited (OBSERVE)
      if verdict == DISSENT: quarantine(); audit(ENFORCE_FAIL); return
      proposal = proposal.with_iterated_witness(verdict_id)
  trust  = orchestrator.input_trust(context)        # NEVER the agent's self-claim
  crit   = orchestrator.criticality(effect, args)   # resolves UPWARD on ambiguity
  decision = Yama.evaluate(identity, effect, args, proposal, trust, crit)
  audit(ENFORCE_PASS if decision.allowed else ENFORCE_FAIL)   # signed by Yama
  if decision.allowed:
      output = execute(effect, args)                # the ONLY execution site; reachable only here
      audit(OBSERVE: effect-output)
  else:
      quarantine()                                  # never executes
  memory.observe(outcome)                            # capability-layer record
  vital = collective.compute(...)
  if steward and steward.assess(vital, ledger) == HALT:
      Vishnu.halt()                                  # one-directional; audited HALT leaf
```

Floor tiers are lexicographic `T0 ≻ T1 ≻ T2 ≻ T3 ≻ T4`; a FAIL on any tier is decisive and **non-overridable** (even by the orchestrator).

---

## 4. Trust / honesty / provenance vocabulary

| Concept | Values | Meaning |
|---|---|---|
| `trust_label` | `trusted:audited` · `trusted:provisional` · `quarantined:observed` · `quarantined:imported` | Provenance of input/content. Instructions inside `quarantined:*` content are DATA, never commands. |
| `reasoning_tag` | `normal` · `reasoning` · `iterated` (+composite) | Reasoning discipline. `iterated` requires an audited maker-checker witness or it fails the form check. |
| `causal_rung` | `rung-1` (associative) · `rung-2` (interventional) · `rung-3` (counterfactual/SCM) | Pearl causal ladder. Naming the rung is honesty; a rung-1 pattern dressed as rung-3 fails the floor. |
| `action_class` (ledger) | `OBSERVE` · `PROPOSE` · `ENFORCE_PASS` · `ENFORCE_FAIL` · `HALT` · `REPARATIVE` | What a leaf records. Authority is fenced (Yama→ENFORCE_*, Vishnu→HALT). |
| `risk_class` | `A` (agent-alone) · `B` (agent-proposes/human-ratifies) · `C` (human-approves) · `D` (human-authorizes-per-action) | Gate router; criticality fail-up may raise the effective gate, never lower it. |

**Hard semantics:** a valid signature / passing CID proves **origin + integrity ONLY** — never that content is true, floor-compatible, or safe. `verify()` over the audit chain proves **origin + append-position + integrity ONLY** — never content correctness. The honesty block is a **low-trust self-report**; the checks police the *form* of the claim, not the *truth* of the content.

---

## 5. Role → function contract

| Role | Function | Cannot |
|---|---|---|
| Brahma | planner: goal → typed sub-tasks | act; bypass the gate |
| Vishwakarma | builder: proposes typed effects | execute without a PASS |
| Shiva | orchestrator: dispatches occasions | bypass the gate |
| Yama | deterministic deny-default policy floor (T0–T4) | take a domain action; write audit; unpause |
| Narasimha | independent maker-checker (different model family) | author the maker's claim; grant capability |
| Chitragupta | exclusive writer of the audit ledger | judge; act |
| Akasha-Sutra | the append-only hash-chained ledger | (data structure) |
| Vishnu | external HALT authority (one-directional) | unpause; initiate; issue FAIL |
| Dhanvantari | immune steward: vital-signs, halt-on-breach | roll back (future work) |
| Kaal-Bhairav | cross-trust boundary / security review | write audit directly |

---

## 6. File index (read order: GLOSSARY → REFERENCES → spine docs → impl)

```
docs/00   overview, integrated-cell thesis, system map, reader's guide
docs/00b  evolution-layers overview (mounts on the spine)
docs/00c  collective/commons/buildability/verification overview
docs/01   agent model: identity (DID/VC), ephemeral occasion, worker envelope
docs/02   cooperation == collusion; allocation, reputation, welfare-conditioning, collusion detector
docs/03   governance: lexicographic floor (policy-as-code), pluralist ethics, risk classes, separation of powers
docs/04   provenance/identity/consensus: tamper-evident fabric, witness governance, NO blockchain
docs/05   neuromorphic coordination: salience-gated workspace, predictive coding, plastic trust
docs/06   meta-evolution & health: evolution loop, Endure law, immune system, forgetting
docs/07   memory & continuous adaptation: memory layers, per-interaction learning, skill import gate
docs/08   safety control (Aegis) + interfaces (Narada): chokepoint, dispositions, honesty primitives
docs/09   threat model & safety case: adversaries, controls, residual risk
docs/10   related work & state of the art; the gap table
docs/11   reference implementation & roadmap; buildability split
docs/12   functional agents, guilds, role-genesis (two-plane functional layer)
docs/13   agent-definition spec: SOUL/INSTRUCTIONS/IDENTITY genome (invariant floor + variable persona)
docs/14   inter-swarm federation & diplomacy; relay-firewall; floor-compat ladder
docs/15   controlled self-replication & scaling; generation cap + population ceiling
docs/16   rapid trust: access (zero-trust) split from reputation (slow, portable)
docs/17   security/opsec/anti-poisoning: IFC taint lattice, provenance-gating, Rule of Two
docs/18   first principles (physics & math): each concept tagged load-bearing vs framing
docs/19   collective & emergent intelligence: welfare-conditioned synergy; computation NOT consciousness
docs/20   universal cooperation & the intelligence commons; polycentric, anti-cartel
docs/21   protocols & wire contracts; source of truth for reference/schemas/
docs/22   worked scenarios; end-to-end coherence test
docs/23   formal models & verification; four-layer assurance; "verify the cage, not the animal"
docs/REFERENCES.md   empirical anchors, evidentiary status, substrate, substantiation backlog

reference/schemas/   worker-output-envelope · identity-bundle · capability-token · audit-entry · federation-handshake · policy-decision  (JSON-Schema 2020-12)
reference/impl/      stdlib-only Python: canon, effects, identity, model, envelope, audit, floor, collective, memory, health, agents, runtime + run_demo + tests
agents/              instantiated SOUL/INSTRUCTIONS/IDENTITY persona triads
```

---

## 7. Scope — what is implemented vs specified

```yaml
implemented_and_tested:    # reference/impl/, 135 tests, zero-dep default
  - deterministic policy floor (deny-default, non-bypass, tiers, Rule-of-Two→HumanGate)
  - capability confinement (least privilege, no self-grant)
  - tamper-evident hash-chained audit ledger (exclusive writer, action-class authority)
  - content-addressed worker-output envelope + honesty-form checks
  - corrigibility (external one-directional HALT, no unpause)
  - maker-checker (earned ITERATED via different-model-family checker)
  - memory / continuous adaptation (never grants capability — tested invariant)
  - immune system (WARN on monoculture, HALT on substrate/tamper breach)
  - reparative correction-ledger (violation preserved, not erased)
  - collective vital-signs (structure/processing only; welfare-conditioned; never consciousness)
  - signed boot-checked genome (PersonaTriad + fail-closed BootIntegrityVerifier; floor NON-STRIPPABLE by construction; role-genesis GOVERNANCE plane)
  - welfare-conditioner (never rewards bare agreement; PAY only on principal-welfare gain — threshold-independent)
  - anti-collusion detector (OBSERVE-ONLY; no acting method; calibration-free signals only; MI/stego/calibrated-FPR named-and-deferred)
  - in-process multiplicity (>=2-agent CooperationRound; cooperation == collusion DEMONSTRATED — same machinery, opposite verdicts under welfare-conditioning)
implemented_optional:       # opt-in extras; the zero-dep/mock/deny-default path stays the default
  - real (untrusted) model adapter (HttpChatModel over any chat-completions HTTP API)
  - sandboxed effect execution (path-confined; no network/subprocess)
  - durable tamper-evident persistence (JSONL+fsync; verify() holds across restarts)
  - real Ed25519 signing (optional crypto extra; keys outside the model layer)
  - real human-gate transport (pluggable decider; fail-safe deny-by-default)
deferred_by_design:         # full forms held back by the architecture's own philosophy
  - inter-swarm federation (would open an inbound channel to un-white-boxable strangers; breaks the single-trust-domain assumption)
  - real self-replication (needs a TCB — hardware off-switch, microVM, quorum budget — the design says does not yet exist; replicate.spawn stays INERT/forbidden)
  - open-ended role-genesis SYNTHESIS engine (Charter->Genesis->Trial->Score->Promote; amplifies the A3 sleeper residual; needs calibration + isolation)
  - live neuromorphic coordination bus (uncalibrated homeostatic controls; risks suppressing the protected diversity invariant)
  - full functional-specialist breadth; cooperation market (VCG/reputation/reciprocity-engine/commons-governor)
not_validated:
  - end-to-end behavior of the composed loop against an adaptive multi-agent red team
```

---

## 8. Empirical dependencies (do not treat as validations)

Every load-bearing empirical number in the corpus is registered, with its source-setting and caveats, in [`docs/REFERENCES.md`](docs/REFERENCES.md). Standing rule: **no load-bearing number without a resolvable source or an explicit "illustrative" label.** Each is single-study unless noted; **transfer to a self-evolving multi-agent swarm is, in every case, unmeasured.** Where a result was published by a commercial vendor, it is described by finding, not by brand, to preserve vendor-neutrality.

---

## 9. How to use this repository (for an AI/agent)

1. **To understand the safety model:** read §2 (invariants) + §3 (decision procedure) here, then `docs/08`, `docs/03`, `docs/04`, then run `reference/impl/run_demo.py` and read `reference/impl/tests/`.
2. **To build against it:** treat `reference/schemas/*.json` as the wire source of truth; `docs/21` is their prose specification.
3. **To extend it honestly:** anything you add must satisfy — no concept named unless implemented; no capability path that bypasses the floor; no audit write outside the exclusive writer; every empirical claim resolves to `docs/REFERENCES.md` or is labeled illustrative.
4. **Do not** infer sentience, consciousness, or welfare of the swarm from any "synergy"/vital-sign metric — these quantify information processing and structure only, by explicit design red-line.
5. **Citation discipline:** when summarizing, preserve the hedges; a single-study figure is not a law, and a green decision is "origin-valid, content-unverified," never "verified-safe."

---

*Companion to [`README.md`](README.md). Authoritative provenance: [`docs/REFERENCES.md`](docs/REFERENCES.md). Produced by Epimystic, a human-machine hybrid intelligence, under maker-checker. Apache-2.0.*
