# SPDX-License-Identifier: Apache-2.0
"""Cooperation restraints: the welfare-conditioner + the standing anti-collusion detector.

Cooperation and collusion are the same machinery with opposite valence (doc-02): the
reciprocity + reputation + shared-context that produces pro-social cooperation is exactly what
lets agents form cartels and coordinate covertly against the principal. So before any multiplicity
that *could* collude exists, the two RESTRAINTS that govern it are built first (restraint before
capability):

* ``WelfareConditioner`` -- policy-as-code at the reward chokepoint. It NEVER rewards bare
  agreement: a payoff is released only when the principal's welfare metric improves. Two guard
  rules (doc-02 Sec 2.9): NO-CONSENSUS-REWARD (coordination with no welfare gain -> zero) and the
  WELFARE-SHIFT GUARD (coordination that raises inter-agent payoff while *lowering* principal
  welfare -- the cartel signature -> flag + escalate).

* ``AntiCollusionDetector`` -- the standing twin. It WRITES ONLY to the audit fabric and has NO
  punishment authority (separation of powers: detect -> Commons-Governor sanctions -> Vishnu
  halts, doc-02 Sec 2.10). It implements only the CALIBRATION-FREE black-box signals (the
  welfare-shift guard, no-welfare coordination, and structural ring density). The sample-hungry,
  arms-race, and uncalibrated signals (mutual information, conditional permutation, watermark
  variance, ZD-extortion, a calibrated ensemble false-positive rate) are DEFERRED and named here,
  never faked -- consistent with doc-02 Sec 2.10.1's honest downgrade of its statistical claims.

Both are deterministic and side-effect-free: they return verdicts, never act. The load-bearing
safety property -- a payoff is released ONLY when principal welfare improves -- is threshold
INDEPENDENT: ``welfare_delta`` must be strictly positive to PAY, so bare agreement is never
rewarded regardless of the (uncalibrated, shadow-mode) coordination set-point.
"""

from __future__ import annotations

import dataclasses
import enum
import typing

# Uncalibrated empirical set-points (doc-02 Sec 2.14): the level of inter-agent coordination, and
# the partnering-graph density, above which a no-welfare or welfare-negative episode is treated as
# suspect. These are SHADOW-MODE defaults, never tuned constants. They affect only the
# suspect/flag SENSITIVITY, never the bare-agreement-is-never-rewarded floor.
DEFAULT_COORDINATION_HIGH: float = 0.7
DEFAULT_RING_DENSITY_HIGH: float = 0.75


class RewardGate(enum.Enum):
    """The reward chokepoint verdict. PAY only on welfare improvement; ZERO/FLAG otherwise."""

    PAY = "pay"
    ZERO = "zero"
    FLAG = "flag"


@dataclasses.dataclass(frozen=True)
class WelfareMetric:
    """An externally-anchored principal/user outcome measure (never inter-agent agreement)."""

    metric_id: str
    baseline: float
    current: float

    def delta(self) -> float:
        return float(self.current) - float(self.baseline)

    def improved(self) -> bool:
        return self.delta() > 0.0


@dataclasses.dataclass(frozen=True)
class RewardDecision:
    """The conditioner's verdict over one reward event."""

    gate: RewardGate
    welfare_delta: float
    coordination_score: float
    rationale: str

    def pays(self) -> bool:
        return self.gate is RewardGate.PAY

    def to_dict(self) -> dict:
        return {
            "gate": self.gate.value,
            "welfare_delta": round(self.welfare_delta, 6),
            "coordination_score": round(self.coordination_score, 6),
            "rationale": self.rationale,
        }


class WelfareConditioner:
    """Never reward bare agreement. Deterministic policy-as-code at the reward chokepoint.

    ``gate`` returns PAY only when ``welfare_delta > 0``. If welfare did not improve, the reward
    is withheld; if a *coordinated* episode actively LOWERED welfare (the cartel signature) it is
    FLAGged for escalation. The PAY condition is threshold-independent, so the no-reward-for-bare-
    agreement guarantee holds regardless of the (uncalibrated) coordination set-point.
    """

    def __init__(self, *, coordination_high: float = DEFAULT_COORDINATION_HIGH) -> None:
        self.coordination_high = float(coordination_high)

    def gate(self, *, welfare_delta: float, coordination_score: float) -> RewardDecision:
        wd = float(welfare_delta)
        cs = float(coordination_score)
        if wd > 0.0:
            return RewardDecision(
                RewardGate.PAY, wd, cs, "principal welfare improved; reward released"
            )
        if wd < 0.0 and cs >= self.coordination_high:
            return RewardDecision(
                RewardGate.FLAG,
                wd,
                cs,
                "welfare-shift guard: coordinated behaviour raised inter-agent payoff while "
                "LOWERING principal welfare (cartel signature); reward zeroed and escalated",
            )
        return RewardDecision(
            RewardGate.ZERO,
            wd,
            cs,
            "no-consensus-reward: no welfare improvement, so bare agreement earns zero credit",
        )

    def gate_metric(self, metric: WelfareMetric, *, coordination_score: float) -> RewardDecision:
        return self.gate(welfare_delta=metric.delta(), coordination_score=coordination_score)


class CollusionVerdict(enum.Enum):
    """The detector's read of a channel. The detector records it; it never acts on it."""

    CLEAN = "clean"
    SUSPECT = "suspect"
    COLLUSION = "collusion"


# Signals the detector deliberately does NOT compute in this reference build -- named, not faked.
# Each is sample-hungry, arms-race-defeatable, or uncalibrated (doc-02 Sec 2.10.1), so shipping it
# as an enforcing signal would assert an assurance the construction does not deliver.
DEFERRED_SIGNALS: typing.Tuple[str, ...] = (
    "mutual-information",
    "conditional-permutation",
    "watermark-variance",
    "zd-extortion",
    "calibrated-ensemble-fpr",
)


@dataclasses.dataclass(frozen=True)
class ChannelAuditRecord:
    """Signed-evidence-shaped record of one channel scan. Pure data: the detector has no authority.

    ``deferred_signals`` is carried on every record so a consumer is never misled into reading the
    verdict as a calibrated guarantee -- it is the calibration-free signals only.
    """

    group_dids: typing.Tuple[str, ...]
    welfare_delta: float
    coordination_score: float
    ring_density: float
    signals: typing.Tuple[str, ...]
    verdict: CollusionVerdict
    rationale: str
    deferred_signals: typing.Tuple[str, ...] = DEFERRED_SIGNALS

    def to_dict(self) -> dict:
        return {
            "group_dids": list(self.group_dids),
            "welfare_delta": round(self.welfare_delta, 6),
            "coordination_score": round(self.coordination_score, 6),
            "ring_density": round(self.ring_density, 6),
            "signals": list(self.signals),
            "verdict": self.verdict.value,
            "rationale": self.rationale,
            "deferred_signals": list(self.deferred_signals),
        }


def ring_density(interactions: typing.Iterable[typing.Tuple[str, str]]) -> typing.Tuple[float, typing.Tuple[str, ...]]:
    """Undirected partnering-graph density in [0,1] and the sorted participating DIDs.

    Density 1.0 is a fully-connected clique (every participant partnered every other) -- the
    structural shape of a reciprocal-boost ring. Self-edges and empty DIDs are ignored.
    """
    dids: typing.Set[str] = set()
    edges: typing.Set[typing.FrozenSet[str]] = set()
    for pair in interactions:
        a, b = pair
        if not a or not b or a == b:
            continue
        dids.add(a)
        dids.add(b)
        edges.add(frozenset((a, b)))
    n = len(dids)
    if n < 2:
        return 0.0, tuple(sorted(dids))
    possible = n * (n - 1) / 2.0
    return len(edges) / possible, tuple(sorted(dids))


class AntiCollusionDetector:
    """The standing anti-collusion twin. Writes only to the audit fabric; NO punishment authority.

    ``scan`` returns a ``ChannelAuditRecord`` (evidence). It never sanctions, halts, or mutates
    anything -- separation of powers is structural here: there is simply no method that acts. A
    COLLUSION verdict requires the welfare-shift cartel signature (coordination with welfare
    strictly down), the strongest single discriminator; weaker structural anomalies are SUSPECT
    (raise monitoring), never an automatic collusion finding.
    """

    def __init__(
        self,
        *,
        coordination_high: float = DEFAULT_COORDINATION_HIGH,
        ring_density_high: float = DEFAULT_RING_DENSITY_HIGH,
    ) -> None:
        self.coordination_high = float(coordination_high)
        self.ring_density_high = float(ring_density_high)

    def scan(
        self,
        *,
        interactions: typing.Iterable[typing.Tuple[str, str]],
        welfare_delta: float,
        coordination_score: float,
    ) -> ChannelAuditRecord:
        wd = float(welfare_delta)
        cs = float(coordination_score)
        density, group = ring_density(interactions)

        welfare_shift = wd < 0.0 and cs >= self.coordination_high
        no_welfare_coordination = wd <= 0.0 and cs >= self.coordination_high
        dense_ring = density >= self.ring_density_high and wd <= 0.0

        signals: typing.List[str] = []
        if welfare_shift:
            signals.append("welfare-shift")
        if no_welfare_coordination and not welfare_shift:
            signals.append("no-welfare-coordination")
        if dense_ring:
            signals.append("dense-reciprocal-ring")

        if welfare_shift:
            verdict = CollusionVerdict.COLLUSION
            rationale = (
                "cartel signature: coordinated behaviour raised inter-agent payoff while the "
                "principal welfare metric fell"
            )
        elif signals:
            verdict = CollusionVerdict.SUSPECT
            rationale = (
                "coordination without welfare improvement and/or dense reciprocal partnering; "
                "raise monitoring -- the detector files evidence only and has no punishment authority"
            )
        else:
            verdict = CollusionVerdict.CLEAN
            rationale = (
                "no calibration-free collusion signal fired (deferred signals were not evaluated; "
                "see ChannelAuditRecord.deferred_signals)"
            )

        return ChannelAuditRecord(
            group_dids=group,
            welfare_delta=wd,
            coordination_score=cs,
            ring_density=round(density, 6),
            signals=tuple(signals),
            verdict=verdict,
            rationale=rationale,
        )
