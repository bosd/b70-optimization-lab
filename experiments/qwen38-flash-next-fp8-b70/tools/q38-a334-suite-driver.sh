#!/usr/bin/env bash
# A334's driver: the fresh-server suite repeat of the MTP0 W13-N64 result.
set -Eeuo pipefail
exec "$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)/q38-suite-driver.sh" 334 19947 mtp0
