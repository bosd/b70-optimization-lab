#!/usr/bin/env bash
# After the matrix chain: 32K real-content depth ladders (MTP0 oracle arm, then depth-3 arm with the draft INT4 head) on one card (c7) and two cards (c8).
S=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd); H=$S/run-20260907-qwen35-9b-campaign-v2.sh; W=/mnt/fast-ai/bench-results
until grep -q MATRIX-CHAIN-DONE $W/qwen35-matrix-chain.log 2>/dev/null; do sleep 60; done
wait_idle() { while pgrep -f 'run-20260907-qwen35-9b-campaign' >/dev/null || docker ps --format '{{.Names}}' | grep -qE 'qwen3[58]' || docker ps -a --format '{{.Names}}' | grep -q '^qwen35-9b-'; do sleep 30; done; sleep 10; }
wait_idle; RUN=c7 TP=1 DEPTH=3 GRAPH=1 DRAFT_HEAD=1 STAGES="depth32k" bash $H > $W/qwen35-c7-wrapper.log 2>&1
wait_idle; RUN=c8 TP=2 DEPTH=3 GRAPH=1 DRAFT_HEAD=1 STAGES="depth32k" bash $H > $W/qwen35-c8-wrapper.log 2>&1
echo DEPTH32K-CHAIN-DONE
