#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Building API Reference HTML Site ==="
"$SCRIPT_DIR/build_html.sh"

echo "All builds completed successfully!"
