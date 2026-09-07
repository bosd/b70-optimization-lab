#!/usr/bin/env bash
# Runs the llama.cpp Q8 lane once the W4A16 follow-up campaigns have released the cards.
set -uo pipefail
repo=/home/steve/b70-optimization-lab; W=/mnt/fast-ai/bench-results
until grep -q W4A16-FOLLOWUPS-DONE $W/qwen35-w4a16-followups.log 2>/dev/null; do sleep 60; done
while pgrep -f 'run-20260907-qwen35-campaign[.]sh' >/dev/null || docker ps --format '{{.Names}}' | grep -qE 'qwen3[58]'; do sleep 30; done; sleep 10
RUN=g1 bash $repo/experiments/qwen35-9b-b70/scripts/run-20260907-qwen35-9b-q8-llamacpp.sh > $W/qwen35-9b-q8-llamacpp-g1.log 2>&1
echo Q8-LLAMACPP-DONE
