# Qwen3.6 INT8 MoE Route Replay

- Fused SiLU+quant enabled: `False`.
- TP size: `4`.
- Result rows: `7`.
- Route mode/source: `route_jsonl`.
- Quant out-variant available: `True`.
- Route source: `/home/steve/llm-optimizations/data/qwen36-quark-int8-tp4-firstdecode-route-fixture-routes-20260612ct.jsonl`.
- Route records matched: `120`; top-k rows loaded: `120`.
- Route start indices: `0,40,80,85,95,100,115`.
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

- Mean `xpu_fused_moe`: `363.768 us`.
- Mean scratch `xpu_fused_moe`: `291.155 us`.
- Mean preallocated staged: `224.015 us`.
- Mean fused-prologue staged: `310.824 us`.
- Mean fused-prologue offset-GEMM staged: `224.844 us`.
- Mean fused-prologue active-offset-GEMM staged: `232.807 us`.
- Mean fused-prologue middle-layerlet staged: `198.937 us`.
- Mean full C++ layerlet: `190.527 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 362.341 | 292.172 | 227.131 | 321.495 | 228.535 | 238.566 | 228.868 | 194.771 | 105.877 | 109.730 | 197.595 |
| 1 | 40 | 8 | 308.870 | 246.480 | 194.215 | 270.785 | 193.799 | 201.313 | 171.844 | 168.969 | 94.198 | 93.418 | 176.909 |
| 1 | 80 | 8 | 341.208 | 275.522 | 209.669 | 290.893 | 217.157 | 219.050 | 180.830 | 179.691 | 106.257 | 100.272 | 176.706 |
| 1 | 85 | 8 | 367.047 | 304.091 | 229.429 | 314.985 | 225.092 | 232.570 | 195.021 | 191.589 | 112.284 | 109.751 | 194.392 |
| 1 | 95 | 8 | 387.962 | 314.673 | 243.942 | 323.206 | 236.059 | 245.492 | 210.798 | 200.715 | 116.511 | 113.204 | 199.924 |
| 1 | 100 | 8 | 388.502 | 302.640 | 231.275 | 322.717 | 234.130 | 236.408 | 199.638 | 197.532 | 111.228 | 112.627 | 204.521 |
| 1 | 115 | 8 | 390.447 | 302.505 | 232.445 | 331.687 | 239.132 | 256.251 | 205.561 | 200.418 | 112.637 | 112.195 | 195.593 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `7`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `168.969 us` (`1.828x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 194.771 | 1.860 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | full_layerlet | 168.969 | 1.828 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 179.691 | 1.899 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | full_layerlet | 191.589 | 1.916 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 95 | full_layerlet | 200.715 | 1.933 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | full_layerlet | 197.532 | 1.967 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 200.418 | 1.948 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
