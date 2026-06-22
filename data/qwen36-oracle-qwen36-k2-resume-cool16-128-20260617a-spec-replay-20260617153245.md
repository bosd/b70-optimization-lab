# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-oracle-k2-resume-cool16-20260617a-spec.jsonl`
- rows: `8`
- malformed rows: `0`
- requests: `2`
- suppressed follow-up mismatches: `0`
- suppressed schedule mismatches: `0`
- suppressed accept mismatches: `0`
- accounting mismatches: `0`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-cool16-000000-0-a7c35b0c` | 6 | 12 | 11 | 1 | 0 | `natural_latency_plan (scheduler_prefix)` | 0 | 0 | 0 | 0 |
| `cmpl-qwen36-cool16-000001-0-9ff4d77c` | 2 | 4 | 3 | 1 | 0 | `repetitive_kernel_notes (scheduler_prefix)` | 0 | 0 | 0 | 0 |

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-cool16-000000-0-a7c35b0c` | 1 | 3 | 2 | 0 | 0 | 3 | 3 |
| `cmpl-qwen36-cool16-000000-0-a7c35b0c` | 2 | 3 | 2 | 0 | 0 | 3 | 3 |
| `cmpl-qwen36-cool16-000000-0-a7c35b0c` | 3 | 3 | 2 | 0 | 0 | 3 | 3 |
| `cmpl-qwen36-cool16-000000-0-a7c35b0c` | 4 | 3 | 2 | 0 | 0 | 3 | 3 |
| `cmpl-qwen36-cool16-000000-0-a7c35b0c` | 5 | 3 | 2 | 0 | 0 | 3 | 3 |
| `cmpl-qwen36-cool16-000000-0-a7c35b0c` | 6 | 3 | 1 | 1 | -3 | 0 | 0 |
| `cmpl-qwen36-cool16-000001-0-9ff4d77c` | 7 | 3 | 2 | 0 | 0 | 3 | 3 |
| `cmpl-qwen36-cool16-000001-0-9ff4d77c` | 8 | 3 | 1 | 1 | -3 | 0 | 0 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
