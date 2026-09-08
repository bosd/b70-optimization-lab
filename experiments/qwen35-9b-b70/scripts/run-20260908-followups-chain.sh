#!/usr/bin/env bash
# Three follow-ups, serialized on the cards.
#
# A) 4B two-card firm-up. The t1 depth-3 pair measured 240.615 and 227.533 tok/s, a 5.8% spread against 0.13% on the
#    one-card pair of the same lane. That is too soft a center to submit, so this adds a second strict campaign for
#    four servers total.
# B) Gemma draftless arm. Four fresh servers at the record settings returned 0/12 matching outputs. The lane serves
#    with a Q4_0 MTP draft verified by the Q8 target, so that measurement cannot say whether the target alone is
#    reproducible. Two servers with speculation off answer it.
# C) 4B depth sweep. The 4B inherited depth 3 from the FP8 sweep exactly as the 9B did, and on the 9B every depth
#    from 3 to 6 turned out lossless while FP8 held only at 3. Same prediction, cheap model.
set -uo pipefail
repo=/home/steve/b70-optimization-lab; H=$repo/experiments/qwen35-9b-b70/scripts/run-20260907-qwen35-campaign.sh
W=/mnt/fast-ai/bench-results/chain-logs; mkdir -p "$W"
M4=/home/steve/llm-models/qwen35-4b-w4a16; N4=$repo/experiments/qwen35-4b-b70/manifests/model-direct-redhatai-qwen35-4b-w4a16-7a613872.json
D=/home/steve/llm-models/gemma4-26b-a4b-it-q8-gguf; C=/home/steve/llm-models/gemma4-record-container-2026.0
cd "$repo"
log() { echo "$(date -u +%FT%TZ) $*" | tee -a "$W/followups-20260908.log"; }

idle() {
  while pgrep -f 'run-20260907-qwen35-campaign[.]sh' >/dev/null \
     || docker ps --format '{{.Names}}' | grep -qE 'qwen3[58]|gemma'; do sleep 60; done
  sleep 30
}

# A) 4B two-card firm-up
idle; log "A: 4B TP2 strict firm-up (campaign t2)"
LANE=qwen35-4b-w4a16 MODEL_DIR=$M4 MODEL_MANIFEST=$N4 QUANT=compressed-tensors \
  RUN=t2 TP=2 DEPTH=3 GRAPH=1 DRAFT_HEAD=1 STAGES="strict" \
  bash "$H" > "$W/qwen35-4b-w4a16-t2-tp2-wrapper.log" 2>&1
log "A: exit=$?"

# B) Gemma draftless: same gate, speculation removed
idle; log "B: gemma draftless arm"
for i in 1 2; do
  stamp=$(date -u +%Y%m%dT%H%M%SZ)
  LLAMA_SERVER=$C/bin/llama-server MODEL=$D/gemma-4-26B-A4B-it-UD-Q8_K_XL.gguf \
  GPU_INDEX=0 PORT=19350 LABEL="gemma4-q8-gpu0-draftless-run${i}-${stamp}" \
  EXTRA_LLAMA_ARGS="--parallel 1 --cache-ram 0 --ctx-checkpoints 0" \
  CTX_SIZE=32768 FLASH_ATTN=on GGML_SYCL_ENABLE_VMM=1 \
  CANARY_REPEATS=128 MAX_TOKENS=512 REALISTIC_GATE=1 REALISTIC_METRIC_TOKENS=100 READINESS_TIMEOUT_S=900 \
    bash repro/gemma4-26b-a4b-q8-b70/run-vdr2-selecteddown-record.sh \
      > "$W/gemma4-draftless-run${i}-${stamp}.log" 2>&1
  log "B: draftless run${i} exit=$?"
  while docker ps --format '{{.Names}}' | grep -q gemma; do sleep 20; done
done

# C) 4B depth sweep
for d in 4 5 6; do
  idle; log "C: 4B depth ${d}"
  LANE=qwen35-4b-w4a16 MODEL_DIR=$M4 MODEL_MANIFEST=$N4 QUANT=compressed-tensors \
    RUN="e${d}" TP=1 DEPTH="$d" GRAPH=1 DRAFT_HEAD=1 STAGES="strict" \
    bash "$H" > "$W/qwen35-4b-w4a16-depth${d}-wrapper.log" 2>&1
  log "C: depth ${d} exit=$?"
done
log "followups chain done"
