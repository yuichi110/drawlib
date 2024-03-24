#!/bin/bash

cd "$(dirname "$0")" || exit
if command -v poetry &> /dev/null; then
    poetry run mypy .
else
    mypy .
fi