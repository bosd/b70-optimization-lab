#!/usr/bin/env bash
# Readiness wrapper for a packet's frozen client: the launcher starts the driver seconds after the host
# wrapper, before the run dir exists; the client must not start until the server is up (a client that
# fails early writes the failure file, and the supervisor aborts the launch). Waits for the run dir,
# 'Application startup complete' and /health, then execs the frozen client.
#   q38-client-driver.sh <attempt> <port> <mtp0|mtp1|mtp2> <client-script>
set -uo pipefail
attempt=${1:?attempt}; port=${2:?port}; mtp=${3:?mtp}; client=${4:?client script}
B=/mnt/usb-models/bench-results/qwen38-flash-next-fp8-b70; rc_file="/tmp/q38-${mtp}-ple-only-a${attempt}.rc"
deadline=$(( $(date +%s) + 2700 ))
while true; do
  RD=$(ls -d $B/*fullgraphdet-${mtp}-4352-ple-only-r1-attempt${attempt} 2>/dev/null | grep -v supervisor | head -1)
  [[ -n "$RD" ]] && grep -q 'Application startup complete' "$RD/server.log" 2>/dev/null && curl -fsS --max-time 5 "http://127.0.0.1:${port}/health" >/dev/null 2>&1 && break
  [[ -f "$rc_file" ]] && { echo "driver: server exited before healthy (rc $(cat "$rc_file"))"; exit 1; }
  (( $(date +%s) < deadline )) || { echo "driver: server not healthy after 45 minutes"; exit 1; }
  sleep 15
done
sleep 20; echo "driver: server healthy at $(date +%H:%M:%S); exec frozen client $client"
exec "$client"
