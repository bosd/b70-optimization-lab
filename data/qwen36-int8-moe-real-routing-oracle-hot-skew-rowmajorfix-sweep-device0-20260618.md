# Qwen3.6 INT8 MoE Route Replay

- Fused SiLU+quant enabled: `False`.
- TP size: `4`.
- Result rows: `5`.
- Route mode/source: `synthetic_hot_skew`.
- Quant out-variant available: `True`.
- Prologue-inclusive target: `160.000 us/layerlet`.
- Exactness threshold: `0.000000`.

## Exactness

- Manual staged max abs diff versus `xpu_fused_moe`: `0.000`.
- Scratch `xpu_fused_moe` max abs diff: `0.000`.
- Preallocated staged max abs diff: `0.000`.
- Fused-prologue staged max abs diff: `0.000`.
- Fused-prologue offset-GEMM max abs diff: `0.000`.
- Full C++ layerlet max abs diff: `0.000`.

### Rows-Oracle Checks

- Current `xpu_fused_moe` max abs diff versus forced rows-per-expert oracle: `0.000`.
- Forced offset-GEMM max abs diff versus rows-per-expert oracle: `0.000`.
- Full C++ layerlet max abs diff versus rows-per-expert oracle: `0.000`.
- Rows-per-expert INT8 oracle max abs diff versus BF16 dequantized reference: `2.000`.

## Timing

- Mean `xpu_fused_moe`: `317.810 us`.
- Mean scratch `xpu_fused_moe`: `266.215 us`.
- Mean preallocated staged: `208.019 us`.
- Mean fused-prologue staged: `284.822 us`.
- Mean fused-prologue offset-GEMM staged: `206.706 us`.
- Mean full C++ layerlet: `172.572 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | None | 8 | 377.634 | 315.933 | 245.108 | 340.473 | 250.630 | n/a | n/a | 201.172 | 114.098 | 112.853 | 197.281 |
| 2 | None | 12 | 294.635 | 247.114 | 191.623 | 262.756 | 189.221 | n/a | n/a | 159.299 | 90.428 | 92.043 | 158.301 |
| 4 | None | 14 | 292.532 | 242.970 | 191.815 | 260.507 | 189.842 | n/a | n/a | 161.083 | 91.276 | 91.166 | 159.542 |
| 8 | None | 16 | 291.964 | 244.488 | 191.269 | 259.906 | 188.325 | n/a | n/a | 160.326 | 89.837 | 91.803 | 157.290 |
| 16 | None | 16 | 332.283 | 280.572 | 220.278 | 300.466 | 215.511 | n/a | n/a | 180.980 | 103.031 | 101.468 | 175.191 |

## Prologue-Inclusive Gate

- Gate status: `some_rows_have_exact_nonreference_layerlet_candidate`.
- Rows ready for endpoint gate: `1` / `5`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `159.299 us` (`1.850x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | None | full_layerlet | 201.172 | 1.877 | False | best_exact_nonreference_misses_target_layerlet_us |
| 2 | None | full_layerlet | 159.299 | 1.850 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 4 | None | full_layerlet | 161.083 | 1.816 | False | best_exact_nonreference_misses_target_layerlet_us |
| 8 | None | full_layerlet | 160.326 | 1.821 | False | best_exact_nonreference_misses_target_layerlet_us |
| 16 | None | full_layerlet | 180.980 | 1.836 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
