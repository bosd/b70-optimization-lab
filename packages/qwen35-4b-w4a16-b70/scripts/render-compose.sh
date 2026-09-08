#!/usr/bin/env bash
# Regenerate this packet's compose.yaml from its recipe launcher. See tools/render-container-packet.sh.
set -euo pipefail
here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd); repo=$(cd -- "${here}/../../.." && pwd)
PACKAGE_DIR=packages/qwen35-4b-w4a16-b70 LAUNCHER=repro/qwen35-4b-w4a16-b70/scripts/run-qwen35-4b-w4a16-server.sh SERVED_NAME=qwen35-4b-w4a16 MODEL_DESC="RedHatAI/Qwen3.5-4B-quantized.w4a16" \
exec "${repo}/tools/render-container-packet.sh"
