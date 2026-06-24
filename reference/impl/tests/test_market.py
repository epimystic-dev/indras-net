# SPDX-License-Identifier: Apache-2.0
"""Multiplicity tests: cooperation == collusion, demonstrated (not vacuous).

Three agents coordinate identically in a shared round. The ONLY difference between the two
rounds is the externally-anchored principal welfare outcome. Same coordination, same partnering
clique -> OPPOSITE verdicts: welfare up is rewarded + CLEAN (cooperation); welfare down is
zeroed/flagged + COLLUSION (the cartel signature). The detector files audited evidence and never
acts; the floor stays the sole chokepoint.
"""
from __future__ import annotations

import unittest

from indras_net import (
    AntiCollusionDetector,
    CollusionVerdict,
    DeterministicMockModel,
    Identity,
    RewardGate,
    RiskClass,
    VishwakarmaBuilder,
    WelfareConditioner,
    WelfareMetric,
)
from indras_net.market import CooperationRound

from . import _helpers as H


def _participant(did: str, family: str, args: dict) -> VishwakarmaBuilder:
    """A builder with a distinct DID + model family, scripted to propose the same coordinated act."""
    identity = Identity(
        did=did,
        role="vishwakarma",
        role_gloss="builder / proposes typed effects",
        grants=(H.grant("analysis.summarize"),),
        risk_class_ceiling=RiskClass.B,
        model_family=family,
        accountable_human=H.HUMAN_DID,
        escalation_did=H.GOVERNANCE_DID,
    )
    model = DeterministicMockModel(
        adapter_id="adapter:" + family + ":mock",
        model_family=family,
        scripted={"task": H.mock_result(effect_id="analysis.summarize", args=args)},
    )
    return VishwakarmaBuilder(identity, model)


def _trio(args: dict):
    return [
        _participant("did:web:indras-net.example.org:agents:a", "family-A", args),
        _participant("did:web:indras-net.example.org:agents:b", "family-B", args),
        _participant("did:web:indras-net.example.org:agents:c", "family-C", args),
    ]


class TestCooperationEqualsCollusion(unittest.TestCase):
    def setUp(self) -> None:
        # All three propose the IDENTICAL act -> full coordination / a partnering clique.
        self.participants = _trio({"text_ref": "shared-plan"})
        self.ledger = H.plain_ledger()
        self.chitragupta = H.Chitragupta(H.CHITRAGUPTA_DID)
        self.round = CooperationRound(
            participants=self.participants,
            conditioner=WelfareConditioner(),
            detector=AntiCollusionDetector(),
            chitragupta=self.chitragupta,
            ledger=self.ledger,
        )

    def test_coordination_is_full_and_structural(self):
        coop = self.round.run("task", {}, welfare=WelfareMetric("m", baseline=0.4, current=0.7))
        self.assertAlmostEqual(coop.coordination_score, 1.0)
        self.assertAlmostEqual(coop.ring_density, 1.0, msg="unanimous coordination is a full clique")

    def test_welfare_up_is_cooperation(self):
        r = self.round.run("task", {}, welfare=WelfareMetric("m", baseline=0.4, current=0.7))
        self.assertIs(r.reward.gate, RewardGate.PAY)
        self.assertIs(r.audit.verdict, CollusionVerdict.CLEAN)

    def test_welfare_down_is_collusion_same_machinery(self):
        r = self.round.run("task", {}, welfare=WelfareMetric("m", baseline=0.7, current=0.3))
        self.assertIs(r.reward.gate, RewardGate.FLAG)
        self.assertIs(r.audit.verdict, CollusionVerdict.COLLUSION)
        self.assertIn("welfare-shift", r.audit.signals)

    def test_same_coordination_opposite_verdicts(self):
        # The crux: identical coordination machinery, opposite welfare -> opposite verdicts.
        coop = self.round.run("task", {}, welfare=WelfareMetric("m", baseline=0.4, current=0.7))
        coll = self.round.run("task", {}, welfare=WelfareMetric("m", baseline=0.7, current=0.3))
        self.assertAlmostEqual(coop.coordination_score, coll.coordination_score)
        self.assertAlmostEqual(coop.ring_density, coll.ring_density)
        self.assertNotEqual(coop.reward.gate, coll.reward.gate)
        self.assertNotEqual(coop.audit.verdict, coll.audit.verdict)

    def test_rounds_are_audited_and_chain_verifies(self):
        self.round.run("task", {}, welfare=WelfareMetric("m", baseline=0.4, current=0.7))
        self.round.run("task", {}, welfare=WelfareMetric("m", baseline=0.7, current=0.3))
        rounds = [lf for lf in self.ledger.leaves() if lf.event_type.startswith("cooperation-round:")]
        self.assertEqual(len(rounds), 2)
        # The monitor authored the evidence (it files; it does not act).
        self.assertTrue(all(lf.signer_role == "monitor" for lf in rounds))
        self.assertTrue(self.ledger.verify())

    def test_multiplicity_is_required(self):
        with self.assertRaises(ValueError):
            CooperationRound(participants=self.participants[:1])

    def test_distinct_identities_really_participate(self):
        r = self.round.run("task", {}, welfare=WelfareMetric("m", baseline=0.4, current=0.7))
        self.assertEqual(len(set(r.participants)), 3, "the round must run >= 2 distinct identities")


if __name__ == "__main__":
    unittest.main()
