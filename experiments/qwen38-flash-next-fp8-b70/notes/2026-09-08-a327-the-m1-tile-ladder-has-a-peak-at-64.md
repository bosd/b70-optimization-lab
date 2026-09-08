# A327: the M=1 tile ladder peaks at 64, and the offline probe is unreliable rather than inverted

**Result.** The W13 phase tile at 128 costs 7.86 tok/s against the promoted 64 — a 23%
regression, all four rows, hashes unmoved, full client gates passed.

| W13 BLOCK_N | 16 (A320) | 32 (A304, old certified) | **64 (A321/A322/A323, promoted)** | 128 (A327) |
| --- | --- | --- | --- | --- |
| exact-2K r1 / r2 | 31.385 / 31.395 | 33.322 / 33.447 | **34.127 / 34.170** | 26.281 / 26.295 |
| exact-4K r1 / r2 | 31.354 / 31.324 | 33.471 / 33.410 | **34.096 / 34.034** | 26.203 / 26.202 |

**The ladder is measured end to end now**, in the server, on the lineage that actually
resolves the tile: it rises 16 → 32 → 64 and falls off a cliff at 128. The promoted
configuration sits on the peak.

**The hypothesis that motivated this run was wrong.** After 16 lost and 64 won I read the
server's preference as monotone in tile width, opposite to the offline ladder, and 128 was
the obvious test of that. It is not monotone; there is an optimum, and 64 is it.

**And the correction matters more than the run.** I recorded after A320 that the offline
probe is "anti-predictive" for MoE tiles. A327 shows that is too strong: the probe ranked 128
worst of all four, and the server agrees emphatically. The probe got the 16/32/64 ordering
backwards and the 128 cliff right. So it is **unreliable in both directions**, not reliably
inverted — which forbids using it to rank tiles either way, but does not license reading it
upside down. The memory note is corrected accordingly.

**What is now closed.** The W13 M=1 tile ladder, at every power of two `tl.dot` accepts, on
the promoted lineage. Combined with A317/A318 (the delta is inert at MTP1's M=2) and the M=2
sweep (64 already optimal there), the MoE tile question is closed in both directions on both
lineages, and no further tile screen is worth a run.

## Evidence

- `data/20260908-tp4-mtp0-a327-w13n128-exact-depth-{2k,4k}-r{1,2}.json` — the four rows.
- `data/20260908-tp4-mtp0-a327-w13n128-moe-m1-w13-n128-selection-receipt.json` — `status pass`,
  W13 N=128, W2 N=64, so the tile was genuinely selected.
- `data/20260908-tp4-mtp0-a327-w13n128-client-gates-passed.txt`.
- Packet: `tools/rewrite-q38-a304-to-a327-mtp0-w13-blockn128-screen.py`, head `2a372e86`.
