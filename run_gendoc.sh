#!/bin/bash
set -e

cd "$(dirname "$0")" || exit
if command -v poetry &> /dev/null; then
    poetry run python -m drawlib ./docs
else
    python -m drawlib ./docs
fi