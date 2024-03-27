#!/bin/bash
set -e

cd "$(dirname "$0")"
cd ../
echo "$ pwd"
pwd
if command -v poetry &> /dev/null; then
    echo "$ poetry run bandit -r ./drawlib"
    poetry run bandit -r ./drawlib
else
    echo "$ bandit -r ./drawlib"
    bandit -r ./drawlib
fi