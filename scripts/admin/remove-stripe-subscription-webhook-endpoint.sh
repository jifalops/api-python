#!/usr/bin/env bash

set -e

WEBHOOK_ENDPOINT_ID="$1"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Load .env
source "$SCRIPT_DIR/.env"

if [ -z "$WEBHOOK_ENDPOINT_ID" ]; then
  echo "Usage: $0 <Webhook ID>"
  stripe webhook_endpoints list \
    --api-key "$STRIPE_SECRET_KEY"
  exit 1
fi

stripe webhook_endpoints delete \
  --api-key "$STRIPE_SECRET_KEY" \
  "$WEBHOOK_ENDPOINT_ID"