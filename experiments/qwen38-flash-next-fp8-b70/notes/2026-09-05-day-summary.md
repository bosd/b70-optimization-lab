# Qwen3.8 Flash-Next TP4 lane: 2026-09-05 (overnight through morning)

Standing lane: fastest possible without changing the answers, published so
anyone can reproduce it. Overnight work attributed the promoted MTP0 line's
72.7 ms decode step, by graph-mode subtraction and offline probes.

## What the step is made of (graph MTP0 identity, 2K, per step)

| component | ms | how |
|---|---:|---|
| everything except the MoE block | 19.1 | A145 (MoE path skipped) |
| MoE routing, alignment, quantization, sum | 3.3 | A148 minus A145 |
| the two MoE grouped GEMMs, execution | ~10 | A151 (all-reduce skipped) minus A148 |
| waiting at the 48 MoE all-reduces | ~40 | A146 minus A151/A154 |
| total | 72.7 | A146 control, authority hash |

The waiting appears only when the real GEMMs run before the collective and
the collective reduces the real MoE output (A146). It vanishes when the
GEMM launches are memsets (A148, 22.4), when the all-reduce is a no-op
(A151, 32.9), when it reduces a static zero buffer at the same site (A154,
34.2), and it is unaffected by the GEMM's launch configuration (A155, 4
warps / 2 stages, 74.8, exact). Offline, none of it reproduces: the same
collective on the dumped real MoE outputs (A156 dump, 48 tensors in
sequence, identical or rank-distinct) costs 0.025 ms per call inside an
XPU graph, every data class and every oneCCL knob is 0.6-1.7 ms per 48
calls, a Triton or matmul kernel before it adds nothing, and graph replay
adds nothing per Triton launch. Split-K for the GEMMs is a negative (the
launch is fixed-cost bound) and the platform XPU MoE backend does not match
the staged kernel package (rebuild needed).

## What the morning settled (A159-A163)

A159 (real data all-reduced, result discarded: 34.1 ms) showed the
subtraction was not additive: every perturbed run puts the model on a
wrong trajectory and costs 22-34 ms; only the real trajectory costs 72-75.
The per-layer embedding was cleared as the cause (A161 on device: exact but
313 ms, an on-device dequantization artifact; A162 eager with the XPU PLE
path instrumented: about 2.5 ms per step in total). A163, the same eager
instrumentation on a wrong trajectory, gives the differential: real minus
wrong is +18.5 ms per forward, all in the MoE block (all-reduce segment
+11.4, expert kernel +6.1, w13 GEMM +4.3), every other sub-operation flat.
The real trajectory routes to more distinct local experts per rank and
reaches the MoE collective more skewed; the graph replay, with nothing
else resynchronizing the ranks, doubles that into the 40 ms.

Midday results (promoted graph identity, one change each, telemetry
bypassed, 2K request, hash against the authority `afffd211`):

| attempt | change | hash | rate / step | verdict |
|---|---|---|---|---|
| A164 | `CCL_SYCL_ALLREDUCE_SIMPLE_THRESHOLD=0` | differs | 13.65 tok/s, 75.8 ms | rejected |
| A165 | `CCL_SYCL_ALLREDUCE_LL_THRESHOLD=8192` (low-latency path) | authority | 13.69 tok/s | exact, neutral (graph replay is correct with oneCCL 4ceafd1 now) |
| A166 | `CCL_SYCL_ALLREDUCE_ARC=1` | differs | 14.19 tok/s | rejected |
| A169 | split-K 4 MoE GEMMs (`VLLM_XPU_MOE_SPLIT_K=4`) | authority | 12.54 tok/s, median 63.7 with 90-118 ms outliers | exact, not faster |
| A168 | routing dump (eager, real text) | authority | slowest rank 204 blocks/step vs mean 120; round-robin 202, frequency-balanced 195 | static placement recovers at most 10% of the skew |

Offline, a deliberately late rank makes each captured all-reduce cost
exactly the extra arrival time (no fixed poll or backoff penalty), so the
40 ms is genuine per-layer arrival skew of the MoE block on the real
trajectory. Queue: A170 (split-K 8), then A171/A172 with forced
pseudo-random routing, balanced across ranks versus all on one rank
(timing only), to separate imbalance from per-hit weight streaming.

## Host

Sixth silent freeze at 09:48. In five of the six crashed boots the last
journal entry is the GPU telemetry audit (xpu-smi through the Intel MEI
driver), run by every packet at launch and teardown, seconds before the
freeze. New packets copy cached receipts (attempt 146) instead of calling
it (`tools/q38_freeze_mitigation.py`, supervisor and base-script rules);
launches since 10:39 ran with zero telemetry calls. The pending root-NVMe
firmware activation still needs a power-off.

Notes: [MoE share and attribution](2026-09-04-tp4-mtp0-a145-a146-moe-share-of-the-graph-step.md),
[request-shape matrix](2026-09-04-tp4-mtp1-a143-request-shape-matrix-result.md),
[sub-op timing](2026-09-04-tp4-mtp1-a141-a142-subop-timing-attribution.md).
Data: `../data/20260905-tp4-*`, `../data/20260905-b70-moe-*`,
`../data/20260905-tp4-allreduce-data-and-knob-probes/`.

## Afternoon: forced-routing runs point at VRAM oversubscription

| run | routing | step (ms, forward) | note |
|---|---|---|---|
| promoted graph MTP0 | real | 72.7 | authority |
| A171 | forced balanced pseudo-random, ≤3 hits/rank | ~125 | identical on all ranks, no recompiles, output collapsed to one token |
| A172 | forced, all 10 hits on one rank | 159.3 | identical on all ranks, coherent output |
| A173 | A171 + `Q38_LAYER_TIMING_LOG=3` | capture failed | the layer hook synchronizes; illegal while recording a graph → sub-op timing is eager-only |

Offline, the same Triton MoE GEMMs with fresh random experts every call (cold, `Q38_BENCH_FRESH_ROUTING`) cost 0.35 ms/layer at 1 hit and 0.54 ms/layer at 10 hits, so the server's extra ~2 ms/layer under forced routing is not the kernel. Linear fit across A171/A172: ≈0.09 ms per hit plus a fixed ≈2 ms per layer that appears only when cold experts are touched.

Per rank the weights take 31.57 GiB of the B70's 31.89 GiB (routed experts 114.86 GiB / 4 = 28.7 GiB; the rest is GDN, attention, the vocab-sharded embedding and head, shared expert, router). Card 0 showed 0.09 GiB free during a load. The runtime is already minimal (64-token prefill chunks, one sequence, one graph size, 128 MiB KV). Hypothesis: the xe driver evicts weight buffers to host memory under pressure and pages them back on first touch at PCIe speed (≈7 GB/s, the A171 rate). Hot experts stay resident, which is why degenerate trajectories (a few warm experts) run in 22–34 ms and PLE on the device (A161) ran at 313 ms. Probes queued: free VRAM after startup, an offline VRAM-filler run of the fresh-routing bench (chain19), and A174 (eager forced routing with the sub-op split).

## 14:42 seventh host freeze, the first with a kernel trace

A174 (eager lineage, checkpoint on the root NVMe) launched 14:40:31; its server log stops at 14:41:35 as weight loading begins. The previous boot's journal then shows `watchdog: BUG: soft lockup - CPU#30 stuck for 678s! [VLLM::Worker_TP]` in `smp_call_function_many_cond` (TLB-shootdown IPIs from the page-fault path) and `kworker … blk_mq_timeout_work blocked for more than 122 seconds` (the block layer), i.e. the root 980 PRO stalled under the mmap'd checkpoint read and the host hung. With xpu-smi bypassed since the morning, this is the next failure mode exposed. The host was hard-restarted at 16:33 (a first reboot at 16:16 was restarted again). Eager-lineage runs, which load from the root NVMe, are now a suspected freeze trigger; the graph lineage loads from USB.

## 17:00 the step is VRAM paging, confirmed offline at the server's footprint

`timing-moe-gemm-events-offline.py` gained `Q38_BENCH_SETS` (layer-sized FP8 expert weight sets, 629 MB each) and `Q38_BENCH_FRESH_ROUTING` (new random local experts every call). On card 0:

| resident expert sets | GB | reported free | w13 GEMM | w2 GEMM |
|---|---|---|---|---|
| 8 | 5 | 26 | 0.23 ms | 0.16 ms |
| 24 | 15 | 12.8 | 0.23 | 0.16 |
| 40 | 25 | 3.45 | 0.23 | 0.16 |
| 42 / 44 / 46 | 26 / 28 / 29 | 1.9 / 0.33 / 0.33 | 0.23 | 0.16 |
| 48 | 30.2 | 0.51 | **21.7** | **12.2** |

The 48-set cost is the same for 3 and 10 hits and equals one whole 419 MB / 210 MB buffer crossing PCIe at ~19 GB/s: the xe driver migrates entire buffers on touch once the footprint no longer fits, and there is no watermark slack below that (0.33 GiB free is still clean). A175's memory note puts the server at 31.746 GiB reserved of 31.891 per rank, i.e. at the edge, so transients evict weight buffers and every later touch of a cold expert pays a migration. This is the mechanism behind the promoted 72.7 ms step (real routing keeps hot experts resident), the 125–159 ms forced-routing steps (A171/A172), the 313 ms PLE-on-device step (A161), and the fast degenerate trajectories (a few warm experts).

Fix under test: A177 = promoted graph identity with `embed_tokens.weight`, `layers.46.mlp.experts` and `layers.47.mlp.experts` added to the UVA offload (≈1.56 GiB/rank freed for ≈5 ms/step of PCIe expert reads; the kernel reads the same bytes, so the output hash must stay `afffd211…`).

## 17:37 A179: bit-exact 2x from VRAM headroom

A177's per-layer selectors (`layers.46.mlp.experts`) matched nothing: the UVA offloader wraps decoder layers through `make_layers` with the prefix `…layers.` and the layer module's own parameter names carry no index, so the total stayed at 12.22 GiB (embedding + PLE) and the base script's receipt guard stopped the run. A179 uses the selector `mlp.experts` under a 13.4 GiB budget; the greedy fill takes the embedding, layer 0's experts, PLE, layer 1's experts and layer 2's `w13_weight`, and every rank logged the predicted 13.78 GiB.

| | A175 (promoted identity, memory note) | A179 (+ expert offload) |
|---|---|---|
| host-offloaded per rank | 11.92 GiB (PLE) | 13.78 GiB |
| allocator reserved per rank | 31.746 GiB | 29.891 GiB |
| forward step (graph, M=1) | 74.5 ms | **37.0 ms** |
| exact-2K conventional tok/s | 14.42 | **25.13** |
| output token ids | authority `afffd211…` | identical |

The same Triton kernels read the same bytes (two and a half layers' experts now cross PCIe each step, ≈6 ms), so the change is numerically inert by construction and the ids match token for token. A180 (fresh server, exact-2K twice) is the certification pair; A181 (budget 12.5 GiB: embedding + one expert layer) probes how little headroom is enough. MTP1/MTP2, whose 0.60x on real text was measured under the same paging, are next in line for re-evaluation with headroom.

## 18:12 headroom certification pair and budget probe

| run | host offload per rank | allocator reserved | forward step | exact-2K tok/s | output |
|---|---|---|---|---|---|
| A175 (promoted identity + memory note) | 11.92 GiB (PLE) | 31.746 GiB | 74.5 ms | 14.42 | authority `afffd211…` |
| A179 (budget 13.4: +embed, L0/L1 experts, L2 w13) | 13.78 GiB | 29.891 GiB | 37.0 ms | 25.13 | identical |
| A180 (A179 identity, fresh server, r1 / r2) | 13.78 GiB | 29.891 GiB | 37.1 ms | 25.14 / 25.20 | identical / identical |
| A181 (budget 12.5: +embed, L0 experts) | 12.8 GiB | 30.867 GiB | 35.8 ms | 24.44 / 25.94 | identical / identical |

Under 1 GiB of headroom already ends the paging, and each offloaded expert layer costs about 1 ms of PCIe reads per step, so the smallest offload that fits is the fastest. Certification (A182 realistic suite, A183 frozen-client battery) continues on the A179 identity that was already in flight; the embedding-only placement (A178) is the follow-up floor probe, and A184 re-evaluates MTP1 with headroom.

## 18:54 MTP1 with headroom is lossless and faster than MTP0

A184 = the graph MTP1 lineage (A120/A135) with the same expert offload (13.78 GiB per rank), the USB checkpoint copy and overlay `08df70ea`. Both exact-2K requests reproduce the MTP0 authority ids (`afffd211…`): r1 20.42 tok/s, r2 28.52 tok/s (MTP0 with headroom: 25.1-25.2). The two-token step is 57.7 ms forward plus 2.5 ms draft, where the same step cost 120-220 ms under paging (A143), so MTP1's "0.60x on real text" was paging, not the draft. Allocator reserved 30.93 GiB with the device again full to the byte, so MTP may want a little more budget. A185 (MTP1 headroom on the realistic suite) and A186 (MTP2 with headroom) are queued after the certification battery and the floor probe.

## 19:28 A178: the embedding alone is not enough headroom

A178 (budget 12.25 GiB: embedding + PLE, 12.22 GiB offloaded, the lineage's original "PLE plus embedding" placement) keeps the hash but runs at 14.58 / 15.97 tok/s at exact 2K, i.e. still in the paging regime (A175 14.42). One expert layer (A181, 0.88 GiB freed) is the smallest placement that ends the paging; the floor lies between 0.3 and 0.9 GiB of freed VRAM.

## 20:08 A185: MTP1 with headroom on the realistic suite is lossless and edges past MTP0

A185 (the A184 identity) passes the fixed cold realistic gate at **25.933214 tok/s** class-balanced median (all-prompt 26.34, p10 23.31, wall 25.09, TTFT median 0.86 s), with all twelve row hashes equal to the approved MTP0 A134 run. The same MTP1 line scored 8.66 class-balanced under paging (A135), so the withdrawn "MTP1 slower on real text" conclusion was a paging artifact; the draft costs ~2.5 ms per step and the two-token step is 57 ms. MTP0 with headroom is 25.27 on the same suite, so MTP1 is a small net gain at this budget; the MTP line is reopened (A186 = MTP2 with headroom queued).

## 20:27 A187: the certification battery passes on the promoted overlay

The frozen client's W13-N32 verifier also hashes the MoE source files, so the diagnostic overlay `08df70ea` can never pass it (A183, three launches). Publishing on the promoted overlay `2169dbfe` with nothing but the placement flags changed is the stronger claim anyway. A187 (battery) passed every gate: 6/7 quality with the inherited miss, 16/16 repeat, exact needle, exact-2K `afffd211…` at 25.43/25.43 (TTFT 12.6 s, was 58), exact-4K `c6193cc6…` at 25.43/25.40 (TTFT 25 s, was 100; rate was 12.9). See the [A187 note](2026-09-05-tp4-mtp0-a187-certification-battery-headroom-result.md). A188 (realistic suite at `2169dbfe`) is the LocalMaxxing run.

## 20:52 published: LocalMaxxing run `cmtp3g14502cun701y5ey93rh` approved at 25.617613 tok/s

A188 (realistic suite on the promoted overlay `2169dbfe`, headroom placement) passed the gate at 25.617613 tok/s class-balanced (all-prompt 25.88, p10 25.82, wall 24.83, TTFT median 0.59 s), all twelve row hashes equal to the approved A134 run. Attestation `20260905-tp4-mtp0-a188-promotion-attestation.json` binds the suite JSON to the A187 battery and the three-server exact-2K pair; payload queue `20260905-tp4-mtp0-a188-localmaxxing-payload-queue.json`; submission approved on the first attempt (HTTP 201). The ledger, results packet, top README row, index research-preview paragraph, model page result strip and CURRENT.md are updated. The prior approved row (14.43, `cmtn32b2w000tmm01t7j2wlpn`) stays listed; nothing was lowered or overwritten.

## 21:08 A186: MTP2 with headroom is lossless but no faster than MTP1

A186 (graph MTP2 lineage A139/A140 with the same expert offload, USB checkpoint, overlay `08df70ea`) reproduces the MTP0 authority ids on both exact-2K requests at 19.72 / 25.82 tok/s, against MTP1's 20.42 / 28.52 (A184) and MTP0's 25.4 (A187). The three-token step costs more than its extra accepted token buys at this budget, so MTP1 is the speculative depth to certify; MTP2 stays research.

## 21:31 A190: the MTP1 headroom line passes the certification battery

A190 = the MTP1 lineage's frozen client on its own overlay `1b2a17c1` (the head the W13-N32 verifier accepts) with the headroom flags and the USB checkpoint. Every gate passed: 6/7 quality with the inherited miss, 16/16 repeat, exact needle; exact-2K `afffd211…` at 28.27 / 28.73 tok/s (MTP0 headroom 25.43), exact-4K `c6193cc6…` at 27.31 / 30.26 (MTP0 headroom 25.4; the paged MTP0 line was 12.87); short rows 35.3. Both depth hashes are the MTP0 line's own two-server authorities, so MTP1 is lossless at every measured pin. A189 (realistic suite, same identity) is the LocalMaxxing run for this line.

## 21:56 published: lossless MTP1 headroom line approved, run `cmtp5u0ip02eln701lntsl2ns` at 27.048435 tok/s

A189 (MTP1 lineage overlay `1b2a17c1`, headroom flags) passed the fixed cold realistic gate at 27.048435 tok/s class-balanced (all-prompt 27.53, p10 24.12, wall 26.05, TTFT median 0.96 s), all twelve row hashes equal to the MTP0 rows; attestation binds it to the A190 battery and the A184/A190 exact-2K pair. Approved on submission. Ledger, results packet, README, index, model page and CURRENT.md updated; both prior rows stay listed.

## 22:19 A191: the MTP1 line needs the larger offload budget

A191 (MTP1 lineage, budget 12.5 GiB → 12.8 GiB offloaded: embedding + layer-0 experts + PLE, 0.88 GiB of headroom) keeps the authority ids but runs at 9.43 / 9.66 tok/s at exact 2K: the M=2 step, its draft buffers and the larger KV fill the card again and the driver pages (memory note: allocator reserved 31.908 GiB against 31.891 GiB of device memory, the first run where the pool itself exceeds the card). MTP0 is fine at this budget (A181, 35.8 ms); MTP1 needs the 13.4 GiB budget it was certified with (13.78 GiB offloaded). The headroom floor is workload-dependent, so the budget is part of each line's identity.

## 22:37 A192: the honest sub-op split of the un-paged step

A192 = the eager lineage (USB checkpoint, overlay `08df70ea`) with the headroom placement and LEVEL-3 sub-op events on real routing. The synchronizing hooks inflate the step to 389 ms, so only the event timings count: the two MoE GEMMs sum to 11.4 ms (w13, 0.21 ms/launch) and 8.2 ms (w2, 0.17 ms/launch) per step, matching the offline kernel cost, and the all-reduce events (33-35 ms) are almost entirely rank skew under per-op synchronization (sum of max-min across ranks 31 ms). Against the 37 ms graph step this puts the MoE GEMMs at roughly 20 ms and everything else (GDN, QSA attention, hyper-connection mix, norms, 49 all-reduces, sampler) at roughly 17 ms. The w13 launch moves 33 MB in 0.21 ms (~160 GB/s, a third of the card's bandwidth) at M=1, so the decode-shaped MoE GEMM is the next real lever; the split-K and GEMM-config negatives (A155, A169, A170) were measured under paging and deserve a re-screen with headroom.

## 22:56 A193: split-K 4 re-screened with headroom is exact and neutral

A193 (the A179 identity plus `VLLM_XPU_MOE_SPLIT_K=4`, `VLLM_XPU_MOE_SPLIT_K_MAX_TOKENS=40`) keeps the authority hash at 25.15 / 25.18 tok/s with a 37.2 ms step, i.e. the same as without split-K (A179/A180 25.13-25.20, 37.0 ms). The paged-era negative (A169) stands for the right reason now: at M=1 the two MoE GEMMs are not bandwidth-bound on a resident weight set either, so splitting K does not help. A194 (split-K 8) follows for completeness; the next MoE lever is the M=1 tile configuration (the W13-N32 map was selected under paging, A155's config negative too).

## 23:13 A194: split-K 8 with headroom, exact and neutral

A194 (`VLLM_XPU_MOE_SPLIT_K=8`) keeps the authority hash at 25.08 / 25.07 tok/s with the same step as A179/A193. Split-K is closed as a lever on this model: exact at 4 and 8, never faster, with or without paging. The offline M=1 tile-config sweep (54 candidates: block N 32/64/128, W1 block 16/32/64, warps 4/8, stages 2/3/4, hot clocks) runs next on card 0.

## 23:22 offline M=1 tile-config sweep: the W13-N32 map is already the optimum

54 configs (block N 32/64/128 × W1 block 16/32/64 × warps 4/8 × stages 2/3/4) on card 0 with hot clocks and fresh 10-hit routing. Warps 4 is 1.3-4x slower everywhere; stages do not matter; the W1 block does not change the w13 timing in this path; block N 64 with 8 warps is the floor at 0.30 / 0.15 ms per launch and the shipped map (N 64, W1 32, warps 8, stages 4) sits on it. No tile change beats it; the next MoE lever has to change the kernel's shape of work (fused w13→silu→w2 for M=1, or fewer launches), not its tiles. Data: `../data/20260905-b70-moe-m1-tile-config-sweep-hot-card0.log`.

Layer-level split from A192 (per-op synchronization, so proportions only): mlp 171 ms, hyper-connection mix 88, GDN attention 69, QSA attention 55 per step across 48 layers, i.e. the MoE block is ~45% and the three non-MoE blocks ~55% of the synchronized step; in graph replay the MoE GEMMs alone are ~20 of 37 ms, so the non-MoE blocks (many small launches) shrink most under the graph. The hyper-connection mix is the largest non-MoE block and is elementwise work, a candidate for fusion once the MoE lever is spent.

## 23:30 cold-expert census: most experts are never touched on a trajectory

From the A168 top-k dump (4,848 decode rows of a 2K request, 48,480 hits): 14,310 of the 24,576 (layer, expert) pairs are never hit, the coldest 40% of experts per layer receive 0.00% of hits, and per rank (linear placement) the coldest 13 of 128 local experts per layer receive 0.00%. The headroom the driver needs (about 1.6 GiB per rank, 2.7 expert layers) could therefore come from host-resident cold experts at essentially zero decode cost instead of 2.7 ms per step of PCIe reads, if the cold set is chosen from a broad sample. A195 dumps the top-k ids over the whole realistic suite on the headroom identity for that census; the placement change itself is a split-storage MoE launch (resident rows and host rows into one intermediate buffer, bit-exact) that needs a re-oracle.

## 23:45 per-expert host placement: patch written, test queued

Overlay (uncommitted until the offline test passes): `fused_moe_kernel` takes an optional per-expert base-address table (`USE_B_TABLE`; `b_base = table[max(e, 0)]` cast to a pointer, then the unchanged tiles, K loop and scale indexing), the launch passes `B._q38_base_table` when present, and `vllm/q38_expert_placement.py` splits each MoE layer's `w13_weight`/`w2_weight` into resident device rows and pinned host rows (UVA view) after the FP8 post-load step, per a JSON placement from `Q38_EXPERT_HOST_PLACEMENT`. Repo tools: `equivalence-and-timing-moe-expert-placement.py` (bit-identical outputs on 32 routings for table-no-host and table-half-host against the resident reference, then event timing for resident-only and host-hitting routings) and `build-q38-expert-host-placement.py` (never-hit experts from the top-k dumps, coldest first, capped by host GiB per rank). See the [design note](2026-09-05-per-expert-host-placement-design.md). A195 (top-k dump over the realistic suite) is running; the test follows it on card 0.

## 23:50 per-expert placement: bit-identical, resident rows at reference speed

The offline test passes: with a per-expert offset table the fused MoE kernel produces bit-identical outputs on 32 routings both with no host rows and with half the experts host-resident, and resident rows run at the reference speed (0.226 / 0.146 ms per launch against 0.224 / 0.144) once the loaded offset carries a `tl.multiple_of(off, 256)` hint; without the hint (or with an int-to-pointer cast) the kernel lost its vector loads and ran 3x slower on resident rows. A routing that hits three host-resident experts per call costs 0.59 / 0.23 ms, about 0.1 ms per host expert hit, so a rarely-hit cold set is close to free. Committed to the overlay as `567117d1`. A195 (graph lineage) could not run the top-k dump under graph capture; A197 repeats the census on the eager lineage with headroom at the new head. Data: `../data/20260905-b70-moe-expert-placement-equivalence-timing.txt`.

## 00:18 A197 census over the realistic suite

A197 (eager lineage, headroom, top-k dump over the whole realistic suite; 250,000 tensors ≈ 5,200 decode rows × 48 layers; outputs identical to A134): 3,141 of 24,576 (layer, expert) pairs (12.8%) are never routed to, the coldest 5% of experts per layer receive 0.002% of hits and the coldest 10% receive 0.035%. A 2.0 GiB per-rank host placement needs 6.8% of each rank's experts, so it is filled entirely from never-hit experts of the union census (A168 + A197); on other prompts a placed expert that does get hit costs about 0.1 ms per hit instead of a driver page migration. The eager rate with the dump hook (5.2 tok/s) is the hook's cost, not the line's.

## 00:30 A196 (placement) running; clean placement branch prepared

A196 = the promoted PLE-only identity plus the 2 GiB/rank cold-expert placement at overlay `68a410ba` (diagnostics + placement). For publication, the placement patch is re-applied on the promoted overlay alone as branch `q38-placement` (`c5228465`, three files, no diagnostics; `fused_moe.py` sha `4e611de0…`); the W13-N32 verifier's source contract has to learn that head and hash before the frozen client can certify it, which is a certification-policy change to be reviewed rather than slipped in.

## 00:36 A196: placement applies and stays bit-exact, but the split fragments the pool

A196 (promoted PLE-only identity + 2 GiB/rank cold-expert placement, overlay `68a410ba`) applied the placement on every layer (1.86-1.91 GiB per rank host-resident) and keeps the authority hash on both requests, but runs at 19.17 / 21.07 tok/s with a 44.9 ms step. The memory note explains it: allocator allocated 29.78 GiB (the weights did shrink, as in A179), but reserved 30.73-30.79 GiB and device free 0.01 GiB, i.e. copying each layer's resident rows into a new tensor while the original was alive left about 1 GiB of fragmentation in the caching pool and the card full again, so the driver pages partially. Fix: a two-phase split that stages every layer's resident rows to pinned host memory, frees all originals, empties the cache, then reallocates the resident tensors compactly and copies back.

## 00:45 placement split rewritten to free-then-reallocate; A199/A200 queued

The per-layer split now stages a layer's resident and cold rows on the host, frees the original device tensor, and only then allocates the compact resident copy, so it lands in the block the original released; `empty_cache` runs once after the last placed layer and logs the allocator's reserved size. A global two-phase staging was rejected because it would pin about 115 GB of host memory across the four ranks. A199 re-screens the promoted MTP0 identity with the placement (target: reserved ≈29.9 GiB, hash `afffd211…`, step ≈34 ms); A200 does the same for MTP1. The clean certification branch `q38-placement` carries the same module.

Certification prep for the placement line (held until A199 decides): a verifier draft that accepts `q38-placement` head `2780ab24` with its `fused_moe.py` hash, and generator makers for A201 (frozen-client battery) and A202 (realistic suite) on that head with the PLE-only offload plus `Q38_EXPERT_HOST_PLACEMENT`; both dry-run validated and removed again. Applying the verifier change is a certification-policy edit and will be committed as such.

## 01:00 A199: per-layer free-then-reallocate still leaves the pool at 31.2 GiB

The allocator gives each expert tensor a dedicated large segment; freeing it and allocating the smaller resident copy puts the copy inside the same segment, so the driver never gets the hole back (reserved 31.15-31.21 GiB after `empty_cache`). Version 3 records the placed layers and, on the last one, has the ranks take turns (gloo barrier) staging all their resident rows on the host, freeing every original, emptying the cache and reallocating compact tensors; the transient host staging is ~28.7 GB per rank in turn. A204 (MTP0) and A205 (MTP1) re-screen it; the clean branch `q38-placement` is at `df61032c` with the same module.

## 01:18-09:42 eighth host freeze; 09:53 A207 launched

A204's rank 0 was OOM-killed by the host while pinning 28.7 GB for the v3 staging (about 24 GB were available next to the PLE offload); the frozen launcher's host reset for A207 (swap off/on, cache drop) then ran seconds later and the kernel went into soft lockups (a CPU stuck for 28,212 s by the end), with `swapoff`, systemd, smartd and a block worker in D state and no disk I/O until the hard restart at 09:42. A207 had never launched. After the reboot: USB remounted, A207/A208 committed, A207 launched in the background with placement v4 (stage one layer, free, empty the cache, reallocate compactly); A208 (MTP1) chained. Lesson: never run the frozen launcher's host reset from a foreground shell, and treat a reset right after killed workers holding pinned memory as a freeze trigger.

## 10:05 A207: placement v4 cannot compact either; post-load compaction is closed

With the per-layer stage → free → `empty_cache` → reallocate order, the allocator still reports 31.15-31.21 GiB reserved (30.24 GiB allocated) after the last placed layer, the same as v2. The loader packs the expert tensors into shared allocator segments, so a freed expert tensor never lets a segment go back to the driver and the compact copy cannot land outside it. Three variants (copy-while-alive, free-then-reallocate, free + cache empty + reallocate) all end at ~31.2 GiB reserved; the global stage-everything variant (v3) is ruled out by host memory. A206 tries the expandable-segments allocator, which returns physical pages at page granularity inside segments; if that distorts decode timing (an earlier memory notes 2-5x on B70), the remaining route is placing experts at load time through the weight loader so the device tensors are created at their resident size.

## 10:28 A206: expandable segments have no effect on the XPU allocator; load-time placement next

With `PYTORCH_ALLOC_CONF=expandable_segments:True` the placement run lands on the same figures as A207 (31.2 GiB reserved after the last placed layer, 30.7 at the decode note, 0.014 GiB free), so the setting is ignored by the XPU caching allocator here. Placement v5 moves the split to weight-creation time: a placed layer's `w13_weight`/`w2_weight` are created at their resident size plus pinned host rows, the weight loader writes each expert through `row_view()` (cold experts straight to host memory), and the post-load hook only re-attaches the offset tables; the device pool is then compact by construction. It lives on the overlay branch `q38-placement-v5` (`ba1f4cde`); the offline check `test-q38-expert-placement-loadtime.py` runs before A209 (promoted MTP0 identity + load-time placement).

## 10:29 load-time placement passes the offline check

`test-q38-expert-placement-loadtime.py` on card 0: a placed layer created at resident size (110 of 128 rows on the device, 18 cold rows in pinned host memory), every expert written through the loader's `row_view()`, and `fused_experts` bit-identical to the full resident reference on 48 routings, 22 of which touch host-resident experts. A209 (promoted MTP0 identity + load-time placement, overlay `q38-placement-v5`) relaunched after a first launch tripped on a worktree holding the branch.

## 10:30–10:40 09-06 — A209 negative, A210 relaunch (load-time placement v5)

- **A209 crashed in model construction**: `q38_expert_placement.prepare_layer` raised `RuntimeError: Only dense CPU tensors can be pinned` from `torch.empty(..., pin_memory=True)`. The offline check had passed with the same code because it ran with the CPU default device; vLLM constructs the model under the XPU default device, so an allocation without an explicit `device="cpu"` lands on the card and cannot be pinned. Negative kept: load-time hooks must name the host device explicitly.
- Fix: both pinned allocations in `vllm/q38_expert_placement.py` now pass `device="cpu"`. Branch heads: `q38-placement-v5` c4f921f5 (diagnostic lineage), `q38-placement-clean-v5` 21633cea (certification lineage; `fused_moe.py` unchanged, so the verifier draft's per-head source hash still applies).
- **A210** = A209 with the fix (promoted MTP0 identity, exact-2K r1/r2, table kernel + load-time placement of 2 GiB/rank of never-hit experts, port 19880). Launched 10:32 in the background; chain55 restores `q38-exact-verify` after the run.
- Prep during the load window: A201 (frozen-client battery) and A202 (realistic suite) regenerated at the clean head 21633cea; both validate. A201 pins the *current* verifier sha, so it must be regenerated once the verifier policy commit (accept 21633cea with its `fused_moe.py` hash) lands — that commit waits for A210 to hold the hash.
- Overlay-restore race: the previous chain (chain54) was still alive and restored `q38-exact-verify` 27 s before A210's launch; the packet launch script checks out its pinned branch itself, so A210 started on `q38-placement-v5` regardless. Rule kept anyway: kill the previous restore chain by pid and confirm it is gone before the next launch on a diagnostic branch.

## 10:50–11:10 09-06 — A210 positive (small), A212 screen, the lossless line becomes a recipe

- **A210**: load-time placement of 2 GiB/rank never-hit experts holds both authority hashes (exact-2K `afffd211…`, `e39e32c3…`); exact-2K r1/r2 20.70/21.05 vs A207 20.29/20.62 (+2%). Allocator reserved 29.87 GiB (30.77 before), device free 0.124 GiB. A211 was lost to a launch-order mistake (the overlay restore chain of the previous run flipped the branch; the packet pins the *current* overlay head and does not check out its branch); **A212** = same with 3.5 GiB/rank (543–587 never-hit experts per rank) launched 10:53 on `q38-placement-v5`; loaded at 28.9–29.05 GiB.
- The user asked whether the lossless line is a released recipe, image, and non-experimental repro entry. It was not: only the `research-status` MTP3 guide (Aug 27 identity) existed, no Dockerfile, no package, no Recipes-page entry, overlay heads unhosted. Published now (commit "repro(qwen38): lossless MTP1 lab-replay guide…"):
  - `patches/qwen38-flash-next-fp8-b70/vllm-lossless-mtp1-1b2a17c1/`: 55-commit series + bundle over public `76cfe1cd`, `verify-series.sh --apply` re-creates tree `1cb86e07`;
  - `patches/qwen38-flash-next-fp8-b70/oneccl-4ceafd1-b70-public/`: byte receipt; release `qwen38-flash-next-oneccl-4ceafd1-b70-public-20260906` (zst `34dc2cad…`, verified by direct download);
  - `repro/qwen38-flash-next-fp8-tp4-mtp1-lossless-b70-27tps-20260905/` (`lab-replay`): `verify-identity.sh`, `run-record-gate.sh` (derives a fresh attempt from the pinned A189 packet, launches through the frozen launcher, runs the frozen client once, `check-replay-result.py` compares all 12 output pins and every gate with the record), `identity.json`, evidence manifests, untested `Dockerfile`/`container-serve.sh`/`build-image.sh` with `CONTAINER-STATUS.md`;
  - package `candidate` (`packages/…-27tps-20260905`), family packet grade B, coverage registry, `repro/README.md`, `docs/model-recipes.md`, results README link, index preview link; generated pages rebuilt; validators and the 91 tooling tests pass (two count-guard tests updated).
  - Not certified: clean-host install, dependency hash lock, non-originating-host replay, container replay. The record gate itself has not been executed end-to-end yet (it wraps the exact A189 path; first run queued behind the placement work).

## 11:08–11:17 09-06 — A212, the lineage mistake, A213

- **A212** (3.5 GiB/rank never-hit placement, 543–587 experts/rank): hashes hold; exact-2K r1/r2 21.04/21.09; allocator reserved 29.07 GiB, device free 0.53 GiB. Against A210 (20.70/21.05) the extra budget adds nothing: the placement lever plateaus at about +2% **on the PLE-only lineage**.
- **Lineage correction**: A196–A212 were derived from the frozen A78 packet (PLE-only, `--cpu-offload-gb 12.0`, 11.92 GiB offloaded), not from the promoted 13.4 GiB headroom identity. Same harness (`bench-openai-token-depth-suite`, exact-depth 2K, conventional 99-interval tok/s): the 13.4 identity reads **25.43** (A187 r1/r2), the lossless MTP1 line 28.27/28.73 (A190). So placement-on-PLE-only at 21.1 is far below the promoted line: placement replaced only part of the paging, while the 13.4 identity ends it by offloading embeddings plus the layer-0/1 expert tensors (which are hot: read over PCIe every step).
- **A213** = the right experiment: PLE + embeddings offloaded (`--cpu-offload-gb 12.25`, 12.22 GiB, `_selective_ple_embed_budget12p25_uva`), hot experts resident, 3.5 GiB/rank of never-hit experts host-placed at load time (v5 head c4f921f5). Generator `rewrite-q38-a78-to-a213-placement-ple-embed-12p25.py` derived from the A188 generator. First launch failed on the overwrite guard because `ATTEMPT=188` survived the text derivation (packet names, port and `attempt188` were renamed; the `ATTEMPT=` assignment was not); fixed and relaunched 11:15 on port 19883. Decision rule: A213 exact-2K vs 25.43; if higher with hashes held, certify this identity (A201/A202-style packets need the same offload change), then port to MTP1.
- Container route: first build failed because the stage tar's members sit under the archive prefix, not under `vllm_xpu_kernels/`; the Dockerfile now installs the stage through the mtp3 guide's frozen `prepare-runtime.py`; rebuild running.

## 11:31–11:40 09-06 — A213 negative resolved: the placed layers lost the tuned MoE map

- **A213** (PLE + embeddings offloaded at 12.25, hot experts resident, 3.5 GiB/rank never-hit placement, v5): hashes hold, exact-2K r1/r2 21.19/21.18, allocator reserved 28.78 GiB, device free 0.82 GiB. Same rate as A212 despite the identity change, and 17% below the 13.78 identity (25.43, A187) with more free memory than any run. The same-harness table (A151–A213) shows every placement head at 19–21 regardless of headroom.
- **Root cause**: `fused_experts` keys the tuned-config lookup on `w1.size()`; a placed layer's weight tensors are resident-sized (110–128 rows), so `E=110…` has no file in `moe-m1-w13-n32` and the layer silently takes the default config. A213's log carries eight "Using default MoE config" warnings (one per distinct resident count); A187's log has the single `E=128,N=640` selection. The sweep that produced the map showed the shipped config matters by exactly this kind of margin.
- **Fix** (clean head `823d4e42`, cherry-picked onto v5 as `2a7f1ea3`): the lookup uses the layer's logical expert count (`_q38_num_experts`) when the placement table is present. Verifier policy moved to `823d4e42` with its `fused_moe.py` hash. A214 (clean head before the fix) was stopped during load as a foregone negative.
- **A216** = frozen-client certification battery (A187 lineage) at the A213 identity on `823d4e42`, launched 11:38 on port 19886 (wait-and-run driver; client pins the verifier sha). **A217** = realistic suite (A188 lineage) at the same identity, generated and validated, launches after A216. Decision: A216 exact-2K vs 25.43 and both authority hashes; then A217 for the LocalMaxxing metric vs 25.62.

## 11:49–11:55 09-06 — the fix had to land in both lookup paths

- A216 (clean head 823d4e42) still logged `Using default MoE config … E=125`: the XPU Triton MoE backend goes through the modular `TritonExperts.apply` in `experts/triton_moe.py`, which has its own `try_get_optimal_moe_config(w1.size(), …)` call; only `fused_experts_impl` in `fused_moe.py` had been patched. Stopped during load; A217 skipped by flag.
- Clean head `bcabdf2f` patches both sites (`triton_moe.py` hash `62181163…`); the same two commits sit on the MTP1 placement branch `q38-placement-mtp1-clean` (`2e04cdbd`, on the lossless head 1b2a17c1) and on the diagnostics branch (`5dc515c3`). Verifier policy accepts both clean heads with per-head `fused_moe.py` and `triton_moe.py` hashes.
- **A220** (battery) / **A221** (suite): the A213 identity on `bcabdf2f`, launched 11:52 on port 19890; chain62 launches A221 after A220 and stops either run at the first `default MoE config` line. **A218** (battery) / **A219** (suite): the same identity on the MTP1 placement head, generated for the next slot.

## 12:04–12:22 09-06 — the third lookup site

- A220 (clean head bcabdf2f, two sites fixed) still logged one `default MoE config … E=125` on rank 0; the warning is a rank-0-only "once" message, so the other ranks were silent, not clean. A222 (diagnostics branch with an attribute/stack dump at both patched sites) never fired the dump while the warning reappeared: the caller was a third site, the overlay's own M1 phase-config path `try_get_optimal_moe_gemm_configs(w1.size(), w2.size(), …)` in `experts/triton_moe.py` (the `w13/n32` split-config lookup that the tuned map exists for; the grep pattern had matched the other two names only).
- Fixed on clean head `cb59004b` (`triton_moe.py` hash `c0ef7d8b…`), cherry-picked to the MTP1 placement branch (`005dc578`). Verifier policy accepts both with per-head `fused_moe.py`/`triton_moe.py` hashes. A223 (MTP0 battery), A224 (MTP0 suite), A225 (MTP1 battery), A226 (MTP1 suite) generated; chain65 runs them back-to-back from 12:21, stopping any run at the first fallback line.
- Cost of the miss: three 12-minute loads (A216, A220, A222). Lesson kept: enumerate config-lookup callers by the shared helper (`get_moe_configs`) and by grepping the *log line's* source, not by function names.

## 12:32–13:05 09-06 — the placement identity certifies: +8% bit-exact on MTP0

- **A223** (clean head `cb59004b`, all three tuned-map sites fixed): `Using configuration from … E=128` only, no fallback. Frozen-client battery PASS (recovery, quality 6/7, short 16/16 one hash, exact-2K/4K repeats): exact-2K **27.48 / 27.34**, exact-4K **27.40 / 27.43** tok/s, authorities `afffd211…` and `c6193cc6…` held, verifier receipt written. Against the approved 13.4 GiB line (A187: 25.43 / 25.43) that is **+8%** with every output pin unchanged.
- **A224** (same identity, second fresh server): PASS again, exact-2K 27.42 / 27.41, exact-4K 27.40 / 27.36. It ran the battery, not the suite: the A188 lineage's frozen client is the battery; the LocalMaxxing suite was driven separately in the prior session. Reconstructed the suite driver from the A188 result's `run_identity` and the A182 note (`--api-mode chat --max-tokens 512 --metric-tokens 100 --seed 20260609 --return-token-ids`, `enable_thinking=false`, temperature 0, fixed `realistic-suite-v1.json` sha `0ad543d1…`, once, cold).
- Queue: A225 (MTP1 battery on `005dc578`, running 13:01) → A227 (MTP0 suite, new packet) → A226 (MTP1 suite, existing packet with the suite driver). Promotion scripts for both rows staged.

## 13:25–14:45 09-06 — two approved rows and a second recipe

- **A227** (MTP0 suite): 27.640875 tok/s class-balanced, all twelve outputs equal to A188/A134; LocalMaxxing `cmtq4elns03ivn701hgvpo053` approved. **A226** (MTP1 suite): 31.929484 tok/s class-balanced (p10 30.19, TTFT 0.57 s), all twelve outputs equal to A189/A188; LocalMaxxing `cmtq59cy503jvn701kgvg62zt` approved, the fastest quality-preserving Flash-Next line. A224 had run the battery instead of the suite (the A188 lineage's frozen client is the battery; the suite is driver-run), so it became a second fresh-server repeat and the suite driver was reconstructed from the A188 `run_identity`; its first version resolved the run directory before the server created it and died silently (18 idle minutes on A227), fixed.
- Published: results page, ledger, README, CURRENT, site preview, plan, family manifest (placement exact-4K measurements for MTP0 and MTP1, hero on the no-speculation placement line). New recipe `repro/qwen38-flash-next-fp8-tp4-mtp1-placement-b70-32tps-20260906/` (lab-replay, candidate package, family packet grade B) with the placement overlay series `patches/qwen38-flash-next-fp8-b70/vllm-placement-mtp1-005dc578/` (nine commits over 1b2a17c1, verifier `--apply` re-creates tree `d82fb5f2`), evidence manifests, replay gate that drives the suite. The 27.05 guide's gate was corrected the same way (it had run the battery client).
- **A228** (MTP2 on the MTP1 placement head, exact-2K timing) launched 14:30: MTP2 was lossless but no faster than MTP1 under the 13.4 identity (A186); with hot experts resident the verify step may now pay off.

## 14:50 09-06 — A228: MTP2 on the placement identity is lossless but slower than MTP1 (closed again)

A228 (MTP1 placement head `005dc578`, two speculative tokens, PLE + embeddings offloaded at 12.25, hot experts resident, 3.5 GiB/rank never-routed experts host-placed): exact-2K r1 22.40 / r2 30.94 tok/s, authority `afffd211…` held on both. The A225 MTP1 pair on the same identity read 33.21 / 33.22. As under the 13.4 identity (A186), the second speculative token costs more in the verify step than it returns at this acceptance rate; the slow first pass is the MTP lineage's warm-up (A184 showed the same 20 → 28 pattern). MTP2 stays closed; data `20260906-tp4-mtp2-a228-exact-depth-2k-r{1,2}.json`.

## 14:52–15:05 09-06 — record-gate shakedown, verifier pins, the M=2 hypothesis

- The new recipe's record gate (attempt 229) failed twice on its own tooling before running: (1) `verify-identity.sh` imported the venv's vLLM (the launcher records the installed distribution's metadata version while the overlay tree in front of it is the code; the check now imports through `PYTHONPATH=stage:overlay`, pins `importlib.metadata.version("vllm")` and requires `vllm.__file__` inside the overlay); (2) the replay maker copied from the 27.05 guide still renamed `ATTEMPT=189`, so the derived launcher kept `ATTEMPT=226` and the packet refused to overwrite A226's run directory (the maker now asserts that no source literal survives). Third launch at 14:57 is running.
- Verifier drift: the 27.05 guide's frozen A189 packet pins the exactness verifier at sha `0bd36f13…` (git blob `00c54573…`), and the file moved three times today for the placement policy. Both guides now carry `verifier-pin.txt` (sha, blob, last lab commit that carries it: `6591515b` for the 27.05 guide); `verify-identity.sh` names that commit instead of failing late. The 31.93 guide pins the current bytes.
- Next lever: the MTP1 two-token step costs 62.7 ms against 36.5 ms for one token; the W13-N32 map has entries for M=1,4,8,… and the nearest-key lookup gives the verify step (M=2) the M=1 flat config with the phase deltas disabled. An offline M=2 sweep (36 candidates, card 0, `$SP/moe-m2-config-sweep.py`) is queued behind the gate; a better M=2 entry would then be screened on the MTP1 line (new tuned-map hash, verifier policy update, battery/suite).

## 15:21 09-06 — the 31.93 recipe replays itself

`run-record-gate.sh` (attempt 229, derived from the frozen A226 packet, frozen launcher, suite once cold) passed end-to-end on the originating host: 12/12 outputs identical to the record, every gate equal, 32.181792 tok/s class-balanced (record 31.929484). Evidence in the guide's `evidence/` and `data/20260906-tp4-mtp1-a229-record-gate-replay-realistic-suite-v1-result.json`. The M=2 tile-config sweep starts on card 0.

## 15:31 09-06 — offline M=2 tile sweep: the M=1 entry is already the M=2 optimum (closed)

37 candidates (block N 32/64/128 × warps 4/8 × stages 2/3/4 × optional W1 block 32) as an explicit `"2"` entry in the W13-N32 map, card 0, `Q38_MOE_GEMM_EVENT_TIMING`, ep-like routing (6 of 20 slots local). Baseline (the nearest-key M=1 entry): w13 0.2229 / w2 0.1539 ms per launch at M=2 against 0.2203 / 0.1407 at M=1; the best candidate (`bn64-w8-s3-w1bn32`, 0.2246 / 0.1542) does not beat it. Two consequences: no M=2 map entry to add, and the expert GEMMs cannot explain the MTP1 two-token step (62.7 ms) against the one-token step (36.5 ms): 48 layers × (0.38 vs 0.36 ms) is about 1 ms. The delta sits in the row-serial exactness selectors that keep MTP1 lossless (serial GDN verifier rows, row-wise TP all-reduce and hyperconnection norm at M=2). Data `20260906-moe-m2-tile-config-sweep-card0.json`, tool `sweep-moe-m2-tile-configs-offline.py` (needs the stage's `vllm_xpu_kernels` on `LD_LIBRARY_PATH`, otherwise the XPU platform silently fails to load and the functional MoE op registers for CPU).

## 16:05 09-06 — A230: the placement identity's eager sub-op split (same shape as A192)

Eager, level-3 marks and event timings at the placement identity on the diagnostics head (hashes held). Per step (48 layers, TP0 medians): w13 GEMM events **11.03 ms** (A192: 12.06; the hot layer-0/1 experts no longer read over UVA), w2 8.77 (8.69); the synchronized layer buckets are unchanged (mlp 172, hc_mix 90, GDN 70, QSA 56 of a 394 ms sync-inflated forward) and so are the all-reduce events (33-35 ms, inter-rank wait under eager). Reading: of the 36.5 ms graph step the two MoE GEMMs are about 18-20 ms and their tile config is the sweep optimum, so the next MoE lever is a decode-specialised small-M kernel (new accumulation order, re-oracled at promotion), not a map entry. Data `20260906-tp4-mtp0-a230-subop-timing-placement-2k.json`. A231 next: the MTP1 two-token step with the row-serial exactness selectors switched off (diagnostic, outputs not protected) to bound what batch-invariant M=2 kernels could return.

## 16:24–16:40 09-06 — A231 bound, and the MoE GEMM attribution was the event hooks

- **A231** (MTP1 placement head, the three row-serial exactness selectors off; diagnostic, outputs change: `460b0d5c…`): exact-2K r1 25.60 (warm-up), r2 **38.63 tok/s** against 33.2 with the selectors. Batch-invariant M=2 paths could return at most ~16% on the fastest line.
- Offline on card 0 (`timing-moe-gemm-events-offline.py`, fresh routing): the event-timed MoE GEMM launch cost is flat in the number of local experts hit (1 hit 0.21 / 0.18 ms, 5 hits 0.23 / 0.17, 10 hits 0.37 / 0.17) and flat in the local expert count with the tuned entry held fixed (E_LOCAL 128 → 2: 0.23 → 0.25 ms), so neither bandwidth nor grid waste explains it. A wall-clock loop of the whole fused-MoE block (align, two GEMMs, activation, sum) with the hooks off costs **0.43 ms per layer** at 2 hits and 0.46 at 10; with the event hooks on the same loop costs 1.18 ms: the hooks add ~0.75 ms per block, so the "18-20 ms of MoE GEMMs per step" read from A192/A230 was hook overhead, not kernel time (see the measurement-distortion note). The eager loop is itself CPU-launch-bound (six kernels per block); the graph replay of 48 blocks gives the GPU-side cost (below).
- Graph-level numbers (card 0, `timing-moe-block-graph-offline.py`, `probe-xpu-graph-kernel-floor.py`): under XPU graph replay the whole fused-MoE block costs **0.21 ms per layer at 2 local hits** (10.1 ms per 48-layer step) and 0.45 ms at 10 hits (21.5 ms); the per-kernel replay floor is 2.3 µs (tiny adds) and a 60 MB elementwise kernel runs at 526 GB/s, so the block's ~35 µs per kernel is kernel latency, not launch floor. The MoE block is therefore about 10-12 ms of the 36.5 ms step at the server's routing (2-3 local hits per rank), not half; the other ~25 ms is attention, hyper-connections, all-reduces and the rest. A232 (skip moe_allreduce), A233 (skip moe), A234 (skip moe_gemm) and A235 (skip gdn_core) re-measure the shares under the graph at the placement identity (A145-A151 did this under paging).

## 16:31–17:21 09-06 — graph-step decomposition at the placement identity (A232–A234)

Diagnostics head `93985742` (placement + all fixes + hooks), exact-2K r1/r2 conventional 99-interval rates; the control on the clean head is A223/A224 at 27.4 tok/s (36.5 ms per token), the diagnostics-head control A236 follows.

| run | skipped (`Q38_DIAG_SKIP`) | exact-2K r1 / r2 | step | delta vs 36.5 ms |
|---|---|---|---|---|
| A232 | `moe_allreduce` (the 48 MoE final all-reduces become no-ops) | 27.59 / 27.58 | 36.3 ms | **~0.3 ms**: the all-reduces are negligible once paging is gone (the 40 ms of A151 was rank skew) |
| A233 | `moe` (whole routed-expert block) | 45.84 / 45.96 | 21.8 ms | **14.7 ms (40%)** |
| A234 | `moe_gemm` (only the two grouped GEMM launches) | 39.80 / 39.78 | 25.1 ms | **11.4 ms (31%)**: 0.12 ms per launch; routing, alignment, quantization, activation and combine are the remaining 3.3 ms |
| A235 | `gdn_core` (the GDN attention core kernel) | 30.35 / 30.43 | 32.9 ms | **4.3 ms (12%)** against the diagnostics-head control |
| A236 | control on the diagnostics head (hooks on, nothing skipped) | 26.90 / 26.82 | **37.2 ms** | the hooks cost 0.7 ms against the clean head's 36.5; deltas below use 37.2 |
| A239 | `qsa_attn` (the whole QSA attention module on full-attention layers, output zeroed) | 31.21 / 31.21 | 32.0 ms | **5.2 ms (14%)** |
| A240 | `gdn_attn` (the whole GDN attention module on linear-attention layers, output zeroed) | 29.09 / 29.06 | 34.4 ms | **2.8 ms**: less than the core alone (A235, 4.3), so zeroing a block perturbs downstream routing by about a millisecond; read these deltas at ±1 ms |
| A242 | `hc_mix` (both per-layer hyper-connection mixes: combine-norm, LoRA down and up projections, gate mix; the block input becomes the first stream, a zero injection keeps the combine) | 34.76 / 34.76 | 28.8 ms | **8.4 ms (23%)**: the second-largest item, above QSA attention |

Ranking at the placement identity (37.2 ms on the diagnostics head): MoE GEMMs 12.1, hyper-connection mixes 8.4, QSA attention 5.2, GDN attention 3-4, MoE surround 3.3, MoE all-reduces 0.9; the remaining ~4-5 ms is norms, embeddings, sampling and glue. The mixes are 96 per step of about six tiny kernels each at M=1 (combine-norm, down GEMM to lora_rank + injection logits, SiLU, up GEMM, gate mix), i.e. ~15 µs per launch: a fusion target, one Triton kernel per mix.

Against the A236 control: MoE block 15.4 ms (41%), of which the two GEMMs 12.1 ms (33%) and the surround 3.3 ms (9%); GDN core 4.3 ms (12%); MoE all-reduces 0.9 ms (2%); everything else (QSA attention, GDN projections and norm, hyper-connection mixes, norms, sampling, embeddings) about 16.6 ms (45%) in aggregate, none of it a single measured item yet. Data `20260906-tp4-mtp0-a23[2-6]-skip-*-exact-depth-2k-r{1,2}.json`.

So the two Triton block-FP8 GEMMs are the largest single item (11.4 ms) and the non-MoE part of the step is about 21.8 ms (attention, hyper-connections, norms, sampling); A235 (skip `gdn_core`) measures the GDN attention core next. The GEMMs move about 7 MB of expert weights per launch at 2-3 local hits, i.e. ~60 GB/s against a 500 GB/s card, and their tile map is the sweep optimum, so the lever is a decode-specialised kernel with more parallelism per launch (new accumulation order, re-oracled at promotion).

## 17:57 09-06 — offline graph-replay screen: deterministic split-K cuts the MoE block by a third; SWAP_AB does nothing

Card 0, `timing-moe-block-graph-offline.py` under the sweep worktree (diagnostics head plus an XPU `VLLM_XPU_MOE_SWAP_AB` toggle), 48 fused-MoE blocks per graph replay, fresh routing:

| variant | 2 local hits | 3 local hits |
|---|---|---|
| baseline (W13-N32 map) | 0.2106 ms / block | 0.2129 |
| `VLLM_XPU_MOE_SPLIT_K=4` (fp32 partials, fixed-order reduce) | **0.1429** | **0.1658** |
| `VLLM_XPU_MOE_SPLIT_K=8` | **0.1352** | 0.1765 |
| SWAP_AB forced (weights as the MMA M dimension) | 0.2184 | 0.2218 |
| SWAP_AB + split-K 4 | 0.1635 | 0.1846 |

At the server's 2-3 local hits, split-K 4 saves 0.05-0.07 ms per layer, i.e. 2.3-3.3 ms of the 36.5 ms step. A193/A194 had found split-K "exact and neutral" on the 13.4 identity (tensor descriptors are off for quantized weights, so the path was live then too); A237 (split-K 4) and A238 (split-K 8) re-screen it in the server at the placement identity against the A236 control. Log `20260906-moe-block-variant-screen-graph-replay-card0.log`.

## 18:03–18:38 09-06 — split-K in the server at the placement identity: neutral again (closed)

A237 (`VLLM_XPU_MOE_SPLIT_K=4`, `MAX_TOKENS=40`): exact-2K 26.88 / 26.89; A238 (split-K 8): 26.82 / 26.87; the A236 control 26.90 / 26.82; authority hash held on all. The offline graph-replay gain (0.211 → 0.143 ms per block) does not transfer because the offline harness runs the functional path with the flat tuned entry (w13 at BLOCK_N 64), while the server's modular M1 path applies the W13 BLOCK_N 32 phase delta, which already doubles the w13 grid; the remaining per-launch cost is not parallelism-bound. Split-K is closed on this stack for the third time. Lesson for the offline harness: screen through the modular path (or force the phase-delta config) before believing a kernel-variant gain. Data `20260906-tp4-mtp0-a23[78]-splitk*-exact-depth-2k-r{1,2}.json`.

## 19:45–19:55 09-06 — the hyper-connection glue runs on torch fallbacks; the Triton kernels are 10x faster and last-bit different

Offline (card 0, graph replay, `timing-hc-mix-graph-offline.py`): one mix costs 84.7 µs (8.13 ms per step of 96, matching the A242 skip delta of 8.4): the two bf16 projections 35.7 µs (3.43 ms per step against a 2.58 ms bandwidth floor) and the three glue ops 49.1 µs (4.71 ms). The glue is slow because `ops/hc.py` routes every op to the torch reference on XPU (`if x.device.type == "xpu": return _..._torch(...)`, the 2026-08-26 "XPU hyperconnection fallbacks"), a chain of small aten kernels each: combine-norm 30.7 µs, gate mix 12.9, SiLU 5.9. The Triton kernels in the same file, launched on XPU with `launch_pdl=False`, run in 2.8 / 1.1 / 0.8 µs (`timing-hc-glue-triton-vs-torch-graph-offline.py`): about 4.2 ms per step recovered on the mixes, plus the attention-side grouped RMSNorm and the final combine.

They are not bit-identical to the fallbacks: over 150 random cases (M 1/2/4/7, scales 0.5-30, shared and per-branch norm weights; `sweep-hc-triton-vs-torch-equality.py`) the norm outputs differ in 39-84 of 150 cases and the combine in 78, all at the last bf16 bit (max 0.25 at scale 30, 0.016 at scale 1). So switching the glue to Triton is a new-authority change (fp32 rounding order), to be certified the way the lab certifies kernel changes: deterministic across servers, quality profiles, then new output pins. Screen next: A243, the MTP0 placement identity with `VLLM_XPU_HC_TRITON=1` on the diagnostics head (expected ~4 ms per step, ~+12%).

## 19:57 09-06 — host reset #9 during A243's load

The previous boot's journal ends at 19:51:42, seconds after the A243 launch (swap deactivated, supervisor session opened); the machine came back at 19:57 with no kernel trace, the session scratchpad wiped and `/mnt/usb-models` unmounted. Post-reboot routine applied (ntfs-3g remount; four B70s present). A243 (MTP0 placement identity + `VLLM_XPU_HC_TRITON=1` on diagnostics head `7751df34`) had reached its host wrapper only; relaunched through the new repository-resident chain (`tools/q38-run-attempt-chain.sh`, logs under `/mnt/fast-ai/q38-attempt-logs/`).

## 20:20–20:45 09-06 — the launcher strips inherited `VLLM_*`; split-K, screened for real, is +2.4% and exact

- A243 (`VLLM_XPU_HC_TRITON=1` exported at the wrapper level) reproduced the control exactly (26.82 / 26.83, authority hash held): the base launcher `unset`s every inherited `VLLM_*|CCL_*|FI_*|ZE_*|SYCL_*|TRITON_*|PYTORCH_*` variable before starting the server, so only exports printed into the derived launch source survive (the `Q38_*` diagnostics do because they are not on that list). The same applies to the earlier split-K screens (A193/A194 on the headroom identity, A237/A238 here): their switch never reached the workers, which is why "offline positive, server neutral" never made sense.
- A245 (`VLLM_XPU_MOE_SPLIT_K=4` printed into the derived source after the MKLDNN export): exact-2K **27.53 / 27.51** against the diagnostics-head control 26.90 / 26.82, authority `afffd211…` held (the fp32 partials are reduced in fixed order). +2.4%, about 0.9 ms per step, exact. Smaller than the offline 2-3 ms because the server's w13 GEMM already runs the W13 BLOCK_N 32 phase delta. Candidate for certification on the clean branches (cherry-pick `38ca78ba`, per-head verifier hashes, battery, suite, rows); split-K 8 to be screened the same way.
- A244 (`VLLM_XPU_HC_TRITON=1` in the derived source): the API server segfaulted at engine construction (after "Enabled custom fusions", native frames only) before any load; A246 retries it with `PYTHONFAULTHANDLER=1`.

## 20:45–21:02 09-06 — the Triton hyper-connection glue runs on XPU: 31.8 tok/s at MTP0 (+18%), a new-authority lever

- A246 (`VLLM_XPU_HC_TRITON=1` in the derived source, head 7751df34, `PYTHONFAULTHANDLER=1`): no fault this time; the run loaded, captured the decode graph (41 s) and the Triton cache shows the four HC kernels compiled (`_hc_gate_mix_kernel`, `_hc_combine_kernel`, `_hc_combine_norm_kernel`, `_hc_silu_kernel`). Exact-2K **31.81 / 31.81 tok/s** against the diagnostics-head control 26.90 / 26.82 and split-K 4 at 27.53 (a 31.4 ms decode step). A244's segfault at engine construction did not reproduce; it stays filed as a one-off until it recurs.
- Outputs differ from the torch-fallback authority (`86b5b6c7…` vs `afffd211…` at exact-2K; both repeats identical, so the path is deterministic). The offline equality sweep already predicted this: the fused Triton kernels round differently at the last bf16 bit in the mix/combine/norm glue, and on a 2K-token greedy continuation the first differing argmax changes the rest. This is the reference path on CUDA (the torch fallbacks exist only for XPU), so the candidate is a legitimate implementation, not a shortcut — but it is a new authority and must earn it: the quality profile (6/7 exact cases, 25/25 repeat, long context), a deterministic fresh-server pair, then new fixture hashes and re-pinned packets.
- Candidate branches: `q38-placement-clean-v5-splitk-hc` = 09279b6a (clean MTP0 placement + split-K 38ca78ba + HC gate 7751df34) and `q38-placement-mtp1-clean-splitk-hc` = f57d40d7. A252 (packet on 09279b6a, split-K 4 + HC Triton exports, port 19918) runs the quality screen driver (`tools/q38-quality-screen-driver.sh`: quality suite, exact 2K/4K r1/r2 recorded, realistic suite) after A247; the split-K 4 exact certification (A248–A251) follows it.
- Filed: `data/20260906-tp4-mtp0-a246-hc-triton-glue-exact-depth-2k-r{1,2}.json`, `…-a246-identity.txt`.

## 21:02–21:19 09-06 — split-K 8 is neither faster nor exact (closed)

- A247 (`VLLM_XPU_MOE_SPLIT_K=8` in the derived source, same diagnostics head 7751df34): exact-2K **26.81 / 26.83** against the control 26.90 / 26.82 — no gain — and the output hash moved (`934ff3e2…` vs the authority `afffd211…`), unlike split-K 4 (A245, exact at 27.53). The offline replay had predicted 8 ahead of 4 at two hits and behind at three; in the server the extra partials cost what they save, and the reduction no longer reproduces the single-pass accumulation. Split-K stays at 4 for certification (A248–A251). Filed: `data/20260906-tp4-mtp0-a247-splitk8-derived-export-exact-depth-2k-r{1,2}.json`.

## 21:20–21:42 09-06 — A252: the HC-Triton candidate keeps the certified quality profile at 33.1 tok/s exact-2K and 33.6 on the realistic suite

- A252 (clean candidate head 09279b6a = MTP0 placement + split-K 4 + Triton HC glue; both exports in the derived source; `tools/q38-quality-screen-driver.sh`): quality suite **identical to the certified A223 run case by case** — the seven exact cases produce byte-identical outputs (six pass, `code_execution` fails on both, as always), the 16 repeats collapse to one hash, the 2157-token needle is found. Exact-2K **33.12 / 33.15**, exact-4K **33.12 / 33.21** (a 30.2 ms step), realistic suite **33.63** class-balanced median (gate passed, cached_tokens 0 on every row) against 27.65 for the published placement row (+21.6%).
- New authority hashes on this server: exact-2K `bcd3d6ee…`, exact-4K `090d980c…` (the torch-fallback authority is `afffd211…` / `c6193cc6…`). A253 repeats the screen on a fresh server for the deterministic pair; A254 screens the MTP1 candidate f57d40d7 (lossless MTP1 must reproduce the MTP0 hashes). Both run right after A248; the rest of the split-K exact certification follows.
- The first sequencer gate mis-parsed the quality JSON (repeat_case is an object, not a list) and skipped A253/A254 once; the hand comparison above is the gate of record and the runs are re-queued.
- Filed: `data/20260906-tp4-mtp0-a252-hctriton-splitk4-screen-*` (quality, exact-depth 2K/4K r1/r2, realistic suite, identity).

## 21:43–21:55 09-06 — a driver race aborted A248 and cascaded through the queue (fixed)

- The attempt chain handed the packet's frozen client to the launcher as the driver; the launcher starts the driver three seconds after the host wrapper, before the run directory exists, so the client failed at once, wrote the failure file, and the supervisor tore the launch down — removing the RPC directory under the launcher's socket probe (`FileNotFoundError` in the host log). The five launches queued behind it then failed within two seconds on "swap still in use: bytes" while the wrapper's restore was still re-enabling swap. Nothing ran on the GPUs.
- Fixes: `tools/q38-client-driver.sh` waits for the run directory, "Application startup complete" and `/health` before exec'ing the client; the queue (`seq-cert.sh`) aborts on a launch failure instead of cascading and rests 90 s between attempts. A248's state is archived as `…attempt248-failed-2143-driver-race`. Queue order now: A248 (split-K MTP0 battery), A253 (HC fresh pair), A254 (HC MTP1 screen), A249, A250, A251.

## 22:04–22:20 09-06 — split-K 4 on the clean heads was not exact: the gate follow-up was missing (heads rebuilt)

- A248 (clean MTP0 placement head + split-K commit 38ca78ba = 6a79c56d, `VLLM_XPU_MOE_SPLIT_K=4`): the frozen client's exact-depth gate failed — 2K `ad4c0af7…` and 4K `bf25b9d1…` against the authority `afffd211…` / `c6193cc6…`, at 27.88 / 27.88 (2K) and 27.82 / 27.81 (4K); quality, short and both repeats otherwise clean. A245 had held the authority with the same env on the diagnostics head 7751df34.
- Cause: the diagnostics branches carry a follow-up to the split-K commit, 07131f02 ("gate on expanded rows, `VLLM_XPU_MOE_SPLIT_K_MAX_TOKENS` default 40"), which the cherry-pick onto the clean heads did not include; the original gate (`M <= 4`) enables split-K on a different subset of launches, and that subset does not reproduce the single-pass accumulation. With 07131f02 the fused MoE file on the clean heads equals the diagnostics head's apart from the `_q38` hook lines.
- Rebuilt heads (v2): `q38-placement-clean-v5-splitk-v2` 82b9f9cf, `q38-placement-mtp1-clean-splitk-v2` 893e1ccc, and their Triton-HC variants `…-hc-v2` 2aa369a6 / b0836afb; verifier repinned (790f48b3…) to the four v2 heads (v1 heads dropped). Packets A259–A262 (split-K v2 certification), A263–A265 (HC screen, fresh pair, MTP1 screen on the v2 HC heads); the HC certification maker now targets A266–A269. A252's 33.1/33.6 result stands as a screen on the v1 HC head; the certification lineage uses the v2 heads so the only authority change is the HC glue.
- Queue (`seq-cert-v2.sh`, abort on launch failure): A259 → A263 → A264 → A265 → A260 → A261 → A262. Filed: `data/20260906-tp4-mtp0-a248-splitk4-oldgate-nonexact-exact-depth-{2k,4k}-r{1,2}.json`, `…-a248-identity.txt`.

## 22:13–22:40 09-06 — split-K 4 is exact at 2K but not at 4K (excluded); the HC lineage goes HC-only

- A259 (v2 head 82b9f9cf with the gate follow-up): exact-2K **27.93 / 27.95** with the authority `afffd211…` held, but exact-4K `92e91dc9…` against `c6193cc6…` (27.82 / 27.88); quality, short and both repeat pairs clean. Split-K's fixed-order partial sums do not reproduce the single-pass accumulation; the 2K agreement (also A245) was luck of the token stream, not a property. Split-K is closed for the exact ladder, and it is kept out of the new-authority lineage so that lineage carries exactly one justified numerics change (the Triton HC glue, the reference path on CUDA). Filed: `data/20260906-tp4-mtp0-a259-splitk4v2-4k-nonexact-exact-depth-{2k,4k}-r{1,2}.json`.
- HC-only heads: `q38-placement-clean-v5-hc` 8d7d6fd8 (cb59004b + 7751df34) and `q38-placement-mtp1-clean-hc` 62219122 (005dc578 + 7751df34); `hc.py` is the only file that changes, the MoE files keep the certified hashes. Verifier repinned (20546ff1…) to these two heads; every split-K head is dropped from the accepted set.
- Queue `seq-hc.sh` (abort on launch failure): A266 (MTP0 quality screen, port 19936) → A267 (fresh-server pair, 19937) → A268 (MTP1 screen, 19938). The certification maker now derives A269–A272 from the certified placement generators (A223/A227/A225/A226) with the HC export, the HC heads and the pair's hashes.

## 22:35–22:58 09-06 — A266: the HC-only candidate holds the certified profile at 32.6 tok/s exact-2K and 32.85 on the suite

- A266 (head 8d7d6fd8 = certified MTP0 placement head + 7751df34, `VLLM_XPU_HC_TRITON=1` only): quality suite identical to A223 case by case (all seven exact-case outputs byte-identical, one repeat hash over 16 runs, needle found). Exact-2K **32.64 / 32.59** with hash `86b5b6c7…` — the same hash A246 produced on the diagnostics head, so the HC path is deterministic across heads — and exact-4K **32.57 / 32.65** (`b89822ce…`); realistic suite **32.85** class-balanced median, gate passed, cached_tokens 0 (published placement row: 27.65, +18.8%). A 30.6 ms step against 36.2 ms on the same head without the flag.
- Certification packets A269 (MTP0 battery, port 19939), A270 (MTP0 suite, 19940), A271 (MTP1 battery, 19941), A272 (MTP1 suite, 19942) derived from the certified placement generators with the HC export, the HC heads, verifier 20546ff1… and the frozen client's exact-depth literals repinned to `86b5b6c7…` / `b89822ce…`. `seq-cert-hc.sh` waits for the screens and certifies MTP0 only if A267 (fresh server) reproduces both hashes, MTP1 only if A268 (lossless MTP1) reproduces them as well; the gate decisions are written to `seq-cert-hc.gate`.
- Filed: `data/20260906-tp4-mtp0-a266-hctriton-screen-*` (quality, exact-depth 2K/4K r1/r2, realistic suite, identity).

## 22:59–23:50 09-06 — the HC lineage's fresh-server pair holds, and lossless MTP1 with the HC glue reaches 37.4 tok/s

- A267 (fresh MTP0 server, head 8d7d6fd8): exact-2K **32.61 / 32.56** and exact-4K **32.63 / 32.60** with A266's hashes (`86b5b6c7…` / `b89822ce…`) reproduced token for token, realistic suite **32.84**, quality profile identical to A223. The new authority is deterministic across servers.
- A268 (head 62219122 = lossless MTP1 placement head + 7751df34): the same two hashes — one publisher MTP token stays lossless under the HC glue — at exact-2K **36.47 / 36.49**, exact-4K **36.41 / 36.42**, realistic suite **37.45** class-balanced median (gate passed, cached_tokens 0) against the published 31.93 (+17.3%); quality profile identical to A223.
- Both `seq-cert-hc.sh` gates pass: A269/A270 (MTP0 battery + suite) and A271/A272 (MTP1 battery + suite) run in sequence on the HC heads with the frozen clients pinned to the new hashes. Filed: `data/20260906-tp4-mtp0-a267-hctriton-screen-fresh-*`, `data/20260906-tp4-mtp1-a268-hctriton-screen-*`.

## 23:52–00:40 09-07 — Triton-HC MTP0 certified and approved: 32.898806 tok/s (LocalMaxxing `cmtqqyulr006fpa01erfuiri8`)

- A269 (frozen-client certification battery on head 8d7d6fd8, client pinned to the lineage's hashes): every gate passed — recovery, quality (6/7 with the inherited `code_execution` miss, byte-identical outputs), short-repeat, exact-2K **32.58 / 32.56** (`86b5b6c7…`) and exact-4K **32.58 / 32.62** (`b89822ce…`) same-boot repeats, runtime verifier — with a valid stop. Summary: `data/20260907-tp4-mtp0-a269-fresh-repeat-deterministic-summary.json`; exact-2K pair summary across A266, A267 and A269 (six rows, all identical): `data/20260907-tp4-mtp0-a266-a267-a269-exact-2k-pair-summary.json`.
- A270 (fresh server, fixed cold realistic suite once): **32.898806 tok/s** class-balanced median (gate passed, cached_tokens 0; tokSTotal 31.69, TTFT median 0.51 s) against 27.640875 for the approved placement row (+19.0%). Attestation `data/20260907-tp4-mtp0-a270-promotion-attestation.json` (all six gates true; profile `…-mtp0-fullgraphdet-4352-placement-hctriton-realistic-v1`, identity `…-hctriton`), payload `data/20260907-tp4-mtp0-a270-localmaxxing-payload-queue.json`, response `data/localmaxxing-responses/qwen38-flash-next-fp8-tp4-mtp0-placement-hctriton-realistic-20260907.json`: LocalMaxxing run **`cmtqqyulr006fpa01erfuiri8` approved**.
- The attestation and the row's notes state the authority change explicitly: the Triton glue rounds the hyper-connection mix/combine/norm at the last bf16 bit, so the pins are `86b5b6c7…` / `b89822ce…` rather than `afffd211…` / `c6193cc6…`; within the lineage every pin is deterministic across three fresh servers and the quality profile equals the certified rows case by case.

## 00:34–01:30 09-07 — Triton-HC lossless MTP1 certified and approved: 37.045844 tok/s (LocalMaxxing `cmtqspsy00092pa01kli5htlb`)

- A271 (frozen-client battery on head 62219122, pins repinned to the lineage's hashes): every gate passed — exact-2K **36.43 / 36.47** (`86b5b6c7…`), exact-4K **36.37 / 36.36** (`b89822ce…`), 6/7 quality with the inherited miss, 16/16 repeat, exact needle, valid stop. Pair summary across A266 (MTP0), A268 and A271 (MTP1): six rows, all identical — MTP1 stays lossless within the new authority. Summary `data/20260907-tp4-mtp1-a271-fresh-repeat-deterministic-summary.json`.
- A272 (fresh server, fixed cold realistic suite once): **37.045844 tok/s** class-balanced median (gate passed, cached_tokens 0; tokSTotal 35.79, TTFT median 0.55 s) against 31.929484 for the approved placement row (+16.0%) and 37.45 on the A268 screen. Attestation `data/20260907-tp4-mtp1-a272-promotion-attestation.json` (six gates true), payload and response filed; LocalMaxxing run **`cmtqspsy00092pa01kli5htlb` approved**. Together with the MTP0 row (`cmtqqyulr006fpa01erfuiri8`, 32.898806) the Triton-HC lineage is fully certified: five servers reproduce the pins, the quality profile equals the certified rows case by case, and every artifact discloses the authority change.
- Publication: guide `repro/qwen38-flash-next-fp8-tp4-mtp1-hctriton-b70-37tps-20260907/` (lab-replay; identity, pins, evidence manifests, replay tooling adapted from the placement guide with the Triton-HC series in the identity chain), candidate package, guide and package catalogs, family manifest measurements `…-mtp0-placement-hctriton-context4k-a269` / `…-mtp1-placement-hctriton-context4k-a271` with the hero moved to the MTP1 row, results packet section, recipes and repro index rows, model and family pages regenerated. The 31.93 row remains the fastest bit-identical (torch-fallback authority) line and its guide is untouched.

## 01:30–01:54 09-07 — the Triton-HC guide replays: attempt 273, 12/12 outputs identical, 37.433041 tok/s

- `run-record-gate.sh` (REPRO_ATTEMPT=273) on the originating host: identity chain verified (placement and Triton-HC series, bundles, tags, trees), packet derived from the frozen A272 packet, server launched through the host-controlled launcher, the fixed cold suite sent once: **12/12 output hashes equal to the record, every gate equal, 37.433041 tok/s** class-balanced (record 37.045844). The first derivation had aimed at the record's run directory because the guide's replay maker still carried the launcher's `ATTEMPT=` literal from the placement guide; fixed and committed before the passing replay. Evidence: `evidence/a273-record-gate.log`, `evidence/a273-record-gate-replay.sha256`, `data/20260907-tp4-mtp1-a273-record-gate-replay-realistic-suite-v1-result.json`.

## 01:55–02:17 09-07 — MTP2 on the Triton-HC head: lossless, still slower than MTP1 (closed)

- A274 (head 62219122, two speculative tokens, HC export in the derived source): exact-2K r1 23.44 / r2 33.03 tok/s with the lineage authority `86b5b6c7…` held on both, against MTP1's 36.43 / 36.47 (A271). As on the placement identity (A228: 22.40 / 30.94 against 33.2), the third-token verify step costs more than the extra accepted token returns; the cheaper HC step does not change the balance. Filed: `data/20260907-tp4-mtp2-a274-hctriton-exact-depth-2k-r{1,2}.json`.

## 02:18–04:07 09-07 — graph-step decomposition with the Triton HC glue live (A275–A280)

Skip switches on the diagnostics head 7751df34 with `VLLM_XPU_HC_TRITON=1` printed into the derived source; exact-2K conventional 99-interval rates, two requests per server (deterministic pairs unless noted); step = 1000 / tok/s.

| run | skipped (`Q38_DIAG_SKIP`) | exact-2K r1 / r2 | step | delta vs the 31.4 ms control |
|---|---|---|---|---|
| A275 | control (hooks on, HC glue live) | 31.82 / 31.84 | **31.4 ms** | the torch-fallback control was 37.2 ms (A236): the Triton glue took 5.8 ms out of the step |
| A277 | `moe_gemm` (the two grouped GEMM launches per MoE layer) | 51.28 / 51.33 | 19.5 ms | **11.9 ms (38%)**, unchanged from 11.4 before: 96 launches at 0.124 ms |
| A276 | `moe` (whole routed-expert block) | 61.29 / 61.12 | 16.3 ms | **15.1 ms (48%)**: GEMMs 11.9 + surround (routing, alignment, quantization, activation, combine) **3.2 ms** |
| A279 | `qsa_attn` (whole QSA attention module on full-attention layers) | 37.93 / 37.97 | 26.4 ms | **5.1 ms (16%)** |
| A280 | `gdn_attn` (whole GDN attention module on linear-attention layers) | 34.44 / 34.45 | 29.0 ms | **2.4 ms (8%)** |
| A278 | `gdn_core` (the GDN core kernel only) | 31.02 / 31.96 | — | inconclusive: no saving and the two repeats hash differently (`c6f65cbf` / `1d998d61`), so the skip left nondeterministic state; the earlier 4.3 ms (A235) is not reproduced with the glue live |

Attribution of the 31.4 ms step: MoE 15.1 (GEMMs 11.9, surround 3.2), QSA attention 5.1, GDN attention 2.4, the remaining hyper-connection glue about 2.6 (8.4 under torch fallbacks minus the 5.8 the Triton kernels removed; A281 measures it directly), and about 6.2 ms unattributed (norms, residual streams, PLE and embedding gathers over UVA, lm_head and sampling, graph launch floor). Ranking for the next lever: the MoE GEMM launches remain the largest slice and run well below the card's weight bandwidth (≈1.5 GB of FP8 expert rows per rank per step would take ≈3.3 ms at full bandwidth against 11.9 measured), then QSA attention, then MoE surround fusion. Filed: `data/20260907-tp4-mtp0-a27{5,6,7,8,9}-hctriton-*-exact-depth-2k-r{1,2}.json`, `…-a280-hctriton-skip-gdn-attn-…`.
- A281 (`hc_mix` skipped with the Triton glue live): 34.84 / 34.78 tok/s, a 28.7 ms step — the hyper-connection mix/combine now costs **2.7 ms** (8.4 under the torch fallbacks), which closes the attribution: MoE 15.1, QSA 5.1, HC 2.7, GDN 2.4, and 6.1 ms in norms, residual streams, PLE/embedding gathers, lm_head, sampling and the graph launch floor. Filed: `data/20260907-tp4-mtp0-a281-hctriton-skip-hc-mix-exact-depth-2k-r{1,2}.json`.

## 04:30 09-07 — next lever: the MoE GEMM K loop is latency-bound and tile-invariant; prefetch inside the kernel is the exact-preserving move

- The M2 tile sweep (`data/20260906-moe-m2-tile-config-sweep-card0.json`, 37 configurations) lands every BLOCK_N (32–128), warp count (4/8) and stage count (2–4) on the same event-timed cost: ~0.38 ms for the W13 launch (N=1280, K=2560) and ~0.17–0.22 for W2 at ten local hits; the tuned map's choice (W13 at BLOCK_N 32) is a few percent, not a regime. `num_stages` has no measurable effect, so the Triton XPU backend is not pipelining this loop.
- The server pays 11.9 ms for 96 launches (0.124 ms each) moving ~6–8 MB of expert rows per launch: ~55 GB/s against a card that streams several hundred. Each program walks K in twenty serial 128-wide steps; per step it loads a 4 KB B tile, the A tile and two scale vectors and issues one `tl.dot` — a dependent load→compute chain of ~5 µs per step, which is exactly 0.1 ms per launch. More programs (smaller tiles) cannot shorten a serial chain, which is why the sweep is flat and why split-K (which shortens the chain) was the only thing that moved it — at the cost of the accumulation order.
- Exact-preserving lever: software-pipeline the loop by hand. In the block-FP8 path the per-block update is `accumulator += tl.dot(a_k, b_k) * a_scale_k[:, None] * b_scale_k[None, :]`; issuing the loads of block k+1 (A tile, B tile, both scale vectors) before the dot of block k changes only the schedule, not the arithmetic, so the outputs stay bit-identical to the lineage authority. Gate it as a constexpr (`PREFETCH_K`) selected from the tuned map so the certified rows are untouched until it is screened: offline first (`timing-moe-gemm-events-offline.py` on card 0 in an overlay worktree, M=1/2 ep-like lines, baseline vs prefetch), then a diagnostics-head screen with the exact-2K hash, then the ladder. Expected ceiling if the loop reaches two loads in flight: roughly half of the 11.9 ms.
- Offline result (card 0, `timing-moe-gemm-events-offline.py`, worktree branch `q38-moe-kprefetch` on the skips head; `PREFETCH_K` carried by a tuned-map copy): the hand-pipelined loop is **slower** at every regime — M=1 ep-like W13 0.264 ms against 0.220 baseline (W2 0.142 vs 0.143), M=1 all-local 0.513 vs 0.387, M=2 ep-like 0.271 vs 0.225. So the serial K loop is not the memory-latency chain the flat tile sweep suggested (doubling the live tiles costs more than the overlap returns), and the 0.2 ms per W13 launch at two hits has to be attributed inside the kernel before another variant is written: candidates are the fp8→bf16 conversion feeding `tl.dot` on Xe2 (no native fp8 XMX path), the per-program prologue (sorted-token and expert-map loads), and the event-hook distortion itself (graph replay puts the whole MoE block at 0.21 ms/layer at two hits, below the event-timed sum of the two GEMMs). Next step: a Triton-level micro-probe of the same kernel with the dot replaced by a bf16 dot on pre-converted weights, and a launch with K=128 (one iteration) to isolate the prologue. The branch stays as a reference; nothing of it enters the certified heads.
- Graph-replay attribution (card 0, `timing-moe-block-graph-offline.py` with K from the environment, M=1, two local hits): the whole MoE block is **0.211 ms per layer at K=2560 and 0.051 ms at K=128**, so the K loop of the two GEMMs is ~0.16 ms per layer (≈9.8 MB of expert rows, ≈61 GB/s) and the K-independent floor of all the block's kernels is 0.05 ms. The event-timed harness adds a fixed ~0.14 ms per launch (K=128 launches cost 0.14 ms under it), which is why the tile sweep looked flat: it was measuring hook overhead. The `PREFETCH_K` variant is slower under replay as well (0.264 ms per block), so the negative stands. Consequences: (1) the tile sweep has to be redone under graph replay; (2) the loop streams 128-byte row segments per program per iteration (B tiles of 32 rows × 128 K-bytes from a (E, N, K) row-major layout) — a load-time repack of expert rows into tile-contiguous order (values unchanged, so bit-identical outputs) is the structural candidate if the replay sweep confirms the loads are the limit.

## 04:15–05:10 09-07 — the graph-replay tile sweep found a 29% MoE-block cut offline that the server does not show (A282 negative)

- Graph-replay sweep on card 0 (`data/20260907-moe-m1-tile-config-sweep-graph-replay-card0.json`, whole MoE block per layer, M=1, two local hits): the current M=1 entry (BLOCK_N 64, 8 warps, W13 at N32) costs 0.211 ms; **16 warps at BLOCK_N 64 costs 0.151** (W13 N16/32/64 and stages 3/4 all equal); 4 warps 0.296, 32 warps 0.202, BLOCK_N 32 at 8 warps 0.161, BLOCK_N 128 0.41. With a full rank of rotating weights (48 sets, 0.5 GiB free) the same two numbers hold (0.2105 / 0.1505). For M=2 the 8-warp entry stays best (16 warps 0.286 against 0.248), and the map lookup picks the nearest key, so M=2 (the MTP1 verify step) shares the M=1 entry: a 16-warp map is an MTP0-line lever only.
- A282 (HC diagnostics head, map `configs/moe-m1-w13-n32-w16` = the certified map with the M=1 entry at 16 warps, sha `39a1cce2…`, printed into the derived source; the server log confirms the folder): exact-2K **30.46 / 30.36 tok/s** with the lineage hash `86b5b6c7…` held, against the 31.82 / 31.84 control (A275) — 1.5 ms per step **slower**, where the replay predicted 2.9 ms faster. Exact, but a negative; the map stays uncertified. Filed: `data/20260907-tp4-mtp0-a282-hctriton-w16-map-exact-depth-2k-r{1,2}.json`.
- The isolated-block replay therefore does not predict the server step for this knob (the server interleaves attention, GDN and the glue between MoE blocks, runs the modular Triton experts path rather than `fused_experts`, and routes real tokens through the placement). The next pair (A283 control, A284 16-warp map, both with `Q38_MOE_GEMM_EVENT_TIMING=1` and the step-timing snapshot) measures the GEMM launches inside the server under identical hooks, which settles whether the launches sped up and something else paid for it, or whether the offline tool is simply wrong for this kernel path.
- A283 (control map + `Q38_MOE_GEMM_EVENT_TIMING=1` + layer/step timing on the full-decode-graph packet): the worker died at graph capture — `wait cannot be called for a queue which is recording to a command graph` — so the supervisor reported an identity change (rc 70) before the driver ran. The GEMM event hooks record and synchronize per launch, which the XPU graph capture forbids; the earlier sub-op timings (A141/A142/A160/A162/A192/A230) were all on the eager lineage. In-server per-launch GEMM attribution under the graph therefore needs a capture-safe probe (Level Zero tracing, or a graph-replay harness that reproduces the server's modular-experts launch sequence rather than `fused_experts`). A284 was cancelled. The 16-warp map is closed on the server measurement alone (A282: exact, 1.5 ms/step slower); the replay-versus-server discrepancy is the open question for the MoE GEMM lever.
