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
- Fused-prologue middle-layerlet max abs diff: `0.000`.
- Full C++ layerlet max abs diff: `0.000`.

### Rows-Oracle Checks

- Current `xpu_fused_moe` max abs diff versus forced rows-per-expert oracle: `0.000`.
- Forced offset-GEMM max abs diff versus rows-per-expert oracle: `0.000`.
- Full C++ layerlet max abs diff versus rows-per-expert oracle: `0.000`.

## Timing

- Mean `xpu_fused_moe`: `339.020 us`.
- Mean scratch `xpu_fused_moe`: `274.719 us`.
- Mean preallocated staged: `216.905 us`.
- Mean fused-prologue staged: `292.735 us`.
- Mean fused-prologue offset-GEMM staged: `211.680 us`.
- Mean fused-prologue middle-layerlet staged: `186.579 us`.
- Mean full C++ layerlet: `182.218 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | None | 8 | 392.892 | 320.079 | 255.456 | 343.005 | 243.029 | n/a | 211.361 | 228.176 | 113.236 | 113.061 | 207.382 |
| 2 | None | 12 | 319.130 | 253.740 | 199.030 | 275.593 | 200.844 | n/a | 182.169 | 166.017 | 93.730 | 94.536 | 166.952 |
| 4 | None | 14 | 342.726 | 287.131 | 224.809 | 304.109 | 218.783 | n/a | 188.799 | 181.233 | 101.562 | 103.135 | 181.727 |
| 8 | None | 16 | 322.517 | 259.603 | 200.850 | 270.887 | 200.811 | n/a | 177.495 | 169.169 | 94.751 | 95.004 | 164.755 |
| 16 | None | 16 | 317.837 | 253.038 | 204.380 | 270.081 | 194.935 | n/a | 173.069 | 166.498 | 95.153 | 92.482 | 166.614 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `5`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `166.017 us` (`1.922x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | None | fused_prologue_middle_layerlet | 211.361 | 1.859 | False | best_exact_nonreference_misses_target_layerlet_us |
| 2 | None | full_layerlet | 166.017 | 1.922 | False | best_exact_nonreference_misses_target_layerlet_us |
| 4 | None | full_layerlet | 181.233 | 1.891 | False | best_exact_nonreference_misses_target_layerlet_us |
| 8 | None | full_layerlet | 169.169 | 1.906 | False | best_exact_nonreference_misses_target_layerlet_us |
| 16 | None | full_layerlet | 166.498 | 1.909 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
