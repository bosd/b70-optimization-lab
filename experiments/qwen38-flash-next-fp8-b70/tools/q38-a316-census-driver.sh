#!/usr/bin/env bash
# A316's driver: the snapshot-window census driver bound to this packet.
set -Eeuo pipefail
exec "$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)/q38-census-window-driver.sh" 316 19986 mtp1
