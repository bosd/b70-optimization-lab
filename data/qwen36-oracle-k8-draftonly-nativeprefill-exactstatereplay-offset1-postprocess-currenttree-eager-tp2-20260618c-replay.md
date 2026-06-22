# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-oracle-k8-draftonly-nativeprefill-exactstatereplay-offset1-postprocess-currenttree-eager-tp2-20260618c-spec-trace.jsonl`
- rows: `1`
- malformed rows: `0`
- requests: `1`
- suppressed follow-up mismatches: `0`
- suppressed schedule mismatches: `0`
- suppressed accept mismatches: `0`
- accounting mismatches: `0`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k8-draftonly-nativeprefill-exactstatereplay-offset1-postprocess-currenttree-eager-tp2-20260618c-000000-0-bfb334c2` | 1 | 8 | 0 | 8 | 0 | `natural_latency_plan (scheduler_prefix)` | 0 | 0 | 0 | 0 |

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k8-draftonly-nativeprefill-exactstatereplay-offset1-postprocess-currenttree-eager-tp2-20260618c-000000-0-bfb334c2` | 1 | 9 | 0 | 8 | -8 | 0 | 0 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
