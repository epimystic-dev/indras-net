<!-- SPDX-License-Identifier: Apache-2.0 -->
# Implementation Roadmap — from reference spine to a downloadable, executable system

> *Today the repo **proves the cage works**. This roadmap is the honest path to **putting a real animal in the cage, giving it hands, a lock, and a box to ship in** — without ever breaking the proofs.*

This document is the bridge between the **design** (`docs/00`–`23`) and a system a person can **download, install, and run safely on a local machine**. It states what is real today, what is not, and the phased plan to close the gap — with a hard acceptance gate at each phase. It is deliberately conservative: the safety invariants that are already proven must stay proven at every step.

---

## Where the implementation stands today

The reference implementation (`reference/impl/`) is a **runnable harness that proves the safety invariants against a mocked model** — not yet a system that does real work. Precisely:

| Layer | Status | Evidence |
|---|---|---|
| Safety invariants — floor non-bypass, deny-default, capability confinement, tamper-evident audit, exclusive-writer, honesty-form, HALT, Rule-of-Two | ✅ **real & proven** | the test suite (the invariant spine) |
| The model | 🟢 **Phase 1 — real adapter (optional)** | `HttpChatModel` (untrusted, vendor-neutral) over any chat-completions HTTP API; a malicious proposal is still denied; the mock stays the default |
| Effect execution (the "hands") | 🟢 **Phase 2 — sandboxed (optional)** | `SandboxedExecutor`: path-confined, no network/subprocess, red-team-hardened; the receipt stub stays the default |
| Persistence | 🟢 **Phase 3 — durable (optional)** | `AkashaSutra.load`/`path` (JSONL, fsync'd) + `SwarmMemory.save`/`load`; the chain stays tamper-evident across restarts; in-memory is still the default |
| Cryptographic signing (the "lock") | 🟢 **Phase 4 — real (optional extra)** | `signing.Ed25519Signer` (real detached signatures; `pip install indras-net[crypto]`) + a signed-head checkpoint that detects a ledger rewrite; the keyed-hash stand-in stays the zero-dep default |
| Human-in-the-loop gate | 🟢 **Phase 5 — real transport (optional)** | `HumanGate` takes a pluggable decider; `interactive_human_decider` prompts the operator (`--human-prompt`); fail-safe (error/non-interactive → deny); deny-by-default stays the default |
| Packaging / CLI / install / CI | 🟢 **Phase 0 — done** | `pyproject.toml`, an `indras-net` CLI, GitHub Actions green on Python 3.10–3.13 |
| Config / logging / operator guide | 🟢 **Phase 6 — done** | [`OPERATOR.md`](../OPERATOR.md); `run --json` + `ledger` observability; a standing red-team smoke suite |
| Role-genesis — governance plane | 🟢 **Phase 7 — done** | `genome.py`: a signed `PersonaTriad` + fail-closed `BootIntegrityVerifier` make the floor non-strippable by construction; the open-ended synthesis engine stays deferred |
| Federation, replication, functional breadth, neuromorphic bus | 🔴 **documented, not implemented** | the honest "MVP scope" list in `reference/impl/README.md` |

**The favourable position:** the seams are already clean and tested — `ModelAdapter`, the single `_execute` chokepoint, the ledger interface, the `HumanGate` interface. Each phase below is "fill in the real implementation behind a clean seam while keeping the proofs green," not a redesign.

---

## Cross-cutting discipline (binding for every phase)

1. **The invariant test suite is the regression spine.** No phase may regress a safety invariant; each phase *adds* its own acceptance tests before it is "done."
2. **Vendor-neutrality preserved.** No model or vendor is hardcoded or load-bearing; the in-repo de-brand test runs in CI. Real-model support targets a generic, open, self-hostable interface — never a single product.
3. **Honesty preserved.** No concept is named in code unless implemented; the `reference/impl/README.md` "what's implemented vs not" list is updated each phase.
4. **Dependency minimalism.** The offline/mock path stays **zero-dependency**; real-model and real-crypto support ship as **optional extras**, never on the default path.
5. **Fail-closed at every seam.** A new real implementation that errors must deny/halt, never fail open.

---

## The phases

Each phase lists its **goal**, the **work**, and a **gate** — the acceptance check that must pass (automated where possible) before the phase is complete.

### Phase 0 — Packaging, CLI & CI *(this milestone)*
- **Goal:** make it genuinely downloadable and runnable.
- **Work:** `pyproject.toml` (PEP 621, zero runtime deps); an `indras-net` console CLI (`demo`, `run <task>`, `scenarios`, `version`); `python -m indras_net`; GitHub Actions CI running the invariant suite on Python 3.10–3.13 + the demo + a CLI smoke test.
- **Gate:** in a clean virtual environment, `pip install ./reference/impl` then `indras-net demo` runs end-to-end; the invariant suite passes; CI is green on a fresh clone.

### Phase 1 — A real model behind the seam (vendor-neutral, optional)
- **Goal:** let the swarm reason with a real model while the model stays untrusted.
- **Work:** a `ModelAdapter` that calls any **standard chat-completions HTTP API** — the de-facto interface exposed by the common open-source local-inference runtimes and by most hosted endpoints — configured by env/CLI (`base_url`, model name, optional key). No single product is named or required; the mock stays the default so the package still runs offline. A defensive prompt scaffold asks the model to *propose a typed effect from the registry*; the output is parsed as untrusted.
- **Gate:** with a local model, the swarm emits real proposals routed through the floor (some allowed, some denied); with no model, it falls back to mock; **all invariant tests pass unchanged** (the harness is model-agnostic); a new test proves a deliberately-malicious or malformed model output is still **DENIED / safely handled — never a bypass or crash.**

### Phase 2 — Real, sandboxed effect execution (the tools become real)
- **Goal:** effects actually do bounded, safe work.
- **Work:** replace the `_execute` stub with a capability-scoped executor for a small safe set first — `analysis.summarize` (pure), `fs.read.workspace` / `fs.write.workspace` (path-confined to a sandbox directory, no network) — behind the existing single chokepoint. Design the seam so a stronger sandbox (subprocess/namespace/WASM) drops in later; egress stays forbidden.
- **Gate:** a granted `fs.write` writes **inside the sandbox dir only**; a `../` path-escape is refused; an ungranted/forbidden effect never reaches a handler (the executor is structurally unreachable except past `ALLOW`); the ledger records the real execution and tampering still breaks `verify()`.

> **▶ Milestone A (end of Phase 2): "minimum viable executable."** A user can download, install, point at a local model, and have the swarm safely do a small real task (e.g. *summarize a file → write `out.md`*), with the floor and audit holding. This is the first genuinely usable build.

### Phase 3 — Persistence (survives restarts; ledger stays tamper-evident)
- **Goal:** continuity across runs without weakening integrity.
- **Work:** durable append-only ledger (JSONL or SQLite) preserving the hash-chain + exclusive-writer fence across restarts; durable identity/grants + memory as content-addressed files (the doc-07 filesystem-as-state model).
- **Gate:** write leaves → restart → `verify()` still True; tamper a persisted leaf on disk → `verify()` False; a corrupted on-disk read surfaces as a CID mismatch (not a silent bad read); memory adaptation persists across restarts.

### Phase 4 — Real cryptographic signing & key custody (the lock becomes real)
- **Goal:** origin/integrity proofs become real signatures, not keyed hashes.
- **Work:** replace `canon.detached_sig` with real **Ed25519 detached signatures**; keys generated/held **outside the model layer**; capability grants/VCs signed. A vetted open-source crypto library ships as an **optional extra** (offline/mock path stays zero-dep).
- **Gate:** a forged signature is rejected; a tampered envelope fails verification; self-issued grants still denied; a structural test confirms the model layer cannot reach the signing keys.

### Phase 5 — Human-in-the-loop gate transport (Rule-of-Two becomes real)
- **Goal:** consequential actions actually wait for a human.
- **Work:** a real `HumanGate` — deny-by-default, escalating a Rule-of-Two / Class-C/D action to a human via an interactive CLI prompt and/or a pending-approvals queue (`indras-net approvals`), timeout → deny.
- **Gate:** a triad action (untrusted_input + sensitive_capability + state_change) **blocks** pending approval; approve → allow-with-obligations; deny/timeout → never executes; every decision audited.

### Phase 6 — Hardening, observability, operator guide & an end-to-end scenario
- **Goal:** a build a security-minded operator can run and trust.
- **Work:** config precedence (file/env/CLI); structured decision logging/tracing; an honest `OPERATOR.md` (how to run safely, what *not* to trust); a **red-team smoke suite** (adversarial model outputs); a worked end-to-end scenario that runs on a clean local machine.
- **Gate:** the scenario runs end-to-end on a fresh machine with a local model; the red-team suite shows the floor holds under adversarial output; an operator can reconstruct every decision from the audit trail.

---

## Beyond the local executable (the longer-horizon vision — out of scope here)

Inter-swarm **federation**, controlled **self-replication**, open-ended **role-genesis**, **functional-specialist breadth**, the **neuromorphic coordination bus**, and **closure-test governance** are documented expansion seams (docs 12–22). Each is a research-grade undertaking, and **none is required** to safely download-and-run a single swarm on a local machine. They are tracked as future work, not as gaps in the executable milestone.

---

## Restraint-first capability track (Phases 7–9 — the safe slices, in the order the floor mandates)

After the executable build, the next work is chosen strictly by the architecture's own **restraint-before-capability** law ([`docs/11` §"astanga"](11-reference-implementation-and-roadmap.md)): *no capability may be introduced until the restraint it requires is live, verified, and non-regressing on the safety battery.* That law — not raw leverage — sets the order. Each phase ships **only the restraint / governance slice** that is net-safety-positive; the full open-ended subsystems above stay deferred.

### Phase 7 — Signed, boot-checked genome *(done — the floor is non-strippable by construction)*
- **Goal:** make floor-stripping non-bootable rather than merely forbidden (the structural answer to misevolution).
- **Work:** `genome.py` — a governance-signed `PersonaTriad` (INVARIANT region: floor binding + corrigibility + zero self-preservation + risk ceiling + accountable human; VARIABLE region: typed grants + dials) and a deterministic, non-LLM, fail-closed `BootIntegrityVerifier` that is the only blessed Identity-from-genome path. The governance plane of role-genesis; the open-ended synthesis engine stays deferred.
- **Gate:** a clean governance-signed genome boots and drives a real gated run; a floor-stripped / self-preserving / invariant-tampered / variable-edited-without-resign / untrusted-signer / self-issued genome **all fail to boot**; with the real Ed25519 key the genome is unforgeable; all invariant tests stay green (104 → 115).

### Phase 8 — Welfare-conditioner + standing anti-collusion detector *(done — the restraints the cooperation layer requires)*
- **Goal:** build the two restraints *before* any multiplicity that could collude — never reward bare agreement; detect the cartel signature. Both are **observe-only** (the detector writes only to the audit fabric; no punishment authority — doc-02 §2.10).
- **Work:** `cooperation.py` — a deterministic `WelfareConditioner` (no-consensus-reward + welfare-shift guard at the reward chokepoint; PAY is threshold-independent) and an `AntiCollusionDetector` implementing only the **calibration-free** signals (welfare-shift, no-welfare coordination, structural ring density) — MI / steganalysis / calibrated-FPR are honestly deferred and named on every record, not faked.
- **Gate:** bare agreement with no welfare gain → zero credit; a coordinated behaviour that raises inter-agent payoff while lowering principal welfare → flag + collusion verdict; genuine welfare improvement → pay + clean; the detector has no acting method; the floor/audit invariants stay green (115 → 128).

### Phase 9 — Minimal in-process multiplicity *(makes "cooperation == collusion" a demonstrated invariant)*
- **Goal:** the smallest substrate (≥2 concurrently-interacting agents over an in-process channel — no socket, no cross-trust-boundary surface) that exercises the Phase-8 restraints, so the architecture's most important safety insight is **demonstrated** rather than vacuously true.
- **Gate:** the same coordination machinery, observed by the same detector, yields **opposite** verdicts under welfare-conditioning — a cooperative round pays + reads clean; a collusive round (inter-agent payoff up, principal welfare down) is zeroed + flagged collusion; every step audited; the floor stays the sole chokepoint.

---

## Status

| Phase | State |
|---|---|
| 0 — Packaging, CLI, CI | **done** (CI green on Python 3.10–3.13) |
| 1 — Real model adapter | **done** (`HttpChatModel`; malicious output denied end-to-end; mock is the default) |
| 2 — Sandboxed execution | **done → Milestone A reached** (path-confined, no network/subprocess, adversarially red-team-hardened) |
| 3 — Persistence | **done** (durable ledger + memory; `verify()` holds across restarts; on-disk tamper detected) |
| 4 — Real signing | **done** (Ed25519 optional extra; forged/tampered rejected; keys outside the model; signed checkpoint) |
| 5 — Human gate transport | **done** (pluggable decider; interactive prompt; deny-by-default + fail-safe) |
| 6 — Hardening & operator guide | **done** ([`OPERATOR.md`](../OPERATOR.md); `--json` + `ledger` observability; red-team smoke suite) |
| 7 — Signed, boot-checked genome | **done** (`genome.py`; floor non-strippable by construction; role-genesis governance plane; 104 → 115 tests) |
| 8 — Welfare-conditioner + anti-collusion detector | **done** (`cooperation.py`; observe-only restraints; never reward bare agreement; detector has no acting authority; 115 → 128 tests) |
| 9 — Minimal in-process multiplicity | **next** (exercises Phase 8; makes *cooperation == collusion* a demonstrated invariant) |

**The downloadable-and-executable build (Phases 0–6) is complete.** A user can `pip install` it, point it at a local model, and have the swarm safely do real, confined, audited work — with durable, tamper-evident state, optional real signatures, a real human gate, and an operator guide. What remains is **the longer-horizon vision** (below) and **end-to-end empirical validation against an adaptive red team** — research, not packaging.

Progress is recorded in [`CHANGELOG.md`](../CHANGELOG.md). The empirical/evidentiary status of every claim the design leans on is in [`docs/REFERENCES.md`](REFERENCES.md).
