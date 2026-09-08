#!/usr/bin/env bash
# Census driver: run the packet's exact-2K pair for the lineage hash, then snapshot the
# routing census around a decode-heavy generation so the decode window can be isolated by
# differencing the snapshots.
#
# Why a short prompt and a long generation: a snapshot window covers every routed block in
# it, and a 2048-token prefill routes as many blocks as 2048 decode steps. The placement
# only needs to avoid experts the decode window selects (the original survey filtered to
# decode-sized routing the same way), so the census request keeps the fixture's own content
# but takes a short slice of it and generates far past it.
#   q38-census-window-driver.sh <attempt> <port> <mtp0|mtp1|mtp2>
set -uo pipefail
attempt=${1:?attempt}; port=${2:?port}; mtp=${3:?mtp}
repo=/home/steve/llm-optimizations
depth_harness="${repo}/scripts/bench-openai-token-depth-suite.py"
fixture="${repo}/data/qwen27-exact-depth/qwen38-flash-next-bcd9f01-exact-depth-v1.json"
python=/home/steve/.venvs/vllm-xpu/bin/python
model=qwen38-flash-next-fp8-tp4
B=/mnt/usb-models/bench-results/qwen38-flash-next-fp8-b70
rc_file="/tmp/q38-${mtp}-ple-only-a${attempt}.rc"
PROMPT_TOKENS=${Q38_CENSUS_PROMPT_TOKENS:-128}
GEN_TOKENS=${Q38_CENSUS_GEN_TOKENS:-4096}
[[ "$(sha256sum "$depth_harness" | cut -d' ' -f1)" == 8f162c1ab9fde7e0daffed2c4f0d6ff061ad6076c5de716e36f3d883ab4a1067 ]] || {
  printf 'FAIL: depth harness drifted\n' >&2; exit 1; }
[[ "$(sha256sum "$fixture" | cut -d' ' -f1)" == c44fccbaf600cc506d8ed0cc7357161057b86abc44469b611be71db97558061d ]] || {
  printf 'FAIL: exact-depth fixture drifted\n' >&2; exit 1; }

snapshot() {
  # Signal the workers by pid, never with a pkill pattern: a pattern that appears in this
  # script's own command line would match the caller.
  local pids
  pids=$(pgrep -f 'VLLM::Worker' | grep -v "^$$\$" || true)
  [[ -n "$pids" ]] || { echo "snapshot: no workers found"; return 1; }
  local n=0
  for p in $pids; do kill -USR1 "$p" 2>/dev/null && n=$((n+1)); done
  echo "snapshot: signalled $n workers ($1)"
  sleep 5
}

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
d = json.load(open(sys.argv[1])); r = d["response"]
print(json.dumps({"o": r.get("output_token_ids_sha256", "")[:12],
                  "t": r.get("text_sha256", "")[:12],
                  "r": d["metric_window"]["conventional_99_interval_tok_s"]}))
PY
)
  echo "exact-2k r${row} rc=${rc} ${summary}"
done

snapshot "before the census window"
"$python" - "$fixture" "$port" "$model" "$PROMPT_TOKENS" "$GEN_TOKENS" "${RD}/census-window.json" <<'PY'
import json, sys, time, urllib.request
fixture, port, model, ptok, gtok, out = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
case = next(c for c in json.load(open(fixture))["cases"] if c["depth"] == 2048)
payload = {"model": model, "prompt": case["prompt_token_ids"][:ptok], "max_tokens": gtok,
           "temperature": 0, "top_p": 1, "seed": 1, "ignore_eos": True, "stream": False}
req = urllib.request.Request(f"http://127.0.0.1:{port}/v1/completions",
                             data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
t0 = time.perf_counter()
body = json.loads(urllib.request.urlopen(req, timeout=1800).read())
dt = time.perf_counter() - t0
usage = body.get("usage", {})
json.dump({"prompt_tokens": usage.get("prompt_tokens"), "completion_tokens": usage.get("completion_tokens"),
           "seconds": dt, "decode_share_of_routed_blocks":
               usage.get("completion_tokens", 0) / max(usage.get("completion_tokens", 0) + usage.get("prompt_tokens", 0), 1)},
          open(out, "w"), indent=1)
print(f"census window: {usage.get('prompt_tokens')} prompt + {usage.get('completion_tokens')} generated "
      f"in {dt:.1f}s ({usage.get('completion_tokens', 0)/max(dt, 1e-9):.2f} tok/s, decode is "
      f"{100.0*usage.get('completion_tokens', 0)/max(usage.get('completion_tokens', 0)+usage.get('prompt_tokens', 0), 1):.1f}% of routed blocks)")
PY
snapshot "after the census window"
echo "driver: done at $(date +%H:%M:%S)"
