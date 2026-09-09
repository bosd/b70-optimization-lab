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
    "gdn": "sha256:334c353ffc543eaea2de85d25d947ab5a0db36b9cfa043d0ed7d849627662e81",
}
FAULT = re.compile(r"Fault response|CAT error|engine reset|GPU reset|soft lockup|Timedout job", re.I)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--model-dir", type=Path, required=True)
    parser.add_argument("--arms", nargs="+", default=["baseline", "candidate", "candidate-repeat"],
                        choices=["baseline", "candidate", "candidate-repeat", "candidate-no-compile",
                                 "candidate-target-only", "gdn-target-only", "gdn-mtp", "gdn-mtp-repeat",
                                 "gdn-target-strict", "gdn-target-strict-repeat"])
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    with open("/tmp/b70-pr45-review.lock", "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if subprocess.check_output(["docker", "ps", "-q"], text=True).strip():
            raise RuntimeError("another container is active; inspect ownership before GPU work")
        for arm in args.arms:
            record_path = args.out / arm / "run.json"
            if record_path.parent.exists():
                raise FileExistsError(f"refusing to overwrite prior attempt: {record_path.parent}")
            run_arm(args, arm)


def cleanup_container(name, process=None):
    """Stop only this arm's container, reap its launcher, then verify removal."""
    result = {"container": name, "errors": []}
    try:
        stopped = subprocess.run(["docker", "stop", "--timeout", "20", name],
                                 capture_output=True, text=True, timeout=40)
        result.update(stop_returncode=stopped.returncode, stop_stderr=stopped.stderr)
        # A --rm container may already have disappeared after a failed launcher.
        # The authoritative absence check below handles that case.
    except BaseException as exc:
        result["errors"].append("stop: " + repr(exc))
    if process is not None:
        try:
            try:
                process.wait(timeout=30)
            except subprocess.TimeoutExpired:
                process.terminate()
                process.wait(timeout=10)
            result["launcher_reaped"] = True
        except BaseException as exc:
            result["launcher_reaped"] = False
            result["errors"].append("launcher: " + repr(exc))
    try:
        remaining = subprocess.check_output(
            ["docker", "ps", "--all", "--filter", f"name=^/{name}$", "--format", "{{.ID}}"],
            text=True, timeout=15).strip()
        result["container_absent"] = not remaining
        if remaining:
            result["errors"].append("owned container remains after stop")
    except BaseException as exc:
        result["container_absent"] = False
        result["errors"].append("absence verification: " + repr(exc))
    result["passed"] = not result["errors"] and result["container_absent"]
    return result


def postflight(folder, image, started, safe_to_probe):
    result = {"errors": [], "kernel_passed": False, "gpu_health": "skipped"}
    try:
        journal = subprocess.check_output(
            ["journalctl", "-k", "--since", started, "--no-pager"], text=True, timeout=20)
        (folder / "kernel-postflight.log").write_text(journal)
        result["kernel_passed"] = not bool(FAULT.search(journal))
        if not result["kernel_passed"]:
            result["errors"].append("kernel fault detected; GPU health skipped")
    except BaseException as exc:
        result["errors"].append("kernel postflight: " + repr(exc))
    if safe_to_probe and result["kernel_passed"]:
        try:
            gpu_health(folder, image)
            result["gpu_health"] = "passed"
        except BaseException as exc:
            result["gpu_health"] = "failed"
            result["errors"].append("GPU health: " + repr(exc))
        finally:
            result["health_cleanup"] = cleanup_container("pr45-review-health")
            if not result["health_cleanup"]["passed"]:
                result["errors"].append("GPU health container cleanup failed")
    else:
        result["skip_reason"] = "unsafe teardown or kernel check"
    result["passed"] = not result["errors"] and result["gpu_health"] == "passed"
    return result


def run_arm(args, arm):
    folder = args.out / arm
    folder.mkdir(exist_ok=False)
    image = IMAGES["gdn" if arm.startswith("gdn-") else "baseline" if arm == "baseline" else "candidate"]
    container = "pr45-review-" + arm
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    env = dict(os.environ, IMAGE=image, EXPECTED_IMAGE_ID=image,
               MODEL_DIR=str(args.model_dir), VLLM_CACHE_DIR=str(folder / "cache"),
               MAX_MODEL_LEN="4096", MAX_NUM_SEQS="4", MAX_NUM_BATCHED_TOKENS="1024",
               CONTAINER_NAME=container, SERVED_MODEL_NAME="pr45-review", PORT="18124")
    probe_only = arm in ("candidate-no-compile", "candidate-target-only", "gdn-target-only")
    target_only = arm in ("candidate-target-only", "gdn-target-only",
                          "gdn-target-strict", "gdn-target-strict-repeat")
    if probe_only:
        env["COMPILATION_CONFIG"] = '{"mode":0,"cudagraph_mode":"NONE"}'
    if target_only:
        env["SPECULATIVE_CONFIG"] = "null"
    record = {"arm": arm, "image": image, "started_utc": started,
              "max_model_len": 4096, "max_num_seqs": 4, "max_num_batched_tokens": 1024,
              "status": "running", "performance_promotion": False,
              "strict_workload_run": not probe_only, "compilation_disabled": probe_only,
              "speculative_disabled": target_only, "gdn_phase_guard": arm.startswith("gdn-")}
    (folder / "run.json").write_text(json.dumps(record, indent=2) + "\n")
    print(f"START {arm}: {image}", flush=True)
    primary_error = None
    process = None
    kernel_fault_seen = False
    with (folder / "server.log").open("w") as log:
        try:
            process = subprocess.Popen(["bash", str(RECIPE / "run-w8a16-mtp1-strict-server.sh")],
                                       env=env, stdout=log, stderr=subprocess.STDOUT)
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
                        kernel_fault_seen = True
                        raise RuntimeError("new kernel fault; aborting GPU campaign")
                    next_journal = time.monotonic() + 20
                try:
                    with urllib.request.urlopen("http://127.0.0.1:18124/health", timeout=2):
                        break
                except OSError:
                    time.sleep(3)
            else:
                raise TimeoutError("server did not become ready within 900 seconds")
            print(f"READY {arm}; running " + ("diagnostic probes only" if probe_only else "complete strict workload, canaries and probes"), flush=True)
            bench_env = dict(env, OUT_DIR=str(folder / "strict"), BASE_URL="http://127.0.0.1:18124",
                             MODEL_NAME="pr45-review", PROFILE_LABEL="pr45-" + arm,
                             ATTEMPT_LABEL=arm)
            if not probe_only:
                if arm.startswith("gdn-"):
                    subprocess.run(["python3", str(PACKET / "probe_endpoint.py"),
                                    "--base-url", "http://127.0.0.1:18124", "--model", "pr45-review",
                                    "--out", str(folder / "probes-before-quality.json")],
                                   timeout=600, check=True)
                with (folder / "strict.log").open("w") as bench_log:
                    subprocess.run(["bash", str(RECIPE / "bench-w8a16-mtp1-strict.sh")], env=bench_env,
                                   stdout=bench_log, stderr=subprocess.STDOUT, timeout=900, check=True)
            subprocess.run(["python3", str(PACKET / "probe_endpoint.py"),
                            "--base-url", "http://127.0.0.1:18124", "--model", "pr45-review",
                            "--out", str(folder / "probes.json")], timeout=600, check=True)
            record["status"] = "passed_probes" if probe_only else "passed_workload_and_probes"
        except BaseException as exc:
            primary_error = exc
            record["error"] = repr(exc)
        finally:
            record["cleanup"] = cleanup_container(container, process)
            record["cleanup_passed"] = record["cleanup"]["passed"]
            record["kernel_fault_seen_during_startup"] = kernel_fault_seen
            record["postflight"] = postflight(folder, image, started,
                                              record["cleanup_passed"] and not kernel_fault_seen)
            record["postflight_passed"] = record["postflight"]["passed"]
            passed = primary_error is None and record["cleanup_passed"] and record["postflight_passed"]
            record.update(status="passed" if passed else "failed", campaign_stage_complete=passed)
            record["finished_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
            (folder / "run.json").write_text(json.dumps(record, indent=2) + "\n")
            print(f"END {arm}: {record['status']}", flush=True)
    if primary_error is not None:
        raise primary_error.with_traceback(primary_error.__traceback__)
    if record["status"] != "passed":
        raise RuntimeError("cleanup or postflight failed; see run.json; no further launches")


def gpu_health(folder, image):
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
