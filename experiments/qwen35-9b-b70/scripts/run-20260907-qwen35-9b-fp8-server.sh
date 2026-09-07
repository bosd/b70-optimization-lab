#!/usr/bin/env bash
# Qwen3.5-9B FP8-dynamic (RedHatAI, rev 790f0576) quick lane: one B70, the lab's R276 vLLM XPU image, FP8 launcher with
# compressed-tensors quantization. Usage: DEPTH=<0|1|2|3> EAGER=<0|1> GRAPH=<0|1> qwen35-9b-smoke.sh   (foreground server; run under nohup)
set -uo pipefail
LAB=/home/steve/b70-optimization-lab; cd $LAB
DEPTH=${DEPTH:-1}; EAGER=${EAGER:-0}; GRAPH=${GRAPH:-1}; PORT=${PORT:-18131}; STAMP=$(date -u +%Y%m%dT%H%M%SZ)
if [ "$DEPTH" = 0 ]; then LAUNCHER=run-server.sh; SPEC='{}'; else LAUNCHER=run-w8a16-mtp1-server.sh; SPEC="{\"method\":\"qwen3_5_mtp\",\"num_speculative_tokens\":$DEPTH}"; fi
CACHE=/mnt/fast-ai/vllm-cache/qwen35-9b-fp8-${STAMP}-d${DEPTH}-e${EAGER}
IMAGE=neural-download/vllm-openai-xpu:qwen38-int4-gdn-spec-group-sync-free-r276 EXPECTED_IMAGE_ID=sha256:521eb277c0733f8c2ce47aea1bb98ed576c6f1ad63bf5baf22d38fc07abf54ad \
MODEL_DIR=/home/steve/llm-models/qwen35-9b-fp8-dynamic MODEL_MANIFEST=/home/steve/llm-models/qwen35-9b-fp8-dynamic-manifest.json VLLM_CACHE_DIR=$CACHE \
CONTAINER_NAME=qwen35-9b-fp8-smoke PORT=$PORT SERVED_MODEL_NAME=qwen35-9b-fp8 SPECULATIVE_CONFIG="$SPEC" \
TENSOR_PARALLEL_SIZE=1 XPU_DEVICE_MASK=${XPU_DEVICE_MASK:-0} QUANTIZATION=compressed-tensors VLLM_XPU_FP8_BLOCK_W8A16=0 \
MAX_MODEL_LEN=${MAX_MODEL_LEN:-8192} MAX_NUM_SEQS=${MAX_NUM_SEQS:-16} MAX_NUM_BATCHED_TOKENS=${MAX_NUM_BATCHED_TOKENS:-2048} ENFORCE_EAGER=$EAGER VLLM_XPU_ENABLE_XPU_GRAPH=$GRAPH \
CONTAINER_MEMORY=12g CONTAINER_MEMORY_SWAP=20g \
  bash repro/qwen38-27b-fp8-vllm-tp2-asrock-b70/$LAUNCHER
