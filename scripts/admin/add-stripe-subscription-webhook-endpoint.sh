#!/usr/bin/env bash

set -e

# Ensure a URL is passed
if [ -z "$1" ]; then
  echo "Usage: $0 <'aws'|url>"
  exit 1
fi

URL="$1"


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Load .env
source "$SCRIPT_DIR/.env"

if [ "$URL" == "aws" ]; then
  URL="$PROD_API_URL_AWS"
fi


stripe webhook_endpoints create \
  --api-key "$STRIPE_SECRET_KEY" \
  --url "$URL/subscription/webhook" \
  --enabled-events customer.subscription.created \
  --enabled-events customer.subscription.updated \
  --enabled-events customer.subscription.deleted \
  --enabled-events customer.subscription.paused \
  --enabled-events customer.subscription.resumed