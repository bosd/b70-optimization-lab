# GDN one-token prefill follow-up

**Bounded local fix validated:** 120/120 diagnostic probes pass; two fresh
compiled MTP runs pass quality/canaries and match all 12 normal-suite complete
token arrays, also matching the original baseline. All containers stopped;
both GPUs and XCCL pass postflight. No production/long-soak promotion.

This isolates a second local defect, not the submitted classifier patch or
the contributor's multi-hour incident. Preregistration and abort gates are in
[the follow-up plan](../priority-followup-plan.md).

## Mechanism and scope

The R50 GDN metadata builder calls `split_decodes_and_prefills` with its default
`treat_short_extends_as_decodes=True`. A fresh one-token prompt therefore takes
the recurrent decode path, which reads existing convolution and SSM state.
`KVBlockZeroer` explicitly skips non-`AttentionSpec` layers, including Mamba,
so its general block-zeroing path does not initialize those states.

The local [patch](../gdn-short-prefill-candidate.patch) passes
`treat_short_extends_as_decodes=m.is_prefilling is None`: target batches with
phase metadata route fresh/short prefills through the initializing prefill
kernels. Metadata-less draft/capture callers retain compatibility behavior.
The patch does not change prompts, weights, numerical kernels, precision or
sampling; it does not repair general Mamba block-zeroing omissions.

This delta is maintainer follow-up. The prior classifier fix remains credited
to allenzz-dev and its R50 adaptation/incident packet to dominick253.

## Validation status

- Actual-source helper and GDN call: eight CPU cases, stock/fixed expectations,
  independently against both editable and installed source copies.
- Operator census: six production W8A16 shapes plus actual FP16 head. M=1..4
  repeats were stable; row-zero values match across M=1..4. Four W8A16 shapes
  retain known nondeterminism at larger M, beginning at 168. This is not a
  general batch-invariance pass. Full matrices are retained in `operators/`.
- Compilation-disabled, MTP-disabled control: 3/24 tiny/mixed probes fail
  with 64 exclamation tokens, proving MTP is unnecessary for the local symptom.
- Same control plus GDN phase guard: 24/24 probes pass with no sequential
  repeat drift.
- Two fresh compiled MTP servers: each passes 24 probes before and 24 after
  the complete strict quality/canary suite. All 12 complete normal-suite token
  arrays match the original baseline and each other. All 24 probe arrays
  also match between fresh servers both before and after quality. See
  [screen summary](screen-summary.json),
  [baseline comparison](baseline-vs-gdn-mtp.json), and
  [fresh-repeat comparison](gdn-mtp-fresh-repeat-comparison.json).

Each arm retains complete requests/responses/token IDs, run identity and
postflight. The unchanged screen is diagnostic, not a long soak or semantic
quality oracle. Normal strict-suite evidence is retained under each MTP arm's
`strict/` directory. No speed or production promotion is claimed.

## Identity and replay

- Base classifier candidate:
  `sha256:4bb40c00826d3adeb577306afe8d7a6836eaef61d33e1e97a99b74ea85081fb4`.
- GDN phase-guard candidate:
  `sha256:334c353ffc543eaea2de85d25d947ab5a0db36b9cfa043d0ed7d849627662e81`.
- GDN patch SHA256:
  `4f911100601e79b1bd2e130cfff2d424169696e0a0a28be4f922bf54e9557ab0`.
- Source runtime: vLLM `0.27.2rc1.dev77+gac7509e2b`, XPU kernel
  `1e90ffa672ba02f17a909da11838a4c55b199783`, two B70s on `steve-TURIND8-2L2T`.
- Build [Dockerfile.gdn](../Dockerfile.gdn) using the community packet as
  context. Both source copies must pass `--expect-stock`, patch application,
  and `--expect-fixed`; no GPU exposure is needed during this build.
- Run [the supervisor](../run_gpu_review.py) with `--arms gdn-target-only
  gdn-mtp gdn-mtp-repeat`, an unused `--out` and the verified `--model-dir`.
  Exact image IDs are pinned; these local images are not public release assets.
- Original full logs and caches:
  `/mnt/fast-ai/bench-results/pr45-followup-20260909T0226Z`.

## Remaining gates

The contributor's 6–24-hour workload and exact FP8-KV/prefix-cache settings have
not been reproduced. Four-GPU model replay is unavailable on this two-card
host. Neither limitation can be converted into a pass by this bounded review.
The lane's full promotion matrix also requires two matched-image MTP0 strict
oracle runs; this follow-up ran only a diagnostic MTP0 control. The existing
production recipe and score remain unchanged.
