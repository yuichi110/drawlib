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

from typing import Final

from drawlib._core.l2_models import Color
from drawlib._core.l3_styles import ColorsBase


class Colors(ColorsBase):
    """Class representing the 16 basic web colors along with a transparent color."""

    Aqua: Final[Color] = Color(0, 255, 255)
    Black: Final[Color] = Color(0, 0, 0)
    Blue: Final[Color] = Color(0, 0, 255)
    Fuchsia: Final[Color] = Color(255, 0, 255)
    Gray: Final[Color] = Color(128, 128, 128)
    Green: Final[Color] = Color(0, 128, 0)
    Lime: Final[Color] = Color(0, 255, 0)
    Maroon: Final[Color] = Color(128, 0, 0)
    Navy: Final[Color] = Color(0, 0, 128)
    Olive: Final[Color] = Color(128, 128, 0)
    Purple: Final[Color] = Color(128, 0, 128)
    Red: Final[Color] = Color(255, 0, 0)
    Silver: Final[Color] = Color(192, 192, 192)
    Teal: Final[Color] = Color(0, 128, 128)
    White: Final[Color] = Color(255, 255, 255)
    Yellow: Final[Color] = Color(255, 255, 0)


__all__ = [
    "Colors",
]
