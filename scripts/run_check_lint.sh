#!/bin/bash
set -e

cd "$(dirname "$0")"
cd ../
echo "$ pwd"
pwd
if command -v poetry &> /dev/null; then
    echo "$ poetry run pylint ./drawlib --rcfile=./drawlib/.pylintrc"
    poetry run pylint ./drawlib --rcfile=./drawlib/.pylintrc
    echo
    echo "$ poetry run pylint ./tests --rcfile=./tests/.pylintrc"
    poetry run pylint ./tests --rcfile=./tests/.pylintrc
    echo
    echo "$ poetry run pylint ./docs --rcfile=./docs/.pylintrc"
    poetry run pylint ./docs --rcfile=./docs/.pylintrc
else
    echo "$ pylint ./drawlib --rcfile=./drawlib/.pylintrc"
    pylint ./drawlib --rcfile=./drawlib/.pylintrc
    echo
    echo "$ pylint ./tests --rcfile=./tests/.pylintrc"
    pylint ./tests --rcfile=./tests/.pylintrc
    echo
    echo "$ pylint ./docs --rcfile=./docs/.pylintrc"
    pylint ./docs --rcfile=./docs/.pylintrc
    echo
fi