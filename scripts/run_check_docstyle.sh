#!/bin/bash
set -e

cd "$(dirname "$0")" || exit
if command -v poetry &> /dev/null; then
    echo "$ poetry run pydocstyle ./drawlib"
    poetry run pydocstyle ./drawlib
else
    echo "$ pydocstyle ./drawlib"
    pydocstyle ./drawlib
fi