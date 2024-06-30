#!/bin/bash

# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

set -e

# cd to project root directory
cd "$(dirname "$0")"
cd ../

# create old stubs
echo '$ find "./drawlib" -type f -name "*.pyi" -exec rm -f {} +'
find "./drawlib" -type f -name "*.pyi" -exec rm -f {} +
echo

# create stub
echo "$ pyright --createstub drawlib"
pyright --createstub drawlib
echo

# copy new stubs
echo '$ rsync -avm --include="*/" --include="*.pyi" --exclude="*" --ignore-existing "typings/drawlib" "./"'
rsync -avm --include="*/" --include="*.pyi" --exclude="*" --ignore-existing "typings/drawlib" "./"
echo

# delete stub output directory
echo '$ rm -rf ./typings/drawlib'
rm -rf ./typings/drawlib
echo