# SPDX-License-Identifier: Apache-2.0
"""Real cryptographic signing (Phase 4) — an optional extra over the zero-dep stand-in.

Origin/integrity can be a real detached signature, not a keyed hash. Two implementations behind
one interface:

* ``KeyedHashSigner`` — the zero-dep stand-in: ``sig = SHA-256(key_id || payload)``. It is
  deterministic and binds a payload to a key_id, but it has **no secret**, so it is **FORGEABLE**
  by anyone who knows the key_id. It is origin-*shaped*, **not** a real signature; use it only on
  the offline/zero-dep path.
* ``Ed25519Signer`` — a real Ed25519 detached signature (requires the optional ``cryptography``
  extra: ``pip install indras-net[crypto]``). A forged or tampered signature is rejected.

**Keys live in the signer object, OUTSIDE the model layer.** Nothing in ``model.py`` /
``model_http.py`` imports this module, so a compromised model cannot reach a private key.

The ``sign_checkpoint`` / ``verify_checkpoint`` helpers sign a ledger's *head* (index + head_hash).
With a real Ed25519 key this closes the Phase-3 whole-chain-rewrite residual: a rewritten ledger's
new head will not match the signed checkpoint, and the attacker cannot re-sign without the private
key. With the stand-in it is origin-shaped only (no rewrite protection).
"""
from __future__ import annotations

import hashlib
import hmac
import typing


class SigningError(Exception):
    """Raised when a signing backend is unavailable or a key/signature is malformed."""


def _consteq(a: str, b: str) -> bool:
    return hmac.compare_digest(str(a), str(b))


class KeyedHashSigner:
    """Zero-dep ORIGIN stand-in. Deterministic, FORGEABLE, NOT a real signature."""

    algorithm = "keyed-sha256-standin"

    def __init__(self, key_id: str) -> None:
        self.key_id = str(key_id)
        self.public_key = self.key_id  # there is no secret; the "public key" is just the id

    def sign(self, payload: bytes) -> str:
        return hashlib.sha256(self.key_id.encode("utf-8") + b"." + bytes(payload)).hexdigest()

    @staticmethod
    def verify(public_key: str, payload: bytes, signature: str) -> bool:
        expected = hashlib.sha256(str(public_key).encode("utf-8") + b"." + bytes(payload)).hexdigest()
        return _consteq(expected, signature)


def _ed25519():
    """Import the Ed25519 primitives, or raise a clear SigningError if the extra is absent."""
    try:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives.asymmetric import ed25519
        from cryptography.hazmat.primitives import serialization

        return ed25519, serialization, InvalidSignature
    except Exception as exc:  # noqa: BLE001 - ImportError or a backend init error
        raise SigningError(
            "Ed25519 signing requires the optional 'cryptography' extra: pip install indras-net[crypto]"
        ) from exc


def crypto_available() -> bool:
    """True iff a real signing backend (the ``cryptography`` extra) is importable."""
    try:
        _ed25519()
        return True
    except SigningError:
        return False


class Ed25519Signer:
    """A real Ed25519 detached signer. The private key lives here, outside the model layer."""

    algorithm = "ed25519"

    def __init__(self, private_bytes: typing.Optional[bytes] = None) -> None:
        ed25519, serialization, _ = _ed25519()
        self._key = (
            ed25519.Ed25519PrivateKey.from_private_bytes(bytes(private_bytes))
            if private_bytes is not None
            else ed25519.Ed25519PrivateKey.generate()
        )
        self.public_key = (
            self._key.public_key()
            .public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)
            .hex()
        )

    def private_bytes(self) -> bytes:
        """The raw private key (32 bytes). Keep this off the model side and out of the audit log."""
        _, serialization, _ = _ed25519()
        return self._key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption(),
        )

    def sign(self, payload: bytes) -> str:
        return self._key.sign(bytes(payload)).hex()

    @staticmethod
    def verify(public_key: str, payload: bytes, signature: str) -> bool:
        ed25519, _, InvalidSignature = _ed25519()
        try:
            pub = ed25519.Ed25519PublicKey.from_public_bytes(bytes.fromhex(str(public_key)))
            pub.verify(bytes.fromhex(str(signature)), bytes(payload))
            return True
        except (InvalidSignature, ValueError, TypeError):
            return False


# -- signed checkpoint over a ledger head (closes the Phase-3 rewrite residual with real crypto) --

def _checkpoint_payload(head_index: int, head_hash: str) -> bytes:
    return ("checkpoint.%d.%s" % (int(head_index), str(head_hash))).encode("utf-8")


def sign_checkpoint(signer, head_index: int, head_hash: str) -> dict:
    """Produce a signed checkpoint over a ledger's head (index + head_hash)."""
    return {
        "algorithm": signer.algorithm,
        "head_index": int(head_index),
        "head_hash": str(head_hash),
        "public_key": signer.public_key,
        "signature": signer.sign(_checkpoint_payload(head_index, head_hash)),
    }


def verify_checkpoint(checkpoint: dict, head_index: int, head_hash: str) -> bool:
    """True iff ``checkpoint`` is a valid signature over exactly this head. Never raises."""
    if not isinstance(checkpoint, dict):
        return False
    if checkpoint.get("head_index") != int(head_index) or checkpoint.get("head_hash") != str(head_hash):
        return False
    backend = Ed25519Signer if checkpoint.get("algorithm") == "ed25519" else KeyedHashSigner
    try:
        return backend.verify(
            checkpoint.get("public_key"), _checkpoint_payload(head_index, head_hash), checkpoint.get("signature", "")
        )
    except SigningError:
        return False
