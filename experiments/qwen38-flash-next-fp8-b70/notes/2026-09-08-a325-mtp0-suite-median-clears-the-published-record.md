# A325: the MTP0 suite median clears the published record by 2.1%

**Result.** The fixed cold realistic suite on the W13-N64 configuration, run through the same
suite driver that produced the published figure:

| | A301 (published, W13 N=32) | A325 (W13 N=64) |
| --- | --- | --- |
| class-balanced median | **33.797067** | **34.510128** |
| raw median of 12 rows | 33.812881 | 34.514663 |
| row range | 33.7022 – 33.8938 | 34.4334 – 34.5905 |
| cached_tokens all zero | yes | yes |

**+0.713061 tok/s, +2.11%**, and the distributions do not overlap: A325's slowest row
(34.4334) is above A301's fastest (33.8938). Twelve fresh rows each.

**Consistent with the exact-depth evidence.** A321, A322 and A323 measured +0.695, +0.728
and about +0.71 on exact rows across three separate servers, all bit-identical. The suite now
agrees at +0.713 on its own metric. Four runs, one direction, no overlap with the control at
any point.

**What the change is.** One line of the tuned map: `W1_CONFIG.BLOCK_SIZE_N` 32 → 64, which
makes the W13 phase delta equal to the base tile and therefore inert. No source change — 64
was already an allowed tile — so the certified head `2a372e86` runs unmodified. The published
configuration becomes strictly simpler.

**Not yet promoted.** A326 is the fresh-server suite repeat. The lane does not move a record
on one suite run, and until that lands the claim is "one suite run at 34.510128, four
consistent measurements", not a record.

**Publication surface, once it clears.** The MTP0 figure is not a repro guide — all four
guides are MTP1 — it lives in `results/qwen38-flash-next-fp8-b70/README.md` (the suite table
row), `families/qwen-flash-next.json` (`run_measurements` promotion status), a promotion
attestation, and a LocalMaxxing payload modelled on A301's.

## Evidence

- `data/20260908-tp4-mtp0-a325-w13n64-realistic-suite-v1-result.json` — twelve rows.
- `data/20260908-tp4-mtp0-a325-w13n64-identity.txt`.
- Packet: `tools/rewrite-q38-a301-to-a325-mtp0-w13-blockn64-suite.py`, head `2a372e86`,
  map `configs/moe-m1-w13-n64/`.
