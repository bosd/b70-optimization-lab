# A315: the routing census, and why a census needs a window

**What A315 did.** It repeated A311's census on the graph-safe head `cc653214`, with the
histogram widened to every routed expert rather than only the parked ones. Graph capture
finished in 43 s — the stage where A313 aborted — so the `scatter_add_` form is sound. Both
exact-2K rows returned the fused-QSA lineage's own hashes, `afffd2110812…` /
`e39e32c33a7f…`, so the census counts without moving the stream.

**The counts.**

| rank | routed selections | experts selected ≥ once | never selected | parked | parked and hit |
| --- | --- | --- | --- | --- | --- |
| 0 | 1,794,890 | 5,324 / 6,144 | 820 | 543 | 235 (314,174 selections, 17.50%) |
| 1 | 217,136 | 5,283 / 6,144 | 861 | 587 | 227 (2,188, 1.01%) |
| 2 | 217,244 | 5,234 / 6,144 | 910 | 550 | 201 (2,308, 1.06%) |
| 3 | 209,130 | 5,246 / 6,144 | 898 | 586 | 251 (2,322, 1.11%) |

Rank 0 is the rank whose local experts the router prefers: 8.6x the routed blocks of the
others, and the 17.5% figure A311 measured belongs to it. The hit rates reproduce A311's
to four decimal places, so the measurement is stable.

**Why this census cannot choose the placement.** Every dump landed at 21:26:44, before
either generation. The counters are device tensors and do accumulate during graph replay,
but the Python in the hook runs only when a launch is traced, and under full decode capture
that means prefill. So the one dump per rank covers the startup profiling run — rank 0's
1.79M selections are dummy-input routing — and almost none of the traffic anyone cares
about. Parking experts on that evidence would be worse than the survey it was meant to
replace, which at least came from real decode-sized top-k dumps.

This is worth stating plainly because the numbers look authoritative and are not: a census
without a defined window measures whatever the process happened to do, weighted by whatever
dominated the launch count.

**The fix.** The dump now also answers SIGUSR1. A signal handler runs in the worker's main
thread between bytecodes — never inside capture, never inside a replay — so it can read the
counters back and write a numbered snapshot on demand. Differencing two snapshots taken
around a generation gives that generation's routing, on the certified graph-captured
configuration rather than the eager one the original top-k dump required (A197 ran
`--enforce-eager` for exactly this reason).

A316 uses it, with a short prompt and a long generation: a snapshot window counts every
routed block in it, and a 2,048-token prefill routes as many blocks as 2,048 decode steps.
The placement only has to avoid the experts the decode window selects — the original survey
filtered to decode-sized routing the same way — so the census request keeps the fixture's
content, takes a 128-token slice of it, and generates 4,096 tokens past it.

**One thing the census already settles.** Each rank has 820–910 (layer, expert) pairs this
lineage never selected, against 543–587 currently parked. Even allowing that a decode-window
census will find fewer cold pairs, there is room to park the same number of experts as the
certified placement does. The corrected placement can therefore keep the record's host bytes
and VRAM exactly, and change only which experts are parked.

## Evidence

- `data/20260907-tp4-mtp1-a315-routing-census-rank{0..3}.json` — the per-rank census.
- `data/20260907-tp4-mtp1-a315-placement-hit-census.log` — the census log lines.
- `data/20260907-tp4-mtp1-a315-exact-depth-2k-r{1,2}.json` — the exact-2K pair.
- Packet: `tools/rewrite-q38-a311-to-a315-mtp1-placement-routing-census.py`; head `cc653214`.
