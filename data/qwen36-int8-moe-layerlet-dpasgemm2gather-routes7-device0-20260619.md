# Qwen3.6 INT8 MoE Route Replay

- Fused SiLU+quant enabled: `False`.
- TP size: `4`.
- Result rows: `7`.
- Route mode/source: `route_jsonl`.
- Quant out-variant available: `True`.
- Route source: `/home/steve/llm-optimizations/data/qwen36-quark-int8-tp4-routecapture6-routes-rank0-20260611.jsonl`.
- Route records matched: `95`; top-k rows loaded: `95`.
- Route start indices: `0,40,80,85,95,100,115`.
- Prologue-inclusive target: `160.000 us/layerlet`.
- Exactness threshold: `0.000000`.

## Exactness

- Manual staged max abs diff versus `xpu_fused_moe`: `0.000`.
- Scratch `xpu_fused_moe` max abs diff: `0.000`.
- Preallocated staged max abs diff: `0.000`.
- Fused-prologue staged max abs diff: `0.000`.
- Full C++ layerlet max abs diff: `0.000`.

## Timing

- Mean `xpu_fused_moe`: `317.945 us`.
- Mean scratch `xpu_fused_moe`: `262.913 us`.
- Mean preallocated staged: `205.848 us`.
- Mean fused-prologue staged: `279.852 us`.
- Mean full C++ layerlet: `172.244 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 332.022 | 271.941 | 215.612 | 290.969 | n/a | n/a | n/a | 178.651 | 99.542 | 99.651 | 175.182 |
| 1 | 40 | 8 | 318.423 | 262.802 | 205.147 | 280.334 | n/a | n/a | n/a | 171.993 | 96.529 | 97.834 | 170.886 |
| 1 | 80 | 8 | 322.910 | 264.837 | 209.199 | 283.350 | n/a | n/a | n/a | 174.527 | 97.544 | 98.311 | 171.277 |
| 1 | 85 | 8 | 320.833 | 270.032 | 208.914 | 283.357 | n/a | n/a | n/a | 174.027 | 96.851 | 98.340 | 173.329 |
| 1 | 95 | 8 | 329.360 | 270.337 | 211.881 | 288.551 | n/a | n/a | n/a | 177.481 | 100.502 | 99.105 | 173.789 |
| 1 | 100 | 8 | 305.742 | 254.368 | 197.474 | 270.456 | n/a | n/a | n/a | 167.477 | 93.835 | 95.649 | 165.340 |
| 1 | 115 | 8 | 296.324 | 246.075 | 192.710 | 261.949 | n/a | n/a | n/a | 161.554 | 91.324 | 91.665 | 159.749 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `7`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `161.554 us` (`1.834x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 178.651 | 1.858 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | full_layerlet | 171.993 | 1.851 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 174.527 | 1.850 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | full_layerlet | 174.027 | 1.844 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 95 | full_layerlet | 177.481 | 1.856 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | full_layerlet | 167.477 | 1.826 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 161.554 | 1.834 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
