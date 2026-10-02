# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Visualizers package for drawlib CLI commands."""

from __future__ import annotations

from drawlib._cli._visualizers._common import display_dimage
from drawlib._cli._visualizers.colors import render_color_chart
from drawlib._cli._visualizers.styles import (
    export_all_pages,
    get_styles_page_count,
    handle_single_page_output,
    render_styles_matrix,
)

__all__ = [
    "display_dimage",
    "export_all_pages",
    "get_styles_page_count",
    "handle_single_page_output",
    "render_color_chart",
    "render_styles_matrix",
]
