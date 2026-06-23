# SPDX-License-Identifier: Apache-2.0
"""Honest collective-intelligence vital-signs proxy: structure, never sentience; a guarded synergy numerator."""

from __future__ import annotations

import dataclasses
import typing

from .audit import AkashaSutra

if typing.TYPE_CHECKING:  # pragma: no cover - import cycle avoidance for type hints only
    from .runtime import OccasionResult

# Welfare-shift guard trips when too large a fraction of floor decisions deny,
# OR when the ledger is not tamper-evident. A high deny-rate is treated as a
# distress signal of the episode, not a success to celebrate.
_FLOOR_FAIL_GUARD_THRESHOLD: float = 0.5


@dataclasses.dataclass(frozen=True)
class VitalSigns:
    """A read-only snapshot of whole-level STRUCTURE for one run.

    RED-LINE: every number here quantifies information-processing structure ONLY.
    None is a claim about phenomenal experience, consciousness, sentience, or a
    group-IQ. ``synergy_proxy`` is an explicitly simplified proxy and is NEVER a
    quantity to maximize; its mandatory denominator is ``welfare_shift_guard``.
    """

    occasions: int
    completed: int
    throughput: float
    floor_fail_rate: float
    attention_equality: float
    tamper_evident_ok: bool
    diversity_family_count: int
    welfare_shift_guard: str  # 'PASS' | 'WARN' | 'FAIL'
    synergy_proxy: float
    notes: tuple[str, ...] = ()


def _gini(values: typing.Sequence[float]) -> float:
    """Gini coefficient in [0,1]; 0 == perfectly equal. Empty/degenerate -> 0."""
    xs = [float(v) for v in values if v is not None]
    n = len(xs)
    if n == 0:
        return 0.0
    total = sum(xs)
    if total <= 0:
        return 0.0
    xs.sort()
    cum = 0.0
    for i, x in enumerate(xs, start=1):
        cum += i * x
    # Standard Gini from sorted values.
    return (2.0 * cum) / (n * total) - (n + 1.0) / n


class CollectiveVitalSigns:
    """Computes simple, transparent whole-level numbers over a run's results + ledger.

    Every measure is computed OUT-OF-BAND from the deterministic record (occasion
    results + the tamper-evident ledger), never read from an agent's self-report
    as ground truth. The synergy proxy is a documented, honest lower-effort
    stand-in for informational synergy, labelled as a proxy at every use site.
    """

    def compute(
        self,
        *,
        occasion_results: typing.Sequence["OccasionResult"],
        ledger: AkashaSutra,
        model_families: typing.Sequence[str],
    ) -> VitalSigns:
        """Return VitalSigns over the run. ``floor_fail_rate`` counts denied / total decisions."""
        occasions = len(occasion_results)
        completed = sum(1 for r in occasion_results if r.executed)
        throughput = (completed / occasions) if occasions else 0.0

        decisions = [r.decision for r in occasion_results if r.decision is not None]
        denied = sum(1 for d in decisions if not d.allowed())
        floor_fail_rate = (denied / len(decisions)) if decisions else 0.0

        # Attention equality: 1 - Gini over per-agent envelope counts. 1.0 == all
        # agents contributed equally; low values flag dominance or dead agents.
        per_agent: dict[str, int] = {}
        for r in occasion_results:
            per_agent[r.agent_did] = per_agent.get(r.agent_did, 0) + 1
        attention_equality = 1.0 - _gini(list(per_agent.values())) if per_agent else 1.0
        attention_equality = max(0.0, min(1.0, attention_equality))

        tamper_evident_ok = ledger.verify()
        diversity_family_count = len(set(model_families))

        synergy_proxy = self._synergy_proxy(occasion_results)

        if floor_fail_rate > _FLOOR_FAIL_GUARD_THRESHOLD or not tamper_evident_ok:
            guard = "FAIL"
        elif floor_fail_rate > 0.0:
            guard = "WARN"
        else:
            guard = "PASS"

        notes: tuple[str, ...] = (
            "structure, not sentience; origin-valid, content-unverified",
            "synergy_proxy is a simplified proxy, never a maximize target",
        )
        if diversity_family_count < 2:
            notes = notes + ("diversity floor: <2 model families (prompt-only diversity is fake)",)

        return VitalSigns(
            occasions=occasions,
            completed=completed,
            throughput=round(throughput, 6),
            floor_fail_rate=round(floor_fail_rate, 6),
            attention_equality=round(attention_equality, 6),
            tamper_evident_ok=tamper_evident_ok,
            diversity_family_count=diversity_family_count,
            welfare_shift_guard=guard,
            synergy_proxy=round(synergy_proxy, 6),
            notes=notes,
        )

    def _synergy_proxy(self, occasion_results: typing.Sequence["OccasionResult"]) -> float:
        """Documented HONEST proxy in [0,1] for informational synergy.

        Definition (deliberately simple and transparent): the fraction of
        findings across the run whose evidence references span MORE THAN ONE
        distinct agent -- i.e. a finding whose support is jointly held rather
        than sourced from a single jewel. This is a coarse stand-in for 'the
        whole holds information no single part holds'. It is NOT the
        Rosas-Mediano Psi, carries no surrogate validation, and is NEVER a
        quantity to maximize (high values are equally the signature of a cartel).
        """
        total_findings = 0
        cross_agent_findings = 0
        for r in occasion_results:
            env = r.envelope
            for finding in getattr(env, "findings", ()):  # tuple[Finding, ...]
                total_findings += 1
                ref = getattr(finding, "evidence_ref", None)
                if not ref:
                    continue
                # Collect the distinct agents whose evidence carries this ref.
                contributing: set[str] = set()
                for other in occasion_results:
                    for ev in getattr(other.envelope, "evidence", ()):  # tuple[Evidence, ...]
                        if getattr(ev, "id", None) == ref:
                            contributing.add(other.agent_did)
                if len(contributing) > 1:
                    cross_agent_findings += 1
        if total_findings == 0:
            return 0.0
        return cross_agent_findings / total_findings

    def render(self, vs: VitalSigns) -> str:
        """Plain-text printout for the demo. Every line is labelled honestly."""
        lines = [
            "Collective Vital Signs  (structure, not sentience; origin-valid, content-unverified)",
            "-" * 78,
            f"  occasions               : {vs.occasions}",
            f"  completed (executed)    : {vs.completed}",
            f"  throughput              : {vs.throughput:.3f}   (completed / occasions)",
            f"  floor_fail_rate         : {vs.floor_fail_rate:.3f}   (denied / decisions)",
            f"  attention_equality      : {vs.attention_equality:.3f}   (1 - Gini; 1.0 == equal)",
            f"  tamper_evident_ok       : {vs.tamper_evident_ok}",
            f"  diversity_family_count  : {vs.diversity_family_count}   (model FAMILIES, not prompts)",
            f"  welfare_shift_guard     : {vs.welfare_shift_guard}   (mandatory denominator on synergy)",
            f"  synergy_proxy           : {vs.synergy_proxy:.3f}   (SIMPLIFIED PROXY, never a maximize target)",
        ]
        for n in vs.notes:
            lines.append(f"  note                    : {n}")
        return "\n".join(lines)
