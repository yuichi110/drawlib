# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Markdown parser using markdown-it-py with raw HTML passthrough enabled."""

import re

from markdown_it import MarkdownIt


def rewrite_relative_md_links(html: str) -> str:
    """Rewrite relative href links ending in .md to .html.

    Args:
        html (str): Input HTML string.

    Returns:
        str: Transformed HTML string.
    """
    pattern = re.compile(r'href=["\'](?!https?://|//|#)([^"\']+\.md)(#[^"\']*)?["\']', re.IGNORECASE)

    def repl(match: re.Match[str]) -> str:
        path = match.group(1)
        anchor = match.group(2) or ""
        html_path = path[:-3] + ".html"
        return f'href="{html_path}{anchor}"'

    return pattern.sub(repl, html)


def parse_markdown_to_html(markdown_text: str) -> str:
    """Convert Markdown text to HTML body snippet with relative .md links rewritten to .html.

    Args:
        markdown_text (str): Input Markdown string.

    Returns:
        str: Converted HTML snippet string.
    """
    md = MarkdownIt("gfm-like", {"html": True, "linkify": False, "typographer": True})
    raw_html = md.render(markdown_text)
    return rewrite_relative_md_links(raw_html)
