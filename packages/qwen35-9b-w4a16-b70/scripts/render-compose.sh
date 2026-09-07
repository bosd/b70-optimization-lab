#!/usr/bin/env bash
# Regenerate compose.yaml from the recipe launcher, so the container packet cannot drift away from
# the configuration that produced the measured result.
#
# It runs the real launcher (image contract check, model manifest verification and all) behind a
# docker shim that captures the final `docker run` argv instead of starting a container, once per
# card-count profile, then renders both into compose.yaml. Nothing is started and no GPU is touched.
#
#   MODEL_DIR   verified RedHatAI/Qwen3.5-9B-quantized.w4a16 directory (required)
#   IMAGE       local tag of the R276 image (defaults to the recipe's tag; must be present)
set -euo pipefail
here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd); pkg=$(cd -- "${here}/.." && pwd); repo=$(cd -- "${pkg}/../.." && pwd)
model_dir=${MODEL_DIR:?set MODEL_DIR to the verified RedHatAI/Qwen3.5-9B-quantized.w4a16 directory}
image=${IMAGE:-neural-download/vllm-openai-xpu:qwen38-int4-gdn-spec-group-sync-free-r276}
digest_ref=${DIGEST_REF:-ghcr.io/steveseguin/vllm-openai-xpu-qwen38-int4@sha256:521eb277c0733f8c2ce47aea1bb98ed576c6f1ad63bf5baf22d38fc07abf54ad}

work=$(mktemp -d); trap 'rm -rf "${work}"' EXIT
mkdir -p "${work}/shim"
cat > "${work}/shim/docker" <<'SHIM'
#!/usr/bin/env bash
# Capture only the docker run whose --name is CAPTURE_CONTAINER_NAME; everything else (image
# contract checks, inspect, ps) goes to the real binary untouched.
real=/usr/bin/docker
if [[ "${1:-}" == "run" && -n "${CAPTURE_CONTAINER_NAME:-}" ]]; then
  for a in "$@"; do
    if [[ "$a" == "${CAPTURE_CONTAINER_NAME}" ]]; then
      : >"${DOCKER_ARGV_CAPTURE:?}"; for x in "$@"; do printf '%s\0' "$x" >>"${DOCKER_ARGV_CAPTURE}"; done
      exit 0
    fi
  done
fi
exec "$real" "$@"
SHIM
chmod +x "${work}/shim/docker"

# A port that is never bound: the shim intercepts before docker sees it, and the value is replaced
# by ${PORT} in the rendered file, so it must not collide with a running lane if the shim is bypassed.
render_port=18199
for prof in one two; do
  if [[ "${prof}" == one ]]; then tp=1; mask=0; else tp=2; mask=0,1; fi
  name=qwen35-9b-w4a16-render-${prof}
  PATH="${work}/shim:${PATH}" DOCKER_ARGV_CAPTURE="${work}/argv-${prof}.nul" CAPTURE_CONTAINER_NAME="${name}" \
    env MODEL_DIR="${model_dir}" IMAGE="${image}" VLLM_CACHE_DIR="${work}/cache-${prof}" \
        CONTAINER_NAME="${name}" SERVED_MODEL_NAME=qwen35-9b-w4a16 \
        TENSOR_PARALLEL_SIZE="${tp}" XPU_DEVICE_MASK="${mask}" PORT="${render_port}" \
        MTP_DEPTH=3 XPU_GRAPH=1 DRAFT_HEAD_INT4=1 \
        MAX_MODEL_LEN=8192 MAX_NUM_SEQS=16 MAX_NUM_BATCHED_TOKENS=1024 \
        bash "${repo}/repro/qwen35-9b-w4a16-b70/scripts/run-qwen35-9b-w4a16-server.sh" >"${work}/render-${prof}.log" 2>&1
  [[ -s "${work}/argv-${prof}.nul" ]] || { echo "capture failed for ${prof}; see ${work}/render-${prof}.log" >&2; cp "${work}/render-${prof}.log" /tmp/ 2>/dev/null || true; exit 1; }
done

python3 "${here}/render-compose.py" "${work}/argv-one.nul" "${work}/argv-two.nul" "${pkg}/compose.yaml" "${digest_ref}"
