# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Build script to compile docs_src into GitHub-readable docs/ and web-ready docs_html/."""

from __future__ import annotations

import shutil
from pathlib import Path

from drawlib.tools import build_html, build_markdown
from tools.dcli.common import PROJECT_ROOT


def build_docs() -> None:
    """Build docs (markdown for GitHub) and docs_html (HTML for web publishing)."""
    docs_src_dir = PROJECT_ROOT / "docs_src"
    docs_dir = PROJECT_ROOT / "docs"
    docs_html_dir = PROJECT_ROOT / "docs_html"

    if docs_dir.exists():
        shutil.rmtree(docs_dir)
    if docs_html_dir.exists():
        shutil.rmtree(docs_html_dir)

    print(f"Building Markdown docs for GitHub: {docs_src_dir} -> {docs_dir}")
    build_markdown(input_dir=str(docs_src_dir), output_dir=str(docs_dir))

    print(f"Building HTML docs for Web: {docs_src_dir} -> {docs_html_dir}")
    build_html(input_dir=str(docs_src_dir), output_dir=str(docs_html_dir))

    print("\nDocumentation build completed successfully!")


if __name__ == "__main__":
    build_docs()
