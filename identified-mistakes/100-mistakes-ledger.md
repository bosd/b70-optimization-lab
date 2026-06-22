# 100 Identified Research Mistakes

Scope: Qwen 3.6 35B / MiniMax-related Intel XPU optimization work visible under `/home/steve`, with emphasis on the last several weeks of Qwen work. This is a mistake ledger, not a promotion document. Each entry records what went wrong, where the evidence is, how to fix the process or implementation, and what different outcome the fix could have enabled.

## M001 - Missing PIECEWISE Was Treated As A Performance Regression

- What went wrong: a run without `COMPILATION_CONFIG='{"cudagraph_mode":"PIECEWISE"}'` defaulted to graph-none, measured around 15 tok/s, and was compared against the fast forced-comm PIECEWISE lane.
- Evidence: `/home/steve/AGENTS.md`; `/home/steve/llm-optimizations/AGENTS.md`; `/home/steve/llm-optimizations/notes/2026-06-16-qwen36-current-handoff.md`.
- Fix: make launchers fail closed when Qwen benchmark identity omits graph mode, and always diff launcher logs before interpreting a speed shift.
- Related history: 2026-06-14 to 2026-06-16 Qwen fast-lane debugging.
- Different outcome: the team would not have spent cycles explaining a fake regression and could have stayed focused on graph replay correctness.

## M002 - Metrics-Only Fast Lane Was Described Like A Validated Lane

- What went wrong: `qwen36-ablation-fastlane-config-restored-control-metrics-summary-20260614h4.json` reported 93.45 tok/s, but JSON, color, and quality gates were skipped.
- Evidence: `/home/steve/llm-optimizations/data/qwen36-ablation-fastlane-config-restored-control-metrics-summary-20260614h4.json`; `/home/steve/suggestions.md`.
- Fix: require summary rows to label metrics-only artifacts as `speed-only` and block promotion wording when canaries are skipped.
- Related history: 2026-06-14 fast graph baseline.
- Different outcome: the 93 tok/s number would have stayed a diagnostic ceiling until quality caught up.

## M003 - Quality Suite Pass Was Allowed To Hide Repeat Canary Failure

- What went wrong: h20/h21 artifacts passed the quality suite but failed JSON and color repeat canaries, so the overall candidate was not acceptable.
- Evidence: `qwen36-ablation-fastlane-gdnmask-no-output-clone-promotion-summary-20260614h20.json`; `qwen36-ablation-fastlane-gdnmask-clone-output5-6-promotion-summary-20260614h21.json`.
- Fix: promotion must require metrics, JSON, color, quality, and baseline match together, not any one gate independently.
- Related history: 2026-06-14 graph replay corruption promotion attempts.
- Different outcome: the graph replay stale-state bug would have been treated as blocking immediately.

## M004 - Shallow Gates Were Treated As Equivalent To Promotion Gates

- What went wrong: short or shallow JSON/color checks passed on some 77-86 tok/s conservative lanes, but stronger 4-repeat promotion gates later failed in the same repeat windows as forced graph replay.
- Evidence: `/home/steve/suggestions.md`; `/home/steve/llm-optimizations/notes/2026-06-13-qwen36-decode-graph-replay-corruption.md`.
- Fix: record gate depth in every claim, for example `JSON 16`, `JSON 96`, `JSON 128`, and never shorten it in summaries.
- Related history: 2026-06-14 to 2026-06-15 fast conservative quality lanes.
- Different outcome: fewer false "quality-passed" interpretations and earlier focus on long-run replay nondeterminism.

## M005 - Localmaxxing Rows Were Used As Architecture Signals Without Enough Identity Separation

- What went wrong: public rows around 99-100 tok/s were useful, but they were sometimes discussed near current accepted lanes without fully separating quality, graph identity, and diagnostic flags.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-12-qwen36-next-bigger-bets.md`; `/home/steve/suggestions.md`.
- Fix: keep public rows in a separate table with `validated`, `diagnostic`, or `unvalidated` labels and complete identity fields.
- Related history: 2026-06-12 to 2026-06-20 planning.
- Different outcome: public benchmarks would guide direction without creating internal promotion pressure.

## M006 - Older Dirty Block-Table Speed Was Compared Against A Different Safe Base

- What went wrong: an older dirty block-table near-100 tok/s A/B was not comparable to the later validated 93.55 tok/s safe identity.
- Evidence: `/home/steve/suggestions.md`; dirty block-table notes in `/home/steve/llm-optimizations/data/qwen36-*dirty*` where present.
- Fix: rerun dirty block-table on the exact current identity before claiming a regression or a path to 100+.
- Related history: 2026-06-15 to 2026-06-16 dirty block-table follow-up.
- Different outcome: less confusion between stale unsafe wins and current safe baselines.

## M007 - TP2 And TP4 Results Were Too Easy To Cross-Compare

- What went wrong: TP2 and TP4 results appeared in the same planning discussions even though the current safe TP2 identity measured 85.87 tok/s and was slower than TP4.
- Evidence: `/home/steve/suggestions.md`; `/home/steve/llm-optimizations/notes/2026-06-16-qwen36-current-handoff.md`.
- Fix: include TP/PP and selected devices in every result title and filename where possible.
- Related history: 2026-06-15 TP2 rejection under current fast-safe identity.
- Different outcome: topology work would still be explored, but not mixed into single-lane speed claims.

## M008 - GPU Memory Utilization Was Not Treated As A First-Class Identity Field

- What went wrong: runs used `GPU_MEMORY_UTILIZATION=0.90`, `0.95`, `0.82`, and other values for different experiments, which affects capture sizes, KV headroom, and stability.
- Evidence: `/home/steve/AGENTS.md`; `/home/steve/llm-optimizations/notes/2026-06-16-qwen36-current-handoff.md`; summary JSON `env` sections.
- Fix: make the ablation report show GPU memory utilization in the headline identity block.
- Related history: Qwen graph and EAGLE data experiments across June 2026.
- Different outcome: fewer accidental apples-to-oranges comparisons and fewer unexplained OOM/device-lost differences.

## M009 - Diagnostic Flags Were Missing From Some Early Summaries

- What went wrong: skip/include layer gates for fused prologue were only later added to summary JSON and log echo, so earlier runs were harder to audit.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-16-qwen36-current-handoff.md`, 2026-06-17 addendum.
- Fix: every environment variable that changes behavior must be echoed into the artifact before the server launches.
- Related history: 2026-06-16 to 2026-06-17 fused prologue bisection.
- Different outcome: less time reconstructing which layers were enabled in failed capture tests.

## M010 - `accepted_by_requested_gates` Could Be Misread When Quality Was Skipped

- What went wrong: some summaries show `accepted_by_requested_gates: true` when the requested run did not include a full quality suite, for example fastgraph exact layerlet smoke.
- Evidence: `qwen36-ablation-fastgraph-exact-layerlet-smoke-summary-20260615a4.json`.
- Fix: separate `accepted_by_requested_gates` from `promotion_eligible`, and make promotion require a fixed gate set.
- Related history: 2026-06-15 layerlet smoke.
- Different outcome: smoke-clean but slower or incomplete candidates would not look promotable.

## M011 - Direct Backend Quality Was Tested Without Matching Frontdoor Behavior

- What went wrong: direct backend quality for Qwen sometimes emitted thinking text because it did not use the LAN frontdoor `enable_thinking=false` override.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-10-qwen36-ngram-cg128-single-win-quality-pass-concurrency-fail.md`.
- Fix: quality comparisons must either go through the frontdoor or explicitly replicate the chat-template kwargs.
- Related history: 2026-06-10 n-gram CG128 testing.
- Different outcome: quality failures would be attributed to model behavior or wrapper mismatch correctly.

## M012 - Long-Context And Repeat Stability Were Not Always Required Together

- What went wrong: the n-gram scheduler guard failed long-context once and repeat stability on rerun, showing either test alone was insufficient.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-10-qwen36-ngram-scheduler-guard-rejected.md`.
- Fix: gate candidates on exact, JSON, repeat, color, and long-context in the same promotion bundle.
- Related history: 2026-06-10 guarded n-gram candidate.
- Different outcome: rare wrong temperature-0 tokens would be caught before a speed result looked useful.

## M013 - Repetitive Concurrency Benchmarks Were Over-Interpreted

- What went wrong: c8 n-gram aggregate throughput looked excellent on repeated benchmark-token prompts, but this was an upper-bound reliability signal, not general throughput.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-10-qwen36-ngram-scheduler-guard-rejected.md`.
- Fix: label synthetic repetitive prompts as proposer-favorable and require diverse prompts before aggregate claims.
- Related history: 2026-06-10 n-gram c2/c8 reliability screens.
- Different outcome: speculation work would not be optimized toward an unrealistic prompt distribution.

## M014 - Smoke Tests Were Allowed To Carry Too Much Weight

- What went wrong: readiness, import, and short completion tests were sometimes discussed alongside performance gates, even when they only proved loading or wiring.
- Evidence: EAGLE loader smoke in `/home/steve/llm-optimizations/notes/2026-06-16-qwen36-current-handoff.md`; sidecar readiness in `/home/steve/llm-optimizations/notes/2026-06-13-qwen36-moe-sidecar-readiness.md`.
- Fix: name artifacts `smoke`, `load`, `readiness`, `metrics`, or `promotion` and never collapse those states in summaries.
- Related history: 2026-06-13 sidecar and 2026-06-18 EAGLE work.
- Different outcome: clearer sequencing from loadability to correctness to speed.

## M015 - Post-Device-Lost Runs Were Sometimes Treated As Evidence Before A Clean Control

- What went wrong: after a device reset/coredump, follow-up candidate runs failed or behaved differently; those results were invalid until a matched control passed.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-21-qwen36-phase3-copy-skip.md`.
- Fix: require a clean adjacent no-change control after any Level Zero device-lost before accepting candidate evidence.
- Related history: 2026-06-21 metadata copy skip and GPU num-computed tests.
- Different outcome: fewer false rejections or false failures caused by a damaged runtime state.

## M016 - Graph Replay Corruption Was Initially Treated Like Output Formatting

- What went wrong: output copy, SSE, detokenization, and formatting were investigated even though raw `/v1/completions` and logprob NaN evidence pointed below the wrapper.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-13-qwen36-decode-graph-replay-corruption.md`.
- Fix: when raw completions reproduce corruption, pivot immediately to logits/hidden-state/replay state, not response formatting.
- Related history: 2026-06-13 graph replay boundary.
- Different outcome: faster isolation of graph-owned stale state and less time on non-root-cause output paths.

## M017 - Runtime Recapture Was A Diagnostic, Not A Fix

- What went wrong: recapture made some canaries pass, but it re-anchored graph state and collapsed or perturbed the fast path, so it was not promotable.
- Evidence: `/home/steve/suggestions.md`; `/home/steve/llm-optimizations/notes/2026-06-13-qwen36-decode-graph-replay-corruption.md`.
- Fix: use recapture only to prove stale/aliased graph state, then identify and refresh the specific buffer.
- Related history: 2026-06-13 to 2026-06-15 P0a debugging.
- Different outcome: effort would focus on targeted static input copy or pool isolation instead of periodic recapture.

## M018 - CUDA-Issue Remedies Were Tried Without Proving They Matched XPU Failure

- What went wrong: `cudagraph_mark_step_begin`, strong outputs, and output cloning were plausible from upstream CUDA issues but did not solve the XPU PIECEWISE corruption.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-13-qwen36-decode-graph-replay-corruption.md`; `/home/steve/suggestions.md`.
- Fix: use CUDA issue analogies to form hypotheses, but require first-divergence tensor evidence before broad patching.
- Related history: 2026-06-13 replay corruption repairs.
- Different outcome: fewer broad toggles and quicker movement to XPU-specific graph pool/input aliasing.

## M019 - Cloning Graph0 Output 5 Was Too Narrow

- What went wrong: cloning graph0 output index 5 helped a standalone canary but failed deep gates after metrics warmup, showing a second alias or state path remained.
- Evidence: `/home/steve/suggestions.md`; h14/h15/h20/h21 summary artifacts.
- Fix: clone-based probes should be followed immediately by all-boundary alias tracing, not treated as a fix.
- Related history: 2026-06-14 h14 through h21 experiments.
- Different outcome: the team would not have chased partial output clone fixes for a multi-buffer stale-state problem.

## M020 - Medium-Clean Graph Pool Toggles Were Not Deep-Clean

- What went wrong: strong output and no-global-pool variants passed medium gates but failed deep JSON/color windows around repeat 49/138.
- Evidence: `/home/steve/suggestions.md`; `qwen36-ablation-p0a-strong-output-medium-gate-summary-20260615p0strong1.json`; `qwen36-ablation-p0a-strong-output-deep-gate-summary-20260615p0strong2.json`; `qwen36-ablation-p0a-no-global-pool-medium-gate-summary-20260615p0noglobal1.json`; `qwen36-ablation-p0a-no-global-pool-deep-gate-summary-20260615p0noglobal2.json`.
- Fix: require the deepest known failure windows for every graph-pool/lifetime candidate.
- Related history: 2026-06-15 P0a differential matrix.
- Different outcome: graph pool toggles would be discarded or refined earlier.

## M021 - Static Input Copy Was Found Late Relative To The Alias Evidence

- What went wrong: the eventual static-input copy lane for selected `piecewise:1/41` args `8,10` was the first deep-clean fast base, but the process spent many runs on less targeted pool/output toggles first.
- Evidence: `/home/steve/suggestions.md`.
- Fix: when piece boundary aliasing is suspected, prioritize minimal input decoupling at the boundary before pool-wide changes.
- Related history: 2026-06-15 P0a static copy discovery.
- Different outcome: a quality-safe 93 tok/s base could have arrived sooner.

## M022 - The Reduced Graph Reproducer Lagged The Endpoint Debug Loop

- What went wrong: endpoint restarts and long canary loops were used for many graph hypotheses before a compact reproducer existed.
- Evidence: `/home/steve/suggestions.md`; `/home/steve/llm-optimizations/notes/2026-06-16-qwen36-current-handoff.md`.
- Fix: create a seconds-scale `torch.xpu` graph reproducer as soon as replay-only corruption is localized.
- Related history: 2026-06-13 to 2026-06-16 P0a and prologue work.
- Different outcome: faster iteration and fewer device-lost endpoint cycles.

## M023 - More Speed Work Was Stacked On A Corrupt Graph Base

- What went wrong: MoE, sampler, and GDN speed ideas were tested while the underlying fast graph replay lane was known to corrupt under warm repeats.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-13-qwen36-decode-graph-replay-corruption.md`; `/home/steve/suggestions.md`.
- Fix: freeze stacking work until the base lane is deep-clean, or run every stack as a diagnostic-only branch.
- Related history: 2026-06-13 to 2026-06-15 fast graph era.
- Different outcome: fewer ambiguous failures where a candidate looked wrong because the base was already unstable.

## M024 - Stock `cudagraph_copy_inputs=true` Failure Was Not Immediately Turned Into A Minimal XPU Copy

- What went wrong: the stock copy-inputs path hit an XPU inductor bounds assert, but the direct fix should have been a reduced XPU-safe piecewise copy path.
- Evidence: `/home/steve/suggestions.md`.
- Fix: implement a minimal eager/device copy in the piecewise boundary path rather than relying on the stock compiled wrapper.
- Related history: 2026-06-15 P0a fix options.
- Different outcome: a robust production fix for the alias class may have replaced several fragile toggles.

## M025 - Native GDN Decode Was Treated As A Separate Root Cause Too Long

- What went wrong: native GDN decode and zero-fresh GDN variants looked fast in short metrics, but warm repeat canaries still failed. Later traces indicated this was another symptom of stale graph/state boundaries rather than an independent GDN math fix.
- Evidence: `/home/steve/suggestions.md`; `qwen36-ablation-native-gdn-syncdecode-json-repeat96-20260614c2.json`; `qwen36-ablation-native-gdn-layer0-3-summary-20260614c3.json`; `qwen36-ablation-fastlane-gdnmask-zero-fresh-promotion-summary-20260614h23.json`.
- Fix: classify native GDN failures by whether they disappear under graph-none or decode replay bypass before changing GDN kernels.
- Related history: 2026-06-14 to 2026-06-15 native GDN tests.
- Different outcome: less time spent treating GDN as the primary root cause before graph state was fixed.

## M026 - GDN Fallback Mode Changes Polluted Benchmark Identity

- What went wrong: `VLLM_XPU_GDN_NATIVE_FALLBACK` changed between decode, prefill, decode|prefill, and other variants, making speed and correctness comparisons fragile.
- Evidence: `/home/steve/AGENTS.md`; `/home/steve/llm-optimizations/notes/2026-06-16-qwen36-current-handoff.md`.
- Fix: include the exact GDN fallback string in every artifact title or summary headline.
- Related history: June 2026 Qwen GDN and graph experiments.
- Different outcome: fewer false conclusions about whether a speed change came from GDN or graph/copy changes.

## M027 - Mixed Spec Decode Reclassified Ordinary Decode As Prefill

- What went wrong: a step containing ordinary one-token decode plus speculative decode caused metadata to push the ordinary decode into a FLA chunk prefill path, crashing with Intel Triton `PassManager::run failed`.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-10-qwen36-ngram-cg128-single-win-quality-pass-concurrency-fail.md`.
- Fix: keep non-spec decode metadata as decode when spec rows are present, and test mixed prefill/decode/spec scheduling explicitly.
- Related history: 2026-06-10 n-gram CG128.
- Different outcome: the first n-gram c2 crash would have been understood as metadata classification, not generic speculation instability.

## M028 - Full Serial GDN Was Put Into The Endpoint Before A Tiny Repro Proved It Safe

- What went wrong: full serial GDN under PIECEWISE starved or timed out in shared-memory broadcast and required manual cleanup.
- Evidence: `/home/steve/suggestions.md`.
- Fix: run serial diagnostics in tiny eager-only parity repros and stop at first divergence before using the full graph endpoint.
- Related history: 2026-06-15 oracle k1 follow-up.
- Different outcome: fewer dead engine sessions and clearer GDN state evidence.

## M029 - Store-All GDN Speculative Diagnostics Were Too Heavy For Endpoint First

- What went wrong: the GDN speculative store-all diagnostic reached readiness but device-lost on the first trace request.
- Evidence: `/home/steve/suggestions.md`.
- Fix: stage store-all in a single-layer or single-request reproducer before full endpoint trace mode.
- Related history: 2026-06-16 speculative state debugging.
- Different outcome: avoided a device-lost cycle and produced more focused state evidence.

## M030 - Accepted Running GDN State Promotion Was Missing From Early Spec Attempts

- What went wrong: native XPU GDN prefill did not initially mirror running prefill state into speculative state slots, causing zero-state or wrong-base speculative rows.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-17-eagle-path-to-150-tok-s-plan.md`; `/home/steve/llm-optimizations/notes/2026-06-16-qwen36-current-handoff.md`.
- Fix: make state promotion an invariant in the spec transaction and test it with per-layer state traces.
- Related history: 2026-06-17 verifier repair.
- Different outcome: oracle parity work would have skipped several misleading state-copy attempts.

## M031 - The Bonus-KV Bug Was Framed Backwards

- What went wrong: the initial P0b framing said bonus KV was never committed, but later source review showed normal path commits it; the observed predecessor re-emission was diagnostic-flag-induced.
- Evidence: `/home/steve/suggestions.md`, R1 section.
- Fix: validate unsuppressed oracle k1 before adding workaround flags, and trace the original reason suppression was introduced.
- Related history: 2026-06-15 P0b correction.
- Different outcome: effort would shift from false missing-commit fixes to the actual verifier bonus state divergence.

## M032 - Suppressed Bonus Flags Created The Failure Being Debugged

- What went wrong: `VLLM_XPU_SPEC_DECODE_DISABLE_FULL_ACCEPT_BONUS=1` plus cache filtering uncommitted and dropped the bonus by design, then the trace was interpreted as a normal path bug.
- Evidence: `/home/steve/suggestions.md`; source references listed there to `scheduler.py` and `gpu_model_runner.py`.
- Fix: never use behavior-changing diagnostic flags in root-cause traces without marking the trace as synthetic.
- Related history: 2026-06-15 COW trace interpretation.
- Different outcome: fewer days chasing a self-inflicted trace artifact.

## M033 - No-Bonus Workarounds Chased Symptoms Instead Of The Transaction

- What went wrong: no-bonus and suppressed-replacement variants avoided one visible bad emission but exposed incomplete scheduler/worker/KV recovery transactions.
- Evidence: `/home/steve/suggestions.md`; `/home/steve/llm-optimizations/notes/2026-06-16-qwen36-current-handoff.md`.
- Fix: implement a transactional invariant covering scheduler counts, worker cache, KV commit state, and visible output.
- Related history: 2026-06-16 k2/k4 speculative work.
- Different outcome: spec decode could advance toward token identity rather than accumulating flags.

## M034 - Oracle Trace Joins Were Initially Too Weak

- What went wrong: replay/summarizer tooling needed to join by both request ID and response ID to avoid aliasing evidence.
- Evidence: `/home/steve/suggestions.md`, speculation status update.
- Fix: include stable request and response identifiers in every spec trace and summarizer.
- Related history: 2026-06-15 oracle k1 tracing.
- Different outcome: P0b evidence would be less ambiguous earlier.

## M035 - Spec Divergence Was Attributed To Draft Quality After Acceptance Was Already High

- What went wrong: unsuppressed oracle k1 had real speculative activity and high acceptance, but the mismatch roles were verifier bonus/replacement state, not proposer quality.
- Evidence: `/home/steve/suggestions.md`; `qwen36-oracle-graph-safe-k1-fixture-20260615graphsafe1.md`.
- Fix: classify every spec mismatch by role: accepted draft, replacement after reject, or verifier bonus after full accept.
- Related history: 2026-06-15 graph-safe oracle k1.
- Different outcome: more precise work on verifier state and less work on draft generation.

## M036 - MTP Hybrid Was Too Heavy For The Claimed Speed Path

- What went wrong: MTP hybrid showed acceptance potential but the draft cost was full MoE/GDN-like and slowed the endpoint instead of multiplying throughput.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-17-eagle-path-to-150-tok-s-plan.md`; `qwen36-ablation-tp4-mtp-k1-replayssm-prewarmed-summary-20260620194432.json`.
- Fix: separate draft-quality evidence from draft-cost evidence, and use thin EAGLE/DFlash drafts for throughput.
- Related history: 2026-06-17 to 2026-06-20 MTP/ReplaySSM work.
- Different outcome: speculation planning would target cheap trained drafts sooner.

## M037 - N-Gram Speculation Was Tested On Too Favorable A Distribution

- What went wrong: prompt-lookup n-gram looked good on repetitive prompts but had poor acceptance or quality on diverse/natural prompts.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-10-qwen36-ngram-scheduler-guard-rejected.md`; `/home/steve/llm-optimizations/notes/2026-06-17-eagle-path-to-150-tok-s-plan.md`.
- Fix: report acceptance by prompt class and require natural-chat acceptance before speed claims.
- Related history: 2026-06-10 n-gram and 2026-06-17 EAGLE decision.
- Different outcome: n-gram would be kept as harness plumbing, not as the main >150 path.

## M038 - ReplaySSM Profile Numbers Were Collected Before Integration Was Ready

- What went wrong: graphcaptured ReplaySSM profiling showed extremely slow runtime (`0.2377 tok/s` corrected in one artifact), dominated by draft/runtime overhead, yet still sat near performance planning.
- Evidence: `qwen36-replayssm-graphcaptured-profile-allranks-p64o4-run-summary-20260620191714.json`.
- Fix: treat ReplaySSM profile runs as integration diagnostics until canaries pass and per-step costs are in the expected range.
- Related history: 2026-06-20 ReplaySSM graph capture profile.
- Different outcome: performance work would wait for state lifecycle and warmup integration to be correct.

## M039 - EAGLE Data Generation Was Correctness Work, Not Performance Evidence

- What went wrong: TP2 graph-none hidden-state dumps succeeded under a different identity from the TP4 PIECEWISE target lane, so they proved data-export mechanics, not deployment performance or exact identity match.
- Evidence: `qwen36-eagle-hidden-dataset-smoke-tp2-20260618e-summary.json`; `qwen36-eagle-hidden-dump-pos-tp2-20260618a.log`; `qwen36-eagle-hidden-dump-expanded-tp2-20260618k.log`; `/home/steve/llm-optimizations/notes/2026-06-16-qwen36-current-handoff.md`.
- Fix: label hidden-state export artifacts as data-validity only and keep them out of speed tables.
- Related history: 2026-06-18 EAGLE data path.
- Different outcome: EAGLE work would progress cleanly through data, training, load, acceptance, then speed.

## M040 - The Hidden-State Dataset Needed A Self-Consistency Gate Up Front

- What went wrong: dataset summaries proved continuity and row counts, but did not always record the plan's required `lm_head(hidden_state)` argmax self-consistency against saved next-token labels.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-17-eagle-path-to-150-tok-s-plan.md`; `qwen36-eagle-hidden-dataset-corpus2-tp2-20260618a-summary.json`; `qwen36-eagle-hidden-dataset-expanded-tp2-20260618k-summary.json`; `/home/steve/llm-optimizations/scripts/train-qwen36-eagle1-draft.py`.
- Fix: write a dataset verifier that rejects any shard where hidden-state argmax or continuity fails.
- Related history: 2026-06-17 to 2026-06-18 EAGLE data design.
- Different outcome: avoids training a draft on subtly misaligned or non-target-equivalent states.

## M041 - EAGLE Had To Be Trained On The Quark INT8 Target, Not A Convenient Official Checkpoint

- What went wrong: an EAGLE draft trained on different hidden-state distributions, such as official FP8 or HF transformer states, would not match the production Quark W8A8 verifier.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-17-eagle-path-to-150-tok-s-plan.md`.
- Fix: always generate EAGLE training data from the exact vLLM Quark INT8 target identity.
- Related history: 2026-06-17 EAGLE architecture decision.
- Different outcome: higher acceptance and fewer verifier mismatch bugs.

## M042 - The Random EAGLE Smoke Checkpoint Proved Loading Only

- What went wrong: the smoke draft reached readiness and acceptance was 0%, which is expected for random weights. Separately, one-sample smoke training could report perfect top1 without proving generalization.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-16-qwen36-current-handoff.md`, 2026-06-18 EAGLE loader smoke; `qwen36-eagle-hidden-dataset-smoke-tp2-20260618e-summary.json`; `qwen36-eagle1-smoke-trained-20260618a/summary.json`.
- Fix: record loader smoke separately from trained-draft acceptance smoke.
- Related history: 2026-06-18 EAGLE-1 checkpoint load.
- Different outcome: avoids overvaluing infrastructure success as model success.

## M043 - TP4 Data Dump Device-Lost Was Not Equivalent To Dump Code Failure

- What went wrong: TP4 graph-none dump startup device-lost while creating an attention quant scale tensor before dump code ran, so the dump path itself was not disproven.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-16-qwen36-current-handoff.md`, TP4 dump smoke section.
- Fix: separate pre-dump startup failures from exporter failures in notes and summaries.
- Related history: 2026-06-18 EAGLE hidden dump smoke.
- Different outcome: avoids discarding the exporter because of unrelated runtime startup instability.

## M044 - Draft Checkpoint Sharing Was A Compatibility Risk That Needed Explicit Validation

- What went wrong: the EAGLE smoke intentionally omitted `embed_tokens` and `lm_head` for target sharing, which would be a serious mismatch if vLLM did not detect it correctly.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-16-qwen36-current-handoff.md`.
- Fix: keep the loader log checks for shared embedding and lm_head as mandatory in every draft smoke.
- Related history: 2026-06-18 EAGLE loader.
- Different outcome: catches silent draft-target vocabulary or head mismatches before training.

## M045 - EAGLE Corpus Assumptions Were Not Yet Tied To Deployment Distribution

- What went wrong: the plan called for roughly 10k-50k samples, but early datasets were tiny and not yet tied to the deployment distribution.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-17-eagle-path-to-150-tok-s-plan.md`; `qwen36-eagle-hidden-dataset-corpus-tp2-20260618a-summary.json`; `qwen36-eagle-hidden-dataset-corpus2-tp2-20260618a-summary.json`; `/home/steve/llm-optimizations/scripts/collect-qwen36-eagle-hidden-corpus.py`.
- Fix: define target prompt classes and acceptance goals, then build a train/eval corpus at planned scale before selecting a checkpoint.
- Related history: 2026-06-17 EAGLE plan.
- Different outcome: trained draft acceptance would improve on real workloads instead of benchmark-friendly samples.

## M046 - EAGLE Acceptance Was Not Yet End-To-End Speed Evidence

- What went wrong: teacher-forced top1, offline acceptance, and synthetic acceptance ceilings were tempting but did not prove live endpoint acceptance, quality, or speed.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-20-master-plan.md`; `/home/steve/llm-optimizations/notes/2026-06-17-eagle-path-to-150-tok-s-plan.md`; `/home/steve/llm-optimizations/scripts/evaluate-qwen36-eagle-draft-offline.py`; `qwen36-ablation-eagle2-tokenheavy-synthaccept4-piecewise-tp2-k3-ceiling-20260618h-summary-20260618h01.json`; `qwen36-ablation-eagle2-tokenheavy-synthaccept6-piecewise-tp2-k5-ceiling-20260618h-summary-20260618h02.json`.
- Fix: require server-side `SpecDecoding metrics`, real verifier acceptance, full canaries, and corrected tok/s before claiming EAGLE throughput.
- Related history: 2026-06-20 master plan.
- Different outcome: avoids a false >150 claim based on offline draft quality.

## M047 - Synthetic Layerlet Parity Was Blind

- What went wrong: layerlet-vs-offsets-reference compared the same three ops and therefore proved wiring, not real correctness against `ref_fused_moe` or rows-per-expert.
- Evidence: `/home/steve/suggestions.md`, R3 section.
- Fix: add a real-routing test with real per-expert scales, skewed routing, and zero-row experts against independent references.
- Related history: 2026-06-15 P1 layerlet review.
- Different outcome: endpoint layerlet failures would be found in harnesses instead of full server runs.

## M048 - Offset Tensor Conventions Were Mixed

- What went wrong: oneDNN code used `[N]` end-only offsets while cutlass/layerlet paths required `[N+1]` leading-zero offsets.
- Evidence: `/home/steve/suggestions.md`; `/home/steve/llm-optimizations/notes/2026-06-13-qwen36-moe-sidecar-readiness.md`.
- Fix: assert offset length, dtype, first zero, and final total rows at every bridge.
- Related history: 2026-06-13 to 2026-06-15 W8A8/oneDNN work.
- Different outcome: prevents deterministic expert shift or OOB reads in layerlet experiments.

## M049 - Mixed Workspace Ownership Was Looked For In The Wrong Tree

- What went wrong: `VLLM_XPU_INT8_MOE_MIXED_WORKSPACE` lives in vLLM `xpu_moe.py`, not in `vllm-xpu-kernels`, so kernel-only rebuilds could not address all workspace aliasing.
- Evidence: `/home/steve/suggestions.md`, R3 section.
- Fix: trace workspace and scratch ownership across Python and kernels before rebuilding.
- Related history: 2026-06-15 layerlet and workspace analysis.
- Different outcome: fewer rebuilds targeting code that did not own the behavior.

## M050 - Sparse Decode Tile Policy Was Not Tested With Real Skew

- What went wrong: `Total_M=1` and 256 experts can drive average rows per expert near zero, selecting a corner-case tile policy that synthetic balanced tests may miss.
- Evidence: `/home/steve/suggestions.md`, R3 section.
- Fix: include real skewed routing and zero-row expert cases in grouped-GEMM tests.
- Related history: 2026-06-15 W8A8 grouped GEMM review.
- Different outcome: catches performance and correctness cliffs before endpoint A/B.

## M051 - Prologue Capture Bisection Continued After Evidence Pointed To Systemic Failure

- What went wrong: once even enabling layers 38-39 failed at the same dummy sampler copy site, the problem was systemic to fused-prologue capture, not per-layer math.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-16-qwen36-current-handoff.md`, 2026-06-17 addendum.
- Fix: stop layer bisection when the same off-path failure site recurs with minimal enabled scope.
- Related history: 2026-06-16 to 2026-06-17 fused prologue.
- Different outcome: earlier pivot to graph/memory-manager state or persistent layerlet without captured prologue.

## M052 - Reduced Prologue Repros Were Missing Full Endpoint Capture State

- What went wrong: reduced prologue reproducer variants passed, but the full endpoint still device-lost during PIECEWISE c1 capture, showing the repro lacked the relevant full-vLLM graph context.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-16-qwen36-current-handoff.md`.
- Fix: enrich repros with surrounding endpoint capture, dummy sampler copies, graph pools, and full model memory-manager state.
- Related history: 2026-06-16 reduced prologue repro state.
- Different outcome: a reproducer would fail in the same way as the endpoint and guide a real fix.

## M053 - oneDNN Sidecar Timings Included Diagnostic Overhead

- What went wrong: one-shot sidecar logs included diagnostic clone/sync and setup effects, so they were exactness evidence but not steady-state layerlet timing.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-13-qwen36-moe-sidecar-readiness.md`.
- Fix: separate parity logging from timing A/B and measure diagnostic-off cached resident execution.
- Related history: 2026-06-13 oneDNN sidecar GEMM parity.
- Different outcome: avoids false pessimism or optimism about oneDNN sidecar speed.

## M054 - Sidecar Builds Used The Wrong SYCL Runtime Lane

- What went wrong: an earlier sidecar build linked against `libsycl.so.9` and failed in the accepted PyTorch/vLLM runtime lane that required SYCL 8 compatibility.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-13-qwen36-moe-sidecar-readiness.md`.
- Fix: build sidecar probes with the same oneAPI/SYCL lane as the accepted vLLM process and verify `ldd` under the launcher environment.
- Related history: 2026-06-13 oneDNN sidecar.
- Different outcome: less time lost to ABI/runtime failures unrelated to MoE math.

## M055 - Standalone oneDNN Engine Failure Was Over-Broad Evidence

- What went wrong: standalone import hit `bad engine kind`, but the normal vLLM endpoint context was the relevant environment for the sidecar.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-13-qwen36-moe-sidecar-readiness.md`.
- Fix: validate sidecar execute prototypes inside the normal vLLM process before rejecting engine compatibility.
- Related history: 2026-06-13 sidecar execute prototype.
- Different outcome: the endpoint-side GEMM1/GEMM2 parity checks would have happened sooner.

## M056 - Fused-Act-Quant Was Blamed At The Wrong Layer

- What went wrong: deep dive showed `silu_and_mul_quant_int8_xpu` was bit-exact; the endpoint path was slower and unstable because it swapped to a slower raw down projection and interacted with replay.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-16-qwen36-current-handoff.md`, 2026-06-17 addendum.
- Fix: isolate fused kernel math from full path performance before deciding which component is faulty.
- Related history: 2026-06-17 shared-expert fused-act-quant.
- Different outcome: avoids rewriting a correct kernel and redirects work to path composition and graph safety.

## M057 - Shared-Expert Aux Streams Were Tried Against XPU Graph Capture Limits

- What went wrong: aux-stream overlap failed because XPU graph capture cannot wait on the event type used, not because shared-expert math was wrong.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-16-qwen36-current-handoff.md`, shared-experts addendum.
- Fix: prove XPU graph-compatible stream/event semantics in a small capture test before endpoint overlap work.
- Related history: 2026-06-17 shared-expert stream attempt.
- Different outcome: less endpoint churn and a clearer runtime limitation report.

## M058 - Output Tail Cleanup Was Overvalued As A 2x Lever

- What went wrong: stream vs final-only showed tail/queue overhead around 0.012 ms, far too small to explain the 5 ms/token gap.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-12-qwen36-next-bigger-bets.md`.
- Fix: use timing magnitude cutoffs before investing in polish paths as major speed levers.
- Related history: 2026-06-12 bigger-bets plan.
- Different outcome: more effort would go to model_forward, MoE, graph replay, and spec.

## M059 - `_to_list` Materialization Became Visible Too Late

- What went wrong: later TP2 no-async timing showed `bookkeeping_to_list` around 4.62 ms, almost as large as forward, indicating sampled-token materialization deserved a focused exact path.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-16-qwen36-current-handoff.md`, 2026-06-19 update.
- Fix: add stage-boundary timing earlier and distinguish output formatting from sampled-token CPU materialization.
- Related history: 2026-06-19 output materialization trace.
- Different outcome: exact overlap/removal work could start earlier.

## M060 - Async Was Blamed Broadly Instead Of Async Plus PIECEWISE Replay

- What went wrong: graph-none async passed canaries, while async plus PIECEWISE replay failed repeatedly, so the bug was not async scheduling alone.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-16-qwen36-current-handoff.md`.
- Fix: always run the 2x2 matrix: async on/off and graph replay on/off.
- Related history: 2026-06-19 async isolation.
- Different outcome: async repair would target graph replay interaction instead of disabling async generally.

## M061 - Simple Fences And Sampled-ID Clones Were Treated As Likely Async Fixes

- What went wrong: sync before return, sync around replay, output-copy sync, and sampled-token clones all failed JSON in similar windows.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-16-qwen36-current-handoff.md`.
- Fix: after two fence/clone variants fail at the same visible prefix, stop and trace hidden state/logits.
- Related history: 2026-06-19 async isolation.
- Different outcome: fewer superficial async patches and faster first-divergence instrumentation.

## M062 - Periodic Full-Request Eager Decode Was Correct But Not A Speed Fix

- What went wrong: eager every 8 requests made async/PIECEWISE canaries pass, but measured about 83.35 tok/s, not a path above the safe baseline.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-16-qwen36-current-handoff.md`.
- Fix: record it as a reliability control, not as a speed candidate.
- Related history: 2026-06-19 async `N=8` workaround.
- Different outcome: avoids promoting correctness workarounds that regress speed.

## M063 - Broad Metadata Copy Skip Removed Live State

- What went wrong: skipping `query_start_loc` along with other metadata gave a small speed bump but hung during JSON canary with no generation progress.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-21-qwen36-phase3-copy-skip.md`.
- Fix: classify each metadata tensor as invariant, per-request, or per-step before skipping copies.
- Related history: 2026-06-21 EE8-B-skip.
- Different outcome: avoids liveness failures from treating live scheduler inputs as steady state.

## M064 - Two-Copy Metadata Skip Passed Short Gates But Failed The Known-Good Lane

- What went wrong: B2 skip passed short EE8 checks, but on the no-EE8 known-good baseline final96 JSON failed at repeat 12.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-21-qwen36-phase3-copy-skip.md`; `qwen36-ablation-tp4-baseline-verify-B2-skip-idxpos-final96-summary-20260621154414.json`.
- Fix: validate metadata optimizations on the known-good baseline lane, not only an already-compromised EE8 lane.
- Related history: 2026-06-21 B2 copy skip.
- Different outcome: quicker rejection of unsafe metadata skip.

## M065 - GPU-Side `num_computed_tokens` Update Violated Hidden Assumptions

- What went wrong: replacing the CPU tensor copy with GPU `add_(1)` failed JSON at repeat 12 and was slower, meaning the state update had ordering or semantic assumptions not captured by the shortcut.
- Evidence: `qwen36-ablation-tp4-numcomp-gpu-smoke16-summary-20260621155417.json`; `/home/steve/llm-optimizations/notes/2026-06-21-qwen36-phase3-copy-skip.md`.
- Fix: prove scheduler/worker visibility and ordering invariants before moving metadata updates device-side.
- Related history: 2026-06-21 GPU num-computed follow-up.
- Different outcome: prevents wrong JSON and wasted speed screens.

## M066 - Sampler Shortcuts Were Repeated After The Failure Class Was Clear

- What went wrong: local argmax, max, FP32 top-k shortcut, and synced top-k variants were faster or plausible but repeatedly failed JSON/color or device-lost.
- Evidence: `/home/steve/suggestions.md`; relevant `qwen36-*topk*`, `localargmax*`, and sampler summary artifacts.
- Fix: keep accepted `torch.topk` fallback until a first-divergence trace proves a new sampler-specific issue.
- Related history: 2026-06-13 to 2026-06-15 sampler work.
- Different outcome: fewer corrupt fast sampler variants.

## M067 - Removing `contiguous()` Was Judged By Speed Before Endpoint Correctness

- What went wrong: removing the GEMM2 activation contiguous handoff looked faster but JSON failed with a semantic wrong answer.
- Evidence: `/home/steve/suggestions.md`.
- Fix: require quick JSON/color canaries before celebrating any memory-layout speed win.
- Related history: 2026-06-15 layerlet/path optimization.
- Different outcome: avoids promoting memory-layout changes that alter downstream assumptions.

## M068 - Sampled-Token Broadcast Was Tried As A Correctness Repair Despite Device-Lost Risk

- What went wrong: TP sampled-token broadcast plus `xpu_topk_sync` reached readiness but device-lost on the first metrics request.
- Evidence: `/home/steve/suggestions.md`.
- Fix: isolate broadcast/token sync in a small TP reproducer before endpoint use.
- Related history: 2026-06-15 sampler sync attempts.
- Different outcome: avoids endpoint crashes from unproven sampler communication paths.

## M069 - Unsafe Diagnostics Ran Beside A Production-Candidate Backend

- What went wrong: rejected fused-kernel diagnostics and other unsafe screens were run while the accepted backend was serving or recoverable, contributing to external request device-lost incidents.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-10-qwen36-device-lost-restart.md`.
- Fix: stop the backend, isolate devices, and pause frontdoor routing before unsafe extension diagnostics.
- Related history: 2026-06-10 device-lost restart.
- Different outcome: fewer user-facing HTTP 500s and less runtime contamination.

## M070 - `/health` Was Treated As Sufficient Restore Evidence

- What went wrong: after restore, `/health` could pass while the first generation request still device-lost at `block_table.copy_to_gpu`.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-10-qwen36-device-lost-after-runtime-screens.md`.
- Fix: require a real backend completion and frontdoor chat smoke after every restore.
- Related history: 2026-06-10 post-runtime screen recovery.
- Different outcome: invalid restored baselines would be caught before more experiments.

## M071 - Device-Lost Incidents Were Mixed With Speed Evidence

- What went wrong: device-lost conditions occurred during rapid runtime screens; such incidents are reliability data, not normal steady-state performance data.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-10-qwen36-device-lost-after-runtime-screens.md`.
- Fix: log device-lost incidents separately and require a clean control before the next speed result.
- Related history: 2026-06-10 runtime screens.
- Different outcome: avoids attributing reset-state behavior to candidate code.

## M072 - Stale Worker Cleanup Was Manual Instead Of Gated

- What went wrong: several failures left orphaned or suspect vLLM workers that had to be killed manually before continuing.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-16-qwen36-current-handoff.md`; `/home/steve/llm-optimizations/notes/2026-06-21-qwen36-phase3-copy-skip.md`.
- Fix: add a preflight that checks and optionally refuses to launch when stale workers hold XPU devices.
- Related history: June 2026 device-lost and capture failures.
- Different outcome: cleaner experiments and fewer contaminated starts.

## M073 - XCCL Interface Drift After Reset Was Not In The Baseline Identity

- What went wrong: after reset, `eth1` no longer existed and all-reduce preflight required `FI_TCP_IFACE=eno1 CCL_KVS_IFACE=eno1`.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-21-qwen36-phase3-copy-skip.md`.
- Fix: include network interface and XCCL preflight output in the benchmark identity.
- Related history: 2026-06-21 post-reset launches.
- Different outcome: fewer mysterious all-reduce startup failures.

## M074 - Stale SYCL Build Artifacts Blocked Runtime Screens

- What went wrong: stale oneAPI 2026 build artifacts required `libsycl.so.9` and broke attempts that should have used the accepted SYCL 8 lane.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-10-qwen36-ngram1-holdprefill-rejected.md`; `/home/steve/llm-optimizations/notes/2026-06-13-qwen36-moe-sidecar-readiness.md`.
- Fix: clean build roots and verify linked SYCL libraries before endpoint tests.
- Related history: 2026-06-10 n-gram and 2026-06-13 sidecar work.
- Different outcome: fewer false startup failures from ABI mismatch.

## M075 - Full `setup.py build_ext --inplace` Was Used For Small Kernel Iteration

- What went wrong: `_C`-only edits dragged in unrelated attention and allocator builds, slowing or killing iteration.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-10-vllm-xpu-kernels-c-only-build.md`.
- Fix: use the validated targeted CMake `_C`-only build path for small fused-kernel work.
- Related history: 2026-06-10 RMS+INT8 fusion attempt.
- Different outcome: faster kernel experiments and fewer unrelated build failures.

## M076 - oneAPI `setvars.sh` Library Precedence Was A Hidden Variable

- What went wrong: old FP8 and sidecar notes warned that global oneAPI library precedence could destabilize XCCL or break vLLM imports, but this remained easy to reintroduce.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-13-experiment-coverage-audit.md`; `/home/steve/llm-optimizations/notes/2026-06-13-qwen36-moe-sidecar-readiness.md`.
- Fix: record `LD_LIBRARY_PATH`, active oneAPI vars, and `ldd` for promoted native-extension runs.
- Related history: Qwen FP8 lessons and 2026-06-13 sidecar.
- Different outcome: fewer runtime-only failures unrelated to code correctness.

## M077 - SYCL Persistent Cache Segfault Was Not Preflighted

- What went wrong: EAGLE load TP2 first hit a oneCCL/SYCL persistent-device-code-cache segfault and only succeeded after `SYCL_CACHE_PERSISTENT=0`.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-16-qwen36-current-handoff.md`, EAGLE loader smoke.
- Fix: make cache mode part of launch identity and preflight new draft/spec paths with persistent cache disabled if needed.
- Related history: 2026-06-18 EAGLE loader.
- Different outcome: fewer confusing early all-reduce/load failures.

## M078 - Rapid Fresh Compile/Relaunch Loops Were Treated Like Normal Steady State

- What went wrong: repeated graph compiles and relaunches stressed the Level Zero runtime and coincided with device-lost incidents.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-10-qwen36-device-lost-after-runtime-screens.md`.
- Fix: add cool-down, XPU copy smoke, and discovery checks between high-risk relaunches.
- Related history: 2026-06-10 runtime screens.
- Different outcome: cleaner separation between candidate bugs and runtime exhaustion.

## M079 - Cache Root Provenance Was Not Always Strong Enough

- What went wrong: MiniMax history showed stale cache roots could be fast but wrong; Qwen notes adopted provenance checks but not every claim carried cache-root hashes.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-13-minimax-m27-transfer-audit-for-qwen36.md`; `/home/steve/llm-optimizations/notes/2026-06-13-experiment-coverage-audit.md`.
- Fix: include cache root path and hash/provenance in every promotable summary.
- Related history: MiniMax transfer and Qwen public-row planning.
- Different outcome: fewer stale-cache false wins.

## M080 - Direct MiniMax Flag Ports Were Retried After Qwen Rejected Them

- What went wrong: `--block-size 256` and `--max-num-batched-tokens 512` were MiniMax wins but Qwen W8A8 rejected them for the current 32K/no-prefix endpoint.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-13-minimax-m27-transfer-audit-for-qwen36.md`.
- Fix: transfer methods and measurement patterns, not flags, unless Qwen-specific profiles justify reopening them.
- Related history: 2026-06-13 MiniMax transfer audit.
- Different outcome: less time spent on already rejected scheduler envelope ports.

## M081 - More Cards Were Assumed Better For C1 Latency

- What went wrong: older Qwen Q4 evidence showed TP3 beat TP4 for c1 latency, but Qwen35/36 work still often treated TP4 as the default optimum.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-13-experiment-coverage-audit.md`.
- Fix: run paired TP2/TP3/TP4 latency gates when collectives and narrow shards dominate.
- Related history: Qwen Q4/FP8 lessons applied to June Qwen W8A8.
- Different outcome: topology might uncover a lower-latency non-TP4 lane.

## M082 - MiniMax Local-Argmax Lessons Were Over-Transferred

- What went wrong: MiniMax had safe local-argmax/logits paths, but Qwen sampler shortcuts repeatedly corrupted or underperformed.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-13-experiment-coverage-audit.md`; `/home/steve/suggestions.md`.
- Fix: require Qwen-specific sampler first-divergence evidence before porting MiniMax logits tricks.
- Related history: 2026-06-13 MiniMax transfer and Qwen sampler attempts.
- Different outcome: fewer unsafe Qwen sampler optimizations.

## M083 - Structured-Output Fast Lanes Were Not Always Kept Separate Enough

- What went wrong: MiniMax regex/structured lanes are useful production patterns but not general chat decode numbers.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-13-minimax-m27-transfer-audit-for-qwen36.md`.
- Fix: maintain separate benchmark categories for free-form chat, strict JSON/schema, and regex-constrained tasks.
- Related history: MiniMax transfer audit and Qwen Localmaxxing planning.
- Different outcome: avoids inflated general performance claims.

## M084 - Site-Labeled Collective Timing Came After Many Generic Collective Toggles

- What went wrong: MiniMax succeeded by labeling collective sites first; Qwen tried several generic collective/allreduce toggles before a full call-site census.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-13-minimax-m27-transfer-audit-for-qwen36.md`; `/home/steve/llm-optimizations/notes/2026-06-13-experiment-coverage-audit.md`.
- Fix: log call site, layer, dtype, byte count, rank, and wait time before changing collective policy.
- Related history: June 2026 custom allreduce and MiniMax transfer.
- Different outcome: more targeted collective optimizations and fewer noisy toggles.

## M085 - Display/Host Isolation Was Not Recorded In Qwen Benchmarks

- What went wrong: MiniMax 32K results recorded display isolation, but Qwen promotion rules did not always require display attachment and power/runtime state.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-13-minimax-m27-transfer-audit-for-qwen36.md`.
- Fix: include display, power, driver, kernel, firmware, and active desktop use in Localmaxxing-worthy Qwen runs.
- Related history: MiniMax transfer audit.
- Different outcome: fewer unexplained variance sources in multi-B70 benchmarks.

## M086 - Attention/KV Placement Was Assumed Correct

- What went wrong: MiniMax GGUF work found placement mistakes; Qwen vLLM likely stays XPU-resident, but hidden CPU staging still needed explicit audit.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-13-minimax-m27-transfer-audit-for-qwen36.md`.
- Fix: add CPU staging and host transfer indicators for attention, KV, GDN, router, logits, and collectives to timing artifacts.
- Related history: 2026-06-13 transfer audit.
- Different outcome: catches any hidden fallback before chasing kernel micro-optimizations.

## M087 - Sub-1 Tok/S Deltas Were Sometimes Chased Without Adjacent A/B

- What went wrong: several candidates showed tiny deltas within likely noise or lower than the current baseline, yet still consumed follow-up time.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-13-experiment-coverage-audit.md`; exact SiLU-Q and graph-clone-off notes.
- Fix: require adjacent control/candidate repeats and minimum effect size before follow-up.
- Related history: June Qwen exact SiLU-Q, clone, and small-flag screens.
- Different outcome: more effort reserved for structural 5 ms/token gaps.

## M088 - Public Benchmark Submission Discipline Lagged Internal Discovery

- What went wrong: notes warn future Localmaxxing rows should include only accepted-quality endpoints, implying earlier public-facing rows risked blending diagnostic speed and validation status.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-13-minimax-m27-transfer-audit-for-qwen36.md`; `/home/steve/suggestions.md`.
- Fix: require the full promotion bundle before any public row.
- Related history: 2026-06-12 to 2026-06-13 public Qwen rows.
- Different outcome: fewer false public performance claims.

## M089 - MoE Output Collective Was Not Folded Into The Layerlet Plan Early Enough

- What went wrong: Qwen offset/active-offset work improved layer floor but did not absorb the output collective boundary, while MiniMax had shown boundary placement mattered.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-13-minimax-m27-transfer-audit-for-qwen36.md`; `/home/steve/llm-optimizations/notes/2026-06-13-qwen36-moe-sidecar-readiness.md`.
- Fix: design the persistent W8A8 layerlet around route, GEMM, gather/combine, and adjacent collective scheduling as one boundary.
- Related history: 2026-06-13 MoE layerlet planning.
- Different outcome: a non-speculative path with a higher ceiling than middle-only layerlet tests.

## M090 - Hot-Expert Table Size Was Over-Tested Relative To Dispatch Cost

- What went wrong: top128 and compact-active hotset probes did not move enough because table size alone was not the dominant c1 layerlet cost.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-12-qwen36-next-bigger-bets.md`.
- Fix: prioritize resident dispatch reduction and real route/gather/combine boundaries over table-size-only experiments.
- Related history: 2026-06-12 bigger-bets index.
- Different outcome: faster convergence on persistent MoE architecture or spec.

## M091 - Simple Rank Route Skew Was Ruled Out But Rank Variance Still Needed A Different Probe

- What went wrong: identical route counters across ranks ruled out simple route skew, but forward wait still varied by rank, requiring device/runtime variance probes.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-13-qwen36-moe-sidecar-readiness.md`.
- Fix: after route counters match, inspect rank/device wait, power, thermals, PCIe, and runtime queue state instead of more route kernels.
- Related history: 2026-06-13 rank route overlay.
- Different outcome: better explanation of rank variance without chasing wrong routing theories.

## M092 - Prologue Endpoint Device-Lost Was Initially Treated Like A Layer Math Problem

- What went wrong: prologue-only, synthetic op, and repeated single-rank captures passed; endpoint failure occurred at dummy sampler copy during PIECEWISE capture.
- Evidence: `/home/steve/suggestions.md`; `/home/steve/llm-optimizations/notes/2026-06-16-qwen36-current-handoff.md`.
- Fix: classify failures by the actual failing stack site before changing layer math.
- Related history: 2026-06-15 to 2026-06-17 prologue capture.
- Different outcome: faster pivot to full-vLLM graph/memory-manager interaction.

## M093 - No-Chunked-Prefill N-Gram Was Rejected By Config, Not By Model Behavior

- What went wrong: disabling chunked prefill for 32K required `max_num_batched_tokens >= max_model_len`; the startup reject did not prove the idea wrong, only invalid under that memory envelope.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-10-qwen36-ngram-cg128-single-win-quality-pass-concurrency-fail.md`.
- Fix: if revisiting, test a valid 32768 MBT or smaller context with explicit memory gate.
- Related history: 2026-06-10 n-gram no-chunk screen.
- Different outcome: clearer decision between memory cost and mixed prefill/spec reliability.

## M094 - Async Scheduling Was Disabled By Spec Without Revalidating Aggregate Tradeoffs

- What went wrong: n-gram speculation disables async scheduling, so single-request wins did not automatically imply aggregate serving wins.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-10-qwen36-ngram-cg128-single-win-quality-pass-concurrency-fail.md`.
- Fix: every spec candidate needs c1, c2, and c8 measurements on representative prompts after reliability passes.
- Related history: 2026-06-10 n-gram CG128.
- Different outcome: prevents a c1-only improvement from degrading real service throughput.

## M095 - Quality Failures With Thinking Text Were Not Always Separated From Core Token Drift

- What went wrong: some failures were wrapper/template mismatches while others were raw token corruption; grouping them obscured root cause.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-10-qwen36-ngram-cg128-single-win-quality-pass-concurrency-fail.md`; `/home/steve/llm-optimizations/notes/2026-06-13-qwen36-decode-graph-replay-corruption.md`.
- Fix: maintain separate labels for wrapper mismatch, raw completion mismatch, semantic wrong answer, and token/logit corruption.
- Related history: 2026-06-10 to 2026-06-13 quality investigations.
- Different outcome: faster routing of failures to chat-template, sampler, or graph-state owners.

## M096 - Frontdoor Exact-Smoke `OK` Was Not Enough For Long Responses

- What went wrong: `OK` smokes proved endpoint wiring but not long decode stability, repeat canaries, or 32K behavior.
- Evidence: restore notes in `/home/steve/llm-optimizations/notes/2026-06-10-qwen36-device-lost-after-runtime-screens.md`; quality gate notes elsewhere.
- Fix: after `OK`, run fixed JSON/color and at least one p512/o512 decode before calling a restore experiment-ready.
- Related history: 2026-06-10 accepted backend restores.
- Different outcome: catches decode-path corruption immediately after restore.

## M097 - Runtime Stack Upgrades Were Planned Without A First-Class Inventory Gate

- What went wrong: master plan considered runtime bakeoffs, but prior incidents showed stack inventory had to be captured before comparing speed or stability.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-20-master-plan.md`; runtime hygiene notes above.
- Fix: build and run an inventory script for kernel, xe, compute-runtime, IGC, GMM, oneAPI, PyTorch, Triton-XPU, vLLM, and kernels before every stack bakeoff.
- Related history: 2026-06-20 runtime/driver controlled bakeoff plan.
- Different outcome: stack changes could be evaluated without hidden library drift.

## M098 - Upstream Kernel Delta Work Was Delayed By Local Rabbit Holes

- What went wrong: the 2026-06-20 plan recognized upstream v0.1.10 and narrow PRs might raise the no-spec baseline by 10-30%, after days of local spec/MoE cascades.
- Evidence: `/home/steve/llm-optimizations/notes/2026-06-20-master-plan.md`.
- Fix: run upstream delta bakeoffs earlier when local work is repeatedly hitting runtime/capture walls.
- Related history: 2026-06-20 master plan.
- Different outcome: the baseline might have moved above 100 before layering speculation.

## M099 - We Did Not Always Record Why A Diagnostic Flag Was Introduced

- What went wrong: suppression flags, fallback flags, and guard flags later became confusing because the original failure they papered over was not always tied to the flag.
- Evidence: `/home/steve/suggestions.md`, R1 tasks; many `VLLM_XPU_*` guarded notes.
- Fix: every new diagnostic flag needs a comment and note entry: original failure, expected behavior change, and removal condition.
- Related history: June 2026 speculative and graph debugging.
- Different outcome: fewer stale flags contaminating later evidence.

## M100 - The Research Ledger Itself Was Too Distributed

- What went wrong: evidence was spread across `suggestions.md`, many notes, raw JSON summaries, logs, and patches, making it easy to repeat failed paths or miss process corrections.
- Evidence: `/home/steve/suggestions.md`; `/home/steve/llm-optimizations/notes/2026-06-13-experiment-coverage-audit.md`; `/home/steve/llm-optimizations/data`.
- Fix: keep a single mistakes-and-decisions index with exact artifact paths, status, and reopen conditions.
- Related history: the current 100-mistake audit.
- Different outcome: future agents can avoid already-known traps and spend more time on genuinely new fixes.
