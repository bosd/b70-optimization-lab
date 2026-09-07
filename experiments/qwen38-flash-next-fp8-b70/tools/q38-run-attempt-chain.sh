#!/usr/bin/env bash
# Run one frozen attempt end to end on a given overlay branch, then restore q38-exact-verify.
#   q38-run-attempt-chain.sh <attempt> <port> <mtp0|mtp1|mtp2> <overlay-branch> <log-dir>
a=${1:?attempt}; port=${2:?port}; mtp=${3:?mtp}; br=${4:?branch}; L=${5:?log dir}
V=/home/steve/src/vllm-current-main; E=/home/steve/llm-optimizations/experiments/qwen38-flash-next-fp8-b70
log(){ echo "chain a$a $(date +%H:%M:%S): $*"; }
mkdir -p "$L"; printf '#!/usr/bin/env bash\nexec %s/q38-timing-driver.sh %s %s %s\n' "$E/tools" "$a" "$port" "$mtp" > "$L/a$a-driver.sh"; chmod +x "$L/a$a-driver.sh"
for i in $(seq 1 30); do ps -eo args | grep -q "[E]ngineCore\|[W]orker_TP\|[v]llm serve" || break; sleep 10; done
git -C $V checkout -q "$br" && log "overlay $br $(git -C $V rev-parse --short HEAD)"
bash $E/tools/q38-launch-frozen-attempt.sh "$a" "$L/a$a-driver.sh" "$L" > "$L/a$a-launch.out" 2>&1; log "launch rc=$? $(tail -1 "$L/a$a-launch.out" | cut -c1-90)"
if ! grep -q "^FAIL" "$L/a$a-launch.out"; then
  n=0; until [ -f /tmp/q38-$mtp-ple-only-a$a.rc ]; do sleep 30; n=$((n+1)); [ $n -gt 600 ] && { log timeout; break; }; done
  log "rc $(cat /tmp/q38-$mtp-ple-only-a$a.rc 2>/dev/null)"; grep "driver:" "$L/a$a-driver.log" 2>/dev/null | grep "rc=" | cut -c1-160
  sleep 30; for i in $(seq 1 30); do ps -eo args | grep -q "[E]ngineCore\|[W]orker_TP\|[v]llm serve" || break; sleep 10; done
fi
git -C $V checkout -q q38-exact-verify && log "overlay back at $(git -C $V rev-parse --short HEAD)"; log done
