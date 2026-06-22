# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-oracle-k7-draftonly-nativeprefill-exactstatereplay-offset1-manualconv-nofinalpromote-postprocess-currenttree-eager-tp2-20260618e-spec-trace.jsonl`
- rows: `4`
- malformed rows: `0`
- requests: `1`
- suppressed follow-up mismatches: `0`
- suppressed schedule mismatches: `0`
- suppressed accept mismatches: `0`
- accounting mismatches: `3`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k7-draftonly-nativeprefill-exactstatereplay-offset1-manualconv-nofinalpromote-postprocess-currenttree-eager-tp2-20260618e-000000-0-a28c014a` | 4 | 28 | 23 | 5 | 0 | `natural_latency_plan (scheduler_prefix)` | 0 | 0 | 0 | 3 |

## Accounting Mismatches

- request `cmpl-qwen36-oracle-k7-draftonly-nativeprefill-exactstatereplay-offset1-manualconv-nofinalpromote-postprocess-currenttree-eager-tp2-20260618e-000000-0-a28c014a` line `1`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k7-draftonly-nativeprefill-exactstatereplay-offset1-manualconv-nofinalpromote-postprocess-currenttree-eager-tp2-20260618e-000000-0-a28c014a` line `2`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k7-draftonly-nativeprefill-exactstatereplay-offset1-manualconv-nofinalpromote-postprocess-currenttree-eager-tp2-20260618e-000000-0-a28c014a` line `3`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k7-draftonly-nativeprefill-exactstatereplay-offset1-manualconv-nofinalpromote-postprocess-currenttree-eager-tp2-20260618e-000000-0-a28c014a` | 1 | 8 | 7 | 0 | -1 | 7 | 7 |
| `cmpl-qwen36-oracle-k7-draftonly-nativeprefill-exactstatereplay-offset1-manualconv-nofinalpromote-postprocess-currenttree-eager-tp2-20260618e-000000-0-a28c014a` | 2 | 8 | 7 | 0 | -1 | 7 | 7 |
| `cmpl-qwen36-oracle-k7-draftonly-nativeprefill-exactstatereplay-offset1-manualconv-nofinalpromote-postprocess-currenttree-eager-tp2-20260618e-000000-0-a28c014a` | 3 | 8 | 7 | 0 | -1 | 7 | 7 |
| `cmpl-qwen36-oracle-k7-draftonly-nativeprefill-exactstatereplay-offset1-manualconv-nofinalpromote-postprocess-currenttree-eager-tp2-20260618e-000000-0-a28c014a` | 4 | 8 | 2 | 5 | -5 | 2 | 2 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
