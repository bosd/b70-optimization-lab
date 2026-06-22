# Qwen3.6 INT8 MoE Route Replay

- Fused SiLU+quant enabled: `False`.
- TP size: `4`.
- Result rows: `2`.
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

- Mean `xpu_fused_moe`: `335.276 us`.
- Mean scratch `xpu_fused_moe`: `279.361 us`.
- Mean preallocated staged: `217.373 us`.
- Mean fused-prologue staged: `293.061 us`.
- Mean fused-prologue offset-GEMM staged: `210.444 us`.
- Mean fused-prologue middle-layerlet staged: `182.251 us`.
- Mean full C++ layerlet: `188.812 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | None | 8 | 349.995 | 295.824 | 228.765 | 302.614 | 220.029 | n/a | 190.957 | 201.240 | 104.962 | 105.972 | 185.259 |
| 2 | None | 12 | 320.558 | 262.899 | 205.981 | 283.508 | 200.859 | n/a | 173.546 | 176.384 | 101.023 | 91.537 | 164.199 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `2`.
- Best exact non-reference full-layerlet candidate: `fused_prologue_middle_layerlet` at `173.546 us` (`1.847x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | None | fused_prologue_middle_layerlet | 190.957 | 1.833 | False | best_exact_nonreference_misses_target_layerlet_us |
| 2 | None | fused_prologue_middle_layerlet | 173.546 | 1.847 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
