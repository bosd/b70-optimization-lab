# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-oracle-k8-graph-tp2-suppressreplacement-extra1-20260618i-spec-trace.jsonl`
- rows: `3`
- malformed rows: `0`
- requests: `1`
- suppressed follow-up mismatches: `0`
- suppressed schedule mismatches: `0`
- suppressed accept mismatches: `0`
- accounting mismatches: `2`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k8-graph-tp2-suppressreplacement-extra1-20260618i-000000-0-8d44c1ca` | 3 | 24 | 20 | 4 | 0 | `natural_latency_plan (scheduler_prefix)` | 0 | 0 | 0 | 2 |

## Accounting Mismatches

- request `cmpl-qwen36-oracle-k8-graph-tp2-suppressreplacement-extra1-20260618i-000000-0-8d44c1ca` line `2`: expected computed delta `-2` from rejected `1` plus suppressed `0`, observed `-9`.
- request `cmpl-qwen36-oracle-k8-graph-tp2-suppressreplacement-extra1-20260618i-000000-0-8d44c1ca` line `3`: expected computed delta `-4` from rejected `3` plus suppressed `0`, observed `-9`.

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k8-graph-tp2-suppressreplacement-extra1-20260618i-000000-0-8d44c1ca` | 1 | 9 | 8 | 0 | 0 | 9 | 9 |
| `cmpl-qwen36-oracle-k8-graph-tp2-suppressreplacement-extra1-20260618i-000000-0-8d44c1ca` | 2 | 9 | 7 | 1 | -9 | 0 | 0 |
| `cmpl-qwen36-oracle-k8-graph-tp2-suppressreplacement-extra1-20260618i-000000-0-8d44c1ca` | 3 | 9 | 5 | 3 | -9 | 0 | 0 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
