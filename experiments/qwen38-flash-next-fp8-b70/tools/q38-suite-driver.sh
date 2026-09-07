#!/usr/bin/env bash
# Realistic-suite driver for a frozen attempt (the LocalMaxxing metric: A134/A182/A188/A189 flags,
# suite and seed): wait for the packet's server, run the fixed cold realistic suite once into the
# run dir (realistic-suite-v1-result.json/.log, as A227/A229), then stop the server.
#   q38-suite-driver.sh <attempt> <port> <mtp0|mtp1|mtp2>
set -euo pipefail
attempt=${1:?attempt}; port=${2:?port}; mtp=${3:?mtp0|mtp1|mtp2}
repo=/home/steve/llm-optimizations; python=/home/steve/.venvs/vllm-xpu/bin/python; B=/mnt/usb-models/bench-results/qwen38-flash-next-fp8-b70
rc_file="/tmp/q38-${mtp}-ple-only-a${attempt}.rc"; stop_file="/tmp/q38-${mtp}-ple-only-a${attempt}.stop"
deadline=$(( $(date +%s) + 2700 ))
until curl -fsS --max-time 5 "http://127.0.0.1:${port}/health" >/dev/null 2>&1; do
  [[ -f "$rc_file" ]] && { echo "driver: server exited before healthy (rc $(cat "$rc_file"))"; exit 1; }
  (( $(date +%s) < deadline )) || { echo "driver: server not healthy after 45 minutes"; exit 1; }
  sleep 15
done
RD=$(ls -d $B/*fullgraphdet-${mtp}-4352-ple-only-r1-attempt${attempt} 2>/dev/null | grep -v supervisor | head -1)
[[ -n "$RD" && -d "$RD" ]] || { echo "driver: no run dir for attempt ${attempt}"; exit 1; }
sleep 30
echo "driver: server healthy at $(date +%H:%M:%S); realistic suite once, cold, into $RD"
[[ ! -e "$RD/realistic-suite-v1-result.json" ]] || { echo "driver: refusing to overwrite the suite result"; exit 1; }
set +e
timeout --signal=TERM --kill-after=10s 1800s "$python" "$repo/scripts/bench-openai-realistic-suite.py" --base-url "http://127.0.0.1:${port}" --model qwen38-flash-next-fp8-tp4 --api-mode chat \
  --suite "$repo/repro/rapid-model-snapshots-b70/realistic-suite-v1.json" --max-tokens 512 --metric-tokens 100 --seed 20260609 --timeout 900 --return-token-ids \
  --request-extra-json '{"chat_template_kwargs":{"enable_thinking":false},"seed":20260609,"temperature":0,"top_p":1.0}' \
  --out "$RD/realistic-suite-v1-result.json" > "$RD/realistic-suite-v1-result.log" 2>&1; rc=$?
echo "driver: suite rc=$rc $(jq -c '{med:.summary.class_balanced_tok_s_1_100_intervals_after_ttft.median, passed:.realistic_final_gate.passed}' "$RD/realistic-suite-v1-result.json" 2>/dev/null)"
echo "STOP after suite a${attempt}" > "$stop_file"
echo "driver: suite exit=$rc at $(date +%H:%M:%S)"
