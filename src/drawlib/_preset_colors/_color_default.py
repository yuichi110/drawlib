# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Default colors module."""

from __future__ import annotations

from drawlib._core.l2_types import Color
from drawlib._core.l3_styles import BaseColors


class DefaultColors(BaseColors):
    """Class representing colors for default preset styles along with a transparent color."""

    Red: Color = Color(255, 23, 23)
    LightRed: Color = Color(239, 95, 95)
    Green: Color = Color(15, 127, 15)
    LightGreen: Color = Color(79, 191, 79)
    Blue: Color = Color(31, 31, 255)
    LightBlue: Color = Color(111, 111, 239)
    Yellow: Color = Color(239, 239, 31)
    Purple: Color = Color(127, 31, 127)
    Orange: Color = Color(255, 95, 31)
    Navy: Color = Color(15, 15, 127)
    Pink: Color = Color(239, 63, 239)
    Charcoal: Color = Color(39, 39, 39)
    Graphite: Color = Color(63, 63, 63)
    Gray: Color = Color(127, 127, 127)
    Silver: Color = Color(191, 191, 191)
    Snow: Color = Color(239, 239, 239)
    Teal: Color = Color(15, 127, 127)
    Olive: Color = Color(127, 127, 31)
    Brown: Color = Color(159, 31, 31)
    Black: Color = Color(0, 0, 0)
    White: Color = Color(255, 255, 255)
    Aqua: Color = Color(47, 239, 239)
    GreenYellow: Color = Color(127, 207, 31)
    Ivory: Color = Color(239, 239, 207)
    Steel: Color = Color(96, 96, 143)

    # Semantic Colors
    Primary: Color = LightBlue
    Secondary: Color = Teal
    Accent: Color = Orange
    Muted: Color = Snow
    Danger: Color = Red
    Success: Color = Green


default_colors: DefaultColors = DefaultColors()

__all__ = [
    "DefaultColors",
    "default_colors",
]
