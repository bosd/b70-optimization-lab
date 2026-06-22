# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-spec-trace.jsonl`
- rows: `31`
- malformed rows: `0`
- requests: `1`
- suppressed follow-up mismatches: `0`
- suppressed schedule mismatches: `0`
- suppressed accept mismatches: `0`
- accounting mismatches: `31`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` | 31 | 31 | 31 | 0 | 0 | `natural_latency_plan (scheduler_prefix)` | 0 | 0 | 0 | 31 |

## Accounting Mismatches

- request `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` line `1`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` line `2`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` line `3`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` line `4`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` line `5`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` line `6`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` line `7`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` line `8`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` line `9`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` line `10`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` line `11`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` line `12`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` line `13`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` line `14`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` line `15`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` line `16`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` line `17`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` line `18`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` line `19`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` line `20`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` line `21`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` line `22`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` line `23`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` line `24`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` line `25`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` line `26`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` line `27`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` line `28`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` line `29`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` line `30`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` line `31`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` | 1 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` | 2 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` | 3 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` | 4 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` | 5 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` | 6 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` | 7 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` | 8 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` | 9 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` | 10 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` | 11 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` | 12 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` | 13 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` | 14 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` | 15 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` | 16 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` | 17 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` | 18 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` | 19 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-000000-0-a79b1889` | 20 | 2 | 1 | 0 | -1 | 1 | 1 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
