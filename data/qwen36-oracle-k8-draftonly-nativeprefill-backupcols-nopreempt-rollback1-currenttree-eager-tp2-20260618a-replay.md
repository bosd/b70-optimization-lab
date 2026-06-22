# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-oracle-k8-draftonly-nativeprefill-backupcols-nopreempt-rollback1-currenttree-eager-tp2-20260618a-spec-trace.jsonl`
- rows: `4`
- malformed rows: `0`
- requests: `1`
- suppressed follow-up mismatches: `0`
- suppressed schedule mismatches: `0`
- suppressed accept mismatches: `0`
- accounting mismatches: `4`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k8-draftonly-nativeprefill-backupcols-nopreempt-rollback1-currenttree-eager-tp2-20260618a-000000-0-b5efa862` | 4 | 32 | 20 | 12 | 0 | `natural_latency_plan (scheduler_prefix)` | 0 | 0 | 0 | 4 |

## Accounting Mismatches

- request `cmpl-qwen36-oracle-k8-draftonly-nativeprefill-backupcols-nopreempt-rollback1-currenttree-eager-tp2-20260618a-000000-0-b5efa862` line `1`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k8-draftonly-nativeprefill-backupcols-nopreempt-rollback1-currenttree-eager-tp2-20260618a-000000-0-b5efa862` line `2`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k8-draftonly-nativeprefill-backupcols-nopreempt-rollback1-currenttree-eager-tp2-20260618a-000000-0-b5efa862` line `3`: expected computed delta `-8` from rejected `8` plus suppressed `0`, observed `-10`.
- request `cmpl-qwen36-oracle-k8-draftonly-nativeprefill-backupcols-nopreempt-rollback1-currenttree-eager-tp2-20260618a-000000-0-b5efa862` line `4`: expected computed delta `-4` from rejected `4` plus suppressed `0`, observed `-6`.

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k8-draftonly-nativeprefill-backupcols-nopreempt-rollback1-currenttree-eager-tp2-20260618a-000000-0-b5efa862` | 1 | 9 | 8 | 0 | -1 | 8 | 8 |
| `cmpl-qwen36-oracle-k8-draftonly-nativeprefill-backupcols-nopreempt-rollback1-currenttree-eager-tp2-20260618a-000000-0-b5efa862` | 2 | 9 | 8 | 0 | -1 | 8 | 8 |
| `cmpl-qwen36-oracle-k8-draftonly-nativeprefill-backupcols-nopreempt-rollback1-currenttree-eager-tp2-20260618a-000000-0-b5efa862` | 3 | 9 | 0 | 8 | -10 | 0 | 0 |
| `cmpl-qwen36-oracle-k8-draftonly-nativeprefill-backupcols-nopreempt-rollback1-currenttree-eager-tp2-20260618a-000000-0-b5efa862` | 4 | 9 | 4 | 4 | -6 | 4 | 4 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
