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
- Fused-prologue active-offset-GEMM max abs diff: `0.000`.
- Fused-prologue middle-layerlet max abs diff: `0.000`.
- Full C++ layerlet max abs diff: `0.000`.

### Rows-Oracle Checks

- Current `xpu_fused_moe` max abs diff versus forced rows-per-expert oracle: `0.000`.
- Forced offset-GEMM max abs diff versus rows-per-expert oracle: `0.000`.
- Full C++ layerlet max abs diff versus rows-per-expert oracle: `0.000`.

## Timing

- Mean `xpu_fused_moe`: `312.845 us`.
- Mean scratch `xpu_fused_moe`: `258.943 us`.
- Mean preallocated staged: `200.578 us`.
- Mean fused-prologue staged: `270.459 us`.
- Mean fused-prologue offset-GEMM staged: `198.566 us`.
- Mean fused-prologue active-offset-GEMM staged: `199.549 us`.
- Mean fused-prologue middle-layerlet staged: `168.542 us`.
- Mean full C++ layerlet: `167.934 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | None | 8 | 315.653 | 259.707 | 202.520 | 272.155 | 198.386 | 200.102 | 168.792 | 187.122 | 95.349 | 94.367 | 165.035 |
| 2 | None | 12 | 316.459 | 265.128 | 202.501 | 272.714 | 199.823 | 200.772 | 167.921 | 163.722 | 93.996 | 94.997 | 167.667 |
| 4 | None | 14 | 309.705 | 253.987 | 198.198 | 267.787 | 197.106 | 195.026 | 167.212 | 164.606 | 92.547 | 95.784 | 162.006 |
| 8 | None | 16 | 315.075 | 258.589 | 199.407 | 270.634 | 199.621 | 200.824 | 171.210 | 163.241 | 94.035 | 94.139 | 165.925 |
| 16 | None | 16 | 307.333 | 257.302 | 200.265 | 269.002 | 197.892 | 201.019 | 167.576 | 160.979 | 94.061 | 104.578 | 164.482 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `5`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `160.979 us` (`1.909x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | None | fused_prologue_middle_layerlet | 168.792 | 1.870 | False | best_exact_nonreference_misses_target_layerlet_us |
| 2 | None | full_layerlet | 163.722 | 1.933 | False | best_exact_nonreference_misses_target_layerlet_us |
| 4 | None | full_layerlet | 164.606 | 1.881 | False | best_exact_nonreference_misses_target_layerlet_us |
| 8 | None | full_layerlet | 163.241 | 1.930 | False | best_exact_nonreference_misses_target_layerlet_us |
| 16 | None | full_layerlet | 160.979 | 1.909 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
