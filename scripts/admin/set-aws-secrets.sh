#!/usr/bin/env bash

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Load .env
set -o allexport
source "$SCRIPT_DIR/.env"
set +o allexport

set_secret() {
  aws secretsmanager create-secret \
  --name $1 \
  --secret-string "$2" \
  2>/dev/null \
  || aws secretsmanager update-secret \
  --secret-id $1 \
  --secret-string "$2"
}

set_param() {
  aws ssm put-parameter \
  --name "/api-python/$1" \
  --value "$2" \
  --type String \
  --overwrite
}

set_param "logging-level" "$PROD_LOGGING_LEVEL"
set_secret "postgres-uri" "$PROD_POSTGRES_URI"
set_secret "neo4j-uri" "$PROD_NEO4J_URI"
set_secret "neo4j-password" "$PROD_NEO4J_PASSWORD"
set_param "stripe-public-key" "$PROD_STRIPE_PUBLIC_KEY"
set_secret "stripe-secret-key" "$PROD_STRIPE_SECRET_KEY"
set_secret "stripe-webhook-secret" "$PROD_STRIPE_WEBHOOK_SECRET"
set_param "firebase-project-id" "$PROD_FIREBASE_PROJECT_ID"

