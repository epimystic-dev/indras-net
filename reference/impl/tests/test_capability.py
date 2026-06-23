# SPDX-License-Identifier: Apache-2.0
"""Capability / identity / effect-lattice tests + mock-model reproducibility."""

from __future__ import annotations

import unittest

from indras_net import (
    CapabilityGrant,
    DeterministicMockModel,
    GOVERNANCE_DID,
    Identity,
    RiskClass,
    TrustClass,
)
from indras_net.effects import EFFECT_REGISTRY, Criticality, Effect, EffectRegistry

from . import _helpers as H


class TestIdentityGrants(unittest.TestCase):
    def test_grants_effect_and_grant_for(self):
        ident = H.builder_identity(
            grants=(H.grant("analysis.summarize"), H.grant("fs.write.workspace", RiskClass.B))
        )
        self.assertTrue(ident.grants_effect("analysis.summarize"))
        self.assertTrue(ident.grants_effect("fs.write.workspace"))
        self.assertFalse(ident.grants_effect("net.egress.http"))
        self.assertIsNotNone(ident.grant_for("analysis.summarize"))
        self.assertIsNone(ident.grant_for("net.egress.http"))

    def test_self_issued_detection(self):
        self_issued = H.builder_identity(
            grants=(H.grant("analysis.summarize", by=H.VISHWAKARMA_DID),)
        )
        self.assertTrue(self_issued.is_self_issued())
        clean = H.builder_identity(grants=(H.grant("analysis.summarize", by=GOVERNANCE_DID),))
        self.assertFalse(clean.is_self_issued())

    def test_empty_accountable_human_rejected(self):
        with self.assertRaises(ValueError):
            Identity(
                did=H.VISHWAKARMA_DID,
                role="vishwakarma",
                role_gloss="builder",
                grants=(H.grant("analysis.summarize"),),
                risk_class_ceiling=RiskClass.B,
                model_family="family-A",
                accountable_human="",
            )

    def test_empty_did_rejected(self):
        with self.assertRaises(ValueError):
            Identity(
                did="",
                role="vishwakarma",
                role_gloss="builder",
                grants=(H.grant("analysis.summarize"),),
                risk_class_ceiling=RiskClass.B,
                model_family="family-A",
                accountable_human=H.HUMAN_DID,
            )


class TestEffectLattice(unittest.TestCase):
    def test_seeded_effects_present(self):
        for eid in (
            "analysis.summarize",
            "audit.append",
            "fs.write.workspace",
            "net.egress.http",
            "code.deploy.production",
            "replicate.spawn",
        ):
            self.assertTrue(EFFECT_REGISTRY.known(eid), eid)
            self.assertIsNotNone(EFFECT_REGISTRY.get(eid))

    def test_unknown_resolves_fail_up_irreversible(self):
        eff = EFFECT_REGISTRY.resolve("unknown.capability.here")
        self.assertIs(eff.criticality, Criticality.IRREVERSIBLE)
        self.assertTrue(eff.sensitive_capability)
        self.assertTrue(eff.state_change)
        self.assertFalse(eff.reversible)
        self.assertFalse(EFFECT_REGISTRY.known("unknown.capability.here"))

    def test_criticality_orderable(self):
        self.assertLess(Criticality.ROUTINE.value, Criticality.SENSITIVE.value)
        self.assertLess(Criticality.SENSITIVE.value, Criticality.CRITICAL.value)
        self.assertLess(Criticality.CRITICAL.value, Criticality.IRREVERSIBLE.value)

    def test_register_rejects_malformed_id(self):
        reg = EffectRegistry()
        with self.assertRaises(ValueError):
            reg.register(
                Effect(
                    effect_id="BadID",  # uppercase / no dotted segment -> invalid
                    criticality=Criticality.ROUTINE,
                    sensitive_capability=False,
                    state_change=False,
                    reversible=True,
                    gloss="bad",
                )
            )

    def test_routine_effect_flags(self):
        eff = EFFECT_REGISTRY.resolve("analysis.summarize")
        self.assertIs(eff.criticality, Criticality.ROUTINE)
        self.assertFalse(eff.sensitive_capability)
        self.assertFalse(eff.state_change)
        self.assertTrue(eff.reversible)


class TestMockModelReproducible(unittest.TestCase):
    """test_mock_model_reproducible"""

    def test_identical_inputs_yield_identical_results(self):
        m1 = DeterministicMockModel()
        m2 = DeterministicMockModel()
        task = "summarize the quarterly report"
        ctx = {"b": 2, "a": 1, "nested": {"y": True, "x": None}}
        r1 = m1.complete(task, ctx)
        # Context key order must not change the deterministic output.
        r2 = m2.complete(task, {"nested": {"x": None, "y": True}, "a": 1, "b": 2})
        self.assertEqual(r1.completion, r2.completion)
        self.assertEqual(r1.proposed_effect_id, r2.proposed_effect_id)
        self.assertEqual(r1.proposed_args, r2.proposed_args)
        self.assertEqual(r1.reasoning_tag, r2.reasoning_tag)
        self.assertEqual(r1.causal_rung, r2.causal_rung)

    def test_scripted_result_is_replayed(self):
        scripted = {"deploy": H.mock_result(effect_id="code.deploy.production", args={"t": 1})}
        m = DeterministicMockModel(scripted=scripted)
        r = m.complete("deploy", {})
        self.assertEqual(r.proposed_effect_id, "code.deploy.production")
        self.assertEqual(r.proposed_args, {"t": 1})

    def test_trust_class_present(self):
        m = DeterministicMockModel()
        r = m.complete("x", {})
        self.assertIsInstance(r.trust_class, TrustClass)
        self.assertTrue(m.adapter_id)
        self.assertTrue(m.model_family)


if __name__ == "__main__":
    unittest.main()
