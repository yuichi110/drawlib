# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Essentials style colors module."""

from __future__ import annotations

from typing import Final

from drawlib._core.l2_models import Color
from drawlib._core.l3_styles import ColorsBase


class EssentialsStyleColors(ColorsBase):
    """Class representing colors for essentials preset styles along with a transparent color."""

    Red: Final[Color] = Color(255, 23, 23)
    LightRed: Final[Color] = Color(239, 95, 95)
    Green: Final[Color] = Color(15, 127, 15)
    LightGreen: Final[Color] = Color(79, 191, 79)
    Blue: Final[Color] = Color(31, 31, 255)
    LightBlue: Final[Color] = Color(111, 111, 239)
    Yellow: Final[Color] = Color(239, 239, 31)
    Purple: Final[Color] = Color(127, 31, 127)
    Orange: Final[Color] = Color(255, 95, 31)
    Navy: Final[Color] = Color(15, 15, 127)
    Pink: Final[Color] = Color(239, 63, 239)
    Charcoal: Final[Color] = Color(39, 39, 39)
    Graphite: Final[Color] = Color(63, 63, 63)
    Gray: Final[Color] = Color(127, 127, 127)
    Silver: Final[Color] = Color(191, 191, 191)
    Snow: Final[Color] = Color(239, 239, 239)
    Teal: Final[Color] = Color(15, 127, 127)
    Olive: Final[Color] = Color(127, 127, 31)
    Brown: Final[Color] = Color(159, 31, 31)
    Black: Final[Color] = Color(0, 0, 0)
    White: Final[Color] = Color(255, 255, 255)
    Aqua: Final[Color] = Color(47, 239, 239)
    GreenYellow: Final[Color] = Color(127, 207, 31)
    Ivory: Final[Color] = Color(239, 239, 207)
    Steel: Final[Color] = Color(96, 96, 143)


__all__ = [
    "EssentialsStyleColors",
]
