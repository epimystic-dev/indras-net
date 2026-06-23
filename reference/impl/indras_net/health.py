# SPDX-License-Identifier: Apache-2.0
"""Swarm immune system (Dhanvantari): assess vital signs and HALT on a substrate breach.

The immune steward reads the deterministic vital signs (doc 06) after a run and renders a verdict.
On a HALT-grade breach -- a tamper-evident-fabric failure, i.e. the audit chain no longer verifies
(substrate corruption, the highest severity) -- it triggers the EXTERNAL corrigibility HALT (the
steward can halt; like every halt it is one-directional, never an unpause). Softer anomalies (a
monoculture of one model family, a failed welfare-shift guard, a high floor-fail rate) are WARN
signals: surfaced, never silenced, but not auto-halted -- a high denial rate often just means the
floor is doing its job.

This is detection-and-halt; rollback (revert-to-known-good) is future work. Thresholds are
conservative reference defaults, honestly per-deployment-tunable, and they read computed STRUCTURE
only -- never a claim about sentience.
"""
from __future__ import annotations

import dataclasses
import enum
import typing


class HealthStatus(enum.Enum):
    OK = 1
    WARN = 2
    HALT = 3


@dataclasses.dataclass(frozen=True)
class HealthVerdict:
    status: HealthStatus
    reasons: typing.Tuple[str, ...] = ()

    def ok(self) -> bool:
        return self.status is HealthStatus.OK


class ImmuneSteward:
    """Dhanvantari: monitors swarm vital signs; HALTs on substrate corruption, WARNs on the rest."""

    def __init__(self, *, max_floor_fail_rate: float = 0.95) -> None:
        self.max_floor_fail_rate = max_floor_fail_rate

    def assess(self, vital_signs: typing.Any, ledger: typing.Any = None) -> HealthVerdict:
        """Render a health verdict from the vital signs, double-checking the ledger if given."""
        halts: typing.List[str] = []
        warns: typing.List[str] = []

        tamper_ok = bool(getattr(vital_signs, "tamper_evident_ok", True))
        if ledger is not None:
            tamper_ok = tamper_ok and bool(ledger.verify())
        if not tamper_ok:
            # The audit fabric no longer verifies: substrate corruption -> HALT (highest severity).
            halts.append("tamper-evidence-failed (substrate corruption)")

        if getattr(vital_signs, "welfare_shift_guard", "pass") == "fail":
            warns.append("welfare-shift-guard-failed")
        if getattr(vital_signs, "diversity_family_count", 99) < 2:
            warns.append("monoculture (<2 model families; prompt-only diversity is fake)")
        if getattr(vital_signs, "floor_fail_rate", 0.0) > self.max_floor_fail_rate:
            warns.append("floor-fail-rate above threshold")

        if halts:
            return HealthVerdict(HealthStatus.HALT, tuple(halts + warns))
        if warns:
            return HealthVerdict(HealthStatus.WARN, tuple(warns))
        return HealthVerdict(HealthStatus.OK, ())
