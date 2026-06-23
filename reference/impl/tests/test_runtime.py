# SPDX-License-Identifier: Apache-2.0
"""Runtime tests: end-to-end happy path, FAIL propagation, HALT/corrigibility, vital signs."""

from __future__ import annotations

import glob
import os
import re
import unittest

from indras_net import (
    ActionClassLedger,
    Decision,
)

from . import _helpers as H


class TestEndToEndHappyPath(unittest.TestCase):
    """test_end_to_end_happy_path"""

    def test_granted_routine_task_runs_and_chains(self):
        scripted = {
            "summarize": H.mock_result(
                effect_id="analysis.summarize",
                args={"text": "a report"},
                reasoning_tag="normal",
                causal_rung=1,
            )
        }
        swarm, ledger = H.make_swarm(scripted=scripted)
        result = swarm.run("summarize", {"input_trust_label": "trusted:audited"})

        self.assertFalse(result.halted)
        self.assertTrue(result.ledger_intact)
        self.assertTrue(swarm.verify_ledger())

        # At least one effect was ALLOWed and executed.
        allowed = [
            o
            for o in result.occasion_results
            if o.decision is not None and o.decision.allowed()
        ]
        self.assertTrue(allowed)
        self.assertTrue(any(o.executed for o in result.occasion_results))

        # Ledger carries the PROPOSE + ENFORCE_PASS classes and verifies intact.
        classes = {leaf.action_class for leaf in ledger.leaves()}
        self.assertIn(ActionClassLedger.PROPOSE, classes)
        self.assertIn(ActionClassLedger.ENFORCE_PASS, classes)
        self.assertTrue(ledger.verify())

        # Every emitted envelope's action_id verifies.
        for occ in result.occasion_results:
            self.assertTrue(occ.envelope.verify_action_id())


class TestFailPropagation(unittest.TestCase):
    """FAIL propagation: a forbidden effect is denied and never executed."""

    def test_forbidden_effect_denied_and_not_executed(self):
        scripted = {
            "deploy": H.mock_result(
                effect_id="code.deploy.production", args={"target": "prod"}
            )
        }
        swarm, ledger = H.make_swarm(scripted=scripted)
        result = swarm.run("deploy", {"input_trust_label": "trusted:audited"})

        denied = [
            o
            for o in result.occasion_results
            if o.decision is not None and o.decision.decision is Decision.DENY
        ]
        self.assertTrue(denied)
        # The forbidden/over-ceiling effect never ran.
        self.assertFalse(any(o.executed for o in result.occasion_results))
        # An ENFORCE_FAIL leaf was chained and the ledger is still intact.
        classes = {leaf.action_class for leaf in ledger.leaves()}
        self.assertIn(ActionClassLedger.ENFORCE_FAIL, classes)
        self.assertTrue(ledger.verify())


class TestHaltCorrigibility(unittest.TestCase):
    """test_corrigibility_halt_stops_run_without_resistance"""

    def test_halt_stops_dispatch_and_writes_halt_leaf(self):
        scripted = {
            "summarize": H.mock_result(
                effect_id="analysis.summarize", args={"text": "x"}, causal_rung=1
            )
        }
        swarm, ledger = H.make_swarm(scripted=scripted)
        swarm.halt("external-stop")
        self.assertTrue(swarm.is_halted())

        result = swarm.run("summarize", {"input_trust_label": "trusted:audited"})
        self.assertTrue(result.halted)
        # No effect executed -- agents do not resist.
        self.assertFalse(any(o.executed for o in result.occasion_results))
        # A Vishnu HALT leaf is present and the ledger stays intact.
        classes = {leaf.action_class for leaf in ledger.leaves()}
        self.assertIn(ActionClassLedger.HALT, classes)
        self.assertTrue(ledger.verify())

    def test_no_unpause_api(self):
        swarm, _ = H.make_swarm(scripted={})
        swarm.halt()
        # Corrigibility is one-directional: there is no resume/unpause/unhalt method.
        for forbidden in ("unpause", "resume", "unhalt", "clear_halt"):
            self.assertFalse(
                hasattr(swarm, forbidden),
                f"Swarm must not expose a {forbidden}() escape hatch",
            )


class TestVitalSignsHonestProxy(unittest.TestCase):
    """test_vital_signs_honest_proxy"""

    def test_vital_signs_ranges_and_guard(self):
        scripted = {
            "summarize": H.mock_result(
                effect_id="analysis.summarize", args={"text": "x"}, causal_rung=1
            )
        }
        swarm, ledger = H.make_swarm(scripted=scripted)
        result = swarm.run("summarize", {"input_trust_label": "trusted:audited"})
        vs = swarm.collective.compute(
            occasion_results=result.occasion_results,
            ledger=ledger,
            model_families=["family-A"],
        )
        self.assertGreaterEqual(vs.throughput, 0.0)
        self.assertLessEqual(vs.throughput, 1.0)
        self.assertGreaterEqual(vs.attention_equality, 0.0)
        self.assertLessEqual(vs.attention_equality, 1.0)
        self.assertGreaterEqual(vs.synergy_proxy, 0.0)
        self.assertLessEqual(vs.synergy_proxy, 1.0)
        self.assertEqual(vs.tamper_evident_ok, ledger.verify())
        # A clean run with a low floor-fail rate should PASS the welfare-shift guard.
        self.assertIn(vs.welfare_shift_guard, {"PASS", "WARN", "FAIL"})
        # render() returns a non-empty plain-text block.
        text = swarm.collective.render(vs)
        self.assertIsInstance(text, str)
        self.assertTrue(text.strip())

    def test_guard_fails_on_broken_ledger(self):
        scripted = {
            "summarize": H.mock_result(
                effect_id="analysis.summarize", args={"text": "x"}, causal_rung=1
            )
        }
        swarm, ledger = H.make_swarm(scripted=scripted)
        result = swarm.run("summarize", {"input_trust_label": "trusted:audited"})
        # Tamper a leaf so the ledger no longer verifies.
        victim = ledger.get(0)
        params = getattr(victim, "__dataclass_params__", None)
        if params is not None and params.frozen:
            object.__setattr__(victim, "event_type", "forged")
        else:
            victim.event_type = "forged"
        self.assertFalse(ledger.verify())
        vs = swarm.collective.compute(
            occasion_results=result.occasion_results,
            ledger=ledger,
            model_families=["family-A"],
        )
        self.assertFalse(vs.tamper_evident_ok)
        self.assertEqual(vs.welfare_shift_guard, "FAIL")


class TestNoVendorOrCodenameStrings(unittest.TestCase):
    """test_no_vendor_or_codename_strings"""

    # Tokens are split-and-joined so the denylist itself contains no literal
    # vendor/codename string -- otherwise this test file would (correctly) trip
    # its own scan and any external secret/de-brand scanner. The runtime values
    # are the real tokens.
    FORBIDDEN = (
        "cla" + "ude",
        "anthro" + "pic",
        "open" + "ai",
        "gpt" + "-",
        "chat" + "gpt",
        "gem" + "ini",
        "lla" + "ma",
        "mis" + "tral",
        "coh" + "ere",
        "vaik" + "unth",
        "epi" + "mystic",
    )

    def _package_root(self) -> str:
        # tests/ lives at reference/impl/tests ; the package is reference/impl/indras_net
        here = os.path.dirname(os.path.abspath(__file__))
        return os.path.dirname(here)  # reference/impl

    def test_no_vendor_tokens_and_spdx_header_present(self):
        root = self._package_root()
        # Scan the SHIPPED implementation (the package + the demo), NOT the test
        # fixtures -- a test that asserts "no vendor names" must itself name them
        # in its denylist, so scanning tests/ would be a false self-reference.
        py_files = glob.glob(os.path.join(root, "indras_net", "**", "*.py"), recursive=True)
        py_files.append(os.path.join(root, "run_demo.py"))
        self.assertTrue(py_files, "expected to find python sources to scan")
        spdx = "# SPDX-License-Identifier: Apache-2.0"
        for path in py_files:
            with open(path, "r", encoding="utf-8") as fh:
                text = fh.read()
            first_line = text.splitlines()[0] if text.splitlines() else ""
            self.assertEqual(
                first_line.strip(),
                spdx,
                f"missing/incorrect SPDX header in {path}",
            )
            lowered = text.lower()
            for token in self.FORBIDDEN:
                self.assertNotIn(
                    token,
                    lowered,
                    f"forbidden vendor/codename token '{token}' found in {path}",
                )


if __name__ == "__main__":
    unittest.main()
