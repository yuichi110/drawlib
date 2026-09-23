# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unified document input type detector for drawlib doc_builder."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Literal

DocType = Literal["markdown_drawlib", "markdown", "html_drawlib", "html"]

_MD_DRAWLIB_PATTERN = re.compile(r"(?:^|\n)[ \t]*```drawlib\b", re.IGNORECASE)
_HTML_DRAWLIB_PATTERN = re.compile(
    r'<script\b[^>]*type=["\']text/drawlib["\'][^>]*>.*?</script>',
    re.DOTALL | re.IGNORECASE,
)
_FULL_HTML_PATTERN = re.compile(r"<!doctype\s+html\b|<html\b", re.IGNORECASE)


@dataclass(frozen=True)
class DocumentInputInfo:
    """Classification metadata for an input document file.

    Attributes:
        path (str): Absolute or relative path to the input document.
        doc_type (DocType): Canonical document type ('markdown_drawlib', 'markdown', 'html_drawlib', 'html').
        has_drawlib (bool): True if the document contains executable drawlib code blocks.
        is_markdown (bool): True if the document is a Markdown file (.md, .markdown).
        is_html (bool): True if the document is an HTML file (.html, .htm).
        is_full_html (bool): True if the HTML document includes <!DOCTYPE html> or <html> root tags.
        block_count (int): Number of drawlib code blocks detected in the document.
    """

    path: str
    doc_type: DocType
    has_drawlib: bool
    is_markdown: bool
    is_html: bool
    is_full_html: bool
    block_count: int


def detect_document_type(file_path: str, content: str | None = None) -> DocumentInputInfo:
    """Classify an input Markdown or HTML document into one of 4 canonical document types.

    Args:
        file_path (str): Path to the input document (.md, .markdown, .html, .htm).
        content (str | None): Optional pre-loaded file text content. If None, reads from file_path.

    Returns:
        DocumentInputInfo: Classification metadata for the input document.

    Raises:
        ValueError: If file extension is neither Markdown nor HTML.
    """
    ext = os.path.splitext(file_path)[1].lower()
    if content is None:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

    if ext in {".md", ".markdown"}:
        matches = _MD_DRAWLIB_PATTERN.findall(content)
        block_count = len(matches)
        has_drawlib = block_count > 0
        doc_type: DocType = "markdown_drawlib" if has_drawlib else "markdown"
        return DocumentInputInfo(
            path=file_path,
            doc_type=doc_type,
            has_drawlib=has_drawlib,
            is_markdown=True,
            is_html=False,
            is_full_html=False,
            block_count=block_count,
        )

    if ext in {".html", ".htm"}:
        matches = _HTML_DRAWLIB_PATTERN.findall(content)
        block_count = len(matches)
        has_drawlib = block_count > 0
        is_full_html = bool(_FULL_HTML_PATTERN.search(content))
        doc_type = "html_drawlib" if has_drawlib else "html"
        return DocumentInputInfo(
            path=file_path,
            doc_type=doc_type,
            has_drawlib=has_drawlib,
            is_markdown=False,
            is_html=True,
            is_full_html=is_full_html,
            block_count=block_count,
        )

    raise ValueError(f"Unsupported document extension '{ext}' for '{file_path}'. Expected .md or .html.")
