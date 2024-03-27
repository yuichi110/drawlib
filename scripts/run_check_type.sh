#!/bin/bash
set -e

cd "$(dirname "$0")"
cd ../
echo "$ pwd"
pwd
if command -v poetry &> /dev/null; then
    echo "$ poetry run mypy ./drawlib --disallow-untyped-defs --check-untyped-defs"
    poetry run mypy ./drawlib --disallow-untyped-defs --check-untyped-defs
    echo
    echo "$ poetry run mypy ./tests"
    poetry run mypy ./tests
    echo
    echo "$ run mypy ./docs"
    poetry run mypy ./docs
else
    echo "mypy ./drawlib --disallow-untyped-defs --check-untyped-defs"
    mypy ./drawlib --disallow-untyped-defs --check-untyped-defs
    echo
    echo "mypy ./tests"
    mypy ./tests
    echo
    echo "mypy ./docs"
    mypy ./docs
fi