#!/usr/bin/env bash

set -e

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"


set -o allexport
source "$script_dir/../../.env"
set +o allexport

pushd "$script_dir/../.." > /dev/null
IMAGE_TAG="$(git rev-parse --short HEAD)-$(date +%s)"
docker build -f ./deploy/aws_sam/Dockerfile -t "$PROD_AWS_ECR_REPOSITORY:$IMAGE_TAG" .
popd > /dev/null


pushd "$script_dir/../../deploy/aws_sam" > /dev/null
aws ecr push --region "$AWS_DEFAULT_REGION" --repository "$PROD_AWS_ECR_REPOSITORY" --image-uri "$PROD_AWS_ECR_REPOSITORY:$IMAGE_TAG"

sam deploy --debug \
  --no-confirm-changeset \
  --no-fail-on-empty-changeset \
  --parameter-overrides \
    ImageTag="$IMAGE_TAG" \
    LoggingLevel="$PROD_LOGGING_LEVEL" \
    Workers=$PROD_WORKERS \
    PostgresUri="$PROD_POSTGRES_URI" \
    Neo4jUri="$PROD_NEO4J_URI" \
    Neo4jPassword="$PROD_NEO4J_PASSWORD"
popd > /dev/null
