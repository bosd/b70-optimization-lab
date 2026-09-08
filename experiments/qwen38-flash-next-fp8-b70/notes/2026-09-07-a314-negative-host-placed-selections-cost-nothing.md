# A314 (negative): removing 99.6% of host-placed expert selections buys nothing

**The hypothesis.** The expert host placement parks cold experts in pinned host memory. Its
never-hit survey was taken on the torch-fallback line, and A311/A316 showed it is stale for
the published fused-QSA line: over a real-traffic window the routing selects a parked expert
on **12.410%** of the hot rank's routed blocks, and 2.7–4.1% on the other three. If each
such selection were a PCIe read of a whole expert row, that would explain the gap between
the MoE GEMM's 566 GB/s isolated weight reads (A290-era probe) and its effective 61 GB/s in
the server.

**The test.** A314 is A306's frozen packet — the certified fused-QSA MTP1 record — with one
change: the placement file. The rebuild parks exactly as many experts in exactly the same
layers (543/587/550/586; both runs' load receipts report the same 2.49, 2.52, 2.68, 2.69 GiB
per rank), choosing them coldest-first from the lineage's own routing census. 308–353 pairs
per rank are swapped. Predicted host selections fall from 12.410% to **0.048%** on the hot
rank and to 0.10–0.13% on the others. A305 is the same client on the same configuration with
the old placement, so the comparison is like for like.

**The result: nothing moves.**

| leg | old placement (A305) | rebuilt (A314) | Δ tok/s | Δ TTFT |
| --- | --- | --- | --- | --- |
| exact-2K r1 | 38.981 | 38.932 | −0.050 | +0.006 s |
| exact-2K r2 | 38.972 | 38.945 | −0.027 | +0.003 s |
| exact-4K r1 | 39.299 | 39.274 | −0.025 | +0.022 s |
| exact-4K r2 | 39.304 | 39.320 | +0.016 | +0.007 s |

Mean −0.021 tok/s, which is inside this lane's run-to-run spread. Time to first token, where
prefill host reads would land, is unchanged to within 22 ms on a 22-second prefill.

**Exactness held, as designed.** A314 returned the lineage's authorities unchanged:
exact-2K `afffd2110812…` / `e39e32c33a7f…`, exact-4K `1d833e5f4633…`. Which memory a weight
lives in does not touch the arithmetic, and the client's pins enforced it. The quality screen
returned 6/7 with `code_execution` expecting 14 and answering 30 — the same failure, with the
same two values, as a225, a268, a271 and a305, and the state the client's gate requires.

**What this rules out.** A host-placed expert selection does not cost measurable time. The
most likely reason is that a touched page migrates to the device and stays there while the
card has headroom, so the offload's cost is a one-time migration rather than a per-selection
PCIe read — which also means the identity of the parked experts does not matter for speed,
only the total that is never touched at all. Either way, the 61 GB/s effective weight-read
rate in the server is **not** explained by host residency, and the stale-survey lever is
closed with data.

**What it leaves.** The MoE GEMM's cost is neither bandwidth (566 GB/s strided in isolation),
nor arithmetic (a GEMV of one sixteenth the FLOPs runs at the same speed), nor host reads
(this negative), nor prefetch (inert, A290), nor tile shape (four directions closed), nor
split-K (closed, 4K inexact). What remains is the dependency chain the earlier probe named:
twenty dependent K iterations per program that the machine cannot hide, on a card with one
CCS and therefore no compute/compute overlap.

**The rebuilt placement is kept but not promoted.** It is equal within noise and rests less
on driver migration, but it is not faster, and the certified record's placement stays the
published one.

## Evidence

- `data/20260907-tp4-mtp1-a314-exact-depth-{2k,4k}-r{1,2}.json` — the four rows above.
- `data/20260907-tp4-mtp1-a314-client-gates-passed.txt` — `PASS recovery quality short-repeat
  exact-2K-repeat exact-4K-repeat PLE-only 4352 MTP1 QSA-stable treatment`.
- `data/20260907-tp4-mtp1-a314-placement-load-receipt.txt` — the per-rank parked bytes.
- `data/20260907-tp4-mtp1-a314-quality-current.json`, `…-bench-short-r2.json`, `…-identity.txt`.
- Packet: `tools/rewrite-q38-a306-to-a314-mtp1-qsafused-census-placement.py`; head
  `6d872457`, the certified fused-QSA MTP1 head, unchanged.
