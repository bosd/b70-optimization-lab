"""N identical prompts; the layer hook records per-layer slice-digest counts.

With MAX_TOKENS=1 only the prefill is captured. Set it higher to capture decode steps, where the
flattened hidden state is one row per request and the divergences actually occur.

With N identical prompts of equal length in a single forward, the flattened hidden state splits into
N equal slices that must be bitwise identical unless the computation depends on a row's position in
the batch. The first layer reporting more than one distinct digest is where that breaks.

The __main__ guard is required: the engine starts workers with spawn, which re-imports this module.
"""
import os

from vllm import LLM, SamplingParams


def main() -> None:
    n = int(os.environ.get("VLLM_XPU_LAYER_HASH_SPLITS", "64"))
    prompt = (
        "Summarise the operational impact of a cache invalidation rule that fires on every write "
        "to the primary index, for an on-call engineer paged at 3am."
    )
    # GRAPH=1 reproduces the ladder's execution mode: full decode-only XPU graph capture. Note that
    # a replayed graph bypasses Python forward hooks, so the layer hashes only cover capture-time
    # forwards there - the output comparison below is what carries the result in that mode.
    graph = os.environ.get("GRAPH", "0") == "1"
    kwargs = {}
    if graph:
        kwargs["compilation_config"] = {
            "cudagraph_mode": "FULL_DECODE_ONLY",
            "cudagraph_capture_sizes": [1, 2, 4, 8, 16, 32, 64],
            "max_cudagraph_capture_size": 64,
            "splitting_ops": [],
            "inductor_compile_config": {"combo_kernels": False, "benchmark_combo_kernel": False,
                                        "deterministic": True, "split_reductions": False,
                                        "triton.autotune_pointwise": False,
                                        "benchmark_epilogue_fusion": False},
        }
    llm = LLM(
        model="/model", dtype="float16", quantization="compressed-tensors",
        tensor_parallel_size=int(os.environ.get("TP", "2")),
        max_model_len=512, max_num_seqs=n, max_num_batched_tokens=8192,
        enable_prefix_caching=False, gpu_memory_utilization=0.90,
        enforce_eager=not graph, **kwargs,
    )
    out = llm.generate([prompt] * n, SamplingParams(temperature=0, max_tokens=int(os.environ.get("MAX_TOKENS", "1")), ignore_eos=True))
    ids = [tuple(o.outputs[0].token_ids) for o in out]
    distinct = len(set(ids))
    print(f"RESULT graph={int(graph)} requests={len(out)} distinct_outputs={distinct}")
    if distinct > 1:
        from collections import Counter
        counts = Counter(ids)
        ref = counts.most_common(1)[0][0]
        for seq, c in counts.most_common():
            k = next((i for i, (a, b) in enumerate(zip(ref, seq)) if a != b), None)
            print(f"  variant seen {c}x, first differs at token {k}")


if __name__ == "__main__":
    main()
