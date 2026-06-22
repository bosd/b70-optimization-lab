# Qwen3.6 Shared-Expert Replay

- Device selector: `Intel(R) Arc(TM) Pro B70 Graphics`
- Config: `/mnt/fast-ai/llm-cache/hf/models--nameistoken--Qwen3.6-35B-A3B-Quark-W8A8-INT8/snapshots/cced56592e8c8935f8220836b4baa04dfd389118/config.json`
- TP size: `2`
- Iterations: `5` warmup `2`

| rows | baseline us | fused alloc us | fused out us | C++ boundary us | C++ diff |
|---:|---:|---:|---:|---:|---:|
| 1 | 265.294 | 252.720 | 251.971 | 218.566 | 0 |
| 2 | 265.512 | 262.018 | 254.415 | 230.027 | 0 |

## Stage Means

### rows=1

| stage | mean us | min us | max us |
|---|---:|---:|---:|
| `quant_x_plus_gate_up_int8_gemm` | 131.529 | 130.416 | 132.652 |
| `separate_silu_mul_quant_down_int8_gemm` | 145.246 | 141.284 | 155.532 |
| `fused_alloc_silu_quant_down_int8_gemm` | 132.153 | 128.492 | 141.544 |
| `fused_out_silu_quant_down_int8_gemm` | 129.823 | 126.048 | 139.412 |
| `expert_gate_sigmoid_mul` | 151.247 | 148.252 | 158.860 |

### rows=2

| stage | mean us | min us | max us |
|---|---:|---:|---:|
| `quant_x_plus_gate_up_int8_gemm` | 135.689 | 131.456 | 144.352 |
| `separate_silu_mul_quant_down_int8_gemm` | 146.234 | 141.440 | 157.040 |
| `fused_alloc_silu_quant_down_int8_gemm` | 136.843 | 132.756 | 143.416 |
| `fused_out_silu_quant_down_int8_gemm` | 131.414 | 128.440 | 137.748 |
| `expert_gate_sigmoid_mul` | 153.494 | 150.436 | 160.108 |

