#!/usr/bin/env bash
# After the 32K chain: deeper strict pairs with the draft INT4 head on one card (c9 depth 5, c10 depth 6).
S=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd); H=$S/run-20260907-qwen35-9b-campaign-v2.sh; W=/mnt/fast-ai/bench-results
until grep -q DEPTH32K-CHAIN-DONE $W/qwen35-depth32k-chain.log 2>/dev/null; do sleep 60; done
wait_idle() { while pgrep -f 'run-20260907-qwen35-9b-campaign' >/dev/null || docker ps --format '{{.Names}}' | grep -qE 'qwen3[58]' || docker ps -a --format '{{.Names}}' | grep -q '^qwen35-9b-'; do sleep 30; done; sleep 10; }
wait_idle; RUN=c9 TP=1 DEPTH=5 GRAPH=1 DRAFT_HEAD=1 STAGES="strict" bash $H > $W/qwen35-c9-wrapper.log 2>&1
wait_idle; RUN=c10 TP=1 DEPTH=6 GRAPH=1 DRAFT_HEAD=1 STAGES="strict" bash $H > $W/qwen35-c10-wrapper.log 2>&1
echo DEEP-CHAIN-DONE
