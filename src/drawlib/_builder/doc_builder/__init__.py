# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Document compiler package for drawlib."""

from __future__ import annotations

from typing import Any, List, Optional, Sequence, Union

from drawlib._builder._common import (
    BuildImageCache,
    FileBuildProgress,
    load_styles_and_utils,
    resolve_styles_and_utils,
)
from drawlib._builder.doc_builder.compiler import (
    build_html,
    build_markdown,
    build_pdf,
)
from drawlib._builder.doc_builder.detector import (
    DocType,
    DocumentInputInfo,
    detect_document_type,
)
from drawlib._builder.doc_builder.exporter_html import (
    get_default_css,
    render_html_document,
)
from drawlib._builder.doc_builder.exporter_md import write_rendered_markdown
from drawlib._builder.doc_builder.exporter_pdf import export_html_to_pdf
from drawlib._builder.doc_builder.merger import build_merged_html, expand_input_files
from drawlib._builder.doc_builder.navbar import (
    NavbarItem,
    NavbarSection,
    parse_navbar_markdown,
    resolve_navbar_for_page,
)
from drawlib._builder.doc_builder.parser_md import parse_markdown_to_html
from drawlib._builder.doc_builder.processor import (
    DrawlibBlockProcessor,
    export_code_block,
    extract_code_blocks,
    show_code_block,
)
from drawlib._builder.doc_builder.progress import (
    check_document_output_duplicates,
    format_duplicate_output_error,
)
from drawlib._templates import (
    export_css,
    list_css,
    list_html_css,
    list_pdf_css,
)


def build_document(
    input_dir: str,
    output_path: Optional[str] = None,
    output_format: Optional[str] = None,
    *,
    image_format: str = "png",
    css_mode: str = "external",
    styles_path: Optional[str] = None,
    utils_path: Optional[str] = None,
    no_cache: bool = False,
    timestamp: bool = False,
) -> str:
    """Compile input documentation directory into HTML, PDF, or Markdown.

    Args:
        input_dir (str): Directory containing documentation source files.
        output_path (Optional[str]): Output directory or destination file.
        output_format (Optional[str]): 'html', 'pdf', or 'markdown'. Defaults to 'html'.
        image_format (str): 'png' or 'webp'. Defaults to 'png'.
        css_mode (str): CSS mode for HTML ('external' or 'embed').
        styles_path (Optional[str]): Path to custom styles.py script.
        utils_path (Optional[str]): Path to custom utils.py script.
        no_cache (bool): If True, disable image build caching.
        timestamp (bool): Include build timestamp in PDF if output_format is 'pdf'.

    Returns:
        str: Absolute path of generated output directory or file.
    """
    fmt = output_format.lower() if output_format else None
    if not fmt:
        if output_path and output_path.endswith(".pdf"):
            fmt = "pdf"
        elif output_path and output_path.endswith(".md"):
            fmt = "markdown"
        else:
            fmt = "html"

    if fmt == "markdown":
        return build_markdown(
            input_dir=input_dir,
            output_dir=output_path,
            image_format=image_format,
            styles_path=styles_path,
            utils_path=utils_path,
            no_cache=no_cache,
        )
    if fmt == "pdf":
        return build_pdf(
            input_dir=input_dir,
            output_file=output_path,
            styles_path=styles_path,
            utils_path=utils_path,
            no_cache=no_cache,
            timestamp=timestamp,
        )
    return build_html(
        input_dir=input_dir,
        output_dir=output_path,
        image_format=image_format,
        styles_path=styles_path,
        utils_path=utils_path,
        no_cache=no_cache,
        css_mode=css_mode,
    )


__all__ = [
    "BuildImageCache",
    "DocType",
    "DocumentInputInfo",
    "DrawlibBlockProcessor",
    "FileBuildProgress",
    "NavbarItem",
    "NavbarSection",
    "build_document",
    "build_html",
    "build_markdown",
    "build_merged_html",
    "build_pdf",
    "check_document_output_duplicates",
    "detect_document_type",
    "export_code_block",
    "export_css",
    "export_html_to_pdf",
    "extract_code_blocks",
    "format_duplicate_output_error",
    "get_default_css",
    "list_css",
    "list_html_css",
    "list_pdf_css",
    "load_styles_and_utils",
    "parse_markdown_to_html",
    "parse_navbar_markdown",
    "render_html_document",
    "resolve_navbar_for_page",
    "resolve_styles_and_utils",
    "show_code_block",
    "write_rendered_markdown",
]
