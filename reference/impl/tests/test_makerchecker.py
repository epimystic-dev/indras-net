# SPDX-License-Identifier: Apache-2.0
"""Maker-checker tests: an independent, different-family checker (Narasimha) makes ITERATED earnable.

A CONCUR lets the orchestrator -- never the maker -- tag the output ITERATED with an audited
witness; a DISSENT holds the action; an ITERATED claim with no witness fails honesty-FORM.
"""
from __future__ import annotations

import unittest

from indras_net import ReasoningTag

from . import _helpers as H


class TestMakerChecker(unittest.TestCase):
    def test_concur_earns_iterated_with_witness(self):
        scripted = {"summarize": H.mock_result(effect_id="analysis.summarize", args={"text": "x"}, causal_rung=1)}
        swarm, ledger = H.make_swarm(scripted=scripted, with_checker=True)
        result = swarm.run("summarize", {"input_trust_label": "trusted:audited"}, maker_checker=True)

        executed = [o for o in result.occasion_results if o.executed]
        self.assertTrue(executed, "the granted routine effect should execute after a concurring check")
        env = executed[0].envelope
        self.assertEqual(env.honesty.reasoning_tag, ReasoningTag.ITERATED)
        self.assertTrue(env.honesty.maker_checker_witness, "concurrence must carry a maker-checker witness")
        ok, reasons = env.honesty_form_ok()
        self.assertTrue(ok, f"witnessed ITERATED must pass honesty-FORM; got {reasons}")

        # an INDEPENDENT check-verdict leaf, authored by the checker (a DIFFERENT DID than the maker)
        verdicts = [lf for lf in ledger.leaves() if lf.event_type.startswith("check-verdict:")]
        self.assertTrue(verdicts)
        self.assertEqual(verdicts[-1].signer_did, H.NARASIMHA_DID)
        self.assertNotEqual(verdicts[-1].signer_did, swarm.builder.identity.did)
        self.assertTrue(ledger.verify())

    def test_dissent_holds_the_action(self):
        # code.deploy.production is IRREVERSIBLE and carries no evidence -> the checker dissents.
        scripted = {"deploy": H.mock_result(effect_id="code.deploy.production", args={"target": "prod"})}
        swarm, ledger = H.make_swarm(scripted=scripted, with_checker=True)
        result = swarm.run("deploy", {"input_trust_label": "trusted:audited"}, maker_checker=True)

        self.assertFalse(any(o.executed for o in result.occasion_results), "a dissented action must never execute")
        verdicts = [lf for lf in ledger.leaves() if lf.event_type.startswith("check-verdict:")]
        self.assertTrue(verdicts)
        self.assertTrue(verdicts[-1].event_type.endswith("FAIL"), "checker should dissent on irreversible-without-evidence")
        self.assertTrue(ledger.verify())

    def test_checker_is_a_different_model_family(self):
        swarm, _ = H.make_swarm(scripted={}, with_checker=True)
        self.assertIsNotNone(swarm.checker)
        self.assertNotEqual(
            swarm.checker.identity.model_family,
            swarm.builder.identity.model_family,
            "the checker must be a different model family (decorrelated errors)",
        )

    def test_iterated_requires_a_witness(self):
        # ITERATED with no witness -> false-iterated
        bare = H.build_envelope(honesty_block=H.honesty(reasoning_tag=ReasoningTag.ITERATED))
        ok, reasons = bare.honesty_form_ok()
        self.assertFalse(ok)
        self.assertIn("false-iterated", reasons)
        # the orchestrator-only re-seal carries the witness -> passes
        witnessed = H.build_envelope().with_iterated_witness("01J-checker-record-id")
        ok2, reasons2 = witnessed.honesty_form_ok()
        self.assertTrue(ok2, f"witnessed ITERATED should pass; got {reasons2}")
        self.assertEqual(witnessed.honesty.reasoning_tag, ReasoningTag.ITERATED)
        self.assertTrue(witnessed.verify_action_id(), "the re-sealed witnessed envelope must verify")


if __name__ == "__main__":
    unittest.main()
