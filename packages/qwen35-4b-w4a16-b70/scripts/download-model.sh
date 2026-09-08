#!/usr/bin/env bash
# Thin wrapper over tools/container-packet/download-model.sh with this packet's manifest.
set -euo pipefail
here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd); repo=$(cd -- "${here}/../../.." && pwd)
export MODEL_MANIFEST=${MODEL_MANIFEST:-${repo}/repro/qwen35-4b-w4a16-b70/manifests/model-direct-redhatai-qwen35-4b-w4a16-7a613872.json}
exec "${repo}/tools/container-packet/download-model.sh" "$@"
