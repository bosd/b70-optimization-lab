# A328: the certified lossless-MTP1 record still replays on this host

After the MiniMax re-check found a published guide that could no longer run, the same
question was put to this lane's own records: does the certified MTP1 suite number still
reproduce today? A328 is A306's packet with nothing changed but the attempt number and port
— same overlay `6d872457`, same certified `moe-m1-w13-n32` map, same suite driver.

**Class-balanced median: 37.622275 against the published 37.825654** — −0.203 tok/s, −0.54%.

**The row detail is what matters.**

| row | A306 | A328 | Δ |
| --- | --- | --- | --- |
| 0 (first of a cold run) | 25.9583 | 25.4099 | −0.5485 |
| 1 | 37.9697 | 36.4162 | **−1.5536** |
| 7 | 35.4222 | 35.2113 | −0.2109 |
| 2–6, 8–11 (nine rows) | — | — | within ±0.09 |

Nine of the twelve rows reproduce to better than 0.09 tok/s, and six of those are *faster*
on the replay. The shortfall is concentrated in the first two prompts of a cold run, which
is where warm-up and thermal state land, not spread across the suite as a regression would
be. `cached_tokens` is zero on every row of both.

**Reading.** The record reproduces. A 0.54% class-balanced difference driven by two early
rows is not evidence that 37.825654 was wrong, and it is not a new record either — it is one
cold replay, and the honest summary is "reproduces within about half a percent, with the
deviation in the cold rows".

It does say something useful about precision: tonight's two MTP0 suites agreed to 0.015
(0.04%), so MTP1's suite-to-suite spread is much wider than MTP0's. That is consistent with
speculation — acceptance varies run to run in a way a non-speculative line cannot — and it
means MTP1 record comparisons need more than one suite to separate a real change from cold-row
noise. The MTP0 promotion earlier tonight cleared its control by an order of magnitude more
than this, on four independent runs, so it is unaffected by this observation.

**Contrast with MiniMax.** The MiniMax M2.7 guide could not be run at all: its runtime has
been advanced past the record's stack. This lane's record runs, on its own frozen packet,
two weeks later. That is the difference between a lane whose runtime is pinned by frozen
packets and one whose venv is shared.

## Evidence

- `data/20260908-tp4-mtp1-a328-record-replay-realistic-suite-v1-result.json` — twelve rows.
- `data/20260908-tp4-mtp1-a328-record-replay-identity.txt`.
- Packet: `tools/rewrite-q38-a306-to-a328-mtp1-suite-replay.py`, head `6d872457`, map
  `moe-m1-w13-n32` — a pure replay, nothing changed but attempt and port.
