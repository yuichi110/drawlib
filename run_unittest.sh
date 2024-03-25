#!/bin/bash
set -e

cd "$(dirname "$0")" || exit
if command -v poetry &> /dev/null; then
    poetry run pytest -s
else
    pytest -s
fi