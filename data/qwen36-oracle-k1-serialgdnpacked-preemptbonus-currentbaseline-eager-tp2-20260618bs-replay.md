# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-oracle-k1-serialgdnpacked-preemptbonus-currentbaseline-eager-tp2-20260618bs-spec-trace.jsonl`
- rows: `6`
- malformed rows: `0`
- requests: `1`
- suppressed follow-up mismatches: `5`
- suppressed schedule mismatches: `5`
- suppressed accept mismatches: `5`
- accounting mismatches: `0`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k1-serialgdnpacked-preemptbonus-currentbaseline-eager-tp2-20260618bs-000000-0-ad9f694c` | 6 | 6 | 6 | 0 | 6 | `natural_latency_plan (scheduler_prefix)` | 5 | 5 | 5 | 0 |

## Suppressed Follow-Up Mismatches

- request `cmpl-qwen36-oracle-k1-serialgdnpacked-preemptbonus-currentbaseline-eager-tp2-20260618bs-000000-0-ad9f694c` line `1` -> `2`:
  suppressed `27044` ` dense`, next scheduled `14246` ` engineering`, next verifier token was `14246` ` engineering`, next emitted `14246` ` engineering`.
- request `cmpl-qwen36-oracle-k1-serialgdnpacked-preemptbonus-currentbaseline-eager-tp2-20260618bs-000000-0-ad9f694c` line `2` -> `3`:
  suppressed `8129` ` notes`, next scheduled `24985` ` Focus`, next verifier token was `24985` ` Focus`, next emitted `24985` ` Focus`.
- request `cmpl-qwen36-oracle-k1-serialgdnpacked-preemptbonus-currentbaseline-eager-tp2-20260618bs-000000-0-ad9f694c` line `3` -> `4`:
  suppressed `383` ` on`, next scheduled `43318` `-request`, next verifier token was `43318` `-request`, next emitted `43318` `-request`.
- request `cmpl-qwen36-oracle-k1-serialgdnpacked-preemptbonus-currentbaseline-eager-tp2-20260618bs-000000-0-ad9f694c` line `4` -> `5`:
  suppressed `16401` ` decode`, next scheduled `11` `,`, next verifier token was `11` `,`, next emitted `11` `,`.
- request `cmpl-qwen36-oracle-k1-serialgdnpacked-preemptbonus-currentbaseline-eager-tp2-20260618bs-000000-0-ad9f694c` line `5` -> `6`:
  suppressed `29541` ` reliability`, next scheduled `11` `,`, next verifier token was `11` `,`, next emitted `11` `,`.

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k1-serialgdnpacked-preemptbonus-currentbaseline-eager-tp2-20260618bs-000000-0-ad9f694c` | 1 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-serialgdnpacked-preemptbonus-currentbaseline-eager-tp2-20260618bs-000000-0-ad9f694c` | 2 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-serialgdnpacked-preemptbonus-currentbaseline-eager-tp2-20260618bs-000000-0-ad9f694c` | 3 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-serialgdnpacked-preemptbonus-currentbaseline-eager-tp2-20260618bs-000000-0-ad9f694c` | 4 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-serialgdnpacked-preemptbonus-currentbaseline-eager-tp2-20260618bs-000000-0-ad9f694c` | 5 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-serialgdnpacked-preemptbonus-currentbaseline-eager-tp2-20260618bs-000000-0-ad9f694c` | 6 | 2 | 1 | 0 | -1 | 1 | 1 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
