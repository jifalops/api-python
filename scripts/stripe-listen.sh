#!/usr/bin/env bash

port="${1:-8000}" # 8001 for Docker, 8002 for SAM
stripe listen \
  --api-key "${STRIPE_SECRET_KEY}" \
  --forward-to localhost:${port}/subscription/webhook