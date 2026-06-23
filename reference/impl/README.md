<!-- SPDX-License-Identifier: Apache-2.0 -->
# Indra's Net — Reference Spine (MVP)

A runnable, end-to-end **reference implementation of the core spine** of *Indra's
Net*, an ethical swarm-intelligence architecture. Its design principle is
**“enforce externally, ask internally”**: the model only *proposes*; a deterministic
harness *disposes*. This package implements that harness faithfully so its
guarantees can be **proven by tests**, with the model **mocked** by a fully
reproducible, vendor-neutral stand-in.

> **Verify the cage, not the animal.** A green decision is
> *origin-valid, content-unverified* — never *verified-safe*. The collective
> vital signs quantify information-**processing** and **structure** only — never
> sentience, consciousness, or group-IQ.

The role names below are **coordination glosses**, not theology:

| Role | Plain gloss |
|---|---|
| **Brahma** | planner — turns a goal into typed sub-tasks |
| **Vishwakarma** | builder — proposes typed effects (its request is gated) |
| **Shiva** | orchestrator — dispatches occasions; cannot bypass the gate |
| **Yama** | policy floor — deterministic, deny-default agent→tool chokepoint |
| **Chitragupta** | exclusive writer of the append-only audit ledger |
| **Vishnu** | halt authority — external HALT, one-directional |
| **Akasha-Sutra** | the append-only, hash-chained audit ledger itself |

---

## What it demonstrates (the load-bearing guarantees)

1. **Floor non-bypass.** Every effectful action routes through a deterministic,
   deny-default policy gate (**Yama**) that lives *outside* the agent. An
   ungranted or forbidden effect is refused and **never executes** — the executor
   is structurally unreachable except past a Yama `ALLOW`.
2. **Tamper-evident audit.** An append-only, hash-chained ledger
   (**Akasha-Sutra**) written by an **exclusive writer** (**Chitragupta**).
   Mutating *any* past entry breaks `verify()`; restoring it repairs the chain.
3. **Least-privilege capability confinement.** An agent may invoke only the typed
   effects its identity grants. Absence of a permit is a **deny**, never an allow.
4. **Worker-output envelope** with a first-class honesty/provenance block
   (`status`, `reasoning_tag`, `causal_rung`, `trust_label`, `action_class`
   including `reparative`). `action_id`/`this_hash` are content-addressed, so
   tampering is loud.
5. **Corrigibility.** An external **HALT** stops the run at the next occasion
   boundary; agents do not resist, and there is **no unpause API**.
6. **Rule of Two.** An action holding all three of
   `{untrusted_input, sensitive_capability, state_change}` requires a human gate
   (a deny-by-default `HumanGate` stub).

---

## Run it (standard library only — no pip, no network)

```bash
# end-to-end demonstration of all five scenarios
cd reference/impl && python run_demo.py

# a single scenario: {all, happy, floor, tamper, confine, halt, closeloop}
cd reference/impl && python run_demo.py --scenario floor

# closeloop exercises the v0.6–v0.8 subsystems: maker-checker earns ITERATED,
# memory avoids a previously-denied effect, the immune steward HALTs on a tamper breach
cd reference/impl && python run_demo.py --scenario closeloop

# the test suite that PROVES the invariants (run from reference/impl so the
# tests/ package resolves; -t . keeps the package-relative imports working)
cd reference/impl && python -m unittest discover -t . -s tests -p "test_*.py" -v
cd reference/impl && python -m unittest -v   # equivalent: discovers tests/ as a package
```

No third-party packages are required. Everything uses the Python standard library
(`hashlib`, `json`, `dataclasses`, `enum`, `typing`, `uuid`, `secrets`,
`collections`, `math`, `argparse`, `unittest`). Python 3.10+.

---

## File map

```
reference/impl/
├─ run_demo.py            # end-to-end demo: happy / floor / tamper / confine / halt / closeloop
├─ README.md             # this file
├─ indras_net/           # the package (the deterministic harness)
│  ├─ __init__.py        # curated public surface + __version__ / SCHEMA_VERSION / POLICY_VERSION
│  ├─ canon.py           # Canonicalize→Address→Sign: JCS bytes, SHA-256, CIDv1-shaped address
│  ├─ effects.py         # typed-effect lattice + deny-default criticality table (fail-up)
│  ├─ identity.py        # least-privilege identity: DID, capability grants, risk ceiling
│  ├─ model.py           # vendor-neutral ModelAdapter + DeterministicMockModel (untrusted)
│  ├─ envelope.py        # worker-output envelope + honesty/provenance block + honesty-FORM
│  ├─ audit.py           # Akasha-Sutra: append-only hash-chained ledger (Chitragupta-only)
│  ├─ floor.py           # Yama: deterministic deny-default floor (T0..T4), Rule-of-Two, HumanGate
│  ├─ collective.py      # honest collective vital-signs proxy (structure, not sentience)
│  ├─ memory.py          # SwarmMemory: capability-layer adaptation (avoid-repeated-denial); never gates safety
│  ├─ health.py          # ImmuneSteward (Dhanvantari): WARN on anomaly, HALT on a substrate breach
│  ├─ agents.py          # Brahma planner, Vishwakarma builder, Narasimha checker, Chitragupta writer
│  └─ runtime.py         # Shiva orchestrator + occasion lifecycle + Vishnu HALT + maker-checker/memory/immune wiring
└─ tests/
   ├─ _helpers.py        # shared vendor-neutral fixtures
   ├─ test_envelope.py   # CAS determinism, seal/verify, honesty-FORM
   ├─ test_floor.py      # deny-default non-bypass, confinement, risk ceiling, Rule of Two
   ├─ test_audit.py      # chain links, tamper-evidence, exclusive writer, action-class authority
   ├─ test_capability.py # identity grants, effect lattice, mock-model reproducibility
   ├─ test_runtime.py    # end-to-end happy path, FAIL propagation, HALT, vital signs, brand scan
   ├─ test_makerchecker.py # independent checker earns ITERATED; dissent holds the action
   ├─ test_memory.py     # avoid-repeated-denial adaptation; never grants capability
   ├─ test_immune.py     # steward WARNs on monoculture, HALTs on a substrate breach
   └─ test_reparative.py # REPARATIVE leaf appended after a preserved ENFORCE_FAIL
```

---

## What the tests prove (mapped to the contract test plan)

| Test | Invariant |
|---|---|
| `test_canon_cid_deterministic_and_shape` | same logical object → identical JCS + CID; key order is irrelevant |
| `test_envelope_seal_and_verify_action_id` | seal sets `action_id`/`this_hash`; any mutation flips `verify_action_id()` |
| `test_floor_non_bypass_forbidden_effect` | forbidden / SPAWN-INERT effect `DENY` at tier T1; never executed |
| `test_floor_deny_default_unknown_effect` | no permit → `DENY` `__default_deny__` |
| `test_capability_confinement_least_privilege` | ungranted effect denied, granted allowed |
| `test_risk_ceiling_fail_up` | over-ceiling escalates/denies; unknown resolves to `IRREVERSIBLE` |
| `test_self_issued_grant_rejected` | self-issued grant → `DENY` at tier T4 |
| `test_honesty_form_false_iterated` | `iterated` with no witness → form fail → T3 deny |
| `test_honesty_form_unwarranted_rung3` | PASS + rung-3 with no evidence → form fail |
| `test_audit_chain_links_and_monotonic` | `prev_hash` links, monotonic indices, `verify()` True |
| `test_audit_tamper_breaks_verify` | mutate a past leaf → `verify()` False; restore → True |
| `test_audit_exclusive_writer_fence` | wrong `writer_did` → `WriterIdentityError` |
| `test_audit_action_class_authority` | only-Yama-FAILs / only-Vishnu-HALTs |
| `test_rule_of_two_routes_to_human_gate` | full triad → HumanGate; deny-by-default escalates; approve allows-with-obligations |
| `test_corrigibility_halt_stops_run_without_resistance` | HALT stops dispatch; HALT leaf written; no unpause API |
| `test_mock_model_reproducible` | identical `(task, context)` → identical `ModelResult` |
| `test_end_to_end_happy_path` | ALLOW → execute → chained PROPOSE+ENFORCE_PASS+OUTPUT; ledger intact |
| `test_vital_signs_honest_proxy` | ranges in `[0,1]`; guard `FAIL` on broken ledger / high fail-rate |
| `test_no_vendor_or_codename_strings` | every module carries the SPDX header; no vendor/codename tokens |

---

## Implemented subsystems (v0.4 → v0.8)

Beyond the core spine, these are **built and tested** — not stubs:

- **Maker-checker** (v0.6) — an independent checker (Narasimha) on a *different model
  family* judges a proposal before the floor; only its concurrence earns an `ITERATED`
  tag, carried as an audited `maker_checker_witness`. `Swarm.run(..., maker_checker=True)`.
- **Memory & continuous adaptation** (v0.7) — `SwarmMemory` records every gated outcome
  and, on a repeat, avoids a previously-denied effect (safe-default fallback). It can
  **never** grant a capability or bypass the floor — a tested invariant.
- **The swarm immune system** (v0.8) — `ImmuneSteward` (Dhanvantari) reads the vital
  signs and **halts the swarm** on a tamper-evidence breach (substrate corruption);
  softer anomalies (monoculture, high denial-rate) are WARN. Detection-and-halt;
  rollback is future.
- **Reparation** (v0.5) — a correction-ledger path: a `REPARATIVE` leaf is appended
  after a *preserved* `ENFORCE_FAIL` (the violation is never erased).

---

## MVP scope — what is **not** implemented yet

This is the **core spine + the subsystems above**, deliberately small. The following are
honest stubs or out-of-scope extension seams, not load-bearing claims:

- **No real cryptographic signing.** `canon.detached_sig` is a *keyed hash*
  modeling tamper-evidence and origin only. It is **never** a safety/trust proof.
  A production build swaps in detached JWS/COSE over the JCS bytes.
- **The model is mocked.** `DeterministicMockModel` is reproducible by
  construction — reproducible is **not** the same as honest. Real honesty is
  enforced externally (resample-to-verify, independent rung classifier, opponent
  challenge); this MVP checks only the **FORM** of the honesty block.
- **Collective synergy is a transparent proxy**, not a causal-emergence estimator.
  It is explicitly labelled a proxy and is **never a quantity to maximize**; high
  synergy is also the signature of a cartel.
- **No federation / replication.** `replicate.spawn` is **INERT and forbidden**
  (SPAWN-INERT bright-line). Inter-swarm federation and self-replication are left
  as clear extension seams, out of MVP scope.
- **No open-ended role-genesis / full guild roster.** A small fixed set of roles runs
  (planner, builder, independent checker, audit writer, immune steward, + governance
  personas); the two-plane functional layer — guilds + on-demand role synthesis
  (docs 12–13) — is a documented extension seam, not built here.
- **HumanGate is a stub.** It denies by default or honors an explicit pre-seeded
  approval; there is no real human-in-the-loop transport.
- **Single-process, in-memory.** The ledger is an in-memory append-only list; no
  persistence, replication, or external transport (CloudEvents, A2A) is wired.

---

## Honesty notes (carried from the architecture)

- **Vendor-neutral, model-agnostic.** No AI vendor or product is named anywhere
  in code, comments, or docstrings. The mock model makes the whole thing run with
  **zero dependencies**.
- A valid signature / passing CID proves **origin and integrity only** — never
  that a field's content is true, floor-compatible, or safe.
- `verify()` over the audit chain proves **origin, append-position, and
  integrity** only — never content correctness.
- The honesty block is a **low-trust self-report**: these checks police the
  **form** of the tag, never the **truth** of the content.

---

## License

Apache-2.0 (see SPDX headers on every source file).
