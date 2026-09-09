# Qwen3.8-27B FP8 vLLM XPU (R50 lineage): shape-aliased prefill silently skips GDN state writes → degenerate output walls

> **Read [STATUS.md](STATUS.md) first.** This is a `community-reported`
> contribution: an incident analysis and patch adoption from a production
> two-B70 host. It is not a lab result and not a promoted recipe.

## What this is

A root-cause match for a degradation the R50/R187 vLLM XPU lane family is
vulnerable to: after hours of real multi-session uptime, the server emits
degenerate single-token walls (`!!!!!`, `00000…`, `oooooo…`, `||||…`) while
health, throughput, and short probes stay clean. Restart cures it; it returns.

**Mechanism (upstream [issue #53051](https://github.com/vllm-project/vllm/issues/53051)):**
`GPUModelRunner._is_uniform_decode` classifies a batch as uniform decode by
shape only. With speculative decoding, `uniform_decode_query_len = 1 +
num_spec_tokens`. Any prefill step that schedules exactly that many tokens per
request (tiny prompts, chunked-prefill chunk tails, prefix-cache hit tails,
mixed batches) aliases the uniform-decode shape. The step then dispatches into
the decode/cudagraph path with capture-time metadata whose GDN
recurrent-state indices are null/stale, so the kernels' null guards silently
skip the recurrent-state writes. Zeroed state → degenerate logits walls. The
victim varies with allocator layout (some runs poison a persistent tensor, e.g.
`conv1d.weight`, which then stays corrupt while fresh short probes look clean)
— which explains both the long dwell and why restarts cure it.

**Fix (upstream [PR #53059](https://github.com/vllm-project/vllm/pull/53059), open):**
after the shape test passes, additionally require every request to be past its
prompt before calling the batch a uniform decode:

```python
input_batch = self.input_batch
return bool(
    (
        input_batch.num_computed_tokens_cpu[:num_reqs]
        >= input_batch.num_prompt_tokens[:num_reqs]
    ).all()
)
```

Full diff: [`reported/vllm-gpu-model-runner-uniform-decode-alias.patch`](reported/vllm-gpu-model-runner-uniform-decode-alias.patch)
(47 lines; also carries a companion microbatch veto guard, see STATUS Known
Issues — that part is contributor-added, not upstream).

Regression test: [`reported/test_is_uniform_decode_red_green.py`](reported/test_is_uniform_decode_red_green.py)
extracts the classifier from both files and runs 14 cases — the 5 aliased
shapes must fail on stock (RED) and pass on patched (GREEN). Contributor run:
both PASS.

## Why this lane should care

- The lab's [2026-08-22 chunked-prefill corruption finding](../../experiments/qwen38-27b-b70/notes/2026-08-22-qwen38-longkv2-closure-and-chunk-corruption-finding.md)
  (`B70_QWEN3!!!!…` after a multi-chunk prefill dose, mitigated by
  `VLLM_XPU_GDN_SPEC_PERSISTENT_SCRATCH=0`) shows the same end signature and
  the same GDN-state-write theme from a different trigger. Whether the aliased
  prefill and the chunk dose are the same mechanism is an open question — see
  STATUS.
- The R187 whole-graph compile (`splitting_ops=[]`) may avoid this trigger
  the same way it avoids the depth-2 phantom (it avoids, does not fix,
  upstream). A 2-token prompt under the strict harness on both compile modes
  would settle it.
- Deployment detail that cost real debugging time: in the R50-lineage image
  the live module is the **editable install** at
  `/workspace/vllm/vllm/v1/worker/gpu_model_runner.py`; the `/opt/venv`
  site-packages copies are shadowed. Patching site-packages does nothing.
  A bind-mount over the editable path (read-only) + launcher grep assert
  survives container recreation; keep the stock copy for rollback.

## Incident evidence (contributor host, summarized in STATUS)

- 2026-09-07→09-08: degenerate walls after 6–24 h dwell under real 3–4
  concurrent-session agent traffic; incident-window screenshots ~00:48–01:02
  EDT 2026-09-08 show a ~40-line single-character wall and a full-panel zero
  wall in one session.
- Post-fix: clean startup/health/alias, exact arithmetic and counting smokes,
  streaming `!!!!!` detector zero events through soak start. Soak in progress;
  controlled on-demand reproduction NOT RUN.

## Status

`community-reported` — incident analysis + upstream-fix adoption with a
RED/GREEN classifier test. No rates are claimed. See STATUS.md for the
boundary questions that would raise the evidence level.
