# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-oracle-k1-initfirst-20260617a-spec.jsonl`
- rows: `6`
- malformed rows: `0`
- requests: `2`
- suppressed follow-up mismatches: `0`
- suppressed schedule mismatches: `0`
- suppressed accept mismatches: `0`
- accounting mismatches: `0`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-initfirst20260617a-000000-0-88659ca7` | 4 | 4 | 3 | 1 | 0 | `natural_latency_plan (scheduler_prefix)` | 0 | 0 | 0 | 0 |
| `cmpl-initfirst20260617a-000001-0-92fa674b` | 2 | 2 | 1 | 1 | 0 | `repetitive_kernel_notes (scheduler_prefix)` | 0 | 0 | 0 | 0 |

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-initfirst20260617a-000000-0-88659ca7` | 1 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-initfirst20260617a-000000-0-88659ca7` | 2 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-initfirst20260617a-000000-0-88659ca7` | 3 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-initfirst20260617a-000000-0-88659ca7` | 4 | 2 | 0 | 1 | -1 | 1 | 1 |
| `cmpl-initfirst20260617a-000001-0-92fa674b` | 5 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-initfirst20260617a-000001-0-92fa674b` | 6 | 2 | 0 | 1 | -1 | 1 | 1 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
