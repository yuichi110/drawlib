# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Public styles module for drawlib.

Provides the active preset styles and corresponding theme colors for drawings.
"""

from __future__ import annotations

from drawlib.preset_colors import Color, DefaultColors
from drawlib.preset_styles import DefaultStyles, Style

# Active design tokens
Colors: DefaultColors = DefaultColors()
Styles: DefaultStyles = DefaultStyles()

__all__ = [
    "Color",
    "Colors",
    "Style",
    "Styles",
]
