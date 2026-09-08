# A336: the guide's replay script works, and a caution about how I quoted spread

The MTP0 package listed "record-gate replay scripts" as missing. `run-record-replay.sh` now
derives a packet, verifies the identity pins, proves the packet regenerates identically,
checks the attempt rename actually took, and launches. A336 is its end-to-end test.

**It works.** Its first act was to refuse: the overlay head was still on `005dc578` from the
Laguna work, and it stopped with the checkout command rather than running the wrong lineage.
After checking out `2a372e86` it derived, validated and launched, and the resulting run
carries the record's identity exactly — 64-wide map, zero `default MoE config` fallbacks,
`cudagraph_capture_sizes: [1]`.

**Result: 34.477514**, inside the 34.47–34.55 band the script prints as its own acceptance
criterion.

## The caution

A336 is the lowest of the four suites, so the range widens:

| | suites | range | sd |
| --- | --- | --- | --- |
| MTP0 W13-N64, first three | 34.4953 / 34.5101 / 34.5201 | 0.0248 | 0.0102 |
| MTP0 W13-N64, all four | + 34.4775 | **0.0426** | 0.0161 |

I have quoted the MTP0 spread three times tonight and it has grown each time — 0.015 from two
suites, 0.025 from three, 0.043 from four. That is not the lineage getting noisier. **Range is
a biased estimator that grows with sample count**, so quoting it without the n attached
invites exactly the comparison I made: an MTP0 range from a growing sample against MTP1 ranges
fixed at three.

The like-for-like comparison, three per arm, is unchanged and is the one to cite:

| lineage | 3-suite range | 3-suite sd |
| --- | --- | --- |
| MTP0 W13-N64 | 0.0248 | 0.0102 |
| MTP1 fused-QSA | 0.3239 | 0.1337 |
| MTP1 Triton-HC | 0.3802 | 0.1649 |

So "MTP0 is 13–15x tighter" stands **as a three-against-three statement**, and I should have
said so when I first wrote it. Standard deviation is the better quantity to quote across
unequal samples: 0.016 against 0.134 and 0.165, about a factor of nine, and that one does not
drift as n grows.

## Nothing about the record changes

Mean of four suites 34.500757, against the submitted headline of 34.495292 — which remains the
lowest of the first three and conservative. The promotion margin against the superseded line
is +0.7016 on means and +0.6763 worst case, still an order of magnitude above the spread by
any of these measures.

## Evidence

- `data/20260908-tp4-mtp0-a336-script-driven-replay-realistic-suite-v1-result.json`
- `repro/qwen38-flash-next-fp8-tp4-mtp0-w13n64-b70-34tps-20260908/run-record-replay.sh`
- Supersedes the spread figures quoted in `…-a333-the-promoted-mtp0-record-with-error-bars.md`
  and `…-a334-the-mtp0-promotion-as-distribution-against-distribution.md`, which remain correct
  as three-sample statements.
