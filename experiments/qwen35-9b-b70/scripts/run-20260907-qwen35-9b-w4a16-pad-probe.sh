#!/usr/bin/env bash
# Does the W4A16 determinism pad buy exactness at 32-64 users on the 9B, and at what cost? Same configuration as w1
# with VLLM_XPU_W4A16_DETERMINISM_PAD=1, ladders only. On the 27B the pad roughly doubled cost above 128 rows.
set -uo pipefail
repo=/home/steve/b70-optimization-lab; H=$repo/experiments/qwen35-9b-b70/scripts/run-20260907-qwen35-campaign.sh; W=/mnt/fast-ai/bench-results
until grep -q REPEAT-PROBE-DONE $W/qwen35-4b-repeat-probe.log 2>/dev/null; do sleep 60; done
while pgrep -f 'run-20260907-qwen35-campaign[.]sh' >/dev/null || docker ps --format '{{.Names}}' | grep -qE 'qwen3[58]'; do sleep 30; done; sleep 10
LANE=qwen35-9b-w4a16 MODEL_DIR=/home/steve/llm-models/qwen35-9b-w4a16 \
  MODEL_MANIFEST=$repo/experiments/qwen35-9b-b70/manifests/model-direct-redhatai-qwen35-9b-w4a16-a398088c.json \
  QUANT=compressed-tensors RUN=w2 TP=1 DEPTH=3 GRAPH=1 DRAFT_HEAD=1 W4A16_PAD=1 STAGES="ladders" bash $H > $W/qwen35-9b-w4a16-w2-wrapper.log 2>&1
echo PAD-PROBE-DONE
