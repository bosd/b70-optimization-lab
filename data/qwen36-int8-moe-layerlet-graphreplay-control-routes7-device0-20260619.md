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

- Mean `xpu_fused_moe`: `305.529 us`.
- Mean scratch `xpu_fused_moe`: `253.961 us`.
- Mean preallocated staged: `199.216 us`.
- Mean fused-prologue staged: `269.891 us`.
- Mean full C++ layerlet: `166.066 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 296.510 | 245.940 | 195.580 | 263.478 | n/a | n/a | n/a | 163.709 | 95.984 | 95.765 | 171.773 |
| 1 | 40 | 8 | 311.608 | 260.809 | 203.893 | 276.667 | n/a | n/a | n/a | 170.123 | 100.096 | 100.572 | 177.865 |
| 1 | 80 | 8 | 300.263 | 247.999 | 195.922 | 264.919 | n/a | n/a | n/a | 164.201 | 96.983 | 98.248 | 171.425 |
| 1 | 85 | 8 | 295.166 | 244.810 | 193.138 | 261.289 | n/a | n/a | n/a | 161.504 | 95.133 | 96.147 | 170.934 |
| 1 | 95 | 8 | 314.237 | 259.918 | 202.519 | 276.116 | n/a | n/a | n/a | 167.763 | 96.926 | 98.690 | 169.827 |
| 1 | 100 | 8 | 308.801 | 258.444 | 200.281 | 272.813 | n/a | n/a | n/a | 167.834 | 95.731 | 97.741 | 166.436 |
| 1 | 115 | 8 | 312.116 | 259.808 | 203.176 | 273.956 | n/a | n/a | n/a | 167.326 | 95.701 | 96.299 | 168.245 |

## Graph Replay Timing

These timings capture each eligible candidate in an XPU graph and time `graph.replay()`. They remain single-device replay diagnostics, not endpoint throughput.

| rows | route start | candidate | status | graph us |
|---:|---:|---|---|---:|
| 1 | 0 | xpu_fused_moe_with_scratch | executed | 328.297 |
| 1 | 0 | preallocated_staged | executed | 339.351 |
| 1 | 0 | fused_prologue_staged | executed | 345.182 |
| 1 | 0 | full_layerlet | executed | 181.851 |
| 1 | 40 | xpu_fused_moe_with_scratch | executed | 327.783 |
| 1 | 40 | preallocated_staged | executed | 255.367 |
| 1 | 40 | fused_prologue_staged | executed | 184.089 |
| 1 | 40 | full_layerlet | executed | 195.768 |
| 1 | 80 | xpu_fused_moe_with_scratch | executed | 302.451 |
| 1 | 80 | preallocated_staged | executed | 175.170 |
| 1 | 80 | fused_prologue_staged | executed | 187.364 |
| 1 | 80 | full_layerlet | executed | 179.414 |
| 1 | 85 | xpu_fused_moe_with_scratch | executed | 260.714 |
| 1 | 85 | preallocated_staged | executed | 174.771 |
| 1 | 85 | fused_prologue_staged | executed | 182.904 |
| 1 | 85 | full_layerlet | executed | 179.286 |
| 1 | 95 | xpu_fused_moe_with_scratch | executed | 325.349 |
| 1 | 95 | preallocated_staged | executed | 336.333 |
| 1 | 95 | fused_prologue_staged | executed | 339.865 |
| 1 | 95 | full_layerlet | executed | 186.839 |
| 1 | 100 | xpu_fused_moe_with_scratch | executed | 329.410 |
| 1 | 100 | preallocated_staged | executed | 297.201 |
| 1 | 100 | fused_prologue_staged | executed | 184.087 |
| 1 | 100 | full_layerlet | executed | 181.281 |
| 1 | 115 | xpu_fused_moe_with_scratch | executed | 323.005 |
| 1 | 115 | preallocated_staged | executed | 198.150 |
| 1 | 115 | fused_prologue_staged | executed | 181.938 |
| 1 | 115 | full_layerlet | executed | 177.510 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `7`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `161.504 us` (`1.828x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 163.709 | 1.811 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | full_layerlet | 170.123 | 1.832 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 164.201 | 1.829 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | full_layerlet | 161.504 | 1.828 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 95 | full_layerlet | 167.763 | 1.873 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | full_layerlet | 167.834 | 1.840 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 167.326 | 1.865 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
