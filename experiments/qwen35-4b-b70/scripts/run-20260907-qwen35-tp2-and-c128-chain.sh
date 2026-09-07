#!/usr/bin/env bash
# Two campaigns the published Qwen3.5 matrix has not covered:
#   A) 4B W4A16 on two cards. The 4B family packet records TP1 only. The 9B gained 52% from the second card; a model this
#      small may instead lose to the collective, which is a result either way.
#   B) 9B W4A16 one card, identity ladder past 64 users. Every published rung through c64 is exact in both passes, so the
#      ceiling is untested. Capture sizes are raised with the ladder so no rung falls back to eager.
set -uo pipefail
repo=/home/steve/b70-optimization-lab; H=$repo/experiments/qwen35-9b-b70/scripts/run-20260907-qwen35-campaign.sh
W=/mnt/fast-ai/bench-results/chain-logs; mkdir -p "$W"
M4=/home/steve/llm-models/qwen35-4b-w4a16; N4=$repo/experiments/qwen35-4b-b70/manifests/model-direct-redhatai-qwen35-4b-w4a16-7a613872.json
M9=/home/steve/llm-models/qwen35-9b-w4a16; N9=$repo/experiments/qwen35-9b-b70/manifests/model-direct-redhatai-qwen35-9b-w4a16-a398088c.json
idle() { while pgrep -f 'run-20260907-qwen35-campaign[.]sh' >/dev/null; do sleep 30; done; sleep 20; }

idle
LANE=qwen35-4b-w4a16 MODEL_DIR=$M4 MODEL_MANIFEST=$N4 QUANT=compressed-tensors \
  RUN=t1 TP=2 DEPTH=3 GRAPH=1 DRAFT_HEAD=1 STAGES="strict ladders" \
  bash "$H" > "$W/qwen35-4b-w4a16-t1-tp2-wrapper.log" 2>&1

idle
LANE=qwen35-9b-w4a16 MODEL_DIR=$M9 MODEL_MANIFEST=$N9 QUANT=compressed-tensors \
  RUN=x1 TP=1 DEPTH=3 GRAPH=1 DRAFT_HEAD=1 STAGES="ladders" \
  CAPTURE_SIZES=1,2,3,4,5,6,8,10,15,16,20,25,30,32,40,50,60,64,80,96,112,128 CAPTURE_MAX=128 \
  LADDER_CONCURRENCY=1,2,4,8,16,32,64,96,128 LADDER_MNS=128 LADDER_MBT=1024 \
  bash "$H" > "$W/qwen35-9b-w4a16-x1-c128-wrapper.log" 2>&1

echo "chain done $(date --iso-8601=seconds)" >> "$W/tp2-and-c128-chain.done"
