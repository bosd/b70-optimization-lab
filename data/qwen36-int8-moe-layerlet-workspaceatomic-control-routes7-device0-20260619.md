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

- Mean `xpu_fused_moe`: `309.955 us`.
- Mean scratch `xpu_fused_moe`: `257.277 us`.
- Mean preallocated staged: `201.572 us`.
- Mean fused-prologue staged: `272.554 us`.
- Mean full C++ layerlet: `166.446 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 327.292 | 272.135 | 213.181 | 287.723 | n/a | n/a | n/a | 175.779 | 98.693 | 98.515 | 174.609 |
| 1 | 40 | 8 | 306.574 | 255.401 | 199.849 | 269.777 | n/a | n/a | n/a | 164.355 | 95.622 | 94.365 | 164.263 |
| 1 | 80 | 8 | 300.285 | 250.106 | 194.999 | 264.773 | n/a | n/a | n/a | 161.697 | 92.682 | 93.657 | 163.562 |
| 1 | 85 | 8 | 303.113 | 251.900 | 198.021 | 265.516 | n/a | n/a | n/a | 162.563 | 92.990 | 92.883 | 165.018 |
| 1 | 95 | 8 | 309.145 | 256.214 | 202.052 | 273.194 | n/a | n/a | n/a | 166.258 | 94.481 | 94.212 | 165.948 |
| 1 | 100 | 8 | 314.229 | 259.644 | 203.793 | 274.933 | n/a | n/a | n/a | 168.426 | 94.839 | 94.827 | 166.979 |
| 1 | 115 | 8 | 309.047 | 255.536 | 199.106 | 271.961 | n/a | n/a | n/a | 166.044 | 93.527 | 94.643 | 165.409 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `7`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `161.697 us` (`1.857x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 175.779 | 1.862 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | full_layerlet | 164.355 | 1.865 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 161.697 | 1.857 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | full_layerlet | 162.563 | 1.865 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 95 | full_layerlet | 166.258 | 1.859 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | full_layerlet | 168.426 | 1.866 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 166.044 | 1.861 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
