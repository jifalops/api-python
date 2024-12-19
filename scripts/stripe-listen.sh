#!/usr/bin/env bash

PORT="${1:-8000}" # 8001 for Docker, 8002 for SAM
TARGET="localhost:${port}/subscription/webhook"
echo "Forwarding to $TARGET"
stripe listen --forward-to "$TARGET" --api-key "$STRIPE_SECRET_KEY"
