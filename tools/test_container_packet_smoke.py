"""Run the real packet smoke script against local fake Docker and HTTP commands."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ContainerPacketSmokeTest(unittest.TestCase):
    def run_smoke(self, first, second):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            docker = bin_dir / "docker"
            docker.write_text("#!/bin/sh\nexit 0\n")
            docker.chmod(0o755)
            curl = bin_dir / "curl"
            curl.write_text("""#!/usr/bin/env python3
import os,sys
from pathlib import Path
if any(arg.endswith('/health') for arg in sys.argv):
    sys.exit(0)
root=Path(os.environ['FAKE_ROOT'])
counter=root/'counter'
n=int(counter.read_text())+1 if counter.exists() else 1
counter.write_text(str(n))
print((root/f'response-{n}.json').read_text())
""")
            curl.chmod(0o755)
            for n, response in enumerate((first, second), 1):
                (root / f"response-{n}.json").write_text(response)
            env = dict(os.environ, PATH=f"{bin_dir}:{os.environ['PATH']}",
                       FAKE_ROOT=tmp, PACKAGE_DIR="packages/qwen35-4b-w4a16-b70",
                       SERVED_NAME="test-4b", MODEL_DIR=tmp, OUT_DIR=f"{tmp}/out",
                       VLLM_CACHE_DIR=f"{tmp}/cache", KEEP_UP="0", PROFILE="one-gpu")
            result = subprocess.run(
                ["bash", str(ROOT / "tools/container-packet/smoke-test.sh")],
                env=env, capture_output=True, text=True, timeout=15)
            record = root / "out/result.json"
            return result, json.loads(record.read_text()) if record.exists() else None

    @staticmethod
    def response(text):
        return json.dumps({"choices": [{"text": text}], "usage": {"completion_tokens": 4}})

    def test_identical_responses_pass_and_example_uses_served_model(self):
        result, record = self.run_smoke(self.response("A tensor.\n"), self.response("A tensor.\n"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(record["repeat_exact"])
        self.assertEqual(record["sample_text"], "A tensor.\n")
        self.assertIn('"model":"test-4b"', result.stdout)
        self.assertNotIn('"model":"qwen35-9b-w4a16"', result.stdout)

    def test_trailing_newline_mismatch_fails(self):
        result, record = self.run_smoke(self.response("A tensor."), self.response("A tensor.\n"))
        self.assertNotEqual(result.returncode, 0)
        self.assertIsNone(record)
        self.assertNotIn("PASS ", result.stdout)

    def test_malformed_second_response_fails(self):
        for response in ("not json", "{}", self.response(None)):
            with self.subTest(response=response):
                result, record = self.run_smoke(self.response("A tensor."), response)
                self.assertNotEqual(result.returncode, 0)
                self.assertIsNone(record)
                self.assertNotIn("PASS ", result.stdout)


if __name__ == "__main__":
    unittest.main()
