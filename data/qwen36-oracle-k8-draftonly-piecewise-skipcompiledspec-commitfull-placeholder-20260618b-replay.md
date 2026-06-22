# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-oracle-k8-draftonly-piecewise-skipcompiledspec-commitfull-placeholder-20260618b-spec-trace.jsonl`
- rows: `2`
- malformed rows: `0`
- requests: `1`
- suppressed follow-up mismatches: `0`
- suppressed schedule mismatches: `0`
- suppressed accept mismatches: `0`
- accounting mismatches: `1`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k8-draftonly-piecewise-skipcompiledspec-commitfull-placeholder-20260618b-000000-0-901be818` | 2 | 16 | 15 | 1 | 0 | `natural_latency_plan (scheduler_prefix)` | 0 | 0 | 0 | 1 |

## Accounting Mismatches

- request `cmpl-qwen36-oracle-k8-draftonly-piecewise-skipcompiledspec-commitfull-placeholder-20260618b-000000-0-901be818` line `2`: expected computed delta `-1` from rejected `1` plus suppressed `0`, observed `-2`.

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k8-draftonly-piecewise-skipcompiledspec-commitfull-placeholder-20260618b-000000-0-901be818` | 1 | 9 | 8 | 0 | 0 | 8 | 8 |
| `cmpl-qwen36-oracle-k8-draftonly-piecewise-skipcompiledspec-commitfull-placeholder-20260618b-000000-0-901be818` | 2 | 9 | 7 | 1 | -2 | 7 | 7 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
