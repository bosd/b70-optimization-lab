# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-dflash-k15-eager-tp2-replay-think-statetrace-20260619a-20260619dflashstatetrace1-spec-trace.jsonl`
- rows: `4`
- malformed rows: `0`
- requests: `1`
- suppressed follow-up mismatches: `0`
- suppressed schedule mismatches: `0`
- suppressed accept mismatches: `0`
- accounting mismatches: `1`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-dflash-k15-eager-tp2-replay-think-statetrace-20260619a-20260619dflashstatetrace1-000000-0-94afc954` | 4 | 60 | 29 | 31 | 0 | `natural_latency_plan (scheduler_prefix)` | 0 | 0 | 0 | 1 |

## Accounting Mismatches

- request `cmpl-qwen36-dflash-k15-eager-tp2-replay-think-statetrace-20260619a-20260619dflashstatetrace1-000000-0-94afc954` line `3`: expected computed delta `-12` from rejected `12` plus suppressed `0`, observed `-16`.

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-dflash-k15-eager-tp2-replay-think-statetrace-20260619a-20260619dflashstatetrace1-000000-0-94afc954` | 1 | 16 | 3 | 12 | -12 | 4 | 4 |
| `cmpl-qwen36-dflash-k15-eager-tp2-replay-think-statetrace-20260619a-20260619dflashstatetrace1-000000-0-94afc954` | 2 | 16 | 14 | 1 | -1 | 15 | 15 |
| `cmpl-qwen36-dflash-k15-eager-tp2-replay-think-statetrace-20260619a-20260619dflashstatetrace1-000000-0-94afc954` | 3 | 16 | 3 | 12 | -16 | 0 | 0 |
| `cmpl-qwen36-dflash-k15-eager-tp2-replay-think-statetrace-20260619a-20260619dflashstatetrace1-000000-0-94afc954` | 4 | 16 | 9 | 6 | -6 | 5 | 5 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
