#!/usr/bin/env bash
# R288 (2026-09-06): depth 1 on the large-admission server shape at 2/4/8/16 users (two passes) to place the crossover from
# depth 4 (best at 1-4 users) to depth 1 (best at 16-32 users, R287).
S=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
while docker ps --format '{{.Names}}' | grep -q qwen38; do sleep 30; done; sleep 20
while docker ps --format '{{.Names}}' | grep -q qwen38; do sleep 30; done
DEPTH=1 RUN=r288 LADDER_CONCURRENCY=2,4,8,16 bash "$S/run-20260906-qwen38-int4-r286-r287-depth2-depth1-big-admission-ladders.sh"
echo R288-DONE
