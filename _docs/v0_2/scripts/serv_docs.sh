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

open_browser_1sec_later() {
    sleep 1
    open http://localhost
}

# cd to doc root
cd "$(dirname "$0")"
cd ../

# activate
source .venv/bin/activate

# open browser later
open_browser_1sec_later &

# cd to html directory and start http server
cd ./html
python -m http.server 80