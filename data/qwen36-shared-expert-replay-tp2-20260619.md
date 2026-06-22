# Qwen3.6 Shared-Expert Replay

- Device selector: `Intel(R) Arc(TM) Pro B70 Graphics`
- Config: `/mnt/fast-ai/llm-cache/hf/models--nameistoken--Qwen3.6-35B-A3B-Quark-W8A8-INT8/snapshots/cced56592e8c8935f8220836b4baa04dfd389118/config.json`
- TP size: `2`
- Iterations: `100` warmup `20`

| rows | baseline us | fused alloc us | fused out us | fused out diff |
|---:|---:|---:|---:|---:|
| 1 | 257.750 | 248.091 | 237.169 | 0 |
| 2 | 251.641 | 241.310 | 237.019 | 0 |
| 4 | 251.932 | 243.700 | 251.578 | 0 |
| 8 | 260.580 | 249.661 | 249.491 | 0 |
| 16 | 256.052 | 241.954 | 228.372 | 0 |
| 32 | 252.939 | 247.937 | 240.452 | 0 |

## Stage Means

### rows=1

| stage | mean us | min us | max us |
|---|---:|---:|---:|
| `quant_x_plus_gate_up_int8_gemm` | 125.143 | 121.680 | 145.288 |
| `separate_silu_mul_quant_down_int8_gemm` | 132.487 | 128.804 | 149.864 |
| `fused_alloc_silu_quant_down_int8_gemm` | 123.160 | 120.536 | 139.204 |
| `fused_out_silu_quant_down_int8_gemm` | 118.681 | 115.908 | 141.440 |
| `expert_gate_sigmoid_mul` | 140.645 | 135.668 | 154.596 |

### rows=2

| stage | mean us | min us | max us |
|---|---:|---:|---:|
| `quant_x_plus_gate_up_int8_gemm` | 124.174 | 121.524 | 134.472 |
| `separate_silu_mul_quant_down_int8_gemm` | 132.071 | 129.636 | 142.792 |
| `fused_alloc_silu_quant_down_int8_gemm` | 123.112 | 120.588 | 136.188 |
| `fused_out_silu_quant_down_int8_gemm` | 118.848 | 115.960 | 137.280 |
| `expert_gate_sigmoid_mul` | 143.331 | 137.904 | 311.792 |

### rows=4

| stage | mean us | min us | max us |
|---|---:|---:|---:|
| `quant_x_plus_gate_up_int8_gemm` | 130.756 | 127.192 | 142.844 |
| `separate_silu_mul_quant_down_int8_gemm` | 139.897 | 132.756 | 159.016 |
| `fused_alloc_silu_quant_down_int8_gemm` | 129.875 | 126.932 | 142.272 |
| `fused_out_silu_quant_down_int8_gemm` | 128.046 | 115.908 | 173.732 |
| `expert_gate_sigmoid_mul` | 194.438 | 141.596 | 247.780 |

### rows=8

| stage | mean us | min us | max us |
|---|---:|---:|---:|
| `quant_x_plus_gate_up_int8_gemm` | 131.149 | 124.280 | 146.276 |
| `separate_silu_mul_quant_down_int8_gemm` | 139.320 | 131.144 | 149.916 |
| `fused_alloc_silu_quant_down_int8_gemm` | 130.609 | 126.620 | 140.452 |
| `fused_out_silu_quant_down_int8_gemm` | 125.259 | 121.472 | 134.316 |
| `expert_gate_sigmoid_mul` | 147.206 | 140.452 | 161.720 |

### rows=16

| stage | mean us | min us | max us |
|---|---:|---:|---:|
| `quant_x_plus_gate_up_int8_gemm` | 120.300 | 117.572 | 132.600 |
| `separate_silu_mul_quant_down_int8_gemm` | 127.947 | 124.644 | 154.128 |
| `fused_alloc_silu_quant_down_int8_gemm` | 119.758 | 115.908 | 234.624 |
| `fused_out_silu_quant_down_int8_gemm` | 114.138 | 111.592 | 129.220 |
| `expert_gate_sigmoid_mul` | 141.114 | 137.488 | 152.516 |

### rows=32

| stage | mean us | min us | max us |
|---|---:|---:|---:|
| `quant_x_plus_gate_up_int8_gemm` | 126.608 | 119.132 | 138.060 |
| `separate_silu_mul_quant_down_int8_gemm` | 130.758 | 125.840 | 152.048 |
| `fused_alloc_silu_quant_down_int8_gemm` | 125.957 | 122.668 | 137.436 |
| `fused_out_silu_quant_down_int8_gemm` | 120.590 | 118.092 | 130.000 |
| `expert_gate_sigmoid_mul` | 147.902 | 143.676 | 160.212 |

