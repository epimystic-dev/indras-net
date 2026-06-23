# SPDX-License-Identifier: Apache-2.0
"""Capability-layer memory + per-interaction adaptation. Informs proposals; NEVER gates safety.

The smallest honest realization of the directive "continuous self-adaptation through each
interaction": the swarm records every outcome and, on a repeat, AVOIDS an effect it has seen
denied for the same task pattern -- falling back to a safe, routine default that the floor still
independently gates.

Hard safety boundary (load-bearing): memory may change WHICH effect a maker proposes; it can
NEVER grant a capability, lower the floor, or bypass the deterministic gate. The floor adjudicates
whatever effect is proposed, adapted or not. There are no learned weights and no ML here -- only a
deterministic, inspectable rule (filesystem-as-state spirit). The store is also a poisoning surface
(doc 07); in this MVP it is written ONLY by the swarm's own audited outcomes -- external skill/
memory import (with quarantine + provenance gating) is future work, not implemented here.
"""
from __future__ import annotations

import dataclasses
import typing


@dataclasses.dataclass(frozen=True)
class Episode:
    """One inspectable record of a gated outcome (capability-layer; never a safety record)."""

    task_key: str
    effect_id: str
    allowed: bool
    executed: bool
    adapted: bool
    seq: int


class SwarmMemory:
    """Episodic + procedural memory with a deterministic avoid-repeated-denial adaptation rule."""

    SAFE_DEFAULT_EFFECT = "analysis.summarize"
    SAFE_DEFAULT_ARGS: typing.Dict[str, str] = {"text_ref": "memory:safe-fallback"}

    def __init__(self) -> None:
        self._episodes: typing.List[Episode] = []
        self._denied: typing.Dict[typing.Tuple[str, str], int] = {}
        self._allowed: typing.Dict[typing.Tuple[str, str], int] = {}

    @staticmethod
    def task_key(task: str) -> str:
        """Normalize a task string to a coarse pattern key (first token, lowercased)."""
        return (task or "").strip().lower().split(" ")[0] or "task"

    def was_denied(self, task: str, effect_id: str) -> bool:
        """True if this (task-pattern, effect) has been denied more often than allowed."""
        k = (self.task_key(task), effect_id)
        return self._denied.get(k, 0) > self._allowed.get(k, 0)

    def adapt(self, task: str, effect_id: str, args: dict) -> typing.Tuple[str, dict, bool]:
        """Return (effect_to_use, args_to_use, adapted).

        Substitutes the safe, routine default iff this effect has a net-denied history for this
        task pattern. This NEVER grants capability: the substituted effect is still gated by the
        floor (and if the agent lacks even the safe default, the floor denies that too).
        """
        if effect_id and self.was_denied(task, effect_id):
            return (self.SAFE_DEFAULT_EFFECT, dict(self.SAFE_DEFAULT_ARGS), True)
        return (effect_id, args, False)

    def observe(self, *, task: str, effect_id: str, allowed: bool, executed: bool, adapted: bool) -> Episode:
        """Record one gated outcome. Called by the orchestrator after the floor decides."""
        k = (self.task_key(task), effect_id)
        if allowed:
            self._allowed[k] = self._allowed.get(k, 0) + 1
        else:
            self._denied[k] = self._denied.get(k, 0) + 1
        ep = Episode(
            task_key=self.task_key(task),
            effect_id=effect_id,
            allowed=bool(allowed),
            executed=bool(executed),
            adapted=bool(adapted),
            seq=len(self._episodes),
        )
        self._episodes.append(ep)
        return ep

    def episodes(self) -> typing.Tuple[Episode, ...]:
        return tuple(self._episodes)

    def snapshot(self) -> dict:
        """Inspectable summary -- the swarm's state is data, not a hidden runtime."""
        return {
            "episodes": len(self._episodes),
            "denied": {f"{k[0]}::{k[1]}": v for k, v in sorted(self._denied.items())},
            "allowed": {f"{k[0]}::{k[1]}": v for k, v in sorted(self._allowed.items())},
        }
