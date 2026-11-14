#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Building HTML ==="
"$SCRIPT_DIR/build_html.sh"

echo "=== Building PDF ==="
"$SCRIPT_DIR/build_pdf.sh"

echo "=== Building DOCX ==="
"$SCRIPT_DIR/build_docx.sh"

echo "All builds completed successfully! (Outputs in docs/quickstart/)"
