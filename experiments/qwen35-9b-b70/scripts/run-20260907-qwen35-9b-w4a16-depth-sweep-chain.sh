#!/usr/bin/env bash
# The W4A16 lane runs MTP depth 3 because the FP8 lane's sweep chose 3. It was never swept on this route, and there is
# a specific reason to expect a different answer.
#
# On FP8, depths 4, 5 and 6 were all withheld: each was repeat-exact (G2 12/12) but diverged from the MTP0 oracle on a
# third of the suite (G3 8/12), and none was faster than depth 3. A verify step at depth d processes d+1 rows, so
# changing the depth changes the GEMM's row count - and on FP8 the reduction varies with row count, which is the same
# mechanism that makes that route flip near-tie tokens as concurrency changes. The W4A16 kernel is row-count invariant
# by construction, so the prediction is that deeper drafts stay lossless here where they did not on FP8.
#
# Either outcome is worth having: if depth 4+ is lossless and faster, the lane has been leaving speed on the table; if
# it is lossless and slower, depth 3 is confirmed on its own evidence rather than inherited; if it is not lossless, the
# row-invariance story needs a correction. Strict stage only - the ladders are not what this asks about.
set -uo pipefail
repo=/home/steve/b70-optimization-lab; H=$repo/experiments/qwen35-9b-b70/scripts/run-20260907-qwen35-campaign.sh
W=/mnt/fast-ai/bench-results/chain-logs; mkdir -p "$W"
M9=/home/steve/llm-models/qwen35-9b-w4a16; N9=$repo/experiments/qwen35-9b-b70/manifests/model-direct-redhatai-qwen35-9b-w4a16-a398088c.json

idle() {
  while pgrep -f 'run-20260907-gemma4-replay-distribution[.]sh' >/dev/null \
     || pgrep -f 'run-20260907-qwen35-9b-rowwise-allreduce-chain[.]sh' >/dev/null \
     || pgrep -f 'run-20260907-qwen35-campaign[.]sh' >/dev/null \
     || docker ps --format '{{.Names}}' | grep -qE 'qwen3[58]|gemma'; do sleep 60; done
  sleep 30
}

for d in 4 5 6; do
  idle
  LANE=qwen35-9b-w4a16 MODEL_DIR=$M9 MODEL_MANIFEST=$N9 QUANT=compressed-tensors \
    RUN="d${d}" TP=1 DEPTH="$d" GRAPH=1 DRAFT_HEAD=1 STAGES="strict" \
    bash "$H" > "$W/qwen35-9b-w4a16-depth${d}-wrapper.log" 2>&1
  echo "depth $d exit=$?" >> "$W/w4a16-depth-sweep.log"
done
echo "w4a16 depth sweep done $(date --iso-8601=seconds)" >> "$W/w4a16-depth-sweep.log"
