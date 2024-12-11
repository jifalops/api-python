#!/usr/bin/env bash

set -e

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
pushd $script_dir/.. > /dev/null

port=$((HOST_API_PORT + 1))
docker build -f deploy/docker/Dockerfile -t api-python .
docker run -p $port:$port -it api-python

popd > /dev/null
