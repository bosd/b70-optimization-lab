# Qwen3.6 INT8 MoE Route Replay

- Fused SiLU+quant enabled: `False`.
- TP size: `4`.
- Result rows: `12`.
- Route mode/source: `route_jsonl`.
- Quant out-variant available: `True`.
- Route source: `/home/steve/llm-optimizations/data/qwen36-quark-int8-tp4-firstdecode-route-fixture-routes-20260612ct.jsonl`.
- Route records matched: `120`; top-k rows loaded: `120`.
- Route start indices: `0,10,20,30,40,50,60,70,80,90,100,110`.
- Prologue-inclusive target: `160.000 us/layerlet`.
- Exactness threshold: `0.000000`.

## Exactness

- Manual staged max abs diff versus `xpu_fused_moe`: `0.000`.
- Scratch `xpu_fused_moe` max abs diff: `0.000`.
- Preallocated staged max abs diff: `0.000`.
- Fused-prologue staged max abs diff: `0.000`.
- Fused-prologue offset-GEMM max abs diff: `0.000`.
- Fused-prologue active-offset-GEMM max abs diff: `0.000`.
- Fused-prologue middle-layerlet max abs diff: `0.000`.
- Full C++ layerlet max abs diff: `0.000`.

### Rows-Oracle Checks

- Current `xpu_fused_moe` max abs diff versus forced rows-per-expert oracle: `0.000`.
- Forced offset-GEMM max abs diff versus rows-per-expert oracle: `0.000`.
- Full C++ layerlet max abs diff versus rows-per-expert oracle: `0.000`.

## Timing

- Mean `xpu_fused_moe`: `346.287 us`.
- Mean scratch `xpu_fused_moe`: `283.200 us`.
- Mean preallocated staged: `220.529 us`.
- Mean fused-prologue staged: `303.014 us`.
- Mean fused-prologue offset-GEMM staged: `221.938 us`.
- Mean fused-prologue active-offset-GEMM staged: `223.121 us`.
- Mean fused-prologue middle-layerlet staged: `188.810 us`.
- Mean full C++ layerlet: `182.993 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 306.930 | 259.506 | 194.233 | 259.727 | 192.127 | 195.546 | 166.855 | 164.112 | 91.130 | 105.690 | 164.164 |
| 1 | 10 | 8 | 298.701 | 268.320 | 208.637 | 284.531 | 214.591 | 209.755 | 179.127 | 179.894 | 93.652 | 91.026 | 158.327 |
| 1 | 20 | 8 | 417.339 | 343.525 | 276.562 | 391.131 | 260.520 | 272.753 | 239.356 | 225.966 | 122.070 | 122.798 | 236.665 |
| 1 | 30 | 8 | 337.597 | 267.592 | 203.242 | 270.855 | 202.813 | 200.876 | 166.907 | 168.207 | 102.453 | 99.996 | 171.262 |
| 1 | 40 | 8 | 305.825 | 244.634 | 192.686 | 264.173 | 193.986 | 189.696 | 161.785 | 163.280 | 90.077 | 89.648 | 158.886 |
| 1 | 50 | 8 | 332.306 | 281.580 | 228.930 | 310.193 | 239.798 | 230.893 | 197.691 | 194.857 | 97.864 | 97.760 | 172.666 |
| 1 | 60 | 8 | 322.647 | 251.004 | 193.973 | 265.239 | 195.715 | 192.231 | 163.436 | 161.577 | 95.576 | 92.534 | 167.388 |
| 1 | 70 | 8 | 300.664 | 248.729 | 193.856 | 264.199 | 190.840 | 192.361 | 161.395 | 159.874 | 92.729 | 90.363 | 158.860 |
| 1 | 80 | 8 | 409.591 | 320.411 | 248.456 | 342.758 | 244.842 | 269.932 | 222.430 | 201.929 | 121.992 | 116.649 | 208.832 |
| 1 | 90 | 8 | 293.579 | 248.131 | 189.722 | 263.289 | 191.451 | 191.594 | 161.278 | 157.794 | 90.272 | 90.363 | 157.573 |
| 1 | 100 | 8 | 389.649 | 336.180 | 258.726 | 369.538 | 263.094 | 263.328 | 225.498 | 216.372 | 116.597 | 114.153 | 199.550 |
| 1 | 110 | 8 | 440.622 | 328.783 | 257.322 | 350.532 | 273.481 | 268.489 | 219.960 | 202.059 | 120.991 | 134.888 | 217.802 |

## Prologue-Inclusive Gate

- Gate status: `some_rows_have_exact_nonreference_layerlet_candidate`.
- Rows ready for endpoint gate: `2` / `12`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `157.794 us` (`1.861x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 164.112 | 1.870 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 10 | fused_prologue_middle_layerlet | 179.127 | 1.668 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 20 | full_layerlet | 225.966 | 1.847 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 30 | fused_prologue_middle_layerlet | 166.907 | 2.023 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | fused_prologue_middle_layerlet | 161.785 | 1.890 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 50 | full_layerlet | 194.857 | 1.705 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 60 | full_layerlet | 161.577 | 1.997 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 70 | full_layerlet | 159.874 | 1.881 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 80 | full_layerlet | 201.929 | 2.028 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 90 | full_layerlet | 157.794 | 1.861 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 100 | full_layerlet | 216.372 | 1.801 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 110 | full_layerlet | 202.059 | 2.181 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
