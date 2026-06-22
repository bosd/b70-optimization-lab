# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-oracle-k1-recomputeverifier-smallgraph-20260617a-spec.jsonl`
- rows: `2`
- malformed rows: `0`
- requests: `2`
- suppressed follow-up mismatches: `0`
- suppressed schedule mismatches: `0`
- suppressed accept mismatches: `0`
- accounting mismatches: `2`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-recompverifsmall20260617a-000000-0-8e541dac` | 1 | 1 | 1 | 0 | 1 | `natural_latency_plan (scheduler_prefix)` | 0 | 0 | 0 | 1 |
| `cmpl-recompverifsmall20260617a-000001-0-a473cd70` | 1 | 1 | 1 | 0 | 1 | `repetitive_kernel_notes (scheduler_prefix)` | 0 | 0 | 0 | 1 |

## Accounting Mismatches

- request `cmpl-recompverifsmall20260617a-000000-0-8e541dac` line `1`: expected computed delta `-1` from rejected `0` plus suppressed `1`, observed `-2`.
- request `cmpl-recompverifsmall20260617a-000001-0-a473cd70` line `2`: expected computed delta `-1` from rejected `0` plus suppressed `1`, observed `-2`.

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-recompverifsmall20260617a-000000-0-8e541dac` | 1 | 2 | 1 | 0 | -2 | 0 | 0 |
| `cmpl-recompverifsmall20260617a-000001-0-a473cd70` | 2 | 2 | 1 | 0 | -2 | 0 | 0 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
