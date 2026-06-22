# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-oracle-k1-draftonly-currentbaseline-eager-tp2-20260618bu-spec-trace.jsonl`
- rows: `17`
- malformed rows: `0`
- requests: `1`
- suppressed follow-up mismatches: `0`
- suppressed schedule mismatches: `0`
- suppressed accept mismatches: `0`
- accounting mismatches: `17`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k1-draftonly-currentbaseline-eager-tp2-20260618bu-000000-0-9f994652` | 17 | 17 | 16 | 1 | 0 | `natural_latency_plan (scheduler_prefix)` | 0 | 0 | 0 | 17 |

## Accounting Mismatches

- request `cmpl-qwen36-oracle-k1-draftonly-currentbaseline-eager-tp2-20260618bu-000000-0-9f994652` line `1`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-currentbaseline-eager-tp2-20260618bu-000000-0-9f994652` line `2`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-currentbaseline-eager-tp2-20260618bu-000000-0-9f994652` line `3`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-currentbaseline-eager-tp2-20260618bu-000000-0-9f994652` line `4`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-currentbaseline-eager-tp2-20260618bu-000000-0-9f994652` line `5`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-currentbaseline-eager-tp2-20260618bu-000000-0-9f994652` line `6`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-currentbaseline-eager-tp2-20260618bu-000000-0-9f994652` line `7`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-currentbaseline-eager-tp2-20260618bu-000000-0-9f994652` line `8`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-currentbaseline-eager-tp2-20260618bu-000000-0-9f994652` line `9`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-currentbaseline-eager-tp2-20260618bu-000000-0-9f994652` line `10`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-currentbaseline-eager-tp2-20260618bu-000000-0-9f994652` line `11`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-currentbaseline-eager-tp2-20260618bu-000000-0-9f994652` line `12`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-currentbaseline-eager-tp2-20260618bu-000000-0-9f994652` line `13`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-currentbaseline-eager-tp2-20260618bu-000000-0-9f994652` line `14`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-currentbaseline-eager-tp2-20260618bu-000000-0-9f994652` line `15`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-currentbaseline-eager-tp2-20260618bu-000000-0-9f994652` line `16`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k1-draftonly-currentbaseline-eager-tp2-20260618bu-000000-0-9f994652` line `17`: expected computed delta `-1` from rejected `1` plus suppressed `0`, observed `-2`.

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k1-draftonly-currentbaseline-eager-tp2-20260618bu-000000-0-9f994652` | 1 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-draftonly-currentbaseline-eager-tp2-20260618bu-000000-0-9f994652` | 2 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-draftonly-currentbaseline-eager-tp2-20260618bu-000000-0-9f994652` | 3 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-draftonly-currentbaseline-eager-tp2-20260618bu-000000-0-9f994652` | 4 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-draftonly-currentbaseline-eager-tp2-20260618bu-000000-0-9f994652` | 5 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-draftonly-currentbaseline-eager-tp2-20260618bu-000000-0-9f994652` | 6 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-draftonly-currentbaseline-eager-tp2-20260618bu-000000-0-9f994652` | 7 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-draftonly-currentbaseline-eager-tp2-20260618bu-000000-0-9f994652` | 8 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-draftonly-currentbaseline-eager-tp2-20260618bu-000000-0-9f994652` | 9 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-draftonly-currentbaseline-eager-tp2-20260618bu-000000-0-9f994652` | 10 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-draftonly-currentbaseline-eager-tp2-20260618bu-000000-0-9f994652` | 11 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-draftonly-currentbaseline-eager-tp2-20260618bu-000000-0-9f994652` | 12 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-draftonly-currentbaseline-eager-tp2-20260618bu-000000-0-9f994652` | 13 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-draftonly-currentbaseline-eager-tp2-20260618bu-000000-0-9f994652` | 14 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-draftonly-currentbaseline-eager-tp2-20260618bu-000000-0-9f994652` | 15 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-draftonly-currentbaseline-eager-tp2-20260618bu-000000-0-9f994652` | 16 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-draftonly-currentbaseline-eager-tp2-20260618bu-000000-0-9f994652` | 17 | 2 | 0 | 1 | -2 | 0 | 0 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
