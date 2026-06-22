# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-oracle-k1-staleguard-serialconv-smallgraph-20260617a-spec.jsonl`
- rows: `31`
- malformed rows: `0`
- requests: `2`
- suppressed follow-up mismatches: `0`
- suppressed schedule mismatches: `0`
- suppressed accept mismatches: `0`
- accounting mismatches: `0`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-staleguard-serialconv-a-000001-0-94e0d25b` | 16 | 16 | 16 | 0 | 0 | `repetitive_kernel_notes (scheduler_prefix)` | 0 | 0 | 0 | 0 |
| `cmpl-staleguard-serialconv-a-000000-0-ae50d7c4` | 15 | 15 | 14 | 1 | 0 | `natural_latency_plan (scheduler_prefix)` | 0 | 0 | 0 | 0 |

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-staleguard-serialconv-a-000001-0-94e0d25b` | 16 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-staleguard-serialconv-a-000001-0-94e0d25b` | 17 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-staleguard-serialconv-a-000001-0-94e0d25b` | 18 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-staleguard-serialconv-a-000001-0-94e0d25b` | 19 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-staleguard-serialconv-a-000001-0-94e0d25b` | 20 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-staleguard-serialconv-a-000001-0-94e0d25b` | 21 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-staleguard-serialconv-a-000001-0-94e0d25b` | 22 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-staleguard-serialconv-a-000001-0-94e0d25b` | 23 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-staleguard-serialconv-a-000001-0-94e0d25b` | 24 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-staleguard-serialconv-a-000001-0-94e0d25b` | 25 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-staleguard-serialconv-a-000001-0-94e0d25b` | 26 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-staleguard-serialconv-a-000001-0-94e0d25b` | 27 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-staleguard-serialconv-a-000001-0-94e0d25b` | 28 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-staleguard-serialconv-a-000001-0-94e0d25b` | 29 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-staleguard-serialconv-a-000001-0-94e0d25b` | 30 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-staleguard-serialconv-a-000001-0-94e0d25b` | 31 | 2 | 1 | 0 | 0 | 1 | 1 |
| `cmpl-staleguard-serialconv-a-000000-0-ae50d7c4` | 1 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-staleguard-serialconv-a-000000-0-ae50d7c4` | 2 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-staleguard-serialconv-a-000000-0-ae50d7c4` | 3 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-staleguard-serialconv-a-000000-0-ae50d7c4` | 4 | 2 | 1 | 0 | 0 | 2 | 2 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
