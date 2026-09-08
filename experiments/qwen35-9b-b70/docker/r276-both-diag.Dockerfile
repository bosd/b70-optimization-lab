# R276 plus both diagnostic overlays at once: the row-wise TP all-reduce and the serialised RMSNorm
# variance reduction. Each was tested alone and neither removes the two-card identity divergence, so
# this exists to test whether they are jointly necessary. Pure Python; every pinned kernel digest
# unchanged, and both replaced modules are declared to the image contract.
FROM neural-download/vllm-openai-xpu:qwen38-int4-gdn-spec-group-sync-free-r276
COPY xpu_communicator.py /opt/venv/lib/python3.12/site-packages/vllm/distributed/device_communicators/xpu_communicator.py
COPY envs.py /opt/venv/lib/python3.12/site-packages/vllm/envs.py
COPY layernorm.py /opt/venv/lib/python3.12/site-packages/vllm/ir/ops/layernorm.py
