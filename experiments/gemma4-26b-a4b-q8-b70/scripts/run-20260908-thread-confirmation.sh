#!/usr/bin/env bash
# Promote or drop the 16-draft-thread finding on evidence rather than on two runs.
#
# The record passes --spec-draft-threads 32, which is twice this host's 16 hardware threads. Two runs at 16 measured
# 3.06% above the six-sample 32-thread mean and differed from each other by 0.43%, against a 2.394% coefficient of
# variation at 32. That is enough to be interesting and not enough to change a recipe's recommended setting, which is
# what this is for: four more runs at 16 threads, for six.
#
# If it holds, the two-card host class gets a documented setting. If it does not, the note stays a note.
set -uo pipefail
LAB=/home/steve/b70-optimization-lab; D=/home/steve/llm-models/gemma4-26b-a4b-it-q8-gguf
C=/home/steve/llm-models/gemma4-record-container-2026.0
Q4C=$D/MTP/gemma-4-26B-A4B-it-Q4_0-MTP.container-2026.0.gguf
W=/mnt/fast-ai/bench-results/chain-logs; mkdir -p "$W"; cd "$LAB"
log() { echo "$(date -u +%FT%TZ) $*" | tee -a "$W/gemma4-thread-confirmation.log"; }

# Built by substitution, not printf with the string as the format: it starts with "--parallel", which printf reads as
# an option and refuses. That bug silently produced empty arguments once already.
record_args() {
  printf -- '--parallel 1 --cache-ram 0 --spec-type draft-mtp --spec-draft-model %s --spec-draft-n-max 3 --spec-draft-device SYCL0 --spec-draft-ngl all --spec-draft-type-k f16 --spec-draft-type-v f16 --spec-draft-n-min 2 --spec-draft-p-min 0.0475 --no-spec-draft-backend-sampling --spec-draft-threads %s --spec-draft-threads-batch %s --ctx-checkpoints 0' "$Q4C" "$1" "$1"
}

idle() {
  while pgrep -f 'run-20260907-qwen35-campaign[.]sh' >/dev/null \
     || pgrep -f 'run-20260908-followups-chain[.]sh' >/dev/null \
     || docker ps --format '{{.Names}}' | grep -qE 'qwen3[58]|gemma'; do sleep 60; done
  sleep 30
}

for i in 3 4 5 6; do
  idle
  stamp=$(date -u +%Y%m%dT%H%M%SZ)
  log "start threads16-run${i}"
  LLAMA_SERVER=$C/bin/llama-server MODEL=$D/gemma-4-26B-A4B-it-UD-Q8_K_XL.gguf \
  GPU_INDEX=0 PORT=19350 LABEL="gemma4-q8-gpu0-threads16-run${i}-${stamp}" \
  EXTRA_LLAMA_ARGS="$(record_args 16)" \
  CTX_SIZE=32768 FLASH_ATTN=on GGML_SYCL_ENABLE_VMM=1 \
  CANARY_REPEATS=128 MAX_TOKENS=512 REALISTIC_GATE=1 REALISTIC_METRIC_TOKENS=100 READINESS_TIMEOUT_S=900 \
    bash repro/gemma4-26b-a4b-q8-b70/run-vdr2-selecteddown-record.sh > "$W/gemma4-threads16-run${i}-${stamp}.log" 2>&1
  log "end threads16-run${i} exit=$?"
done
log "thread confirmation done"
