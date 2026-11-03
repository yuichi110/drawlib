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

echo "Building OGP / Social Preview images..."
$DRAWLIB_CMD build image docs_src/ogp/ -o docs/ogp_images/

if [ -f "docs/ogp_images/social_preview.png" ]; then
    if [ -d "docs_src/site/_assets" ]; then
        cp "docs/ogp_images/social_preview.png" "docs_src/site/_assets/ogp.png"
        echo "  - Synced: docs_src/site/_assets/ogp.png"
    fi
    if [ -d "docs_src/architecture/_assets" ]; then
        cp "docs/ogp_images/social_preview.png" "docs_src/architecture/_assets/ogp.png"
        echo "  - Synced: docs_src/architecture/_assets/ogp.png"
    fi
    if [ -d "docs_src/api/_assets" ]; then
        cp "docs/ogp_images/social_preview.png" "docs_src/api/_assets/ogp.png"
        echo "  - Synced: docs_src/api/_assets/ogp.png"
    fi
fi

echo "Build complete: docs/ogp_images/"
