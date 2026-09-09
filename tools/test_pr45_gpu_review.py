"""Mock-only lifecycle checks: never invoke Docker, GPUs, journalctl or an endpoint."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock, patch

PATH = Path(__file__).resolve().parents[1] / "community/dominick253-qwen38-27b-fp8-uniform-decode-alias/validation/run_gpu_review.py"
SPEC = importlib.util.spec_from_file_location("gpu_review", PATH)
m = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(m)


class ReviewTest(unittest.TestCase):
    def exercise(self, workload_failure=False, remains=False, fault=False, health_failure=False,
                 arm="candidate", stop_failure=False):
        with tempfile.TemporaryDirectory() as tmp:
            args = SimpleNamespace(out=Path(tmp), model_dir=Path("/unused"))
            launcher = MagicMock()
            launcher.poll.return_value = None
            original = subprocess.CalledProcessError(7, ["mock-workload"])
            def run(cmd, **kwargs):
                if cmd[0] == "docker" and stop_failure:
                    raise subprocess.TimeoutExpired(cmd, 40)
                if cmd[0] == "bash" and workload_failure:
                    raise original
                return SimpleNamespace(stdout="", stderr="", returncode=0)
            def output(cmd, **kwargs):
                if cmd[0] == "journalctl":
                    return "GPU reset" if fault else ""
                return "still-running" if remains else ""
            with patch.object(m.subprocess, "Popen", return_value=launcher) as launch, \
                 patch.object(m.subprocess, "run", side_effect=run), \
                 patch.object(m.subprocess, "check_output", side_effect=output), \
                 patch.object(m.urllib.request, "urlopen", return_value=MagicMock()), \
                 patch.object(m, "gpu_health", side_effect=RuntimeError("bad health") if health_failure else None) as health:
                error = None
                try:
                    m.run_arm(args, arm)
                except BaseException as exc:
                    error = exc
                record = json.loads((args.out / arm / "run.json").read_text())
                if workload_failure:
                    self.assertIs(error, original)
                if workload_failure or remains or fault or health_failure or stop_failure:
                    self.assertIsNotNone(error)
                    self.assertEqual(record["status"], "failed")
                    self.assertFalse(record["campaign_stage_complete"])
                else:
                    self.assertIsNone(error)
                    self.assertEqual(record["status"], "passed")
                self.assertEqual(health.call_count, 0 if remains or fault or stop_failure else 1)
                self.assertIn("cleanup", record)
                self.assertIn("postflight", record)
                launcher.wait.assert_called_once()
                return record, launch.call_args.kwargs["env"]

    def test_workload_failure_still_checks_health_and_preserves_exception(self):
        self.exercise(workload_failure=True)

    def test_cleanup_failure_skips_gpu_but_records_kernel(self):
        record, _ = self.exercise(workload_failure=True, remains=True)
        self.assertTrue(record["postflight"]["kernel_passed"])
        self.assertFalse(record["cleanup_passed"])

    def test_stop_timeout_does_not_mask_workload_failure(self):
        self.exercise(workload_failure=True, stop_failure=True)

    def test_kernel_fault_skips_gpu_health(self):
        self.exercise(fault=True)

    def test_health_failure_does_not_leave_passing_record(self):
        self.exercise(health_failure=True)

    def test_success_requires_all_lifecycle_checks(self):
        self.exercise()

    def test_target_only_disables_compilation_and_speculation(self):
        record, env = self.exercise(arm="candidate-target-only")
        self.assertEqual(env["SPECULATIVE_CONFIG"], "null")
        self.assertEqual(json.loads(env["COMPILATION_CONFIG"])["mode"], 0)
        self.assertTrue(record["speculative_disabled"])
        self.assertFalse(record["strict_workload_run"])

    def test_gdn_target_control_changes_only_candidate_image(self):
        record, env = self.exercise(arm="gdn-target-only")
        self.assertEqual(env["IMAGE"], m.IMAGES["gdn"])
        self.assertEqual(env["SPECULATIVE_CONFIG"], "null")
        self.assertEqual(json.loads(env["COMPILATION_CONFIG"])["mode"], 0)
        self.assertTrue(record["gdn_phase_guard"])
        self.assertFalse(record["strict_workload_run"])

    def test_gdn_mtp_runs_full_workload(self):
        record, env = self.exercise(arm="gdn-mtp")
        self.assertEqual(env["IMAGE"], m.IMAGES["gdn"])
        self.assertFalse(record["speculative_disabled"])
        self.assertTrue(record["strict_workload_run"])


if __name__ == "__main__":
    unittest.main()
