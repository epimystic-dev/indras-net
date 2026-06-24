# SPDX-License-Identifier: Apache-2.0
"""Canonicalize -> Address -> Sign (CAS) primitives: the deterministic integrity spine.

Every other module addresses content by the hash of its canonical bytes, so a
datum's identity IS its hash, not a hope. A truncated, corrupted, or stale read
fails its content address before it can propagate (doc 21 / doc 04).

Honesty note: ``detached_sig`` here is a keyed-hash ORIGIN stand-in for the
zero-dependency path -- it is forgeable and proves nothing about the truth,
safety, or floor-compatibility of the signed content. Real Ed25519 signing is
available in ``signing.py`` (the optional ``cryptography`` extra). Either way a
valid signature proves origin/integrity only -- verify the cage, not the animal.
"""
import hashlib
import json
from typing import Any


class CanonicalizationError(Exception):
    """Raised when an object cannot be deterministically canonicalized to JSON."""


# RFC 4648 base32 lowercase alphabet (no padding) -- multibase 'b' prefix.
_B32_ALPHABET = "abcdefghijklmnopqrstuvwxyz234567"


def _base32_nopad_lower(data: bytes) -> str:
    """Lowercase, unpadded base32 of raw bytes (multibase base32 body)."""
    bits = 0
    value = 0
    out = []
    for byte in data:
        value = (value << 8) | byte
        bits += 8
        while bits >= 5:
            bits -= 5
            out.append(_B32_ALPHABET[(value >> bits) & 0x1F])
    if bits > 0:
        out.append(_B32_ALPHABET[(value << (5 - bits)) & 0x1F])
    return "".join(out)


def jcs_canonicalize(obj: Any) -> bytes:
    """RFC-8785-style canonical JSON bytes: sorted keys, no whitespace, UTF-8.

    Deterministic for any JSON-serializable object: the same logical object
    produces identical bytes regardless of original key order.
    """
    try:
        return json.dumps(
            obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise CanonicalizationError(str(exc)) from exc


def sha256_hex(data: bytes) -> str:
    """Lowercase hex SHA-256 digest (64 chars)."""
    return hashlib.sha256(data).hexdigest()


def cid(obj: Any) -> str:
    """CIDv1-shaped content address of an object's canonical bytes.

    Layout: multibase 'b' (base32) over (CIDv1 | raw-codec | sha2-256 | len-32 | digest).
    Matches the schema pattern ^b[a-z2-7]{20,}$ (e.g. 'bafkrei...'). Pure function:
    the same logical object yields an identical CID across all callers.
    """
    digest = hashlib.sha256(jcs_canonicalize(obj)).digest()
    prefix = bytes([0x01, 0x55, 0x12, 0x20])  # CIDv1, raw codec, sha2-256, 32-byte length
    return "b" + _base32_nopad_lower(prefix + digest)


def leaf_hash(data: bytes) -> str:
    """RFC-6962 domain-separated leaf hash: SHA-256(0x00 || data)."""
    return hashlib.sha256(b"\x00" + data).hexdigest()


def node_hash(left_hex: str, right_hex: str) -> str:
    """RFC-6962 domain-separated interior node hash: SHA-256(0x01 || left || right).

    Reserved forward primitive. The MVP ledger is a LINEAR hash-chain (see audit.py),
    so nothing in this implementation calls this yet; it is kept as the seam for a
    future Merkle / transparency-log (tlog-tiles) ledger.
    """
    return hashlib.sha256(b"\x01" + bytes.fromhex(left_hex) + bytes.fromhex(right_hex)).hexdigest()


def detached_sig(jcs_bytes: bytes, signer_did: str) -> str:
    """MVP origin stand-in: SHA-256(signer_did || '.' || jcs_bytes).

    A keyed hash for tamper-evidence ONLY. It is NOT a real signature and NEVER
    a proof of truth, safety, or trust.
    """
    return hashlib.sha256(signer_did.encode("utf-8") + b"." + jcs_bytes).hexdigest()
