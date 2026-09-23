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

rm -rf docs/ docs_html/ quickstart.pdf

echo "=== Building Markdown documentation (docs_src/ -> docs/) ==="
uv run drawlib build markdown docs_src/ -o docs/

echo ""
echo "=== Building HTML documentation (docs_src/ -> docs_html/) ==="
uv run drawlib build html docs_src/ -o docs_html/ --css google

echo ""
echo "=== Building Quickstart PDF (docs_src_quickstart_pdf/ -> quickstart.pdf) ==="
uv run drawlib build pdf docs_src_quickstart_pdf/ -o quickstart.pdf --generate-index --css google

echo ""
echo "=== Building README images (docs_readme_images/codes/ -> docs_readme_images/images/) ==="
uv run drawlib build images docs_readme_images/codes/ -o docs_readme_images/images/

echo ""
echo "Documentation build completed successfully!"
