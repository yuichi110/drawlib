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

# create stub
echo '$ ./scripts/create_stub.sh'
./scripts/create_stub.sh

# check next version ok
echo '$ python scripts/pypi_tools.py --check_new_version_ok'
python scripts/pypi_tools.py --check_new_version_ok

# update pyproject.toml
echo '$ python scripts/update_pyprojecttoml.py'
python scripts/update_pyprojecttoml.py

# delete font cache
echo '$ python -m drawlib --purge_font_cache'
python -m drawlib --purge_font_cache

# publish to pypi
echo '$ poetry publish --build'
poetry publish --build