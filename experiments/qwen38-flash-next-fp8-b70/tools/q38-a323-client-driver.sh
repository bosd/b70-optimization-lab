#!/usr/bin/env bash
# A323's driver: the realistic-suite client on the MTP0 W13-N64 configuration.
set -Eeuo pipefail
d=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
exec "$d/q38-client-driver.sh" 323 19993 mtp0 "$d/run-tp4-mtp0-4352-ple-only-a323-fullgraphdet-w13n64-client.sh"
