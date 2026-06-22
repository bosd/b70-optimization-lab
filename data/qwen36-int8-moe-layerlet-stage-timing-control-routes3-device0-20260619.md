# Qwen3.6 INT8 MoE Route Replay

- Fused SiLU+quant enabled: `False`.
- TP size: `4`.
- Result rows: `3`.
- Route mode/source: `route_jsonl`.
- Quant out-variant available: `True`.
- Route source: `/home/steve/llm-optimizations/data/qwen36-quark-int8-tp4-routecapture6-routes-rank0-20260611.jsonl`.
- Route records matched: `95`; top-k rows loaded: `95`.
- Route start indices: `0,80,115`.
- Prologue-inclusive target: `160.000 us/layerlet`.
- Exactness threshold: `0.000000`.

## Exactness

- Manual staged max abs diff versus `xpu_fused_moe`: `0.000`.
- Scratch `xpu_fused_moe` max abs diff: `0.000`.
- Preallocated staged max abs diff: `0.000`.
- Fused-prologue staged max abs diff: `0.000`.
- Fused-prologue offset-GEMM max abs diff: `0.000`.
- Full C++ layerlet max abs diff: `0.000`.

## Timing

- Mean `xpu_fused_moe`: `318.948 us`.
- Mean scratch `xpu_fused_moe`: `261.328 us`.
- Mean preallocated staged: `204.094 us`.
- Mean fused-prologue staged: `286.459 us`.
- Mean fused-prologue offset-GEMM staged: `205.281 us`.
- Mean full C++ layerlet: `170.596 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 310.381 | 254.301 | 200.723 | 282.986 | 200.344 | n/a | n/a | 165.459 | 96.060 | 97.455 | 169.005 |
| 1 | 80 | 8 | 324.267 | 263.971 | 204.114 | 296.272 | 208.432 | n/a | n/a | 175.666 | 99.980 | 99.336 | 174.840 |
| 1 | 115 | 8 | 322.197 | 265.711 | 207.445 | 280.119 | 207.067 | n/a | n/a | 170.664 | 98.784 | 100.086 | 174.214 |

## Prologue Offset Stage Timing

These stage timings are for the exact fused-prologue offset-GEMM candidate and are used to decide the next native layerlet boundary. They are single-device replay diagnostics.

| rows | route start | total us | prologue | quant1 | gemm1 | activation | quant2 | gemm2 | gather | component sum |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 200.344 | 103.958 | 80.950 | 94.789 | 77.085 | 80.142 | 94.440 | 79.484 | 610.849 |
| 1 | 80 | 208.432 | 102.998 | 78.201 | 93.189 | 75.537 | 77.427 | 92.684 | 77.921 | 597.957 |
| 1 | 115 | 207.067 | 100.756 | 78.147 | 92.300 | 75.024 | 77.344 | 91.451 | 79.424 | 594.445 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `3`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `165.459 us` (`1.876x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 165.459 | 1.876 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 175.666 | 1.846 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 170.664 | 1.888 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
