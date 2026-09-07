#!/usr/bin/env bash
# Waits for the harness bisect to finish, then runs the matrix chain (c2-c5) and the 32K depth chain (c6-c7).
S=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd); W=/mnt/fast-ai/bench-results
until grep -q BISECT2-DONE /home/steve/llm-models/qwen35-9b-harness-bisect.log 2>/dev/null; do sleep 60; done
bash $S/run-20260907-qwen35-9b-matrix-chain-v2.sh > $W/qwen35-matrix-chain.log 2>&1
bash $S/run-20260907-qwen35-9b-depth32k-chain.sh > $W/qwen35-depth32k-chain.log 2>&1
echo AFTER-BISECT-CHAIN-DONE
