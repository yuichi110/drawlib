# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Package for core drawing action modules."""

from drawlib.v0_2.private.l3_styles._colors import (
    Colors,
    Colors140,
    ColorsBase,
    ColorsThemeDefault,
    ColorsThemeEssentials,
    ColorsThemeMonochrome,
)
from drawlib.v0_2.private.l3_styles._style_models import (
    IconStyle,
    ImageStyle,
    LineStyle,
    ShapeStyle,
    ShapeTextStyle,
    TextStyle,
)
from drawlib.v0_2.private.l3_styles._system_default import (
    SYSTEM_DEFAULT_ICON_STYLE,
    SYSTEM_DEFAULT_IMAGE_STYLE,
    SYSTEM_DEFAULT_LINE_STYLE,
    SYSTEM_DEFAULT_SHAPE_STYLE,
    SYSTEM_DEFAULT_SHAPE_TEXT_STYLE,
    SYSTEM_DEFAULT_TEXT_STYLE,
)

__all__ = [
    # _colors.py
    "Colors",
    "Colors140",
    "ColorsBase",
    "ColorsThemeDefault",
    "ColorsThemeEssentials",
    "ColorsThemeMonochrome",
    # _style_models.py
    "IconStyle",
    "ImageStyle",
    "LineStyle",
    "ShapeStyle",
    "ShapeTextStyle",
    "TextStyle",
    # _system_default.py
    "SYSTEM_DEFAULT_ICON_STYLE",
    "SYSTEM_DEFAULT_IMAGE_STYLE",
    "SYSTEM_DEFAULT_LINE_STYLE",
    "SYSTEM_DEFAULT_SHAPE_STYLE",
    "SYSTEM_DEFAULT_SHAPE_TEXT_STYLE",
    "SYSTEM_DEFAULT_TEXT_STYLE",
]
