#!/usr/bin/env bash
# One-time scaffold of app/ and tests/ from openapi/openapi.yml [--name NAME].
source "$(dirname "$0")/_lib.sh"
# Default the name from the host directory; inside the container cwd is always /app.
compose build app && gen init --name "$(basename "$PWD")" "$@"
