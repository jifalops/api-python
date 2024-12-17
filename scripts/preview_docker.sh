#!/usr/bin/env bash

set -e

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
pushd $script_dir/.. > /dev/null

docker build -f deploy/docker/Dockerfile -t api-python .
printenv > deploy/docker/.env
docker run --env-file=deploy/docker/.env -e PORT=8001 -e WORKERS=1 -it api-python

popd > /dev/null
