# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-oracle-k8-draftonly-fullacceptrestore-align-eager-20260618c-spec-trace.jsonl`
- rows: `4`
- malformed rows: `0`
- requests: `1`
- suppressed follow-up mismatches: `0`
- suppressed schedule mismatches: `0`
- suppressed accept mismatches: `0`
- accounting mismatches: `4`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k8-draftonly-fullacceptrestore-align-eager-20260618c-000000-0-b888a9f9` | 4 | 32 | 22 | 10 | 0 | `natural_latency_plan (scheduler_prefix)` | 0 | 0 | 0 | 4 |

## Accounting Mismatches

- request `cmpl-qwen36-oracle-k8-draftonly-fullacceptrestore-align-eager-20260618c-000000-0-b888a9f9` line `1`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-9`.
- request `cmpl-qwen36-oracle-k8-draftonly-fullacceptrestore-align-eager-20260618c-000000-0-b888a9f9` line `2`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-9`.
- request `cmpl-qwen36-oracle-k8-draftonly-fullacceptrestore-align-eager-20260618c-000000-0-b888a9f9` line `3`: expected computed delta `-8` from rejected `8` plus suppressed `0`, observed `-9`.
- request `cmpl-qwen36-oracle-k8-draftonly-fullacceptrestore-align-eager-20260618c-000000-0-b888a9f9` line `4`: expected computed delta `-2` from rejected `2` plus suppressed `0`, observed `-9`.

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k8-draftonly-fullacceptrestore-align-eager-20260618c-000000-0-b888a9f9` | 1 | 9 | 8 | 0 | -9 | 0 | 0 |
| `cmpl-qwen36-oracle-k8-draftonly-fullacceptrestore-align-eager-20260618c-000000-0-b888a9f9` | 2 | 9 | 8 | 0 | -9 | 0 | 0 |
| `cmpl-qwen36-oracle-k8-draftonly-fullacceptrestore-align-eager-20260618c-000000-0-b888a9f9` | 3 | 9 | 0 | 8 | -9 | 0 | 0 |
| `cmpl-qwen36-oracle-k8-draftonly-fullacceptrestore-align-eager-20260618c-000000-0-b888a9f9` | 4 | 9 | 6 | 2 | -9 | 6 | 6 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
