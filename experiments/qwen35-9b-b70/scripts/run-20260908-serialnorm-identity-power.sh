#!/usr/bin/env bash
# Does serialising the norm's variance reduction actually close the two-card identity gap?
#
# Every previous attempt at this question used two passes per arm and could not answer it. The
# control distribution at 64 users spans 63/64 and 64/64 across campaigns - six control passes read
# four with one miss and two with none - so a single pass carries almost no information. The fix is
# to stop collapsing 64 requests into one bit and count divergent requests over many passes instead.
#
# Sizing, from that control distribution: about 4 misses in 384 control requests, roughly 1%. Twenty
# passes at 64 users is 1280 requests per arm, so the control should show on the order of 13 misses
# and an arm that truly removes them should show none. That separates the two; two passes never could.
#
# Both arms run the same overlay image, so the only difference is the knob. Concurrency is pinned to
# 64 because without speculation that is one row per user, the largest row count the 64-row threshold
# engages at. The speculative ladder runs too and is inert there (256 rows), which makes it a second
# control confirming the arms are otherwise identical.
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
    RUN="$1" TP=2 DEPTH=3 GRAPH=1 DRAFT_HEAD=1 STAGES="ladders" \
    LADDER_CONCURRENCY=64 LADDER_REPEATS=20 \
    ROOT=/mnt/fast-ai/bench-results/qwen35-9b-w4a16-tp2-identitypower-$1 \
    bash "$H" > "$W/qwen35-9b-identitypower-$1-wrapper.log" 2>&1
  echo "arm $1 (serial_rows=$2) exit=$? $(date --iso-8601=seconds)" >> "$W/identity-power.log"
}

arm p0 0
arm p1 64
echo "identity power chain done $(date --iso-8601=seconds)" >> "$W/identity-power.log"
