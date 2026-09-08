#!/usr/bin/env bash
# The targeted identity experiment: run the batch full of the prompts that actually flip.
#
# The whole-suite divergence rate is about 0.7% of requests, which is why 20 passes of 64 users gave
# the control only 9 events and nothing reached significance. That rate is not uniform - it is near
# zero on most prompts and about 6% on the twelve that carried all 25 observed divergences.
#
# Filling the 64 slots with those twelve instead (about five copies each) raises the expected yield
# from roughly 0.45 events per pass to about 1.7, so 20 passes gives around 34 events per arm rather
# than 9. Keeping all twelve rather than 64 copies of the single worst site trades a little yield for
# a result that rests on a dozen independent ties instead of one.
#
# --verbatim-prompts is required: the harness normally appends a per-slot case suffix, which would
# change the prompt and remove the very tie under study.
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

arm() { # $1=RUN  $2=rowwise  $3=serialnorm
  idle
  LANE=qwen35-9b-w4a16 MODEL_DIR=$M9 MODEL_MANIFEST=$N9 QUANT=compressed-tensors \
    IMAGE="$BOTH" IMAGE_ID="$BOTH_ID" \
    EXPECTED_XPU_COMMUNICATOR_SHA256="$COMM" EXPECTED_IR_LAYERNORM_SHA256="$IRLN" \
    ROWWISE_ALLREDUCE_MAX_ROWS="$2" RMSNORM_SERIAL_ROWS="$3" \
    RUN="$1" TP=2 DEPTH=3 GRAPH=1 DRAFT_HEAD=1 STAGES="ladders" \
    LADDER_SUITE=$repo/experiments/qwen35-9b-b70/data/2026-09-08-fragile-tie-site-suite-v1.json \
    LADDER_EXTRA_ARGS="--verbatim-prompts" \
    LADDER_CONCURRENCY=64 LADDER_REPEATS=20 \
    ROOT=/mnt/fast-ai/bench-results/qwen35-9b-w4a16-tp2-fragile-$1 \
    bash "$H" > "$W/qwen35-9b-fragile-$1-wrapper.log" 2>&1
  echo "fragile arm $1 (rowwise=$2 serialnorm=$3) exit=$? $(date --iso-8601=seconds)" >> "$W/fragile-sites.log"
}

arm f0 0 0
arm f1 64 64
echo "fragile-site chain done $(date --iso-8601=seconds)" >> "$W/fragile-sites.log"
