#!/usr/bin/env bash
# The serial-norm cost at concurrency, which the s1 arm never reached.
#
# s1 answered the single-request half already: with the variance reduction serialised, the strict
# suite measured 172.438 tok/s against 172.241/172.422 with it off - no measurable cost, because at
# one request and depth 3 the verify step is only 4 rows, so serialising means 4 sub-reductions
# instead of 1. The 33x microbenchmark ratio does not reach the end-to-end number there.
#
# Concurrency is where it should. At 64 users the no-speculation step is 64 rows, so serialising is
# 64 sub-reductions per norm per layer. That is the figure that decides whether this is a usable fix.
# s1 aborted before its ladder stage when a server hit the container memory cap during weight load,
# so this runs the ladders alone against the s0 ladders already measured.
#
# Identity is deliberately not the question here: the c64 metric is intermittent and two passes
# cannot resolve an intervention (see the 2026-09-08 intermittency note). This is a cost measurement.
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

LANE=qwen35-9b-w4a16 MODEL_DIR=$M9 MODEL_MANIFEST=$N9 QUANT=compressed-tensors \
  IMAGE="$IMG" IMAGE_ID="$IID" EXPECTED_IR_LAYERNORM_SHA256="$IRLN" \
  RMSNORM_SERIAL_ROWS=64 \
  RUN=s2 TP=2 DEPTH=3 GRAPH=1 DRAFT_HEAD=1 STAGES="ladders" \
  ROOT=/mnt/fast-ai/bench-results/qwen35-9b-w4a16-tp2-serialnorm-s2 \
  bash "$H" > "$W/qwen35-9b-serialnorm-s2-wrapper.log" 2>&1
echo "serialnorm ladders exit=$? $(date --iso-8601=seconds)" >> "$W/serialnorm-chain.log"
