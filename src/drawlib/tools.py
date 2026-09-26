# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Public developer tools facade for drawlib."""

from __future__ import annotations

from drawlib._builder.cache_manager import clear_cache, download_cache, list_cache
from drawlib._builder.doc_builder import (
    build_html,
    build_markdown,
    build_pdf,
    detect_document_type,
    export_code_block,
    show_code_block,
)
from drawlib._builder.image_builder import build_image
from drawlib._builder.project_init import init_project, list_project_types
from drawlib._css_templates import (
    export_css,
    get_css,
    list_css,
    list_html_css,
    list_pdf_css,
)
from drawlib._http_server import run_server, scan_broken_links, serve_docs

export_block = export_code_block
show_block = show_code_block

__all__ = [
    "build_html",
    "build_image",
    "build_markdown",
    "build_pdf",
    "clear_cache",
    "detect_document_type",
    "download_cache",
    "export_block",
    "export_code_block",
    "export_css",
    "get_css",
    "init_project",
    "list_cache",
    "list_css",
    "list_html_css",
    "list_pdf_css",
    "list_project_types",
    "run_server",
    "scan_broken_links",
    "serve_docs",
    "show_block",
    "show_code_block",
]
