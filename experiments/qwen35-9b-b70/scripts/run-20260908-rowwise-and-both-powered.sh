#!/usr/bin/env bash
# Re-run the two interventions that were never actually applied on the lane they were measured on.
#
# run-server.sh - the no-speculation path - forwarded neither the row-wise all-reduce knob nor the
# serialised-norm knob. The norm omission was found and fixed earlier; the row-wise one was not, so
# every no-speculation arm that claimed to test it was in fact the control. That includes the
# original r0/r1 comparison and the "both interventions" arm p2, whose container carried only the
# norm knob.
#
# Both are fixed now, and the harness aborts if a requested knob is missing from the container rather
# than producing a clean null. These are the real arms, at the same sizing as the powered control
# already measured at 9 divergent in 1280 requests:
#   q1  row-wise all-reduce alone
#   q2  row-wise all-reduce and serialised norm together
set -uo pipefail
repo=/home/steve/b70-optimization-lab; H=$repo/experiments/qwen35-9b-b70/scripts/run-20260907-qwen35-campaign.sh
W=/mnt/fast-ai/bench-results/chain-logs; mkdir -p "$W"
M9=/home/steve/llm-models/qwen35-9b-w4a16; N9=$repo/experiments/qwen35-9b-b70/manifests/model-direct-redhatai-qwen35-9b-w4a16-a398088c.json
BOTH=neural-download/vllm-openai-xpu:qwen38-int4-r276-both-diag
BOTH_ID=sha256:fc15efaeff995aa0f482b02d6b338bf3ec29878ae76daa08c13cd4fe94609b1f
COMM=97c75747e93e557dae3db632f3aab2cc38649eddb561316737cb596816c9f2fa
IRLN=5cfe3e54b6d19b371ce5379ad0ba7309881b10fc4aedfaec54096d0a34488a54

idle() {
  while pgrep -f 'run-20260907-qwen35-campaign[.]sh' >/dev/null \
     || docker ps --format '{{.Names}}' | grep -qE 'qwen3[58]|gemma'; do sleep 60; done
  sleep 30
}

# The combined image carries both overlays; each arm selects which knobs are on, so the image is
# constant and only the intervention varies.
arm() { # $1=RUN  $2=rowwise rows  $3=serial rows
  idle
  LANE=qwen35-9b-w4a16 MODEL_DIR=$M9 MODEL_MANIFEST=$N9 QUANT=compressed-tensors \
    IMAGE="$BOTH" IMAGE_ID="$BOTH_ID" \
    EXPECTED_XPU_COMMUNICATOR_SHA256="$COMM" EXPECTED_IR_LAYERNORM_SHA256="$IRLN" \
    ROWWISE_ALLREDUCE_MAX_ROWS="$2" RMSNORM_SERIAL_ROWS="$3" \
    RUN="$1" TP=2 DEPTH=3 GRAPH=1 DRAFT_HEAD=1 STAGES="ladders" \
    LADDER_CONCURRENCY=64 LADDER_REPEATS=20 \
    ROOT=/mnt/fast-ai/bench-results/qwen35-9b-w4a16-tp2-identitypower-$1 \
    bash "$H" > "$W/qwen35-9b-identitypower-$1-wrapper.log" 2>&1
  echo "arm $1 (rowwise=$2 serialnorm=$3) exit=$? $(date --iso-8601=seconds)" >> "$W/identity-power.log"
}

arm q1 64 0
arm q2 64 64
echo "rowwise/both powered chain done $(date --iso-8601=seconds)" >> "$W/identity-power.log"
