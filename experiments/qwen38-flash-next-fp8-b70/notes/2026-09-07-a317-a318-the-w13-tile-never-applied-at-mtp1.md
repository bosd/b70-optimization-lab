# A317/A318: the W13 tile screen was vacuous, and why that is worth knowing

**What I set out to test.** The offline attribution put the W13 decode GEMM at 64% of the
modelled MoE step and found it 10.6% faster at a 16-wide N tile than at the certified 32
(69.08 against 77.30 µs per layer), bit-identical over 300 decode cases. A317 ran that tile
on the fused-QSA MTP1 identity; A318 is its control, the same driver and heads with the
certified map, because A305's rows were client-warmed and could not be compared against
driver rows.

| run | map | exact-2K r1 | r2 | hashes |
| --- | --- | --- | --- | --- |
| A317 | W13 N=16 | 25.704 | 38.823 | `afffd2110812…` |
| A318 | W13 N=32 | 26.045 | **38.894** | `afffd2110812…` |

−0.071 tok/s. **The screen proved nothing, because both runs ran the same kernel.**

**Why.** The per-phase config resolver drops phase deltas at any batch size but one:

```
M=1: W13 N=32  W2 N=64  -> delta APPLIED
M=2: W13 N=64  W2 N=64  -> delta DROPPED
M=4: W13 N=64  W2 N=64  -> delta DROPPED
```

MTP1 verifies two positions per step, so its decode graph is M=2 — the server captures
`cudagraph_capture_sizes: [1, 2]` with `num_speculative_tokens: 1`, method `mtp`. And M=2
resolves to map key 1 by nearest key (`min(keys, key=lambda x: abs(x - M))` over
{1,4,8,16,32,64}), so MTP1 decode takes key 1's *base* — N=64, warps 8 — and never the
`W1_CONFIG` delta. Both A317 and A318 therefore ran W13 at N=64.

**So the certified W13-N32 map is inert at MTP1 decode.** The published lossless MTP1 record
carries a tuned delta its decode steps never use. That is not a defect: measured at M=2, the
delta would have *hurt*.

**The tile ladder at the shape MTP1 actually runs.** Both GEMMs share one config at M=2, so
the sweep is over the shared N:

| shared N | warps | gemm1 + gemm2 per layer |
| --- | --- | --- |
| 32 | 8 | 260.0 µs |
| **64** | **8** | **200.5 µs** — what it runs today |
| 128 | 8 | 324.6 µs |
| 32 / 64 / 128 | 4 | 296.1 / 332.6 / 819.1 µs |

MTP1's MoE tiling is already at the optimum of this ladder, and W13 alone at M=2 prefers 64
(131.8 µs) over 32 (168.2) and 16 (197.7) — the reverse of the M=1 ordering. Closed, and this
time measured at the right shape rather than at M=1 and assumed to transfer.

**What survives.** The 16-wide tile is real, exact and untested where it applies: M=1, which
is MTP0 decode. The published MTP0 record is the lineage that can use it.

**On my own error.** I built A318 to remove a warmup confound and it did its job, but the
confound I did not check was whether the knob was connected at all. The isolated probe ran
M=1 because that is what "decode" means without speculation; the lineage under test speculates.
A knob's ladder should be swept at the shape the target actually runs before a server run is
spent on it — the cost here was two 25-minute loads.

## Evidence

- `data/20260907-tp4-mtp1-a317-w13n16-exact-depth-2k-r{1,2}.json` and
  `data/20260907-tp4-mtp1-a318-w13n32-control-exact-depth-2k-r{1,2}.json` — the four rows.
- `data/20260907-tp4-mtp1-a317-w13n16-tuned-map-receipt.txt` — A317 loaded the 16-wide map
  with zero `default MoE config` fallbacks, so the map was in use even though the delta was not.
- `tools/probe-moe-surround-decode-offline.py` with `Q38_PROBE_M=2` — the M=2 ladder.
- Packets: `tools/rewrite-q38-a311-to-a317-mtp1-w13-blockn16-screen.py`,
  `tools/rewrite-q38-a311-to-a318-mtp1-w13-blockn32-control.py`.
