# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-oracle-k2-resume-cool4-20260617a-spec.jsonl`
- rows: `12`
- malformed rows: `0`
- requests: `2`
- suppressed follow-up mismatches: `0`
- suppressed schedule mismatches: `0`
- suppressed accept mismatches: `0`
- accounting mismatches: `0`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-cool4-000000-0-a14d3ad0` | 8 | 16 | 14 | 2 | 0 | `natural_latency_plan (scheduler_prefix)` | 0 | 0 | 0 | 0 |
| `cmpl-qwen36-cool4-000001-0-a8371609` | 4 | 8 | 7 | 1 | 0 | `repetitive_kernel_notes (scheduler_prefix)` | 0 | 0 | 0 | 0 |

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-cool4-000000-0-a14d3ad0` | 1 | 3 | 2 | 0 | 0 | 3 | 3 |
| `cmpl-qwen36-cool4-000000-0-a14d3ad0` | 2 | 3 | 2 | 0 | 0 | 3 | 3 |
| `cmpl-qwen36-cool4-000000-0-a14d3ad0` | 3 | 3 | 2 | 0 | 0 | 3 | 3 |
| `cmpl-qwen36-cool4-000000-0-a14d3ad0` | 4 | 3 | 2 | 0 | 0 | 3 | 3 |
| `cmpl-qwen36-cool4-000000-0-a14d3ad0` | 5 | 3 | 2 | 0 | 0 | 3 | 3 |
| `cmpl-qwen36-cool4-000000-0-a14d3ad0` | 6 | 3 | 1 | 1 | -3 | 0 | 0 |
| `cmpl-qwen36-cool4-000000-0-a14d3ad0` | 7 | 3 | 2 | 0 | 0 | 3 | 3 |
| `cmpl-qwen36-cool4-000000-0-a14d3ad0` | 8 | 3 | 1 | 1 | -3 | 0 | 0 |
| `cmpl-qwen36-cool4-000001-0-a8371609` | 9 | 3 | 2 | 0 | 0 | 3 | 3 |
| `cmpl-qwen36-cool4-000001-0-a8371609` | 10 | 3 | 1 | 1 | -3 | 0 | 0 |
| `cmpl-qwen36-cool4-000001-0-a8371609` | 11 | 3 | 2 | 0 | 0 | 3 | 3 |
| `cmpl-qwen36-cool4-000001-0-a8371609` | 12 | 3 | 2 | 0 | 0 | 3 | 3 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
