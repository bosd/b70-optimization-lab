# Maintainer validation — 2026-09-08

The actual R50 classifier accepts six prefill shapes as decode before the
patch and rejects them afterwards. All 15 checks pass before/after with their
respective expectations, independently against both source copies:

- `/workspace/vllm/vllm/v1/worker/gpu_model_runner.py` (editable checkout,
  selected by the image's default working directory);
- `/opt/venv/lib/python3.12/site-packages/vllm/v1/worker/gpu_model_runner.py`
  (installed copy selected with working directory `/`).

The test extracts the real method using Python's AST; it does not import the
GPU runner or substitute an independently written classifier. Cases cover
MTP1/MTP2 tiny prefills, chunk and prefix-cache tails, mixed batches, one-token
prompts, the prompt/decode boundary, normal/speculative decode, inactive padded
rows, mismatched shapes and capture overrides without an initialized batch.
Assertions fail the image build. Both copies are patched to avoid a working
directory change silently bypassing the fix.

## Identity and credit

- Contributor: [dominick253](https://github.com/dominick253), incident report
  and R50 adaptation, [lab PR #45](https://github.com/steveseguin/b70-optimization-lab/pull/45)
  at `f12e834cf3eb53a03ce4eae46ae54029b51b86d6`.
- Classifier fix: [allenzz-dev](https://github.com/allenzz-dev),
  [vLLM PR #53059](https://github.com/vllm-project/vllm/pull/53059), reviewed
  at `3462586be8f1f6d8c9535b1fd41e26c676fe2e75`; open at review time.
- Submitted patch SHA256:
  `2a8c7ca4ea6b1c782a89074d0e3277323f78251535a537a6e044124a829dafbb`.
- Local R50 base image ID:
  `sha256:2932e495b560e79c6301f5cc64584af928a2260f0d0d19c145142b2ef35860d3`.
- Built candidate image ID:
  `sha256:4bb40c00826d3adeb577306afe8d7a6836eaef61d33e1e97a99b74ea85081fb4`.
- Candidate tag:
  `neural-download/vllm-openai-xpu:qwen38-r50-uniform-decode-fix-review-20260908`.
- Lab follow-up: actual-source tests, both-installation candidate build,
  documentation corrections and bounded two-B70 GPU comparison.

## Replay on a host with the recorded local base

From the repository root:

```bash
docker build --network=none \
  --build-arg BASE_IMAGE=sha256:2932e495b560e79c6301f5cc64584af928a2260f0d0d19c145142b2ef35860d3 \
  -f community/dominick253-qwen38-27b-fp8-uniform-decode-alias/validation/Dockerfile \
  -t neural-download/vllm-openai-xpu:qwen38-r50-uniform-decode-fix-review-20260908 \
  community/dominick253-qwen38-27b-fp8-uniform-decode-alias
```

Expected build output: four `PASS: 15 actual-source cases` lines (stock and
fixed for each copy), with both patch applications succeeding. This ran with
network disabled and no GPU device exposure. It is a local candidate build,
not a published image or clean-host reproduction claim.

## Limits and next gate

The [September 9 GPU record](gpu-20260909/README.md) includes real two-B70
baseline and candidate runs: the normal strict suite passed with 12/12 exact
complete token arrays, but both failed two of 24 tiny/mixed probes with
exclamation walls. A compilation-disabled candidate diagnostic also failed
(one of 24 probes). The patch is **not promoted or a verified incident fix**.
No multi-hour soak or fresh candidate repeat was completed after these failures.
Historical images and recipes were preserved. The submitted patch does not
contain the microbatch guard described in its original prose; none was adopted.
