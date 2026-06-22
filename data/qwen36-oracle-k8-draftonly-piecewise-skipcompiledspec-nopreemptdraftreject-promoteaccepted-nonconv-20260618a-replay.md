# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-oracle-k8-draftonly-piecewise-skipcompiledspec-nopreemptdraftreject-promoteaccepted-nonconv-20260618a-spec-trace.jsonl`
- rows: `3`
- malformed rows: `0`
- requests: `1`
- suppressed follow-up mismatches: `0`
- suppressed schedule mismatches: `0`
- suppressed accept mismatches: `0`
- accounting mismatches: `3`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k8-draftonly-piecewise-skipcompiledspec-nopreemptdraftreject-promoteaccepted-nonconv-20260618a-000000-0-a0ab2d29` | 3 | 24 | 21 | 3 | 0 | `natural_latency_plan (scheduler_prefix)` | 0 | 0 | 0 | 3 |

## Accounting Mismatches

- request `cmpl-qwen36-oracle-k8-draftonly-piecewise-skipcompiledspec-nopreemptdraftreject-promoteaccepted-nonconv-20260618a-000000-0-a0ab2d29` line `1`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k8-draftonly-piecewise-skipcompiledspec-nopreemptdraftreject-promoteaccepted-nonconv-20260618a-000000-0-a0ab2d29` line `2`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k8-draftonly-piecewise-skipcompiledspec-nopreemptdraftreject-promoteaccepted-nonconv-20260618a-000000-0-a0ab2d29` line `3`: expected computed delta `-3` from rejected `3` plus suppressed `0`, observed `-4`.

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k8-draftonly-piecewise-skipcompiledspec-nopreemptdraftreject-promoteaccepted-nonconv-20260618a-000000-0-a0ab2d29` | 1 | 9 | 8 | 0 | -1 | 8 | 8 |
| `cmpl-qwen36-oracle-k8-draftonly-piecewise-skipcompiledspec-nopreemptdraftreject-promoteaccepted-nonconv-20260618a-000000-0-a0ab2d29` | 2 | 9 | 8 | 0 | -1 | 8 | 8 |
| `cmpl-qwen36-oracle-k8-draftonly-piecewise-skipcompiledspec-nopreemptdraftreject-promoteaccepted-nonconv-20260618a-000000-0-a0ab2d29` | 3 | 9 | 5 | 3 | -4 | 5 | 5 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
