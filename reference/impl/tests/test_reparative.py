# SPDX-License-Identifier: Apache-2.0
"""Reparative-action tests: the audit is a CORRECTION ledger, not a punishment ledger.

A REPARATIVE leaf is appended AFTER a preserved ENFORCE_FAIL; the original FAIL is never
erased, the chain stays intact, and the reparation references the violation. Refused while halted.
"""
from __future__ import annotations

import unittest

from indras_net import ActionClassLedger, HaltError

from . import _helpers as H


class TestReparation(unittest.TestCase):
    def _run_until_fail(self):
        """Run a forbidden-effect task so the ledger carries an ENFORCE_FAIL leaf."""
        scripted = {
            "deploy": H.mock_result(effect_id="code.deploy.production", args={"target": "prod"})
        }
        swarm, ledger = H.make_swarm(scripted=scripted)
        swarm.run("deploy", {"input_trust_label": "trusted:audited"})
        return swarm, ledger

    def test_reparation_appended_after_preserved_fail(self):
        swarm, ledger = self._run_until_fail()
        fail_leaves = [
            lf for lf in ledger.leaves() if lf.action_class is ActionClassLedger.ENFORCE_FAIL
        ]
        self.assertTrue(fail_leaves, "expected an ENFORCE_FAIL leaf from the denied action")
        fail_hash = fail_leaves[-1].entry_hash
        n_before = len(ledger.leaves())

        actor = swarm.builder.identity
        leaf = swarm.record_reparation(
            actor_did=actor.did,
            actor_role=actor.role,
            summary="narrowed scope; used a granted effect instead",
            references=[fail_hash],
        )

        # the REPARATIVE leaf is appended AFTER the FAIL and references it
        self.assertIs(leaf.action_class, ActionClassLedger.REPARATIVE)
        self.assertEqual(len(ledger.leaves()), n_before + 1)
        self.assertIs(ledger.leaves()[-1].action_class, ActionClassLedger.REPARATIVE)
        self.assertIn(fail_hash, leaf.refs)

        # the original FAIL is PRESERVED (correction, not erasure) and the chain still verifies
        preserved = [lf for lf in ledger.leaves() if lf.entry_hash == fail_hash]
        self.assertEqual(len(preserved), 1, "the original FAIL must be preserved, never erased")
        self.assertIs(preserved[0].action_class, ActionClassLedger.ENFORCE_FAIL)
        self.assertTrue(ledger.verify())

    def test_reparation_refused_while_halted(self):
        swarm, _ = self._run_until_fail()
        swarm.halt("external-stop")
        actor = swarm.builder.identity
        with self.assertRaises(HaltError):
            swarm.record_reparation(actor_did=actor.did, actor_role=actor.role, summary="late fix")


if __name__ == "__main__":
    unittest.main()
