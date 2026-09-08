# Qwen3.8 Flash-Next FP8 · no speculation · W13 tile at base width · four B70s (candidate package)

Manifest: [`package.json`](package.json). Guide:
[`repro/qwen38-flash-next-fp8-tp4-mtp0-w13n64-b70-34tps-20260908/`](../../repro/qwen38-flash-next-fp8-tp4-mtp0-w13n64-b70-34tps-20260908/README.md).

Status `candidate`: originating-host replay material with every identity pinned
and every binary hosted; no clean-host install, no container replay, and this
guide pins packets and evidence rather than shipping the record-gate replay
helpers (the MTP1 sibling carries those).

**34.495292 tok/s**, class-balanced median of prompt-class medians over the fixed
cold realistic suite, no speculation — LocalMaxxing run
[`cmts8zca50032ps01e0ddqm18`](https://www.localmaxxing.com/runs/cmts8zca50032ps01e0ddqm18).
This is the lab's fastest non-speculative Flash-Next line. It supersedes the
33.797067 tok/s package identity (`cmtrmp37v001bps01a7fi46nf`), which is retained.

## What this package is, in one paragraph

It is the previous MTP0 record with **one line of a tuned configuration file
changed and nothing else**: the per-phase MoE map's `W1_CONFIG.BLOCK_SIZE_N`
goes from 32 to 64, which makes the W13 phase tile equal to the base tile so the
delta stops doing anything. There is no source change — 64 was already an allowed
tile — so the certified overlay head `2a372e86` runs unmodified. The delta had
been adopted bundled with an unrelated eight-warp change and never isolated; when
it finally was, it cost 2.1%.

Two cold suites (34.510128 and 34.495292 on a fresh server) with every row above
every row of the superseded suite, and six exact-2K plus six exact-4K rows across
three servers all carrying the certified stream's hashes, so the change is
lossless as well as faster.

## What it does not carry

- No container route. The MTP1 sibling's recipe stops at its runtime check on a
  torch 2.13 vs 2.11 ABI mismatch, and that blocker applies here unchanged, so
  copying it would add a file without adding a route. See the guide's
  `CONTAINER-STATUS.md`.
- No record-gate replay scripts of its own.
- The `missing` list in `package.json` is the full accounting.

## Do not apply this to MTP1

The same change is a **regression** on the speculative line: −0.066 tok/s across
four rows. A per-phase delta resolves only at batch size 1; MTP1 verifies two
positions and decodes at batch 2, where the delta is dropped regardless, so the
only path it still reaches is the separately captured draft head — and that
prefers 32. The MTP1 package keeps its tile.
