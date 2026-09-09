"""Bounded same-profile R50 comparison; does not promote performance or start a service permanently."""
import argparse
import datetime as dt
import fcntl
import json
import os
from pathlib import Path
import re
import subprocess
import time
import urllib.request

REPO = Path(__file__).resolve().parents[3]
PACKET = Path(__file__).resolve().parent
RECIPE = REPO / "repro/qwen38-27b-fp8-vllm-tp2-asrock-b70"
IMAGES = {
    "baseline": "sha256:2932e495b560e79c6301f5cc64584af928a2260f0d0d19c145142b2ef35860d3",
    "candidate": "sha256:4bb40c00826d3adeb577306afe8d7a6836eaef61d33e1e97a99b74ea85081fb4",
}
FAULT = re.compile(r"Fault response|CAT error|engine reset|GPU reset|soft lockup|Timedout job", re.I)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--model-dir", type=Path, required=True)
    parser.add_argument("--arms", nargs="+", default=["baseline", "candidate", "candidate-repeat"],
                        choices=["baseline", "candidate", "candidate-repeat"])
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    with open("/tmp/b70-pr45-review.lock", "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if subprocess.check_output(["docker", "ps", "-q"], text=True).strip():
            raise RuntimeError("another container is active; inspect ownership before GPU work")
        for arm in args.arms:
            run_arm(args, arm)


def run_arm(args, arm):
    folder = args.out / arm
    folder.mkdir(exist_ok=False)
    image = IMAGES["baseline" if arm == "baseline" else "candidate"]
    container = "pr45-review-" + arm
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    env = dict(os.environ, IMAGE=image, EXPECTED_IMAGE_ID=image,
               MODEL_DIR=str(args.model_dir), VLLM_CACHE_DIR=str(folder / "cache"),
               MAX_MODEL_LEN="4096", MAX_NUM_SEQS="4", MAX_NUM_BATCHED_TOKENS="1024",
               CONTAINER_NAME=container, SERVED_MODEL_NAME="pr45-review", PORT="18124")
    record = {"arm": arm, "image": image, "started_utc": started,
              "max_model_len": 4096, "max_num_seqs": 4, "max_num_batched_tokens": 1024,
              "status": "running", "performance_promotion": False}
    (folder / "run.json").write_text(json.dumps(record, indent=2) + "\n")
    print(f"START {arm}: {image}", flush=True)
    with (folder / "server.log").open("w") as log:
        process = subprocess.Popen(["bash", str(RECIPE / "run-w8a16-mtp1-strict-server.sh")],
                                   env=env, stdout=log, stderr=subprocess.STDOUT)
        try:
            deadline = time.monotonic() + 900
            next_journal = 0
            while time.monotonic() < deadline:
                if process.poll() is not None:
                    raise RuntimeError(f"server launcher exited {process.returncode}; see server.log")
                if time.monotonic() >= next_journal:
                    journal = subprocess.run(["journalctl", "-k", "--since", started, "--no-pager"],
                                             capture_output=True, text=True, check=True).stdout
                    (folder / "kernel.log").write_text(journal)
                    if FAULT.search(journal):
                        raise RuntimeError("new kernel fault; aborting GPU campaign")
                    next_journal = time.monotonic() + 20
                try:
                    with urllib.request.urlopen("http://127.0.0.1:18124/health", timeout=2):
                        break
                except OSError:
                    time.sleep(3)
            else:
                raise TimeoutError("server did not become ready within 900 seconds")
            print(f"READY {arm}; running complete strict workload and canaries", flush=True)
            bench_env = dict(env, OUT_DIR=str(folder / "strict"), BASE_URL="http://127.0.0.1:18124",
                             MODEL_NAME="pr45-review", PROFILE_LABEL="pr45-" + arm,
                             ATTEMPT_LABEL=arm)
            with (folder / "strict.log").open("w") as bench_log:
                subprocess.run(["bash", str(RECIPE / "bench-w8a16-mtp1-strict.sh")], env=bench_env,
                               stdout=bench_log, stderr=subprocess.STDOUT, timeout=900, check=True)
            subprocess.run(["python3", str(PACKET / "probe_endpoint.py"),
                            "--base-url", "http://127.0.0.1:18124", "--model", "pr45-review",
                            "--out", str(folder / "probes.json")], timeout=600, check=True)
            record["status"] = "passed_workload_and_probes"
        except BaseException as exc:
            record["status"] = "failed"
            record["error"] = str(exc)
            raise
        finally:
            subprocess.run(["docker", "stop", "--timeout", "20", container],
                           capture_output=True, timeout=40)
            try:
                process.wait(timeout=30)
            except subprocess.TimeoutExpired:
                process.terminate()
                process.wait(timeout=10)
            record["finished_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
            (folder / "run.json").write_text(json.dumps(record, indent=2) + "\n")
            print(f"END {arm}: {record['status']}", flush=True)
    journal = subprocess.check_output(["journalctl", "-k", "--since", started, "--no-pager"], text=True)
    (folder / "kernel-postflight.log").write_text(journal)
    if FAULT.search(journal):
        raise RuntimeError("kernel postflight failed; no further launches")
    health = ["docker", "run", "--rm", "--name", "pr45-review-health", "--network", "none",
              "--ipc", "host", "--device", "/dev/dri", "--group-add", "render",
              "--cap-add", "SYS_PTRACE", "--security-opt", "label=disable", "-w", "/",
              "--volume", f"{REPO}:/repo:ro", "--env", "PYTHON=/opt/venv/bin/python",
              "--env", "ROOT=/repo", "--env", "PHYSICAL_DEVICES=0,1",
              "--env", "XCCL_DEVICES=0,1", "--env", "CCL_ZE_IPC_EXCHANGE=pidfd",
              "--env", "TIMEOUT_S=60", "--entrypoint", "bash", image,
              "/repo/scripts/check-qwen36-xpu-xccl-health.sh"]
    with (folder / "gpu-postflight.log").open("w") as log:
        subprocess.run(health, stdout=log, stderr=subprocess.STDOUT, timeout=120, check=True)


if __name__ == "__main__":
    main()
