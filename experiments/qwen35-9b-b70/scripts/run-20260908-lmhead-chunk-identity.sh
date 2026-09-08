#!/usr/bin/env bash
# Does making the vocabulary projection row-invariant remove the divergence?
#
# The FP16 lm_head is bitwise invariant to batch size at 32 rows and below and switches reduction
# from 33 up, moving every row's logits by as much as 3.9e-3. It is the last matmul before the
# argmax and sits outside the fixed-K predicate, so nothing was keeping it invariant - and every
# previous intervention arm left it untouched, controls included.
#
# Chunking it to 32 rows is verified in-container to make every row's logits bitwise equal to its
# single-row value, which is what the identity oracle computes. So unlike the norm, this candidate is
# value-preserving by construction: if it removes the divergence it needs no re-qualification.
#
# Fragile-site suite at the sizing that already yields 23 control events per 1280 requests, both arms
# on the same overlay image so only the knob differs.
set -uo pipefail
repo=/home/steve/b70-optimization-lab; H=$repo/experiments/qwen35-9b-b70/scripts/run-20260907-qwen35-campaign.sh
W=/mnt/fast-ai/bench-results/chain-logs; mkdir -p "$W"
M9=/home/steve/llm-models/qwen35-9b-w4a16; N9=$repo/experiments/qwen35-9b-b70/manifests/model-direct-redhatai-qwen35-9b-w4a16-a398088c.json
IMG=neural-download/vllm-openai-xpu:qwen38-int4-r276-lmheadchunk-diag
IID=sha256:ca4f8731800f977a331c0393876c3f5c8ab1163616a3e832ca0270acd6547d18
LOGITS=7f8a93e50974653d92cf301587b15ba427191bf53655ae77a23c9a48dbb9b673

idle() {
  while pgrep -f 'run-20260907-qwen35-campaign[.]sh' >/dev/null \
     || docker ps --format '{{.Names}}' | grep -qE 'qwen3[58]|gemma'; do sleep 60; done
  sleep 30
}

arm() { # $1=RUN  $2=lm_head row chunk
  idle
  LANE=qwen35-9b-w4a16 MODEL_DIR=$M9 MODEL_MANIFEST=$N9 QUANT=compressed-tensors \
    IMAGE="$IMG" IMAGE_ID="$IID" EXPECTED_LOGITS_PROCESSOR_SHA256="$LOGITS" \
    LM_HEAD_ROW_CHUNK="$2" \
    RUN="$1" TP=2 DEPTH=3 GRAPH=1 DRAFT_HEAD=1 STAGES="ladders" \
    LADDER_SUITE=$repo/experiments/qwen35-9b-b70/data/2026-09-08-fragile-tie-site-suite-v1.json \
    LADDER_EXTRA_ARGS="--verbatim-prompts" \
    LADDER_CONCURRENCY=64 LADDER_REPEATS=20 \
    ROOT=/mnt/fast-ai/bench-results/qwen35-9b-w4a16-tp2-lmhead-$1 \
    bash "$H" > "$W/qwen35-9b-lmhead-$1-wrapper.log" 2>&1
  echo "lmhead arm $1 (row_chunk=$2) exit=$? $(date --iso-8601=seconds)" >> "$W/lmhead-chunk.log"
}

arm L0 0
arm L1 32
echo "lmhead chunk chain done $(date --iso-8601=seconds)" >> "$W/lmhead-chunk.log"
