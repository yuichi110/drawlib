#!/bin/bash
set -e

cd "$(dirname "$0")"
cd ../
echo "$ pwd"
pwd
find drawlib -type f -name "*.py" | while read -r filename; do
    if command -v poetry &> /dev/null; then
        echo "$ poetry run radon cc $filename"
        poetry run radon cc $filename
    else
        echo "$ radon cc $filename"
        radon cc $filename
    fi
done