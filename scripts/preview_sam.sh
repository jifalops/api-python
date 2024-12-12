#!/usr/bin/env bash

set -e
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Build first
$script_dir/build-sam.sh

pushd "$script_dir/../deploy/aws_sam" > /dev/null

# Use SAM to start the API.
HOST_API_PORT=${HOST_API_PORT:-8000}
port=$((HOST_API_PORT + 2))
sam local start-api --debug --host 0.0.0.0 --port $port \
  --parameter-overrides \
    LoggingLevel="$LOGGING_LEVEL" \
    Workers=1 \
    PostgresUri="$POSTGRES_URI" \
    Neo4jUri="$NEO4J_URI" \
    Neo4jPassword="$NEO4J_PASSWORD"

popd > /dev/null
