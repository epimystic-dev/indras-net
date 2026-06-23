# SPDX-License-Identifier: Apache-2.0
"""Audit (Akasha-Sutra) tests: hash-chain links, tamper-evidence, exclusive writer, authority."""

from __future__ import annotations

import unittest

from indras_net import (
    ActionClassLedger,
    AkashaSutra,
    Chitragupta,
    GENESIS_HASH,
    Status,
    WriterIdentityError,
)

from . import _helpers as H


def _set_field(obj, name, value):
    """Mutate a (possibly frozen) dataclass field in place to simulate tampering."""
    params = getattr(obj, "__dataclass_params__", None)
    if params is not None and params.frozen:
        object.__setattr__(obj, name, value)
    else:
        setattr(obj, name, value)


class TestChainLinks(unittest.TestCase):
    """test_audit_chain_links_and_monotonic"""

    def test_links_and_monotonic(self):
        ledger = H.plain_ledger()
        chit = Chitragupta(H.CHITRAGUPTA_DID)
        leaves = []
        for i in range(3):
            env = H.build_envelope(summary=f"entry-{i}", seal=True)
            leaf = chit.write(
                ledger,
                signer_did=H.YAMA_DID,
                signer_role="yama",
                action_class=ActionClassLedger.ENFORCE_PASS,
                event_type="floor.decision",
                envelope=env,
            )
            leaves.append(leaf)

        # First leaf chains to GENESIS; each subsequent prev_hash == prior entry_hash.
        self.assertEqual(leaves[0].prev_hash, GENESIS_HASH)
        for i in range(1, len(leaves)):
            self.assertEqual(leaves[i].prev_hash, leaves[i - 1].entry_hash)
            self.assertGreater(leaves[i].leaf_index, leaves[i - 1].leaf_index)
            self.assertGreater(leaves[i].record_id, leaves[i - 1].record_id)
        self.assertTrue(ledger.verify())
        self.assertEqual(len(ledger), 3)
        self.assertEqual(ledger.head_hash(), leaves[-1].entry_hash)


class TestTamperBreaksVerify(unittest.TestCase):
    """test_audit_tamper_breaks_verify"""

    def test_mutation_breaks_then_restore_fixes(self):
        ledger = H.plain_ledger()
        chit = Chitragupta(H.CHITRAGUPTA_DID)
        for i in range(3):
            chit.write(
                ledger,
                signer_did=H.YAMA_DID,
                signer_role="yama",
                action_class=ActionClassLedger.ENFORCE_PASS,
                event_type="floor.decision",
                envelope=H.build_envelope(summary=f"e-{i}", seal=True),
            )
        self.assertTrue(ledger.verify())
        victim = ledger.get(1)
        original = victim.event_type
        _set_field(victim, "event_type", "forged.event")
        self.assertFalse(ledger.verify())
        _set_field(victim, "event_type", original)
        self.assertTrue(ledger.verify())


class TestExclusiveWriter(unittest.TestCase):
    """test_audit_exclusive_writer_fence"""

    def test_wrong_writer_did_is_fenced(self):
        ledger = H.plain_ledger()
        env = H.build_envelope(seal=True)
        with self.assertRaises(WriterIdentityError):
            ledger.append(
                signer_did=H.YAMA_DID,
                signer_role="yama",
                action_class=ActionClassLedger.ENFORCE_PASS,
                event_type="floor.decision",
                envelope=env,
                writer_did="did:web:indras-net.example.org:roles:impostor",
            )
        # Chitragupta (the registered exclusive writer) succeeds.
        chit = Chitragupta(H.CHITRAGUPTA_DID)
        leaf = chit.write(
            ledger,
            signer_did=H.YAMA_DID,
            signer_role="yama",
            action_class=ActionClassLedger.ENFORCE_PASS,
            event_type="floor.decision",
            envelope=env,
        )
        self.assertEqual(leaf.leaf_index, 0)


class TestActionClassAuthority(unittest.TestCase):
    """test_audit_action_class_authority"""

    def test_enforce_fail_requires_yama_signer(self):
        ledger = H.plain_ledger()
        env = H.build_envelope(status=Status.FAIL, seal=True)
        # ENFORCE_FAIL signed by a non-Yama DID must be rejected.
        with self.assertRaises(WriterIdentityError):
            ledger.append(
                signer_did=H.VISHWAKARMA_DID,
                signer_role="vishwakarma",
                action_class=ActionClassLedger.ENFORCE_FAIL,
                event_type="floor.deny",
                envelope=env,
                writer_did=H.CHITRAGUPTA_DID,
            )

    def test_halt_requires_vishnu_signer(self):
        ledger = H.plain_ledger()
        env = H.build_envelope(seal=True)
        with self.assertRaises(WriterIdentityError):
            ledger.append(
                signer_did=H.YAMA_DID,  # not Vishnu
                signer_role="yama",
                action_class=ActionClassLedger.HALT,
                event_type="control.halt",
                envelope=env,
                writer_did=H.CHITRAGUPTA_DID,
            )
        # Correct Vishnu signer is accepted.
        leaf = ledger.append(
            signer_did=H.VISHNU_DID,
            signer_role="vishnu",
            action_class=ActionClassLedger.HALT,
            event_type="control.halt",
            envelope=env,
            writer_did=H.CHITRAGUPTA_DID,
        )
        self.assertEqual(leaf.action_class, ActionClassLedger.HALT)
        self.assertTrue(ledger.verify())


if __name__ == "__main__":
    unittest.main()
