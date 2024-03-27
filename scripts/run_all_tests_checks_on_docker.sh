#!/bin/bash
set -e

cd "$(dirname "$0")"
cd ../
if command -v docker &> /dev/null; then
    pwd
else
    echo 'please install "docker" first.'
    exit 1
fi