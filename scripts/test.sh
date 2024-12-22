#!/usr/bin/env bash

set -e

GROUP="$1"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

pushd "$SCRIPT_DIR/.." > /dev/null

if [ -z "$GROUP" ]; then
  poetry run pytest
else
  poetry run pytest -m "$GROUP" ${@:2}
fi

popd > /dev/null