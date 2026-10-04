# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Public builder module for drawlib.

Provides document and image compilation functions for HTML, Markdown, PDF, and images.
"""

from __future__ import annotations

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
from drawlib._slide import build_slide

__all__ = [
    "build_document",
    "build_html",
    "build_image",
    "build_markdown",
    "build_pdf",
    "build_slide",
    "detect_document_type",
    "export_code_block",
    "show_code_block",
]
