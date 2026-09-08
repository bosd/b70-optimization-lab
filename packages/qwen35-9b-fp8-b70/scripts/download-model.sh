#!/usr/bin/env bash
# Thin wrapper over tools/container-packet/download-model.sh with this packet's manifest.
set -euo pipefail
here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd); repo=$(cd -- "${here}/../../.." && pwd)
export MODEL_MANIFEST=${MODEL_MANIFEST:-${repo}/repro/qwen35-9b-fp8-b70/manifests/model-direct-redhatai-qwen35-9b-fp8-dynamic-790f0576.json}
exec "${repo}/tools/container-packet/download-model.sh" "$@"
