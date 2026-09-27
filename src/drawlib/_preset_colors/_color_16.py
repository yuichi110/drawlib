# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""16 standard web colors module."""

from __future__ import annotations

from drawlib._core.l2_types import Color
from drawlib._core.l3_styles import BaseColors


class Colors16(BaseColors):
    """Class representing the 16 basic web colors along with a transparent color."""

    Aqua: Color = Color(0, 255, 255)
    Black: Color = Color(0, 0, 0)
    Blue: Color = Color(0, 0, 255)
    Fuchsia: Color = Color(255, 0, 255)
    Gray: Color = Color(128, 128, 128)
    Green: Color = Color(0, 128, 0)
    Lime: Color = Color(0, 255, 0)
    Maroon: Color = Color(128, 0, 0)
    Navy: Color = Color(0, 0, 128)
    Olive: Color = Color(128, 128, 0)
    Purple: Color = Color(128, 0, 128)
    Red: Color = Color(255, 0, 0)
    Silver: Color = Color(192, 192, 192)
    Teal: Color = Color(0, 128, 128)
    White: Color = Color(255, 255, 255)
    Yellow: Color = Color(255, 255, 0)


Colors: Colors16 = Colors16()
colors_16: Colors16 = Colors

__all__ = [
    "Colors",
    "Colors16",
    "colors_16",
]
