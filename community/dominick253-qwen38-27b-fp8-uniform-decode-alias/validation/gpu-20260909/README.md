# Bounded two-B70 runtime review — September 9, 2026

Verdict: **do not promote the classifier patch as a verified incident fix**.
The actual-source classifier checks pass, but tiny-prompt output walls remain.
Contributor dominick253's 6–24-hour incident is not reproduced causally or
resolved by this short review. Upstream classifier credit: allenzz-dev.

## Executed comparison

Host `steve-TURIND8-2L2T`, two B70 GPUs. Images and patch hashes are in the
[parent validation record](../README.md); each arm records its immutable image.
R50 MTP1 strict launcher, TP2, FP16 KV, prefix cache disabled, XPU graphs
disabled, max model length 4096, max sequences 4, max batched tokens 1024.
These differ from the contributor's long-session settings. Localhost port
18124 only; all review model containers stopped after testing.

| Arm | Normal strict suite | Additional tiny/mixed screen |
| --- | --- | --- |
| Original R50 | Quality and canaries pass | 2/24 fail: repeated one-token prompt produces 64 exclamation tokens |
| Patched R50 | Quality and canaries pass; 12/12 complete token arrays exactly match original | Same 2/24 failures |
| Patched, compilation disabled | Not run: diagnostic probes only | 1/24 fails: second sequential one-token prompt produces same wall |

The third arm explicitly sets compilation mode 0 and cudagraph mode NONE;
it is not a qualified workaround. Candidate-repeat was aborted after the
candidate failure. No multi-hour soak ran within the requested bounded review.
Normal-suite parity must not be interpreted as a pass for the entire campaign.

The screen uses integer-token tiny prompts, arithmetic and an operations
paragraph, eight sequential calls and sixteen mixed calls per arm. Saved
responses include complete token arrays and request settings. Repetition is
a hard failure; cross-batch identity differences are diagnostic. The same
screen was used for all arms, without relaxing checks after failure.

## Evidence and replay

- `baseline-vs-candidate.json`: complete normal-suite token-array comparison.
- Each arm directory: `run.json`, `probes.json`, GPU postflight log; baseline
  and candidate additionally retain strict performance, canary and identity
  records. Probe timestamps give actual run duration.
- `preflight.log`: image contract and all 66 model shards/metadata verified.
- `gpu-preflight-launcher-permissions.log`: both GPU ordinals and XCCL pass.
  Each arm's manual postflight also passes both GPUs and allreduce result 2.
  Initial diagnostic invocation mistakes (hostname rendezvous, then missing
  pidfd capability) were corrected to match launcher permissions before runs.
- Original raw server logs remain under
  `/mnt/fast-ai/bench-results/pr45-review-20260909T0130Z` on this host.

Run `python3 ../run_gpu_review.py --help` from this directory for supervisor
arguments. The immutable images and model files must already exist. The
supervisor fails closed, stops its model container, and aborts later arms on
failure. Failed arms here received explicit manual health checks because the
normal success-path postflight is skipped after an exception.

Next: isolate the persistent tiny-prompt/MTP failure before recommending the
patch; then repeat fresh-server qualification and the contributor's actual
long-session workload. The supplied diff has no companion microbatch guard.
