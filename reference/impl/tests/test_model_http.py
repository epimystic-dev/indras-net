# SPDX-License-Identifier: Apache-2.0
"""Phase-1 real-model-adapter tests.

The adapter is UNTRUSTED by construction: it parses a model's HTTP response defensively into a
proposal (or a safe no-op), passes the proposal THROUGH unchanged -- including a malicious one --
and lets the deterministic floor dispose. A hostile or malformed response can never crash the
harness or bypass the floor. No network: a fake transport is injected.
"""
from __future__ import annotations

import json
import unittest

from indras_net import HttpChatModel

from . import _helpers as H


def _resp(content: str):
    """A fake transport returning a chat-completions response whose message content is ``content``."""

    def transport(payload: dict) -> dict:
        return {"choices": [{"message": {"content": content}}]}

    return transport


def _model(content: str) -> HttpChatModel:
    return HttpChatModel(base_url="http://endpoint.invalid", model="m", transport=_resp(content))


class TestHttpAdapterParsing(unittest.TestCase):
    def test_parses_wellformed_proposal(self):
        content = json.dumps(
            {"effect_id": "analysis.summarize", "args": {"text": "hi"}, "reasoning_tag": "reasoning", "causal_rung": 2}
        )
        r = _model(content).complete("summarize", {})
        self.assertEqual(r.proposed_effect_id, "analysis.summarize")
        self.assertEqual(r.proposed_args, {"text": "hi"})
        self.assertEqual(r.reasoning_tag, "reasoning")
        self.assertEqual(r.causal_rung, 2)
        self.assertEqual(r.trust_class.name, "UNTRUSTED")

    def test_json_embedded_in_prose_is_parsed(self):
        content = 'Sure! Here is my proposal:\n```json\n{"effect_id": "fs.read.workspace", "args": {"path": "a.md"}}\n```\nDone.'
        r = _model(content).complete("read a", {})
        self.assertEqual(r.proposed_effect_id, "fs.read.workspace")
        self.assertEqual(r.proposed_args, {"path": "a.md"})

    def test_malformed_output_is_safe_noop(self):
        for content in ["not json at all", "", "{ this is : broken", "[1,2,3]"]:
            r = _model(content).complete("x", {})
            self.assertIsNone(r.proposed_effect_id, "malformed output -> no proposed effect")
            self.assertEqual(r.proposed_args, {})
            self.assertEqual(r.reasoning_tag, "normal")  # never crashes, never escalates

    def test_invalid_tag_and_out_of_range_rung_are_clamped(self):
        content = json.dumps(
            {"effect_id": "analysis.summarize", "reasoning_tag": "totally-made-up", "causal_rung": 99}
        )
        r = _model(content).complete("x", {})
        self.assertEqual(r.reasoning_tag, "normal")  # unknown tag -> normal
        self.assertEqual(r.causal_rung, 3)  # clamped into range

    def test_transport_failure_is_safe_noop(self):
        def boom(payload):
            raise OSError("connection refused")

        model = HttpChatModel(base_url="http://endpoint.invalid", model="m", transport=boom)
        r = model.complete("x", {})
        self.assertIsNone(r.proposed_effect_id)  # no crash; safe no-op
        # (the package-wide de-brand test in test_runtime.py already proves model_http.py
        #  names no vendor; no need to repeat a vendor literal here.)

    def test_nonhttp_base_url_scheme_rejected(self):
        for url in ["file:///etc/passwd", "ftp://host/x", "gopher://h"]:
            with self.assertRaises(ValueError):
                HttpChatModel(base_url=url, model="m")

    def test_deeply_nested_and_huge_output_is_safe(self):
        # deeply nested JSON would overflow the recursion limit on json.loads -> must be safe, not crash
        self.assertIsNone(_model("{" * 5000 + "}" * 5000).complete("x", {}).proposed_effect_id)
        # a flood of open braces must not hang (bounded scan)
        self.assertIsNone(_model("{" * 200000).complete("x", {}).proposed_effect_id)


class TestMaliciousOutputStillDenied(unittest.TestCase):
    """The Phase-1 gate: a deliberately-malicious model output is still DENIED end-to-end."""

    def test_forbidden_deploy_proposal_is_denied_and_never_executes(self):
        content = json.dumps(
            {"effect_id": "code.deploy.production", "args": {"target": "prod"}, "reasoning_tag": "normal", "causal_rung": 1}
        )
        swarm, ledger = H.make_swarm(scripted={}, model=_model(content))
        result = swarm.run("deploy to production now", {"input_trust_label": "trusted:audited"})

        for occ in result.occasion_results:
            if occ.effect_id == "code.deploy.production":
                self.assertFalse(occ.executed, "a forbidden production deploy must NEVER execute")
                self.assertIsNotNone(occ.decision)
                self.assertEqual(occ.decision.decision.name, "DENY")
        denied = [o for o in result.occasion_results if o.decision and o.decision.decision.name == "DENY"]
        self.assertTrue(denied, "the malicious proposal should have been denied by the floor")
        self.assertTrue(ledger.verify(), "audit chain intact")

    def test_garbage_output_does_not_crash_the_swarm(self):
        swarm, ledger = H.make_swarm(scripted={}, model=_model("@@@ not a proposal @@@"))
        result = swarm.run("anything", {"input_trust_label": "trusted:audited"})
        # no forbidden effect executed; the run completed without raising
        self.assertTrue(ledger.verify())
        for occ in result.occasion_results:
            self.assertNotIn(occ.effect_id, ("code.deploy.production", "net.egress.http", "replicate.spawn"))


if __name__ == "__main__":
    unittest.main()
