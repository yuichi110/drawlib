#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$ROOT_DIR"

echo "=== Building HTML Slide Deck ==="
"$SCRIPT_DIR/build_html.sh"

echo "=== Building Presentation PDF ==="
"$SCRIPT_DIR/build_pdf.sh"

echo "=== Building Presentation PPTX ==="
"$SCRIPT_DIR/build_pptx.sh"

echo "=== Generating Cover Preview ==="
if [ -z "${DRAWLIB_CMD:-}" ]; then
    if [ -f "pyproject.toml" ] && command -v uv &> /dev/null; then
        DRAWLIB_CMD="uv run drawlib"
    else
        DRAWLIB_CMD="drawlib"
    fi
fi
$DRAWLIB_CMD show docs_src/about-drawlib/en/00_opening/01_title.md 1 -o docs/about-drawlib/preview.png

echo "All slide builds completed successfully! (Outputs in docs/about-drawlib/)"
