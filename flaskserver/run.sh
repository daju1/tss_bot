#!/bin/sh

set -e
set -x

DOCKER_IMAGE=flask_server:22.04

docker run -it --rm --name flask_server_container --cap-add=NET_ADMIN --device /dev/net/tun \
    --workdir=${PWD} \
    -p 5000:5000 \
    -v .:/app \
    -e FLASK_APP=/app/app.py \
    ${DOCKER_IMAGE} /app/start_server.sh
#/bin/bash

      #- FLASK_ENV=development
      #- FLASK_DEBUG=1
