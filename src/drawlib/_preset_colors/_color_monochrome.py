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

from drawlib._core.styles import BaseColors, Color


class MonochromeColors(BaseColors):
    """Class representing colors for monochrome preset styles along with a transparent color."""

    White: Color = Color(255, 255, 255)
    Gray1: Color = Color(245, 245, 245)
    Gray2: Color = Color(230, 230, 230)
    Gray3: Color = Color(210, 210, 210)
    Gray4: Color = Color(175, 175, 175)
    Gray5: Color = Color(135, 135, 135)
    Gray6: Color = Color(95, 95, 95)
    Gray7: Color = Color(55, 55, 55)
    Gray8: Color = Color(25, 25, 25)
    Black: Color = Color(0, 0, 0)

    # Semantic Colors
    Primary: Color = White
    Secondary: Color = Gray2
    Accent: Color = Black
    Muted: Color = Gray1
    Light: Color = White
    Dark: Color = Gray8
    Danger: Color | None = None
    Success: Color | None = None
    Canvas: Color = White


__all__ = [
    "MonochromeColors",
]
