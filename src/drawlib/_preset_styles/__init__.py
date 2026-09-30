# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Private preset_styles package for drawlib."""

from drawlib._core.styles import (
    BaseStyles,
)
from drawlib._preset_styles._style_default import (
    DefaultDarkStyles,
    DefaultLightStyles,
    DefaultStyles,
    DefaultStyles1,
    DefaultStyles2,
    DefaultStyles3,
    DefaultStyles4,
    DefaultStyles5,
    DefaultStyles6,
)
from drawlib._preset_styles._style_google import GoogleStyles
from drawlib._preset_styles._style_monochrome import MonochromeStyles

__all__ = [
    "BaseStyles",
    "DefaultDarkStyles",
    "DefaultLightStyles",
    "DefaultStyles",
    "DefaultStyles1",
    "DefaultStyles2",
    "DefaultStyles3",
    "DefaultStyles4",
    "DefaultStyles5",
    "DefaultStyles6",
    "GoogleStyles",
    "MonochromeStyles",
]
