# R276 plus a row-chunked FP16 vocabulary projection. The projection is bitwise invariant to batch
# size at 32 rows and below and switches reduction from 33 up; chunking it to 32 makes every row
# equal to its single-row value, which is what the identity oracle computes. Pure Python, default
# off, and the replaced module is declared to the image contract.
FROM neural-download/vllm-openai-xpu:qwen38-int4-gdn-spec-group-sync-free-r276
COPY logits_processor.py /opt/venv/lib/python3.12/site-packages/vllm/model_executor/layers/logits_processor.py
