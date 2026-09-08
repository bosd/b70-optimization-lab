#!/usr/bin/env bash
# Regenerate this packet's compose.yaml from its recipe launcher. See tools/render-container-packet.sh.
set -euo pipefail
here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd); repo=$(cd -- "${here}/../../.." && pwd)
PACKAGE_DIR=packages/qwen35-9b-fp8-b70 LAUNCHER=repro/qwen35-9b-fp8-b70/scripts/run-qwen35-9b-fp8-server.sh SERVED_NAME=qwen35-9b-fp8 MODEL_DESC="RedHatAI/Qwen3.5-9B-FP8-dynamic" \
exec "${repo}/tools/render-container-packet.sh"
