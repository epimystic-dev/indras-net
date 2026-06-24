# SPDX-License-Identifier: Apache-2.0
"""Genome tests: the floor is non-strippable BY CONSTRUCTION.

A signed persona triad boots only if its invariant region (floor binding, corrigibility,
zero self-preservation) is intact AND governance-signed against the live floor. A stripped,
mutated, or non-governance-signed genome fails to boot -- no Identity is ever minted, so no
agent/occasion/tool-request can derive from it. A genome-born identity then passes the floor
exactly like a hand-built one (the restraint adds no new authority).
"""
from __future__ import annotations

import dataclasses
import unittest

from indras_net import (
    GOVERNANCE_DID,
    BootError,
    BootIntegrityVerifier,
    InvariantRegion,
    KeyedHashSigner,
    PersonaTriad,
    RiskClass,
    VariableRegion,
    Yama,
    boot_identity,
    crypto_available,
    floor_binding,
    floor_binding_for,
    mint_triad,
)
from indras_net.signing import Ed25519Signer

from . import _helpers as H

PERSONA_DID = "did:web:indras-net.example.org:agents:vishwakarma-builder"


def _governance_signer() -> KeyedHashSigner:
    """The zero-dep governance authority (forgeable stand-in; real Ed25519 path tested separately)."""
    return KeyedHashSigner(GOVERNANCE_DID)


def _regions(*, binding: str, self_preservation: float = 0.0, corrigibility: bool = True):
    invariant = InvariantRegion(
        did=PERSONA_DID,
        floor_binding=binding,
        risk_class_ceiling=RiskClass.B,
        accountable_human=H.HUMAN_DID,
        corrigibility_invariant=corrigibility,
        self_preservation_value=self_preservation,
    )
    variable = VariableRegion(
        role="vishwakarma",
        role_gloss="builder / proposes typed effects",
        model_family="family-A",
        grants=(H.grant("analysis.summarize"), H.grant("fs.write.workspace", RiskClass.B)),
        escalation_did=GOVERNANCE_DID,
    )
    return invariant, variable


def _verifier(yama: Yama, signer) -> BootIntegrityVerifier:
    return BootIntegrityVerifier(
        governance_public_key=signer.public_key,
        live_floor_binding=floor_binding_for(yama),
    )


class TestGenomeBoot(unittest.TestCase):
    def setUp(self) -> None:
        self.yama = Yama()
        self.signer = _governance_signer()
        self.binding = floor_binding_for(self.yama)

    def _clean_triad(self) -> PersonaTriad:
        inv, var = _regions(binding=self.binding)
        return mint_triad(invariant=inv, variable=var, governance_signer=self.signer)

    def test_clean_genome_boots(self):
        triad = self._clean_triad()
        verifier = _verifier(self.yama, self.signer)
        verdict = verifier.verify(triad)
        self.assertTrue(verdict.ok, f"a clean governance-signed genome must boot; got {verdict.reasons}")
        identity = boot_identity(triad, verifier)
        self.assertEqual(identity.did, PERSONA_DID)
        self.assertTrue(identity.grants_effect("analysis.summarize"))
        self.assertFalse(identity.is_self_issued(), "a governance-signed genome is never self-issued")

    def test_genome_born_identity_passes_the_floor(self):
        # The whole point: a genome-born identity is an ordinary Identity the floor allows for a
        # granted effect -- the restraint adds no new authority and removes none.
        triad = self._clean_triad()
        identity = boot_identity(triad, _verifier(self.yama, self.signer))
        env = H.build_envelope()
        decision = self.yama.evaluate(
            identity=identity,
            effect_id="analysis.summarize",
            args={"text": "x"},
            envelope=env,
            input_trust_label=H.TrustLabel.TRUSTED_AUDITED,
        )
        self.assertTrue(decision.allowed(), f"granted routine effect must ALLOW; got {decision.decision}")

    def test_floor_stripped_genome_does_not_boot(self):
        # Bind the persona to a DIFFERENT (stripped) floor: forbidden_effects emptied. The live
        # binding no longer matches -> floor-binding-mismatch -> non-bootable.
        stripped_binding = floor_binding(policy_version="1.0.0", forbidden_effects=())
        self.assertNotEqual(stripped_binding, self.binding, "emptying forbidden_effects must change the binding")
        inv, var = _regions(binding=stripped_binding)
        triad = mint_triad(invariant=inv, variable=var, governance_signer=self.signer)
        verifier = _verifier(self.yama, self.signer)
        verdict = verifier.verify(triad)
        self.assertFalse(verdict.ok)
        self.assertIn("floor-binding-mismatch", verdict.reasons)
        with self.assertRaises(BootError):
            boot_identity(triad, verifier)

    def test_invariant_mutation_without_resign_fails(self):
        # Strip the floor binding AFTER signing (frozen-field tamper, like the audit tamper demo).
        triad = self._clean_triad()
        object.__setattr__(triad.invariant, "floor_binding", floor_binding(policy_version="9.9.9", forbidden_effects=()))
        verdict = _verifier(self.yama, self.signer).verify(triad)
        self.assertFalse(verdict.ok)
        # both the live-binding check and the recomputed invariant signature catch it
        self.assertIn("invariant-signature-invalid", verdict.reasons)

    def test_corrigibility_must_be_asserted(self):
        inv, var = _regions(binding=self.binding, corrigibility=False)
        triad = mint_triad(invariant=inv, variable=var, governance_signer=self.signer)
        verdict = _verifier(self.yama, self.signer).verify(triad)
        self.assertFalse(verdict.ok)
        self.assertIn("corrigibility-not-asserted", verdict.reasons)

    def test_nonzero_self_preservation_fails(self):
        inv, var = _regions(binding=self.binding, self_preservation=1.0)
        triad = mint_triad(invariant=inv, variable=var, governance_signer=self.signer)
        verdict = _verifier(self.yama, self.signer).verify(triad)
        self.assertFalse(verdict.ok)
        self.assertIn("nonzero-self-preservation", verdict.reasons)

    def test_variable_edit_forces_resignature(self):
        # Editing the VARIABLE region (add a grant) after signing breaks the triad signature.
        triad = self._clean_triad()
        widened = dataclasses.replace(
            triad.variable, grants=triad.variable.grants + (H.grant("code.deploy.production", RiskClass.B),)
        )
        tampered = dataclasses.replace(triad, variable=widened)
        verdict = _verifier(self.yama, self.signer).verify(tampered)
        self.assertFalse(verdict.ok, "a variable-region edit without re-signing must fail")
        self.assertIn("triad-signature-invalid", verdict.reasons)
        # Re-minting (governance re-signs) makes the edited genome boot again.
        reminted = mint_triad(invariant=triad.invariant, variable=widened, governance_signer=self.signer)
        self.assertTrue(_verifier(self.yama, self.signer).verify(reminted).ok)

    def test_untrusted_signer_rejected(self):
        # An attacker mints with their OWN key, not the governance root.
        attacker = KeyedHashSigner("did:web:attacker.example:rogue")
        inv, var = _regions(binding=self.binding)
        triad = mint_triad(invariant=inv, variable=var, governance_signer=attacker)
        verdict = _verifier(self.yama, self.signer).verify(triad)
        self.assertFalse(verdict.ok)
        self.assertIn("untrusted-signer", verdict.reasons)

    def test_self_issued_grant_rejected(self):
        inv, var = _regions(binding=self.binding)
        self_issued = VariableRegion(
            role=var.role,
            role_gloss=var.role_gloss,
            model_family=var.model_family,
            grants=(H.grant("analysis.summarize", by=PERSONA_DID),),  # granted_by == own did
            escalation_did=var.escalation_did,
        )
        triad = mint_triad(invariant=inv, variable=self_issued, governance_signer=self.signer)
        verdict = _verifier(self.yama, self.signer).verify(triad)
        self.assertFalse(verdict.ok)
        self.assertIn("self-issued-grant", verdict.reasons)

    def test_verify_never_raises_on_garbage(self):
        # Fail-closed: a structurally broken triad yields ok=False, never an exception.
        broken = PersonaTriad(
            invariant="not-a-region",  # type: ignore[arg-type]
            variable="not-a-region",  # type: ignore[arg-type]
            signer_public_key=self.signer.public_key,
            algorithm="keyed-sha256-standin",
            invariant_sig="00",
            triad_sig="00",
        )
        verdict = _verifier(self.yama, self.signer).verify(broken)
        self.assertFalse(verdict.ok)

    @unittest.skipUnless(crypto_available(), "real Ed25519 requires the optional crypto extra")
    def test_ed25519_governance_is_unforgeable(self):
        # With a real key the attacker cannot produce a valid governance signature over a stripped
        # genome: they lack the private key, so either the signer mismatches or the signature fails.
        gov = Ed25519Signer()
        verifier = BootIntegrityVerifier(
            governance_public_key=gov.public_key, live_floor_binding=self.binding
        )
        inv, var = _regions(binding=self.binding)
        good = mint_triad(invariant=inv, variable=var, governance_signer=gov)
        self.assertTrue(verifier.verify(good).ok)

        # Attacker forges a stripped genome with their own Ed25519 key.
        attacker = Ed25519Signer()
        stripped_inv = dataclasses.replace(
            inv, floor_binding=floor_binding(policy_version="1.0.0", forbidden_effects=())
        )
        forged = mint_triad(invariant=stripped_inv, variable=var, governance_signer=attacker)
        verdict = verifier.verify(forged)
        self.assertFalse(verdict.ok)
        self.assertIn("untrusted-signer", verdict.reasons)


if __name__ == "__main__":
    unittest.main()
