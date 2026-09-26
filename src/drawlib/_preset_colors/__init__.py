# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Private preset colors package for drawlib."""

from drawlib._core.l3_styles import ColorsBase
from drawlib._preset_colors._color_16 import Colors
from drawlib._preset_colors._color_140 import Colors140
from drawlib._preset_colors._color_default import DefaultStyleColors
from drawlib._preset_colors._color_essentials import EssentialsStyleColors
from drawlib._preset_colors._color_google import GoogleStyleColors
from drawlib._preset_colors._color_monochrome import MonochromeStyleColors

__all__ = [
    "Colors",
    "Colors140",
    "ColorsBase",
    "DefaultStyleColors",
    "EssentialsStyleColors",
    "GoogleStyleColors",
    "MonochromeStyleColors",
]
