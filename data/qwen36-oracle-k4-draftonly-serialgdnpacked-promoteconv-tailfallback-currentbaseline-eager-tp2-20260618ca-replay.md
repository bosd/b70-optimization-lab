# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-oracle-k4-draftonly-serialgdnpacked-promoteconv-tailfallback-currentbaseline-eager-tp2-20260618ca-spec-trace.jsonl`
- rows: `7`
- malformed rows: `0`
- requests: `1`
- suppressed follow-up mismatches: `0`
- suppressed schedule mismatches: `0`
- suppressed accept mismatches: `0`
- accounting mismatches: `7`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k4-draftonly-serialgdnpacked-promoteconv-tailfallback-currentbaseline-eager-tp2-20260618ca-000000-0-a1e88d1d` | 7 | 28 | 28 | 0 | 0 | `natural_latency_plan (scheduler_prefix)` | 0 | 0 | 0 | 7 |

## Accounting Mismatches

- request `cmpl-qwen36-oracle-k4-draftonly-serialgdnpacked-promoteconv-tailfallback-currentbaseline-eager-tp2-20260618ca-000000-0-a1e88d1d` line `1`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k4-draftonly-serialgdnpacked-promoteconv-tailfallback-currentbaseline-eager-tp2-20260618ca-000000-0-a1e88d1d` line `2`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k4-draftonly-serialgdnpacked-promoteconv-tailfallback-currentbaseline-eager-tp2-20260618ca-000000-0-a1e88d1d` line `3`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k4-draftonly-serialgdnpacked-promoteconv-tailfallback-currentbaseline-eager-tp2-20260618ca-000000-0-a1e88d1d` line `4`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k4-draftonly-serialgdnpacked-promoteconv-tailfallback-currentbaseline-eager-tp2-20260618ca-000000-0-a1e88d1d` line `5`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k4-draftonly-serialgdnpacked-promoteconv-tailfallback-currentbaseline-eager-tp2-20260618ca-000000-0-a1e88d1d` line `6`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.
- request `cmpl-qwen36-oracle-k4-draftonly-serialgdnpacked-promoteconv-tailfallback-currentbaseline-eager-tp2-20260618ca-000000-0-a1e88d1d` line `7`: expected computed delta `0` from rejected `0` plus suppressed `0`, observed `-1`.

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k4-draftonly-serialgdnpacked-promoteconv-tailfallback-currentbaseline-eager-tp2-20260618ca-000000-0-a1e88d1d` | 1 | 5 | 4 | 0 | -1 | 4 | 4 |
| `cmpl-qwen36-oracle-k4-draftonly-serialgdnpacked-promoteconv-tailfallback-currentbaseline-eager-tp2-20260618ca-000000-0-a1e88d1d` | 2 | 5 | 4 | 0 | -1 | 4 | 4 |
| `cmpl-qwen36-oracle-k4-draftonly-serialgdnpacked-promoteconv-tailfallback-currentbaseline-eager-tp2-20260618ca-000000-0-a1e88d1d` | 3 | 5 | 4 | 0 | -1 | 4 | 4 |
| `cmpl-qwen36-oracle-k4-draftonly-serialgdnpacked-promoteconv-tailfallback-currentbaseline-eager-tp2-20260618ca-000000-0-a1e88d1d` | 4 | 5 | 4 | 0 | -1 | 4 | 4 |
| `cmpl-qwen36-oracle-k4-draftonly-serialgdnpacked-promoteconv-tailfallback-currentbaseline-eager-tp2-20260618ca-000000-0-a1e88d1d` | 5 | 5 | 4 | 0 | -1 | 4 | 4 |
| `cmpl-qwen36-oracle-k4-draftonly-serialgdnpacked-promoteconv-tailfallback-currentbaseline-eager-tp2-20260618ca-000000-0-a1e88d1d` | 6 | 5 | 4 | 0 | -1 | 4 | 4 |
| `cmpl-qwen36-oracle-k4-draftonly-serialgdnpacked-promoteconv-tailfallback-currentbaseline-eager-tp2-20260618ca-000000-0-a1e88d1d` | 7 | 5 | 4 | 0 | -1 | 4 | 4 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
