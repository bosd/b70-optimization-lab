#!/usr/bin/env bash
# A322's driver: the fresh-server repeat of the MTP0 W13-N64 result.
set -Eeuo pipefail
d=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
exec "$d/q38-client-driver.sh" 322 19992 mtp0 "$d/run-tp4-mtp0-4352-ple-only-a322-fullgraphdet-w13n64-client.sh"
