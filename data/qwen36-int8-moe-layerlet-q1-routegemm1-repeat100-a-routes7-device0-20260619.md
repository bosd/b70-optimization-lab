# Qwen3.6 INT8 MoE Route Replay

- Fused SiLU+quant enabled: `False`.
- TP size: `4`.
- Result rows: `7`.
- Route mode/source: `route_jsonl`.
- Quant out-variant available: `True`.
- Route source: `data/qwen36-quark-int8-tp4-routecapture6-routes-rank0-20260611.jsonl`.
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

- Mean `xpu_fused_moe`: `309.619 us`.
- Mean scratch `xpu_fused_moe`: `256.447 us`.
- Mean preallocated staged: `201.338 us`.
- Mean fused-prologue staged: `271.546 us`.
- Mean full C++ layerlet: `168.391 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 339.204 | 280.776 | 222.280 | 299.017 | n/a | n/a | n/a | 187.160 | 103.161 | 104.392 | 181.473 |
| 1 | 40 | 8 | 333.648 | 273.536 | 214.298 | 289.598 | n/a | n/a | n/a | 182.406 | 100.122 | 100.382 | 181.789 |
| 1 | 80 | 8 | 292.152 | 243.670 | 190.350 | 257.091 | n/a | n/a | n/a | 158.959 | 89.724 | 91.090 | 158.473 |
| 1 | 85 | 8 | 292.180 | 243.071 | 189.523 | 256.540 | n/a | n/a | n/a | 158.398 | 89.305 | 90.748 | 157.727 |
| 1 | 95 | 8 | 290.939 | 242.490 | 189.502 | 256.053 | n/a | n/a | n/a | 158.042 | 89.331 | 90.908 | 159.291 |
| 1 | 100 | 8 | 304.081 | 252.310 | 198.870 | 267.180 | n/a | n/a | n/a | 164.461 | 92.244 | 94.143 | 162.990 |
| 1 | 115 | 8 | 315.126 | 259.280 | 204.541 | 275.343 | n/a | n/a | n/a | 169.314 | 94.269 | 94.111 | 165.497 |

## Prologue-Inclusive Gate

- Gate status: `some_rows_have_exact_nonreference_layerlet_candidate`.
- Rows ready for endpoint gate: `3` / `7`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `158.042 us` (`1.841x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 187.160 | 1.812 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | full_layerlet | 182.406 | 1.829 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 158.959 | 1.838 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 85 | full_layerlet | 158.398 | 1.845 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 95 | full_layerlet | 158.042 | 1.841 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 100 | full_layerlet | 164.461 | 1.849 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 169.314 | 1.861 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
