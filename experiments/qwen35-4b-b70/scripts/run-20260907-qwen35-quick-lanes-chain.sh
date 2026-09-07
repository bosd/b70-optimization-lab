#!/usr/bin/env bash
# Quick lanes after the 9B FP8 work: Qwen3.5-4B FP8-dynamic (q1) and Qwen3.5-9B W4A16 (w1), both one card,
# MTP depth 3 with the draft-only INT4 lm_head, full decode-only capture, strict pairs plus c1-c64 identity ladders.
# Both use the generalized harness in ../../qwen35-9b-b70/scripts/run-20260907-qwen35-campaign.sh.
set -uo pipefail
repo=/home/steve/b70-optimization-lab; H=$repo/experiments/qwen35-9b-b70/scripts/run-20260907-qwen35-campaign.sh; W=/mnt/fast-ai/bench-results
wait_idle() { while pgrep -f 'run-20260907-qwen35-campaign[.]sh' >/dev/null || docker ps --format '{{.Names}}' | grep -qE 'qwen3[58]'; do sleep 30; done; sleep 10; }
until [ -f /home/steve/llm-models/qwen35-4b-fp8-dynamic/REVISION ]; do sleep 60; done
wait_idle
LANE=qwen35-4b-fp8 MODEL_DIR=/home/steve/llm-models/qwen35-4b-fp8-dynamic \
  MODEL_MANIFEST=$repo/experiments/qwen35-4b-b70/manifests/model-direct-redhatai-qwen35-4b-fp8-dynamic-397b7ba4.json \
  QUANT=compressed-tensors RUN=q1 TP=1 DEPTH=3 GRAPH=1 DRAFT_HEAD=1 STAGES="strict ladders" bash $H > $W/qwen35-4b-q1-wrapper.log 2>&1
until [ -f /home/steve/llm-models/qwen35-9b-w4a16/REVISION ]; do sleep 60; done
wait_idle
LANE=qwen35-9b-w4a16 MODEL_DIR=/home/steve/llm-models/qwen35-9b-w4a16 \
  MODEL_MANIFEST=$repo/experiments/qwen35-9b-b70/manifests/model-direct-redhatai-qwen35-9b-w4a16-a398088c.json \
  QUANT=compressed-tensors RUN=w1 TP=1 DEPTH=3 GRAPH=1 DRAFT_HEAD=1 STAGES="strict ladders" bash $H > $W/qwen35-9b-w4a16-w1-wrapper.log 2>&1
echo QUICK-LANES-DONE
