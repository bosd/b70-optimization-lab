# Codex GDN Spec Parity Fix

Date: 2026-06-20

## Root Cause

The XPU GDN verifier path did not leave speculative recurrent state columns
equal to a one-token-at-a-time target-model decode. The packed recurrent update
was called with `num_accepted_tokens`, so the kernel used accepted-count state
semantics: initialize from the selected accepted boundary and store only the
accepted prefix columns. For a verifier sequence `[target, draft_1, ..., bonus]`,
later columns could remain stale or approximate even though the sampler may
later commit them.

The lower-level `_xpu_C.gdn_attention` kernel only accepts one state index per
sequence and writes a final state for that sequence. It has no interface for the
full `spec_state_indices_tensor` column table, so the exact spec-column contract
has to be handled by the Python caller unless the C++/SYCL interface is expanded.

## Fix

In `vllm/model_executor/layers/mamba/gdn_linear_attn.py`, XPU spec decode now
runs the recurrent verifier update one speculative position at a time:

- position 0 updates `spec_state_indices_tensor[:, 0]` from the running state;
- each later position first copies the previous exact prefix state into that
  column, then runs the ordinary one-token recurrent update in place;
- verifier outputs are written back into the same packed output order.

This removes accepted-count recurrent-state semantics from the spec verifier
path. The no-spec native decode path is unchanged.

In `vllm/_xpu_ops.py`, spec rows always fall back from
`torch.ops.vllm.gdn_attention_core_xpu` into `_forward_core`, so the old native
spec escape hatch with approximate slot-copy experiments is no longer used.

## Synthetic Test

Command run:

```bash
cd /home/steve/src/vllm
PYTHONPATH=/home/steve/src/vllm:/home/steve/src/vllm-xpu-kernels \
/home/steve/.venvs/vllm-xpu/bin/python \
/home/steve/llm-optimizations/scripts/check-gdn-spec-recurrent-exact.py
```

Result:

```json
{"candidate_output_max_abs_diff": 0.0, "candidate_state_max_abs_diff": 0.0, "device": "xpu:0", "num_reqs": 2, "old_accepted_count_path_equal": false, "old_state_max_abs_diff": 4.02734375, "output_equal": true, "spec_len": 3, "state_equal": true}
```

The candidate path is bit-identical to the one-token sequential reference for
both verifier outputs and stored recurrent states. The old accepted-count packed
path does not match the reference state columns.

## Endpoint Validation

Operator command:

```bash
cd /home/steve/llm-optimizations
MODEL_PATH=/mnt/fast-ai/qwen36-quark-int8-fp8-mtp-hybrid \
SERVER_LAUNCHER=scripts/launch-qwen36-quark-int8-accepted.sh \
VLLM_QWEN35_MTP_FORCE_FP8_BLOCK=1 \
VLLM_EXTRA_ARGS='--speculative-config {"method":"mtp","num_speculative_tokens":1}' \
COMPILATION_CONFIG='{"cudagraph_mode":"PIECEWISE","max_cudagraph_capture_size":128}' \
XPU_GRAPH=1 VLLM_XPU_ENABLE_XPU_GRAPH=1 VLLM_XPU_FORCE_GRAPH_WITH_COMM=1 \
VLLM_XPU_GRAPH_NOOP_COMM_CAPTURE=1 VLLM_XPU_GDN_NATIVE_FALLBACK=prefill \
VLLM_XPU_GDN_PREFILL_RECURRENT_FALLBACK=1 VLLM_XPU_DISABLE_PREFILL_CUDAGRAPH_REPLAY=1 \
VLLM_XPU_GREEDY_SAMPLE_TOPK_FALLBACK=1 VLLM_XPU_INT8_MOE_MIXED_WORKSPACE=1 \
GPU_MEMORY_UTILIZATION=0.95 ABLATION_FAST_GRAPH_AUTOCONFIG=0 \
bash scripts/run-qwen36-ablation-candidate.sh tp4-mtp-k1-parity-validate
```

Success criteria: json-canary 96/96 and color-canary 96/96 against the no-spec
baseline.
