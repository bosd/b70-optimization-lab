# A323: a third confirmation of the W13 win, and a latent defect in A301's client

**What A323 was for.** To produce the realistic-suite median on the W13-N64 configuration, so
the published MTP0 figure (33.797067) could be compared like for like. It did not get that
far, and the reason is worth recording.

**What it produced.** Every leg ran — bench-short, the quality screen, both exact-2K rows,
both exact-4K rows, the recovery canary — and the exact rows are a third independent
confirmation of the delta removal:

| leg | A304 (N=32) | A321 | A322 | A323 |
| --- | --- | --- | --- | --- |
| exact-2K r1 / r2 | 33.322 / 33.447 | 34.127 / 34.170 | 34.193 / 34.165 | 34.167 / 34.150 |
| exact-4K r1 / r2 | 33.471 / 33.410 | 34.096 / 34.034 | 34.105 / 34.098 | 34.089 / 34.110 |

Three runs, twelve rows, all above every A304 row, hashes `afffd2110812…` and
`1d833e5f4633…` throughout.

**Why it aborted.** The client's final verification asserts

```
depth4k_hashes == ['c6193cc6c9a1553f56d7ce78faea9c8bfa628a67fcea229b1c99279a149f6639'] * 2
```

which is the **torch-fallback** exact-4K authority. This lineage runs Triton-HC and the fused
QSA indexer and produces `1d833e5f4633…`, which is exactly what A323 produced and what A304's
client correctly pins. So the assertion is wrong for the packet it lives in.

**Why nobody had hit it.** A301 never ran its own client. Its run directory contains
`realistic-suite-v1-result.json` and nothing else — it was driven by the suite driver, which
skips the client entirely. The pin has therefore sat unexercised since A301 was generated,
and any future run of that client on its own lineage will fail the same way.

I am not changing A301's client. It is a frozen packet behind a published figure, editing it
would invalidate its own hashes, and its suite leg — the part that produced the number — is
unaffected. This note is the record so the next person to reach for that client knows.

**My own error.** I derived A323 from A301 and then ran the *client*, when the published
number came from the *suite driver*. Deriving the packet was right; choosing the leg was not.
A325 repeats it with the suite driver.

## Evidence

- `data/20260908-tp4-mtp0-a323-w13n64-third-exact-depth-{2k,4k}-r{1,2}.json` — the four rows.
- `data/20260908-tp4-mtp0-a323-w13n64-third-moe-m1-w13-n64-selection-receipt.json`.
- `data/20260908-tp4-mtp0-a323-stale-4k-pin-abort.log` — the abort.
- Packet: `tools/rewrite-q38-a301-to-a323-mtp0-w13-blockn64-suite.py`, head `2a372e86`.
