#!/bin/bash

cd "$(dirname "$0")" || exit
if command -v poetry &> /dev/null; then
    echo "$ poetry run mypy ./drawlib --disallow-untyped-defs"
    poetry run mypy ./drawlib --disallow-untyped-defs
    echo
    echo "$ poetry run mypy ./tests"
    poetry run mypy ./tests
    echo
    echo "$ run mypy ./docs"
    poetry run mypy ./docs
else
    echo "mypy ./drawlib --disallow-untyped-defs"
    mypy ./drawlib --disallow-untyped-defs
    echo
    echo "mypy ./tests"
    mypy ./tests
    echo
    echo "mypy ./docs"
    mypy ./docs
fi