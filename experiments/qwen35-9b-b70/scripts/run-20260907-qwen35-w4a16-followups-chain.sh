#!/usr/bin/env bash
# Follow-ups for the two W4A16 lanes: the two-card row the 9B INT4 route is missing (w3), and the 2K-32K real-content
# context ladders neither INT4 lane has yet (w4 on the 9B, v2 on the 4B). Same harness, same gates.
set -uo pipefail
repo=/home/steve/b70-optimization-lab; H=$repo/experiments/qwen35-9b-b70/scripts/run-20260907-qwen35-campaign.sh; W=/mnt/fast-ai/bench-results
M9=/home/steve/llm-models/qwen35-9b-w4a16; N9=$repo/experiments/qwen35-9b-b70/manifests/model-direct-redhatai-qwen35-9b-w4a16-a398088c.json
M4=/home/steve/llm-models/qwen35-4b-w4a16; N4=$repo/experiments/qwen35-4b-b70/manifests/model-direct-redhatai-qwen35-4b-w4a16-7a613872.json
idle() { while pgrep -f 'run-20260907-qwen35-campaign[.]sh' >/dev/null || docker ps --format '{{.Names}}' | grep -qE 'qwen3[58]'; do sleep 30; done; sleep 10; }
idle; LANE=qwen35-9b-w4a16 MODEL_DIR=$M9 MODEL_MANIFEST=$N9 QUANT=compressed-tensors RUN=w3 TP=2 DEPTH=3 GRAPH=1 DRAFT_HEAD=1 STAGES="strict ladders" bash $H > $W/qwen35-9b-w4a16-w3-wrapper.log 2>&1
idle; LANE=qwen35-9b-w4a16 MODEL_DIR=$M9 MODEL_MANIFEST=$N9 QUANT=compressed-tensors RUN=w4 TP=1 DEPTH=3 GRAPH=1 DRAFT_HEAD=1 STAGES="depth32k" bash $H > $W/qwen35-9b-w4a16-w4-wrapper.log 2>&1
idle; LANE=qwen35-4b-w4a16 MODEL_DIR=$M4 MODEL_MANIFEST=$N4 QUANT=compressed-tensors RUN=v2 TP=1 DEPTH=3 GRAPH=1 DRAFT_HEAD=1 STAGES="depth32k" bash $H > $W/qwen35-4b-w4a16-v2-wrapper.log 2>&1
echo W4A16-FOLLOWUPS-DONE
