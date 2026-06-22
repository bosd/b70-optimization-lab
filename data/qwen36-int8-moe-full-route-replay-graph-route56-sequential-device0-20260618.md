# Qwen3.6 INT8 MoE Route Replay

- Fused SiLU+quant enabled: `False`.
- TP size: `4`.
- Result rows: `1`.
- Quant out-variant available: `True`.
- Route source: `data/qwen36-quark-int8-tp4-routecapture6-routes-rank0-20260611.jsonl`.
- Route records matched: `95`; top-k rows loaded: `95`.
- Route start indices: `56`.
- Prologue-inclusive target: `160.000 us/layerlet`.
- Exactness threshold: `0.000000`.

## Exactness

- Manual staged max abs diff versus `xpu_fused_moe`: `0.000`.
- Scratch `xpu_fused_moe` max abs diff: `0.000`.
- Preallocated staged max abs diff: `0.000`.
- Fused-prologue staged max abs diff: `0.000`.
- Fused-prologue offset-GEMM max abs diff: `0.000`.
- Fused-prologue active-offset-GEMM max abs diff: `0.000`.

## Timing

- Mean `xpu_fused_moe`: `292.214 us`.
- Mean scratch `xpu_fused_moe`: `242.559 us`.
- Mean preallocated staged: `188.838 us`.
- Mean fused-prologue staged: `269.370 us`.
- Mean fused-prologue offset-GEMM staged: `185.661 us`.
- Mean fused-prologue active-offset-GEMM staged: `186.020 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 56 | 8 | 292.214 | 242.559 | 188.838 | 269.370 | 185.661 | 186.020 | 91.837 | 91.827 | 158.132 |

## Graph Replay Timing

These timings capture each preallocated candidate in an XPU graph and time `graph.replay()`. They remain single-device replay diagnostics, not endpoint throughput.

| rows | route start | candidate | status | graph us |
|---:|---:|---|---|---:|
| 1 | 56 | xpu_fused_moe_with_scratch | executed | 336.617 |
| 1 | 56 | preallocated_staged | executed | 332.764 |
| 1 | 56 | fused_prologue_staged | executed | 337.782 |
| 1 | 56 | fused_prologue_offset_gemm | executed | 340.090 |
| 1 | 56 | fused_prologue_active_offset_gemm | executed | 331.713 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `1`.
- Best exact non-reference full-layerlet candidate: `fused_prologue_offset_gemm` at `185.661 us` (`1.574x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 56 | fused_prologue_offset_gemm | 185.661 | 1.574 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
