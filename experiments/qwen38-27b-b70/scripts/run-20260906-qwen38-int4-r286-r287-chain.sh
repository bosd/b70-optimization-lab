#!/usr/bin/env bash
S=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
while docker ps --format '{{.Names}}' | grep -q qwen38; do sleep 30; done
DEPTH=2 RUN=r286 bash "$S/run-20260906-qwen38-int4-r286-r287-depth2-depth1-big-admission-ladders.sh"
while docker ps --format '{{.Names}}' | grep -q qwen38; do sleep 30; done; sleep 20
DEPTH=1 RUN=r287 bash "$S/run-20260906-qwen38-int4-r286-r287-depth2-depth1-big-admission-ladders.sh"
echo CHAIN-DONE
