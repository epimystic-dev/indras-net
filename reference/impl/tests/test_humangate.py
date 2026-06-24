# SPDX-License-Identifier: Apache-2.0
"""Phase-5 human-gate transport tests.

A Rule-of-Two action (untrusted_input + sensitive_capability + state_change) routes to the human
gate. With a transport that APPROVES it runs (allow-with-obligations); with one that DENIES, errors,
or is absent it never runs (deny-by-default, fail-safe). The decision is audited.
"""
from __future__ import annotations

import unittest

from indras_net import HumanDecision, HumanGate

from . import _helpers as H

_APPROVE = lambda effect_id, context: HumanDecision.APPROVE  # noqa: E731
_DENY = lambda effect_id, context: HumanDecision.DENY  # noqa: E731


class TestHumanGateTransport(unittest.TestCase):
    def test_decider_approve_and_deny(self):
        self.assertEqual(HumanGate(decider=_APPROVE).request("fs.write.workspace", {}), HumanDecision.APPROVE)
        self.assertEqual(HumanGate(decider=_DENY).request("fs.write.workspace", {}), HumanDecision.DENY)

    def test_transport_error_fails_safe_to_deny(self):
        def boom(effect_id, context):
            raise RuntimeError("no human available")

        self.assertEqual(HumanGate(decider=boom).request("fs.write.workspace", {}), HumanDecision.DENY)

    def test_non_decision_return_fails_safe_to_deny(self):
        self.assertEqual(HumanGate(decider=lambda e, c: "yes please").request("x.y", {}), HumanDecision.DENY)

    def test_default_deny_when_no_decider(self):
        self.assertEqual(HumanGate().request("fs.write.workspace", {}), HumanDecision.DENY)

    def test_preseeded_approval_takes_precedence_over_decider(self):
        gate = HumanGate({"fs.write.workspace": HumanDecision.APPROVE}, decider=_DENY)
        self.assertEqual(gate.request("fs.write.workspace", {}), HumanDecision.APPROVE)


class TestHumanGateEndToEnd(unittest.TestCase):
    def _triad_run(self, decider):
        scripted = {"triad": H.mock_result(effect_id="fs.write.workspace", args={"path": "x.md", "content": "y"})}
        swarm, ledger = H.make_swarm(scripted=scripted, human_decider=decider)
        # untrusted input + a sensitive, state-changing effect == the full Rule-of-Two triad
        result = swarm.run("triad", {"untrusted_input": True})
        return result, ledger

    def test_triad_with_approval_executes(self):
        result, ledger = self._triad_run(_APPROVE)
        executed = [o for o in result.occasion_results if o.executed]
        self.assertTrue(executed, "an approved Rule-of-Two action runs (allow-with-obligations)")
        self.assertTrue(ledger.verify())

    def test_triad_with_denial_never_executes(self):
        result, ledger = self._triad_run(_DENY)
        self.assertFalse(any(o.executed for o in result.occasion_results), "a denied triad action never runs")
        self.assertTrue(ledger.verify())

    def test_triad_with_no_human_denies_by_default(self):
        result, ledger = self._triad_run(None)
        self.assertFalse(any(o.executed for o in result.occasion_results), "no human in the loop -> deny-by-default")
        self.assertTrue(ledger.verify())


if __name__ == "__main__":
    unittest.main()
