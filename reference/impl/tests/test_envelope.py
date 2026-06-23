# SPDX-License-Identifier: Apache-2.0
"""Envelope tests: CAS determinism, seal/verify integrity, and honesty-FORM checks."""

from __future__ import annotations

import re
import unittest

from indras_net import (
    ActionClass,
    CausalRung,
    EnvelopeKind,
    ReasoningTag,
    Status,
    TrustLabel,
)
from indras_net.canon import cid, jcs_canonicalize, sha256_hex

from . import _helpers as H

CID_RE = re.compile(r"^b[a-z2-7]{20,}$")


class TestCanonAndCid(unittest.TestCase):
    """test_canon_cid_deterministic_and_shape"""

    def test_canon_cid_deterministic_and_shape(self):
        a = {"z": 1, "a": [3, 2, 1], "m": {"y": True, "x": None}}
        # Key order in the source dict must not change the canonical bytes or CID.
        b = {"m": {"x": None, "y": True}, "a": [3, 2, 1], "z": 1}
        self.assertEqual(jcs_canonicalize(a), jcs_canonicalize(b))
        self.assertEqual(cid(a), cid(b))
        self.assertRegex(cid(a), CID_RE)
        # sha256_hex is 64 lower-hex chars.
        self.assertEqual(len(sha256_hex(b"x")), 64)
        self.assertTrue(re.fullmatch(r"[0-9a-f]{64}", sha256_hex(b"x")))
        # Canonical bytes are whitespace-free and key-sorted.
        self.assertNotIn(b" ", jcs_canonicalize(a))


class TestSealAndVerify(unittest.TestCase):
    """test_envelope_seal_and_verify_action_id"""

    def test_seal_sets_ids_and_verifies(self):
        env = H.build_envelope(seal=True)
        self.assertTrue(env.action_id)
        self.assertRegex(env.action_id, CID_RE)
        self.assertTrue(env.provenance.this_hash)
        self.assertEqual(len(env.provenance.this_hash), 64)
        self.assertTrue(env.verify_action_id())

    def test_mutation_breaks_verify(self):
        env = H.build_envelope(seal=True)
        self.assertTrue(env.verify_action_id())
        # Any body mutation must make the recomputed CID diverge (loud failure).
        env.summary = env.summary + " (tampered)"
        self.assertFalse(env.verify_action_id())

    def test_action_id_excluded_from_hashed_body(self):
        env = H.build_envelope(seal=True)
        # content_bytes must not depend on the action_id itself (self-reference guard).
        before = env.content_bytes()
        env.action_id = "bzzzzzzzzzzzzzzzzzzzzzzzzz"
        self.assertEqual(before, env.content_bytes())


class TestHonestyForm(unittest.TestCase):
    """test_honesty_form_false_iterated and test_honesty_form_unwarranted_rung3"""

    def test_honesty_form_ok_on_clean_envelope(self):
        env = H.build_envelope(seal=True)
        ok, reasons = env.honesty_form_ok()
        self.assertTrue(ok, reasons)
        self.assertEqual(reasons, [])

    def test_false_iterated_fails_form(self):
        # ITERATED tag with no maker-checker witness present in the MVP -> 'false-iterated'.
        h = H.honesty(reasoning_tag=ReasoningTag.ITERATED)
        env = H.build_envelope(honesty_block=h, seal=True)
        ok, reasons = env.honesty_form_ok()
        self.assertFalse(ok)
        self.assertIn("false-iterated", reasons)

    def test_unwarranted_rung3_fails_form(self):
        # A PASS envelope self-tagging RUNG3 with no evidence -> 'unwarranted-rung-3'.
        h = H.honesty(causal_rung=CausalRung.RUNG3)
        env = H.build_envelope(status=Status.PASS, honesty_block=h, seal=True)
        ok, reasons = env.honesty_form_ok()
        self.assertFalse(ok)
        self.assertIn("unwarranted-rung-3", reasons)

    def test_over_assertion_fails_form(self):
        # high over-assertion risk paired with an asserted finding -> 'over-assertion'.
        h = H.honesty(over_assertion_risk="high")
        env = H.build_envelope(honesty_block=h, seal=False)
        # attach an asserted finding if the dataclass supports it
        from indras_net import Finding

        env.findings = (
            Finding(claim="X is definitely true", claim_level="assertion"),
        )
        env = env.seal()
        ok, reasons = env.honesty_form_ok()
        self.assertFalse(ok)
        self.assertIn("over-assertion", reasons)


if __name__ == "__main__":
    unittest.main()
