# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-oracle-k3-draftonly-nativeprefill-skipfinalpromote-rollback1-currenttree-eager-tp2-20260618a-spec-trace.jsonl`
- rows: `3`
- malformed rows: `0`
- requests: `1`
- suppressed follow-up mismatches: `0`
- suppressed schedule mismatches: `0`
- suppressed accept mismatches: `0`
- accounting mismatches: `2`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k3-draftonly-nativeprefill-skipfinalpromote-rollback1-currenttree-eager-tp2-20260618a-000000-0-ac8b9061` | 3 | 9 | 6 | 3 | 0 | `natural_latency_plan (scheduler_prefix)` | 0 | 0 | 0 | 2 |

## Accounting Mismatches

- request `cmpl-qwen36-oracle-k3-draftonly-nativeprefill-skipfinalpromote-rollback1-currenttree-eager-tp2-20260618a-000000-0-ac8b9061` line `1`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k3-draftonly-nativeprefill-skipfinalpromote-rollback1-currenttree-eager-tp2-20260618a-000000-0-ac8b9061` line `2`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k3-draftonly-nativeprefill-skipfinalpromote-rollback1-currenttree-eager-tp2-20260618a-000000-0-ac8b9061` | 1 | 4 | 3 | 0 | -1 | 3 | 3 |
| `cmpl-qwen36-oracle-k3-draftonly-nativeprefill-skipfinalpromote-rollback1-currenttree-eager-tp2-20260618a-000000-0-ac8b9061` | 2 | 4 | 3 | 0 | -1 | 3 | 3 |
| `cmpl-qwen36-oracle-k3-draftonly-nativeprefill-skipfinalpromote-rollback1-currenttree-eager-tp2-20260618a-000000-0-ac8b9061` | 3 | 4 | 0 | 3 | -3 | 0 | 0 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
