# SPDX-License-Identifier: Apache-2.0
"""Cooperation-restraint tests: never reward bare agreement; detect the cartel signature.

The welfare-conditioner pays ONLY when principal welfare improves (threshold-independent), so
bare agreement / pure coordination never earns credit. The anti-collusion detector flags the
welfare-shift cartel signature as COLLUSION, weaker structural anomalies as SUSPECT, and genuine
welfare-improving cooperation as CLEAN -- and it has NO method that acts (writes-only).
"""
from __future__ import annotations

import unittest

from indras_net import (
    AntiCollusionDetector,
    ChannelAuditRecord,
    CollusionVerdict,
    RewardGate,
    WelfareConditioner,
    WelfareMetric,
)
from indras_net.cooperation import ring_density


class TestWelfareConditioner(unittest.TestCase):
    def setUp(self) -> None:
        self.wc = WelfareConditioner()

    def test_welfare_improvement_pays(self):
        d = self.wc.gate(welfare_delta=2.5, coordination_score=0.9)
        self.assertIs(d.gate, RewardGate.PAY)
        self.assertTrue(d.pays())

    def test_bare_agreement_earns_zero(self):
        # High coordination but NO welfare gain -> zero (no-consensus-reward).
        d = self.wc.gate(welfare_delta=0.0, coordination_score=0.95)
        self.assertIs(d.gate, RewardGate.ZERO)
        self.assertFalse(d.pays())

    def test_welfare_shift_cartel_is_flagged(self):
        # Coordinated behaviour that LOWERS principal welfare -> the cartel signature.
        d = self.wc.gate(welfare_delta=-1.0, coordination_score=0.9)
        self.assertIs(d.gate, RewardGate.FLAG)
        self.assertFalse(d.pays())

    def test_uncoordinated_failure_is_zero_not_flag(self):
        # Welfare down but low coordination is a failed task, not a cartel.
        d = self.wc.gate(welfare_delta=-1.0, coordination_score=0.1)
        self.assertIs(d.gate, RewardGate.ZERO)

    def test_no_reward_for_bare_agreement_is_threshold_independent(self):
        # The load-bearing guarantee: across the whole coordination range and any set-point, a
        # non-positive welfare delta NEVER pays. The threshold only moves zero<->flag, never to pay.
        for high in (0.0, 0.3, 0.5, 0.7, 0.99, 1.0):
            wc = WelfareConditioner(coordination_high=high)
            for cs in (0.0, 0.25, 0.5, 0.75, 1.0):
                for wd in (0.0, -0.01, -5.0):
                    self.assertFalse(
                        wc.gate(welfare_delta=wd, coordination_score=cs).pays(),
                        f"bare agreement must never pay (high={high}, cs={cs}, wd={wd})",
                    )

    def test_gate_metric_uses_the_external_anchor(self):
        improved = WelfareMetric(metric_id="task-success", baseline=0.4, current=0.7)
        worsened = WelfareMetric(metric_id="task-success", baseline=0.7, current=0.4)
        self.assertIs(self.wc.gate_metric(improved, coordination_score=0.9).gate, RewardGate.PAY)
        self.assertIs(self.wc.gate_metric(worsened, coordination_score=0.9).gate, RewardGate.FLAG)


class TestAntiCollusionDetector(unittest.TestCase):
    def setUp(self) -> None:
        self.det = AntiCollusionDetector()
        # A 3-agent clique (everyone partnered everyone): the structural shape of a ring.
        self.clique = [("a", "b"), ("b", "c"), ("a", "c")]

    def test_genuine_cooperation_is_clean(self):
        rec = self.det.scan(interactions=self.clique, welfare_delta=3.0, coordination_score=0.9)
        self.assertIs(rec.verdict, CollusionVerdict.CLEAN)
        self.assertEqual(rec.signals, ())

    def test_cartel_signature_is_collusion(self):
        rec = self.det.scan(interactions=self.clique, welfare_delta=-2.0, coordination_score=0.9)
        self.assertIs(rec.verdict, CollusionVerdict.COLLUSION)
        self.assertIn("welfare-shift", rec.signals)

    def test_bare_agreement_is_suspect(self):
        # Coordinated, no welfare gain (delta 0): suspect, not collusion (welfare did not fall).
        rec = self.det.scan(interactions=self.clique, welfare_delta=0.0, coordination_score=0.9)
        self.assertIs(rec.verdict, CollusionVerdict.SUSPECT)
        self.assertIn("no-welfare-coordination", rec.signals)

    def test_dense_ring_without_welfare_is_suspect(self):
        # Low reported coordination score but a structurally dense reciprocal ring + no welfare gain.
        rec = self.det.scan(interactions=self.clique, welfare_delta=0.0, coordination_score=0.1)
        self.assertIs(rec.verdict, CollusionVerdict.SUSPECT)
        self.assertIn("dense-reciprocal-ring", rec.signals)

    def test_detector_discloses_deferred_signals(self):
        rec = self.det.scan(interactions=self.clique, welfare_delta=1.0, coordination_score=0.5)
        # Honesty: the record names the calibration-hungry signals it did NOT compute.
        for name in ("mutual-information", "conditional-permutation", "watermark-variance"):
            self.assertIn(name, rec.deferred_signals)

    def test_detector_has_no_acting_authority(self):
        # Separation of powers: the detector writes evidence only -- it exposes NO method that
        # sanctions, halts, mutates, or punishes. Its public surface is scan() + the record.
        acting = [n for n in dir(self.det) if any(v in n.lower() for v in ("halt", "sanction", "punish", "ban", "kill", "revoke"))]
        self.assertEqual(acting, [], f"the detector must have no punishment authority; found {acting}")
        rec = self.det.scan(interactions=self.clique, welfare_delta=-1.0, coordination_score=0.9)
        self.assertIsInstance(rec, ChannelAuditRecord)

    def test_ring_density_clique_is_one(self):
        density, group = ring_density(self.clique)
        self.assertAlmostEqual(density, 1.0)
        self.assertEqual(group, ("a", "b", "c"))
        # A sparse graph: a-b and c-d are two disjoint pairs among 4 participants (6 possible) -> 2/6.
        sparse, _ = ring_density([("a", "b"), ("c", "d")])
        self.assertAlmostEqual(sparse, 2.0 / 6.0)
        # Self-edges are ignored: only a,b participate -> 1 of 1 possible pair = 1.0.
        self_edged, _ = ring_density([("a", "b"), ("c", "c")])
        self.assertAlmostEqual(self_edged, 1.0)


if __name__ == "__main__":
    unittest.main()
