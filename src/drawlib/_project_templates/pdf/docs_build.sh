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

echo "Building PDF document..."
$DRAWLIB_CMD build pdf docs_src/ -o document.pdf --generate-index -c docs_config.py

echo "Build complete: document.pdf"
