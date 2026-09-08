#!/usr/bin/env bash
# A327's driver: the MTP0 W13-N128 screen's frozen client.
set -Eeuo pipefail
d=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
exec "$d/q38-client-driver.sh" 327 19997 mtp0 "$d/run-tp4-mtp0-4352-ple-only-a327-fullgraphdet-w13n128-client.sh"
