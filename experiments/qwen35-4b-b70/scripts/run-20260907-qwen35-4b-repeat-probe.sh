#!/usr/bin/env bash
# The 4B failed its base gate (two fresh MTP0 servers, 11/12: code-review flips at token 284). Two more MTP0 pairs
# (q2, q3) give six samples of the same configuration, to tell a stable two-mode split from a rare random flip.
set -uo pipefail
# Start only after the quick-lanes chain has finished both of its campaigns.
until grep -q QUICK-LANES-DONE /mnt/fast-ai/bench-results/qwen35-quick-lanes-chain.log 2>/dev/null; do sleep 60; done
repo=/home/steve/b70-optimization-lab; H=$repo/experiments/qwen35-9b-b70/scripts/run-20260907-qwen35-campaign.sh; W=/mnt/fast-ai/bench-results
wait_idle() { while pgrep -f 'run-20260907-qwen35-campaign[.]sh' >/dev/null || docker ps --format '{{.Names}}' | grep -qE 'qwen3[58]'; do sleep 30; done; sleep 10; }
for run in q2 q3; do
  wait_idle
  LANE=qwen35-4b-fp8 MODEL_DIR=/home/steve/llm-models/qwen35-4b-fp8-dynamic \
    MODEL_MANIFEST=$repo/experiments/qwen35-4b-b70/manifests/model-direct-redhatai-qwen35-4b-fp8-dynamic-397b7ba4.json \
    QUANT=compressed-tensors RUN=$run TP=1 DEPTH=3 GRAPH=1 DRAFT_HEAD=1 STAGES="strict" bash $H > $W/qwen35-4b-$run-wrapper.log 2>&1
done
echo REPEAT-PROBE-DONE
