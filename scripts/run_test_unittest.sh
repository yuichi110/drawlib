#!/bin/bash
set -e

cd "$(dirname "$0")"
cd ../
echo "$ pwd"
pwd
if command -v poetry &> /dev/null; then
    poetry run pytest -s --cov=drawlib tests/
else
    pytest -s --cov=drawlib tests/
fi