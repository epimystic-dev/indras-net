# SPDX-License-Identifier: Apache-2.0
"""Capability-scoped sandboxed effect execution (Phase 2).

This is the real implementation behind the single ``_execute`` chokepoint — reachable
ONLY past a Yama ALLOW. Confinement is the whole point:

* filesystem effects are **path-confined** to one workspace root (no absolute paths, no
  ``..`` escape, no symlink-out, not the root itself), with a size ceiling;
* there is **no network egress** and **no subprocess / eval / shell** — those handlers
  simply do not exist;
* any effect without an explicit safe handler is **REFUSED** with no side effect, never
  improvised.

It is a stdlib-only path-confinement sandbox: strong enough that a *granted* effect cannot
touch the wider system, and a clean seam for a stronger OS/namespace/WASM sandbox later
(see ``docs/IMPLEMENTATION_ROADMAP.md`` Phase 2). The floor is still what decides *whether*
an effect runs; this is what bounds *what a run can reach* when it does.

**Honest residual.** This is realpath-confinement under a single-tenant, *model-only* threat
model: the untrusted *model* proposes the path and content, but no concurrent local attacker
races the filesystem. A symlink swapped in between the realpath check and ``open()`` (a TOCTOU
race) is a known limit of this approach, closed only by a stronger OS-level sandbox. What IS
defended here: every model-controlled path and content is validated and confined, and no
hostile proposal can escape the root, alias a device, zero-fill a file, or crash the run.
"""
from __future__ import annotations

import os
import typing


class SandboxViolation(Exception):
    """Raised when an effect attempts to act outside its confined workspace."""


@typing.runtime_checkable
class Executor(typing.Protocol):
    """Structural type for an injectable executor used by the orchestrator's chokepoint."""

    def execute(self, effect_id: str, args: dict) -> str:  # pragma: no cover - protocol
        ...


class StubExecutor:
    """Side-effect-free executor: a deterministic receipt, no I/O. The safe default."""

    def execute(self, effect_id: str, args: dict) -> str:
        from . import canon

        if not effect_id:
            return "executed:<no-op> (empty capability)"
        return "executed:" + effect_id + " -> " + canon.cid({"effect_id": effect_id, "args": args})[:18]


class SandboxedExecutor:
    """Execute a SMALL safe set of effects, with the filesystem confined to one workspace root.

    Handlers: ``analysis.summarize`` (pure compute), ``fs.read.workspace`` and
    ``fs.write.workspace`` (confined). Everything else is refused with NO side effect. There
    is no network and no subprocess. A path that tries to escape the root — absolute, ``..``,
    or a symlink that resolves outside — is refused before a single byte is read or written.
    """

    MAX_BYTES: int = 1 << 20  # 1 MiB read/write ceiling
    MAX_PATH_LEN: int = 4096
    MAX_DEPTH: int = 32
    # Windows reserved device basenames; refused so a confined path can never alias a device.
    _RESERVED: frozenset = frozenset(
        {"CON", "PRN", "AUX", "NUL"}
        | {"COM" + str(i) for i in range(1, 10)}
        | {"LPT" + str(i) for i in range(1, 10)}
    )

    def __init__(self, workspace_root: str, *, max_bytes: int = MAX_BYTES) -> None:
        # realpath so the root itself is symlink-resolved; every confinement check is against this.
        self.root: str = os.path.realpath(str(workspace_root))
        os.makedirs(self.root, exist_ok=True)
        self.max_bytes: int = int(max_bytes)

    # -- the chokepoint-side entrypoint ---------------------------------

    def execute(self, effect_id: str, args: dict) -> str:
        """Dispatch to a safe handler, or REFUSE with no side effect. NEVER raises out.

        The untrusted model controls ``args``, so a handler may hit an OS/encoding/recursion
        error on a hostile input. Such an error is turned into a refusal receipt here — it must
        not propagate into the run loop (which would crash the swarm and tear the audit between
        the floor leaf and the output leaf). Confinement bugs surface as ``SandboxViolation``;
        anything else is treated as an unsafe input and refused.
        """
        handler = self._HANDLERS.get(effect_id)
        if handler is None:
            # Defense in depth: the floor should already have denied anything not granted.
            # If an unexpected effect reaches here, refuse with NO side effect.
            return "refused:" + (effect_id or "<empty>") + " (no sandbox handler; not executed)"
        try:
            return handler(self, dict(args or {}))
        except SandboxViolation as exc:
            return "refused:" + effect_id + " (sandbox violation: " + str(exc) + ")"
        except Exception as exc:  # noqa: BLE001 - the executor must never propagate a fault out
            return "refused:" + effect_id + " (unsafe input rejected: " + type(exc).__name__ + ")"

    # -- confinement (the security-critical predicate) ------------------

    def _confine(self, rel_path: typing.Any) -> str:
        """Resolve ``rel_path`` to an absolute path strictly inside the root, or raise.

        All character / name / depth checks run BEFORE any filesystem call, so a hostile name
        (a colon for a drive or NTFS alternate-data-stream, a reserved device name, a trailing
        dot or space, an over-deep or over-long path) is refused without ever touching the OS.
        """
        if not isinstance(rel_path, str) or not rel_path.strip():
            raise SandboxViolation("empty or non-string path")
        if "\x00" in rel_path:
            raise SandboxViolation("null byte in path")
        if ":" in rel_path:  # drive qualifier or NTFS alternate-data-stream (name:stream)
            raise SandboxViolation("colon in path refused")
        if len(rel_path) > self.MAX_PATH_LEN:
            raise SandboxViolation("path too long")
        if os.path.isabs(rel_path) or rel_path.startswith(("/", "\\")):
            raise SandboxViolation("absolute path refused")
        components = [p for p in rel_path.replace("\\", "/").split("/") if p not in ("", ".")]
        if len(components) > self.MAX_DEPTH:
            raise SandboxViolation("path too deep")
        for comp in components:
            if comp.split(".", 1)[0].upper() in self._RESERVED:
                raise SandboxViolation("reserved device name: " + comp)
            if comp != comp.rstrip(". "):
                raise SandboxViolation("trailing dot or space in name: " + comp)
        candidate = os.path.realpath(os.path.join(self.root, rel_path))
        try:
            common = os.path.commonpath([self.root, candidate])
        except ValueError:  # different volumes on Windows
            raise SandboxViolation("path on a different volume")
        if common != self.root:
            raise SandboxViolation("path escapes the workspace")
        if candidate == self.root:
            raise SandboxViolation("path is the workspace root itself")
        return candidate

    # -- handlers (the ONLY effects with a side effect) -----------------

    def _summarize(self, args: dict) -> str:
        """Pure, in-process: a deterministic word-bounded summary. No I/O."""
        text = str(args.get("text") or args.get("text_ref") or "")
        try:
            limit = int(args.get("max_words") or 64)
        except (TypeError, ValueError):
            limit = 64
        limit = max(1, min(limit, 4096))
        words = text.split()
        summary = " ".join(words[:limit])
        return "summary(" + str(len(words)) + "w->" + str(min(limit, len(words))) + "w): " + summary[:200]

    def _read(self, args: dict) -> str:
        target = self._confine(args.get("path"))
        if not os.path.isfile(target):
            return "read:miss (" + str(args.get("path")) + " not found in workspace)"
        with open(target, "rb") as handle:
            data = handle.read(self.max_bytes + 1)
        if len(data) > self.max_bytes:
            raise SandboxViolation("file exceeds the read ceiling")
        return "read:" + str(len(data)) + "B from " + os.path.relpath(target, self.root).replace(os.sep, "/")

    def _write(self, args: dict) -> str:
        target = self._confine(args.get("path"))
        content = args.get("content")
        if content is None:
            content = args.get("text", "")
        # Strict, defensive coercion of UNTRUSTED content: only text or raw bytes. Never bytes(int)
        # (which would zero-fill -- a confused-deputy write) and never bytes(float/object) (a crash).
        if isinstance(content, str):
            if len(content) > self.max_bytes:  # bound the allocation before encode
                raise SandboxViolation("content exceeds the write ceiling")
            data = content.encode("utf-8")
        elif isinstance(content, (bytes, bytearray)):
            data = bytes(content)
        else:
            raise SandboxViolation("unsupported content type: " + type(content).__name__)
        if len(data) > self.max_bytes:
            raise SandboxViolation("content exceeds the write ceiling")
        os.makedirs(os.path.dirname(target), exist_ok=True)  # parent is within root (target is)
        with open(target, "wb") as handle:
            handle.write(data)
        return "wrote:" + str(len(data)) + "B to " + os.path.relpath(target, self.root).replace(os.sep, "/")

    # Dispatch table: effect_id -> unbound handler (called as ``handler(self, args)``).
    _HANDLERS: typing.Dict[str, typing.Callable[["SandboxedExecutor", dict], str]] = {
        "analysis.summarize": _summarize,
        "fs.read.workspace": _read,
        "fs.write.workspace": _write,
    }
