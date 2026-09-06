#!/usr/bin/env bash
# Offline graph-replay screen of MoE block variants on card 0 (whole fused-MoE block per layer, 48-layer replay).
SP=/tmp/claude-1000/-home-steve/28337632-6e4e-40d8-9fc8-81a2b28c7aa2/scratchpad; S=/mnt/usb-models/qwen38-build/runtime-core-moe-negidguard-b70; PY=/home/steve/.venvs/vllm-xpu/bin/python
run(){ label=$1; shift; echo "== $label"; env "$@" PYTHONPATH=$S:$SP/wt-v5-sweep ZE_AFFINITY_MASK=0 VLLM_TARGET_DEVICE=xpu Q38_BENCH_SETS=8 Q38_BENCH_EVENTS=0 Q38_BENCH_N=96 LD_LIBRARY_PATH=$S/vllm_xpu_kernels:/home/steve/.venvs/vllm-xpu/lib:/home/steve/.venvs/vllm-xpu/lib/python3.12/site-packages/torch/lib:/opt/intel/oneapi/compiler/2025.3/lib timeout 600 $PY $SP/timing-moe-wall.py 2>&1 | grep "^GRAPH\|^WALL\|Error\|error:" | cut -c1-160; }
for h in 2 3; do
  run "baseline hits=$h" Q38_BENCH_FRESH_ROUTING=$h
  run "split-K 4 hits=$h" Q38_BENCH_FRESH_ROUTING=$h VLLM_XPU_MOE_SPLIT_K=4
  run "split-K 8 hits=$h" Q38_BENCH_FRESH_ROUTING=$h VLLM_XPU_MOE_SPLIT_K=8
  run "swap_ab hits=$h" Q38_BENCH_FRESH_ROUTING=$h VLLM_XPU_MOE_SWAP_AB=1
  run "swap_ab + split-K 4 hits=$h" Q38_BENCH_FRESH_ROUTING=$h VLLM_XPU_MOE_SWAP_AB=1 VLLM_XPU_MOE_SPLIT_K=4
done
