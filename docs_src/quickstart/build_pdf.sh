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

mkdir -p docs/quickstart
echo "Using Drawlib command: $DRAWLIB_CMD"
echo "Building Quickstart PDF document..."
$DRAWLIB_CMD build pdf docs_src/quickstart/ -o docs/quickstart/quickstart.pdf --generate-index
echo "PDF build complete: docs/quickstart/quickstart_{en,ja}.pdf"
