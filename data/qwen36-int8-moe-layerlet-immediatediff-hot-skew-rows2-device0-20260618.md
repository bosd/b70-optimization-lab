# Qwen3.6 INT8 MoE Route Replay

- Fused SiLU+quant enabled: `False`.
- TP size: `4`.
- Result rows: `1`.
- Route mode/source: `synthetic_hot_skew`.
- Quant out-variant available: `True`.
- Prologue-inclusive target: `160.000 us/layerlet`.
- Exactness threshold: `0.000000`.

## Exactness

- Manual staged max abs diff versus `xpu_fused_moe`: `0.000`.
- Scratch `xpu_fused_moe` max abs diff: `0.000`.
- Preallocated staged max abs diff: `0.000`.
- Fused-prologue staged max abs diff: `235.000`.
- Fused-prologue offset-GEMM max abs diff: `235.000`.
- Fused-prologue middle-layerlet max abs diff: `235.000`.
- Full C++ layerlet max abs diff: `0.000`.

### Rows-Oracle Checks

- Current `xpu_fused_moe` max abs diff versus forced rows-per-expert oracle: `0.000`.
- Forced offset-GEMM max abs diff versus rows-per-expert oracle: `0.000`.
- Full C++ layerlet max abs diff versus rows-per-expert oracle: `0.000`.

## Timing

- Mean `xpu_fused_moe`: `301.873 us`.
- Mean scratch `xpu_fused_moe`: `257.829 us`.
- Mean preallocated staged: `190.762 us`.
- Mean fused-prologue staged: `257.621 us`.
- Mean fused-prologue offset-GEMM staged: `191.867 us`.
- Mean fused-prologue middle-layerlet staged: `167.050 us`.
- Mean full C++ layerlet: `170.625 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | None | 12 | 301.873 | 257.829 | 190.762 | 257.621 | 191.867 | n/a | 167.050 | 170.625 | 89.765 | 97.162 | 158.483 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `1`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `170.625 us` (`1.769x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 2 | None | full_layerlet | 170.625 | 1.769 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is not exact against `xpu_fused_moe`; do not use it as an endpoint candidate.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
