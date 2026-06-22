# 100 Critical Mistakes Ledger

Stop condition: the parent agent has found and reviewed 100 total Critical mistakes.

Critical means the mistake directly risks at least one of:

- false public or internal performance claims;
- unsafe promotion of corrupt or under-gated output;
- a multi-day wrong-root-cause path;
- runtime, cache, graph, or environment contamination that invalidates benchmark identity.

Counting rule: `C001` through `C030` are the 30 entries already marked Critical in `100-significant-mistakes-ledger.md`. `C031` through `C100` are parent-selected Critical candidates from the six read-only subagent reports. Each row is counted once.

Subagent coverage used:

- Averroes: Qwen public/localmaxxing identity and submission rows, 18 candidates.
- Helmholtz: Qwen graph, replay, speculation, and tooling gates, 20 candidates.
- Maxwell: MiniMax public/submission/localmaxxing benchmark rows, 20 candidates.
- Zeno: MiniMax runtime, endpoint, service safety, and structured-output lanes, 20 candidates.
- Copernicus: environment, launcher, build, cache, and provenance, 19 candidates.
- Kuhn: git, docs, and late-correction history, 20 candidates.

| ID | Severity | Mistake | Evidence anchor | Parent critical determination |
|---|---|---|---|---|
| C001 | Critical | M001 - Missing PIECEWISE treated as a performance regression | `100-mistakes-ledger.md` M001; `qwen36-fastlane-config-drift.md` | Compared graph-none `~15 tok/s` against forced-comm PIECEWISE `~93 tok/s`, creating a false regression story. |
| C002 | Critical | M002 - Metrics-only fast lane described like a validated lane | `100-mistakes-ledger.md` M002 | A 93 tok/s artifact with skipped canaries could be mistaken for a promotable lane. |
| C003 | Critical | M003 - Quality suite pass hid repeat canary failure | `100-mistakes-ledger.md` M003 | One quality gate hid deterministic repeat corruption. |
| C004 | Critical | M004 - Shallow gates treated as promotion gates | `100-mistakes-ledger.md` M004 | Short JSON/color passes created false quality confidence for graph replay lanes. |
| C005 | Critical | M010 - `accepted_by_requested_gates` misread when quality skipped | `100-mistakes-ledger.md` M010 | Smoke or metrics-only success could read as acceptance. |
| C006 | Critical | M012 - Long-context and repeat stability not required together | `100-mistakes-ledger.md` M012 | Candidates could pass one correctness dimension while failing another. |
| C007 | Critical | M015 - Post-device-lost runs used before clean control | `100-mistakes-ledger.md` M015 | Damaged runtime state can invalidate the next speed or quality result. |
| C008 | Critical | M016 - Graph replay corruption treated like output formatting | `100-mistakes-ledger.md` M016 | Delayed root-cause work on stale replay/logit state. |
| C009 | Critical | M017 - Runtime recapture treated as a fix | `100-mistakes-ledger.md` M017 | A diagnostic recapture could mask stale graph state while hurting the fast path. |
| C010 | Critical | M020 - Medium-clean pool toggles not deep-clean | `100-mistakes-ledger.md` M020 | Medium gates missed known deep failure windows. |
| C011 | Critical | M023 - Speed work stacked on a corrupt graph base | `100-mistakes-ledger.md` M023 | Later candidate failures became ambiguous because the base was already unsafe. |
| C012 | Critical | M027 - Mixed spec decode reclassified ordinary decode as prefill | `100-mistakes-ledger.md` M027 | Scheduler metadata corruption caused real crash behavior. |
| C013 | Critical | M030 - Accepted running GDN state promotion missing | `100-mistakes-ledger.md` M030 | Spec parity was blocked by wrong recurrent state promotion. |
| C014 | Critical | M031 - Bonus-KV bug framed backwards | `100-mistakes-ledger.md` M031 | Debugging targeted a self-induced missing-commit story. |
| C015 | Critical | M032 - Suppressed bonus flags created the failure | `100-mistakes-ledger.md` M032 | Behavior-changing diagnostics altered the root-cause trace. |
| C016 | Critical | M033 - No-bonus workarounds chased symptoms | `100-mistakes-ledger.md` M033 | Visible bad tokens were hidden while scheduler/KV transactions stayed broken. |
| C017 | Critical | M040 - Hidden-state dataset needed self-consistency gate | `100-mistakes-ledger.md` M040 | Bad EAGLE labels could poison training and acceptance conclusions. |
| C018 | Critical | M041 - EAGLE needed Quark INT8 target states | `100-mistakes-ledger.md` M041 | Training on the wrong target distribution invalidates draft acceptance. |
| C019 | Critical | M046 - Offline or synthetic EAGLE acceptance treated as end-to-end evidence | `100-mistakes-ledger.md` M046 | Teacher-forced acceptance could create false speed claims. |
| C020 | Critical | M047 - Synthetic layerlet parity was blind | `100-mistakes-ledger.md` M047 | Equivalent-path tests could miss real MoE corruption. |
| C021 | Critical | M048 - Offset tensor conventions mixed | `100-mistakes-ledger.md` M048 | `[N]` vs `[N+1]` offsets can shift experts or read out of bounds. |
| C022 | Critical | M060 - Async blamed broadly instead of async plus PIECEWISE replay | `100-mistakes-ledger.md` M060 | Could disable async unnecessarily instead of fixing replay interaction. |
| C023 | Critical | M063 - Broad metadata copy skip removed live state | `100-mistakes-ledger.md` M063 | Live scheduler metadata was treated as invariant, causing liveness failure. |
| C024 | Critical | M064 - Two-copy metadata skip failed known-good lane | `100-mistakes-ledger.md` M064 | Short EE8 pass hid JSON failure on the real baseline. |
| C025 | Critical | M065 - GPU-side `num_computed_tokens` violated assumptions | `100-mistakes-ledger.md` M065 | Scheduler visibility and ordering assumptions were broken. |
| C026 | Critical | M069 - Unsafe diagnostics beside production backend | `100-mistakes-ledger.md` M069 | Diagnostics risked or caused user-facing device-lost/service failures. |
| C027 | Critical | M070 - `/health` treated as sufficient restore evidence | `100-mistakes-ledger.md` M070 | Health could pass while first real generation still device-lost. |
| C028 | Critical | M071 - Device-lost incidents mixed with speed evidence | `100-mistakes-ledger.md` M071 | Runtime failure state contaminated performance conclusions. |
| C029 | Critical | M079 - Cache root provenance not strong enough | `100-mistakes-ledger.md` M079 | Stale graph/AOT caches can produce fast but wrong outputs. |
| C030 | Critical | M088 - Public benchmark discipline lagged discovery | `100-mistakes-ledger.md` M088 | Diagnostic or under-gated endpoints could leak into public rows. |
| C031 | Critical | Public base-model row ran the quantized W8A8 snapshot | `localmaxxing-qwen36-b70-w8a8-response-20260611.json:24`; `:77` | Public model identity said base Qwen while command used Quark W8A8 INT8. |
| C032 | Critical | Same W8A8 endpoint occupied two public ranks | `localmaxxing-b70-qwen-leaderboard-20260612cg.json:1` | Duplicate public rows can inflate ranking and performance claims. |
| C033 | Critical | Public row lost fast-lane environment identity | `localmaxxing-qwen36-b70-w8a8-response-20260611.json:77`; `localmaxxing-qwen36-quark-w8a8-int8-tp4-noprefix-p512n512-20260611.response.json:77` | Missing fast-lane flags make the row non-reproducible. |
| C034 | Critical | W8A8 row served under an FP8 name | Qwen public response command snippets at line 77 | Quantization identity drift makes published comparisons false. |
| C035 | Critical | Base row marked an A3B MoE run as non-MoE | `localmaxxing-qwen36-b70-w8a8-response-20260611.json:30`; Quark response line 30 | Dense-vs-MoE comparisons become wrong. |
| C036 | Critical | Quality gates claimed without artifact identity | `localmaxxing-qwen36-b70-w8a8-submission-20260611.json:23`; response line 18 | Quality could be attached from a different benchmark identity. |
| C037 | Critical | Incompatible VRAM evidence attached to same run family | Quark response lines 17-18; base response line 17 | Public speed/resource claims use different measurement modes. |
| C038 | Critical | `tokSTotal` disappeared on the higher public W8A8 row | base response line 16; Quark response line 16 | Output and total throughput can be miscompared. |
| C039 | Critical | Q4 public submission accepted without engine flags | `localmaxxing-submission-qwen36-q4-3x-20260506.json:36`; pending file line 23 | Correctness-sensitive flags were lost at publication. |
| C040 | Critical | Q4 provenance pointed to a nonexistent artifact root | `localmaxxing-submission-qwen36-q4-3x-20260506.json:44` | Audit trail breaks when disputes or root-cause checks need the artifact. |
| C041 | Critical | Reduced Q4 payload after HTTP 500 lost flags | `localmaxxing-b70-qwen-leaderboard-20260612cg.json:1` | Public row hides the flags that made the run correct. |
| C042 | Critical | Inconclusive correctness smoke became public performance evidence | `localmaxxing-b70-qwen-leaderboard-20260612cg.json:1` | A public row was allowed despite inconclusive text correctness. |
| C043 | Critical | Experimental augmented GGUF submitted under ordinary Qwen identity | `localmaxxing-b70-qwen-leaderboard-20260612cg.json:1` | Unsafe pending ordering fix was mixed with public model identity. |
| C044 | Critical | MTP claim contradicted structured flags | `localmaxxing-b70-qwen-leaderboard-20260612cg.json:1` | Text said MTP while structured flags said no speculative decoding. |
| C045 | Critical | N-gram speculative claim contradicted structured flags | `localmaxxing-b70-qwen-leaderboard-20260612cg.json:1` | Wrong spec-decode attribution can misdirect root-cause and speed work. |
| C046 | Critical | Single-B70 speed presented as four-GPU hardware row | `localmaxxing-b70-qwen-leaderboard-20260612cg.json:1` | Hardware scaling claim becomes false. |
| C047 | Critical | One-card 256K capacity row recorded as four-card hardware | `localmaxxing-b70-qwen-leaderboard-20260612cg.json:1` | Capacity and topology claims are false. |
| C048 | Critical | B70 VRAM semantics differ across public rows | W8A8 response lines 47-50; leaderboard line 1 | Memory and fit comparisons can be wrong by 4x. |
| C049 | Critical | Accepted Qwen launcher still defaults to graph-none without `COMPILATION_CONFIG` | `launch-qwen36-quark-int8-accepted.sh:14`; `run-qwen36-ablation-candidate.sh:74` | Current tooling can recreate the known graph identity failure. |
| C050 | Critical | Auto-PIECEWISE guard misses default `decode,prefill` GDN fallback | `run-qwen36-ablation-candidate.sh:71`; `:74` | Safeguard can fail and silently inherit graph-none identity. |
| C051 | Critical | Production Qwen slot enables prefix caching while accepted lane disables it | slot env line 59; `serve-vllm-profile.sh:148`; accepted launcher line 203 | Production service is not the accepted benchmark identity. |
| C052 | Critical | Production Qwen slot uses a different cache root from accepted lane | slot env line 26; 2026-06-11 notes line 15146 | Cache root changes token behavior and correctness identity. |
| C053 | Critical | Provenance guard is not wired into slot switch or systemd startup | `switch-vllm-model-slot.sh:85`; `b70-vllm-slot.service:14` | Service can start from unverified graph/cache/env state. |
| C054 | Critical | Production Qwen slot omits accepted GDN and sampler correctness flags | accepted launcher line 49; slot env line 38; handoff line 57 | Output and replay identity change without a visible profile change. |
| C055 | Critical | Production Qwen slot uses GPU memory utilization 0.95 while accepted lane uses 0.90 | slot env line 57; accepted launcher line 13 | Memory headroom changes capture and correctness behavior. |
| C056 | Critical | Qwen launchers and XCCL health still hard-code `eth1` | accepted launcher line 59; XCCL health line 42 | Interface drift can masquerade as model/runtime regression. |
| C057 | Critical | XCCL preflight does not record the actual FI/CCL interface used | XCCL health lines 19 and 37 | Logs cannot prove distributed runtime identity after drift. |
| C058 | Critical | Service launcher derives CCL interface from default route | `serve-vllm-profile.sh:85` | Routing changes silently alter benchmark identity. |
| C059 | Critical | Launchers split `VLLM_EXTRA_ARGS` with shell word-splitting | accepted launcher line 182; ngram trace line 255; replay digest line 127 | JSON graph/spec flags can be corrupted. |
| C060 | Critical | Replay-digest launcher defaults to oneAPI 2026 compiler library | replay digest lines 21 and 61 | SYCL ABI split can contaminate diagnostic evidence. |
| C061 | Critical | Sidecar probe swallows oneAPI sourcing failure | sidecar probe line 27 | Environment setup failure can be blamed on model/runtime code. |
| C062 | Critical | Overlay launchers validate only `_xpu_C.abi3.so` existence | replay digest line 23; sidecar line 22; W8A8 offset line 31 | Stale or wrong-SYCL native binaries pass launch gates. |
| C063 | Critical | Build tree contains stale native-extension variants with mixed SYCL artifacts | `/home/steve/src/vllm-xpu-kernels/build` ldd anchors | Native-extension provenance can dominate root cause while scripts only encode a tag. |
| C064 | Critical | Kernel README requires oneAPI 2025.3 but tells users to source generic `setvars.sh` | `vllm-xpu-kernels/README.md:46`; `:58`; MiniMax repro README line 83 | Following docs can build the wrong ABI. |
| C065 | Critical | `setup.py` prints oneAPI info but does not enforce expected version | `vllm-xpu-kernels/setup.py:61`; `:136` | Wrong compiler/runtime versions pass build-time checks and fail later. |
| C066 | Critical | Default vLLM cache root falls back to populated anonymous `~/.cache/vllm` | `envs.py:583`; `backends.py:1053`; local cache root | Missing `VLLM_CACHE_ROOT` can reuse opaque graph/AOT caches. |
| C067 | Critical | Ablation runner exits 0 even when gates fail | `run-qwen36-ablation-candidate.sh:476`; `:507` | Automation can promote failed quality or canary runs. |
| C068 | Critical | Quality suite can report `baseline_match_all=true` with no baseline | `qwen36-text-quality-suite.py:334`; `:371` | No-regression can be asserted without comparison evidence. |
| C069 | Critical | Ablation runner weakens long-context gate to 4096 tokens | ablation script line 29; quality suite line 341 | 32K service can pass a shortened proxy gate. |
| C070 | Critical | Oracle parity wrapper ignores replay process failure in final exit | oracle parity gate lines 55, 143, and 163 | Broken replay can be hidden behind checker-only success. |
| C071 | Critical | Exact oracle gate can pass with replay accounting mismatches | handoff line 856; oracle checker line 54 | Token-exact output can mask scheduler or GDN transaction bugs. |
| C072 | Critical | Serial oracle control ran under wrong identity | handoff line 801 | A bad control invalidates the serial GDN correctness anchor. |
| C073 | Critical | Spec parity launcher defaults to n-gram if `SPEC_CONFIG` is omitted | spec parity candidate line 4; ngram trace line 217 | DFlash or EAGLE conclusions can accidentally be n-gram conclusions. |
| C074 | Critical | Spec parity cleanup broadly `kill -9`s matching vLLM processes | spec parity candidate line 34 | Cleanup can kill unrelated jobs and contaminate devices. |
| C075 | Critical | Graph compare-direct diagnostic can return direct output instead of replay | `cuda_graph.py:1824`; return-direct summary line 40 | Synthetic non-replay lane can hide replay corruption. |
| C076 | Critical | Replay input address stability remains debug-only | `cuda_graph.py:1574`; `:1723`; suggestions line 296 | Production forced graph trusts stale pointers without enforced invariants. |
| C077 | Critical | Shared-expert fused act/quant was shallow-exact but deep-corrupt | handoff line 2746 | Microbench plus shallow canary could promote graph-unsafe workspace reuse. |
| C078 | Critical | Endpoint full-layerlet A/B did not prove C++ path active | handoff lines 3534 and 3549 | Speed deltas could be attributed to inactive code. |
| C079 | Critical | Routed topk8 GEMM used wrong B layout before fix | handoff lines 3496 and 3511 | Kernel and route conclusions before layout fix were numerically unsafe. |
| C080 | Critical | DFlash showed acceptance but exact gate still failed | handoff lines 2481, 2486, and 2513 | Acceptance rate was overread despite token mismatch. |
| C081 | Critical | DFlash recovery flags moved mismatches earlier and hit device-lost | handoff lines 2524 and 2561; scheduler line 1906 | Recovery flags corrupted token/GDN/KV state and could crash endpoint. |
| C082 | Critical | DFlash stateful replay failed under async, sync, and serial GDN anchors | handoff line 2600; GPU runner line 3488 | Scheduler/replay knobs were not a real packed-state fix. |
| C083 | Critical | Failed native GDN diagnostics remain hot-path flags | handoff line 873; `_xpu_ops.py:1508` | Re-enabling them can alter verifier outputs or mask corruption. |
| C084 | Critical | Eager-every-N workaround masks async plus PIECEWISE corruption | handoff lines 120 and 159 | It can be mistaken for deployable async repair while losing speed. |
| C085 | Critical | Spec parity launcher model-name default says FP8 for INT8 Quark path | Qwen spec and ablation launch scripts | Model identity can be wrong before any benchmark starts. |
| C086 | Critical | Re-prefill sidecar verification was not semantically aligned with incremental decode | `CURRENT.md:2210` | Wrong verifier design produced mismatches around early positions. |
| C087 | Critical | Warm in-process diagnostic became an approved public MiniMax row | stockbench methodology line 33; warm-steady payload line 20 | Diagnostic method was not directly comparable but became public speed evidence. |
| C088 | Critical | Stale cache root produced coherent but wrong MiniMax output | `minimax-m27-warm-steady-quality-cache-20260521.json:31` | A fast result can look plausible while exact hash is wrong. |
| C089 | Critical | `GPU_MEMORY_UTILIZATION=0.95` produced speed-stable but quality-failing MiniMax run | `minimax-m27-gmem095-quality-guardrail-20260521.json:21` | Memory utilization invalidated a speed candidate. |
| C090 | Critical | Known long-context graph corruption preceded a 32K public row | long-context controls line 52; 32K payload line 23 | 32K public claim lacked directly attached graph-quality proof. |
| C091 | Critical | 32K MiniMax row mixed capacity proof with short-decode speed | 32K payload line 16 | Could be read as 84 tok/s at true 32K decode. |
| C092 | Critical | JSON retry-until-pass masked raw MiniMax corruption | JSON gated payload line 20 | Public quality hid user-visible malformed or control-character candidates. |
| C093 | Critical | Structured regex or HTML fast lane overpromoted as general quality | regex payload line 16; AGENT_HANDOFF lines 25-44 | Constrained-output speed inflated general MiniMax claims. |
| C094 | Critical | Website PIECEWISE lane kept graph corruption behind discard/retry wrappers | website quality continued line 2; website task quality lines 71-80 | Retry wrappers hid endpoint failure in a fast graph path. |
| C095 | Critical | Full-decode graph row approved on quality smoke despite adjacent all-NUL graph path | full-decode submission response line 1 | Rejected adjacent graph failure required stricter attached gates. |
| C096 | Critical | Public MiniMax model/backend identity was wrong or backend-ambiguous | attn-delay payload line 2; submission line 10 | Base MiniMax, AutoRound local weights, and XPU backend identity drifted at publication. |
| C097 | Critical | Persistent MiniMax graph service produced wrong answers and NaN logprobs after repeats | graph repeatability note lines 5-8, 25-31, 155-161 | Long-running service hazard, not just a one-shot benchmark failure. |
| C098 | Critical | MiniMax frontdoor pause and LAN exposure allowed traffic to contaminate service lanes | frontdoor script lines 41-43, 323-350, 520-526; service doc lines 17-19 | Local or LAN traffic could bypass pause or consume the active generation queue. |
| C099 | Critical | MiniMax c4 live service stalled then hit Level Zero device-lost on restart | session-cache ops lines 193-237; repro map lines 231-238 | Direct production instability contaminated restore and runtime state. |
| C100 | Critical | TurboQuant near-limit run left orphaned workers that blocked production restore | TurboQuant active-boundary lines 184-206 and 208-238 | Failed context testing left XPU workers holding memory until manual cleanup. |

## Counts

- Critical rows: 100
- Baseline Critical rows: 30
- Subagent-selected Critical rows: 70
- Stop condition satisfied by parent audit: yes
