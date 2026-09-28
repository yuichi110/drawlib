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


class MonochromeColors(BaseColors):
    """Class representing colors for monochrome preset styles along with a transparent color."""

    White: Color = Color(255, 255, 255)
    Gray1: Color = Color(245, 245, 245)
    Gray2: Color = Color(220, 220, 220)
    Gray3: Color = Color(180, 180, 180)
    Gray4: Color = Color(130, 130, 130)
    Gray5: Color = Color(75, 75, 75)
    Gray6: Color = Color(35, 35, 35)
    Black: Color = Color(0, 0, 0)

    # Semantic Colors
    Primary: Color = White
    Secondary: Color = Gray2
    Accent: Color = Black
    Muted: Color = Gray1
    Light: Color = White
    Dark: Color = Gray6
    Danger: Color | None = None
    Success: Color | None = None
    Canvas: Color = White


monochrome_colors: MonochromeColors = MonochromeColors()

__all__ = [
    "MonochromeColors",
    "monochrome_colors",
]
