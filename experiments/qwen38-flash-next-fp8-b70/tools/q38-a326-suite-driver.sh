#!/usr/bin/env bash
# A326's driver: the fresh-server suite repeat of the MTP0 W13-N64 result.
set -Eeuo pipefail
exec "$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)/q38-suite-driver.sh" 326 19996 mtp0
