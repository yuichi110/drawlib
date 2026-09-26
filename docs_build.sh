#!/usr/bin/env bash
# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

rm -rf docs/ docs_html/ quickstart.pdf images_readme/

echo "=== Building Documentation Site (docs_src/build.sh) ==="
bash docs_src/build.sh

echo ""
echo "=== Building Quickstart PDF (quickstart_src/build.sh) ==="
bash quickstart_src/build.sh

echo ""
echo "=== Building README Images (images_readme_src/build.sh) ==="
bash images_readme_src/build.sh

echo ""
echo "All builds completed successfully!"
