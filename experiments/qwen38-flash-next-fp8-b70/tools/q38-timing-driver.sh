#!/usr/bin/env bash
# Generic exact-2K timing driver for q38-launch-frozen-attempt.sh: wait for 'Application startup complete'
# (resolving the run directory on every poll), send two exact-depth 2K requests, then stop the server.
#   q38-timing-driver.sh <attempt> <port> <mtp0|mtp1|mtp2>
attempt=${1:?attempt}; port=${2:?port}; mtp=${3:?mtp0|mtp1|mtp2}
repo=/home/steve/llm-optimizations; python=/home/steve/.venvs/vllm-xpu/bin/python; B=/mnt/usb-models/bench-results/qwen38-flash-next-fp8-b70
polls=0; RD=""
while true; do
  RD=$(ls -d $B/*${mtp}-4352-ple-only-r1-attempt${attempt} 2>/dev/null | grep -v supervisor | head -1)
  [ -n "$RD" ] && grep -q 'Application startup complete' "$RD/server.log" 2>/dev/null && break
  sleep 10; polls=$((polls+1)); [ $polls -gt 300 ] && { echo "driver: server never became ready"; exit 2; }
  ps -eo args | grep -q "[r]un-q38-a${attempt}-host-controlled.sh" || { echo "driver: host wrapper gone"; exit 3; }
done
[ -e "$RD/exact-depth-2k-r1.json" ] && { echo "driver: refusing: $RD already holds a result"; exit 4; }
sleep 20
for r in 1 2; do
  echo "driver: request r$r start at $(date +%H:%M:%S)"
  timeout --signal=TERM --kill-after=10s 1500s "$python" "$repo/scripts/bench-openai-token-depth-suite.py" --execute --fixture "$repo/data/qwen27-exact-depth/qwen38-flash-next-bcd9f01-exact-depth-v1.json" --depth 2048 --context-capacity 4352 --base-url http://127.0.0.1:$port --model qwen38-flash-next-fp8-tp4 --response-adapter vllm --timeout 1400 --out "$RD/exact-depth-2k-r$r.json" > "$RD/exact-depth-2k-r$r.log" 2>&1; rc=$?
  echo "driver: exact-2k r$r rc=$rc $(jq -c '{o:.response.output_token_ids_sha256[0:12], t:.response.text_sha256[0:12], r:.metric_window.conventional_99_interval_tok_s}' "$RD/exact-depth-2k-r$r.json" 2>/dev/null)"
  sleep 15
done
echo "STOP after a${attempt} timing" > /tmp/q38-${mtp}-ple-only-a${attempt}.stop
echo "driver: battery exit=$rc at $(date +%H:%M:%S)"
