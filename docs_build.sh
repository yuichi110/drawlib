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

rm -rf docs/ docs_html/

echo "=== Building Markdown documentation (docs_src/ -> docs/) ==="
uv run drawlib build markdown docs_src/ -o docs/

echo ""
echo "=== Building HTML documentation (docs_src/ -> docs_html/) ==="
uv run drawlib build html docs_src/ -o docs_html/ --css google

echo ""
echo "Documentation build completed successfully!"
