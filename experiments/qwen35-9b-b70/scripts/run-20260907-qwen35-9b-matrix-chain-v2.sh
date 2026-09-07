#!/usr/bin/env bash
# Matrix chain (revised after the draft-head finding): every campaign uses the draft-only INT4 lm_head (DRAFT_HEAD=1).
# c2 TP1 depth 3 strict+ladders (headline candidate); c3 TP1 depth 4 strict; c4 TP1 graph-off depth 3 strict;
# c5 TP2 depth 3 strict+ladders; c6 TP2 depth 4 strict.
S=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd); H=$S/run-20260907-qwen35-9b-campaign-v2.sh; W=/mnt/fast-ai/bench-results
wait_idle() { while pgrep -f 'run-20260907-qwen35-9b-campaign' >/dev/null || docker ps --format '{{.Names}}' | grep -qE 'qwen3[58]' || docker ps -a --format '{{.Names}}' | grep -q '^qwen35-9b-'; do sleep 30; done; sleep 10; }
wait_idle; RUN=c2 TP=1 DEPTH=3 GRAPH=1 DRAFT_HEAD=1 STAGES="strict ladders" bash $H > $W/qwen35-c2-wrapper.log 2>&1
wait_idle; RUN=c3 TP=1 DEPTH=4 GRAPH=1 DRAFT_HEAD=1 STAGES="strict" bash $H > $W/qwen35-c3-wrapper.log 2>&1
wait_idle; RUN=c4 TP=1 DEPTH=3 GRAPH=0 DRAFT_HEAD=1 STAGES="strict" bash $H > $W/qwen35-c4-wrapper.log 2>&1
wait_idle; RUN=c5 TP=2 DEPTH=3 GRAPH=1 DRAFT_HEAD=1 STAGES="strict ladders" bash $H > $W/qwen35-c5-wrapper.log 2>&1
wait_idle; RUN=c6 TP=2 DEPTH=4 GRAPH=1 DRAFT_HEAD=1 STAGES="strict" bash $H > $W/qwen35-c6-wrapper.log 2>&1
echo MATRIX-CHAIN-DONE
