#!/bin/bash

set -e
set -x


if [ -z "${1}" ] || [ -z "${2}" ]
then
    echo "no arguments are given! Using the default settings ..."
    echo "docker_build.sh [PROJECT_PATH] [DOCKERFILE within PROJECT_PATH]"
    PROJECT_PATH=${PWD}
    DOCKERFILE=${PROJECT_PATH}/Dockerfile
else
    PROJECT_PATH=${1}
    DOCKERFILE=${1}/${2}
fi

DOCKER_IMAGE=flask_server:22.04

docker image build \
    ${PROJECT_PATH} -f ${DOCKERFILE} -t ${DOCKER_IMAGE}


