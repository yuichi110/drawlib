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

from drawlib._core.l2_types import TypeColorRGB
from drawlib._core.l3_styles import ColorsBase


class Colors(ColorsBase):
    """Class representing the 16 basic web colors along with a transparent color."""

    Aqua: Final[TypeColorRGB] = (0, 255, 255)
    Black: Final[TypeColorRGB] = (0, 0, 0)
    Blue: Final[TypeColorRGB] = (0, 0, 255)
    Fuchsia: Final[TypeColorRGB] = (255, 0, 255)
    Gray: Final[TypeColorRGB] = (128, 128, 128)
    Green: Final[TypeColorRGB] = (0, 128, 0)
    Lime: Final[TypeColorRGB] = (0, 255, 0)
    Maroon: Final[TypeColorRGB] = (128, 0, 0)
    Navy: Final[TypeColorRGB] = (0, 0, 128)
    Olive: Final[TypeColorRGB] = (128, 128, 0)
    Purple: Final[TypeColorRGB] = (128, 0, 128)
    Red: Final[TypeColorRGB] = (255, 0, 0)
    Silver: Final[TypeColorRGB] = (192, 192, 192)
    Teal: Final[TypeColorRGB] = (0, 128, 128)
    White: Final[TypeColorRGB] = (255, 255, 255)
    Yellow: Final[TypeColorRGB] = (255, 255, 0)


__all__ = [
    "Colors",
]
