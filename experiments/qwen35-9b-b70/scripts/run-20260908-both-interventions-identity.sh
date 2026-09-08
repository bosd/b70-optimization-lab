#!/usr/bin/env bash
# Are the two shape-dependent steps jointly necessary?
#
# Tested alone, neither removes the two-card identity divergence. The cross-card all-reduce did not
# (2 divergent against 1 in 254 requests - underpowered, but no signal), and serialising the norm's
# variance reduction does not (7 against 9 in 1280 requests, properly powered: a difference of 2
# events against a Poisson standard error of 4).
#
# Both are real shape dependences - XCCL's reduction varies with message size, and the norm's
# variance differs on 2-3% of rows once a batch reaches 16 - so the natural remaining hypothesis is
# that each alone leaves the other free to perturb a near-tie, and only the pair closes it. That pair
# has never been run. This is one image carrying both overlays, against the p0 control already
# measured at 9 divergent in 1280.
#
# Same sizing as the powered arm: 20 passes at 64 users, 1280 requests. If the pair removes the
# divergence, a near-zero count against a control expectation of 9 will show; if it does not, that is
# a third negative and the search should move to what else varies with batch shape.
set -uo pipefail
repo=/home/steve/b70-optimization-lab; H=$repo/experiments/qwen35-9b-b70/scripts/run-20260907-qwen35-campaign.sh
W=/mnt/fast-ai/bench-results/chain-logs; mkdir -p "$W"
M9=/home/steve/llm-models/qwen35-9b-w4a16; N9=$repo/experiments/qwen35-9b-b70/manifests/model-direct-redhatai-qwen35-9b-w4a16-a398088c.json
IMG=neural-download/vllm-openai-xpu:qwen38-int4-r276-both-diag
IID=sha256:fc15efaeff995aa0f482b02d6b338bf3ec29878ae76daa08c13cd4fe94609b1f
COMM=97c75747e93e557dae3db632f3aab2cc38649eddb561316737cb596816c9f2fa
IRLN=5cfe3e54b6d19b371ce5379ad0ba7309881b10fc4aedfaec54096d0a34488a54

while pgrep -f 'run-20260907-qwen35-campaign[.]sh' >/dev/null \
   || docker ps --format '{{.Names}}' | grep -qE 'qwen3[58]|gemma'; do sleep 60; done
sleep 30

LANE=qwen35-9b-w4a16 MODEL_DIR=$M9 MODEL_MANIFEST=$N9 QUANT=compressed-tensors \
  IMAGE="$IMG" IMAGE_ID="$IID" \
  EXPECTED_XPU_COMMUNICATOR_SHA256="$COMM" EXPECTED_IR_LAYERNORM_SHA256="$IRLN" \
  ROWWISE_ALLREDUCE_MAX_ROWS=64 RMSNORM_SERIAL_ROWS=64 \
  RUN=p2 TP=2 DEPTH=3 GRAPH=1 DRAFT_HEAD=1 STAGES="ladders" \
  LADDER_CONCURRENCY=64 LADDER_REPEATS=20 \
  ROOT=/mnt/fast-ai/bench-results/qwen35-9b-w4a16-tp2-identitypower-p2 \
  bash "$H" > "$W/qwen35-9b-identitypower-p2-wrapper.log" 2>&1
echo "arm p2 (both interventions) exit=$? $(date --iso-8601=seconds)" >> "$W/identity-power.log"
