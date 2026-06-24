# SPDX-License-Identifier: Apache-2.0
"""Phase-3 persistence tests.

The hash-chained ledger survives a restart and stays tamper-evident on disk (an edited leaf
breaks verify(); a corrupt line is loud), and memory adaptation persists across a restart.
All files live under a tempfile dir and are cleaned up; nothing touches the real system.
"""
from __future__ import annotations

import os
import shutil
import tempfile
import unittest

from indras_net import AkashaSutra, ActionClassLedger, SwarmMemory, TamperError

from . import _helpers as H


def _append(ledger: AkashaSutra, n: int) -> None:
    for i in range(n):
        env = H.build_envelope(summary="leaf-%d" % i)
        ledger.append(
            signer_did=H.CHITRAGUPTA_DID,
            signer_role="chitragupta",
            action_class=ActionClassLedger.OBSERVE,
            event_type="t%d" % i,
            envelope=env,
            writer_did=H.CHITRAGUPTA_DID,
        )


class TestLedgerPersistence(unittest.TestCase):
    def setUp(self) -> None:
        self.dir = tempfile.mkdtemp(prefix="indras-led-")
        self.path = os.path.join(self.dir, "ledger.jsonl")

    def tearDown(self) -> None:
        shutil.rmtree(self.dir, ignore_errors=True)

    def test_reload_preserves_chain_and_verifies(self):
        led = AkashaSutra(H.CHITRAGUPTA_DID, path=self.path)
        _append(led, 5)
        self.assertTrue(led.verify())
        head = led.head_hash()

        led2 = AkashaSutra.load(self.path, H.CHITRAGUPTA_DID)  # "restart"
        self.assertEqual(len(led2), 5)
        self.assertTrue(led2.verify(), "the chain verifies across a restart")
        self.assertEqual(led2.head_hash(), head)

        _append(led2, 2)  # appending continues the chain, persisted
        self.assertTrue(led2.verify())
        led3 = AkashaSutra.load(self.path, H.CHITRAGUPTA_DID)
        self.assertEqual(len(led3), 7)
        self.assertTrue(led3.verify(), "continuity across two restarts")

    def test_on_disk_tamper_breaks_verify(self):
        led = AkashaSutra(H.CHITRAGUPTA_DID, path=self.path)
        _append(led, 4)
        with open(self.path, encoding="utf-8") as fh:
            lines = fh.readlines()
        lines[1] = lines[1].replace('"t1"', '"FORGED"')  # edit a past leaf's content, not its hash
        with open(self.path, "w", encoding="utf-8") as fh:
            fh.writelines(lines)
        led2 = AkashaSutra.load(self.path, H.CHITRAGUPTA_DID)
        self.assertFalse(led2.verify(), "an on-disk edit to a past leaf must break verify()")

    def test_corrupt_line_is_loud(self):
        led = AkashaSutra(H.CHITRAGUPTA_DID, path=self.path)
        _append(led, 2)
        with open(self.path, "a", encoding="utf-8") as fh:
            fh.write("{ not valid json\n")
        with self.assertRaises(TamperError):
            AkashaSutra.load(self.path, H.CHITRAGUPTA_DID)


class TestMemoryPersistence(unittest.TestCase):
    def test_adaptation_persists_across_restart(self):
        d = tempfile.mkdtemp(prefix="indras-mem-")
        try:
            path = os.path.join(d, "memory.json")
            mem = SwarmMemory()
            mem.observe(task="egress task", effect_id="net.egress.http", allowed=False, executed=False, adapted=False)
            self.assertTrue(mem.was_denied("egress task", "net.egress.http"))
            mem.save(path)

            mem2 = SwarmMemory.load(path)  # "restart"
            self.assertTrue(mem2.was_denied("egress task", "net.egress.http"), "the denial persists")
            effect, _args, adapted = mem2.adapt("egress task", "net.egress.http", {})
            self.assertTrue(adapted, "adaptation still fires after reload")
            self.assertEqual(effect, SwarmMemory.SAFE_DEFAULT_EFFECT, "it substitutes the safe default, never grants")
        finally:
            shutil.rmtree(d, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
