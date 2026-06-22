# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-oracle-k1-think-bonus-force-single-20260618h-spec-trace.jsonl`
- rows: `16`
- malformed rows: `0`
- requests: `1`
- suppressed follow-up mismatches: `0`
- suppressed schedule mismatches: `0`
- suppressed accept mismatches: `0`
- accounting mismatches: `0`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k1-think-bonus-force-single-20260618h-000000-0-bef21031` | 16 | 16 | 15 | 1 | 15 | `natural_latency_plan (scheduler_prefix)` | 0 | 0 | 0 | 0 |

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k1-think-bonus-force-single-20260618h-000000-0-bef21031` | 1 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-think-bonus-force-single-20260618h-000000-0-bef21031` | 2 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-think-bonus-force-single-20260618h-000000-0-bef21031` | 3 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-think-bonus-force-single-20260618h-000000-0-bef21031` | 4 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-think-bonus-force-single-20260618h-000000-0-bef21031` | 5 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-think-bonus-force-single-20260618h-000000-0-bef21031` | 6 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-think-bonus-force-single-20260618h-000000-0-bef21031` | 7 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-think-bonus-force-single-20260618h-000000-0-bef21031` | 8 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-think-bonus-force-single-20260618h-000000-0-bef21031` | 9 | 2 | 0 | 1 | -2 | 0 | 0 |
| `cmpl-qwen36-oracle-k1-think-bonus-force-single-20260618h-000000-0-bef21031` | 10 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-think-bonus-force-single-20260618h-000000-0-bef21031` | 11 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-think-bonus-force-single-20260618h-000000-0-bef21031` | 12 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-think-bonus-force-single-20260618h-000000-0-bef21031` | 13 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-think-bonus-force-single-20260618h-000000-0-bef21031` | 14 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-think-bonus-force-single-20260618h-000000-0-bef21031` | 15 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-think-bonus-force-single-20260618h-000000-0-bef21031` | 16 | 2 | 1 | 0 | -1 | 1 | 1 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
