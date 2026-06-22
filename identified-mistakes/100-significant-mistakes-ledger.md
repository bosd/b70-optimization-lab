# 100 Significant Research Mistakes

This is the significant-only index derived from `100-mistakes-ledger.md`.

Significance rule: an item counts as significant when it caused or plausibly could have caused false performance claims, invalid comparisons, unsafe promotion of corrupt output, repeated device/runtime contamination, wasted multi-day investigation paths, or missed root cause due to weak controls.

Severity tiers:

- Critical: directly risks false public/internal performance claims, unsafe promotion, or a multi-day wrong root cause.
- High: materially redirects engineering work or invalidates a class of experiments.
- Material: important enough to prevent recurrence, even if narrower than Critical/High.

All 100 entries below are significant under that rule. The original ledger keeps the full evidence/fix/history/outcome detail for each source entry.

| # | Source | Severity | Significant reason |
|---:|---|---|---|
| 1 | M001 Missing PIECEWISE Was Treated As A Performance Regression | Critical | Created a false graph-none versus forced-comm regression story around the core benchmark identity. |
| 2 | M002 Metrics-Only Fast Lane Was Described Like A Validated Lane | Critical | Let a 93 tok/s speed-only artifact look like a validated lane. |
| 3 | M003 Quality Suite Pass Hid Repeat Canary Failure | Critical | Demonstrated that quality-suite-only promotion could ship deterministic corruption. |
| 4 | M004 Shallow Gates Treated As Promotion Gates | Critical | Converted short-pass artifacts into false quality confidence. |
| 5 | M005 Localmaxxing Rows Lacked Identity Separation | High | Risked using public rows as internal proof without full validation context. |
| 6 | M006 Dirty Block-Table Speed Compared Against Different Base | High | Made an old unsafe result look relevant to a newer safe identity. |
| 7 | M007 TP2 And TP4 Cross-Comparison Was Too Easy | High | Blurred topology identity and could misdirect TP layout decisions. |
| 8 | M008 GPU Memory Utilization Not First-Class Identity | High | Changed KV/capture/stability conditions without always surfacing it in claims. |
| 9 | M009 Diagnostic Flags Missing From Summaries | High | Made failed capture and layer-gate runs difficult to reconstruct. |
| 10 | M010 `accepted_by_requested_gates` Misread When Quality Skipped | Critical | Allowed smoke or metrics-only runs to appear accepted by construction. |
| 11 | M011 Direct Backend Quality Did Not Match Frontdoor | High | Confused wrapper/template mismatch with model/runtime quality. |
| 12 | M012 Long-Context And Repeat Stability Not Required Together | Critical | Let candidates pass one quality dimension while failing another. |
| 13 | M013 Repetitive Concurrency Benchmarks Over-Interpreted | High | Overstated n-gram/spec benefit on proposer-friendly prompts. |
| 14 | M014 Smoke Tests Carried Too Much Weight | High | Collapsed loadability/readiness into correctness or speed evidence. |
| 15 | M015 Post-Device-Lost Runs Used Before Clean Control | Critical | Risked accepting or rejecting candidates based on damaged runtime state. |
| 16 | M016 Graph Replay Corruption Treated Like Output Formatting | Critical | Delayed the true replay/logit/state root-cause investigation. |
| 17 | M017 Runtime Recapture Treated As Fix | Critical | Could have promoted a diagnostic that only masked stale graph state. |
| 18 | M018 CUDA Remedies Tried Without XPU Failure Proof | High | Led to broad toggles before first-divergence evidence. |
| 19 | M019 Graph0 Output 5 Clone Too Narrow | High | Overfit a partial alias symptom and missed broader stale-state class. |
| 20 | M020 Medium-Clean Pool Toggles Not Deep-Clean | Critical | Medium gates repeatedly missed the known deep failure window. |
| 21 | M021 Static Input Copy Found Late | High | The most relevant alias fix came after many lower-signal toggles. |
| 22 | M022 Reduced Graph Reproducer Lagged Endpoint Debug | High | Kept iteration slow and increased device-loss exposure. |
| 23 | M023 Speed Work Stacked On Corrupt Graph Base | Critical | Made later candidate failures ambiguous and wasted optimization time. |
| 24 | M024 Stock Copy-Inputs Failure Not Turned Into Minimal XPU Copy | High | Delayed the likely production fix for piece boundary aliasing. |
| 25 | M025 Native GDN Decode Treated As Independent Root Cause | High | Sent work into GDN math before graph/state boundary was solved. |
| 26 | M026 GDN Fallback Modes Polluted Identity | High | Made correctness and speed comparisons fragile across fallback strings. |
| 27 | M027 Mixed Spec Decode Reclassified Ordinary Decode As Prefill | Critical | Caused a real crash class and showed scheduler metadata was unsafe. |
| 28 | M028 Full Serial GDN Put Into Endpoint Too Early | High | Produced endpoint instability instead of bounded diagnostic evidence. |
| 29 | M029 Store-All GDN Diagnostic Too Heavy For Endpoint First | High | Caused device-lost before yielding targeted state evidence. |
| 30 | M030 Accepted Running GDN State Promotion Missing | Critical | Directly blocked spec parity through wrong speculative recurrent state. |
| 31 | M031 Bonus-KV Bug Framed Backwards | Critical | Chased a false missing-commit bug induced by diagnostics. |
| 32 | M032 Suppressed Bonus Flags Created The Failure | Critical | Root-cause trace behavior was changed by the very flags under test. |
| 33 | M033 No-Bonus Workarounds Chased Symptoms | Critical | Avoided visible bad tokens while leaving scheduler/KV transactions broken. |
| 34 | M034 Oracle Trace Joins Initially Too Weak | High | Made spec evidence ambiguous until request and response IDs were joined. |
| 35 | M035 Spec Divergence Attributed To Draft Quality | High | Misfocused on proposer quality despite verifier-bonus/replacement roles. |
| 36 | M036 MTP Hybrid Too Heavy For Claimed Speed Path | High | Confused acceptance potential with usable throughput. |
| 37 | M037 N-Gram Spec Tested On Too Favorable Distribution | High | Overvalued prompt-lookup speculation on repetitive prompts. |
| 38 | M038 ReplaySSM Profile Collected Before Integration Ready | High | Risked treating integration diagnostics as performance evidence. |
| 39 | M039 EAGLE Data Generation Not Performance Evidence | High | TP2 graph-none export could be mistaken for TP4 deployment readiness. |
| 40 | M040 Hidden-State Dataset Needed Self-Consistency Gate | Critical | Bad EAGLE labels would poison training and acceptance conclusions. |
| 41 | M041 EAGLE Needed Quark INT8 Target States | Critical | Training on the wrong target distribution would invalidate draft acceptance. |
| 42 | M042 Random/One-Sample EAGLE Smoke Over-Read | High | Load/format smokes could be mistaken for draft viability. |
| 43 | M043 TP4 Dump Device-Lost Misclassified Risk | Material | Prevented discarding exporter code for unrelated startup failure. |
| 44 | M044 Draft Checkpoint Sharing Needed Explicit Validation | High | Silent tokenizer/embed/lm_head mismatch would corrupt draft integration. |
| 45 | M045 EAGLE Corpus Too Small/Untied To Deployment | High | Early tiny corpora could not support general acceptance claims. |
| 46 | M046 Offline/Synthetic EAGLE Acceptance Not End-To-End Evidence | Critical | Synthetic or teacher-forced numbers could create false >150 claims. |
| 47 | M047 Synthetic Layerlet Parity Was Blind | Critical | The harness compared equivalent paths and could miss real MoE corruption. |
| 48 | M048 Offset Tensor Conventions Mixed | Critical | `[N]` versus `[N+1]` offsets can deterministically shift experts or read OOB. |
| 49 | M049 Mixed Workspace Ownership Looked In Wrong Tree | High | Kernel-only rebuilds could not fix vLLM-owned workspace behavior. |
| 50 | M050 Sparse Decode Tile Policy Not Tested With Real Skew | High | Balanced tests missed decode top-k sparse-routing corner cases. |
| 51 | M051 Prologue Bisection Continued After Systemic Evidence | High | Continued per-layer search after failure site proved broader capture issue. |
| 52 | M052 Reduced Prologue Repros Missing Endpoint State | High | Passing repros lacked the full-vLLM state needed to fail like production. |
| 53 | M053 oneDNN Sidecar Timings Included Diagnostics | High | Exactness logs could be misread as steady-state timing. |
| 54 | M054 Sidecar Builds Used Wrong SYCL Runtime | High | ABI/runtime mismatch blocked valid MoE sidecar conclusions. |
| 55 | M055 Standalone oneDNN Engine Failure Over-Broad | Material | Could have falsely rejected endpoint-context sidecar execution. |
| 56 | M056 Fused-Act-Quant Blamed At Wrong Layer | High | Correct kernel math was targeted while path composition/replay was the issue. |
| 57 | M057 Shared-Expert Aux Streams Hit XPU Graph Limits | High | Runtime capture limitations, not math, blocked the overlap path. |
| 58 | M058 Output Tail Cleanup Overvalued As 2x Lever | High | Directed attention to millisecond-scale gap with microsecond-scale evidence. |
| 59 | M059 `_to_list` Materialization Visible Too Late | High | A major no-async overhead slice was identified after other lower-value work. |
| 60 | M060 Async Blamed Broadly Instead Of Async Plus PIECEWISE | Critical | Could have disabled async unnecessarily instead of fixing replay interaction. |
| 61 | M061 Fences/Clones Treated As Likely Async Fixes | High | Repeated superficial fixes failed at same visible prefix. |
| 62 | M062 Periodic Eager Decode Correct But Not Speed Fix | High | Correctness workaround regressed speed and should remain control-only. |
| 63 | M063 Broad Metadata Copy Skip Removed Live State | Critical | Caused liveness failure by treating live scheduler metadata as steady state. |
| 64 | M064 Two-Copy Metadata Skip Failed Known-Good Lane | Critical | Short EE8 pass hid JSON failure on the real baseline. |
| 65 | M065 GPU-Side `num_computed_tokens` Violated Assumptions | Critical | Broke JSON and showed scheduler visibility/order assumptions were hidden. |
| 66 | M066 Sampler Shortcuts Repeated After Failure Class Clear | High | Continued corrupt fast sampler variants without new first-divergence evidence. |
| 67 | M067 `contiguous()` Removal Judged By Speed First | High | Memory-layout shortcut produced semantic wrong answers. |
| 68 | M068 Sampled-Token Broadcast Tried As Repair Too Early | High | Endpoint device-lost from unproven sampler communication path. |
| 69 | M069 Unsafe Diagnostics Beside Production Backend | Critical | Caused or risked user-facing device-lost/service failures. |
| 70 | M070 `/health` Treated As Sufficient Restore Evidence | Critical | Backend could be healthy yet fail first generation. |
| 71 | M071 Device-Lost Incidents Mixed With Speed Evidence | Critical | Contaminated performance conclusions with runtime failure state. |
| 72 | M072 Stale Worker Cleanup Manual Instead Of Gated | High | Orphaned workers could contaminate subsequent GPU runs. |
| 73 | M073 XCCL Interface Drift Missing From Identity | High | Post-reset interface changes caused startup/preflight confusion. |
| 74 | M074 Stale SYCL Build Artifacts Blocked Screens | High | Old ABI artifacts created false runtime failures. |
| 75 | M075 Full Build Used For Small Kernel Iteration | Material | Slowed kernel iteration and exposed unrelated build failures. |
| 76 | M076 oneAPI `setvars.sh` Library Precedence Hidden | High | Library drift could destabilize XCCL or native extensions. |
| 77 | M077 SYCL Persistent Cache Segfault Not Preflighted | High | Draft/spec load failed before model evidence due to cache/runtime issue. |
| 78 | M078 Fresh Compile/Relaunch Loops Treated Normal | High | Runtime stress was not separated from production-like steady state. |
| 79 | M079 Cache Root Provenance Not Strong Enough | Critical | Stale cache roots can produce fast but wrong outputs. |
| 80 | M080 Direct MiniMax Flag Ports Retried After Qwen Rejects | Material | Burned time on non-transferable scheduler knobs. |
| 81 | M081 More Cards Assumed Better For C1 | High | Ignored prior evidence that fewer cards can beat four for latency. |
| 82 | M082 MiniMax Local-Argmax Lessons Over-Transferred | High | Ported sampler lessons into Qwen despite different corruption behavior. |
| 83 | M083 Structured Fast Lanes Not Separate Enough | High | Could inflate general chat claims with constrained-output speeds. |
| 84 | M084 Collective Timing Came After Generic Toggles | High | Generic allreduce work preceded site-labeled evidence. |
| 85 | M085 Display/Host Isolation Not Recorded | Material | Leaves unexplained multi-B70 variance in public-quality results. |
| 86 | M086 Attention/KV Placement Assumed Correct | Material | Hidden CPU staging would be missed while tuning kernels. |
| 87 | M087 Sub-1 Tok/S Deltas Chased Without Adjacent A/B | Material | Consumed effort on noise-scale changes. |
| 88 | M088 Public Benchmark Discipline Lagged Discovery | Critical | Risked public rows from diagnostic or under-gated endpoints. |
| 89 | M089 MoE Output Collective Not Folded Into Layerlet Early | High | Limited non-spec MoE ceiling by leaving a host-visible boundary. |
| 90 | M090 Hot-Expert Table Size Over-Tested | Material | Focused on table size when dispatch was the larger issue. |
| 91 | M091 Rank Route Skew Ruled Out But Rank Variance Needed Probe | Material | Required a different rank/device variance investigation. |
| 92 | M092 Prologue Device-Lost Treated Like Layer Math | High | Actual failure site was graph/capture machinery, not MoE math. |
| 93 | M093 No-Chunked-Prefill N-Gram Rejected By Config | Material | Invalid config reject was not model/runtime proof. |
| 94 | M094 Async Disabled By Spec Without Aggregate Revalidation | High | C1 wins could degrade serving throughput. |
| 95 | M095 Thinking Text Failures Mixed With Token Drift | High | Blurred wrapper errors and true runtime corruption. |
| 96 | M096 Frontdoor `OK` Smoke Not Enough For Long Decode | High | Restore looked ready without proving decode stability. |
| 97 | M097 Runtime Stack Upgrades Lacked Inventory Gate | High | Stack bakeoffs would be invalid without complete provenance. |
| 98 | M098 Upstream Delta Delayed By Local Rabbit Holes | High | Potential low-risk baseline gains were postponed. |
| 99 | M099 Diagnostic Flag Rationale Not Recorded | High | Stale flags contaminated later evidence and root-cause traces. |
| 100 | M100 Research Ledger Too Distributed | High | Distributed notes made repeated mistakes and missed corrections likely. |

## Counts

- Critical: 30
- High: 60
- Material: 10
- Significant total: 100
