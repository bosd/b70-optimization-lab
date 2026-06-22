# Qwen3.6 INT8 MoE Route Replay

- Fused SiLU+quant enabled: `False`.
- TP size: `4`.
- Result rows: `7`.
- Route mode/source: `route_jsonl`.
- Quant out-variant available: `True`.
- Route source: `/home/steve/llm-optimizations/data/qwen36-quark-int8-tp4-routecapture6-routes-rank0-20260611.jsonl`.
- Route records matched: `285`; top-k rows loaded: `285`.
- Route start indices: `0,40,80,85,95,100,115`.
- Prologue-inclusive target: `160.000 us/layerlet`.
- Exactness threshold: `0.000000`.

## Exactness

- Manual staged max abs diff versus `xpu_fused_moe`: `0.000`.
- Scratch `xpu_fused_moe` max abs diff: `0.000`.
- Prologue-scratch `xpu_fused_moe` max abs diff: `0.000`.
- Preallocated staged max abs diff: `0.000`.
- Fused-prologue staged max abs diff: `0.000`.
- Fused-prologue offset-GEMM max abs diff: `0.000`.
- Fused-prologue active-offset-GEMM max abs diff: `0.000`.
- Full C++ layerlet max abs diff: `0.000`.

### Rows-Oracle Checks

- Current `xpu_fused_moe` max abs diff versus forced rows-per-expert oracle: `0.000`.
- Forced offset-GEMM max abs diff versus rows-per-expert oracle: `0.000`.
- Full C++ layerlet max abs diff versus rows-per-expert oracle: `0.000`.

## Timing

- Mean `xpu_fused_moe`: `344.938 us`.
- Mean scratch `xpu_fused_moe`: `279.939 us`.
- Mean prologue-scratch `xpu_fused_moe`: `284.769 us`.
- Mean preallocated staged: `220.079 us`.
- Mean fused-prologue staged: `298.849 us`.
- Mean fused-prologue offset-GEMM staged: `217.648 us`.
- Mean fused-prologue active-offset-GEMM staged: `220.675 us`.
- Mean full C++ layerlet: `185.176 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | xpu prologue scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 317.823 | 264.496 | 272.102 | 207.682 | 280.033 | 202.214 | 207.012 | n/a | 174.180 | 97.672 | 97.913 | 170.865 |
| 1 | 40 | 8 | 355.602 | 285.569 | 288.504 | 225.469 | 310.968 | 220.953 | 225.899 | n/a | 189.550 | 107.115 | 107.834 | 185.334 |
| 1 | 80 | 8 | 345.175 | 275.169 | 281.939 | 220.056 | 295.998 | 217.900 | 220.269 | n/a | 184.993 | 103.485 | 104.420 | 180.219 |
| 1 | 85 | 8 | 341.061 | 278.818 | 282.642 | 218.463 | 297.860 | 217.146 | 219.088 | n/a | 182.282 | 104.198 | 103.919 | 180.681 |
| 1 | 95 | 8 | 340.797 | 277.682 | 282.075 | 217.199 | 293.716 | 216.567 | 217.878 | n/a | 184.122 | 103.161 | 103.588 | 179.004 |
| 1 | 100 | 8 | 350.055 | 287.328 | 291.576 | 222.200 | 298.576 | 217.098 | 220.524 | n/a | 187.882 | 105.004 | 107.017 | 182.210 |
| 1 | 115 | 8 | 364.051 | 290.510 | 294.543 | 229.481 | 314.793 | 231.654 | 234.051 | n/a | 193.227 | 110.835 | 108.417 | 186.993 |

## Graph Replay Timing

These timings capture each eligible candidate in an XPU graph and time `graph.replay()`. They remain single-device replay diagnostics, not endpoint throughput.

| rows | route start | candidate | status | graph us |
|---:|---:|---|---|---:|
| 1 | 0 | xpu_fused_moe_with_scratch | executed | 318.014 |
| 1 | 0 | xpu_fused_moe_with_prologue_scratch | executed | 324.299 |
| 1 | 0 | preallocated_staged | executed | 331.898 |
| 1 | 0 | fused_prologue_staged | executed | 336.130 |
| 1 | 0 | fused_prologue_offset_gemm | executed | 223.938 |
| 1 | 0 | fused_prologue_active_offset_gemm | executed | 180.966 |
| 1 | 0 | full_layerlet | executed | 179.882 |
| 1 | 40 | xpu_fused_moe_with_scratch | executed | 319.845 |
| 1 | 40 | xpu_fused_moe_with_prologue_scratch | executed | 336.131 |
| 1 | 40 | preallocated_staged | executed | 335.812 |
| 1 | 40 | fused_prologue_staged | executed | 336.423 |
| 1 | 40 | fused_prologue_offset_gemm | executed | 235.845 |
| 1 | 40 | fused_prologue_active_offset_gemm | executed | 177.018 |
| 1 | 40 | full_layerlet | executed | 188.690 |
| 1 | 80 | xpu_fused_moe_with_scratch | executed | 262.103 |
| 1 | 80 | xpu_fused_moe_with_prologue_scratch | executed | 178.868 |
| 1 | 80 | preallocated_staged | executed | 178.882 |
| 1 | 80 | fused_prologue_staged | executed | 189.063 |
| 1 | 80 | fused_prologue_offset_gemm | executed | 191.887 |
| 1 | 80 | fused_prologue_active_offset_gemm | executed | 178.391 |
| 1 | 80 | full_layerlet | executed | 183.117 |
| 1 | 85 | xpu_fused_moe_with_scratch | executed | 328.280 |
| 1 | 85 | xpu_fused_moe_with_prologue_scratch | executed | 333.681 |
| 1 | 85 | preallocated_staged | executed | 224.058 |
| 1 | 85 | fused_prologue_staged | executed | 173.764 |
| 1 | 85 | fused_prologue_offset_gemm | executed | 179.852 |
| 1 | 85 | fused_prologue_active_offset_gemm | executed | 147.760 |
| 1 | 85 | full_layerlet | executed | 173.513 |
| 1 | 95 | xpu_fused_moe_with_scratch | executed | 319.686 |
| 1 | 95 | xpu_fused_moe_with_prologue_scratch | executed | 329.388 |
| 1 | 95 | preallocated_staged | executed | 337.094 |
| 1 | 95 | fused_prologue_staged | executed | 339.440 |
| 1 | 95 | fused_prologue_offset_gemm | executed | 191.679 |
| 1 | 95 | fused_prologue_active_offset_gemm | executed | 155.769 |
| 1 | 95 | full_layerlet | executed | 177.232 |
| 1 | 100 | xpu_fused_moe_with_scratch | executed | 319.991 |
| 1 | 100 | xpu_fused_moe_with_prologue_scratch | executed | 329.557 |
| 1 | 100 | preallocated_staged | executed | 328.249 |
| 1 | 100 | fused_prologue_staged | executed | 337.582 |
| 1 | 100 | fused_prologue_offset_gemm | executed | 264.714 |
| 1 | 100 | fused_prologue_active_offset_gemm | executed | 149.151 |
| 1 | 100 | full_layerlet | executed | 168.959 |
| 1 | 115 | xpu_fused_moe_with_scratch | executed | 317.877 |
| 1 | 115 | xpu_fused_moe_with_prologue_scratch | executed | 324.169 |
| 1 | 115 | preallocated_staged | executed | 318.805 |
| 1 | 115 | fused_prologue_staged | executed | 325.487 |
| 1 | 115 | fused_prologue_offset_gemm | executed | 289.134 |
| 1 | 115 | fused_prologue_active_offset_gemm | executed | 158.927 |
| 1 | 115 | full_layerlet | executed | 177.187 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `7`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `174.180 us` (`1.825x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 174.180 | 1.825 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | full_layerlet | 189.550 | 1.876 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 184.993 | 1.866 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | full_layerlet | 182.282 | 1.871 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 95 | full_layerlet | 184.122 | 1.851 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | full_layerlet | 187.882 | 1.863 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 193.227 | 1.884 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
