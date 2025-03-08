#!/bin/bash

CWD="$(dirname $0)"

export CONTAINER_IMAGE="${CONTAINER_IMAGE:-app}"
export DATA_JOB_DIR="${DATA_JOB_DIR:-$(realpath ${CWD}/..)}"


docker build -t ${CONTAINER_IMAGE}-dev . && \
docker-compose -p tic-tac-tests -f ${CWD}/docker-compose.yml run tic-tac python -m pytest $*
docker-compose -p tic-tac-tests -f ${CWD}/docker-compose.yml rm -fsv
