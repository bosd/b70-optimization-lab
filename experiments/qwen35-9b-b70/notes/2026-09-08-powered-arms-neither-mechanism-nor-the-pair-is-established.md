# Four powered arms: a monotone trend, nothing established, and a cost figure that was wrong by 65 points

All four arms are 20 passes at 64 concurrent users, 1280 requests each, one image carrying both
overlays so only the knobs vary, and each container's environment checked for the knobs it was
supposed to have before the arm was read.

| arm | intervention | divergent / 1280 | two-sided p vs control | tok/s | vs control |
| --- | --- | ---: | ---: | ---: | ---: |
| `p0` | none (control) | 9 | - | `2088.1` | - |
| `p1` | serialised norm | 7 | `0.80` | `2088.7` | `+0.0%` |
| `q1` | row-wise all-reduce | 6 | `0.61` | `726.8` | **`-65.2%`** |
| `q2` | both | 3 | `0.15` | `724.6` | **`-65.3%`** |

## The cost figure that was published and is wrong

The row-wise all-reduce was written up on 2026-09-07 as costing "about `-0.25%`" at 64 users. That
number came from an arm where the knob never reached the container, so it was the control measured
twice. Applied, it costs **`-65.2%`** at this rung: `726.8` against `2088.1 tok/s`.

That changes what the intervention is. A 65% throughput loss is not a fix that could ship even if it
worked perfectly, which reframes it as a diagnostic for locating the cause rather than a candidate
repair - and reinforces that anything real here has to be an invariant kernel, not a serialisation.

The serialised norm's cost figure is unaffected and stands at zero: its knob was verified present
before that arm was read, and twenty passes put it at `+0.0%`.

## What the identity numbers do and do not say

The trend is monotone and in the direction the mechanism predicts - 9, 7, 6, 3 as each shape
dependence is removed and then both - which is what one would expect if each alone leaves the other
free to perturb a near-tie. It is also exactly what noise looks like at these counts.

None of the arms is significant. The pair comes closest at `p = 0.15` two-sided, which is not a
result. With 9 control events, an arm that genuinely removed the divergence would have to show close
to zero to be convincing, and 3 is not close enough to separate from chance.

So: **not established, either individually or jointly**. Settling the pair would need roughly three to
four times the events - on the order of 60 to 80 passes per arm rather than 20 - and at a 65%
throughput cost that is about four hours of cards for a result whose best case is confirming a
diagnosis rather than delivering a fix.

## What is worth doing instead

The pair being the largest reduction is a reason to keep the hypothesis, not to keep testing it this
way. Two cheaper routes to the same question:

1. Instrument rather than infer. Both mechanisms are known shape-dependent from direct probes; the
   open question is which one perturbs the specific rows that flip. Capturing the divergent requests'
   logits and checking whether the margin at the flipped token is within the norm's or the
   collective's perturbation scale would answer it without a throughput-costed ladder.
2. Widen the metric. At roughly 0.7% of requests, 64 users is a slow way to accumulate events.
   Running the same total request count at a higher concurrency, or over longer completions, gathers
   the same statistics faster.

Evidence: `data/2026-09-08-serialnorm-identity-power.json`,
`data/2026-09-08-identity-power-q1.json`, `data/2026-09-08-identity-power-q2.json`.
