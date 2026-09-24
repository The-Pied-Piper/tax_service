#!/usr/bin/env bash
# Shared helpers; sourced by every script. Not a command.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

# Run as the host user so files written through the bind mount stay yours.
export UID GID="$(id -g)"

compose() { docker compose "$@"; }
# One-off command in a fresh app container (waits for a healthy db).
run() { compose run --rm app "$@"; }
# One-off command without starting the database.
run_nodb() { compose run --rm --no-deps app "$@"; }
# The generator, from the copy vendored in this repo.
gen() { run_nodb python -m tools.service_gen.cli "$@"; }
