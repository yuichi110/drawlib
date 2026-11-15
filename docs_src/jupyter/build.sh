#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Building Jupyter Notebooks (.ipynb) & HTML Preview ==="
"$SCRIPT_DIR/build_jupyter.sh" "$@"

echo "All builds completed successfully! (Outputs in docs/jupyter/)"
