#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PARENT_DIR"

if [ -z "${DRAWLIB_CMD:-}" ]; then
    if [ -f "uv.lock" ] && command -v uv &> /dev/null; then
        DRAWLIB_CMD="uv run drawlib"
    elif command -v drawlib &> /dev/null; then
        DRAWLIB_CMD="drawlib"
    elif python3 -m drawlib --version &> /dev/null; then
        DRAWLIB_CMD="python3 -m drawlib"
    elif python -m drawlib --version &> /dev/null; then
        DRAWLIB_CMD="python -m drawlib"
    elif command -v uv &> /dev/null && uv run drawlib --version &> /dev/null; then
        DRAWLIB_CMD="uv run drawlib"
    else
        DRAWLIB_CMD="drawlib"
    fi
fi

echo "Using Drawlib command: $DRAWLIB_CMD"

echo "Building Markdown..."
$DRAWLIB_CMD build markdown docs_src/ -o docs/

echo "Building HTML site..."
$DRAWLIB_CMD build html docs_src/ -o docs_html/

echo "Build complete!"
echo "  - Markdown: docs/"
echo "  - HTML: docs_html/"
