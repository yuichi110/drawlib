# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Public preset colors module for drawlib."""

from drawlib._core.l2_types import Color
from drawlib._preset_colors import (
    BaseColors,
    Colors,
    Colors16,
    Colors140,
    Colors140Model,
    DefaultColors,
    GoogleColors,
    MonochromeColors,
    colors_16,
    colors_140,
    default_colors,
    google_colors,
    monochrome_colors,
)

__all__ = [
    # Color Model
    "Color",
    # Color Classes
    "BaseColors",
    "Colors140Model",
    "Colors16",
    "DefaultColors",
    "GoogleColors",
    "MonochromeColors",
    # Color Instances
    "Colors",
    "Colors140",
    "colors_140",
    "colors_16",
    "default_colors",
    "google_colors",
    "monochrome_colors",
]
