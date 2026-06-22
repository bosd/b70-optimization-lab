# Qwen3.6 Shared-Expert Replay

- Device selector: `Intel(R) Arc(TM) Pro B70 Graphics`
- Config: `/mnt/fast-ai/llm-cache/hf/models--nameistoken--Qwen3.6-35B-A3B-Quark-W8A8-INT8/snapshots/cced56592e8c8935f8220836b4baa04dfd389118/config.json`
- TP size: `2`
- Iterations: `100` warmup `20`

| rows | baseline us | fused alloc us | fused out us | C++ boundary us | C++ diff |
|---:|---:|---:|---:|---:|---:|
| 1 | 264.540 | 251.120 | 245.526 | 216.180 | 0 |
| 2 | 250.995 | 283.915 | 245.303 | 206.868 | 0 |
| 4 | 247.807 | 236.528 | 233.323 | 260.857 | 0 |
| 8 | 248.311 | 237.142 | 236.464 | 273.691 | 0 |
| 16 | 283.551 | 243.307 | 237.075 | 208.777 | 0 |
| 32 | 311.497 | 260.770 | 270.655 | 215.368 | 0 |

## Stage Means

### rows=1

| stage | mean us | min us | max us |
|---|---:|---:|---:|
| `quant_x_plus_gate_up_int8_gemm` | 143.483 | 124.904 | 244.504 |
| `separate_silu_mul_quant_down_int8_gemm` | 183.115 | 154.804 | 249.496 |
| `fused_alloc_silu_quant_down_int8_gemm` | 131.753 | 119.964 | 178.828 |
| `fused_out_silu_quant_down_int8_gemm` | 118.083 | 115.284 | 132.288 |
| `expert_gate_sigmoid_mul` | 139.502 | 133.120 | 151.372 |

### rows=2

| stage | mean us | min us | max us |
|---|---:|---:|---:|
| `quant_x_plus_gate_up_int8_gemm` | 124.520 | 120.796 | 141.804 |
| `separate_silu_mul_quant_down_int8_gemm` | 131.582 | 128.284 | 142.896 |
| `fused_alloc_silu_quant_down_int8_gemm` | 122.989 | 115.856 | 142.168 |
| `fused_out_silu_quant_down_int8_gemm` | 117.660 | 115.232 | 127.140 |
| `expert_gate_sigmoid_mul` | 139.128 | 135.824 | 148.928 |

### rows=4

| stage | mean us | min us | max us |
|---|---:|---:|---:|
| `quant_x_plus_gate_up_int8_gemm` | 171.688 | 144.872 | 240.344 |
| `separate_silu_mul_quant_down_int8_gemm` | 189.255 | 176.540 | 257.816 |
| `fused_alloc_silu_quant_down_int8_gemm` | 176.546 | 150.644 | 224.380 |
| `fused_out_silu_quant_down_int8_gemm` | 149.928 | 118.196 | 235.352 |
| `expert_gate_sigmoid_mul` | 141.445 | 134.316 | 157.508 |

### rows=8

| stage | mean us | min us | max us |
|---|---:|---:|---:|
| `quant_x_plus_gate_up_int8_gemm` | 142.266 | 125.008 | 211.432 |
| `separate_silu_mul_quant_down_int8_gemm` | 137.469 | 131.092 | 149.396 |
| `fused_alloc_silu_quant_down_int8_gemm` | 159.339 | 121.836 | 279.136 |
| `fused_out_silu_quant_down_int8_gemm` | 160.113 | 128.284 | 209.144 |
| `expert_gate_sigmoid_mul` | 157.271 | 136.812 | 206.232 |

### rows=16

| stage | mean us | min us | max us |
|---|---:|---:|---:|
| `quant_x_plus_gate_up_int8_gemm` | 124.554 | 121.056 | 149.084 |
| `separate_silu_mul_quant_down_int8_gemm` | 132.308 | 128.544 | 144.248 |
| `fused_alloc_silu_quant_down_int8_gemm` | 136.238 | 119.496 | 176.020 |
| `fused_out_silu_quant_down_int8_gemm` | 144.576 | 111.072 | 212.472 |
| `expert_gate_sigmoid_mul` | 200.424 | 186.836 | 282.620 |

### rows=32

| stage | mean us | min us | max us |
|---|---:|---:|---:|
| `quant_x_plus_gate_up_int8_gemm` | 156.824 | 121.784 | 202.800 |
| `separate_silu_mul_quant_down_int8_gemm` | 166.465 | 125.476 | 238.264 |
| `fused_alloc_silu_quant_down_int8_gemm` | 118.208 | 114.868 | 138.840 |
| `fused_out_silu_quant_down_int8_gemm` | 113.549 | 110.916 | 126.984 |
| `expert_gate_sigmoid_mul` | 139.239 | 136.084 | 156.520 |

