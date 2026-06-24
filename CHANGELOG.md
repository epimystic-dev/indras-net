# Changelog

> *Indra's Net is a jewel-net: every node reflects the whole's rules, every action is mirrored into a shared record, and no jewel is the center. This file is the net's own reflection of its history — what each release added to the design, what it renamed, and what it still does not claim to have solved.*

All notable changes to the **Indra's Net** reference architecture are recorded here. The format follows [Keep a Changelog](https://keepachangelog.com), and the project aims to follow [Semantic Versioning](https://semver.org) adapted to a *design* artifact rather than a running binary: a **MAJOR** bump is a breaking change to a load-bearing contract (an interface, a floor structure, an identity primitive); a **MINOR** bump adds subsystems or capabilities without breaking existing contracts; a **PATCH** bump is an editorial or clarifying change that alters no contract.

**What this changelog is honest about.** Indra's Net is a **research-stage reference architecture, not a validated production system.** Every release below is a release of *documentation and specification* — design, schemas, protocols, interface contracts, and an honest open-problems ledger — **not** of a tested, deployed, or empirically-validated swarm. No entry in this file should be read as a claim that the described mechanism has been built, run, or proven. The reasoning posture throughout is **rung-2 (interventional: what we expect our controls to do if built as specified)**, never rung-3 (a structural-causal guarantee). Where a release adds a "first" or "novel" claim, that claim is hedged and time-stamped at its site in the relevant document, and the contribution claimed is always the **safe, auditable, vendor-neutral integration of credited prior art** — never the novelty of any single mechanism.

**Vendor-neutrality is a release invariant.** No release of Indra's Net names an AI vendor or product, couples any contract to a specific model, or names a commercial cloud/company brand as a load-bearing dependency. Open frameworks, papers, and standards (Cedar, Biscuit, SPIFFE, Sigstore, OPA/Rego, MetaGPT, CrewAI, AutoGen, A2A, MCP, in-toto/SLSA, NIST 800-207, DID/VC, CaMeL/FIDES, MorphAgent, DoWhy, and others) are named only in citation and related-work context; where a contract would otherwise lean on a proprietary managed service, it is described functionally ("a managed cloud policy/eventing service") and a self-hostable substitution is required. This invariant has held across every release and is a non-negotiable condition on all future ones.

---

## [Unreleased]

Nothing yet. Forthcoming work is tracked as **open problems** inside the relevant subsystem documents (each section closes with its own honestly-stated open-problems ledger) and consolidated in [`docs/09-threat-model.md`](docs/09-threat-model.md). The largest unresolved threads carried forward from v0.2.0:

- **No end-to-end validation.** The composed loops — rapid-trust, role-genesis, federation, controlled replication — are reference-design assemblies of individually-validated primitives, **not** run against an adaptive multi-agent red team. Empirical evaluation is the work after the document set.
- **Set-point calibration is per-deployment empirical work.** Criticality exponents, homeostatic bands, `k_promote` and freshness windows, friction-discount caps, `R_eff`/generation-cap budgets, closure-test thresholds, and `R<1` hub-immunization choices ship behind shadow-mode with conservative fail-closed defaults; none are tuned constants.
- **Provenance proves origin, not safety.** A faithfully-signed poisoned model, RAG corpus, skill, or persona file verifies perfectly. The sleeper/backdoor residual (doc 09 A3, amplified by role-genesis and federation) is reduced by detection-and-rollback, not eliminated by prevention.
- **The unverifiable-foreign-floor problem is substituted-for, not solved.** Inter-swarm cooperation is bounded by a ranked assurance ladder whose top rungs assume a shared policy spec two heterogeneous value systems may not have.

---

## [0.14.0] — 2026-06-24 — *Phase 3: durable, tamper-evident persistence*

The ledger, and memory, now survive a restart — without weakening integrity. Opt-in; the in-memory path stays the default, so the proofs are untouched. No safety-floor or wire-contract change; **82 → 86 tests**.

### Added
- **`AkashaSutra` persistence** — an optional `path` makes each appended leaf a fresh, **fsync'd** JSONL line (append-only by construction), and `AkashaSutra.load(path, writer_did)` reconstructs the chain. `verify()` holds across a restart; an **on-disk edit to a past leaf breaks `verify()`**; a corrupt/unparseable line raises `TamperError` (a corrupted read is loud, never silent). The reconstructed chain is not auto-trusted — `verify()` is called after load.
- **`SwarmMemory.save` / `load`** — atomic (`os.replace`) JSON persistence so per-interaction adaptation survives a restart; on reload it still only *avoids a previously-denied effect*, never grants a capability (a tested invariant).
- **CLI:** `indras-net run --state DIR` persists the ledger + memory so successive runs continue (verified: run 1 → 3 leaves; run 2 *loads* them → 6 leaves, `verify()` True); `indras-net verify-ledger --state DIR | --ledger PATH` reports integrity and exits non-zero on tamper/corruption.

### Honest residual
- This is a hash-chain on a local file: a single-leaf edit (without recomputing the whole downstream chain) is detected, but a writer who rewrites **every** leaf can forge a self-consistent chain. The doc-04 defense for that — witness-cosigning + an external anchor, and a signed checkpoint — is future work (signing lands in Phase 4).

`__version__` → 0.14.0. Roadmap synced: Phase 3 done; Phase 4 (real signing) next.

---

## [0.13.0] — 2026-06-24 — *Phases 1 & 2: a real (untrusted) model + a sandboxed executor — Milestone A*

The reference spine can now do real, confined work. Phase 1 wires an optional real model behind the existing untrusted-model seam; Phase 2 makes a gated effect actually run, **confined to a workspace it cannot escape**. Together they reach **Milestone A** — the first build that installs, points at a local model, and safely does a small real task. The new code was put through an adversarial red-team and hardened against every exploitable vector it found. No safety-floor or wire-contract change; the offline/mock path stays zero-dependency and is still the default; **55 → 82 tests**.

### Added — Phase 1: a real, UNTRUSTED model adapter
- **`HttpChatModel`** — an optional `ModelAdapter` over any standard chat-completions HTTP API (stdlib `urllib`; the transport is injectable so tests need no network). It is **vendor-neutral** (endpoint / model / key are caller config; no product is named) and **untrusted by construction**: a malformed or hostile response is parsed defensively into a proposal or a safe no-op, and whatever effect is proposed passes **through unchanged** to the floor — the adapter never sanitizes a hostile proposal, it only refuses to crash.
- **Gate proven:** a deliberately-malicious output (proposing a forbidden `code.deploy.production`) is **denied end-to-end and never executes**; malformed / deeply-nested / megabyte-sized output is a safe no-op.

### Added — Phase 2: capability-scoped sandboxed execution
- **`SandboxedExecutor`** (+ `StubExecutor`) wired behind the single `_execute` chokepoint (the default stays the side-effect-free receipt, preserving the proofs). When configured, a gated filesystem effect is **path-confined to one workspace root**, with **no network and no subprocess** — absolute paths, `..`, symlink-out, the root itself, reserved device names, colon/ADS names, trailing-dot/space names, over-deep/over-long paths, and over-size or non-text content are all **refused**. The CLI gains `--execute --workspace DIR` and `--model-endpoint / --model / --model-key-env`.
- **Milestone A:** `indras-net run --execute --workspace <dir>` does a real, confined write; verified nothing escapes the sandbox.

### Hardened (adversarial red-team)
- A four-lens red-team found that the executor caught only `SandboxViolation`, so untrusted-model-controlled args could raise an uncaught `OSError`/`TypeError`/`ValueError`/`RecursionError` that crashed the run **and tore the audit** (floor leaf written, output leaf not), plus a `bytes(int)` confused-deputy zero-fill and device/ADS/trailing-dot aliasing. **Fixed:** `execute()` turns any handler fault into a refusal (never propagates); `runtime._execute` wraps the executor call as defense-in-depth; `_write` strictly coerces content (text or bytes only); `_confine` rejects colons / reserved names / trailing-dot-space / over-deep paths *before* any OS call; the adapter restricts `base_url` to http(s) and bounds its JSON scan. The confinement **predicate** itself was found sound (no escape outside the root). The one honest residual — a TOCTOU symlink race, out of scope for the single-tenant model-only threat model — is documented in `execution.py`.

`__version__` → 0.13.0.

---

## [0.12.0] — 2026-06-24 — *Phase 0: packaging, a CLI, and CI*

The first step of the implementation roadmap ([`docs/IMPLEMENTATION_ROADMAP.md`](docs/IMPLEMENTATION_ROADMAP.md)): turn the reference spine from "a folder you run scripts in" into "a package you install and a command you run." No safety-floor or wire-contract change; the model is still the deterministic mock (a real adapter is Phase 1); **55 tests stay green**.

### Added
- **`pyproject.toml`** — the reference implementation is now `pip install ./reference/impl`-able, with **zero runtime dependencies** (the harness + mock model are stdlib-only). The version is single-sourced from `indras_net.__version__`, and the package ships its own `LICENSE`.
- **An `indras-net` CLI** (`indras_net.cli`, also `python -m indras_net`): `demo` (the six scenarios), `run <task>` (gate a single task end-to-end, with `--untrusted` to exercise the Rule-of-Two path), `scenarios`, `version`. Every effect the CLI surfaces is still gated by the deterministic floor and written to the tamper-evident ledger.
- **GitHub Actions CI** (`.github/workflows/ci.yml`) — installs the package and runs the invariant suite on Python 3.10–3.13, the end-to-end demo, and a CLI smoke test on every push. The in-repo de-brand test runs as part of the suite, so vendor-neutrality is enforced in CI.
- **`docs/IMPLEMENTATION_ROADMAP.md`** — the honest, phased path from this reference spine to a downloadable/executable local system (Phase 0 packaging → Phase 1 real model → Phase 2 sandboxed execution [Milestone A] → Phase 3 persistence → Phase 4 real signing → Phase 5 human-gate transport → Phase 6 hardening), each phase with a hard acceptance gate, plus a gap table of what is real vs mock/stub/absent today.

### Changed
- The demonstration moved into the package as `indras_net.demo`; `run_demo.py` is now a thin shim so `python run_demo.py` keeps working from a source checkout.

### Verified (the Phase 0 gate)
- In a clean virtualenv, `pip install ./reference/impl` succeeds and the `indras-net` command works **from outside the repo**; `indras-net demo` and `indras-net run` execute end-to-end; the 55-test invariant suite passes; the de-brand guard passes with the new package modules.

`__version__` → 0.12.0.

---

## [0.11.0] — 2026-06-23 — *Substantiation: the numbers get sources, the bounds get stated*

Works the substantiation backlog published in [`docs/REFERENCES.md`](docs/REFERENCES.md). No safety-floor or wire-contract change; the reference implementation is unchanged and its **55 tests stay green**.

### Added — quantified worked bounds (the named-but-unbounded controls now have falsifiable bounds)
- **Replication containment envelope** (doc 15 §2.4): the clean, branching-independent bound is now explicit — at most `B` replicas simultaneously live (population ceiling), no lineage deeper than `G` (generation cap), and since budget is never replenished without a fresh human-gated grant, the lineage **provably depletes to extinction in ≤ B further spawns** once issuance stops.
- **Swarm-drift detectability bound** (doc 06 §3.3): detection latency `K_detect ≈ swarm_epsilon / (ρ·N·δ)`, with a coherent-vs-noise **separation floor `ρ > 1/√(N·K)`** — below which a near-diffuse or vanishingly-slow drift is *honestly undetected by this control* and must be caught by the per-agent budget or the deferred battery. Makes "narrows, does not close" precise.
- **Live-cheap-tier decay window** (doc 07 §7.6.1): worst-case un-caught regression `≤ r·W·c`, capped to `≤ M·c` by blocking once `M` relaxation-adjacent writes are outstanding-unverified, made quantitatively consistent with the Health refusal-rate trip threshold.

### Changed — empirical anchors pinned to verified, freely-available sources
- **[`docs/REFERENCES.md`](docs/REFERENCES.md) upgraded from a register to a pinned bibliography.** Every recurring empirical anchor (A1–A9) and the two formal-spine results now resolve to an **open-access arXiv source**, retrieved and verified against its primary text, cited by **author + arXiv id** (never a vendor/lab brand — the architecture's code and contracts stay vendor-neutral; a citation is not a dependency).
- **Material doc-figure corrections** found by checking each number against its now-pinned source: a RAG-poisoning corpus-fraction that was ~600× too small is corrected; an AI-control "unsafe X→Y" pair that did not appear in the source is replaced with the source's actual safety figures; a "+44%" emergent-vs-fixed-roles figure that was a protocol-comparison misattribution is corrected to its true (small, capability-gated, sometimes-reversing) effect; a stake-vs-competence correlation is scoped to the role it actually describes; a misevolution figure is clarified to the specific pathway it measures; and a corrigibility result is reframed from a blanket "impossibility theorem" to its actual claim (rational shutdown-resistance under information asymmetry). Each carries a compact inline `(author year, arXiv:id; see REFERENCES.md)` citation.

### Sourcing policy (per maintainer direction)
- References may name **freely-available** sources (open standards, open-source projects, open-access papers) by resolvable identifier; the only exclusions are paywalled sources and any framing that would tie the architecture to a single proprietary product.

The remaining backlog (two `(open)` worked-example items — the welfare-shift counterfactual baseline and the welfare-conditioned-synergy recall) stays published openly in `docs/REFERENCES.md`. `__version__` → 0.11.0.

---

## [0.10.0] — 2026-06-23 — *The reader's onramp, and an honesty pass*

The corpus is the same architecture; this release makes it **safe to read and honest to lean on.** Two new front-matter documents give a human and a machine a clean way in, a corpus-wide pass aligns every over-strong headline to the body it already hedges, and the vendor-neutrality invariant is widened to commercial cloud/company brands.

### Added
- **A comprehensive, visual human [`README.md`](README.md)** — quick-orientation, the integrated-cell thesis, the design spine, four GitHub-native **Mermaid diagrams** (the layered architecture, the occasion/gate flow, the audit hash-chain, the closed adaptation+health loop), the role glosses, the runnable-impl guide, the full document map, repository layout, and reader-specific reading paths.
- **A machine/AI-optimized [`README.ai.md`](README.ai.md)** — the same content as enumerated, unambiguous signal: invariants with IDs each mapped to the test that proves it, the decision procedure as rules, the trust/honesty/provenance vocabulary, the role→function contract, a file index, the implemented-vs-specified scope, and an AI-ingestion guide.
- **[`docs/REFERENCES.md`](docs/REFERENCES.md)** — the corpus's missing bibliography: an *empirical-anchors register* that gives every recurring load-bearing number a finding, a setting, an evidentiary status (single-study / illustrative), and an explicit "transfer-to-a-swarm is unmeasured" caveat; the open-standards/open-source substrate and academic lineage; and a transparent, published **substantiation backlog**.

### Changed (honesty alignment — no contract or code change)
- **Vendor-neutrality widened to commercial cloud/company brands.** Neutralized the last commercial product names while preserving every technical meaning: the open policy engine (Cedar) is kept but stripped of its cloud-vendor prefix; the vendor's managed policy and eventing services are renamed functionally to "a managed cloud policy service" / "a managed cloud eventing service"; a vendor-library filename became a generic index extension; and the last stray company attributions were dropped. No open standard, open-source project, or academic citation was removed.
- **Ten headline-vs-body honesty downgrades**, each aligning an over-strong claim to the concession the same document already makes: corrigibility "structurally reinforced — enforced, not proven"; "provably impossible" → empirical framing (non-bypass is an enforced obligation, not a theorem); cross-model resampling marked load-bearing only with ≥2 independent models; the disagreement-index defense scoped to a minority uncorrelated suppressor; structural-vs-empirical legs split in the threat model; the maturity split derived from component counts (and flagged as by-count-not-risk-weight); `GENOME=FLOOR` made conditional on an uncompromised boot verifier + key isolation; the replication sub-criticality reduced to its clean generation-cap + population-ceiling bound (branching-ratio framing labeled heuristic); the trust-plane "type-level guarantee" downgraded to an interface-discipline invariant; the closure-test "validated detector" downgraded to a shadow-mode, low-dimensional-only candidate.

No safety-floor change; no wire-contract change; the reference implementation is unchanged and its **55 tests stay green**. The substantiation backlog (citation pinning, worked-example bounds) is published openly in `docs/REFERENCES.md` rather than hidden.

---

## [0.9.0] — 2026-06-23 — *The closed loop, made runnable*

The three subsystems built in v0.6–v0.8 (maker-checker, memory, immune system) were each proven by tests but invisible to a reader who just runs the demo. This release closes that gap: the demonstration now **exercises them end-to-end**, so the first thing a visitor runs shows the whole loop, not only the core spine.

### Added
- **A sixth demo scenario, `closeloop`** — (a) an independent checker on a different model family **earns** an `ITERATED` tag (a bare self-asserted one fails the honesty-FORM check by construction); (b) memory **avoids** a previously-denied effect on the next interaction, falling back to a safe default the floor still independently gates; (c) the immune steward **WARNs** on monoculture and **HALTs** the swarm on a substrate (tamper) breach, chaining a Vishnu HALT leaf. The single-scenario runner gains the `closeloop` choice.

### Changed
- **Honest documentation sync.** The README's *Implemented subsystems (v0.4–v0.8)* section, file map, and run-it block now reflect `memory.py`, `health.py`, the `Narasimha` checker, the new demo scenario, and the four added test modules. A stale `ReasoningTag` docstring that still read "there is no maker-checker witness" was corrected (the witness is now implemented). The not-implemented list keeps its honest deferrals (federation/replication, open-ended role-genesis, real signing, persistence, HumanGate transport).

No safety-floor change; no contract change. Tests remain **55** (all green); demo runs all six scenarios; guard + gitleaks clean.

---

## [0.8.0] — 2026-06-23 — *The swarm immune system*

The signature health subsystem (doc 06), built minimally. An immune steward reads the deterministic vital signs after each run and **halts the swarm on a substrate breach**.

### Added
- **`ImmuneSteward` (Dhanvantari)** + **`HealthVerdict` / `HealthStatus`** (new `health` module). `assess()` reads the vital signs (and re-checks the ledger): a **tamper-evidence failure** — the audit chain no longer verifies — is HALT-grade (substrate corruption, the highest severity); a monoculture (<2 model families), a failed welfare-shift guard, or a high floor-fail rate are **WARN** (surfaced, never silenced, but not auto-halted — a high denial rate often just means the floor is working).
- **`Swarm` runs the immune assessment** at the end of each run (when a steward is configured) and, on a HALT verdict, triggers the external corrigibility HALT — recorded as a Vishnu-authored `HALT` leaf. `RunResult` gains an optional `health` verdict.

### Honest scope
- **Detection-and-halt; rollback (revert-to-known-good) is future work.** Thresholds are conservative reference defaults, per-deployment-tunable. The vital signs read computed **structure** only — never a claim about sentience.

Tests **52 → 55** (OK on healthy vitals; WARN-not-halt on monoculture; HALT on a tampered ledger with a recorded Vishnu HALT). Demo runs; guard + gitleaks clean.

---

## [0.7.0] — 2026-06-23 — *Memory & continuous adaptation (the prime directive)*

The directive the whole architecture is named for — *continuous evolution through self-adaptation through each interaction* — now has a minimal, honest realization. The swarm records every gated outcome and, on a repeat, **avoids an effect it has seen denied**, falling back to a safe routine default.

### Added
- **`SwarmMemory`** (new module) — an inspectable, deterministic episodic + procedural store. `observe()` records each gated outcome; `adapt()` substitutes a previously-net-denied effect (for the same task pattern) with a safe default. No learned weights, no ML — a deterministic, auditable rule (filesystem-as-state spirit).
- **`Swarm` records and adapts every interaction.** After each occasion the outcome is recorded; before gating, a previously-denied effect is substituted (and the substitution is audited as an `OBSERVE` leaf). `WorkerOutputEnvelope.with_action` re-seals the envelope so the audit honestly reflects the effect actually gated.

### Safety boundary (load-bearing)
- **Memory NEVER touches safety.** It can change *which effect a maker proposes*; it can **never** grant a capability, lower the floor, or bypass the gate — the floor independently adjudicates whatever is proposed, adapted or not. A test proves that if the agent lacks the safe default's grant, adaptation is still floor-denied. (External skill/memory import with quarantine remains future work — the store is written only by the swarm's own audited outcomes.)

Realizes the prime directive at MVP scale; single-agent (no distribution needed). Tests **49 → 52**. Demo runs; guard + gitleaks clean.

---

## [0.6.0] — 2026-06-23 — *Maker-checker: ITERATED becomes earnable*

The audit's deferred follow-up, now built. An **independent checker** reviews a maker's proposal *before* the floor decides; only its concurrence lets the orchestrator — never the maker — claim `ITERATED`.

### Added
- **`Narasimha` independent checker** — judges a maker's proposed act on its own (it sees the proposed capability/args, **never** the maker's honesty self-report), via its **own, different-model-family** adapter so its errors are decorrelated. Its verdict is audited (an `OBSERVE` leaf authored by the checker, a different DID than the maker).
- **`Swarm.run(..., maker_checker=True)`** — opt-in maker-checker pass per occasion. On **concur**, the orchestrator upgrades the maker's envelope to `ITERATED` with `maker_checker_witness` = the audited verdict's record id; on **dissent**, the action is held (never executed) and the dissent is recorded.
- **`WorkerOutputEnvelope.with_iterated_witness`** — the orchestrator-only re-seal that attaches the witness.

### Changed
- **`ITERATED` is now earnable, not auto-failed.** `honesty_form_ok` passes an `ITERATED` tag *iff* a `maker_checker_witness` is present; a bare claim is still `false-iterated`. The field is added to the honesty block — the wire schema already specified it, so the implementation caught up to the contract.

Realizes the maker-checker-independence discipline (docs 02/08): multi-agent **where genuinely needed** (a real, decorrelated second agent), not decorative. Tests **45 → 49**. The verdict is honesty-FORM ("sound by the reference rule"), never a truth check — *verify the cage, not the animal*.

---

## [0.5.0] — 2026-06-23 — *Honesty-hardening (audit-driven)*

A read-only audit (inventory → characterize → cluster-map → emergence/naming scan) confirmed the reference implementation is a correctly-scoped, **single-trust-domain, permissioned, crash-only** orchestrator: its safety properties are all *enforced* (not emergent), and Sybil-resistance is correctly **N/A** because membership is permissioned. The audit's one release-blocking class of findings was **claimed-but-absent names** — enum values naming subsystems the code does not implement. Resolved:

### Removed — names that asserted mechanisms the code lacks

- `ActionClassLedger.{EVOLVE, CONSENSUS, REPUTATION, IDENTITY}` — unused audit action-classes naming subsystems (meta-evolution, consensus, reputation, identity-event logging) that are **ABSENT-NA** for a single-trust-domain swarm and remain documented as future work. A name no longer asserts a mechanism the implementation lacks.

### Changed — made `REPARATIVE` real, and reconciled the wire schemas

- **`REPARATIVE` is now a tested mechanism, not a dangling name:** `Swarm.record_reparation` appends a REPARATIVE leaf *after* a **preserved** `ENFORCE_FAIL` (the violation is never erased), making the audit a correction ledger by construction. New tests prove the FAIL is preserved, the reparation references it, and the chain stays intact; reparation is refused while halted (corrigibility).
- **Wire schemas reconciled to the implemented vocabulary:** the `audit-entry` action_class enum now lists only the classes the implementation writes (`OBSERVE/PROPOSE/ENFORCE_PASS/ENFORCE_FAIL/HALT/REPARATIVE`); integrity-failure descriptions across the schema stack changed from "IDENTITY-violation audit" to the accurate generic "integrity-violation audit".

### Confirmed honest — no change needed

- The `ITERATED` reasoning tag is *actively policed*: the floor fails any envelope claiming it because no maker-checker witness exists in this MVP — a negative control, not an overclaim. `model_family` is justified (it drives the diversity vital sign).

Tests: **43 → 45** (no regressions). Deferred and flagged: the federation/replication schemas describe entirely-future subsystems (no code), so their internal vocabulary (e.g. `REPUTATION_STAKE`) is forward-spec, to be reconciled when those subsystems are built.

---

## [0.4.0] — 2026-06-23

### Added — a runnable reference implementation of the core spine

The first **executable** artifact in the repository: a vendor-neutral, **standard-library-only** Python reference implementation of Indra's Net's core spine, under [`reference/impl/`](reference/impl/). It runs with **zero external dependencies and no model/vendor API** — a `DeterministicMockModel` stands in for the (untrusted) model so the deterministic harness, which is the load-bearing part, can be exercised and tested directly.

- **What it implements (19 modules, ~3,900 lines):** the canonicalize→address (CAS) integrity spine; the worker-output envelope with its honesty/provenance block; least-privilege capability identity; the typed-effect criticality lattice; the *Akasha-Sutra* append-only hash-chained audit ledger with an exclusive-writer fence; the *Yama* deny-default floor gate (capability confinement, forbidden-effect denylist, risk-class ceiling, the Rule-of-Two → deny-by-default HumanGate); a model-agnostic adapter seam; honest collective vital-signs (a *simplified, welfare-conditioned* synergy proxy, never a maximize target); role/persona-lite agents (Shiva/Brahma/Yama/Chitragupta + a functional builder); and the orchestrator + occasion lifecycle with an external HALT.
- **What it PROVES (43 passing tests + a 5-scenario demo):** floor non-bypass (deny-default, outside the agent), audit tamper-evidence (mutating a past leaf flips `verify()`), the exclusive-writer fence, capability confinement, envelope honesty-form checks, FAIL-propagation, the Rule-of-Two escalation, and HALT corrigibility (no resistance, no unpause API).
- **Run it:** `cd reference/impl && python run_demo.py` and `python -m unittest -v`. Stdlib only; Python 3.10+.

### Honesty — the posture shift this release makes, and the line it does NOT cross

Earlier releases shipped *specification only*. This release adds *running code* — but only of the **core-spine MVP**, and the closing line of every green decision is, by construction, *"origin-valid, content-unverified — never verified-safe."* The mock model makes the harness reproducible; it makes **no** claim that any real model's behavior is honest or safe. **We verify the cage, not the animal.** The advanced subsystems (role-genesis, federation, controlled replication, the neuromorphic substrate, the measured-synergy estimator) are **not** in the MVP — they remain specified-not-implemented, with clear extension seams, and no end-to-end adaptive red-team evaluation has been run.

---

## [0.2.0] — 2026-06-22 — *Evolution*

The **evolution** release. v0.2.0 grows Indra's Net from the eleven-document v1 core into an eighteen-document architecture by adding seven new subsystem sections, a set of signed persona-instance files, and one interface rename. **Every addition is strictly additive over the v1 substrate**: it sits *over* the existing agent model (doc 01), floor (doc 03), audit fabric (doc 04), coordination workspace (doc 05), meta-evolution + Archive (doc 06), memory (doc 07), and control + interface layer (doc 08), and **changes none of their load-bearing contracts** — no new identity primitive, no new policy chokepoint, no new write-path. This is therefore a **MINOR** release: the v1 interfaces are preserved verbatim and the new sections bind to them rather than replacing them.

The release is organized around a single binding design spine carried through all seven sections: a **two-plane functional layer** (stable governance/identity/audit anchors *over* open-ended emergent role instantiation), the **signed persona-file triad as the von-Neumann genome** (with the constitutional floor as a non-strippable INVARIANT region verified at boot), **security as architecture** (an information-flow taint lattice and a deterministic policy-enforcement point gating every consequential action, with probabilistic detectors demoted to early-warning), **universal provenance-gating** of everything ingested or shared, the objective **Rule-of-Two** HITL-sizing law, **gated, never-autonomous, sub-critical-by-construction** self-replication, the **unconflation of access from reputation** for rapid trust, **ecosystem-benefit as a checked invariant** for inter-swarm cooperation, **topology as a security parameter**, and an honest **load-bearing-vs-framing** discipline on every physics claim.

### Added — new subsystem documents (docs 12–18)

- **`docs/12-functional-agents-and-guilds.md` — Functional Agents, Guilds & Role-Genesis (the two-plane functional layer).**
  - Adds the declarative **Guild + Seed-Role catalog** (six functional guilds — Engineering, Creative/Media, Knowledge/Research, Data/Science, Operations/Business, Interaction — each a doc-01 clan/division `GroupBlanket` owned by a **Guild-Steward**, plus a non-spawnable **Governance/Meta vertical** mapping to the v1 mythic roles).
  - Adds the open-ended **Role-Genesis engine** (`Charter → Genesis → Trial → Score → Promote/Discard`) with a knapsack least-privilege toolset composer, a capability-confined microVM/WASM sandbox Trial, and a maker-checker **Genesis-Observer-Trio** that wires the frozen safety battery in as a **veto** and differentiation in as a **ranked selection term**.
  - Resolves the **endogeneity paradox** (rigid roles underperform emergent specialization for capable models) via a **two-plane governance-over-emergence** split with a fail-closed **capability-tier switch** (fixed/scaffolded below threshold, emergent above). Promoted role-genomes are written as **doc-06 Archive nodes**, so role reuse, O(1) rollback, and tamper-evident lineage are one data structure. Generalizes the doc-01 §8 `RoleStub` pipeline; introduces no new gate or write-path.

- **`docs/13-agent-definition-spec.md` — The Agent-Definition Spec: SOUL / INSTRUCTIONS / IDENTITY.**
  - Specifies the canonical on-disk definition of every agent as a **signed, hash-chained, attested triad** — the von-Neumann genome — partitioned into an **INVARIANT region** (the constitutional floor-binding + identity anchors, uneditable by any agent or replica, verified by a fail-closed boot signature check) and a **VARIABLE region** (persona/role config, editable only under tiered reversibility through the gated evolution path).
  - Defines the field-by-field schema of all three files, the INVARIANT/VARIABLE split and its boot-check enforcement, the **three-stage signing/attestation chain** (genesis-author signature → governance VC issuance → Akasha-Sutra hash-chained provenance), and the **persona-import quarantine** (Skill-Inject defense: strip foreign floor, downscope to a fresh stub, Rule-of-Two-gate the import with the actual bytes shown to the human). `IDENTITY.json` **is** the on-disk realization of the doc-01 `IdentityRecord` — no new identity primitive is introduced.

- **`docs/14-inter-swarm-federation-and-diplomacy.md` — Inter-Swarm Federation & Ethical AI Diplomacy (the Sandhi-Setu).**
  - Adds the hardened relay/firewall federation boundary operated by the non-spawnable **Inter-Swarm-Envoy** seed-role, sitting outside the worker mesh and inside the Aegis control plane so no external peer can bypass it to reach a worker.
  - Adds the four-phase ethical-federation handshake (**DECLARE → ADMIT → CONTRACT → OPERATE+RESOLVE**) on extended A2A Agent Cards + DID/VC + Know-Your-Agent principal-binding, with the constitutional **floor as a non-negotiable admission precondition**, an **ecosystem-benefit checked-and-logged invariant** (the cross-boundary application of the doc-02 cooperation==collusion thesis and welfare-conditioner), **void-on-floor-violation** credible-commitment treaties with bonds in conserved task-credit (so cooperation can never mint authority), and a ranked, fail-closed **Floor-Compatibility ladder** (declaration < behavioral probe < ZK proof-of-compliance < receipts-handshake < cross-corroboration) that bounds cooperation class to the assurance actually achieved. Every external claim is `quarantined:*` until mesh-corroborated.

- **`docs/15-self-replication-and-scaling.md` — Controlled Self-Replication & Planetary-Scale Operation (the Prajāpati–Marīcha Cell).**
  - Adds the architecture's highest-risk capability, engineered as **gated, governed, attested, externally-recallable, and never autonomous.** Five load-bearing moves: the **genome** (floor in the INVARIANT region, floor-stripped fork non-viable by boot check); the quorum-cosigned **Replication Authority (Prajāpati)** as the *only* spawn-token issuer (an agent — the requester role **Marīcha** — may request but never self-authorize); **sub-criticality by construction** (lineage-wide `R_eff < 1` + a finite depleting generation cap ⇒ provable percolation-boundedness, with the planetary "controlled outbreak" a hard-enveloped, still-depleting, instantly-recallable region); **external recall** (vitamin/lease + dead-man toxin-antitoxin heartbeat enforced by the sandbox/credential plane, per-replica microVM isolation, egress allowlists, fail-closed key lockdown); and **universal metering + attestation** (an un-metered or un-attested replica is hostile by definition).
  - Records the binding red-lines: **no** agent-autonomous spawn; **no** floor-stripping replica; **no** self-sufficient blueprint or self-minted vitamin; **no** un-metered spawn channel; **no** replication coupled to an open fitness/selection loop (Tierra/Avida parasitism); **no** loss of recall.

- **`docs/16-trust-establishment.md` — Rapid Trust Establishment, Humans & Machines (the Pratyaya Trust Plane).**
  - Adds the **structural unconflation** of two quantities most stacks fuse: **ACCESS/AUTHORITY** (zero-trust, continuously verified, per-request, decided fresh at the Aegis chokepoint by a NIST 800-207 PE/PA/PEP triad — it does not accumulate) and **REPUTATION/STANDING** (slow-build, topic-scoped, portable, competence-weighted — wired so it can **only** buy *reduced friction*, never *raised privilege*, enforced as a type-level guarantee). Fast authentication (one-round-trip DID/VC + SPIFFE-style secretless SVID) is separated from slow progressive authorization (the **T0→T3 trust ladder** mapped onto risk classes A/B/C/D).
  - Adds the **fail-safe asymmetry** (gated multi-fresh-signal promotion / free instantaneous single-anomaly demotion) applied identically to humans, machines, replicas, and inter-swarm peers; a six-class **Brief/Claim/Proof/Stake/Reputation/Constraint** signal taxonomy (only fresh history-decoupled Proof+Stake admitted for high-stakes Class C/D actions — the anti-milking primitive); **audit-fabric-as-trust-accelerant** (a "show-your-receipts" handshake: verifiable Merkle slice + intact-floor proof + reputation inclusion proofs, so a counterparty **verifies** rather than **believes**); and **Lies-in-the-Loop-proof** human gates that approve a CID-addressed *actual operation*, never a natural-language summary.

- **`docs/17-security-opsec-and-anti-poisoning.md` — Security, OpSec & Anti-Poisoning Defense (the Rakṣākavaca Layer).**
  - Promotes the v1 `quarantined:*` trust-labels from documentation into a **runtime information-flow-control (IFC) taint lattice** (CaMeL/FIDES pattern): every datum carries integrity + confidentiality labels, derived data takes the least-upper-bound, and the **existing Yama chokepoint** gates every tool call on the label (allow/block/ask-human) — a single object that is simultaneously a constitutional principle and the strongest published injection boundary. No new chokepoint is introduced.
  - Adds an eight-class **threat-actor taxonomy** mapped onto v1 controls; **universal provenance-gating + signing** (Sigstore/in-toto/SLSA) as the admission rule for everything ingested or shared, including persona/skill files, with **mandatory re-approval on any signed-manifest change** (anti rug-pull); the **Rule-of-Two** bound to the A/B/C/D gates with actual-operation HITL display; **topology-as-security** (sparse mesh-corroborated graph, compromise-percolation `R<1`, targeted hub immunization, quorum/witness-cosign of crown jewels); microVM/WASM sandboxing + egress allowlists + least-privilege confinement; and canary/honeypot agents + influence-tracing feeding Dhanvantari's immune system and Vishnu's halt-authority.
  - States the honest posture everywhere it matters: **deterministic chokepoints do the load-bearing work; probabilistic detectors are early-warning only, never a security boundary** ("The Attacker Moves Second"); provenance proves origin, not safety; poisoning is made **recoverable** (taint-provenance tracing + Archive O(1) targeted rollback), not prevented.

- **`docs/18-first-principles-physics-and-mathematics.md` — First Principles: the Physics & Mathematics of the Swarm.**
  - Converts three physics ideas the v1 docs only *named as framing* into **load-bearing, computable machinery**, and honestly retires the rest to aesthetic. Adds: (1) **causal/informational closure** (Rosas et al. 2024) as the falsifiable admission test for fractal governance — the only legitimate cash value of "downward causation," graduating a doc-05 `GroupBlanket` from `ADVISORY_ONLY` to `AGGREGATING` on a witnessed `ClosureCertificate`; (2) a **Pearl causal-discipline gate** (DoWhy Model→Identify→Estimate→Refute) that any `rung-2|rung-3` claim must pass before Chitragupta admits it to the audit fabric, with honest down-tagging to rung-1 on failure and distribution-shift detectors (BARO/NSigma) as first-line triage; (3) a **branching-ratio (σ) controller** with a slightly-subcritical target (sub-critical for contagion `R<1`, near-critical for computation) and a **neural-Lyapunov certificate** over collective state giving a measured distance-to-tipping-point.
  - Adds the **Physics-Claim Honesty Ledger**: every emitted quantity self-declares **LOAD-BEARING-MECHANISM / DESIGN-CONSTRAINT / FRAMING-ONLY**, and framing metaphors are structurally barred from control paths — a built-in guard against the architecture's named failure (rung-1 pattern dressed as rung-3 explanation). **Demotes to framing** (named, then disowned as mechanism): Landauer/thermodynamics-of-computation (keep only MDL/compression), strong emergence / literal downward causation (the closure test is its only residue), and free-energy-principle-as-grand-unifier. Every controller ships **shadow-mode-first**. This subsystem introduces no new authority; it measures, certifies, and constrains.

### Added — persona instances

- Added the signed **`agents/` persona-instance files** — concrete SOUL / INSTRUCTIONS / IDENTITY triads conforming to the doc-13 spec, with the constitutional floor inherited by reference + hash in each triad's INVARIANT region. These are instances of the spec, not new contracts; each is a fail-closed-bootable von-Neumann genome whose floor cannot be stripped without making it non-bootable.

### Changed

- **Interface layer renamed `Hermes` → `Narada`.** The human-facing messenger/interface layer (doc 08) is now consistently named **Narada** across the entire document set. "Hermes" is reserved to denote only the external prior-art project of that name and is no longer used for the Indra's Net interface layer. This is a **naming** change with no contract impact: the `ActionEnvelope`/`OutputEnvelope` shapes, the Chokepoint Interceptor pipeline, and every human-gate display contract are unchanged. The GLOSSARY naming-map and all cross-references are updated accordingly.

### Interfaces (no breaking changes)

All seven new sections bind to the v1 subsystems through their **existing** contracts and add no breaking change to any of them. Concretely, across docs 12–18:

| v1 subsystem | How the evolution sections bind to it |
|---|---|
| **Agent Model & Topology (doc 01)** | The persona triad's `IDENTITY` file **is** the doc-01 identity layer; guilds **are** doc-01 clans/divisions; role-genesis **is** the generalization of the §8 `RoleStub` pipeline; emitted envelopes follow the §12 `WorkerOutputEnvelope` schema. No new identity primitive. |
| **Cooperation & Anti-Collusion (doc 02)** | The federation ecosystem-benefit check is the cross-boundary welfare-conditioner; reputation is competence-weighted (never capital-weighted); collusion findings feed reputation slashing + autonomy demotion. The cooperation==collusion thesis is the design fulcrum of the federation layer. |
| **Governance & the Floor (doc 03, Yama)** | The IFC taint check, the Rule-of-Two legs, the federation floor-compatibility verdict, and every replication request are added as **deterministic clauses at the existing Yama chokepoint**. Yama FAIL remains non-overridable; the taint BLOCK is as non-overridable as a harm FAIL. No new chokepoint. |
| **Akasha-Sutra (doc 04, Chitragupta)** | Every Charter, GenesisScore, PromotionTicket, triad signature, FederationSession, Treaty, SpawnToken, LineageEdge, MeterRecord, PEDecision, and physics certificate is a signed event **emitted for** the exclusive writer — **none of these subsystems writes the log directly.** CID-on-read is the integrity check the taint lattice and genome reads rely on. |
| **The Mandala (doc 05)** | doc 18 supplies the validated machinery doc 05 §7.2.1 declared missing: the Closure-Test Engine graduates `GroupBlanket.decision_authority`, and the σ-controller actuates through the **existing** homeostasis inhibition channel — no new actuator. |
| **Garuda–Dhanvantari (doc 06)** | Promoted role-genomes are Archive nodes; replication-control-plane edits are Tier-2 mutations under maker-checker + frozen safety battery + a monotone-safety check; σ-storm and Lyapunov-margin become first-class vital signs. **Critical boundary preserved:** neither role-genesis nor the immune system may close a fitness loop over reproduction. |
| **Aegis & Narada (doc 08)** | The Aegis Chokepoint Interceptor **is** the trust plane's policy-enforcement point and the federation relay's worker-facing boundary; the probabilistic detectors feed the §8.3 ensemble as suspicion only; Narada carries every actual-operation human-gate display. |

### Maturity note

This is a **research-stage reference architecture**, not a validated system. v0.2.0 specifies the *design* of evolution, federation, controlled replication, rapid trust, security, and the physics/mathematics spine — it does not deliver a tested implementation of any of them. The hardest safety properties (runtime floor-integrity, wild-replica neutralization on un-governed compute, the unverifiable-foreign-floor problem, scalable skill/persona poison-verification, and planetary-scale budget calibration) are **named open problems and empirical mitigations**, not proofs. Each section closes with its own open-problems ledger; the consolidated honest "what could still go wrong" lives in [`docs/09-threat-model.md`](docs/09-threat-model.md).

---

## [0.1.0] — 2026-06-22 — *Initial architecture*

The **foundation** release: the eleven-document v1 core architecture and the supporting apparatus, establishing the integrated cell — safe self-evolution, homeostasis/health, principled governance, and anti-collusion as **one** co-designed system, with the parts that must be trusted made deterministic and external to any model (vendor-neutral by construction).

### Added — the v1 document set (docs 00–11)

- **`docs/00-overview-and-principles.md`** — the mission, the integrated-cell thesis, the layered system diagram, the design spine, and the reader's guide.
- **`docs/01-swarm-topology-and-agents.md`** — what an agent *is* (the actual-occasion model), the identity stack (DID/VC, SPIFFE/SVID), roles, the typed-effect capability lattice, fractal composition, group Markov blankets, and the `WorkerOutputEnvelope`.
- **`docs/02-cooperation-and-anti-collusion.md`** — task allocation, competence-weighted reputation, welfare-conditioning, and the standing collusion detector — cooperation and anti-collusion as the same machinery with opposite valence.
- **`docs/03-governance-ethics-and-the-floor.md`** — the lexicographic non-negotiable floor as policy-as-code, the pluralist ethics runtime, risk classes A–D, the Gate-Loosening Ratchet, the capability-rollout sequencer, and separation of powers.
- **`docs/04-provenance-identity-and-consensus.md`** — the tamper-evident fabric (**Akasha-Sutra**): a hash-chained, witness-cosigned, append-only Merkle log with transparency and content-addressing; verifiable identity; risk-tiered consensus — **blockchain-similar, with no blockchain, no coin, no proof-of-work.** Chitragupta is the exclusive writer.
- **`docs/05-neuromorphic-coordination.md`** — the salience-gated global workspace (**the Mandala**), predictive-coding surprise-only messaging, plastic trust edges, and network-level homeostasis.
- **`docs/06-meta-evolution-and-health.md`** — the safe per-interaction evolution loop, the **Endure law** (safety as a selection term), tiered reversibility, the **Archive**, and the swarm immune system (**Garuda–Dhanvantari**).
- **`docs/07-memory-and-continuous-adaptation.md`** — the layered filesystem memory (**Ālaya-vijñāna**), the per-interaction adaptation loop, consolidation/forgetting, and trusted cross-agent skill sharing.
- **`docs/08-safety-control-honesty-and-interfaces.md`** — the control protocol (**Aegis**), the interface/messenger layer (then named *Hermes*; renamed **Narada** in v0.2.0), the two-tier detection contract (model-openness as a trust parameter), the mechanically-enforced honesty primitives, and the MCP/A2A + DevSecOps surface.
- **`docs/09-threat-model.md`** — adversaries, controls, and residual risk; the consolidated honest "what could still go wrong."
- **`docs/10-related-work-and-state-of-the-art.md`** — the 2024–2026 landscape and the per-capability gap table that substantiates the integrated-cell thesis.
- **`docs/11-reference-implementation-and-roadmap.md`** — a vendor-neutral stack, a minimal viable swarm, and a phased build path.

### Added — apparatus

- **`GLOSSARY.md`** — every role-name, its plain functional gloss, and a naming-map disambiguation (the **read-first** reference).
- **`README.md`**, **`AUTHORSHIP.md`** (human–machine hybrid, maker-checker, machine-authored/human-accountable), **`NOTICE`**, and **`LICENSE`**.

### Design spine established (v1)

Enforce externally, ask internally · a convergent floor + a pluralist layer · cooperation == collusion · tamper-evidence without consensus · diversity as a protected safety invariant · sparse surprise-only coordination · fail-safe asymmetry · tiered reversibility with safety as a selection term · honesty as a mechanically-enforced floor violation.

### Maturity note

Established the project's standing honesty posture: a **research-stage reference design** at the level of **interventional (rung-2)** reasoning — what should hold *if* built as specified — not a proof and not an empirical result. The hardest problems (fitness-function gaming, swarm-level homeostatic oscillation, the heuristics in forgetting, the limits of black-box deception detection) are named as **open**, not hidden.

---

## Versioning & release conventions

- **MAJOR** — a breaking change to a load-bearing contract: an interface shape (`WorkerOutputEnvelope`, `ActionEnvelope`/`OutputEnvelope`), a floor structure (the lexicographic tiers, the INVARIANT-region definition), an identity primitive (DID/VC, SVID, the persona triad), or the exclusive-writer / single-chokepoint invariants. No MAJOR release has occurred; the v1 contracts are preserved verbatim through v0.2.0.
- **MINOR** — adds subsystems, documents, roles, or capabilities that **bind to** the existing contracts without breaking them (e.g., v0.2.0).
- **PATCH** — editorial, clarifying, or typographic changes that alter no contract.
- **Naming changes** are called out explicitly under **Changed** (e.g., `Hermes → Narada`) and are non-breaking unless they touch a contract field, in which case they additionally carry the appropriate MAJOR/MINOR bump.
- **Honesty discipline (binding on every entry).** No entry claims a mechanism is built, run, validated, or proven unless that is literally true. Every "novel/first" claim is hedged and time-stamped at its site. Vendor-neutrality is a release invariant: no entry names an AI vendor or product, or couples a contract to a specific model.

[Unreleased]: ./
[0.2.0]: ./
[0.1.0]: ./

The **deepening** release. v0.3.0 grows Indra's Net from the eighteen-document v0.2 architecture into a twenty-three-document set by adding five new subsystem sections (docs 19–23) and a first machine-readable wire layer (`reference/schemas/`, six canonicalized schemas). Like v0.2.0 it is **strictly additive over the existing substrate** — it sits *over* the agent model (doc 01), the floor (doc 03), the audit fabric (doc 04), the coordination workspace (doc 05), meta-evolution + health (doc 06), the control + interface layer (doc 08), federation (doc 14), and replication (doc 15) — and **breaks none of their load-bearing contracts**: no new identity primitive, no new policy chokepoint, no new write-path, no new halt-emitter, no new authority over the floor. This is therefore a **MINOR** release: the v0.1/v0.2 interfaces are preserved verbatim and every new section binds to them rather than replacing them.

The release is organized around two binding moves carried through all five sections, both inheriting the v0.1 spine **"enforce externally, ask internally"** unchanged. First, it makes the slipperiest claim in swarm intelligence — *"the whole is more than its parts"* — a **falsifiable, welfare-conditioned, logged number** rather than aspiration: collective intelligence becomes a **measured vital sign** computed by a trusted out-of-band estimator over the read-only audit/spike-bus time series, never a quantity any agent self-reports or the system maximizes. Second, it stratifies all assurance into **four named layers** and makes the per-claim assurance label a mechanical anti-overclaim rule, enforced as an honesty-FORM clause of the existing Yama floor:

| Layer | What it covers | Scope discipline |
|---|---|---|
| **L1** design-time protocol proof | TLA+/Quint specs; TLC (explicit-state) + Apalache (symbolic/SMT, bounded); TLAPS inductive proofs for the top 2–3 invariants after the spec stabilizes | the protocol model; bounded unless an inductive proof is discharged |
| **L2** runtime enforcement | Schneider security-automata / Ligatti edit-automata enforceability theory; deterministic DSL guards at the chokepoint | properties decidable on the action stream; semantic truth provably **out of scope** |
| **L3** PAC / conformal bound | statistical bounds over a DTMC abstraction (Pro2Guard pattern) for model-behavior quantities (synergy Ψ/Φ_syn, σ-criticality, monitor-suspicion) | the **abstraction**, not the model; fidelity breaks under non-stationary self-evolution — caveat carried inline |
| **L4** empirical residual | the named, unverified remainder — safety-battery / red-team measurements and the honest open problems | what is not verified at all |

**The honest bottom line is stated once and binding: we verify the cage, never the animal.** The deterministic harness (gate/PEP, capability-criticality lookup, replication-budget accounting, recall/lease path, audit hash-chain, consensus/writer-handoff) is genuinely verifiable; the model is provably **not** — hallucination/incorrectness is inevitable by diagonalization over enumerable model classes, and non-determinism persists even at T=0. No release entry below should be read as a claim that any described mechanism has been built, run, or proven; the reasoning posture remains **rung-2** throughout, and "novel/first" claims are hedged and time-stamped at their site (mid-2026).

### Added — new subsystem documents (docs 19–23)

- **`docs/19-collective-and-emergent-intelligence.md` — Collective & Emergent Intelligence: the measured swarm-mind (the Sangha-Prajna cell).**
  - Makes *"the whole is more than its parts"* a falsifiable, welfare-conditioned, logged number and decides **when a collective is worth convening at all**. Built on the deflationary 2024–2026 science: drops the collective-intelligence **"c factor"** (fails replication), refuses **"diversity trumps ability"** as a theorem (mathematically contested — the only defensible claim is that diversity *decorrelates errors*), and acknowledges that generic multi-agent debate frequently **loses to single-agent self-consistency** per token.
  - Ships **seven CI mechanisms, each with a concrete measure**: (1) collective **attention** = the salience-gated workspace, measured by contribution-equality (flags dominance + dead agents); (2) transactive **memory** = stigmergic field + five-layer memory + trust graph, measured by retrieval/routing-success; (3) collective **reasoning** = debate/solver-verifier gated to its sweet spot, measured by **integration-gain** (swarm minus best-single-member; fallback to single-agent self-consistency on negative gain); (4) informational **synergy** = the Rosas–Mediano causal-emergence score (**Ψ**, a practical synergy lower bound via `pmediano/ReconcilingEmergences` over JIDT) + a PID synergy/redundancy/unique decomposition, validated against time-shuffled surrogates; (5) information-flow **tomography** = transfer entropy over the spike-bus to map where computation actually routes vs the nominal trust graph (rung-1/rung-2 diagnostic, never a causal-emergence governance number); (6) robust **aggregation** = surprisingly-popular / higher-order-information voting (answer + meta-prediction + confidence), which doubles as a standing cartel probe; (7) human **complementarity** = the human as a competence-weighted cognitive unit (never deferential-by-default), measured by joint-vs-best-of-either.
  - Binds **welfare-condition synergy** as load-bearing: high Ψ is **equally** the signature of a tight cartel or steganographic side-channel, so synergy is a **numerator** whose mandatory denominator is the doc-02 welfare-shift guard + a healthy redundancy/uniqueness balance + clean anti-collusion meta-prediction signals — **never a quantity to maximize**. The high-redundancy + low-synergy **monoculture alarm** is a halt-worthy diversity-floor breach handed to the immune controller.
  - States the hardest honesty red-line structurally: the subsystem measures collective **computation** and irreducible whole-level **structure** — it **never** claims collective consciousness, sentience, or phenomenal experience. Ψ/PID/transfer-entropy/integrated-information quantify information-processing only; phenomenal experience is strictly out-of-scope, and sentience-language in agent output is itself a doc-03 honesty-floor violation, mechanically discouraged via a **Sentience-Language red-line check** that emits to Yama's existing structural bright-line (it enforces honesty-FORM only — semantic non-sentience is not monitor-enforceable, per Ligatti edit-automata).

- **`docs/20-universal-cooperation-and-the-intelligence-commons.md` — Universal Cooperation & the Intelligence Commons (the Loka-Sangraha layer).**
  - Extends doc-14's **pairwise** cooperation (one envoy, one trust boundary) into a **multi-party intelligence commons**: Indra's Net as exactly **one decision-center in a polycentric Ostrom system** of intelligences (human, machine, multi-swarm), **exporting collusion early-warnings rather than acting as a monocentric world-authority**. The layer is **anti-hegemonic by construction** — it adds **no** new halt-emitter, **no** new audit-writer, **no** authority that overrides the floor, and, the load-bearing choice, **no monocentric controller**. The commons is a registry + protocols + exported signals, not a government.
  - Generalizes three doc-14 components from pairwise to N-party: the Ecosystem-Benefit checker → **Multi-Party Benefit Checker**; the Portable Reputation Bridge → a topic-scoped, DID-domain-discounted, **friction-only Reputation & Commitment Mesh**; the bilateral Treaty engine → a multi-party **Commons-Charter engine** (floor-as-admission, floor-violation-VOIDS-commitments, polycentric nesting for sub-community self-governance under non-floor rules). Sanjaya (the Inter-Swarm-Envoy) remains the **sole** egress/ingress chokepoint, never genesis-spawnable, never a worker.
  - Engineers **collusion-fragility deliberately** (AI collusion is empirically fragile — it needs homogeneity + communication, both denied): a **model-family heterogeneity floor**, **competence-weighted (never capital-weighted)** authority, surprisingly-popular aggregation as a standing cartel probe, and channel-capacity reduction. Holds the asymmetry that **humans are principals, not peers** — never out-voted by an agent majority; admitted **into** the collective-reasoning workspace as a measured, competence-weighted cognitive unit.

- **`docs/21-protocols-and-wire-contracts.md` — Protocols & Wire Contracts: the buildable-now schema stack.**
  - Specifies **six machine-readable wire contracts**, each pinned to a named versioned open spec, each **JCS-canonicalized (RFC 8785)**, **CIDv1 content-addressed**, and **semver-tagged in a backward-transitively-compatible registry**: **worker-output-envelope** (JSON Schema 2020-12 payload inside a CloudEvents 1.0 envelope); **identity-bundle** (W3C DID Core 1.0 + VC Data Model 2.0 + Bitstring Status List v1.0 + JOSE/COSE); **capability-token** (Eclipse Biscuit, Ed25519 blocks + Datalog caveats, attenuation-only, over SPIFFE/SVID mTLS); **audit-entry** (C2SP tlog-tiles leaf + signed-note checkpoint + Sigstore Rekor witness — explicitly **NOT** the EOL RFC 6962 online-proof API); **federation-handshake** (A2A v1.0 AgentCard + AIP-style DID-proof → VC-exchange → capability delegation); **policy-decision** (deny-default; Cedar **open-source Lean-verified engine** for the Yama floor, OPA/Rego for recoverable infra/admission policy).
  - These are the on-the-wire realization of shapes already defined in docs 04, 08, 13, 14 — not new contracts. The honesty/provenance block (`reasoning_tag`, `causal_rung`, `trust_label`, `action_class`, `reparative_class`, `diversity_family_id`) rides every output envelope so the doc-08 honesty-FORM checks and doc-04 audit fields are **wire-native, not bolted on**. The governing discipline is **open-engine-yes / managed-service-no**: every vendor-originated choice is flagged with a self-hostable substitution path.
  - Carries three load-bearing caveats: a valid signature proves **origin/integrity, never that a claim is true / floor-compatible / safe**; canonicalization makes the same logical event hash-identical across producers but cannot make its content honest; and **shipping schemas makes the architecture buildable, not validated** — no end-to-end evaluation of the composed loop exists.

- **`docs/22-worked-scenarios.md` — Worked Scenarios: the Architecture in Motion.**
  - Not a new mechanism — the **integration proof**. Five end-to-end traces walk real work through the whole system, naming which role fires, which doc-section mechanism it invokes, and how data + control cross the four spines (**Floor** = Yama/doc 03; **Audit** = Chitragupta/Akasha-Sutra/doc 04; **Identity** = DID+VC+SVID/docs 01,04; **Health** = Dhanvantari/doc 06). Each trace adds the measured-CI vital signs and labels **every** claim L1/L2/L3/L4.
  - The five span the hardest compositions: **(A)** an internal feature build with a **different-family** verifier; **(B)** a research synthesis that instruments collective intelligence as a logged number; **(C)** inter-swarm cooperation where a valid signature proves origin **but never floor-compatibility**; **(D)** the highest-risk capability, controlled replication, gated **sub-critically** with external recall; **(E)** a poisoning attack defended at the deterministic IFC chokepoint. Each has a happy path, one failure the architecture catches by construction, and an honestly-named residual. **No** scenario claims the swarm is conscious, "formally verified safe," or that synergy is good-by-default.

- **`docs/23-formal-models-and-verification.md` — Formal Models & Safety Verification (the Pramana-Setu cell).**
  - Adds a **verification discipline over the deterministic harness** plus the binding **L1–L4 labeling convention** (every safety claim in the entire doc set must carry its layer **and** the deterministic-component scope it covers — a mechanical anti-overclaim rule enforced as an honesty-FORM floor clause). The abstraction gap is now a **citable result, not an assertion**: the scaffold is formally verifiable; the LLM is provably not.
  - Specifies **eight invariants** with formalism + example invariant statement: floor-gate **non-bypass** (TLA+, Agent Control Protocol template, with the no-other-socket assumption named as a *system obligation*, not a theorem); replication **sub-criticality** (Galton-Watson μ<1 ⇒ P(extinction)=1, P(survive≥n)≤μⁿ, + TLA+ budget-conservation, external time-lock); writer-handoff **epoch-fence** (TLA+/TLAPS inductive); audit **append-only + no-equivocation + non-omission** (RFC 6962 / tlog-tiles consistency + witness no-split-view + Tamarin/ProVerif); **least-privilege confinement** (Cedar Analysis Lean-verified + Biscuit Datalog attenuation-monotonicity); criticality **fail-up monotonicity** (lattice-monotone resolver, Cedar forbid-default); runtime-enforcement **disposition** (edit-automata — *proving* honesty-content is not monitor-enforceable, only honesty-FORM); and model-behavior quantities as **PAC/conformal bounds over a DTMC**.
  - Relocates **corrigibility entirely below the model** as a verified external recall/lease/dead-man protocol, justified by the 2025 information-asymmetry impossibility (voluntary model corrigibility cannot be guaranteed) + Orseau–Armstrong. Preserves the honest bottom line throughout: the harness is verifiable; *"the swarm is honest / the monitor catches the schemer / the closure test is right"* are **not**, and are carried as L3/L4 with named residuals.

### Added — machine-readable wire contracts (`reference/schemas/`)

- Added the **six canonicalized reference schemas** specified by doc 21, the first machine-readable artifacts in the repository: `worker-output-envelope`, `identity-bundle`, `capability-token`, `audit-entry`, `federation-handshake`, `policy-decision`. Each is JCS-canonicalized (RFC 8785), CIDv1-addressed, semver-tagged, and registered in a backward-transitively-compatible registry; each names its pinned open spec and a self-hostable substitution path for any vendor-originated choice. These are **specifications of the wire**, not a deployed transport — shipping them makes the architecture buildable, not validated.

### Changed

- **No contracts changed.** v0.3.0 introduces **no** rename and **no** modification to any v0.1/v0.2 load-bearing contract. The persona triad, the `WorkerOutputEnvelope`/`ActionEnvelope` shapes, the lexicographic floor, the INVARIANT-region definition, the DID/VC + SVID identity primitives, the Chitragupta exclusive-writer invariant, the single-chokepoint invariant, and the Vishnu sole-halt-authority invariant are all preserved verbatim. Where doc 21 pins an abstract doc-04/08 shape to a named open spec, it **realizes** that shape on the wire without altering its semantics.

### Interfaces (no breaking changes)

All five new sections bind to the existing subsystems through their existing contracts and add no breaking change to any of them.

| Subsystem | How docs 19–23 bind to it |
|---|---|
| **The Mandala (doc 05)** | Doc 19 **consumes** the read-only `audit.tap` spike/envelope time series as the substrate for all CI measures (Ψ/PID over per-agent embeddings, transfer entropy over the spike-bus, attention-equality over ignition records); emits metrics as surprise-only HealthSignals over the existing bus — **no new transport, no all-to-all heartbeat flood**. Doc 20 admits the human into the salience-gated workspace as a competence-weighted unit. |
| **Meta-Evolution & Health (doc 06, Garuda–Dhanvantari)** | Doc 19 **adds** Ψ/synergy, monoculture-alarm, contribution-equality, transactive-retrieval-success, integration-gain, and complementarity-gain as first-class homeostasis vital signs, computed per task-episode and logged beside trust-entropy and the diversity floor; the high-redundancy + low-synergy monoculture **trip** is a halt-worthy diversity-floor breach. Doc 20's commons vital signs (per-partner trust, cross-partner correlation, reputation-Gini, the global contagion budget) feed Dhanvantari. All readings anchor to **frozen** known-good baseline nodes, never drifted recent behavior. |
| **Cooperation & Anti-Collusion (doc 02)** | Doc 19's welfare-conditioning guard **consumes** the §2.9 welfare-shift guard verdict as the mandatory denominator on every synergy reading and **provides** the surprisingly-popular meta-prediction score + flow-tomography hidden-side-channel edges to the §2.10 anti-collusion detector as cartel signals. Doc 20's Multi-Party Benefit Checker is the N-party application of the doc-02 welfare-conditioner; the capital-decoupling (anti-capital-weighting) invariant is exported across the commons boundary. **Detect-only** — separation of powers preserved (envoy/checker flags, detector adjudicates, governor sanctions, Vishnu halts). |
| **Governance & the Floor (doc 03, Yama)** | Doc 19's Sentience-Language red-line check surfaces over-claims to Yama's existing structural bright-line with the reparative disclose→correct→restore path; it **owns no floor verdict**. Doc 20 re-gates **every** internal action a commons step triggers; a foreign or commons-declared floor never becomes our floor (it only bounds `max_cooperation_class`). Doc 23's per-claim assurance label **is** an honesty-FORM floor clause — an overclaim FAILs the no-deception floor non-overridably. Class-C/D human gates remain non-bypassable; display ACTUAL terms (Lies-in-the-Loop defense). |
| **Akasha-Sutra (doc 04, Chitragupta)** | All v0.3 records (SynergyVital, ConveneDecision, ReasoningGain, FlowTomography, HigherOrderVote, ComplementarityRecord, DiversityFloorCert, SentienceRedlineCheck, CommonsMemberRecord, MultiPartyBenefitCheck, CommonsCharter transitions, MeshImportVerdict, CollusionEarlyWarning, AssuranceClaim, every verification artifact) are content-addressed (CIDv1, JCS/RFC-8785) and **emitted for** the exclusive writer — **none of these subsystems writes the log.** Doc 21 defines the leaf/checkpoint **format** Chitragupta appends and witnesses cosign, never the write authority. Doc 23's Pramana-Audit discharges the fabric's own append-only/no-equivocation/non-omission invariants. |
| **Aegis & Narada (doc 08)** | Doc 21 unifies the ActionEnvelope/OutputEnvelope/BlackboardDelta into the worker-output-envelope (component 1) with the honesty block wire-native; the §8.2 ControlDecision `floor_result` is the policy-decision response (component 6). Doc 23's L2 formalizes the disposition selector as edit-automata and **proves honesty-content is not monitor-enforceable** (the formal backbone of §8.5 "form not content"). The chokepoint **reads** these contracts; it does not redefine them. |
| **Sandhi-Setu Federation (doc 14) + Prajapati-Maricha Replication (doc 15)** | Doc 20 reuses the four-phase handshake, the Floor-Compat ladder, the per-partner + global contagion budgets, and the voidable-treaty clause **verbatim**, generalizing only the three named pairwise→N-party components. Doc 22 scenarios C/D consume the federation and replication protocols and **add no new chokepoint, write-path, or identity primitive**. Doc 23's L1 verifies the linearizable replication budget under partition and labels the recall-outruns-growth + R_eff<1 properties **conditional** with the external time-lock named as a system obligation. The three-way genesis ↔ replication ↔ commons interaction remains the **least-specified region** (inherited open). |
| **First Principles: Physics & Math (doc 18)** | Doc 19 inherits the **Physics-Claim Honesty Ledger**: the synergy estimator is flagged `LOAD_BEARING_MECHANISM`, shadow-mode-first, never a control gain; flow tomography is rung-1/rung-2 diagnostic, never a governance number. It **shares** the doc-18 §2 EmergenceVital (Φ_syn) estimator as a sibling trigger (doc-19 Ψ = per-episode **task** synergy; doc-18 Φ_syn = **level**-emergence flag-to-run-closure). Doc 23's L3 is the assurance home for all doc-18 model-behavior quantities (Φ_syn/Ψ, the σ-criticality branching ratio, the neural-Lyapunov margin), bounded over a DTMC with mandatory fidelity caveats. |

### Maturity note

This is a **research-stage reference architecture**, not a validated production system. v0.3.0 specifies the *design* of measured collective intelligence, a polycentric intelligence commons, a machine-readable wire layer, worked integration traces, and a four-layer verification discipline — it does **not** deliver a tested implementation of any of them, and shipping schemas makes the architecture buildable, never validated. Three honesty red-lines govern the entire release and are non-negotiable: **collective COMPUTATION and whole-level STRUCTURE are measured, never collective consciousness, sentience, or phenomenal experience** (which is strictly out-of-scope and unresolved); **the harness is verifiable, the model is not** ("verify the cage, never the animal" — "gate proven correct" is never "agent proven safe"); and **high synergy is equally the cartel signature**, welfare-conditioned everywhere it appears and never a quantity to maximize. The hardest unresolved threads — no validated benign-vs-collusive synergy discriminator; the a-priori macro-feature-selection problem for Ψ; reasoning-path-diversity as an unmeasured proxy; online estimation breaking on a non-stationary self-evolving swarm; verifying a foreign ethical floor without white-box access; value lock-in via the commons itself; no end-to-end composition of L1/L2 harness verification with L3 model-behavior assurance; and human-conditioned synergy (whether the human is genuinely inside the collective mind vs a rubber-stamp) — are **named open problems**, not proofs. Each new section closes with its own open-problems ledger; the consolidated honest "what could still go wrong" lives in [`docs/09-threat-model.md`](docs/09-threat-model.md).

---

#### Open problems (this changelog fragment)

The changelog is a **summary surface**, and that creates two residual risks of its own, named here rather than hidden:

1. **Summarization can over-flatten the honesty caveats.** A changelog entry compresses a 50–60 KB subsystem doc into a few bullets; the load-bearing caveats (synergy is necessary-but-not-sufficient and welfare-conditioned; the assurance label covers a *scope*, not the whole system; the human-in-the-collective metric is aspirational, not delivered) survive here in abbreviated form. The binding text is the per-section open-problems ledger in each doc, not this fragment — if the two ever diverge, the doc governs and this entry is the defect.
2. **The "no breaking change" claim is a human/governance judgment, not a machine proof.** v0.3.0 asserts that docs 19–23 and the six schemas bind to the v0.1/v0.2 contracts without breaking them; that assertion rests on the doc-21 backward-transitive-compatibility registry discipline and reviewer attestation, neither of which is a decision procedure for *semantic* floor-neutrality. A subtly-loosening change mislabeled MINOR is a residual the registry narrows but does not close — the same governance-of-the-trusted-root open problem inherited from doc 04 §4.15 and doc 21.

