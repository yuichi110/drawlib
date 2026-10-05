# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Public developer tools facade for drawlib.

Provides document and image compilation, diagram export, project scaffolding,
local preview server, CSS preset inspection, and cache management functions.
"""

from __future__ import annotations

from drawlib._builder._common.cache_manager import clear_cache, download_cache, list_cache
from drawlib._builder.doc_builder import (
    build_document,
    build_html,
    build_markdown,
    build_pdf,
    detect_document_type,
    export_code_block,
    show_code_block,
)
from drawlib._builder.image_builder import build_image
from drawlib._http_server import scan_broken_links, serve_docs
from drawlib._slide import build_slide
from drawlib._templates import (
    export_css,
    get_css,
    init_project,
    list_css,
    list_html_css,
    list_pdf_css,
    list_project_types,
    list_slide_css,
)

__all__ = [
    "build_document",
    "build_html",
    "build_image",
    "build_markdown",
    "build_pdf",
    "build_slide",
    "clear_cache",
    "detect_document_type",
    "download_cache",
    "export_code_block",
    "export_css",
    "get_css",
    "init_project",
    "list_cache",
    "list_css",
    "list_html_css",
    "list_pdf_css",
    "list_project_types",
    "list_slide_css",
    "scan_broken_links",
    "serve_docs",
    "show_code_block",
]
