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

from drawlib._builder._common.cache_manager import clear_cache, download_cache, list_cache
from drawlib._http_server import scan_broken_links, serve_docs
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
    "clear_cache",
    "download_cache",
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
]
