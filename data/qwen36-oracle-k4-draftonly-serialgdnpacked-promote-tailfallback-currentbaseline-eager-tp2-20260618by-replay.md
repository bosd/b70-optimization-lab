# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-oracle-k4-draftonly-serialgdnpacked-promote-tailfallback-currentbaseline-eager-tp2-20260618by-spec-trace.jsonl`
- rows: `7`
- malformed rows: `0`
- requests: `1`
- suppressed follow-up mismatches: `0`
- suppressed schedule mismatches: `0`
- suppressed accept mismatches: `0`
- accounting mismatches: `7`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k4-draftonly-serialgdnpacked-promote-tailfallback-currentbaseline-eager-tp2-20260618by-000000-0-9c23d12c` | 7 | 28 | 28 | 0 | 0 | `natural_latency_plan (scheduler_prefix)` | 0 | 0 | 0 | 7 |

## Accounting Mismatches

- request `cmpl-qwen36-oracle-k4-draftonly-serialgdnpacked-promote-tailfallback-currentbaseline-eager-tp2-20260618by-000000-0-9c23d12c` line `1`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k4-draftonly-serialgdnpacked-promote-tailfallback-currentbaseline-eager-tp2-20260618by-000000-0-9c23d12c` line `2`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k4-draftonly-serialgdnpacked-promote-tailfallback-currentbaseline-eager-tp2-20260618by-000000-0-9c23d12c` line `3`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k4-draftonly-serialgdnpacked-promote-tailfallback-currentbaseline-eager-tp2-20260618by-000000-0-9c23d12c` line `4`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k4-draftonly-serialgdnpacked-promote-tailfallback-currentbaseline-eager-tp2-20260618by-000000-0-9c23d12c` line `5`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k4-draftonly-serialgdnpacked-promote-tailfallback-currentbaseline-eager-tp2-20260618by-000000-0-9c23d12c` line `6`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k4-draftonly-serialgdnpacked-promote-tailfallback-currentbaseline-eager-tp2-20260618by-000000-0-9c23d12c` line `7`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k4-draftonly-serialgdnpacked-promote-tailfallback-currentbaseline-eager-tp2-20260618by-000000-0-9c23d12c` | 1 | 5 | 4 | 0 | -1 | 4 | 4 |
| `cmpl-qwen36-oracle-k4-draftonly-serialgdnpacked-promote-tailfallback-currentbaseline-eager-tp2-20260618by-000000-0-9c23d12c` | 2 | 5 | 4 | 0 | -1 | 4 | 4 |
| `cmpl-qwen36-oracle-k4-draftonly-serialgdnpacked-promote-tailfallback-currentbaseline-eager-tp2-20260618by-000000-0-9c23d12c` | 3 | 5 | 4 | 0 | -1 | 4 | 4 |
| `cmpl-qwen36-oracle-k4-draftonly-serialgdnpacked-promote-tailfallback-currentbaseline-eager-tp2-20260618by-000000-0-9c23d12c` | 4 | 5 | 4 | 0 | -1 | 4 | 4 |
| `cmpl-qwen36-oracle-k4-draftonly-serialgdnpacked-promote-tailfallback-currentbaseline-eager-tp2-20260618by-000000-0-9c23d12c` | 5 | 5 | 4 | 0 | -1 | 4 | 4 |
| `cmpl-qwen36-oracle-k4-draftonly-serialgdnpacked-promote-tailfallback-currentbaseline-eager-tp2-20260618by-000000-0-9c23d12c` | 6 | 5 | 4 | 0 | -1 | 4 | 4 |
| `cmpl-qwen36-oracle-k4-draftonly-serialgdnpacked-promote-tailfallback-currentbaseline-eager-tp2-20260618by-000000-0-9c23d12c` | 7 | 5 | 4 | 0 | -1 | 4 | 4 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
