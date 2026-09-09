# Local correctness candidate; historical images and score identities stay pinned.
# Build context: this community packet. Pass an immutable local BASE_IMAGE ID.
ARG BASE_IMAGE
FROM ${BASE_IMAGE}
COPY reported/vllm-gpu-model-runner-uniform-decode-alias.patch /tmp/uniform-decode.patch
COPY validation/test_installed_classifier.py /tmp/test_installed_classifier.py
# The image contains both an editable checkout and an installed copy. Validate
# and patch both so changing the working directory cannot bypass the fix.
RUN for source in /workspace/vllm/vllm/v1/worker/gpu_model_runner.py /opt/venv/lib/python3.12/site-packages/vllm/v1/worker/gpu_model_runner.py; do \
      /opt/venv/bin/python /tmp/test_installed_classifier.py "$source" --expect-stock && \
      patch --batch --forward "$source" /tmp/uniform-decode.patch && \
      /opt/venv/bin/python /tmp/test_installed_classifier.py "$source" || exit 1; \
    done
