#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PARENT_DIR"

if [ -z "${DRAWLIB_CMD:-}" ]; then
    if ( [ -f "uv.lock" ] || [ -f "../uv.lock" ] ) && command -v uv &> /dev/null; then
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

echo "Building HTML site..."
if [ -f "../pyproject.toml" ] && [ -f "docs_src/template.html" ]; then
    python3 -c '
import pathlib, re, tomllib
ver = tomllib.loads(pathlib.Path("../pyproject.toml").read_text("utf-8"))["project"]["version"]
p = pathlib.Path("docs_src/template.html")
s = p.read_text("utf-8")
s2 = re.sub(r"(<span class=\"sidebar-version-text\">)v[^<]+(</span>)", rf"\g<1>v{ver}\g<2>", s)
if s2 != s:
    p.write_text(s2, "utf-8")
'
fi
$DRAWLIB_CMD build html docs_src/ -o docs_html/
if [ -d "docs_src/pypi" ]; then
    echo "Building PyPI README images..."
    $DRAWLIB_CMD build image docs_src/pypi/ -o docs_html/pypi_images/
fi
echo "HTML site build complete: docs_html/"
