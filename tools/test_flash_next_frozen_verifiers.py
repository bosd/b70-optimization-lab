"""Historical replay must use each record's own verifier without repinning it."""
import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
PACKETS = sorted(ROOT.glob("repro/qwen38-flash-next-*/verify-moe-selection-frozen.py"))


def load(path):
    spec = importlib.util.spec_from_file_location("replay", path / "make-replay-attempt.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FrozenVerifierTest(unittest.TestCase):
    def test_all_three_historical_recipes_keep_exact_bytes(self):
        self.assertEqual(len(PACKETS), 3)
        for snapshot in PACKETS:
            with self.subTest(packet=snapshot.parent.name):
                pins = dict(line.split("=", 1) for line in
                            snapshot.with_name("verifier-pin.txt").read_text().splitlines())
                self.assertEqual(hashlib.sha256(snapshot.read_bytes()).hexdigest(), pins["sha256"])

    def test_replay_redirects_both_check_and_execution_preserving_every_hash(self):
        for snapshot in PACKETS:
            with self.subTest(packet=snapshot.parent.name):
                m = load(snapshot.parent)
                original = m.source(m.SRC["client"], m.pinned())
                client = m.frozen_client(original)
                new_path = snapshot.relative_to(ROOT).as_posix()
                self.assertEqual(client.count(new_path), 2)
                self.assertNotIn("tools/verify-moe-m1-w13-n32-selection.py", client)
                self.assertEqual(m.HASH_TOKEN.findall(client), m.HASH_TOKEN.findall(original))

    def test_tampered_snapshot_and_missing_reference_fail_closed(self):
        for snapshot in PACKETS:
            m = load(snapshot.parent)
            with self.subTest(packet=snapshot.parent.name), tempfile.TemporaryDirectory() as tmp:
                p = Path(tmp)
                (p / "verifier-pin.txt").write_bytes(snapshot.with_name("verifier-pin.txt").read_bytes())
                (p / snapshot.name).write_text("tampered\n")
                with patch.object(m, "HERE", p), self.assertRaisesRegex(ValueError, "differs"):
                    m.frozen_client("anything")
                with self.assertRaisesRegex(ValueError, "exactly"):
                    m.frozen_client("no verifier references")


if __name__ == "__main__":
    unittest.main()
