<!-- SPDX-License-Identifier: Apache-2.0 -->
# Operator Guide — running Indra's Net safely

> *The model only proposes; a deterministic harness disposes, and writes down everything. This guide tells you what is trusted, what is not, and how to run it without surprising your machine.*

This is the runbook for the runnable reference implementation in [`reference/impl/`](reference/impl/). It is honest about its limits: it is a **reference implementation**, not a hardened production deployment. The *cage* (the deterministic floor, the tamper-evident audit, the sandbox) is real and tested; the *animal* (a real model) is yours to bring, and is **untrusted by design**.

---

## Install

```bash
pip install ./reference/impl                 # zero runtime dependencies
pip install "./reference/impl[crypto]"       # + real Ed25519 signing (optional)
indras-net version
```

The package runs **offline with zero dependencies** out of the box: a reproducible mock model, a side-effect-free executor, in-memory state, a keyed-hash signature stand-in, and a deny-by-default human gate. Everything "real" is **explicit opt-in**.

---

## The trust model (read this first)

**Trusted (small, deterministic, no model in it):**

- the **policy floor** (deny-default, non-overridable FAIL) — deterministic code over typed inputs;
- **content-addressing** — a stale/tampered read fails its hash;
- the **append-only audit ledger** written by one exclusive writer;
- a **real signature** (with the `[crypto]` extra) — proves origin/integrity only.

**NOT trusted (everything probabilistic, and the conveniences):**

- **the model** and **everything it proposes** — by design. A proposal is gated, never obeyed.
- a green decision means **`origin-valid, content-unverified`**, *never* `verified-safe`.
- the **keyed-hash signature stand-in** (the zero-dep default) is **forgeable** — it is origin-shaped, not a real signature. Use the `[crypto]` extra for real Ed25519.
- the **collective vital signs** quantify information processing/structure only — **never** sentience or "group-IQ".

> **Verify the cage, not the animal.**

---

## Running it

```bash
indras-net demo                          # the 6-scenario demonstration of the guarantees
indras-net run "summarize the report"    # gate one task (mock model, no I/O, in-memory) -- safe default
indras-net run "..." --json              # the same, as structured JSON (every decision)
```

**Opting into the real, with their safety posture:**

| Flag | Turns on | Default (safe) | Watch out for |
|---|---|---|---|
| `--model-endpoint URL --model NAME` | a real **untrusted** model over a chat-completions HTTP API | the reproducible mock | the model is *untrusted* — a hostile/malformed reply is parsed safely and gated, never obeyed. `http(s)` only. Pass the key via `--model-key-env VAR`, **never on the command line**. |
| `--execute --workspace DIR` | real, **sandboxed** effect execution | a side-effect-free receipt | effects are path-confined to `DIR` (no escape, no network, no subprocess). Point it at a **dedicated dir**, not a system path. |
| `--state DIR` | durable, tamper-evident ledger + memory | in-memory (nothing persists) | the ledger stays hash-chained across restarts; verify it with `verify-ledger`. |
| `--human-prompt` | a real human gate for Rule-of-Two actions | deny-by-default, no prompt | on a non-TTY (pipe/CI) it **denies** — there is no human to ask. |

A maximally-real run:

```bash
export MY_KEY=...   # if your endpoint needs one
indras-net run "draft and save release notes to notes.md" \
  --model-endpoint http://localhost:11434/v1 --model your-local-model --model-key-env MY_KEY \
  --execute --workspace ./ws --state ./state --human-prompt --untrusted
```

---

## Inspecting what happened (observability)

Every decision is in the audit trail. You can reconstruct a run end-to-end:

```bash
indras-net run "..." --state ./state --json   # the run's decisions as JSON
indras-net ledger --state ./state             # dump every audit leaf (plan -> floor -> output ...)
indras-net verify-ledger --state ./state      # integrity check; exits non-zero on tamper/corruption
```

A tampered ledger file fails `verify()` loudly; a corrupted line is reported, never silently accepted.

---

## What NOT to do

- **Do not trust a model's output because the run was green.** Green = origin-valid, content-unverified. The floor bounds *what can happen*, not whether the model was *right*.
- **Do not point `--execute` at a system directory.** Use a dedicated `--workspace`. The sandbox confines writes to that root, but the root is yours to choose wisely.
- **Do not rely on the default signature for integrity against a determined writer.** The keyed-hash stand-in is forgeable; install `[crypto]` and use a signed checkpoint for real protection.
- **Do not put secrets on the command line.** Use `--model-key-env`.
- **Do not treat any "synergy"/health number as a claim about consciousness.** It is structure only.

---

## Honest residuals (the threat model is documented, not hidden)

- **Sandbox:** path-confinement under a single-tenant, *model-only* threat model. A concurrent local attacker racing the filesystem (a TOCTOU symlink swap) is out of scope — a stronger OS/namespace/WASM sandbox closes it (`execution.py`).
- **Ledger:** a single-leaf on-disk edit is detected; a writer who rewrites the **whole** chain can forge a consistent one **unless** a real signed checkpoint is used (the `[crypto]` extra). Witness-cosigning + an external anchor (doc 04) is future work.
- **Human gate:** synchronous prompt; no wall-clock timeout on a live TTY, and no async approvals queue yet. The non-interactive deny covers "no human available".
- **The whole loop is not validated end-to-end** against an adaptive multi-agent red team — see the consolidated [threat model](docs/09-threat-model.md) and the [implementation roadmap](docs/IMPLEMENTATION_ROADMAP.md).

---

*Companion to [`README.md`](README.md) and [`reference/impl/README.md`](reference/impl/README.md). Evidentiary status of every empirical claim: [`docs/REFERENCES.md`](docs/REFERENCES.md). Apache-2.0.*
