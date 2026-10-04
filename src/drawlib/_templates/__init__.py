# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Drawlib templates and theme assets package."""

from drawlib._templates.builder import (
    BUILTIN_CSS_PRESETS,
    BUILTIN_HTML_CSS_PRESETS,
    BUILTIN_PDF_CSS_PRESETS,
    BUILTIN_SLIDE_CSS_PRESETS,
    BUILTIN_THEMES,
    PROJECT_TYPES,
    export_css,
    get_css,
    get_slide_js,
    init_project,
    list_css,
    list_html_css,
    list_pdf_css,
    list_project_types,
    list_slide_css,
)

__all__ = [
    "BUILTIN_CSS_PRESETS",
    "BUILTIN_HTML_CSS_PRESETS",
    "BUILTIN_PDF_CSS_PRESETS",
    "BUILTIN_SLIDE_CSS_PRESETS",
    "BUILTIN_THEMES",
    "PROJECT_TYPES",
    "export_css",
    "get_css",
    "get_slide_js",
    "init_project",
    "list_css",
    "list_html_css",
    "list_pdf_css",
    "list_project_types",
    "list_slide_css",
]
