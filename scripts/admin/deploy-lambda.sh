#!/usr/bin/env bash

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

$SCRIPT_DIR/../build-sam.sh

# Load .env
set -o allexport
source "$SCRIPT_DIR/.env"
set +o allexport

pushd "$SCRIPT_DIR/../../deploy/aws_sam" > /dev/null

sam deploy --debug \
  --no-confirm-changeset \
  --no-fail-on-empty-changeset

popd > /dev/null
