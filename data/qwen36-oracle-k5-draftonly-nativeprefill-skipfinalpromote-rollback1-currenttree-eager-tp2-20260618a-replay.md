# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-oracle-k5-draftonly-nativeprefill-skipfinalpromote-rollback1-currenttree-eager-tp2-20260618a-spec-trace.jsonl`
- rows: `5`
- malformed rows: `0`
- requests: `1`
- suppressed follow-up mismatches: `0`
- suppressed schedule mismatches: `0`
- suppressed accept mismatches: `0`
- accounting mismatches: `4`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k5-draftonly-nativeprefill-skipfinalpromote-rollback1-currenttree-eager-tp2-20260618a-000000-0-b3f45799` | 5 | 25 | 23 | 2 | 0 | `natural_latency_plan (scheduler_prefix)` | 0 | 0 | 0 | 4 |

## Accounting Mismatches

- request `cmpl-qwen36-oracle-k5-draftonly-nativeprefill-skipfinalpromote-rollback1-currenttree-eager-tp2-20260618a-000000-0-b3f45799` line `1`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k5-draftonly-nativeprefill-skipfinalpromote-rollback1-currenttree-eager-tp2-20260618a-000000-0-b3f45799` line `2`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k5-draftonly-nativeprefill-skipfinalpromote-rollback1-currenttree-eager-tp2-20260618a-000000-0-b3f45799` line `3`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k5-draftonly-nativeprefill-skipfinalpromote-rollback1-currenttree-eager-tp2-20260618a-000000-0-b3f45799` line `4`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k5-draftonly-nativeprefill-skipfinalpromote-rollback1-currenttree-eager-tp2-20260618a-000000-0-b3f45799` | 1 | 6 | 5 | 0 | -1 | 5 | 5 |
| `cmpl-qwen36-oracle-k5-draftonly-nativeprefill-skipfinalpromote-rollback1-currenttree-eager-tp2-20260618a-000000-0-b3f45799` | 2 | 6 | 5 | 0 | -1 | 5 | 5 |
| `cmpl-qwen36-oracle-k5-draftonly-nativeprefill-skipfinalpromote-rollback1-currenttree-eager-tp2-20260618a-000000-0-b3f45799` | 3 | 6 | 5 | 0 | -1 | 5 | 5 |
| `cmpl-qwen36-oracle-k5-draftonly-nativeprefill-skipfinalpromote-rollback1-currenttree-eager-tp2-20260618a-000000-0-b3f45799` | 4 | 6 | 5 | 0 | -1 | 5 | 5 |
| `cmpl-qwen36-oracle-k5-draftonly-nativeprefill-skipfinalpromote-rollback1-currenttree-eager-tp2-20260618a-000000-0-b3f45799` | 5 | 6 | 3 | 2 | -2 | 3 | 3 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
