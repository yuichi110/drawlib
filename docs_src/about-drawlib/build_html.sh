#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$ROOT_DIR"

if [ -z "${DRAWLIB_CMD:-}" ]; then
    if [ -f "pyproject.toml" ] && command -v uv &> /dev/null; then
        DRAWLIB_CMD="uv run drawlib"
    elif command -v drawlib &> /dev/null; then
        DRAWLIB_CMD="drawlib"
    elif python3 -m drawlib --version &> /dev/null; then
        DRAWLIB_CMD="python3 -m drawlib"
    elif python -m drawlib --version &> /dev/null; then
        DRAWLIB_CMD="python -m drawlib"
    else
        DRAWLIB_CMD="drawlib"
    fi
fi

echo "Building HTML Slide Deck..."
$DRAWLIB_CMD build slide docs_src/about-drawlib/ -o docs/about-drawlib/
echo "Slide HTML build complete: docs/about-drawlib/index.html"
