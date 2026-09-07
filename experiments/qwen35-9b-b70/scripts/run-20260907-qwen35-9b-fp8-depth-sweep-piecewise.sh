#!/usr/bin/env bash
# Depth sweep for the Qwen3.5-9B FP8 quick lane: graph-captured server per depth, 12-prompt realistic suite, outputs kept for identity checks.
set -uo pipefail
LAB=/home/steve/b70-optimization-lab; cd $LAB; PORT=18131
for cfg in "1 0 1" "0 0 1" "2 0 1" "3 0 1"; do
  set -- $cfg; DEPTH=$1; EAGER=$2; GRAPH=$3; TAG=d${DEPTH}-graph${GRAPH}
  while docker ps --format '{{.Names}}' | grep -q qwen35-9b-fp8-smoke; do docker stop qwen35-9b-fp8-smoke >/dev/null 2>&1; sleep 5; done
  echo "$(date -u +%FT%TZ) start $TAG"
  (DEPTH=$DEPTH EAGER=$EAGER GRAPH=$GRAPH PORT=$PORT nohup /home/steve/llm-models/qwen35-9b-smoke.sh > /home/steve/llm-models/qwen35-9b-smoke-$TAG.log 2>&1 &)
  for _ in $(seq 1 180); do curl -s -m 2 http://127.0.0.1:$PORT/health >/dev/null 2>&1 && break; docker ps --format '{{.Names}}' | grep -q qwen35-9b-fp8-smoke || sleep 5; sleep 5; done
  if ! curl -s -m 2 http://127.0.0.1:$PORT/health >/dev/null 2>&1; then echo "$(date -u +%FT%TZ) $TAG server not healthy"; grep -iE 'error|Traceback' /home/steve/llm-models/qwen35-9b-smoke-$TAG.log | tail -3 | cut -c1-200; continue; fi
  O=data/qwen35-9b-fp8-smoke-20260907/$TAG; mkdir -p $O
  python3 scripts/bench-openai-realistic-suite.py --base-url http://127.0.0.1:$PORT --model qwen35-9b-fp8 --api-mode chat --max-tokens 512 --metric-tokens 100 --return-token-ids --out $O/realistic-suite.json >/dev/null 2>&1
  python3 - $O/realistic-suite.json $TAG <<'PY'
import json,sys
d=json.load(open(sys.argv[1])); s=d['summary']; k='tok_s_1_100_after_ttft'
print(sys.argv[2], 'median', round(s[k]['median'],2), 'p10', round(s[k]['p10'],2), 'ttft_ms', round(s['ttft_ms']['median'],1), 'valid', d['fresh_response_validity'].get('valid'), 'gate', d['realistic_final_gate'].get('passed'))
PY
  docker stop qwen35-9b-fp8-smoke >/dev/null 2>&1; sleep 5
done
echo SWEEP-DONE
