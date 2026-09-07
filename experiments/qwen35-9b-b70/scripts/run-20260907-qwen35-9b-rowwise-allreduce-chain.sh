#!/usr/bin/env bash
# Does the two-card identity loss come from the cross-card reduction rather than the GEMM?
#
# On one card the 9B W4A16 route is exact at every ladder rung through 64 users in both passes. On two cards the same
# kernel scores 63/64 at 64 users in both passes (campaign w3), and the 4B shows the same shape. The Flash-Next lane
# already established the mechanism that would explain it: XCCL's reduction order depends on message size, so an
# [M, N] all-reduce does not agree bit for bit with M separate [1, N] all-reduces, which makes a decode step's result
# depend on how many rows share it.
#
# R276 does not carry that lane's row-wise all-reduce, so this runs a diagnostic overlay image: R276 plus the row-wise
# communicator, pure Python, every pinned kernel digest unchanged and the replaced module declared to the image
# contract. Two arms on the same overlay isolate the variable:
#   r0  row-wise off  - must reproduce the control's 63/64, proving the overlay itself changes nothing
#   r1  row-wise on   - if 64 users becomes 64/64, the cross-card reduction is the cause
# Row-by-row reduction costs M collectives instead of one, so the r1 rate is the price of the naive fix, not a result.
set -uo pipefail
repo=/home/steve/b70-optimization-lab; H=$repo/experiments/qwen35-9b-b70/scripts/run-20260907-qwen35-campaign.sh
W=/mnt/fast-ai/bench-results/chain-logs; mkdir -p "$W"
M9=/home/steve/llm-models/qwen35-9b-w4a16; N9=$repo/experiments/qwen35-9b-b70/manifests/model-direct-redhatai-qwen35-9b-w4a16-a398088c.json
IMG=neural-download/vllm-openai-xpu:qwen38-int4-r276-rowwise-allreduce-diag
IID=sha256:30226665158aedffc34806565bf362eee1abb407350edf5303d21c46ba59ee46
COMM=97c75747e93e557dae3db632f3aab2cc38649eddb561316737cb596816c9f2fa

idle() {
  while pgrep -f 'run-20260907-qwen35-tp2-and-c128-chain[.]sh' >/dev/null \
     || pgrep -f 'run-20260907-gemma4-replay-distribution[.]sh' >/dev/null \
     || pgrep -f 'run-20260907-qwen35-campaign[.]sh' >/dev/null \
     || docker ps --format '{{.Names}}' | grep -qE 'qwen3[58]|gemma'; do sleep 60; done
  sleep 30
}

arm() { # $1=RUN label  $2=rowwise max rows
  idle
  LANE=qwen35-9b-w4a16 MODEL_DIR=$M9 MODEL_MANIFEST=$N9 QUANT=compressed-tensors \
    IMAGE="$IMG" IMAGE_ID="$IID" EXPECTED_XPU_COMMUNICATOR_SHA256="$COMM" \
    ROWWISE_ALLREDUCE_MAX_ROWS="$2" \
    RUN="$1" TP=2 DEPTH=3 GRAPH=1 DRAFT_HEAD=1 STAGES="ladders" \
    ROOT=/mnt/fast-ai/bench-results/qwen35-9b-w4a16-tp2-rowwise-$1 \
    bash "$H" > "$W/qwen35-9b-rowwise-$1-wrapper.log" 2>&1
  echo "arm $1 (rowwise=$2) exit=$?" >> "$W/rowwise-chain.log"
}

arm r0 0
arm r1 64
echo "rowwise chain done $(date --iso-8601=seconds)" >> "$W/rowwise-chain.log"
