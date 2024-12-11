#!/usr/bin/env bash

set -e
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

pushd "$script_dir/.." > /dev/null
IMAGE_URI="api-python_lambda"
docker build -f ./deploy/aws_sam/Dockerfile -t $IMAGE_URI .
popd > /dev/null

pushd "$script_dir/../deploy/aws_sam" > /dev/null

# Use SAM to start the API.
port=$((HOST_API_PORT + 2))
sam local start-api --debug --host 0.0.0.0 --port $port \
  --parameter-overrides \
    ImageUri="$IMAGE_URI" \
    LoggingLevel="$LOGGING_LEVEL" \
    Workers=1 \
    PostgresUri="$POSTGRES_URI" \
    Neo4jUri="$NEO4J_URI" \
    Neo4jPassword="$NEO4J_PASSWORD"

popd > /dev/null
