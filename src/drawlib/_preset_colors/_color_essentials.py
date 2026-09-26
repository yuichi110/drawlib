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

from drawlib._core.l2_types import TypeColorRGB
from drawlib._core.l3_styles import ColorsBase


class EssentialsStyleColors(ColorsBase):
    """Class representing colors for essentials preset styles along with a transparent color."""

    Red: Final[TypeColorRGB] = (255, 23, 23)
    LightRed: Final[TypeColorRGB] = (239, 95, 95)
    Green: Final[TypeColorRGB] = (15, 127, 15)
    LightGreen: Final[TypeColorRGB] = (79, 191, 79)
    Blue: Final[TypeColorRGB] = (31, 31, 255)
    LightBlue: Final[TypeColorRGB] = (111, 111, 239)
    Yellow: Final[TypeColorRGB] = (239, 239, 31)
    Purple: Final[TypeColorRGB] = (127, 31, 127)
    Orange: Final[TypeColorRGB] = (255, 95, 31)
    Navy: Final[TypeColorRGB] = (15, 15, 127)
    Pink: Final[TypeColorRGB] = (239, 63, 239)
    Charcoal: Final[TypeColorRGB] = (39, 39, 39)
    Graphite: Final[TypeColorRGB] = (63, 63, 63)
    Gray: Final[TypeColorRGB] = (127, 127, 127)
    Silver: Final[TypeColorRGB] = (191, 191, 191)
    Snow: Final[TypeColorRGB] = (239, 239, 239)
    Teal: Final[TypeColorRGB] = (15, 127, 127)
    Olive: Final[TypeColorRGB] = (127, 127, 31)
    Brown: Final[TypeColorRGB] = (159, 31, 31)
    Black: Final[TypeColorRGB] = (0, 0, 0)
    White: Final[TypeColorRGB] = (255, 255, 255)
    Aqua: Final[TypeColorRGB] = (47, 239, 239)
    GreenYellow: Final[TypeColorRGB] = (127, 207, 31)
    Ivory: Final[TypeColorRGB] = (239, 239, 207)
    Steel: Final[TypeColorRGB] = (96, 96, 143)


__all__ = [
    "EssentialsStyleColors",
]
