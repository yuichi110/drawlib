#!/bin/bash
set -e

cd "$(dirname "$0")" || exit
if command -v poetry &> /dev/null; then
    echo "$ poetry run pylint ./drawlib --rcfile=./drawlib/.pylintrc"
    poetry run pylint ./drawlib --rcfile=./drawlib/.pylintrc
    echo "$ poetry run pylint ./tests --rcfile=./tests/.pylintrc"
    poetry run pylint ./tests --rcfile=./tests/.pylintrc
    echo "$ poetry run pylint ./docs --rcfile=./docs/.pylintrc"
    poetry run pylint ./docs --rcfile=./docs/.pylintrc
else
    echo "$ pylint ./drawlib --rcfile=./drawlib/.pylintrc"
    pylint ./drawlib --rcfile=./drawlib/.pylintrc
    echo "$ pylint ./tests --rcfile=./tests/.pylintrc"
    pylint ./tests --rcfile=./tests/.pylintrc
    echo "$ pylint ./docs --rcfile=./docs/.pylintrc"
    pylint ./docs --rcfile=./docs/.pylintrc
fi