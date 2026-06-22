# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-oracle-k2-draftonly-serialgdnpacked-tailfallback-currentbaseline-eager-tp2-20260618bw-spec-trace.jsonl`
- rows: `15`
- malformed rows: `0`
- requests: `1`
- suppressed follow-up mismatches: `0`
- suppressed schedule mismatches: `0`
- suppressed accept mismatches: `0`
- accounting mismatches: `15`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k2-draftonly-serialgdnpacked-tailfallback-currentbaseline-eager-tp2-20260618bw-000000-0-905ecc1a` | 15 | 30 | 30 | 0 | 0 | `natural_latency_plan (scheduler_prefix)` | 0 | 0 | 0 | 15 |

## Accounting Mismatches

- request `cmpl-qwen36-oracle-k2-draftonly-serialgdnpacked-tailfallback-currentbaseline-eager-tp2-20260618bw-000000-0-905ecc1a` line `1`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k2-draftonly-serialgdnpacked-tailfallback-currentbaseline-eager-tp2-20260618bw-000000-0-905ecc1a` line `2`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k2-draftonly-serialgdnpacked-tailfallback-currentbaseline-eager-tp2-20260618bw-000000-0-905ecc1a` line `3`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k2-draftonly-serialgdnpacked-tailfallback-currentbaseline-eager-tp2-20260618bw-000000-0-905ecc1a` line `4`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k2-draftonly-serialgdnpacked-tailfallback-currentbaseline-eager-tp2-20260618bw-000000-0-905ecc1a` line `5`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k2-draftonly-serialgdnpacked-tailfallback-currentbaseline-eager-tp2-20260618bw-000000-0-905ecc1a` line `6`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k2-draftonly-serialgdnpacked-tailfallback-currentbaseline-eager-tp2-20260618bw-000000-0-905ecc1a` line `7`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k2-draftonly-serialgdnpacked-tailfallback-currentbaseline-eager-tp2-20260618bw-000000-0-905ecc1a` line `8`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k2-draftonly-serialgdnpacked-tailfallback-currentbaseline-eager-tp2-20260618bw-000000-0-905ecc1a` line `9`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k2-draftonly-serialgdnpacked-tailfallback-currentbaseline-eager-tp2-20260618bw-000000-0-905ecc1a` line `10`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k2-draftonly-serialgdnpacked-tailfallback-currentbaseline-eager-tp2-20260618bw-000000-0-905ecc1a` line `11`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k2-draftonly-serialgdnpacked-tailfallback-currentbaseline-eager-tp2-20260618bw-000000-0-905ecc1a` line `12`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k2-draftonly-serialgdnpacked-tailfallback-currentbaseline-eager-tp2-20260618bw-000000-0-905ecc1a` line `13`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k2-draftonly-serialgdnpacked-tailfallback-currentbaseline-eager-tp2-20260618bw-000000-0-905ecc1a` line `14`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k2-draftonly-serialgdnpacked-tailfallback-currentbaseline-eager-tp2-20260618bw-000000-0-905ecc1a` line `15`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k2-draftonly-serialgdnpacked-tailfallback-currentbaseline-eager-tp2-20260618bw-000000-0-905ecc1a` | 1 | 3 | 2 | 0 | -1 | 2 | 2 |
| `cmpl-qwen36-oracle-k2-draftonly-serialgdnpacked-tailfallback-currentbaseline-eager-tp2-20260618bw-000000-0-905ecc1a` | 2 | 3 | 2 | 0 | -1 | 2 | 2 |
| `cmpl-qwen36-oracle-k2-draftonly-serialgdnpacked-tailfallback-currentbaseline-eager-tp2-20260618bw-000000-0-905ecc1a` | 3 | 3 | 2 | 0 | -1 | 2 | 2 |
| `cmpl-qwen36-oracle-k2-draftonly-serialgdnpacked-tailfallback-currentbaseline-eager-tp2-20260618bw-000000-0-905ecc1a` | 4 | 3 | 2 | 0 | -1 | 2 | 2 |
| `cmpl-qwen36-oracle-k2-draftonly-serialgdnpacked-tailfallback-currentbaseline-eager-tp2-20260618bw-000000-0-905ecc1a` | 5 | 3 | 2 | 0 | -1 | 2 | 2 |
| `cmpl-qwen36-oracle-k2-draftonly-serialgdnpacked-tailfallback-currentbaseline-eager-tp2-20260618bw-000000-0-905ecc1a` | 6 | 3 | 2 | 0 | -1 | 2 | 2 |
| `cmpl-qwen36-oracle-k2-draftonly-serialgdnpacked-tailfallback-currentbaseline-eager-tp2-20260618bw-000000-0-905ecc1a` | 7 | 3 | 2 | 0 | -1 | 2 | 2 |
| `cmpl-qwen36-oracle-k2-draftonly-serialgdnpacked-tailfallback-currentbaseline-eager-tp2-20260618bw-000000-0-905ecc1a` | 8 | 3 | 2 | 0 | -1 | 2 | 2 |
| `cmpl-qwen36-oracle-k2-draftonly-serialgdnpacked-tailfallback-currentbaseline-eager-tp2-20260618bw-000000-0-905ecc1a` | 9 | 3 | 2 | 0 | -1 | 2 | 2 |
| `cmpl-qwen36-oracle-k2-draftonly-serialgdnpacked-tailfallback-currentbaseline-eager-tp2-20260618bw-000000-0-905ecc1a` | 10 | 3 | 2 | 0 | -1 | 2 | 2 |
| `cmpl-qwen36-oracle-k2-draftonly-serialgdnpacked-tailfallback-currentbaseline-eager-tp2-20260618bw-000000-0-905ecc1a` | 11 | 3 | 2 | 0 | -1 | 2 | 2 |
| `cmpl-qwen36-oracle-k2-draftonly-serialgdnpacked-tailfallback-currentbaseline-eager-tp2-20260618bw-000000-0-905ecc1a` | 12 | 3 | 2 | 0 | -1 | 2 | 2 |
| `cmpl-qwen36-oracle-k2-draftonly-serialgdnpacked-tailfallback-currentbaseline-eager-tp2-20260618bw-000000-0-905ecc1a` | 13 | 3 | 2 | 0 | -1 | 2 | 2 |
| `cmpl-qwen36-oracle-k2-draftonly-serialgdnpacked-tailfallback-currentbaseline-eager-tp2-20260618bw-000000-0-905ecc1a` | 14 | 3 | 2 | 0 | -1 | 2 | 2 |
| `cmpl-qwen36-oracle-k2-draftonly-serialgdnpacked-tailfallback-currentbaseline-eager-tp2-20260618bw-000000-0-905ecc1a` | 15 | 3 | 2 | 0 | -1 | 2 | 2 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
