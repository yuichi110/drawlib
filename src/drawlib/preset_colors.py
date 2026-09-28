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
    DefaultDarkColors,
    DefaultLightColors,
    GoogleColors,
    MonochromeColors,
    colors_16,
    colors_140,
    default_colors,
    default_dark_colors,
    default_light_colors,
    google_colors,
    monochrome_colors,
)


def from_hex(hexcode: str, alpha: float | None = None) -> Color:
    """Create a Color instance from a hexadecimal string.

    Args:
        hexcode (str): Hex color string (e.g. '#3498db', '#FF0000').
        alpha (float | None): Optional alpha override (0.0 - 1.0).

    Returns:
        Color: Color instance.
    """
    return Color.from_hex(hexcode, alpha=alpha)


EssentialsStyleColors = DefaultColors


__all__ = [
    # Color Model
    "Color",
    "from_hex",
    # Color Classes
    "BaseColors",
    "Colors140Model",
    "Colors16",
    "DefaultColors",
    "DefaultDarkColors",
    "DefaultLightColors",
    "EssentialsStyleColors",
    "GoogleColors",
    "MonochromeColors",
    # Color Instances
    "Colors",
    "Colors140",
    "colors_140",
    "colors_16",
    "default_colors",
    "default_dark_colors",
    "default_light_colors",
    "google_colors",
    "monochrome_colors",
]
