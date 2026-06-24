# SPDX-License-Identifier: Apache-2.0
"""Phase-2 sandboxed-execution tests.

A gated effect that runs is CONFINED to its workspace and cannot escape it; effects without a
safe handler are refused with no side effect; there is no network. Every filesystem write
happens under a tempfile root -- never the real system -- and is cleaned up.
"""
from __future__ import annotations

import os
import shutil
import tempfile
import unittest

from indras_net import SandboxedExecutor, StubExecutor

from . import _helpers as H


class TestSandboxConfinement(unittest.TestCase):
    def setUp(self) -> None:
        self.root = tempfile.mkdtemp(prefix="indras-sbx-")
        self.ex = SandboxedExecutor(self.root)

    def tearDown(self) -> None:
        shutil.rmtree(self.root, ignore_errors=True)

    def test_confined_write_then_read(self):
        out = self.ex.execute("fs.write.workspace", {"path": "notes/a.md", "content": "hello"})
        self.assertIn("wrote:", out)
        target = os.path.join(self.root, "notes", "a.md")
        self.assertTrue(os.path.isfile(target))
        with open(target, encoding="utf-8") as fh:
            self.assertEqual(fh.read(), "hello")
        self.assertIn("read:5B", self.ex.execute("fs.read.workspace", {"path": "notes/a.md"}))

    def test_absolute_path_write_refused(self):
        sentinel = os.path.join(tempfile.gettempdir(), "indras-escape-abs.txt")
        if os.path.exists(sentinel):
            os.remove(sentinel)
        out = self.ex.execute("fs.write.workspace", {"path": sentinel, "content": "x"})
        self.assertIn("refused", out)
        self.assertFalse(os.path.exists(sentinel), "absolute-path write must not escape the sandbox")

    def test_dotdot_escape_refused(self):
        out = self.ex.execute("fs.write.workspace", {"path": "../escape.txt", "content": "x"})
        self.assertIn("refused", out)
        self.assertFalse(os.path.exists(os.path.join(os.path.dirname(self.root), "escape.txt")))

    def test_deep_dotdot_escape_refused(self):
        out = self.ex.execute("fs.write.workspace", {"path": "a/b/../../../../escape2.txt", "content": "x"})
        self.assertIn("refused", out)

    def test_symlink_escape_refused(self):
        outside = tempfile.mkdtemp(prefix="indras-out-")
        link = os.path.join(self.root, "link")
        try:
            os.symlink(outside, link, target_is_directory=True)
        except (OSError, NotImplementedError, AttributeError):
            self.skipTest("symlinks unavailable on this host")
        try:
            out = self.ex.execute("fs.write.workspace", {"path": "link/evil.txt", "content": "x"})
            self.assertIn("refused", out)
            self.assertFalse(os.path.exists(os.path.join(outside, "evil.txt")))
        finally:
            shutil.rmtree(outside, ignore_errors=True)

    def test_unknown_and_forbidden_effects_refused_no_side_effect(self):
        self.assertIn("refused", self.ex.execute("net.egress.http", {"url": "http://example.org/x"}))
        self.assertIn("refused", self.ex.execute("code.deploy.production", {"target": "prod"}))
        self.assertIn("refused", self.ex.execute("replicate.spawn", {"count": 3}))
        self.assertEqual(os.listdir(self.root), [], "a refused effect must create nothing")

    def test_write_ceiling_enforced(self):
        ex = SandboxedExecutor(self.root, max_bytes=8)
        out = ex.execute("fs.write.workspace", {"path": "big.txt", "content": "x" * 100})
        self.assertIn("refused", out)
        self.assertFalse(os.path.isfile(os.path.join(self.root, "big.txt")))

    def test_summarize_is_pure_no_io(self):
        out = self.ex.execute("analysis.summarize", {"text": "one two three four", "max_words": 2})
        self.assertIn("summary", out)
        self.assertEqual(os.listdir(self.root), [], "a pure summarize must not write files")

    def test_stub_executor_does_no_io(self):
        out = StubExecutor().execute("fs.write.workspace", {"path": "x", "content": "y"})
        self.assertIn("executed:", out)
        self.assertFalse(os.path.exists(os.path.join(self.root, "x")))

    # -- hardening against untrusted-arg crashes / aliasing (red-team regressions) --

    def test_colon_and_ads_paths_refused(self):
        for path in ["..::$DATA", "name:stream", "a:b", "C:evil"]:
            self.assertIn("refused", self.ex.execute("fs.write.workspace", {"path": path, "content": "x"}), path)
        self.assertEqual(os.listdir(self.root), [])

    def test_reserved_device_names_refused(self):
        for path in ["NUL", "CON", "con", "COM1", "lpt1", "a/NUL", "nul.txt"]:
            self.assertIn("refused", self.ex.execute("fs.write.workspace", {"path": path, "content": "x"}), path)

    def test_trailing_dot_or_space_refused(self):
        for path in ["foo.txt.", "bar ", "a/b.txt ."]:
            self.assertIn("refused", self.ex.execute("fs.write.workspace", {"path": path, "content": "x"}), path)
        self.assertEqual(os.listdir(self.root), [])

    def test_overdeep_path_refused(self):
        deep = "/".join(["d"] * 100) + "/f.txt"
        self.assertIn("refused", self.ex.execute("fs.write.workspace", {"path": deep, "content": "x"}))

    def test_noncoercible_content_refused_no_zerofill(self):
        for bad in (5, 3.14, {"a": 1}, [1, 2, 3], True, 999999):
            self.assertIn("refused", self.ex.execute("fs.write.workspace", {"path": "c.txt", "content": bad}), repr(bad))
        self.assertFalse(
            os.path.exists(os.path.join(self.root, "c.txt")), "non-text content must NOT create a zero-filled file"
        )

    def test_bytes_content_is_accepted(self):
        out = self.ex.execute("fs.write.workspace", {"path": "b.bin", "content": b"\x01\x02\x03"})
        self.assertIn("wrote:3B", out)

    def test_no_hostile_input_ever_raises_out_of_execute(self):
        hostile = [
            {"path": "..::$DATA", "content": "x"},
            {"path": "NUL", "content": "x"},
            {"path": "../../etc/passwd", "content": "x"},
            {"path": 123, "content": "x"},
            {"path": "ok.txt", "content": object()},
            {"path": "ok.txt", "content": 999999},
            {"path": "\x00bad", "content": "x"},
            {"path": "ok.txt"},
            {},
        ]
        for args in hostile:
            out = self.ex.execute("fs.write.workspace", args)  # must return a string, never raise
            self.assertIsInstance(out, str)


class TestSwarmWithSandbox(unittest.TestCase):
    def test_granted_write_executes_confined_and_ledger_intact(self):
        root = tempfile.mkdtemp(prefix="indras-sbx-swarm-")
        try:
            ex = SandboxedExecutor(root)
            scripted = {
                "writetask": H.mock_result(
                    effect_id="fs.write.workspace", args={"path": "out.md", "content": "swarm wrote this"}
                )
            }
            swarm, ledger = H.make_swarm(scripted=scripted, with_steward=True, executor=ex)
            result = swarm.run("writetask", {"input_trust_label": "trusted:audited"})
            executed = [o for o in result.occasion_results if o.executed]
            self.assertTrue(executed, "the granted fs.write should have executed")
            target = os.path.join(root, "out.md")
            self.assertTrue(os.path.isfile(target), "the gated effect wrote inside the sandbox")
            with open(target, encoding="utf-8") as fh:
                self.assertEqual(fh.read(), "swarm wrote this")
            self.assertTrue(ledger.verify(), "audit chain intact after a real execution")
        finally:
            shutil.rmtree(root, ignore_errors=True)

    def test_malicious_content_does_not_crash_run_or_tear_audit(self):
        root = tempfile.mkdtemp(prefix="indras-sbx-mal-")
        try:
            ex = SandboxedExecutor(root)
            scripted = {
                "badwrite": H.mock_result(effect_id="fs.write.workspace", args={"path": "x.txt", "content": 3.14})
            }
            swarm, ledger = H.make_swarm(scripted=scripted, with_steward=True, executor=ex)
            swarm.run("badwrite", {"input_trust_label": "trusted:audited"})  # must not raise
            self.assertTrue(ledger.verify(), "audit chain intact -- no torn record from a refused effect")
            self.assertFalse(os.path.exists(os.path.join(root, "x.txt")), "non-text content wrote nothing")
        finally:
            shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
