#!/usr/bin/env bash
# Robust depth sweep for the Qwen3.5-9B FP8 quick lane with FULL_DECODE_ONLY capture (sizes 1-8): waits on the launcher
# process (the model-manifest verification runs ~30-60 s before the container exists), then the health endpoint.
set -uo pipefail
LAB=/home/steve/b70-optimization-lab; cd $LAB; PORT=18131; NAME=qwen35-9b-fp8-smoke
export COMPILATION_CONFIG='{"cudagraph_mode":"FULL_DECODE_ONLY","cudagraph_capture_sizes":[1,2,3,4,5,6,8],"max_cudagraph_capture_size":8,"splitting_ops":[],"inductor_compile_config":{"combo_kernels":false,"benchmark_combo_kernel":false,"deterministic":true,"split_reductions":false,"triton.autotune_pointwise":false,"benchmark_epilogue_fusion":false}}'
cleanup() { docker stop $NAME >/dev/null 2>&1; for _ in $(seq 1 24); do docker ps -a --format '{{.Names}}' | grep -q "^$NAME$" || break; sleep 5; done; docker rm -f $NAME >/dev/null 2>&1; }
for DEPTH in ${DEPTHS:-1 2 3 0 4 5 6}; do
  TAG=d${DEPTH}-fullgraph; cleanup
  echo "$(date -u +%FT%TZ) start $TAG"
  DEPTH=$DEPTH EAGER=0 GRAPH=1 PORT=$PORT nohup /home/steve/llm-models/qwen35-9b-smoke.sh > /home/steve/llm-models/qwen35-9b-smoke-$TAG.log 2>&1 &
  WP=$!
  ok=0; for _ in $(seq 1 240); do curl -s -m 2 http://127.0.0.1:$PORT/health >/dev/null 2>&1 && { ok=1; break; }; kill -0 $WP 2>/dev/null || break; sleep 5; done
  if [ $ok != 1 ]; then echo "$(date -u +%FT%TZ) $TAG server not healthy"; grep -iE 'error|Traceback|exception' /home/steve/llm-models/qwen35-9b-smoke-$TAG.log | tail -4 | cut -c1-200; cleanup; continue; fi
  O=data/qwen35-9b-fp8-smoke-20260907/$TAG; mkdir -p $O
  python3 scripts/bench-openai-realistic-suite.py --base-url http://127.0.0.1:$PORT --model qwen35-9b-fp8 --api-mode chat --max-tokens 512 --metric-tokens 100 --return-token-ids --out $O/realistic-suite.json >/dev/null 2>&1
  python3 - $O/realistic-suite.json $TAG <<'PY'
import json,sys
d=json.load(open(sys.argv[1])); s=d['summary']; k='tok_s_1_100_after_ttft'
print(sys.argv[2], 'median', round(s[k]['median'],2), 'p10', round(s[k]['p10'],2), 'ttft_ms', round(s['ttft_ms']['median'],1), 'valid', d['fresh_response_validity'].get('valid'), 'gate', d['realistic_final_gate'].get('passed'))
PY
  cleanup; wait $WP 2>/dev/null
done
echo SWEEP-ROBUST-DONE
