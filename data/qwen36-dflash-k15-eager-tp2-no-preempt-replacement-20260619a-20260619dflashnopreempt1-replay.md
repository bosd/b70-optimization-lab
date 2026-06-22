# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-dflash-k15-eager-tp2-no-preempt-replacement-20260619a-20260619dflashnopreempt1-spec-trace.jsonl`
- rows: `7`
- malformed rows: `0`
- requests: `1`
- suppressed follow-up mismatches: `0`
- suppressed schedule mismatches: `0`
- suppressed accept mismatches: `0`
- accounting mismatches: `0`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-dflash-k15-eager-tp2-no-preempt-replacement-20260619a-20260619dflashnopreempt1-000000-0-8a90976e` | 7 | 105 | 34 | 71 | 0 | `natural_latency_plan (scheduler_prefix)` | 0 | 0 | 0 | 0 |

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-dflash-k15-eager-tp2-no-preempt-replacement-20260619a-20260619dflashnopreempt1-000000-0-8a90976e` | 1 | 16 | 3 | 12 | -13 | 3 | 3 |
| `cmpl-qwen36-dflash-k15-eager-tp2-no-preempt-replacement-20260619a-20260619dflashnopreempt1-000000-0-8a90976e` | 2 | 16 | 0 | 15 | -16 | 0 | 0 |
| `cmpl-qwen36-dflash-k15-eager-tp2-no-preempt-replacement-20260619a-20260619dflashnopreempt1-000000-0-8a90976e` | 3 | 16 | 1 | 14 | -15 | 1 | 1 |
| `cmpl-qwen36-dflash-k15-eager-tp2-no-preempt-replacement-20260619a-20260619dflashnopreempt1-000000-0-8a90976e` | 4 | 16 | 8 | 7 | -8 | 8 | 8 |
| `cmpl-qwen36-dflash-k15-eager-tp2-no-preempt-replacement-20260619a-20260619dflashnopreempt1-000000-0-8a90976e` | 5 | 16 | 6 | 9 | -10 | 6 | 6 |
| `cmpl-qwen36-dflash-k15-eager-tp2-no-preempt-replacement-20260619a-20260619dflashnopreempt1-000000-0-8a90976e` | 6 | 16 | 3 | 12 | -13 | 3 | 3 |
| `cmpl-qwen36-dflash-k15-eager-tp2-no-preempt-replacement-20260619a-20260619dflashnopreempt1-000000-0-8a90976e` | 7 | 16 | 13 | 2 | -3 | 4 | 4 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
