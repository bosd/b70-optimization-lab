#!/usr/bin/env bash
# Verify the model directory against the recipe manifest: revision, every file size and every
# LFS SHA-256. This is the same verifier the measured launcher runs before it starts a server, so a
# pass here means the packet is pointed at exactly the bytes the published result used.
#   MODEL_DIR  the model directory (required)
set -euo pipefail
here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd); repo_root=$(cd -- "${here}/../../.." && pwd)
manifest=${MODEL_MANIFEST:-${repo_root}/repro/qwen35-9b-w4a16-b70/manifests/model-direct-redhatai-qwen35-9b-w4a16-a398088c.json}
dest=${MODEL_DIR:?set MODEL_DIR to the model directory}
exec "${repo_root}/repro/qwen38-27b-autoround-int4-b70/scripts/verify-model-direct.py" "${manifest}" "${dest}" "$@"
