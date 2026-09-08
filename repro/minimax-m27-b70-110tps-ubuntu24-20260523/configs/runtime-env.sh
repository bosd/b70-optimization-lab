#!/usr/bin/env bash

export FAST_AI_ROOT="${FAST_AI_ROOT:-/mnt/fast-ai}"
export MODEL="${MODEL:-$FAST_AI_ROOT/llm-models/minimax-m2.7-int4-autoround}"
export HF_HOME="${HF_HOME:-$FAST_AI_ROOT/llm-cache/hf}"
export VLLM_CACHE_ROOT="${VLLM_CACHE_ROOT:-$FAST_AI_ROOT/vllm-cache-exp/minimax-b70-20260523}"
export BENCH_ROOT="${BENCH_ROOT:-$FAST_AI_ROOT/bench-results/minimax-m27-b70-110tps-20260523}"
export VENV="${VENV:-$HOME/.venvs/vllm-xpu}"
# The source trees moved off $FAST_AI_ROOT; prefer the current location and fall back to
# the historical one so the 2026-05 record's own paths still resolve where they exist.
if [ -z "${SRC_ROOT:-}" ] && [ -d "$HOME/src/llm-scaler" ]; then SRC_ROOT="$HOME/src"; fi
export SRC_ROOT="${SRC_ROOT:-$FAST_AI_ROOT/src}"
# The record does not run stock vLLM: 03-build-stack.sh checks out c51df4300 and applies
# the 41-file vllm-active-promoted-minimax patch carried by the 89 tok/s guide. That patch
# is what supplies the INT4 MoE path -- moe_wna16 reading VLLM_XPU_USE_LLM_SCALER_MOE, plus
# the tuned int4_w4a16 MoE config for this device. $SRC_ROOT/vllm has since moved on to
# unrelated work and no longer carries any of it, so INC on XPU returns no MoE method there,
# the MoE loads unquantized, and the model cannot fit. Prefer a dedicated worktree holding
# the pinned commit with the patch applied; fall back to the historical path if it is absent.
if [ -z "${VLLM_SRC:-}" ] && [ -d "$HOME/src/vllm-minimax-record" ]; then
  VLLM_SRC="$HOME/src/vllm-minimax-record"
fi
export VLLM_SRC="${VLLM_SRC:-$SRC_ROOT/vllm}"
export LLM_SCALER_ROOT="${LLM_SCALER_ROOT:-$SRC_ROOT/llm-scaler}"
export LLM_SCALER_KERNELS="${LLM_SCALER_KERNELS:-$LLM_SCALER_ROOT/vllm/custom-esimd-kernels-vllm/python}"

# Device visibility. The 2026-05 record set ONEAPI_DEVICE_SELECTOR=level_zero:0,1,2,3 and
# ZE_AFFINITY_MASK=0,1,2,3 together. Setting both filters the device list twice -- the mask
# restricts what Level Zero reports, then the selector indexes into the already-restricted
# list -- and the working four-card lanes on this host set the mask alone and unset the
# selector explicitly. Do the same, and let an explicit value from the caller win.
export ZE_AFFINITY_MASK="${ZE_AFFINITY_MASK:-0,1,2,3}"
if [ -z "${MINIMAX_KEEP_DEVICE_SELECTOR:-}" ]; then
  unset ONEAPI_DEVICE_SELECTOR SYCL_DEVICE_FILTER SYCL_DEVICE_ALLOWLIST
fi
export SYCL_CACHE_PERSISTENT="${SYCL_CACHE_PERSISTENT:-1}"

# oneCCL. CCL_ATL_TRANSPORT=ofi is the record's value, but the record did not pin a
# libfabric provider, so libfabric auto-selects one. On this host that resolves to UCX, and
# all four workers then take SIGSEGV inside libsycl during communicator setup, with
# libucs.so.0 at the top of every backtrace, immediately after oneCCL's topology-recognition
# warning. Pinning the tcp provider is what the four-card lanes that do work on this machine
# use. CCL_ZE_IPC_EXCHANGE=pidfd likewise matches those lanes; the default exchange path
# depends on kernel features this host's driver no longer offers the same way.
export CCL_ATL_TRANSPORT="${CCL_ATL_TRANSPORT:-ofi}"
export FI_PROVIDER="${FI_PROVIDER:-tcp}"
export FI_TCP_IFACE="${FI_TCP_IFACE:-lo}"
export CCL_ZE_IPC_EXCHANGE="${CCL_ZE_IPC_EXCHANGE:-pidfd}"
export CCL_TOPO_P2P_ACCESS="${CCL_TOPO_P2P_ACCESS:-1}"
export CCL_ENABLE_SYCL_KERNELS="${CCL_ENABLE_SYCL_KERNELS:-0}"
# THE fix for the four-worker SIGSEGV at engine init. oneCCL's SYCL-kernel collectives take
# a low-latency path for tiny messages, and on this host a 1-element (4-byte) float32
# allreduce faults at address (nil) inside arc_ll256_allreduce, reached through
# arc_allreduce from allreduce_sycl_single_node. vLLM's distributed-init sanity collective
# is exactly that shape, so every worker died before the model was even loaded. A minimal
# four-rank harness reproduces it without vLLM: 4 B crashes, 256 B and larger are fine, and
# CCL_ENABLE_SYCL_KERNELS=0 passes all 25 size/dtype cases. Narrower knobs do not help --
# CCL_SYCL_ALLREDUCE_ARC=0, the LL and SMALL thresholds, TMP_BUF and the mpi transport were
# each tried and each still crashed on the first 4-byte allreduce.
export CCL_SEND="${CCL_SEND:-direct}"
export CCL_RECV="${CCL_RECV:-direct}"
# Route every collective through oneCCL's "simple" implementation. Without these, the first
# allreduce of distributed init takes the specialised low-latency path and all four workers
# take SIGSEGV at address (nil) inside arc_ll256_allreduce, called from
# allreduce_sycl_single_node -- that symbol is the top named frame of every worker's
# backtrace. The LL256 kernel wants peer-mapped buffers, and this host's topology
# recognition reports plain PCIe between the cards rather than a P2P fabric. The four-card
# lanes that do work on this machine set all three thresholds to 4 GiB, so nothing reaches
# the specialised path at any message size.
export CCL_SYCL_ALLREDUCE_SIMPLE_THRESHOLD="${CCL_SYCL_ALLREDUCE_SIMPLE_THRESHOLD:-4294967296}"
export CCL_SYCL_ALLGATHERV_SIMPLE_THRESHOLD="${CCL_SYCL_ALLGATHERV_SIMPLE_THRESHOLD:-4294967296}"
export CCL_SYCL_REDUCE_SCATTER_SIMPLE_THRESHOLD="${CCL_SYCL_REDUCE_SCATTER_SIMPLE_THRESHOLD:-4294967296}"

export VLLM_USE_V1="${VLLM_USE_V1:-1}"
# Spawn, do not fork, the tensor-parallel workers. vLLM's default for this tree is fork
# (vllm/envs.py), and the API server process has already initialised the SYCL runtime by the
# time it creates workers, so a forked child inherits a context it does not own and faults
# on its first real kernel submission -- which is the first allreduce of distributed init.
export VLLM_WORKER_MULTIPROC_METHOD="${VLLM_WORKER_MULTIPROC_METHOD:-spawn}"
export VLLM_XPU_FORCE_GRAPH_WITH_COMM="${VLLM_XPU_FORCE_GRAPH_WITH_COMM:-1}"
export VLLM_XPU_GRAPH_NOOP_COMM_CAPTURE="${VLLM_XPU_GRAPH_NOOP_COMM_CAPTURE:-1}"
export VLLM_XPU_USE_LLM_SCALER_MOE="${VLLM_XPU_USE_LLM_SCALER_MOE:-1}"
export VLLM_XPU_USE_LLM_SCALER_MOE_WS="${VLLM_XPU_USE_LLM_SCALER_MOE_WS:-1}"
export VLLM_XPU_USE_LLM_SCALER_MOE_MINIMAX_LOGITS_WS="${VLLM_XPU_USE_LLM_SCALER_MOE_MINIMAX_LOGITS_WS:-1}"
export VLLM_MINIMAX_MOE_FULL_FORWARD_CUSTOM_OP="${VLLM_MINIMAX_MOE_FULL_FORWARD_CUSTOM_OP:-1}"
export VLLM_MINIMAX_MOE_OUTPUT_ALLREDUCE_INSIDE_CUSTOM_OP="${VLLM_MINIMAX_MOE_OUTPUT_ALLREDUCE_INSIDE_CUSTOM_OP:-1}"
export VLLM_MINIMAX_POST_ATTN_NORM_MOE_CUSTOM_OP="${VLLM_MINIMAX_POST_ATTN_NORM_MOE_CUSTOM_OP:-1}"
export VLLM_MINIMAX_QK_NORM_RESTORE_WEIGHT="${VLLM_MINIMAX_QK_NORM_RESTORE_WEIGHT:-1}"
export VLLM_MINIMAX_QK_RMS_APPLY_TP_SCALE="${VLLM_MINIMAX_QK_RMS_APPLY_TP_SCALE:-1}"
export VLLM_MINIMAX_QK_RMS_DIRECT_INPLACE_SCALE="${VLLM_MINIMAX_QK_RMS_DIRECT_INPLACE_SCALE:-1}"
export VLLM_MINIMAX_QK_RMS_XPU_HELPER="${VLLM_MINIMAX_QK_RMS_XPU_HELPER:-1}"

export PYTHONPATH="$LLM_SCALER_KERNELS:$VLLM_SRC:${PYTHONPATH:-}"
# $VENV/lib must come before the oneAPI compiler libs: it carries the runtime this venv
# was built against, and with only torch/lib ahead of oneAPI 2025.3 the loader resolves
# a mismatched library and torch.xpu.device_count() returns 0 on a machine with four
# working cards. The Qwen lanes on this host order it the same way.
# The XPU platform plugin dlopens the kernel libraries; without their directory here vLLM
# silently resolves UnspecifiedPlatform ("libgdn_attn_kernels_xe_2.so: cannot open shared
# object file") even though torch sees all four cards, and every launch then fails a
# platform assertion. The package is importable through its editable install, which does
# not put its .so files on the loader path. The Qwen lanes list their stage the same way.
# This file is sourced before the venv is activated, so ask the venv's interpreter directly
# rather than whichever python3 is on PATH.
XPU_KERNELS_DIR="${XPU_KERNELS_DIR:-$("$VENV/bin/python" -c 'import importlib.util,os; s=importlib.util.find_spec("vllm_xpu_kernels"); print(os.path.dirname(s.origin) if s and s.origin else "")' 2>/dev/null || true)}"
export LD_LIBRARY_PATH="${XPU_KERNELS_DIR:+$XPU_KERNELS_DIR:}$VENV/lib:$VENV/lib/python3.12/site-packages/torch/lib:/opt/intel/oneapi/compiler/2025.3/lib:${LD_LIBRARY_PATH:-}"
