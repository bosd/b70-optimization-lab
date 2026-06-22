# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-dflash-k15-eager-tp2-serial-gdn-sync-20260619a-20260619dflashserial1-spec-trace.jsonl`
- rows: `7`
- malformed rows: `0`
- requests: `1`
- suppressed follow-up mismatches: `0`
- suppressed schedule mismatches: `0`
- suppressed accept mismatches: `0`
- accounting mismatches: `0`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-dflash-k15-eager-tp2-serial-gdn-sync-20260619a-20260619dflashserial1-000000-0-82dee3e3` | 7 | 105 | 27 | 78 | 0 | `natural_latency_plan (scheduler_prefix)` | 0 | 0 | 0 | 0 |

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-dflash-k15-eager-tp2-serial-gdn-sync-20260619a-20260619dflashserial1-000000-0-82dee3e3` | 1 | 16 | 3 | 12 | -12 | 4 | 4 |
| `cmpl-qwen36-dflash-k15-eager-tp2-serial-gdn-sync-20260619a-20260619dflashserial1-000000-0-82dee3e3` | 2 | 16 | 14 | 1 | -1 | 15 | 15 |
| `cmpl-qwen36-dflash-k15-eager-tp2-serial-gdn-sync-20260619a-20260619dflashserial1-000000-0-82dee3e3` | 3 | 16 | 3 | 12 | -12 | 4 | 4 |
| `cmpl-qwen36-dflash-k15-eager-tp2-serial-gdn-sync-20260619a-20260619dflashserial1-000000-0-82dee3e3` | 4 | 16 | 0 | 15 | -15 | 1 | 1 |
| `cmpl-qwen36-dflash-k15-eager-tp2-serial-gdn-sync-20260619a-20260619dflashserial1-000000-0-82dee3e3` | 5 | 16 | 1 | 14 | -14 | 2 | 2 |
| `cmpl-qwen36-dflash-k15-eager-tp2-serial-gdn-sync-20260619a-20260619dflashserial1-000000-0-82dee3e3` | 6 | 16 | 1 | 14 | -14 | 2 | 2 |
| `cmpl-qwen36-dflash-k15-eager-tp2-serial-gdn-sync-20260619a-20260619dflashserial1-000000-0-82dee3e3` | 7 | 16 | 5 | 10 | -10 | 3 | 3 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
