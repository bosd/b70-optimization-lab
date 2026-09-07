#!/usr/bin/env bash
# The 4B FP8 route is not repeat-exact (q1 11/12, q2 9/12: three tie-prone prompts, two variants each, servers pick
# independently). The 9B showed the identity ceiling is a kernel property, so test the same model on the row-invariant
# W4A16 kernel: strict pair plus ladders (v1). Runs after the pad probe so the cards are never shared.
set -uo pipefail
repo=/home/steve/b70-optimization-lab; H=$repo/experiments/qwen35-9b-b70/scripts/run-20260907-qwen35-campaign.sh; W=/mnt/fast-ai/bench-results
until [ -f /home/steve/llm-models/qwen35-4b-w4a16/REVISION ]; do sleep 30; done
until grep -q PAD-PROBE-DONE $W/qwen35-9b-w4a16-pad-probe.log 2>/dev/null; do sleep 60; done
while pgrep -f 'run-20260907-qwen35-campaign[.]sh' >/dev/null || docker ps --format '{{.Names}}' | grep -qE 'qwen3[58]'; do sleep 30; done; sleep 10
LANE=qwen35-4b-w4a16 MODEL_DIR=/home/steve/llm-models/qwen35-4b-w4a16 \
  MODEL_MANIFEST=$repo/experiments/qwen35-4b-b70/manifests/model-direct-redhatai-qwen35-4b-w4a16-7a613872.json \
  QUANT=compressed-tensors RUN=v1 TP=1 DEPTH=3 GRAPH=1 DRAFT_HEAD=1 STAGES="strict ladders" bash $H > $W/qwen35-4b-w4a16-v1-wrapper.log 2>&1
echo 4B-W4A16-CHAIN-DONE
