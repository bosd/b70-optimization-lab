#!/usr/bin/env bash
# New-authority quality screen for a frozen attempt: wait for the packet's server, then run the same
# quality suite as the frozen client (exact cases, repeat, long context), exact-depth 2K r1/r2 and
# 4K r1/r2 (hashes recorded, not asserted), and the cold realistic suite; everything lands in the
# run dir; then stop the server.
#   q38-quality-screen-driver.sh <attempt> <port> <mtp0|mtp1|mtp2>
set -uo pipefail
attempt=${1:?attempt}; port=${2:?port}; mtp=${3:?mtp0|mtp1|mtp2}
repo=/home/steve/llm-optimizations; python=/home/steve/.venvs/vllm-xpu/bin/python; B=/mnt/usb-models/bench-results/qwen38-flash-next-fp8-b70
model=qwen38-flash-next-fp8-tp4; tokenizer=/mnt/usb-models/llm-models/Qwen3.8-Flash-Next-FP8; base_url=http://127.0.0.1:${port}
fixture=$repo/data/qwen27-exact-depth/qwen38-flash-next-bcd9f01-exact-depth-v1.json
rc_file="/tmp/q38-${mtp}-ple-only-a${attempt}.rc"; stop_file="/tmp/q38-${mtp}-ple-only-a${attempt}.stop"
deadline=$(( $(date +%s) + 2700 ))
until curl -fsS --max-time 5 "$base_url/health" >/dev/null 2>&1; do
  [[ -f "$rc_file" ]] && { echo "driver: server exited before healthy (rc $(cat "$rc_file"))"; exit 1; }
  (( $(date +%s) < deadline )) || { echo "driver: server not healthy after 45 minutes"; exit 1; }
  sleep 15
done
RD=$(ls -d $B/*fullgraphdet-${mtp}-4352-ple-only-r1-attempt${attempt} 2>/dev/null | grep -v supervisor | head -1)
[[ -n "$RD" && -d "$RD" ]] || { echo "driver: no run dir"; exit 1; }
sleep 30; echo "driver: server healthy at $(date +%H:%M:%S); screen into $RD"
timeout --signal=TERM --kill-after=10s 1200s "$python" "$repo/scripts/qwen38-text-quality-suite.py" \
  --base-url "$base_url" --model "$model" --tokenizer "$tokenizer" --timeout 900 \
  --seed 20260609 --repeat-runs 16 --request-id-prefix q38-screen-a${attempt} \
  --long-context-tokens 2157 --chat-template-kwargs-json '{"enable_thinking":false}' \
  --output-json "$RD/quality-current.json" >"$RD/quality-current.log" 2>&1; rc=$?
echo "driver: quality rc=$rc $(jq -c '{exact_pass: ([.exact_cases[] | select(.pass==true)] | length), exact_n: (.exact_cases|length), repeat_distinct: ([.repeat_case[]?.sha256] | unique | length), repeat_n: (.repeat_case|length), long: (.long_context_case.pass // .long_context_case.passed)}' "$RD/quality-current.json" 2>/dev/null)"
for depth in 2048 4096; do tag=$([ $depth = 2048 ] && echo 2k || echo 4k); for row in 1 2; do
  timeout --signal=TERM --kill-after=10s 1500s "$python" "$repo/scripts/bench-openai-token-depth-suite.py" --execute \
    --fixture "$fixture" --depth $depth --context-capacity 4352 --base-url "$base_url" --model "$model" --response-adapter vllm --timeout 1400 \
    --out "$RD/exact-depth-${tag}-r${row}.json" >"$RD/exact-depth-${tag}-r${row}.log" 2>&1; rc=$?
  echo "driver: exact-${tag} r${row} rc=$rc $(jq -c '{o:.response.output_token_ids_sha256[0:12], r:.metric_window.conventional_99_interval_tok_s}' "$RD/exact-depth-${tag}-r${row}.json" 2>/dev/null)"
  sleep 10
done; done
timeout --signal=TERM --kill-after=10s 1800s "$python" "$repo/scripts/bench-openai-realistic-suite.py" --base-url "$base_url" --model "$model" --api-mode chat \
  --suite "$repo/repro/rapid-model-snapshots-b70/realistic-suite-v1.json" --max-tokens 512 --metric-tokens 100 --seed 20260609 --timeout 900 --return-token-ids \
  --request-extra-json '{"chat_template_kwargs":{"enable_thinking":false},"seed":20260609,"temperature":0,"top_p":1.0}' \
  --out "$RD/realistic-suite-v1-result.json" > "$RD/realistic-suite-v1-result.log" 2>&1; rc=$?
echo "driver: suite rc=$rc $(jq -c '{med:.summary.class_balanced_tok_s_1_100_intervals_after_ttft.median, passed:.realistic_final_gate.passed}' "$RD/realistic-suite-v1-result.json" 2>/dev/null)"
echo "STOP after screen a${attempt}" > "$stop_file"; echo "driver: screen done at $(date +%H:%M:%S)"
