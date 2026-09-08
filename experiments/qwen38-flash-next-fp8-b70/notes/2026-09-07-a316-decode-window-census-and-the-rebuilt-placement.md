# A316: a real-traffic routing census, and the placement rebuilt from it

**What the certified placement actually costs.** Differenced over a real-traffic window —
the two exact-2K rows plus a 4,096-token generation from a 128-token prompt — the routing
selects a host-placed expert far more often than the startup census suggested:

| rank | host selections | of routed | rebuilt placement | parked experts | host bytes |
| --- | --- | --- | --- | --- | --- |
| 0 | 289,848 | **12.410%** | 1,124 (**0.048%**) | 543 | 2.49 GiB |
| 1 | 29,938 | 2.920% | 1,306 (0.127%) | 587 | 2.69 GiB |
| 2 | 25,980 | 2.651% | 1,008 (0.103%) | 550 | 2.52 GiB |
| 3 | 41,344 | 4.140% | 1,310 (0.131%) | 586 | 2.68 GiB |

Every one of those selections is a PCIe read of a whole expert row on a card that is
otherwise reading weights from VRAM.

**The rebuild changes nothing but the choice.** `--match-compare-shape` parks exactly as
many experts in exactly the same layers as the certified placement — 543/587/550/586, the
same host bytes, the same VRAM — and picks them coldest-first by this lineage's own counts.
Between 308 and 353 pairs per rank are swapped; the rest were already cold. Which memory a
weight lives in does not touch the arithmetic, so A314 must return the lineage's exact-2K
and exact-4K hashes unchanged, and its client pins them.

**Two failures on the way, both worth recording.**

*The snapshot signal was stolen.* The census dump answers SIGUSR1 so a window can be
bracketed, and the handler was installed at import. By the time the driver signalled, a
later import held SIGUSR1: the workers caught the signal and did nothing. The driver
reported "signalled 4 workers" twice, wrote no snapshots, and the run looked healthy
throughout — a diagnostic failing silently while reporting success. The hook now re-claims
the signal whenever it notices something else holds it, checked once per 64 eager launches.

*The run was salvaged rather than repeated.* The periodic dump counts Python-side launches,
and prefill runs eagerly while captured decode does not. So 29 tiny prefill requests drove
the counter past its next threshold and produced the "after" census, at the cost of about
25 minutes not spent reloading the model. The window is therefore ~50% prefill by routed
blocks rather than decode-only. That makes the parked set **more** conservative, not less:
a pair parked here was selected by neither the prefill nor the decode traffic in the window.

**What this does not yet show.** Whether removing the host reads is worth measurable
tok/s. A314 is the single-variable screen against the certified A306 record; if the hot
rank's 12.4% collapses to 0.05% and the suite does not move, that is a clean negative
ruling PCIe reads out of the gap between the MoE GEMM's 566 GB/s isolated weight reads and
its effective 61 GB/s in the server.

## Evidence

- `data/20260907-q38-expert-host-placement-fusedqsa-census-3p5gib-per-rank.json` — the
  rebuilt placement, and `…-census-build-log.txt` the numbers above as the builder printed
  them.
- `data/20260907-tp4-mtp1-a316-census-{before,after,window}-rank{0..3}.json` — the bracketing
  snapshots and their difference.
- `data/20260907-tp4-mtp1-a316-census-window-request.json` — the census generation: 128
  prompt tokens, 4,096 generated, 37.27 tok/s, decode 97.0% of that request's routed blocks.
- `data/20260907-tp4-mtp1-a316-exact-depth-2k-r{1,2}.json` — both rows returned the
  fused-QSA lineage hashes `afffd2110812…` / `e39e32c33a7f…`, so the census does not move
  the stream.
- Packet: `tools/rewrite-q38-a311-to-a316-mtp1-placement-census-window.py`, head `248cd315`;
  the re-arming fix is `9f2ee51a`.
