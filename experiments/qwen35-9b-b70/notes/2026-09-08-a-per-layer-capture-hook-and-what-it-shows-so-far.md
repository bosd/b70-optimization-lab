# A per-layer capture hook, and what it shows so far

The divergence is localised to the model body but no capture existed to bisect it - the four GDN
trace hooks the launchers forward are absent from R276. This builds one and reports the first
results, one clean and one confounded.

## The hook

An overlay adds a module-level installer to `qwen3_5.py` that registers a forward hook on every
decoder layer. With N identical prompts in one forward, the flattened hidden state splits into N
slices that must be bitwise identical unless the computation depends on a row's position; the hook
logs one line per layer with the number of distinct slice digests. Inert unless
`VLLM_XPU_LAYER_HASH_FILE` and `VLLM_XPU_LAYER_HASH_SPLITS` are both set.

Three things had to be fixed to get it firing, each worth knowing:

- the checkpoint's architecture is `Qwen3_5ForConditionalGeneration`, not the `Qwen3_5ForCausalLM`
  the file's first `forward` belongs to, so instrumenting one class silently captured nothing;
- the installer had to be a module-level function rather than a method, since those two classes do
  not share a base;
- the offline entry point needs a `__main__` guard, because the engine starts workers with spawn.

## Prefill is clean

One prefill of 64 identical prompts, TP2: **every layer reports one distinct slice**, at 8192 rows.
Identical prompts produce bitwise identical hidden states at every layer through the whole body. The
prefill path shows no position dependence at all.

## The decode result is confounded, and the confound is the interesting part

Generating 128 tokens, steps with exactly 64 rows report differing slices at almost every layer
including layer 0 - 8000 of 8064 layer-observations. Taken at face value that would say position
dependence starts immediately.

It cannot be taken at face value. vLLM does not lockstep requests: within one step, requests sit at
different generation positions, so their hidden states differ legitimately and a slice comparison
sees that rather than any arithmetic effect. This is the same drift already measured from the ladder
timings, where copies of one prompt span about three decode steps.

Worth noting alongside it: all 64 outputs in this run were byte-identical, so nothing diverged here
even though the hidden states differ - consistent with perturbations that are usually sub-threshold.

## What the hook needs before it can bisect

Record each row's request id and generation position beside its digest, then compare only rows at the
same position. That is a small change to the hook and it turns a confounded comparison into the
bisection this was built for. Until then the prefill result stands on its own and the decode numbers
should not be read as evidence of anything.

Evidence: `data/2026-09-08-layer-hash-prefill-tp2.tsv`; overlay
`docker/r276-layerhash-diag.Dockerfile`; probe `probes/layer-hash-offline-prefill.py`.
