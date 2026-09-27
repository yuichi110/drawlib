# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Default style colors module."""

from __future__ import annotations

from typing import Final

from drawlib._core.l2_models import Color
from drawlib._core.l3_styles import ColorsBase
from drawlib._preset_colors._color_essentials import EssentialsStyleColors


class DefaultStyleColors(ColorsBase):
    """Class representing colors for default preset styles along with a transparent color."""

    Red: Final[Color] = EssentialsStyleColors.LightRed
    Green: Final[Color] = EssentialsStyleColors.LightGreen
    Blue: Final[Color] = EssentialsStyleColors.LightBlue
    Black: Final[Color] = EssentialsStyleColors.Black
    White: Final[Color] = EssentialsStyleColors.White


__all__ = [
    "DefaultStyleColors",
]
