# Qwen3.6 INT8 MoE Route Replay

- Fused SiLU+quant enabled: `False`.
- TP size: `4`.
- Result rows: `5`.
- Route mode/source: `synthetic_uniform`.
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

## Timing

- Mean `xpu_fused_moe`: `344.787 us`.
- Mean scratch `xpu_fused_moe`: `288.462 us`.
- Mean preallocated staged: `239.850 us`.
- Mean fused-prologue staged: `310.272 us`.
- Mean fused-prologue offset-GEMM staged: `240.094 us`.
- Mean full C++ layerlet: `215.728 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | None | 8 | 359.157 | 295.990 | 234.201 | 312.130 | 226.746 | n/a | n/a | 191.958 | 110.682 | 108.192 | 191.704 |
| 2 | None | 16 | 373.536 | 291.323 | 227.779 | 305.311 | 236.684 | n/a | n/a | 194.233 | 108.511 | 107.016 | 188.721 |
| 4 | None | 32 | 305.669 | 250.224 | 194.311 | 265.870 | 192.387 | n/a | n/a | 164.463 | 97.136 | 95.647 | 172.276 |
| 8 | None | 64 | 308.776 | 264.394 | 232.505 | 294.333 | 233.311 | n/a | n/a | 224.438 | 111.553 | 97.682 | 170.215 |
| 16 | None | 128 | 376.798 | 340.379 | 310.453 | 373.717 | 311.344 | n/a | n/a | 303.550 | 163.572 | 109.265 | 175.481 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `5`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `164.463 us` (`1.859x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | None | full_layerlet | 191.958 | 1.871 | False | best_exact_nonreference_misses_target_layerlet_us |
| 2 | None | full_layerlet | 194.233 | 1.923 | False | best_exact_nonreference_misses_target_layerlet_us |
| 4 | None | full_layerlet | 164.463 | 1.859 | False | best_exact_nonreference_misses_target_layerlet_us |
| 8 | None | full_layerlet | 224.438 | 1.376 | False | best_exact_nonreference_misses_target_layerlet_us |
| 16 | None | full_layerlet | 303.550 | 1.241 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
