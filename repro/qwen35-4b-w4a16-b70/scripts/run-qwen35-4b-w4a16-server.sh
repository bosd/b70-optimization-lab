#!/usr/bin/env bash
# Qwen3.5-4B W4A16 (INT4 weights, FP16 activations) on Intel Arc Pro B70. Thin wrapper over the shared Qwen3.5 launcher:
# only the model directory and its manifest differ from the FP8 route. vLLM's compressed-tensors path selects
# CompressedTensorsWNA16, which on XPU is the lab's wNa16 kernel (_xpu_C.int4_gemm_w4a16) carrying the fixed-K two-tier
# W4A16 strategy. That kernel is row-count invariant, which is why this route stays byte-exact at every concurrency
# through 64 users where the FP8 route does not. No config relabel is needed (unlike AutoRound weights on the 27B lane).
#   MODEL_DIR  the downloaded RedHatAI/Qwen3.5-4B-quantized.w4a16 directory (required; verified against the manifest)
#   MTP_DEPTH / TENSOR_PARALLEL_SIZE / XPU_GRAPH / DRAFT_HEAD_INT4 / PORT and the rest: see the shared launcher.
set -euo pipefail
script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd); repo_root=$(cd -- "${script_dir}/../../.." && pwd)
export MODEL_MANIFEST=${MODEL_MANIFEST:-${script_dir}/../manifests/model-direct-redhatai-qwen35-4b-w4a16-7a613872.json}
export CONTAINER_NAME=${CONTAINER_NAME:-qwen35-4b-w4a16-mtp${MTP_DEPTH:-3}} SERVED_MODEL_NAME=${SERVED_MODEL_NAME:-qwen35-4b-w4a16-mtp${MTP_DEPTH:-3}}
exec "${repo_root}/repro/qwen35-9b-fp8-b70/scripts/run-qwen35-9b-fp8-server.sh"
