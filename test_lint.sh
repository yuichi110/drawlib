#!/bin/bash

cd "$(dirname "$0")" || exit
if command -v poetry &> /dev/null; then
    poetry run pylint ./drawlib ./tests ./gen_doc.py
else
    pylint ./drawlib ./tests ./gen_doc.py
fi