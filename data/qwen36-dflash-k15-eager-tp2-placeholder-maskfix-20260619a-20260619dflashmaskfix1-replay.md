# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-dflash-k15-eager-tp2-placeholder-maskfix-20260619a-20260619dflashmaskfix1-spec-trace.jsonl`
- rows: `6`
- malformed rows: `0`
- requests: `1`
- suppressed follow-up mismatches: `0`
- suppressed schedule mismatches: `0`
- suppressed accept mismatches: `0`
- accounting mismatches: `0`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-dflash-k15-eager-tp2-placeholder-maskfix-20260619a-20260619dflashmaskfix1-000000-0-85dc4c39` | 6 | 90 | 35 | 55 | 0 | `natural_latency_plan (scheduler_prefix)` | 0 | 0 | 0 | 0 |

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-dflash-k15-eager-tp2-placeholder-maskfix-20260619a-20260619dflashmaskfix1-000000-0-85dc4c39` | 1 | 16 | 3 | 12 | -12 | 4 | 4 |
| `cmpl-qwen36-dflash-k15-eager-tp2-placeholder-maskfix-20260619a-20260619dflashmaskfix1-000000-0-85dc4c39` | 2 | 16 | 14 | 1 | -1 | 15 | 15 |
| `cmpl-qwen36-dflash-k15-eager-tp2-placeholder-maskfix-20260619a-20260619dflashmaskfix1-000000-0-85dc4c39` | 3 | 16 | 3 | 12 | -12 | 4 | 4 |
| `cmpl-qwen36-dflash-k15-eager-tp2-placeholder-maskfix-20260619a-20260619dflashmaskfix1-000000-0-85dc4c39` | 4 | 16 | 0 | 15 | -15 | 1 | 1 |
| `cmpl-qwen36-dflash-k15-eager-tp2-placeholder-maskfix-20260619a-20260619dflashmaskfix1-000000-0-85dc4c39` | 5 | 16 | 0 | 15 | -15 | 1 | 1 |
| `cmpl-qwen36-dflash-k15-eager-tp2-placeholder-maskfix-20260619a-20260619dflashmaskfix1-000000-0-85dc4c39` | 6 | 16 | 15 | 0 | 0 | 6 | 6 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
