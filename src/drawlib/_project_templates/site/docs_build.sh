#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Detect drawlib command
DRAWLIB_CMD="drawlib"
if command -v drawlib &> /dev/null; then
    DRAWLIB_CMD="drawlib"
elif python3 -m drawlib --version &> /dev/null; then
    DRAWLIB_CMD="python3 -m drawlib"
elif python -m drawlib --version &> /dev/null; then
    DRAWLIB_CMD="python -m drawlib"
elif command -v uv &> /dev/null && uv run drawlib --version &> /dev/null; then
    DRAWLIB_CMD="uv run drawlib"
fi

echo "Building Markdown..."
$DRAWLIB_CMD build markdown docs_src/ -o docs/ -c docs_config.py

echo "Building HTML site..."
$DRAWLIB_CMD build html docs_src/ -o docs_html/ -c docs_config.py

echo "Build complete!"
echo "  - Markdown: docs/"
echo "  - HTML: docs_html/"
