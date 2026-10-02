# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Styles visualizers package and matrix dispatcher."""

from __future__ import annotations

from drawlib._cli._visualizers.styles.base import (
    COL_HEADERS,
    SEMANTIC_ROLES,
    VARIANTS,
    draw_swatch,
    export_all_pages,
    extract_base_colors,
    format_supports_badge,
    get_row_keys,
    get_styles_page_count,
    handle_single_page_output,
    render_legend,
    render_styles_matrix,
)
from drawlib._cli._visualizers.styles.default import DefaultStylesVisualizer
from drawlib._cli._visualizers.styles.google import GoogleStylesVisualizer
from drawlib._cli._visualizers.styles.monochrome import MonochromeStylesVisualizer

__all__ = [
    "COL_HEADERS",
    "DefaultStylesVisualizer",
    "GoogleStylesVisualizer",
    "MonochromeStylesVisualizer",
    "SEMANTIC_ROLES",
    "VARIANTS",
    "draw_swatch",
    "export_all_pages",
    "extract_base_colors",
    "format_supports_badge",
    "get_row_keys",
    "get_styles_page_count",
    "handle_single_page_output",
    "render_legend",
    "render_styles_matrix",
]
