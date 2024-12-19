#!/usr/bin/env bash

set -e

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

source "$script_dir/.env"

aws logs tail "/aws/lambda/$PROD_LAMBDA_LOG_GROUP" --follow
