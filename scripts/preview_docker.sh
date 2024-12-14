#!/usr/bin/env bash

set -e

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
pushd $script_dir/.. > /dev/null

docker build --build-arg PORT=8001 -f deploy/docker/Dockerfile -t api-python .
docker run -it api-python

popd > /dev/null
