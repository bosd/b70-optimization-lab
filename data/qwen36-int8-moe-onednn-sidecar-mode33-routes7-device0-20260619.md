# Qwen3.6 INT8 MoE Route Replay

- Fused SiLU+quant enabled: `False`.
- TP size: `4`.
- Result rows: `7`.
- Route mode/source: `route_jsonl`.
- Quant out-variant available: `True`.
- Route source: `/home/steve/llm-optimizations/data/qwen36-quark-int8-tp4-routecapture6-routes-rank0-20260611.jsonl`.
- Route records matched: `285`; top-k rows loaded: `285`.
- Route start indices: `0,40,80,85,95,100,115`.
- Prologue-inclusive target: `160.000 us/layerlet`.
- Exactness threshold: `0.000000`.

## Exactness

- Manual staged max abs diff versus `xpu_fused_moe`: `0.000`.
- Scratch `xpu_fused_moe` max abs diff: `0.000`.
- Prologue-scratch `xpu_fused_moe` max abs diff: `0.000`.
- Preallocated staged max abs diff: `0.000`.
- Fused-prologue staged max abs diff: `0.000`.
- Fused-prologue offset-GEMM max abs diff: `0.000`.
- Full C++ layerlet max abs diff: `0.000`.
- oneDNN sidecar max abs diff: `0.000`.

### Rows-Oracle Checks

- Current `xpu_fused_moe` max abs diff versus forced rows-per-expert oracle: `0.000`.
- Forced offset-GEMM max abs diff versus rows-per-expert oracle: `0.000`.
- Full C++ layerlet max abs diff versus rows-per-expert oracle: `0.000`.
- oneDNN sidecar max abs diff versus rows-per-expert oracle: `0.000`.

## Timing

- Mean `xpu_fused_moe`: `316.523 us`.
- Mean scratch `xpu_fused_moe`: `261.151 us`.
- Mean prologue-scratch `xpu_fused_moe`: `262.195 us`.
- Mean preallocated staged: `203.490 us`.
- Mean fused-prologue staged: `276.052 us`.
- Mean fused-prologue offset-GEMM staged: `201.381 us`.
- Mean full C++ layerlet: `167.962 us`.
- Mean oneDNN sidecar total: `310.244 us`.
- Mean oneDNN sidecar internal middle wall: `46.752 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | xpu prologue scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | oneDNN sidecar us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 302.972 | 253.505 | 251.759 | 195.495 | 267.156 | 194.211 | n/a | n/a | 162.220 | 299.754 | 93.296 | 93.389 | 160.048 |
| 1 | 40 | 8 | 318.282 | 264.231 | 265.420 | 206.146 | 277.893 | 202.195 | n/a | n/a | 169.638 | 314.424 | 95.671 | 96.007 | 166.971 |
| 1 | 80 | 8 | 310.452 | 253.939 | 257.508 | 198.444 | 270.026 | 199.424 | n/a | n/a | 165.208 | 303.525 | 92.989 | 92.162 | 161.902 |
| 1 | 85 | 8 | 312.353 | 257.380 | 258.670 | 201.096 | 273.410 | 198.245 | n/a | n/a | 166.131 | 305.757 | 93.855 | 93.949 | 163.248 |
| 1 | 95 | 8 | 313.357 | 257.233 | 257.358 | 200.393 | 271.594 | 198.225 | n/a | n/a | 165.821 | 306.969 | 94.193 | 93.632 | 163.364 |
| 1 | 100 | 8 | 331.137 | 270.731 | 272.366 | 211.087 | 286.083 | 208.750 | n/a | n/a | 174.218 | 321.389 | 98.612 | 100.069 | 172.234 |
| 1 | 115 | 8 | 327.109 | 271.035 | 272.284 | 211.771 | 286.201 | 208.616 | n/a | n/a | 172.498 | 319.890 | 97.390 | 97.056 | 169.934 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `7`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `162.220 us` (`1.868x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 162.220 | 1.868 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | full_layerlet | 169.638 | 1.876 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 165.208 | 1.879 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | full_layerlet | 166.131 | 1.880 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 95 | full_layerlet | 165.821 | 1.890 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | full_layerlet | 174.218 | 1.901 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 172.498 | 1.896 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
