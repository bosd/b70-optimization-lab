#!/usr/bin/env bash
# Thin wrapper over tools/container-packet/smoke-test.sh with this packet's identity.
set -euo pipefail
here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd); repo=$(cd -- "${here}/../../.." && pwd)
export PACKAGE_DIR=packages/qwen35-4b-w4a16-b70 SERVED_NAME=qwen35-4b-w4a16 PACKET_NAME="RedHatAI/Qwen3.5-4B-quantized.w4a16 B70 packet" MODEL_GIB=6
exec "${repo}/tools/container-packet/smoke-test.sh" "$@"
