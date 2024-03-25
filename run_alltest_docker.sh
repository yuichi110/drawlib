#!/bin/bash
set -e

cd "$(dirname "$0")" || exit
if command -v docker &> /dev/null; then
    docker build .
else
    echo 'please install "docker" first.'
    exit 1
fi