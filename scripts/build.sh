#!/usr/bin/env bash

ROOT_PATH=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
PARENT_PATH=$( cd "$( dirname "${ROOT_PATH}" )" && pwd )

docker build -t sjbitcode/budget $PARENT_PATH
