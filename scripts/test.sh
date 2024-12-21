#!/usr/bin/env bash

set -e

if [ "$#" -gt 1 ]; then
  echo "Usage: $0 [unit|integration|e2e]"
  echo "Defaults to running all tests."
  exit 1
fi

GROUP="$1"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

pushd "$SCRIPT_DIR/.." > /dev/null

if [ -z "$GROUP" ]; then
  poetry run pytest
else
  poetry run pytest -m "$GROUP"
fi

popd > /dev/null