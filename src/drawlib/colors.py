# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Public colors module for drawlib."""

from drawlib._core.l2_models import Color
from drawlib._preset_colors import (
    Colors,
    Colors140,
    ColorsBase,
    DefaultStyleColors,
    EssentialsStyleColors,
    GoogleStyleColors,
    MonochromeStyleColors,
)

# Backward compatibility aliases
ColorsDefault = DefaultStyleColors
ColorsEssentials = EssentialsStyleColors
ColorsMonochrome = MonochromeStyleColors
ColorsGoogle = GoogleStyleColors

__all__ = [
    # Color Model
    "Color",
    # Color Classes
    "Colors",
    "Colors140",
    "ColorsBase",
    "DefaultStyleColors",
    "EssentialsStyleColors",
    "GoogleStyleColors",
    "MonochromeStyleColors",
    # Backward compatibility aliases
    "ColorsDefault",
    "ColorsEssentials",
    "ColorsGoogle",
    "ColorsMonochrome",
]
