# R276 plus a per-layer hidden-state hash hook, to find the first decoder layer at which identical
# prompts in one forward stop producing identical hidden states. Pure Python, inert unless
# VLLM_XPU_LAYER_HASH_FILE and VLLM_XPU_LAYER_HASH_SPLITS are both set.
FROM neural-download/vllm-openai-xpu:qwen38-int4-gdn-spec-group-sync-free-r276
COPY qwen3_5.py /opt/venv/lib/python3.12/site-packages/vllm/model_executor/models/qwen3_5.py
