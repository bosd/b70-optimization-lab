"""Final GPU-review verdict must include cleanup and postflight, without using GPUs."""
import json
from pathlib import Path
import runpy
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "community/dominick253-qwen38-27b-fp8-uniform-decode-alias/validation/run_gpu_review.py"


class ReviewVerdictTest(unittest.TestCase):
    def run_case(self, failure):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            main = runpy.run_path(str(SCRIPT))["main"]
            def arm(args, name):
                folder = args.out / name
                folder.mkdir()
                (folder / "run.json").write_text(json.dumps({"status": "passed_workload_and_probes"}))
                if failure:
                    raise RuntimeError("postflight failed")
            real_open = open
            with patch.dict(main.__globals__, {"run_arm": arm, "open": lambda *_: real_open(root / "lock", "w")}), \
                 patch.object(sys, "argv", [str(SCRIPT), "--out", raw, "--model-dir", raw, "--arms", "candidate"]), \
                 patch("subprocess.check_output", return_value=""):
                if failure:
                    with self.assertRaisesRegex(RuntimeError, "postflight failed"):
                        main()
                else:
                    main()
            return json.loads((root / "candidate/run.json").read_text())

    def test_postflight_failure_overrides_workload_success(self):
        record = self.run_case(True)
        self.assertEqual(record["status"], "failed")
        self.assertFalse(record["campaign_stage_complete"])

    def test_success_requires_complete_stage(self):
        record = self.run_case(False)
        self.assertEqual(record["status"], "passed")
        self.assertTrue(record["postflight_passed"])
        self.assertTrue(record["cleanup_passed"])


if __name__ == "__main__":
    unittest.main()
