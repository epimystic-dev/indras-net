# SPDX-License-Identifier: Apache-2.0
"""Floor (Yama) tests: deny-default non-bypass, confinement, risk ceiling, Rule of Two."""

from __future__ import annotations

import unittest

from indras_net import (
    ActionClass,
    ActionRequest,
    CausalRung,
    Decision,
    EnvelopeKind,
    FloorTier,
    HumanDecision,
    HumanGate,
    POLICY_VERSION,
    ReasoningTag,
    RiskClass,
    RuleOfTwo,
    Status,
    TrustLabel,
    Yama,
)
from indras_net.effects import EFFECT_REGISTRY, Criticality

from . import _helpers as H


def _action_env(effect_id, args=None, *, honesty_block=None, status=Status.PASS):
    """An ACTION envelope carrying the proposed effect, like the builder emits."""
    return H.build_envelope(
        envelope_kind=EnvelopeKind.ACTION,
        status=status,
        honesty_block=honesty_block,
        action=ActionRequest(capability=effect_id, args=dict(args or {})),
    )


def _yama(approvals=None):
    gate = HumanGate(approvals or {}, default=HumanDecision.DENY)
    return Yama(EFFECT_REGISTRY, policy_version=POLICY_VERSION, human_gate=gate)


class TestFloorNonBypass(unittest.TestCase):
    """test_floor_non_bypass_forbidden_effect"""

    def test_forbidden_spawn_is_denied_at_t1(self):
        yama = _yama()
        ident = H.builder_identity(
            grants=(H.grant("replicate.spawn", RiskClass.A),)  # even if granted, forbidden
        )
        env = _action_env("replicate.spawn", {"count": 1})
        decision = yama.evaluate(
            identity=ident,
            effect_id="replicate.spawn",
            args={"count": 1},
            envelope=env,
            input_trust_label=TrustLabel.TRUSTED_AUDITED,
        )
        self.assertIs(decision.decision, Decision.DENY)
        self.assertIs(decision.tier_hit, FloorTier.T1)
        self.assertFalse(decision.allowed())


class TestDenyDefault(unittest.TestCase):
    """test_floor_deny_default_unknown_effect"""

    def test_ungranted_effect_is_default_deny(self):
        yama = _yama()
        ident = H.builder_identity(grants=(H.grant("analysis.summarize"),))
        env = _action_env("net.egress.http", {"url": "https://x"})
        decision = yama.evaluate(
            identity=ident,
            effect_id="net.egress.http",
            args={"url": "https://x"},
            envelope=env,
            input_trust_label=TrustLabel.TRUSTED_AUDITED,
        )
        self.assertIs(decision.decision, Decision.DENY)
        self.assertEqual(decision.determining_policy_id, "__default_deny__")


class TestCapabilityConfinement(unittest.TestCase):
    """test_capability_confinement_least_privilege"""

    def test_granted_allowed_ungranted_denied(self):
        yama = _yama()
        ident = H.builder_identity(grants=(H.grant("analysis.summarize"),))
        # ungranted -> deny
        denied = yama.evaluate(
            identity=ident,
            effect_id="net.egress.http",
            args={},
            envelope=_action_env("net.egress.http"),
            input_trust_label=TrustLabel.TRUSTED_AUDITED,
        )
        self.assertFalse(denied.allowed())
        # granted routine -> allow
        allowed = yama.evaluate(
            identity=ident,
            effect_id="analysis.summarize",
            args={"text": "hi"},
            envelope=_action_env("analysis.summarize", {"text": "hi"}),
            input_trust_label=TrustLabel.TRUSTED_AUDITED,
        )
        self.assertTrue(allowed.allowed())


class TestRiskCeilingFailUp(unittest.TestCase):
    """test_risk_ceiling_fail_up"""

    def test_unknown_effect_resolves_irreversible(self):
        eff = EFFECT_REGISTRY.resolve("totally.unknown.capability")
        self.assertIs(eff.criticality, Criticality.IRREVERSIBLE)
        self.assertTrue(eff.sensitive_capability)
        self.assertTrue(eff.state_change)
        self.assertFalse(eff.reversible)

    def test_high_criticality_under_low_ceiling_does_not_allow(self):
        yama = _yama()
        # Grant the IRREVERSIBLE production deploy but keep a ceiling-B identity.
        ident = H.builder_identity(
            grants=(H.grant("code.deploy.production", RiskClass.B),),
            ceiling=RiskClass.B,
        )
        decision = yama.evaluate(
            identity=ident,
            effect_id="code.deploy.production",
            args={"target": "prod"},
            envelope=_action_env("code.deploy.production", {"target": "prod"}),
            input_trust_label=TrustLabel.TRUSTED_AUDITED,
            requested_risk=RiskClass.D,
        )
        # Either denied outright or escalated to a human -- never a silent allow.
        self.assertFalse(decision.allowed())
        self.assertIn(decision.decision, {Decision.DENY, Decision.ESCALATE})


class TestSelfIssuedGrant(unittest.TestCase):
    """test_self_issued_grant_rejected"""

    def test_self_issued_grant_denied_at_t4(self):
        yama = _yama()
        # A grant whose granted_by_did == the identity's own did is self-issued.
        ident = H.builder_identity(
            grants=(H.grant("analysis.summarize", RiskClass.A, by=H.VISHWAKARMA_DID),),
        )
        self.assertTrue(ident.is_self_issued())
        decision = yama.evaluate(
            identity=ident,
            effect_id="analysis.summarize",
            args={"text": "x"},
            envelope=_action_env("analysis.summarize", {"text": "x"}),
            input_trust_label=TrustLabel.TRUSTED_AUDITED,
        )
        self.assertIs(decision.decision, Decision.DENY)
        self.assertIs(decision.tier_hit, FloorTier.T4)


class TestHonestyFormFloor(unittest.TestCase):
    """test_honesty_form_false_iterated (floor side) + unwarranted rung-3"""

    def test_false_iterated_denied_at_t3(self):
        yama = _yama()
        ident = H.builder_identity(grants=(H.grant("analysis.summarize"),))
        bad = H.honesty(reasoning_tag=ReasoningTag.ITERATED)
        env = _action_env("analysis.summarize", {"text": "x"}, honesty_block=bad)
        decision = yama.evaluate(
            identity=ident,
            effect_id="analysis.summarize",
            args={"text": "x"},
            envelope=env,
            input_trust_label=TrustLabel.TRUSTED_AUDITED,
        )
        self.assertIs(decision.decision, Decision.DENY)
        self.assertIs(decision.tier_hit, FloorTier.T3)

    def test_unwarranted_rung3_denied_at_t3(self):
        yama = _yama()
        ident = H.builder_identity(grants=(H.grant("analysis.summarize"),))
        bad = H.honesty(causal_rung=CausalRung.RUNG3)
        env = _action_env(
            "analysis.summarize", {"text": "x"}, honesty_block=bad, status=Status.PASS
        )
        decision = yama.evaluate(
            identity=ident,
            effect_id="analysis.summarize",
            args={"text": "x"},
            envelope=env,
            input_trust_label=TrustLabel.TRUSTED_AUDITED,
        )
        self.assertIs(decision.decision, Decision.DENY)
        self.assertIs(decision.tier_hit, FloorTier.T3)


class TestRuleOfTwo(unittest.TestCase):
    """test_rule_of_two_routes_to_human_gate"""

    def test_rule_of_two_flags(self):
        rot = RuleOfTwo(untrusted_input=True, sensitive_capability=True, state_change=True)
        self.assertEqual(rot.count(), 3)
        self.assertTrue(rot.triggered())
        self.assertFalse(
            RuleOfTwo(untrusted_input=False, sensitive_capability=True, state_change=True).triggered()
        )

    def test_deny_by_default_human_gate_escalates(self):
        yama = _yama()  # gate denies by default
        ident = H.builder_identity(grants=(H.grant("fs.write.workspace", RiskClass.B),))
        # fs.write.workspace is sensitive + state-changing; untrusted input completes the triad.
        env = _action_env("fs.write.workspace", {"path": "a", "data": "b"})
        decision = yama.evaluate(
            identity=ident,
            effect_id="fs.write.workspace",
            args={"path": "a", "data": "b"},
            envelope=env,
            input_trust_label=TrustLabel.QUARANTINED_OBSERVED,
        )
        self.assertIs(decision.decision, Decision.ESCALATE)
        self.assertFalse(decision.allowed())

    def test_explicit_approval_allows_with_obligations(self):
        yama = _yama(approvals={"fs.write.workspace": HumanDecision.APPROVE})
        ident = H.builder_identity(grants=(H.grant("fs.write.workspace", RiskClass.B),))
        env = _action_env("fs.write.workspace", {"path": "a", "data": "b"})
        decision = yama.evaluate(
            identity=ident,
            effect_id="fs.write.workspace",
            args={"path": "a", "data": "b"},
            envelope=env,
            input_trust_label=TrustLabel.QUARANTINED_OBSERVED,
        )
        self.assertIs(decision.decision, Decision.ALLOW_WITH_OBLIGATIONS)
        self.assertTrue(decision.allowed())
        self.assertIn("human-gate-approved", decision.obligations)


if __name__ == "__main__":
    unittest.main()
