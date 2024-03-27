#!/bin/bash
set -e

cd "$(dirname "$0")"
cd ../
echo "$ pwd"
pwd
if command -v poetry &> /dev/null; then
    poetry run python -m drawlib ./docs
else
    python -m drawlib ./docs
fi