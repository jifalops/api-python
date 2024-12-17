#!/usr/bin/env bash

set -e
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Build first
$script_dir/build-sam.sh

pushd "$script_dir/../deploy/aws_sam" > /dev/null

cat <<EOF > .env.json
{
  "Parameters": {
    "Environment": {
      "Variables": {
        "LOGGING_LEVEL": "$LOGGING_LEVEL",
        "POSTGRES_URI": "$POSTGRES_URI",
        "NEO4J_URI": "$NEO4J_URI",
        "NEO4J_PASSWORD": "$NEO4J_PASSWORD",
        "STRIPE_PUBLIC_KEY": "$STRIPE_PUBLIC_KEY",
        "STRIPE_SECRET_KEY": "$STRIPE_SECRET_KEY",
        "STRIPE_WEBHOOK_SECRET": "$STRIPE_WEBHOOK_SECRET",
        "FIREBASE_PROJECT_ID": "$FIREBASE_PROJECT_ID",
        "GOOGLE_APPLICATION_CREDENTIALS": "",
        "VERIFY_TOKEN_SIGNATURE": "0"
      }
    }
  }
}
EOF

# Use SAM to start the API.
sam local start-api --debug --host 0.0.0.0 --port 8002 --env-vars .env.json

popd > /dev/null
