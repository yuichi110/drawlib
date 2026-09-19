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

# cd to doc root
cd "$(dirname "$0")"
cd ../

# delete old docs on target directory
rm -rf ../docs/docs/versions

# copy latest html to target directory
cp -r ./html ../docs/docs/versions