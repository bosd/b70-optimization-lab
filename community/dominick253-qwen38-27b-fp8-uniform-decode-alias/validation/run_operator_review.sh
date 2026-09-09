#!/usr/bin/env bash
# Historical R50 localization, not a current-upstream or performance claim.
set -euo pipefail
root=$(git rev-parse --show-toplevel)
out=${1:?usage: bash run_operator_review.sh NEW_ABSOLUTE_OUTPUT_DIR}
[[ "$out" == /mnt/fast-ai/bench-results/pr45-* && ! -e "$out" ]] || exit 2
image=sha256:4bb40c00826d3adeb577306afe8d7a6836eaef61d33e1e97a99b74ea85081fb4
exec 9>/tmp/b70-pr45-review.lock
flock -n 9
[[ -z "$(docker ps -q)" ]] || exit 3
mkdir "$out"
started=$(date -u +%FT%TZ)
health() {
  timeout 120 docker run --rm --name pr45-operator-health --network none --ipc host \
    --device /dev/dri --group-add render --cap-add SYS_PTRACE --security-opt label=disable \
    -w / --volume "$root:/repo:ro" --env PYTHON=/opt/venv/bin/python \
    --env ROOT=/repo --env PHYSICAL_DEVICES=0,1 --env XCCL_DEVICES=0,1 \
    --env CCL_ZE_IPC_EXCHANGE=pidfd --env TIMEOUT_S=60 --entrypoint bash "$image" \
    /repo/scripts/check-qwen36-xpu-xccl-health.sh
}
cleanup() {
  rc=$?
  trap - EXIT
  set +e
  # Only names owned by this locked campaign; no model service is launched.
  docker stop --timeout 10 pr45-operator-census pr45-operator-sweep >/dev/null 2>&1
  journalctl -k --since "$started" --no-pager > "$out/kernel.log"
  journal_rc=$?
  remaining=$(docker ps -q --filter 'name=^/pr45-operator-(census|sweep|health)$')
  absence_rc=$?
  if [[ $journal_rc != 0 || $absence_rc != 0 || -n "$remaining" ]] || rg -qi 'Fault response|CAT error|engine reset|GPU reset|soft lockup|Timedout job' "$out/kernel.log"; then
    printf 'Active health skipped: unsafe teardown or journal.\n' > "$out/postflight.log"
    rc=1
  else
    health > "$out/postflight.log" 2>&1
    health_rc=$?
    docker stop --timeout 10 pr45-operator-health >/dev/null 2>&1
    [[ $health_rc == 0 ]] || rc=1
  fi
  printf '%s\n' "$rc" > "$out/exit-code.txt"
  exit "$rc"
}
trap cleanup EXIT
docker image inspect "$image" > "$out/image.json"
health > "$out/preflight.log" 2>&1
for kind in census sweep; do
  if [[ "$kind" == census ]]; then
    script=qwen38-fp8-kernel-batch-invariance-census.py
    extra=(--skip-lm-head --skip-auxiliary)
  else
    script=qwen38-fp8-kernel-determinism-sweep.py
    extra=()
  fi
  timeout 360 docker run --rm --name "pr45-operator-$kind" --network none \
    --ipc host --device /dev/dri --group-add render --memory 10g --memory-swap 12g \
    --workdir / --env VLLM_TARGET_DEVICE=xpu --env ZE_AFFINITY_MASK=0 \
    --volume "$root/experiments/qwen38-27b-b70/scripts:/work:ro" \
    --volume "$out:/out" --entrypoint /opt/venv/bin/python "$image" \
    "/work/$script" --out "/out/$kind.json" "${extra[@]}" > "$out/$kind.log" 2>&1
done
