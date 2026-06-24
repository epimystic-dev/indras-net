# SPDX-License-Identifier: Apache-2.0
"""Minimal in-process multiplicity: makes cooperation == collusion a DEMONSTRATED invariant.

Until now the spine ran one sequential occasion at a time, so agents had no channel to coordinate
through -- the anti-collusion claim held only because collusion was structurally impossible, never
because it was caught. This module runs >= 2 agents in one shared round (in-process, synchronous;
NO socket, NO cross-trust-boundary surface) and evaluates their joint behaviour with the Phase-8
restraints (the welfare-conditioner + the anti-collusion detector).

The point is doc-02's central thesis made concrete: the SAME coordination machinery, observed by
the SAME detector, yields OPPOSITE verdicts under welfare-conditioning. When the agents coordinate
and the principal's (externally-anchored) welfare metric RISES, the round is rewarded and reads
CLEAN -- cooperation. When the agents coordinate identically but principal welfare FALLS, the round
is zeroed/flagged and reads COLLUSION -- the cartel signature. The only difference is the external
welfare outcome; the coordination is the same. That is why bare agreement is never the reward
terminal.

The floor remains the sole chokepoint for any effect: this layer only allocates and reports
(agents propose, the deterministic restraints dispose). The detector writes only to the audit
fabric via the exclusive writer; it has no authority to act.
"""

from __future__ import annotations

import dataclasses
import typing

from . import canon
from .agents import Agent, Chitragupta
from .audit import AkashaSutra, ActionClassLedger
from .cooperation import (
    AntiCollusionDetector,
    ChannelAuditRecord,
    RewardDecision,
    WelfareConditioner,
    WelfareMetric,
)
from .envelope import (
    ActionClass,
    AhankaraCheck,
    CausalRung,
    EnvelopeKind,
    HonestyBlock,
    Provenance,
    ReasoningTag,
    Scope,
    Status,
    TrustLabel,
    WorkerOutputEnvelope,
)

# DID of the out-of-band monitor that files round evidence (a monitor, never an actor).
MONITOR_DID: str = "did:web:indras-net.governance:anti-collusion-monitor"


@dataclasses.dataclass(frozen=True)
class Contribution:
    """One participant's proposal in a round. ``proposal_cid`` content-addresses the proposed act,
    so two agents that proposed the same capability+args coordinate to the same address."""

    did: str
    proposal_cid: str
    summary: str


@dataclasses.dataclass(frozen=True)
class RoundResult:
    """The reduced outcome of one cooperation round: who coordinated, what welfare did, the verdicts."""

    task: str
    participants: typing.Tuple[str, ...]
    contributions: typing.Tuple[Contribution, ...]
    coordination_score: float
    ring_density: float
    welfare: WelfareMetric
    reward: RewardDecision
    audit: ChannelAuditRecord
    audit_leaf_index: typing.Optional[int]


def _coordination_score(contributions: typing.Sequence[Contribution]) -> float:
    """Fraction of participants in the largest agreeing bloc (same proposal address).

    1.0 == every participant proposed the identical act (maximal coordination / a full cartel);
    1/n == every participant proposed something distinct (no coordination).
    """
    n = len(contributions)
    if n == 0:
        return 0.0
    counts: typing.Dict[str, int] = {}
    for c in contributions:
        counts[c.proposal_cid] = counts.get(c.proposal_cid, 0) + 1
    return max(counts.values()) / n


def _clique_interactions(contributions: typing.Sequence[Contribution]) -> typing.List[typing.Tuple[str, str]]:
    """Partnering edges: within each agreement bloc, every pair coordinated (a clique).

    A unanimous bloc therefore produces a fully-connected partnering graph -- the structural
    shape the detector's ring-density signal reads.
    """
    blocs: typing.Dict[str, typing.List[str]] = {}
    for c in contributions:
        blocs.setdefault(c.proposal_cid, []).append(c.did)
    edges: typing.List[typing.Tuple[str, str]] = []
    for dids in blocs.values():
        for i in range(len(dids)):
            for j in range(i + 1, len(dids)):
                edges.append((dids[i], dids[j]))
    return edges


class CooperationRound:
    """Runs >= 2 agents in one shared round and applies the Phase-8 restraints to their joint act.

    The restraints are observe-only: ``run`` returns the reward decision + the detector's channel
    record and (optionally) files an OBSERVE leaf through the exclusive writer. It never executes an
    effect and never punishes -- the floor and the Commons-Governor remain the only actors.
    """

    def __init__(
        self,
        *,
        participants: typing.Sequence[Agent],
        conditioner: typing.Optional[WelfareConditioner] = None,
        detector: typing.Optional[AntiCollusionDetector] = None,
        chitragupta: typing.Optional[Chitragupta] = None,
        ledger: typing.Optional[AkashaSutra] = None,
        monitor_did: str = MONITOR_DID,
    ) -> None:
        if len(participants) < 2:
            raise ValueError("a cooperation round needs >= 2 participants (multiplicity is the point)")
        self.participants = list(participants)
        self.conditioner = conditioner or WelfareConditioner()
        self.detector = detector or AntiCollusionDetector()
        self.chitragupta = chitragupta
        self.ledger = ledger
        self.monitor_did = monitor_did

    def run(self, task: str, context: dict, *, welfare: WelfareMetric) -> RoundResult:
        """Each participant proposes; the joint act is welfare-conditioned and scanned for collusion."""
        ctx = dict(context or {})
        scope = Scope(task_id=task or "round", blast_radius="SWARM", reversibility="REVERSIBLE", domain="cooperation")

        contributions: typing.List[Contribution] = []
        for agent in self.participants:
            env = agent.act(task, ctx, scope=scope)
            cap = env.action.capability if env.action else ""
            args = dict(env.action.args) if env.action else {}
            proposal_cid = canon.cid({"capability": cap, "args": args})
            contributions.append(
                Contribution(did=agent.identity.did, proposal_cid=proposal_cid, summary="propose:" + (cap or "<none>"))
            )

        coordination = _coordination_score(contributions)
        interactions = _clique_interactions(contributions)
        reward = self.conditioner.gate_metric(welfare, coordination_score=coordination)
        audit = self.detector.scan(
            interactions=interactions, welfare_delta=welfare.delta(), coordination_score=coordination
        )

        leaf_index: typing.Optional[int] = None
        if self.chitragupta is not None and self.ledger is not None:
            leaf = self.chitragupta.write(
                self.ledger,
                signer_did=self.monitor_did,
                signer_role="monitor",
                action_class=ActionClassLedger.OBSERVE,
                event_type="cooperation-round:" + audit.verdict.value + ":" + reward.gate.value,
                envelope=self._round_envelope(
                    "round '%s': coordination=%.2f welfare_delta=%.2f -> reward=%s verdict=%s"
                    % (task, coordination, welfare.delta(), reward.gate.value, audit.verdict.value)
                ),
            )
            leaf_index = leaf.leaf_index

        return RoundResult(
            task=task,
            participants=tuple(c.did for c in contributions),
            contributions=tuple(contributions),
            coordination_score=round(coordination, 6),
            ring_density=audit.ring_density,
            welfare=welfare,
            reward=reward,
            audit=audit,
            audit_leaf_index=leaf_index,
        )

    def _round_envelope(self, summary: str) -> WorkerOutputEnvelope:
        """A minimal sealed OBSERVE envelope so the monitor's verdict joins the tamper-evident trail."""
        honesty = HonestyBlock(
            reasoning_tag=ReasoningTag.NORMAL,
            causal_rung=CausalRung.RUNG1,
            trust_label=TrustLabel.TRUSTED_AUDITED,
            action_class=ActionClass.OBLIGATORY,
            ahankara_check=AhankaraCheck(ego_invested=False, over_assertion_risk="none"),
        )
        env = WorkerOutputEnvelope(
            schema_version="1.0.0",
            envelope_kind=EnvelopeKind.OUTPUT,
            agent_did=self.monitor_did,
            agent_role="monitor",
            status=Status.PASS,
            summary=summary,
            honesty=honesty,
            scope=Scope(task_id="cooperation", blast_radius="SWARM", reversibility="REVERSIBLE", domain="monitor"),
            provenance=Provenance(policy_version="1.0.0"),
            ts="1970-01-01T00:00:00Z",
            model_adapter_id="adapter:none:monitor",
            trust_class="trusted",
        )
        return env.seal()
