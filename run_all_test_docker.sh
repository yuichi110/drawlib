#!/bin/bash

cd "$(dirname "$0")" || exit
if command -v poetry &> /dev/null; then
    docker build .
else
    echo 'please install "docker" first.'
fi