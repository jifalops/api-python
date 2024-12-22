#!/usr/bin/env bash

set -e

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
root_dir=$script_dir/..
sam_dir=$script_dir/../deploy/aws_sam

# Copy files
pushd $root_dir > /dev/null
cp -r config.py app pyproject.toml poetry.lock $sam_dir/
find "$sam_dir" -type f \( -name '*_mock.py' -o -name '*_test.py' -o -name 'conftest.py' \) -delete
popd > /dev/null

# Build
pushd $sam_dir > /dev/null
poetry export -f requirements.txt --output requirements.txt --without-hashes
sam build #--debug
rm -r requirements.txt config.py app pyproject.toml poetry.lock
popd > /dev/null

# Remove files
pushd $sam_dir/.aws-sam/build/ApiFunction > /dev/null
rm COPYING poetry.lock pyproject.toml requirements.txt samconfig.toml template.yaml
popd > /dev/null