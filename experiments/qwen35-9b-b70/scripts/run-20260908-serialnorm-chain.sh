#!/usr/bin/env bash
# What does preserving the norm's single-row oracle cost end to end?
#
# The norm's variance reduction is row-count dependent, and of every formulation measured only
# serialising it one row at a time reproduces the single-row result exactly - which is the result the
# identity ladders compare against. In isolation that costs about 33x on the reduction, but the
# reduction is a small part of a decode step, so the end-to-end figure is the one that decides
# whether this is a usable fix or only a diagnosis. Nobody has measured it.
#
# Two arms on the same overlay image so the rebuild is not the variable:
#   s0  serialisation off  - must reproduce R276's published numbers and gates
#   s1  serialisation on   - the cost, and whether the two-card ladder improves
#
# TP2 because that is where identity is currently lost; the one-card route is already exact through
# 64 users and has nothing to gain here.
set -uo pipefail
repo=/home/steve/b70-optimization-lab; H=$repo/experiments/qwen35-9b-b70/scripts/run-20260907-qwen35-campaign.sh
W=/mnt/fast-ai/bench-results/chain-logs; mkdir -p "$W"
M9=/home/steve/llm-models/qwen35-9b-w4a16; N9=$repo/experiments/qwen35-9b-b70/manifests/model-direct-redhatai-qwen35-9b-w4a16-a398088c.json
IMG=neural-download/vllm-openai-xpu:qwen38-int4-r276-serialnorm-diag
IID=sha256:f9faea7ed47d76fb22ec0e0122691a7eb2e06dac879a7d152b5b73331fb34bb2
IRLN=5cfe3e54b6d19b371ce5379ad0ba7309881b10fc4aedfaec54096d0a34488a54

idle() {
  while pgrep -f 'run-20260907-qwen35-campaign[.]sh' >/dev/null \
     || docker ps --format '{{.Names}}' | grep -qE 'qwen3[58]|gemma'; do sleep 60; done
  sleep 30
}

arm() { # $1=RUN  $2=serial rows
  idle
  LANE=qwen35-9b-w4a16 MODEL_DIR=$M9 MODEL_MANIFEST=$N9 QUANT=compressed-tensors \
    IMAGE="$IMG" IMAGE_ID="$IID" EXPECTED_IR_LAYERNORM_SHA256="$IRLN" \
    RMSNORM_SERIAL_ROWS="$2" \
    RUN="$1" TP=2 DEPTH=3 GRAPH=1 DRAFT_HEAD=1 STAGES="strict ladders" \
    ROOT=/mnt/fast-ai/bench-results/qwen35-9b-w4a16-tp2-serialnorm-$1 \
    bash "$H" > "$W/qwen35-9b-serialnorm-$1-wrapper.log" 2>&1
  echo "arm $1 (serial_rows=$2) exit=$?" >> "$W/serialnorm-chain.log"
}

arm s0 0
arm s1 64
echo "serialnorm chain done $(date --iso-8601=seconds)" >> "$W/serialnorm-chain.log"
