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

# update pyproject.toml
python scripts/update_pyprojecttoml.py

# delete font cache
python -m drawlib --purge_font_cache

# publish to pypi
poetry publish --build