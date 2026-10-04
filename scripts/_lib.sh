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

# The template this service was created from (scripts/init.sh records it, and
# scripts/upgrade.sh fetches from it).
TEMPLATE_PATH="The-Pied-Piper/service-template.git"

# The template at the same host and scheme (SSH or HTTPS) as this repo's own
# origin, so access that works for the service works for the template.
template_repo_from_origin() {
    local origin rest
    origin="$(git remote get-url origin 2>/dev/null)" || origin=""
    case "$origin" in
        git@*:*) echo "${origin%%:*}:$TEMPLATE_PATH" ;;
        ssh://*) rest="${origin#ssh://}"; echo "ssh://${rest%%/*}/$TEMPLATE_PATH" ;;
        https://*) rest="${origin#https://}"; echo "https://${rest%%/*}/$TEMPLATE_PATH" ;;
        *) echo "https://github.com/$TEMPLATE_PATH" ;;
    esac
}

# Where to fetch the template: $TEMPLATE_REPO if set, else the address recorded
# in the TEMPLATE_REPO file, else the origin-based address.
template_repo() {
    if [[ -n "${TEMPLATE_REPO:-}" ]]; then
        echo "$TEMPLATE_REPO"
    elif [[ -s TEMPLATE_REPO ]]; then
        head -n 1 TEMPLATE_REPO
    else
        template_repo_from_origin
    fi
}
