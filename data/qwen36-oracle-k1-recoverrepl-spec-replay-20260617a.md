# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-oracle-k1-recoverrepl-20260617a-spec.jsonl`
- rows: `15`
- malformed rows: `0`
- requests: `2`
- suppressed follow-up mismatches: `0`
- suppressed schedule mismatches: `0`
- suppressed accept mismatches: `0`
- accounting mismatches: `1`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-recoverrepl20260617a-000000-0-ade6efc0` | 9 | 9 | 8 | 1 | 0 | `natural_latency_plan (scheduler_prefix)` | 0 | 0 | 0 | 1 |
| `cmpl-recoverrepl20260617a-000001-0-93ca264d` | 6 | 6 | 6 | 0 | 0 | `repetitive_kernel_notes (scheduler_prefix)` | 0 | 0 | 0 | 0 |

## Accounting Mismatches

- request `cmpl-recoverrepl20260617a-000000-0-ade6efc0` line `9`: expected computed delta `-1` from rejected `1` plus suppressed `0`, observed `-2`.

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-recoverrepl20260617a-000000-0-ade6efc0` | 1 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-recoverrepl20260617a-000000-0-ade6efc0` | 2 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-recoverrepl20260617a-000000-0-ade6efc0` | 3 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-recoverrepl20260617a-000000-0-ade6efc0` | 4 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-recoverrepl20260617a-000000-0-ade6efc0` | 5 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-recoverrepl20260617a-000000-0-ade6efc0` | 6 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-recoverrepl20260617a-000000-0-ade6efc0` | 7 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-recoverrepl20260617a-000000-0-ade6efc0` | 8 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-recoverrepl20260617a-000000-0-ade6efc0` | 9 | 2 | 0 | 1 | -2 | 0 | 0 |
| `cmpl-recoverrepl20260617a-000001-0-93ca264d` | 10 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-recoverrepl20260617a-000001-0-93ca264d` | 11 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-recoverrepl20260617a-000001-0-93ca264d` | 12 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-recoverrepl20260617a-000001-0-93ca264d` | 13 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-recoverrepl20260617a-000001-0-93ca264d` | 14 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-recoverrepl20260617a-000001-0-93ca264d` | 15 | 2 | 1 | 0 | 0 | 2 | 2 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
