"""Mutation checks for ordered, hash-pinned restoration of historical bundles."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("inventory", ROOT / "tools/validate-git-bundle-inventory.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class TrackedChainTest(unittest.TestCase):
    def setUp(self):
        inventory = json.loads((ROOT / "data/git-bundle-portability-inventory-v1.json").read_text())
        self.entry = next(e for e in inventory["bundles"]
                          if "/vllm-qsafused-mtp1-" in e["path"])
        self.manifest = json.loads((ROOT / self.entry["manifest"]["path"]).read_text())

    def test_complete_ordered_chain_passes(self):
        self.assertEqual(len(m._validate_tracked_chain(ROOT, self.entry, self.manifest)), 4)

    def test_bad_chain_declarations_fail(self):
        def swap_order(doc):
            doc["recovery_chain"][0], doc["recovery_chain"][1] = doc["recovery_chain"][1], doc["recovery_chain"][0]

        mutations = [
            swap_order,
            lambda d: d["recovery_chain"].pop(0),
            lambda d: d["recovery_chain"].pop(),
            lambda d: d["recovery_chain"].append(copy.deepcopy(d["recovery_chain"][-1])),
            lambda d: d["recovery_chain"][0].update(sha256="0" * 64),
            lambda d: d["recovery_chain"][0].update(ref="refs/tags/deceptive"),
            lambda d: d["recovery_chain"][0].update(path="patches/missing.bundle"),
            lambda d: d["recovery_chain"][0].update(path="../outside.bundle"),
            lambda d: d["prerequisites"][0].update(tree="0" * 40),
            lambda d: d["public_base"].update(remote="file:///private/checkout"),
            lambda d: d.update(expected_tree="0" * 40),
        ]
        for index, mutate in enumerate(mutations):
            with self.subTest(mutation=index):
                doc = copy.deepcopy(self.manifest)
                mutate(doc)
                with self.assertRaises(m.ValidationError):
                    m._validate_tracked_chain(ROOT, self.entry, doc)


if __name__ == "__main__":
    unittest.main()
