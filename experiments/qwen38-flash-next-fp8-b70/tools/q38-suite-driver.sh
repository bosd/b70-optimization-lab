#!/usr/bin/env bash
# Realistic-suite driver for a frozen attempt: wait for the server, run the shared strict suite
# (rapid-model-snapshots-b70 realistic v1, chat mode, deterministic sampling), write the result
# into the lab data dir, then stop the server.
#   q38-suite-driver.sh <attempt> <port> <mtp0|mtp1|mtp2> <out-json>
attempt=${1:?attempt}; port=${2:?port}; mtp=${3:?mtp0|mtp1|mtp2}; out=${4:?out json}
repo=/home/steve/llm-optimizations; python=/home/steve/.venvs/vllm-xpu/bin/python; B=/mnt/usb-models/bench-results/qwen38-flash-next-fp8-b70
polls=0; RD=""
while true; do
  RD=$(ls -d $B/*${mtp}-4352-ple-only-r1-attempt${attempt} 2>/dev/null | grep -v supervisor | head -1)
  [ -n "$RD" ] && grep -q 'Application startup complete' "$RD/server.log" 2>/dev/null && break
  sleep 10; polls=$((polls+1)); [ $polls -gt 300 ] && { echo "driver: server never became ready"; exit 2; }
  ps -eo args | grep -q "[r]un-q38-a${attempt}-host-controlled.sh" || { echo "driver: host wrapper gone"; exit 3; }
done
[ -e "$out" ] && { echo "driver: refusing: $out already exists"; exit 4; }
sleep 20
echo "driver: suite start at $(date +%H:%M:%S) -> $out"
timeout --signal=TERM --kill-after=10s 5400s "$python" "$repo/scripts/bench-openai-realistic-suite.py" \
  --base-url "http://127.0.0.1:${port}" --model qwen38-flash-next-fp8-tp4 --api-mode chat \
  --suite "$repo/repro/rapid-model-snapshots-b70/realistic-suite-v1.json" --max-tokens 512 --metric-tokens 100 \
  --seed 20260609 --timeout 900 --return-token-ids \
  --request-extra-json '{"chat_template_kwargs":{"enable_thinking":false},"seed":20260609,"temperature":0,"top_p":1.0}' \
  --out "$out"; rc=$?
echo "driver: suite rc=$rc $(jq -c '{gate:.realistic_final_gate.passed, tps:.summary.class_balanced_tok_s_1_100_intervals_after_ttft.median}' "$out" 2>/dev/null)"
echo "STOP after a${attempt} suite" > /tmp/q38-${mtp}-ple-only-a${attempt}.stop
echo "driver: suite exit=$rc at $(date +%H:%M:%S)"
