# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-oracle-k8-graph-tp2-suppressreplacement-20260618g-spec-trace.jsonl`
- rows: `3`
- malformed rows: `0`
- requests: `1`
- suppressed follow-up mismatches: `0`
- suppressed schedule mismatches: `0`
- suppressed accept mismatches: `0`
- accounting mismatches: `2`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k8-graph-tp2-suppressreplacement-20260618g-000000-0-b904aa97` | 3 | 24 | 21 | 3 | 0 | `natural_latency_plan (scheduler_prefix)` | 0 | 0 | 0 | 2 |

## Accounting Mismatches

- request `cmpl-qwen36-oracle-k8-graph-tp2-suppressreplacement-20260618g-000000-0-b904aa97` line `2`: expected computed delta `-2` from rejected `1` plus suppressed `0`, observed `-9`.
- request `cmpl-qwen36-oracle-k8-graph-tp2-suppressreplacement-20260618g-000000-0-b904aa97` line `3`: expected computed delta `-3` from rejected `2` plus suppressed `0`, observed `-9`.

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k8-graph-tp2-suppressreplacement-20260618g-000000-0-b904aa97` | 1 | 9 | 8 | 0 | 0 | 9 | 9 |
| `cmpl-qwen36-oracle-k8-graph-tp2-suppressreplacement-20260618g-000000-0-b904aa97` | 2 | 9 | 7 | 1 | -9 | 0 | 0 |
| `cmpl-qwen36-oracle-k8-graph-tp2-suppressreplacement-20260618g-000000-0-b904aa97` | 3 | 9 | 6 | 2 | -9 | 0 | 0 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
