# Qwen3.6 INT8 MoE Route Replay

- Fused SiLU+quant enabled: `False`.
- TP size: `4`.
- Result rows: `1`.
- Quant out-variant available: `True`.
- Route source: `/home/steve/llm-optimizations/data/qwen36-quark-int8-tp4-routecapture6-routes-rank0-20260611.jsonl`.
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

- Mean `xpu_fused_moe`: `296.194 us`.
- Mean scratch `xpu_fused_moe`: `247.225 us`.
- Mean preallocated staged: `192.844 us`.
- Mean fused-prologue staged: `260.622 us`.
- Mean fused-prologue offset-GEMM staged: `189.493 us`.
- Mean fused-prologue active-offset-GEMM staged: `191.377 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 56 | 8 | 296.194 | 247.225 | 192.844 | 260.622 | 189.493 | 191.377 | 90.478 | 91.102 | 159.675 |

## Prologue Offset Stage Timing

These stage timings are for the exact fused-prologue offset-GEMM candidate and are used to decide the next native layerlet boundary. They are single-device replay diagnostics.

| rows | route start | total us | prologue | quant1 | gemm1 | activation | quant2 | gemm2 | gather | component sum |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 56 | 189.493 | 99.863 | 77.238 | 90.839 | 74.162 | 75.312 | 90.779 | 74.682 | 582.876 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `1`.
- Best exact non-reference full-layerlet candidate: `fused_prologue_offset_gemm` at `189.493 us` (`1.563x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 56 | fused_prologue_offset_gemm | 189.493 | 1.563 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
