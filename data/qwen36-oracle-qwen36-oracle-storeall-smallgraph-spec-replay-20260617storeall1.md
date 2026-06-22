# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-oracle-k1-storeall-smallgraph-20260617a-spec.jsonl`
- rows: `19`
- malformed rows: `0`
- requests: `2`
- suppressed follow-up mismatches: `0`
- suppressed schedule mismatches: `0`
- suppressed accept mismatches: `0`
- accounting mismatches: `0`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-storeall20260617a-000001-0-a9f172f9` | 10 | 10 | 9 | 1 | 0 | `repetitive_kernel_notes (scheduler_prefix)` | 0 | 0 | 0 | 0 |
| `cmpl-storeall20260617a-000000-0-a5a3c50b` | 9 | 9 | 8 | 1 | 0 | `natural_latency_plan (scheduler_prefix)` | 0 | 0 | 0 | 0 |

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-storeall20260617a-000001-0-a9f172f9` | 10 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-storeall20260617a-000001-0-a9f172f9` | 11 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-storeall20260617a-000001-0-a9f172f9` | 12 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-storeall20260617a-000001-0-a9f172f9` | 13 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-storeall20260617a-000001-0-a9f172f9` | 14 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-storeall20260617a-000001-0-a9f172f9` | 15 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-storeall20260617a-000001-0-a9f172f9` | 16 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-storeall20260617a-000001-0-a9f172f9` | 17 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-storeall20260617a-000001-0-a9f172f9` | 18 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-storeall20260617a-000001-0-a9f172f9` | 19 | 2 | 0 | 1 | -1 | 1 | 1 |
| `cmpl-storeall20260617a-000000-0-a5a3c50b` | 1 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-storeall20260617a-000000-0-a5a3c50b` | 2 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-storeall20260617a-000000-0-a5a3c50b` | 3 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-storeall20260617a-000000-0-a5a3c50b` | 4 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-storeall20260617a-000000-0-a5a3c50b` | 5 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-storeall20260617a-000000-0-a5a3c50b` | 6 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-storeall20260617a-000000-0-a5a3c50b` | 7 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-storeall20260617a-000000-0-a5a3c50b` | 8 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-storeall20260617a-000000-0-a5a3c50b` | 9 | 2 | 0 | 1 | -1 | 1 | 1 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
