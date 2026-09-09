"""A failed image inspection must not produce a successful all-inert audit."""
import importlib.util
import io
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch


spec = importlib.util.spec_from_file_location(
    "launcher_audit", Path(__file__).with_name("audit-launcher-env-implemented.py"))
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class LauncherAuditTest(unittest.TestCase):
    def test_docker_failure_has_no_verdict(self):
        failure = subprocess.CalledProcessError(125, ["docker", "run"])
        with patch.object(audit.subprocess, "run", side_effect=failure) as run, \
             patch.object(audit.sys, "argv", ["audit", "missing-image"]), \
             patch.object(audit.sys, "stdout", new_callable=io.StringIO) as stdout, \
             patch.object(audit.sys, "stderr", new_callable=io.StringIO):
            self.assertEqual(audit.main(), 1)
            self.assertNotIn("inert:", stdout.getvalue())
            self.assertTrue(run.call_args.kwargs["check"])

    def test_incomplete_inspection_has_no_verdict(self):
        with patch.object(audit, "implemented", return_value={}), \
             patch.object(audit.sys, "argv", ["audit", "image"]), \
             patch.object(audit.sys, "stderr", new_callable=io.StringIO):
            self.assertEqual(audit.main(), 1)

    def test_successful_inspection_preserves_found_and_absent_entries(self):
        result = subprocess.CompletedProcess([], 0, "USED /site/module.py\nABSENT \n", "")
        with patch.object(audit.subprocess, "run", return_value=result):
            self.assertEqual(audit.implemented("image", ["USED", "ABSENT"]),
                             {"USED": "/site/module.py", "ABSENT": ""})

    def test_inner_scan_distinguishes_missing_root_grep_error_and_no_match(self):
        with patch.object(audit.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, "", "")) as run:
            audit.implemented("image", ["KNOB"])
            script = run.call_args.args[0][-1]
        for mode, expected in (("missing-root", 2), ("grep-error", 2), ("no-match", 0)):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                scan = root / "site-packages"
                if mode != "missing-root":
                    scan.mkdir()
                body = script.replace("/opt/venv/lib/python3.12/site-packages/", str(scan))
                if mode == "grep-error":
                    body = "grep() { return 2; }\n" + body
                result = subprocess.run(["bash", "-c", body], capture_output=True, text=True)
                self.assertEqual(result.returncode, expected, result.stderr)
                if expected:
                    self.assertNotIn("KNOB ", result.stdout)
                else:
                    self.assertEqual(result.stdout, "KNOB \n")


if __name__ == "__main__":
    unittest.main()
