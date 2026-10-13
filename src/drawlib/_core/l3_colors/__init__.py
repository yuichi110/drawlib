# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Package for core color base and utilities."""

from __future__ import annotations

from drawlib._core.l3_colors._base_colors import (
    BaseColors,
)
from drawlib._core.l3_colors._color import (
    Color,
    ColorType,
)
from drawlib._core.l3_colors._color_utils import (
    ColorUtils,
    get_intermediate_color,
    get_intermediate_colors,
)

__all__ = [
    # _base_colors.py
    "BaseColors",
    # _color.py
    "Color",
    "ColorType",
    # _color_utils.py
    "ColorUtils",
    "get_intermediate_color",
    "get_intermediate_colors",
]
