#!/usr/bin/env bash
# Local preview server for Drawlib presentation deck
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ "slide_src" = "." ]; then
    cd "$SCRIPT_DIR"
else
    PARENT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
    cd "$PARENT_DIR"
fi

if [ ! -f "slide/index.html" ]; then
    if [ -f "slide_src/build_html.sh" ]; then
        "./slide_src/build_html.sh"
    elif [ -f "slide_src/build.sh" ]; then
        "./slide_src/build.sh"
    elif [ -f "./build.sh" ]; then
        "./build.sh"
    fi
fi

if [ -z "${DRAWLIB_CMD:-}" ]; then
    if [ -f "uv.lock" ] && command -v uv &> /dev/null; then
        DRAWLIB_CMD="uv run drawlib"
    elif command -v drawlib &> /dev/null; then
        DRAWLIB_CMD="drawlib"
    else
        DRAWLIB_CMD="uv run drawlib"
    fi
fi

PORT="${1:-8000}"
echo "Serving presentation at http://localhost:${PORT}..."
$DRAWLIB_CMD serve slide/ -p "${PORT}"
