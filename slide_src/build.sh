#!/usr/bin/env bash
# Build script for Drawlib HTML slide presentation deck
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ "slide_src" = "." ]; then
    cd "$SCRIPT_DIR"
else
    PARENT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
    cd "$PARENT_DIR"
fi

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

echo "Building presentation deck..."
$DRAWLIB_CMD build slide slide_src/ -o slide/ "$@"

echo "Slide build complete: slide/index.html"
