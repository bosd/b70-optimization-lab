# A324 (negative): the MTP0 win does not transfer to MTP1

**Result.** The same one-line change that is worth +0.70 tok/s on MTP0 — `W1_CONFIG.BLOCK_SIZE_N`
32 → 64, neutralising the W13 phase delta — is slightly *negative* on MTP1.

| leg | A305 (N=32, certified) | A324 (N=64) | Δ |
| --- | --- | --- | --- |
| exact-2K r1 | 38.981 | 38.905 | −0.076 |
| exact-2K r2 | 38.972 | 38.907 | −0.065 |
| exact-4K r1 | 39.299 | 39.223 | −0.076 |
| exact-4K r2 | 39.304 | 39.256 | −0.048 |

Mean **−0.066 tok/s**, all four rows negative. A305's two exact-2K rows differ by 0.009, so
this is about seven times the control's own spread: small, but consistent rather than noise.
Hashes unmoved (`afffd2110812…`, `1d833e5f4633…`) and the client's full gates passed, so this
is a speed result on an unchanged stream.

**Why the two lineages disagree.** A phase delta resolves only at M=1. MTP0 decodes at M=1,
so on MTP0 the tile choice *is* the decode tile, and the server prefers 64. MTP1 verifies two
positions, so its decode graph is M=2 and takes the base tile whatever the delta says; the
only thing the delta still reaches is the M=1 path, which under speculation belongs to the
draft head — captured separately, one token per step. That path evidently prefers 32.

So the change is not a general improvement to the MoE map. It is specific to what runs at
M=1, and the two lineages run different things there.

**Decision: MTP1 keeps the certified W13-N32 delta.** The MTP0 promotion stands on its own
evidence and does not generalise. Nothing about the published MTP1 record changes.

**What this costs the tidy story.** "Removing the delta is better" would have been a cleaner
claim, and it is not the one the data supports. The accurate claim is narrower: on the
lineage whose decode batch is 1, the delta is a pessimisation; on the lineage whose decode
batch is 2, it is worth a little and costs nothing to keep.

## Evidence

- `data/20260908-tp4-mtp1-a324-w13n64-exact-depth-{2k,4k}-r{1,2}.json` — the four rows.
- `data/20260908-tp4-mtp1-a324-w13n64-client-gates-passed.txt`.
- Packet: `tools/rewrite-q38-a305-to-a324-mtp1-w13-blockn64-screen.py`, head `6d872457`,
  map `configs/moe-m1-w13-n64/`.
