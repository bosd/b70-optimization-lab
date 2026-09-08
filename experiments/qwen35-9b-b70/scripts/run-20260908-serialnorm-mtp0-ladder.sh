#!/usr/bin/env bash
# The measurement the s2 run was supposed to make and did not.
#
# s2's speculative ladder was a valid comparison and showed serialising the norm's variance reduction
# is free up to 64 rows. Its no-speculation ladder was not: that path runs through run-server.sh,
# which did not forward the knob, so both arms were unserialised and the 0.0% deltas meant nothing.
# run-server.sh now forwards it, and this re-runs the no-speculation ladder alone.
#
# It is the rung that matters most: without speculation the step is exactly one row per user, so at
# 64 users the reduction is split 64 ways - the largest engaged row count this threshold allows, and
# the case the 33x microbenchmark ratio was measured at.
set -uo pipefail
repo=/home/steve/b70-optimization-lab; H=$repo/experiments/qwen35-9b-b70/scripts/run-20260907-qwen35-campaign.sh
W=/mnt/fast-ai/bench-results/chain-logs; mkdir -p "$W"
M9=/home/steve/llm-models/qwen35-9b-w4a16; N9=$repo/experiments/qwen35-9b-b70/manifests/model-direct-redhatai-qwen35-9b-w4a16-a398088c.json
IMG=neural-download/vllm-openai-xpu:qwen38-int4-r276-serialnorm-diag
IID=sha256:f9faea7ed47d76fb22ec0e0122691a7eb2e06dac879a7d152b5b73331fb34bb2
IRLN=5cfe3e54b6d19b371ce5379ad0ba7309881b10fc4aedfaec54096d0a34488a54

while pgrep -f 'run-20260907-qwen35-campaign[.]sh' >/dev/null \
   || docker ps --format '{{.Names}}' | grep -qE 'qwen3[58]|gemma'; do sleep 60; done
sleep 30

# DEPTH=0 makes the ladder stage launch the no-speculation server only, so the mtp0 arm is the one
# that runs and the knob reaches it through run-server.sh.
LANE=qwen35-9b-w4a16 MODEL_DIR=$M9 MODEL_MANIFEST=$N9 QUANT=compressed-tensors \
  IMAGE="$IMG" IMAGE_ID="$IID" EXPECTED_IR_LAYERNORM_SHA256="$IRLN" \
  RMSNORM_SERIAL_ROWS=64 \
  RUN=s3 TP=2 DEPTH=3 GRAPH=1 DRAFT_HEAD=1 STAGES="ladders" \
  ROOT=/mnt/fast-ai/bench-results/qwen35-9b-w4a16-tp2-serialnorm-s3 \
  bash "$H" > "$W/qwen35-9b-serialnorm-s3-wrapper.log" 2>&1
echo "serialnorm mtp0 ladder exit=$? $(date --iso-8601=seconds)" >> "$W/serialnorm-chain.log"
