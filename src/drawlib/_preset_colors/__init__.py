# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Private preset colors package for drawlib."""

from drawlib._core.styles import BaseColors
from drawlib._preset_colors._color_140 import Colors140
from drawlib._preset_colors._color_default import (
    DefaultColors,
    DefaultColors1,
    DefaultColors2,
    DefaultColors3,
    DefaultColors4,
    DefaultColors5,
    DefaultColors6,
    DefaultDarkColors,
    DefaultLightColors,
)
from drawlib._preset_colors._color_google import GoogleColors
from drawlib._preset_colors._color_monochrome import MonochromeColors

__all__ = [
    "BaseColors",
    "Colors140",
    "DefaultColors",
    "DefaultColors1",
    "DefaultColors2",
    "DefaultColors3",
    "DefaultColors4",
    "DefaultColors5",
    "DefaultColors6",
    "DefaultDarkColors",
    "DefaultLightColors",
    "GoogleColors",
    "MonochromeColors",
]
