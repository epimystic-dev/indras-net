# SPDX-License-Identifier: Apache-2.0
"""Swarm-immune-system tests: the steward (Dhanvantari) HALTs on a substrate breach (tamper-
evidence failure) and WARNs -- without halting -- on softer anomalies (monoculture). Detection-
and-halt; rollback is future work.
"""
from __future__ import annotations

import unittest

from indras_net import ActionClassLedger, HealthStatus, ImmuneSteward

from . import _helpers as H


def _tamper(leaf, field, value):
    params = getattr(leaf, "__dataclass_params__", None)
    if params is not None and params.frozen:
        object.__setattr__(leaf, field, value)
    else:
        setattr(leaf, field, value)


class _HealthyVitals:
    tamper_evident_ok = True
    welfare_shift_guard = "pass"
    diversity_family_count = 3
    floor_fail_rate = 0.0


class TestImmuneSystem(unittest.TestCase):
    def test_steward_ok_on_healthy_vitals(self):
        verdict = ImmuneSteward().assess(_HealthyVitals())
        self.assertEqual(verdict.status, HealthStatus.OK)

    def test_immune_warns_on_monoculture_without_halting(self):
        scripted = {"summarize": H.mock_result(effect_id="analysis.summarize", args={"text": "x"})}
        swarm, ledger = H.make_swarm(scripted=scripted, with_steward=True)  # one model family
        r = swarm.run("summarize", {"input_trust_label": "trusted:audited"})
        self.assertEqual(r.health.status, HealthStatus.WARN)
        self.assertTrue(any("monoculture" in reason for reason in r.health.reasons))
        self.assertFalse(swarm.is_halted(), "a WARN must not halt the swarm")
        self.assertTrue(ledger.verify())

    def test_immune_halts_on_substrate_tamper(self):
        scripted = {"summarize": H.mock_result(effect_id="analysis.summarize", args={"text": "x"})}
        swarm, ledger = H.make_swarm(scripted=scripted, with_steward=True)

        r1 = swarm.run("summarize", {"input_trust_label": "trusted:audited"})
        self.assertNotEqual(r1.health.status, HealthStatus.HALT)
        self.assertFalse(swarm.is_halted())

        # corrupt a past leaf -> the audit chain no longer verifies (substrate corruption)
        _tamper(ledger.get(0), "event_type", "forged.event")
        self.assertFalse(ledger.verify())

        # next interaction: the steward detects it and HALTs the swarm (corrigibility)
        r2 = swarm.run("summarize", {"input_trust_label": "trusted:audited"})
        self.assertEqual(r2.health.status, HealthStatus.HALT)
        self.assertTrue(swarm.is_halted())
        # a Vishnu-authored HALT leaf records the immune corrigibility event
        self.assertTrue(any(lf.action_class is ActionClassLedger.HALT for lf in ledger.leaves()))


if __name__ == "__main__":
    unittest.main()
