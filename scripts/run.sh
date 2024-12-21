#!/usr/bin/env bash

set -e

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
pushd $script_dir/.. > /dev/null

$script_dir/firebase-start-emulators.sh &

poetry lock
poetry install --no-root
poetry run python -m uvicorn app.main:app_router --reload --log-level trace --host 0.0.0.0

popd > /dev/null
