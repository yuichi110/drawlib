# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Monochrome colors module."""

from __future__ import annotations

from drawlib._core.l2_types import Color
from drawlib._core.l3_styles import BaseColors
from drawlib._preset_colors._color_default import default_colors


class MonochromeColors(BaseColors):
    """Class representing colors for monochrome preset styles along with a transparent color."""

    Black: Color = default_colors.Black
    Charcoal: Color = default_colors.Charcoal
    Graphite: Color = default_colors.Graphite
    Gray: Color = default_colors.Gray
    Silver: Color = default_colors.Silver
    Snow: Color = default_colors.Snow
    White: Color = default_colors.White

    # Semantic Colors
    Primary: Color = default_colors.White
    Secondary: Color = default_colors.Gray
    Accent: Color = default_colors.Black
    Muted: Color = default_colors.Snow
    Danger: Color | None = None
    Success: Color | None = None


monochrome_colors: MonochromeColors = MonochromeColors()

__all__ = [
    "MonochromeColors",
    "monochrome_colors",
]
