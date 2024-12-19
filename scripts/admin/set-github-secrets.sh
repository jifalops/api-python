#!/usr/bin/env bash

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Load .env
source "$SCRIPT_DIR/.env"

# Change directory for implicit repo resolution.
pushd "$SCRIPT_DIR" > /dev/null

set_secret() {
  gh secret set $1 --body "$2"
}

set_var() {
  gh variable set $1 --body "$2"
}

set_secret "AWS_ACCESS_KEY_ID" "$AWS_ACCESS_KEY_ID"
set_secret "AWS_SECRET_ACCESS_KEY" "$AWS_SECRET_ACCESS_KEY"
set_var "AWS_REGION" "$AWS_REGION"

popd > /dev/null