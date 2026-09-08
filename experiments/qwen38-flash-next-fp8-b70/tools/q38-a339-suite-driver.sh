#!/usr/bin/env bash
# A339's driver: replay of the Triton-HC lossless-MTP1 suite record.
set -Eeuo pipefail
exec "$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)/q38-suite-driver.sh" 339 19952 mtp1
