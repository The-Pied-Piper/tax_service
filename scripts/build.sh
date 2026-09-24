#!/usr/bin/env bash
# Rebuild the dev image (after changing requirements*.txt).
source "$(dirname "$0")/_lib.sh"
compose build app "$@"
