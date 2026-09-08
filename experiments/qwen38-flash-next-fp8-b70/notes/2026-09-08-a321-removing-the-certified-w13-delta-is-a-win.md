# A321: removing the certified W13 delta is worth +0.695 tok/s on MTP0

**Result.** Setting `W1_CONFIG.BLOCK_SIZE_N` to 64 — the same tile as the base, so the phase
delta stops doing anything — is faster than the certified 32 on every row, bit-identical,
with the full client's gates green.

| leg | A304 (N=32, certified) | A321 (N=64) | Δ |
| --- | --- | --- | --- |
| exact-2K r1 | 33.322 | 34.127 | +0.805 |
| exact-2K r2 | 33.447 | 34.170 | +0.723 |
| exact-4K r1 | 33.471 | 34.096 | +0.625 |
| exact-4K r2 | 33.410 | 34.034 | +0.625 |

Mean **+0.695 tok/s, +2.1%**, every row positive and every row outside A304's own 0.125
spread. Hashes unmoved: `afffd2110812…` at exact-2K, `1d833e5f4633…` at exact-4K. Gates:
`PASS recovery quality short-repeat exact-2K-repeat exact-4K-repeat`. The in-run receipt
returned `status pass`, key 1, W13 N=64, W2 N=64, with zero `default MoE config` fallbacks
and `cudagraph_capture_sizes: [1]`, so the delta genuinely resolved and was genuinely neutral.

**Against the prereg** (`2026-09-07-a321-mtp0-w13-n64-prereg.md`): the offline ladder
predicted −0.8 and got the sign wrong; the inversion hypothesis predicted +1 to +2 and got
the sign right while over-predicting the size; the ±0.5 noise band is cleared by every row.
So the inversion is directionally real and quantitatively unreliable — which is the same
verdict the ladder now carries, and the reason both are screened in the server.

**How the delta came to be certified.** A56 adopted it on 2026-09-02 as half of a composite:
"(eight-warp M1 and W13-N32) therefore compose into a real endpoint gain", moving 19.07 to
23.63 tok/s. The two changes were never separated. My sweeps put the warp count at 20–35% on
its own, so that composite's gain is consistent with the eight-warp change alone, with the
tile riding along untested. The lineage has also changed underneath it since — Triton-HC and
the fused QSA indexer both landed after — so even a then-valid isolation need not hold now.

I am not claiming A56 was wrong about its endpoint; it measured a real gain and gated it
properly. The claim is narrower: one component of it was never isolated, and that component
is now measured, in the server, as a cost.

**What this is worth.** It is a lossless speed win on a published record obtained by
*removing* a tuning: the resulting configuration is strictly simpler than what is published,
the map differs from the certified one by a single line, and there is no source change at all
— 64 is already an allowed tile, so A321 runs the certified head `2a372e86` unmodified.

**What it does not yet establish.** One run. The lane's standard is a deterministic repeat
and a fresh-server pair before a record moves, and the published MTP0 figure is a
realistic-suite number, not an exact-depth row, so the suite has to be run on this
configuration before any record is restated. A322 is the fresh-server repeat.

## Evidence

- `data/20260908-tp4-mtp0-a321-w13n64-exact-depth-{2k,4k}-r{1,2}.json` — the four rows.
- `data/20260908-tp4-mtp0-a321-w13n64-moe-m1-w13-n64-selection-receipt.json` — the in-run receipt.
- `data/20260908-tp4-mtp0-a321-w13n64-client-gates-passed.txt`, `…-quality-current.json`,
  `…-bench-short-r2.json`, `…-identity.txt`.
- `configs/moe-m1-w13-n64/` — one line different from the certified map.
- Packet: `tools/rewrite-q38-a304-to-a321-mtp0-w13-blockn64-screen.py`, head `2a372e86`.
