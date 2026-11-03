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

echo "Building Architecture HTML site..."
if [ -f "pyproject.toml" ] && [ -f "docs_src/architecture/template.html" ]; then
    python3 -c '
import pathlib, re, tomllib
ver = tomllib.loads(pathlib.Path("pyproject.toml").read_text("utf-8"))["project"]["version"]
p = pathlib.Path("docs_src/architecture/template.html")
s = p.read_text("utf-8")
s2 = re.sub(r"(<span class=\"sidebar-version-text\">(?:Architecture\s*·\s*)?)v[^<]+(</span>)", rf"\g<1>v{ver}\g<2>", s)
if s2 != s:
    p.write_text(s2, "utf-8")
'
fi
$DRAWLIB_CMD build html docs_src/architecture/ -o docs/architecture/
echo "HTML site build complete: docs/architecture/"
