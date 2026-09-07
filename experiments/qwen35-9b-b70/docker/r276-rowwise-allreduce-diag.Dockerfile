# R276 plus one diagnostic overlay: a row-wise TP all-reduce, to test whether the two-card identity
# loss at high concurrency comes from the cross-card reduction rather than the GEMM. Pure Python; no
# kernel, extension or device library is touched, so the image contract's pinned digests still hold
# except for the communicator module, which the verifier lets a candidate opt into explicitly.
FROM neural-download/vllm-openai-xpu:qwen38-int4-gdn-spec-group-sync-free-r276
COPY xpu_communicator.py /opt/venv/lib/python3.12/site-packages/vllm/distributed/device_communicators/xpu_communicator.py
COPY envs.py /opt/venv/lib/python3.12/site-packages/vllm/envs.py
