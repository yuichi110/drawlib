#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"

if [ -z "${DRAWLIB_CMD:-}" ]; then
    if [ -f "uv.lock" ] && command -v uv &> /dev/null; then
        DRAWLIB_CMD="uv run drawlib"
        PYTHON_CMD="uv run python"
    elif command -v drawlib &> /dev/null; then
        DRAWLIB_CMD="drawlib"
        PYTHON_CMD="python3"
    else
        DRAWLIB_CMD="uv run drawlib"
        PYTHON_CMD="uv run python"
    fi
fi

echo "Building standalone Python icon illustrations..."
$DRAWLIB_CMD build image tools/icons_src/ -o tools/release_assets/v0.3/icons/

echo "Normalizing icons to 512x512 (460x460 inner bbox)..."
$PYTHON_CMD -m tools.dcli.codegen.icons_build

echo "Icon build complete: tools/release_assets/v0.3/icons/"
