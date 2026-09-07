#!/usr/bin/env bash
# Qwen3.5-9B Q8_0 on llama.cpp SYCL, one B70: the second runtime for a model the lab already serves through vLLM, run
# on the same strict 12-prompt completions suite so the two are directly comparable. No speculation: this GGUF carries
# no MTP head, so it is the like-for-like partner of the vLLM MTP0 numbers (W4A16 64.33, FP8 50.18 tok/s).
#   RUN (label), GPU_INDEX (default 0), PORT (default 19620), REPEATS (default 2 fresh servers, for the identity gate)
set -uo pipefail
repo=/home/steve/b70-optimization-lab; cd $repo
RUN=${RUN:?set RUN}; GPU_INDEX=${GPU_INDEX:-0}; PORT=${PORT:-19620}; REPEATS=${REPEATS:-2}
model=${MODEL:-/mnt/fast-ai/llm-models/qwen35-9b-q8-gguf/Qwen3.5-9B-Q8_0.gguf}
server=${LLAMA_SERVER:-/home/steve/src/llama.cpp-neural-download-20260822/build-sycl-aot-bmg-g31/bin/llama-server}
suite=${SUITE:-$repo/repro/qwen36-27b-autoround-int4-b70/realistic-suite-v1.json}
root=${ROOT:-/mnt/fast-ai/bench-results/qwen35-9b-q8-llamacpp-tp1-20260907-$RUN}
mkdir -p "$root"; [[ -e "$root/started-at.txt" ]] && { echo "root already used: $root" >&2; exit 1; }
date --iso-8601=seconds > "$root/started-at.txt"
log() { printf '[q35q8 %s] %s\n' "$(date +%H:%M:%S)" "$*" | tee -a "$root/campaign.log"; }
[[ -x $server ]] || { log "ABORT: no llama-server at $server"; exit 2; }
[[ -f $model ]]  || { log "ABORT: no model at $model"; exit 2; }
log "server=$server"; log "model=$model ($(stat -c %s "$model") bytes)"
sha=$(sha256sum "$model" | cut -d' ' -f1); log "model sha256=$sha"
[[ $sha == 809626574d0cb43d4becfa56169980da2bb448f2299270f7be443cb89d0a6ae4 ]] || { log "ABORT: model digest does not match the pinned unsloth/Qwen3.5-9B-GGUF file"; exit 2; }
for i in $(seq 1 "$REPEATS"); do
  dir=$root/attempt-$i; mkdir -p "$dir"
  log "attempt $i: launching"
  GPU_INDEX=$GPU_INDEX PORT=$PORT MODEL="$model" MODEL_ALIAS=qwen35-9b-q8 LLAMA_SERVER="$server" \
    CTX_SIZE=${CTX_SIZE:-8192} BATCH_SIZE=1024 UBATCH_SIZE=${UBATCH_SIZE:-1024} N_PARALLEL=1 THREADS=8 \
    FLASH_ATTN=on CACHE_TYPE_K=f16 CACHE_TYPE_V=f16 REASONING=off LLAMA_DEVICES=SYCL$GPU_INDEX \
    OUT_DIR="$dir" bash scripts/serve-rapid-llamacpp-model.sh > "$dir/server.log" 2>&1 &
  pid=$!
  ok=0; for _ in $(seq 1 120); do curl -fsS "http://127.0.0.1:$PORT/health" >/dev/null 2>&1 && { ok=1; break; }; kill -0 $pid 2>/dev/null || break; sleep 5; done
  if [[ $ok != 1 ]]; then log "attempt $i: server did not become healthy"; grep -iE 'error|failed|unknown|unsupported' "$dir/server.log" | tail -5 | tee -a "$root/campaign.log"; kill $pid 2>/dev/null; continue; fi
  log "attempt $i: healthy"
  python3 scripts/bench-openai-realistic-suite.py --base-url "http://127.0.0.1:$PORT" --model qwen35-9b-q8 \
    --api-mode completions --suite "$suite" --max-tokens 512 --metric-tokens 100 --seed 42 --timeout 900 \
    --request-extra-json '{"temperature":0,"top_p":1}' --out "$dir/realistic-suite.json" > "$dir/bench.stdout" 2>&1
  log "attempt $i: $(python3 -c "
import json;d=json.load(open('$dir/realistic-suite.json'));s=d['summary']
print('class_balanced=%.3f median=%.3f p10=%.3f ttft_ms=%.1f gate=%s' % (s['class_balanced_tok_s_1_100_intervals_after_ttft']['median'], s['tok_s_1_100_after_ttft']['median'], s['tok_s_1_100_after_ttft']['p10'], s['ttft_ms']['median'], d['realistic_final_gate'].get('passed')))" 2>&1 | tail -1)"
  kill $pid 2>/dev/null; wait $pid 2>/dev/null; sleep 10
done
if [[ $REPEATS -ge 2 && -f $root/attempt-1/realistic-suite.json && -f $root/attempt-2/realistic-suite.json ]]; then
  log "repeat identity: $(python3 -c "
import json
a=json.load(open('$root/attempt-1/realistic-suite.json'))['rows']; b=json.load(open('$root/attempt-2/realistic-suite.json'))['rows']
ba={r['prompt_id']:r.get('sha256') for r in b}
print('%d/%d prompts byte-identical between the two fresh servers' % (sum(1 for r in a if ba.get(r['prompt_id'])==r.get('sha256')), len(a)))")"
fi
date --iso-8601=seconds > "$root/campaign-end.txt"; log "campaign complete"
