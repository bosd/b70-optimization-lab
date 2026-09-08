# The lossless-MTP1 record is confirmed, and its suite spread is now measured

A328 replayed the certified MTP1 packet and came back 0.54% low, with the shortfall in the
first two rows of a cold run. One pair cannot tell a lineage's spread from a real shift, so
A329 replayed it again. Same packet, same overlay `6d872457`, same certified
`moe-m1-w13-n32` map, nothing changed but attempt and port.

| run | class-balanced median |
| --- | --- |
| A306 (published) | 37.825654 |
| A328 (replay) | 37.622275 |
| **A329 (replay)** | **37.946213** |

Mean 37.798047, range **0.323938 (0.86%)**, sd 0.134. The published value sits +0.028 from
the mean of the three — as close to the centre as a single sample gets.

**So A328 was not drift.** It was the low end of ordinary variation, and A329 is the high
end, above the published number. The record is confirmed rather than merely "close".

**Where the variation lives.** Not in the suite as a whole:

| | A306 | A328 | A329 | spread |
| --- | --- | --- | --- | --- |
| row 0 (first, cold) | 25.9583 | 25.4099 | 25.9934 | 0.584 |
| row 1 | 37.9697 | 36.4162 | 37.6649 | **1.554** |
| rows 2–11, \|A329−A306\| | — | — | — | max 0.306, mean 0.064 |

The warm rows agree to a mean of 0.064 tok/s. Rows 0 and 1 carry essentially all of it, and
A329's log shows why: Triton is still JIT-compiling kernels (`layer_norm`) during the first
prompt. Whatever cache state a cold run starts with decides those two rows.

**The rule this gives.** MTP1 suite-to-suite spread is about ±0.16 around 37.80 (0.86%
peak-to-peak on three runs). MTP0's two suites tonight agreed to 0.015 (0.04%) — roughly
twenty times tighter, which fits: speculation acceptance varies run to run and a
non-speculative line has no such term. So **a single MTP1 suite cannot support a claim
smaller than about ±0.3 tok/s**, while MTP0 can resolve far less. Any future MTP1 change
needs repeats before it is called a win or a regression.

This does not touch tonight's MTP0 promotion, which cleared its control by 0.70 tok/s on
four independent runs against a 0.125 control spread.

## Evidence

- `data/20260908-tp4-mtp1-a329-record-replay2-realistic-suite-v1-result.json` and
  `…-a328-record-replay-realistic-suite-v1-result.json` — the two replays, twelve rows each.
- `data/20260907-tp4-mtp1-a306-qsafused-realistic-suite-v1-result.json` — the published run.
- Packets: `tools/rewrite-q38-a306-to-a32{8,9}-mtp1-suite-replay*.py`, pure replays.
