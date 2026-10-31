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
touch docs_html/.nojekyll
cat << 'EOF' > docs_html/404.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Moved — Drawlib Documentation</title>
    <script>
        (function() {
            var path = window.location.pathname;
            var match = path.match(/^(.*?)(\/(?:0[1-9]|10)_[a-z0-9_]+\/.*)$/);
            if (match && !match[1].endsWith('/en') && !match[1].endsWith('/ja')) {
                var target = match[1] + '/en' + match[2] + window.location.search + window.location.hash;
                window.location.replace(target);
            }
        })();
    </script>
    <style>
        body { font-family: system-ui, -apple-system, sans-serif; color: #334155; background: #f8fafc; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; }
        .card { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 2rem 2.5rem; max-width: 480px; text-align: center; box-shadow: 0 4px 16px rgba(15, 23, 42, 0.06); }
        h1 { font-size: 1.35rem; color: #0f172a; margin-top: 0; }
        p { line-height: 1.6; color: #475569; }
        .links { display: flex; gap: 0.75rem; justify-content: center; margin-top: 1.25rem; }
        a { color: #4f46e5; text-decoration: none; font-weight: 600; padding: 0.5rem 1rem; border: 1px solid #e2e8f0; border-radius: 8px; }
        a:hover { border-color: #4f46e5; background: #eef2ff; }
    </style>
</head>
<body>
    <div class="card">
        <h1>404 — Page Not Found</h1>
        <p>The requested documentation page could not be found or has moved to a localized URL.</p>
        <div class="links">
            <a id="fallback-en" href="en/index.html">English Docs</a>
            <a id="fallback-ja" href="ja/index.html">日本語ドキュメント</a>
        </div>
    </div>
    <script>
        (function() {
            if (window.location.protocol === 'http:' || window.location.protocol === 'https:') {
                var enLink = document.getElementById('fallback-en');
                var jaLink = document.getElementById('fallback-ja');
                if (enLink) enLink.href = '/en/index.html';
                if (jaLink) jaLink.href = '/ja/index.html';
            }
        })();
    </script>
</body>
</html>
EOF
if [ -d "docs_src/pypi" ]; then
    echo "Building PyPI README images..."
    $DRAWLIB_CMD build image docs_src/pypi/ -o docs_html/pypi_images/
fi
echo "HTML site build complete: docs_html/"
