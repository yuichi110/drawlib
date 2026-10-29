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

import importlib
from typing import TYPE_CHECKING, Any, Final

if TYPE_CHECKING:
    from drawlib._builder._common.cache_manager import clear_cache, download_cache, list_cache
    from drawlib._builder.doc_builder import (
        build_document,
        build_docx,
        build_html,
        build_markdown,
        build_pdf,
        detect_document_type,
        export_code_block,
        show_code_block,
    )
    from drawlib._builder.image_builder import build_image
    from drawlib._http_server import scan_broken_links, serve_docs
    from drawlib._slide import build_pptx, build_slide
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

_LAZY_ATTRS: Final[dict[str, str]] = {
    "clear_cache": "drawlib._builder._common.cache_manager",
    "download_cache": "drawlib._builder._common.cache_manager",
    "list_cache": "drawlib._builder._common.cache_manager",
    "build_document": "drawlib._builder.doc_builder",
    "build_docx": "drawlib._builder.doc_builder",
    "build_html": "drawlib._builder.doc_builder",
    "build_markdown": "drawlib._builder.doc_builder",
    "build_pdf": "drawlib._builder.doc_builder",
    "detect_document_type": "drawlib._builder.doc_builder",
    "export_code_block": "drawlib._builder.doc_builder",
    "show_code_block": "drawlib._builder.doc_builder",
    "build_image": "drawlib._builder.image_builder",
    "scan_broken_links": "drawlib._http_server",
    "serve_docs": "drawlib._http_server",
    "build_pptx": "drawlib._slide",
    "build_slide": "drawlib._slide",
    "export_css": "drawlib._templates",
    "get_css": "drawlib._templates",
    "init_project": "drawlib._templates",
    "list_css": "drawlib._templates",
    "list_html_css": "drawlib._templates",
    "list_pdf_css": "drawlib._templates",
    "list_project_types": "drawlib._templates",
    "list_slide_css": "drawlib._templates",
}


def __getattr__(name: str) -> Any:  # noqa: ANN401
    """Lazy-load developer tool functions on first access (PEP 562)."""
    if name in _LAZY_ATTRS:
        module = importlib.import_module(_LAZY_ATTRS[name])
        value = getattr(module, name)
        globals()[name] = value
        return value
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


def __dir__() -> list[str]:
    """Ensure lazy tool functions appear in dir() and autocompletion."""
    return sorted(__all__)


__all__ = [
    "build_document",
    "build_docx",
    "build_html",
    "build_image",
    "build_markdown",
    "build_pdf",
    "build_pptx",
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
