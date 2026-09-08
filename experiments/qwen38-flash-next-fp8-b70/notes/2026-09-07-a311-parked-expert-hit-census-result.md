# A311: the expert host placement's never-hit survey is stale on the fused-QSA line

**Result.** Parked experts are selected. On the fused-QSA MTP1 lineage, with the
2026-09-06 placement loaded unchanged, the routing selects a host-placed expert on
1.0–1.1% of routed blocks on three ranks and **17.5% on the rank holding the hot
experts**. Every such selection is a PCIe read of a whole expert row.

| rank | host-placed selections | routed blocks | share |
| --- | --- | --- | --- |
| — | 2,322 | 209,130 | 1.110% |
| — | 314,174 | 1,794,890 | **17.504%** |
| — | 2,308 | 217,244 | 1.062% |
| — | 2,188 | 217,136 | 1.008% |

Counts are cumulative over the run at 4,800 MoE GEMM launches per rank, so they include
the 2,048-token prefill as well as the measured decode window; the rank with 8.6x the
routed blocks of the others is the one whose local experts the router prefers. Rank
identity is not recoverable from the log line, which prints no rank; the census now
writes a per-rank file instead.

**Why it matters.** The placement was built from a top-k dump taken on the torch-fallback
line and parks (layer, expert) pairs that dump never selected. The Triton-HC and fused-QSA
restorations changed the generated stream, so the trajectory visits different experts, and
a pair that was never hit then is hit now. This is a plausible contributor to the
unexplained gap between the MoE GEMM's isolated weight-read bandwidth (566 GB/s strided,
A290-era probe) and its effective 61 GB/s in the server: a fraction of reads are not
reading VRAM at all.

**What it does not show.** The census cannot say how much of the 15.1 ms MoE step the host
reads cost, only that they happen. A rate from this run is not a speed measurement — the
hook adds a device-side gather and bincount per launch. A311 measured 25.30 and 37.10
tok/s on its two exact-2K rows against 38.97 certified, which is the hook's cost plus
ordinary first-row warmup, not a regression.

**Identity held.** A311's exact-2K output hash `afffd2110812…` and text hash
`e39e32c33a7f…` match the fused-QSA lineage exactly, so the census hook does not move the
stream; it only counts.

**Next.** A313 measures the full per-expert routing histogram for this lineage (every
routed expert, not only the parked ones) and
`tools/build-q38-expert-host-placement-from-census.py` rebuilds the placement from it,
parking the pairs this lineage never selects, under the same 3.5 GiB-per-rank budget.
Choosing which weights live in which memory does not touch the arithmetic, so a corrected
placement is an exact lever: if it is faster it can be certified on the published lineage
without changing a single output token.

## Evidence

- `data/20260907-tp4-mtp1-a311-placement-hit-census.log` — the four census lines above.
- `data/20260907-tp4-mtp1-a311-identity.txt` — the run's identity block.
- `data/20260907-tp4-mtp1-a311-census-exact-depth-2k-r{1,2}.json` — the exact-2K pair.
- Packet: `tools/rewrite-q38-a120-to-a311-mtp1-placement-hit-census.py` and the four
  frozen scripts it emits; overlay head `795a9dd94c16` (`q38-placement-hit-census`).
