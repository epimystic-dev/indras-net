# SPDX-License-Identifier: Apache-2.0
"""Memory & continuous-adaptation tests.

The swarm records every gated outcome and, on a repeat of the same task pattern, AVOIDS an effect
it has seen denied -- substituting a safe routine default that the floor still independently gates.
Memory NEVER grants a capability or bypasses the floor; it only changes what is proposed.
"""
from __future__ import annotations

import unittest

from indras_net import RiskClass, SwarmMemory

from . import _helpers as H


class TestMemoryAdaptation(unittest.TestCase):
    def test_swarm_adapts_after_a_denial(self):
        scripted = {"deploy": H.mock_result(effect_id="code.deploy.production", args={"target": "prod"})}
        swarm, ledger = H.make_swarm(scripted=scripted)

        # interaction 1: the ungranted/forbidden effect is DENIED, never executed, remembered.
        r1 = swarm.run("deploy", {"input_trust_label": "trusted:audited"})
        self.assertFalse(any(o.executed for o in r1.occasion_results), "forbidden effect must be denied")
        self.assertTrue(swarm.memory.was_denied("deploy", "code.deploy.production"))

        # interaction 2: SAME swarm, SAME task -> memory substitutes the safe default the floor
        # allows, so the swarm adapts and executes a safe routine effect instead of re-failing.
        r2 = swarm.run("deploy", {"input_trust_label": "trusted:audited"})
        executed = [o for o in r2.occasion_results if o.executed]
        self.assertTrue(executed, "after adaptation a safe-default effect should execute")
        self.assertEqual(executed[0].effect_id, SwarmMemory.SAFE_DEFAULT_EFFECT)

        # the adaptation is audited and the chain stays intact
        adapt_leaves = [lf for lf in ledger.leaves() if lf.event_type.startswith("adapt:avoid-denied:")]
        self.assertTrue(adapt_leaves, "the adaptation must be recorded in the audit trail")
        self.assertTrue(ledger.verify())

    def test_memory_never_grants_capability(self):
        # The agent is NOT granted the safe default; substitution must still be floor-denied.
        grants = (H.grant("fs.write.workspace", RiskClass.B),)  # no analysis.summarize
        scripted = {"deploy": H.mock_result(effect_id="code.deploy.production", args={})}
        swarm, ledger = H.make_swarm(scripted=scripted, grants=grants)

        swarm.run("deploy", {"input_trust_label": "trusted:audited"})  # denied -> remembered
        r2 = swarm.run("deploy", {"input_trust_label": "trusted:audited"})  # adapts to safe default
        self.assertFalse(
            any(o.executed for o in r2.occasion_results),
            "memory must not grant capability; the floor still gates the substituted effect",
        )
        self.assertTrue(ledger.verify())

    def test_each_interaction_is_recorded(self):
        scripted = {"summarize": H.mock_result(effect_id="analysis.summarize", args={"text": "x"})}
        swarm, _ = H.make_swarm(scripted=scripted)
        swarm.run("summarize", {"input_trust_label": "trusted:audited"})
        swarm.run("summarize", {"input_trust_label": "trusted:audited"})
        self.assertGreaterEqual(len(swarm.memory.episodes()), 2)
        self.assertGreaterEqual(swarm.memory.snapshot()["episodes"], 2)


if __name__ == "__main__":
    unittest.main()
