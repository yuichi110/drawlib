#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$REPO_ROOT"
if [ ! -f "$SCRIPT_DIR/_assets/ogp.png" ]; then
    cp -f "$SCRIPT_DIR/_assets/_logo.png" "$SCRIPT_DIR/_assets/ogp.png"
fi

echo "=== Building PNI Full Audit Report (PDF + HTML -> docs/reports/pni-full-audit/) ==="
uv run --group audit pni report build full_audit \
    --src-dir reports \
    -o reports \
    --html-output-dir docs/reports/pni-full-audit \
    -f pdf,html

cp -f docs/reports/pni-full-audit/images/00_cover/ch00_cover_scorecard.png "$SCRIPT_DIR/_assets/ogp.png"
cp -f docs/reports/pni-full-audit/images/00_cover/ch00_cover_scorecard.png docs/reports/pni-full-audit/_assets/ogp.png
mv -f reports/full_audit.pdf docs/reports/pni-full-audit/full_audit.pdf
echo "All report builds completed successfully!"
