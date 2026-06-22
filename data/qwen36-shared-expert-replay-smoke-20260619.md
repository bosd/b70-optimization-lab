# Qwen3.6 Shared-Expert Replay

- Device selector: `Intel(R) Arc(TM) Pro B70 Graphics`
- Config: `/mnt/fast-ai/llm-cache/hf/models--nameistoken--Qwen3.6-35B-A3B-Quark-W8A8-INT8/snapshots/cced56592e8c8935f8220836b4baa04dfd389118/config.json`
- TP size: `2`
- Iterations: `5` warmup `2`

| rows | baseline us | fused alloc us | fused out us | fused out diff |
|---:|---:|---:|---:|---:|
| 1 | 252.762 | 243.360 | 237.806 | 0 |
| 2 | 264.722 | 240.999 | 234.374 | 0 |

## Stage Means

### rows=1

| stage | mean us | min us | max us |
|---|---:|---:|---:|
| `quant_x_plus_gate_up_int8_gemm` | 125.726 | 123.552 | 131.040 |
| `separate_silu_mul_quant_down_int8_gemm` | 133.089 | 131.248 | 136.812 |
| `fused_alloc_silu_quant_down_int8_gemm` | 123.968 | 122.304 | 126.672 |
| `fused_out_silu_quant_down_int8_gemm` | 124.415 | 118.664 | 128.596 |
| `expert_gate_sigmoid_mul` | 142.158 | 141.284 | 142.844 |

### rows=2

| stage | mean us | min us | max us |
|---|---:|---:|---:|
| `quant_x_plus_gate_up_int8_gemm` | 123.157 | 122.720 | 123.396 |
| `separate_silu_mul_quant_down_int8_gemm` | 140.546 | 130.780 | 156.728 |
| `fused_alloc_silu_quant_down_int8_gemm` | 122.824 | 121.108 | 124.592 |
| `fused_out_silu_quant_down_int8_gemm` | 116.626 | 115.908 | 117.104 |
| `expert_gate_sigmoid_mul` | 174.855 | 139.828 | 310.596 |

