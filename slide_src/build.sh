#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Building HTML Slide Deck ==="
"$SCRIPT_DIR/build_html.sh"

echo "=== Building Presentation PDF ==="
"$SCRIPT_DIR/build_pdf.sh"

echo "All slide builds completed successfully!"
