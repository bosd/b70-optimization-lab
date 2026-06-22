# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-oracle-k8-draftonly-commitfull-acceptedkplus1-eager-20260618a-spec-trace.jsonl`
- rows: `3`
- malformed rows: `0`
- requests: `1`
- suppressed follow-up mismatches: `0`
- suppressed schedule mismatches: `0`
- suppressed accept mismatches: `0`
- accounting mismatches: `1`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k8-draftonly-commitfull-acceptedkplus1-eager-20260618a-000000-0-83f14612` | 3 | 24 | 16 | 8 | 0 | `natural_latency_plan (scheduler_prefix)` | 0 | 0 | 0 | 1 |

## Accounting Mismatches

- request `cmpl-qwen36-oracle-k8-draftonly-commitfull-acceptedkplus1-eager-20260618a-000000-0-83f14612` line `3`: expected computed delta `-8` from rejected `8` plus suppressed `0`, observed `-9`.

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k8-draftonly-commitfull-acceptedkplus1-eager-20260618a-000000-0-83f14612` | 1 | 9 | 8 | 0 | 0 | 8 | 8 |
| `cmpl-qwen36-oracle-k8-draftonly-commitfull-acceptedkplus1-eager-20260618a-000000-0-83f14612` | 2 | 9 | 8 | 0 | 0 | 8 | 8 |
| `cmpl-qwen36-oracle-k8-draftonly-commitfull-acceptedkplus1-eager-20260618a-000000-0-83f14612` | 3 | 9 | 0 | 8 | -9 | 0 | 0 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
