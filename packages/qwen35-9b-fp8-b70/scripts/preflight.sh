#!/usr/bin/env bash
# Thin wrapper over tools/container-packet/preflight.sh with this packet's identity.
set -euo pipefail
here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd); repo=$(cd -- "${here}/../../.." && pwd)
export PACKAGE_DIR=packages/qwen35-9b-fp8-b70 SERVED_NAME=qwen35-9b-fp8 PACKET_NAME="RedHatAI/Qwen3.5-9B-FP8-dynamic B70 packet" MODEL_GIB=14
exec "${repo}/tools/container-packet/preflight.sh" "$@"
