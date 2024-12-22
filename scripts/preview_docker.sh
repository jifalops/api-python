#!/usr/bin/env bash

set -e

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
pushd $script_dir/.. > /dev/null

docker build -f deploy/docker/Dockerfile -t api-python .

docker run \
  -e PORT=8001 \
  -e WORKERS=1 \
  -e LOGGING_LEVEL="$LOGGING_LEVEL" \
  -e POSTGRES_URI="$POSTGRES_URI" \
  -e NEO4J_URI="$NEO4J_URI" \
  -e NEO4J_PASSWORD="$NEO4J_PASSWORD" \
  -e STRIPE_PUBLIC_KEY="$STRIPE_PUBLIC_KEY" \
  -e STRIPE_SECRET_KEY="$STRIPE_SECRET_KEY" \
  -e STRIPE_WEBHOOK_SECRET="$STRIPE_WEBHOOK_SECRET" \
  -e FIREBASE_PROJECT_ID="$FIREBASE_PROJECT_ID" \
  -e FIREBASE_AUTH_EMULATOR_HOST="$FIREBASE_AUTH_EMULATOR_HOST" \
  -e GOOGLE_APPLICATION_CREDENTIALS="$GOOGLE_APPLICATION_CREDENTIALS" \
  -e VERIFY_TOKEN_SIGNATURE="$VERIFY_TOKEN_SIGNATURE" \
  -it api-python

popd > /dev/null
