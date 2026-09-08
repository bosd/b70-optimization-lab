#!/usr/bin/env bash
# Diagnostic driver: wait for a packet's server, then run the exact-2K greedy pair.
# Census and other diagnostic attempts want the lineage hashes (proof the head under test
# did not move the stream) without the frozen client's suite and quality legs. The harness
# call matches the frozen clients' exact-2K leg exactly, so the hashes are comparable.
#   q38-exact-depth-driver.sh <attempt> <port> <mtp0|mtp1|mtp2>
set -uo pipefail
attempt=${1:?attempt}; port=${2:?port}; mtp=${3:?mtp}
repo=/home/steve/llm-optimizations
depth_harness="${repo}/scripts/bench-openai-token-depth-suite.py"
fixture="${repo}/data/qwen27-exact-depth/qwen38-flash-next-bcd9f01-exact-depth-v1.json"
python=/home/steve/.venvs/vllm-xpu/bin/python
model=qwen38-flash-next-fp8-tp4
B=/mnt/usb-models/bench-results/qwen38-flash-next-fp8-b70
rc_file="/tmp/q38-${mtp}-ple-only-a${attempt}.rc"
[[ "$(sha256sum "$depth_harness" | cut -d' ' -f1)" == 8f162c1ab9fde7e0daffed2c4f0d6ff061ad6076c5de716e36f3d883ab4a1067 ]] || {
  printf 'FAIL: depth harness drifted\n' >&2; exit 1; }
[[ "$(sha256sum "$fixture" | cut -d' ' -f1)" == c44fccbaf600cc506d8ed0cc7357161057b86abc44469b611be71db97558061d ]] || {
  printf 'FAIL: exact-depth fixture drifted\n' >&2; exit 1; }

deadline=$(( $(date +%s) + 2700 ))
RD=""
while true; do
  RD=$(ls -d $B/*fullgraphdet-${mtp}-4352-ple-only-r1-attempt${attempt} 2>/dev/null | grep -v supervisor | head -1)
  if [[ -n "$RD" ]] && grep -q 'Application startup complete' "$RD/server.log" 2>/dev/null \
     && curl -fsS --max-time 5 "http://127.0.0.1:${port}/health" >/dev/null 2>&1; then break; fi
  if [[ -f "$rc_file" ]]; then echo "driver: server exited before healthy (rc $(cat "$rc_file"))"; exit 1; fi
  (( $(date +%s) < deadline )) || { echo "driver: server not healthy after 45 minutes"; exit 1; }
  sleep 15
done
sleep 20
echo "driver: server healthy at $(date +%H:%M:%S); run dir $RD"
for row in 1 2; do
  timeout --signal=TERM --kill-after=10s 910s "$python" "$depth_harness" --execute \
    --fixture "$fixture" --depth 2048 --context-capacity 4352 \
    --base-url "http://127.0.0.1:${port}" --model "$model" --response-adapter vllm --timeout 900 \
    --out "${RD}/exact-depth-2k-r${row}.json" \
    >"${RD}/exact-depth-2k-r${row}.log" 2>&1
  rc=$?
  printf '%s\n' "$rc" >"${RD}/exact-depth-2k-r${row}.rc"
  summary=$("$python" - "${RD}/exact-depth-2k-r${row}.json" <<'PY' 2>/dev/null || true
import json, sys
d = json.load(open(sys.argv[1]))
r = d["response"]
print(json.dumps({"o": r.get("output_token_ids_sha256", "")[:12],
                  "t": r.get("top_logprob_sha256", r.get("text_sha256", ""))[:12],
                  "r": d["metric_window"]["conventional_99_interval_tok_s"]}))
PY
)
  echo "exact-2k r${row} rc=${rc} ${summary}"
done
