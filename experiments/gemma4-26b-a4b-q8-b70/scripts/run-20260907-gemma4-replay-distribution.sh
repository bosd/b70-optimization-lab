#!/usr/bin/env bash
# Two questions about the Gemma 4 26B Q8 record replay on this two-card host, both currently answered by assertion
# rather than by measurement.
#
# A) The recipe says the 2026-09-07 replays land "within the known several-percent spread" under the 124.977 record.
#    The best of three was 116.346, which is 6.9% short, while the lane's own documented repeatability is a 2.324%
#    run-median CV and a 4.409% p90 pairwise delta. Three runs cannot separate a wide tail from a systematic
#    difference. This adds four more replays at the exact record settings, for six on this host.
#
# B) The record passes --spec-draft-threads 32 --spec-draft-threads-batch 32. This host's CPU is an 8-core/16-thread
#    EPYC 9015, so 32 draft threads are oversubscribed by 2x here; the four-B70 measuring host is a different machine.
#    If oversubscription is costing decode, lowering the count is free speed on this host. Speculative decoding is
#    verified by the Q8 target, so a thread count cannot change the answers, only the rate.
set -uo pipefail
LAB=/home/steve/b70-optimization-lab; D=/home/steve/llm-models/gemma4-26b-a4b-it-q8-gguf
C=/home/steve/llm-models/gemma4-record-container-2026.0
MODEL=$D/gemma-4-26B-A4B-it-UD-Q8_K_XL.gguf
Q4C=$D/MTP/gemma-4-26B-A4B-it-Q4_0-MTP.container-2026.0.gguf
W=/mnt/fast-ai/bench-results/chain-logs; mkdir -p "$W"
cd "$LAB"
log() { echo "$(date -u +%FT%TZ) $*" | tee -a "$W/gemma4-replay-distribution.log"; }

# never share the cards with a vLLM lane or another llama.cpp gate
# Wait for the whole qwen chain, not just the campaign currently running: the chain has idle gaps between its
# campaigns, and starting a Gemma gate in one of those would put two measured lanes on the same cards.
idle() {
  while pgrep -f 'run-20260907-qwen35-tp2-and-c128-chain[.]sh' >/dev/null \
     || pgrep -f 'run-20260907-qwen35-campaign[.]sh' >/dev/null \
     || docker ps --format '{{.Names}}' | grep -qE 'qwen3[58]'; do sleep 60; done
  sleep 30
}

record_args="--parallel 1 --cache-ram 0 --spec-type draft-mtp --spec-draft-model $Q4C --spec-draft-n-max 3 --spec-draft-device SYCL0 --spec-draft-ngl all --spec-draft-type-k f16 --spec-draft-type-v f16 --spec-draft-n-min 2 --spec-draft-p-min 0.0475 --no-spec-draft-backend-sampling --spec-draft-threads %s --spec-draft-threads-batch %s --ctx-checkpoints 0"

# run_arm <label> <draft_threads>
run_arm() {
  local label=$1 threads=$2 stamp; stamp=$(date -u +%Y%m%dT%H%M%SZ)
  idle
  log "start ${label} threads=${threads}"
  LLAMA_SERVER=$C/bin/llama-server MODEL=$MODEL \
  GPU_INDEX=0 PORT=19350 LABEL="gemma4-q8-gpu0-${label}-${stamp}" \
  EXTRA_LLAMA_ARGS="$(printf "$record_args" "$threads" "$threads")" \
  CTX_SIZE=32768 FLASH_ATTN=on GGML_SYCL_ENABLE_VMM=1 \
  CANARY_REPEATS=128 MAX_TOKENS=512 REALISTIC_GATE=1 REALISTIC_METRIC_TOKENS=100 READINESS_TIMEOUT_S=900 \
    bash repro/gemma4-26b-a4b-q8-b70/run-vdr2-selecteddown-record.sh \
      > "$W/gemma4-${label}-${stamp}.log" 2>&1
  log "end   ${label} rc=$? label=gemma4-q8-gpu0-${label}-${stamp}"
}

# A: four more replays at the record's own 32 draft threads
for i in 3 4 5 6; do run_arm "distrib32-run${i}" 32; done
# B: draft-thread sweep, two runs each
for i in 1 2; do run_arm "threads16-run${i}" 16; done
for i in 1 2; do run_arm "threads08-run${i}" 8; done

log "gemma replay distribution chain done"
