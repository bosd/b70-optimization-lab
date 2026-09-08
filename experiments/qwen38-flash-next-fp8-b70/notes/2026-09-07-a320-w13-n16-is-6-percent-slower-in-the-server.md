# A320 (negative): the tile the probe called 10.6% faster is 6.1% slower in the server

**Prediction, written before the run** (`2026-09-07-a320-mtp0-w13-n16-prereg.md`): the
isolated probe put W13 at 69.08 µs per layer at a 16-wide N tile against 77.30 at the
certified 32, implying −0.39 ms per step and **+0.44 tok/s**, landing near 33.9.

**Result.**

| leg | A304 (N=32) | A320 (N=16) | Δ |
| --- | --- | --- | --- |
| exact-2K r1 | 33.322 | 31.385 | −1.937 |
| exact-2K r2 | 33.447 | 31.395 | −2.051 |
| exact-4K r1 | 33.471 | 31.354 | −2.116 |
| exact-4K r2 | 33.410 | 31.324 | −2.085 |

Mean **−2.047 tok/s, −6.1%**: the opposite sign, at four and a half times the predicted
magnitude, consistent across all four rows and far outside A304's own 0.125 spread.

**The knob was connected this time.** A320 loaded `moe-m1-w13-n16` with zero
`default MoE config` fallbacks, captured `cudagraph_capture_sizes: [1]` so a phase delta
resolves, and its in-run receipt returned `status pass`, key 1, W13 N=16 with W2 N=64. The
client's full gates passed. This is a measurement of the tile, not of a disconnected knob
as A317 turned out to be.

**Exactness held, as predicted.** `afffd2110812…` at exact-2K and `1d833e5f4633…` at
exact-4K, unchanged. The tile is bit-identical and simply slower.

**What this costs the offline harness.** The probe did not merely under-predict; it
inverted. A 16-wide tile doubles the number of programs and halves the work in each, which
the isolated kernel rewards and the server punishes. Isolated MoE timings have now
mispredicted this server four times — A282, A286, A317 (where the knob was not connected at
all) and here, the first with the sign reversed. **The offline tile ladder should not be
used to rank tiles for this kernel again**, in either direction; only a server screen counts.

**What it validates.** The certified W13-N32 map is better than the smaller tile by a wide
margin, so the lane's existing tuning stands, and the downward tile ladder is closed on
MTP0 as it already was on MTP1.

**What it opens.** If the offline ladder is anti-predictive here, the certified N=32 delta
itself deserves a server test against the plain N=64 base, which the offline probe ranks
15 µs per layer *worse* and which may therefore be better. `configs/moe-warps8-m1` is
exactly the certified map without the delta. A321 tests it as a delta of 64, so the map
shape, the verifier contract and the certified head all stay put.

## Evidence

- `data/20260907-tp4-mtp0-a320-w13n16-exact-depth-{2k,4k}-r{1,2}.json` — the four rows.
- `data/20260907-tp4-mtp0-a320-w13n16-moe-m1-w13-n16-selection-receipt.json` — the in-run
  receipt proving the tile was selected.
- `data/20260907-tp4-mtp0-a320-w13n16-client-gates-passed.txt` — full client gates.
- Packet: `tools/rewrite-q38-a304-to-a320-mtp0-w13-blockn16-screen.py`, head `c876369f`.
