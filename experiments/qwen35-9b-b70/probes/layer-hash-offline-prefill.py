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
    llm = LLM(
        model="/model", dtype="float16", quantization="compressed-tensors",
        tensor_parallel_size=int(os.environ.get("TP", "2")),
        max_model_len=512, max_num_seqs=n, max_num_batched_tokens=8192,
        enable_prefix_caching=False, gpu_memory_utilization=0.90, enforce_eager=True,
    )
    out = llm.generate([prompt] * n, SamplingParams(temperature=0, max_tokens=int(os.environ.get("MAX_TOKENS", "1")), ignore_eos=True))
    texts = {o.outputs[0].text for o in out}
    print(f"RESULT requests={len(out)} distinct_first_tokens={len(texts)}")


if __name__ == "__main__":
    main()
