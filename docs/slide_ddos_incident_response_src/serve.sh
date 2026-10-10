#!/usr/bin/env bash
# Local preview server for Drawlib presentation deck
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ "docs/slide_ddos_incident_response_src" = "." ]; then
    cd "$SCRIPT_DIR"
else
    PARENT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
    cd "$PARENT_DIR"
fi

if [ ! -f "slide_ddos_incident_response_html/index.html" ]; then
    if [ -f "$SCRIPT_DIR/build_html.sh" ]; then
        "$SCRIPT_DIR/build_html.sh"
    elif [ -f "$SCRIPT_DIR/build.sh" ]; then
        "$SCRIPT_DIR/build.sh"
    fi
fi

if [ -z "${DRAWLIB_CMD:-}" ]; then
    if ( [ -f "uv.lock" ] || [ -f "../uv.lock" ] ) && command -v uv &> /dev/null; then
        DRAWLIB_CMD="uv run drawlib"
    elif command -v drawlib &> /dev/null; then
        DRAWLIB_CMD="drawlib"
    else
        DRAWLIB_CMD="uv run drawlib"
    fi
fi

PORT="${1:-8000}"
echo "Serving presentation at http://localhost:${PORT}..."
$DRAWLIB_CMD serve slide_ddos_incident_response_html/ -p "${PORT}"
