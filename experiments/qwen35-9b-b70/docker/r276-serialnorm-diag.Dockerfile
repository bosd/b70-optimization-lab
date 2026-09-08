# R276 plus one diagnostic overlay: the RMSNorm variance reduction can be serialised one row at a
# time, to measure end to end what preserving the single-row oracle costs. Pure Python; every pinned
# kernel digest unchanged, and the replaced norm implementation is declared to the image contract
# through EXPECTED_IR_LAYERNORM_SHA256. Default off, so the image behaves as R276 unless asked.
FROM neural-download/vllm-openai-xpu:qwen38-int4-gdn-spec-group-sync-free-r276
COPY layernorm.py /opt/venv/lib/python3.12/site-packages/vllm/ir/ops/layernorm.py
