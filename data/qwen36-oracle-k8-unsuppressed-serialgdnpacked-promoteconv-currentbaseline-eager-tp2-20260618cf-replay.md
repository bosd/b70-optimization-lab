# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-oracle-k8-unsuppressed-serialgdnpacked-promoteconv-currentbaseline-eager-tp2-20260618cf-spec-trace.jsonl`
- rows: `3`
- malformed rows: `0`
- requests: `1`
- suppressed follow-up mismatches: `2`
- suppressed schedule mismatches: `2`
- suppressed accept mismatches: `2`
- accounting mismatches: `0`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k8-unsuppressed-serialgdnpacked-promoteconv-currentbaseline-eager-tp2-20260618cf-000000-0-8689ddad` | 3 | 24 | 21 | 3 | 2 | `natural_latency_plan (scheduler_prefix)` | 2 | 2 | 2 | 0 |

## Suppressed Follow-Up Mismatches

- request `cmpl-qwen36-oracle-k8-unsuppressed-serialgdnpacked-promoteconv-currentbaseline-eager-tp2-20260618cf-000000-0-8689ddad` line `1` -> `2`:
  suppressed `3074` ` single`, next scheduled `43318` `-request`, next verifier token was `43318` `-request`, next emitted `43318` `-request`.
- request `cmpl-qwen36-oracle-k8-unsuppressed-serialgdnpacked-promoteconv-currentbaseline-eager-tp2-20260618cf-000000-0-8689ddad` line `2` -> `3`:
  suppressed `874` ` no`, next scheduled `4131` ` quality`, next verifier token was `4131` ` quality`, next emitted `4131` ` quality`.

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k8-unsuppressed-serialgdnpacked-promoteconv-currentbaseline-eager-tp2-20260618cf-000000-0-8689ddad` | 1 | 9 | 8 | 0 | -1 | 8 | 8 |
| `cmpl-qwen36-oracle-k8-unsuppressed-serialgdnpacked-promoteconv-currentbaseline-eager-tp2-20260618cf-000000-0-8689ddad` | 2 | 9 | 8 | 0 | -1 | 8 | 8 |
| `cmpl-qwen36-oracle-k8-unsuppressed-serialgdnpacked-promoteconv-currentbaseline-eager-tp2-20260618cf-000000-0-8689ddad` | 3 | 9 | 5 | 3 | -3 | 6 | 6 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
