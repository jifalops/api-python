#!/usr/bin/env bash

set -e
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Build first
$script_dir/build-sam.sh

pushd "$script_dir/../deploy/aws_sam" > /dev/null

# Use SAM to start the API.
sam local start-api --debug --host 0.0.0.0 --port 8002 \
  --parameter-overrides \
    LoggingLevel="$LOGGING_LEVEL" \
    Workers=1 \
    PostgresUri="$POSTGRES_URI" \
    Neo4jUri="$NEO4J_URI" \
    Neo4jPassword="$NEO4J_PASSWORD"

popd > /dev/null
