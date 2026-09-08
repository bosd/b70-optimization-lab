#!/usr/bin/env bash
# Verify a model directory against its recipe manifest: revision, every file size, every LFS SHA-256
# and every small-file git blob. This is the same verifier the measured launcher runs before it
# starts a server, so a pass means the packet points at exactly the bytes the published result used.
#   MODEL_DIR       the model directory (required)
#   MODEL_MANIFEST  the recipe manifest (required)
set -euo pipefail
repo=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)
manifest=${MODEL_MANIFEST:?set MODEL_MANIFEST}
dest=${MODEL_DIR:?set MODEL_DIR to the model directory}
exec "${repo}/repro/qwen38-27b-autoround-int4-b70/scripts/verify-model-direct.py" "${manifest}" "${dest}" "$@"
