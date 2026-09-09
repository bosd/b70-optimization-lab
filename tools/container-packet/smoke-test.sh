#!/usr/bin/env bash
# Start the packet, wait for health, and run a short gate before reporting success.
#
# The gate is deliberately small but not decorative: it sends the same greedy request twice and
# requires byte-identical answers. That is the property this lane is packaged for, so a packet that
# starts but does not repeat itself is a failed packet, not a passing one. It is a smoke test, not
# the strict suite: see the recipe README for the measured gates.
#
#   PROFILE     one-gpu (default) or two-gpu
#   MODEL_DIR   verified model directory (required)
#   KEEP_UP     1 to leave the server running afterwards (default 0)
set -uo pipefail
here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd); repo=$(cd -- "${here}/../.." && pwd)
pkg=${PACKAGE_DIR:+${repo}/${PACKAGE_DIR}}; pkg=${pkg:?set PACKAGE_DIR to the packet directory}
served=${SERVED_NAME:?set SERVED_NAME to the served model name}
profile=${PROFILE:-one-gpu}
port=${PORT:-18131}
export MODEL_DIR=${MODEL_DIR:?set MODEL_DIR to the verified model directory}
export VLLM_CACHE_DIR=${VLLM_CACHE_DIR:-${pkg}/cache-${profile}}
export PORT
compose=(docker compose -f "${pkg}/compose.yaml")
out=${OUT_DIR:-${pkg}/smoke-${profile}-$(date -u +%Y%m%dT%H%M%SZ)}
mkdir -p "${out}" "${VLLM_CACHE_DIR}"

cleanup() { [[ "${KEEP_UP:-0}" == 1 ]] || "${compose[@]}" down --remove-orphans >/dev/null 2>&1 || true; }
trap cleanup EXIT

echo "starting ${profile} (logs: ${out}/server.log)"
"${compose[@]}" up -d "${profile}" >"${out}/compose-up.log" 2>&1 || { echo "compose up failed:"; cat "${out}/compose-up.log"; exit 1; }

deadline=$(( $(date +%s) + ${HEALTH_TIMEOUT:-1800} ))
until curl -fsS "http://127.0.0.1:${port}/health" >/dev/null 2>&1; do
  if (( $(date +%s) > deadline )); then
    echo "server did not become healthy in time"; "${compose[@]}" logs --no-color >"${out}/server.log" 2>&1; exit 1
  fi
  "${compose[@]}" ps --format '{{.State}}' 2>/dev/null | grep -q running || {
    echo "container exited before becoming healthy"; "${compose[@]}" logs --no-color >"${out}/server.log" 2>&1; tail -20 "${out}/server.log"; exit 1; }
  sleep 10
done
echo "healthy"

ask() {
  curl -fsS "http://127.0.0.1:${port}/v1/completions" -H 'Content-Type: application/json' -d '{
    "model":"'"${served}"'",
    "prompt":"Write one sentence explaining what a tensor is to a new programmer.",
    "max_tokens":64,"temperature":0,"seed":42,"stream":false}'
}
a=$(ask); rc_a=$?
b=$(ask); rc_b=$?
printf '%s\n' "$a" >"${out}/answer-1.json"; printf '%s\n' "$b" >"${out}/answer-2.json"
"${compose[@]}" logs --no-color >"${out}/server.log" 2>&1 || true

if (( rc_a != 0 || rc_b != 0 )); then echo "FAIL: completion request errored"; exit 1; fi
if ! python3 - "${out}" "${profile}" "${PACKAGE_DIR}" <<'PY'
import json,platform,sys,datetime
from pathlib import Path
out,profile=sys.argv[1],sys.argv[2]
try:
    ans=json.load(open(f"{out}/answer-1.json"))
    other=json.load(open(f"{out}/answer-2.json"))
    first,second=ans["choices"][0]["text"],other["choices"][0]["text"]
    if not isinstance(first,str) or not isinstance(second,str):
        raise ValueError("completion text must be a string")
    if not first.strip():
        raise ValueError("empty completion")
    if first != second:
        raise ValueError("two identical greedy requests returned different text")
except (OSError,ValueError,KeyError,IndexError,TypeError) as exc:
    print(f"FAIL: invalid completion pair: {exc}",file=sys.stderr)
    sys.exit(1)
Path(out,"result.json").write_text(json.dumps({
 "packet":sys.argv[3],"profile":profile,
 "checked_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "host":platform.node(),"kernel":platform.release(),
 "repeat_exact":True,"completion_tokens":ans.get("usage",{}).get("completion_tokens"),
 "sample_text":ans["choices"][0]["text"][:400],
},indent=1)+"\n")
print(f"  answer: {first}")
PY
then
  exit 1
fi

echo
echo "PASS  two identical greedy requests returned byte-identical text"
echo "  packet result: ${out}/result.json"
echo "  OpenAI-compatible endpoint: http://127.0.0.1:${port}/v1  (model: '"${served}"')"
echo "  example: curl http://127.0.0.1:${port}/v1/completions -H 'Content-Type: application/json' \\"
echo "             -d '{\"model\":\"${served}\",\"prompt\":\"Hello\",\"max_tokens\":32,\"temperature\":0}'"
[[ "${KEEP_UP:-0}" == 1 ]] && echo "  server left running; stop it with: docker compose -f ${pkg}/compose.yaml down"
exit 0
