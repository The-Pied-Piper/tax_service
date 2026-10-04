#!/usr/bin/env bash
# Shared helpers; sourced by every script. Not a command.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

# Run as the host user so files written through the bind mount stay yours.
export UID GID="$(id -g)"

# compose.yaml sets IN_APP_CONTAINER=1 on the app service. Inside it (e.g. a VS
# Code dev container) commands run directly; from the host they run in a
# one-off app container. Either way, `./dev.sh test` does the same thing.
in_app_container() { [[ "${IN_APP_CONTAINER:-}" == 1 ]]; }

# Managing containers only works from the host.
compose() {
    if in_app_container; then
        echo "this command manages containers: run it from the host, not inside the app container" >&2
        exit 1
    fi
    docker compose "$@"
}
# A command in the app environment (with the database available).
run() {
    if in_app_container; then "$@"; else compose run --rm app "$@"; fi
}
# A command in the app environment, without starting the database.
run_nodb() {
    if in_app_container; then "$@"; else compose run --rm --no-deps app "$@"; fi
}
# The generator, from the copy vendored in this repo.
gen() { run_nodb python -m tools.service_gen.cli "$@"; }
