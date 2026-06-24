# SPDX-License-Identifier: Apache-2.0
"""Phase-4 signing tests.

The stand-in is honest about being origin-shaped (not a real signature); the real Ed25519 path
(optional ``cryptography`` extra) rejects forged and tampered signatures; the signed checkpoint
detects a rewritten head; and the model layer holds no keys. Ed25519 tests skip when the extra is
absent (CI installs it).
"""
from __future__ import annotations

import inspect
import unittest

import indras_net.model as model_mod
import indras_net.model_http as model_http_mod
from indras_net import (
    Ed25519Signer,
    KeyedHashSigner,
    crypto_available,
    sign_checkpoint,
    verify_checkpoint,
)

_HAS_CRYPTO = crypto_available()


class TestKeyedHashStandIn(unittest.TestCase):
    def test_roundtrip_and_wrong_payload(self):
        s = KeyedHashSigner("did:web:indras-net.roles:chitragupta")
        sig = s.sign(b"some bytes")
        self.assertTrue(KeyedHashSigner.verify(s.public_key, b"some bytes", sig))
        self.assertFalse(KeyedHashSigner.verify(s.public_key, b"other bytes", sig))


@unittest.skipUnless(_HAS_CRYPTO, "cryptography extra not installed")
class TestEd25519Real(unittest.TestCase):
    def test_sign_verify_roundtrip(self):
        s = Ed25519Signer()
        sig = s.sign(b"payload")
        self.assertTrue(Ed25519Signer.verify(s.public_key, b"payload", sig))

    def test_forged_signature_rejected(self):
        s = Ed25519Signer()
        self.assertFalse(Ed25519Signer.verify(s.public_key, b"payload", "00" * 64))

    def test_tampered_payload_rejected(self):
        s = Ed25519Signer()
        sig = s.sign(b"payload")
        self.assertFalse(Ed25519Signer.verify(s.public_key, b"TAMPERED", sig))

    def test_wrong_public_key_rejected(self):
        s1, s2 = Ed25519Signer(), Ed25519Signer()
        sig = s1.sign(b"payload")
        self.assertFalse(Ed25519Signer.verify(s2.public_key, b"payload", sig), "another key must not verify")

    def test_private_bytes_roundtrip(self):
        s = Ed25519Signer()
        clone = Ed25519Signer(private_bytes=s.private_bytes())
        self.assertEqual(clone.public_key, s.public_key)
        self.assertTrue(Ed25519Signer.verify(s.public_key, b"x", clone.sign(b"x")))


class TestSignedCheckpoint(unittest.TestCase):
    def test_checkpoint_roundtrip_and_head_change_detected(self):
        signer = KeyedHashSigner("did:web:indras-net.roles:chitragupta")
        cp = sign_checkpoint(signer, 5, "abc123")
        self.assertTrue(verify_checkpoint(cp, 5, "abc123"))
        self.assertFalse(verify_checkpoint(cp, 5, "DIFFERENT"), "a changed head_hash must not verify")
        self.assertFalse(verify_checkpoint(cp, 6, "abc123"), "a changed head_index must not verify")

    @unittest.skipUnless(_HAS_CRYPTO, "cryptography extra not installed")
    def test_real_checkpoint_cannot_be_forged_for_another_head(self):
        signer = Ed25519Signer()
        cp = sign_checkpoint(signer, 10, "headA")
        # an attacker who rewrote the chain to head 'headB' cannot present a valid checkpoint for it
        forged = dict(cp, head_hash="headB")
        self.assertFalse(verify_checkpoint(forged, 10, "headB"))


class TestKeysOutsideModelLayer(unittest.TestCase):
    def test_model_modules_hold_no_signing_keys(self):
        src = inspect.getsource(model_mod) + inspect.getsource(model_http_mod)
        for forbidden in ("signing", "PrivateKey", "private_bytes", "private_key"):
            self.assertNotIn(forbidden, src, "the model layer must not touch signing/keys")


if __name__ == "__main__":
    unittest.main()
