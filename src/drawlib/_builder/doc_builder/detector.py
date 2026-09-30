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
from typing import Literal

from pydantic import BaseModel, ConfigDict

DocType = Literal["markdown_drawlib", "markdown", "html_drawlib", "html"]

_MD_DRAWLIB_PATTERN = re.compile(r"(?:^|\n)[ \t]*```drawlib\b", re.IGNORECASE)
_HTML_DRAWLIB_PATTERN = re.compile(
    r'<script\b[^>]*type=["\']text/drawlib["\'][^>]*>.*?</script>',
    re.DOTALL | re.IGNORECASE,
)
_FULL_HTML_PATTERN = re.compile(r"<!doctype\s+html\b|<html\b", re.IGNORECASE)


class DocumentInputInfo(BaseModel):
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

    model_config = ConfigDict(frozen=True)

    path: str
    doc_type: DocType
    has_drawlib: bool
    is_markdown: bool
    is_html: bool
    is_full_html: bool
    block_count: int


def preserve_outer_fences(text: str) -> tuple[str, list[tuple[str, list[str]]]]:
    """Preserve outer code fence blocks (opened with 4 or more backticks/tildes).

    Any nested drawlib code blocks inside these outer fences are preserved as literal
    markdown text and will not be compiled into images or replaced with HTML.
    Preserves exact line counts so subsequent line number calculations remain accurate.

    Args:
        text (str): Input Markdown text.

    Returns:
        tuple[str, list[tuple[str, list[str]]]]: Masked text and list of (placeholder_block, original_lines).
    """
    lines = text.split("\n")
    preserved: list[tuple[str, list[str]]] = []
    output_lines: list[str] = []

    in_outer_fence = False
    fence_char = ""
    fence_len = 0
    current_fence_lines: list[str] = []

    for line in lines:
        if not in_outer_fence:
            m = re.match(r"^[ \t]{0,3}(`{4,}|~{4,})", line)
            if m:
                in_outer_fence = True
                fence_char = m.group(1)[0]
                fence_len = len(m.group(1))
                current_fence_lines = [line]
                continue
            output_lines.append(line)
        else:
            current_fence_lines.append(line)
            close_pattern = rf"^[ \t]{{0,3}}{re.escape(fence_char)}{{{fence_len},}}[ \t\r]*$"
            if re.match(close_pattern, line):
                in_outer_fence = False
                idx = len(preserved)
                eol = "\r" if current_fence_lines[0].endswith("\r") else ""
                placeholder_lines = [f"__DRAWLIB_PRESERVED_FENCE_{idx}__{eol}"]
                for pad_idx in range(len(current_fence_lines) - 1):
                    pad_eol = "\r" if current_fence_lines[pad_idx + 1].endswith("\r") else ""
                    placeholder_lines.append(f"__DRAWLIB_FENCE_PAD_{idx}_{pad_idx}__{pad_eol}")
                placeholder_block = "\n".join(placeholder_lines)
                preserved.append((placeholder_block, current_fence_lines))
                output_lines.extend(placeholder_lines)
                current_fence_lines = []

    if in_outer_fence and current_fence_lines:
        output_lines.extend(current_fence_lines)

    return "\n".join(output_lines), preserved


def restore_outer_fences(text: str, preserved: list[tuple[str, list[str]]]) -> str:
    """Restore preserved code fence blocks from placeholders.

    Args:
        text (str): Markdown text containing fence placeholders.
        preserved (list[tuple[str, list[str]]]): Preserved block records.

    Returns:
        str: Fully restored Markdown text.
    """
    for placeholder_block, original_lines in preserved:
        original_block = "\n".join(original_lines)
        text = text.replace(placeholder_block, original_block)
    return text


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
        masked_content, _ = preserve_outer_fences(content)
        matches = _MD_DRAWLIB_PATTERN.findall(masked_content)
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
