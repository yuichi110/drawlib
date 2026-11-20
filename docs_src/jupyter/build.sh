#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Building Jupyter HTML Preview & Bundled Notebooks ==="
"$SCRIPT_DIR/build_html.sh" "$@"

echo "All builds completed successfully! (Outputs in docs/jupyter/)"
