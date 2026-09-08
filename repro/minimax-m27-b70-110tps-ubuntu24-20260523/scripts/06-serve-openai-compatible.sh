#!/usr/bin/env bash
set -euo pipefail

extra_args=("$@")
if [ -n "${VLLM_KV_OFFLOADING_SIZE:-}" ]; then
  extra_args+=(--kv-offloading-size "$VLLM_KV_OFFLOADING_SIZE")
fi
if [ "${VLLM_NO_SCHEDULER_RESERVE_FULL_ISL:-0}" = "1" ]; then
  extra_args+=(--no-scheduler-reserve-full-isl)
fi
THIS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "$THIS_DIR/configs/runtime-env.sh"
source "$VENV/bin/activate"
# Intel's vars.sh dereferences SETVARS_CALL and OCL_ICD_FILENAMES, which are unbound when
# it is sourced directly, so under `set -u` it aborts -- and with both streams muted the
# abort is silent. It also *replaces* LD_LIBRARY_PATH rather than prepending, which drops
# the venv's torch libraries and leaves torch.xpu.device_count() at 0 on a machine with
# four working cards. So: relax -u for the vendor script only, fail loudly if it fails, and
# re-apply the search path runtime-env.sh set before it.
_q38_ld_before="${LD_LIBRARY_PATH:-}"
set +u
source /opt/intel/oneapi/compiler/2025.3/env/vars.sh >/dev/null 2>&1 || {
  echo "FAIL: could not source the oneAPI compiler environment" >&2; exit 1; }
set -u
export LD_LIBRARY_PATH="${_q38_ld_before}${_q38_ld_before:+:}${LD_LIBRARY_PATH:-}"
unset _q38_ld_before

if [ ! -d "$MODEL" ]; then
  echo "Model directory is missing: $MODEL" >&2
  exit 1
fi

exec vllm serve "$MODEL" \
  --host "${VLLM_HOST:-0.0.0.0}" \
  --port "${VLLM_PORT:-8000}" \
  --trust-remote-code \
  --dtype float16 \
  --tensor-parallel-size 4 \
  --distributed-executor-backend mp \
  --max-model-len "${VLLM_MAX_MODEL_LEN:-32768}" \
  --max-num-batched-tokens "${VLLM_MAX_NUM_BATCHED_TOKENS:-512}" \
  --max-num-seqs "${VLLM_MAX_NUM_SEQS:-1}" \
  --gpu-memory-utilization "${VLLM_GPU_MEMORY_UTILIZATION:-0.95}" \
  --block-size 256 \
  --no-enable-prefix-caching \
  --compilation-config '{"use_inductor_graph_partition":true,"compile_sizes":[1],"cudagraph_mode":"PIECEWISE"}' \
  "${extra_args[@]}"
