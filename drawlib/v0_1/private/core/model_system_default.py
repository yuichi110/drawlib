# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Module for defining default parameter of styling models."""

from drawlib.v0_1.private.core.colors import Colors
from drawlib.v0_1.private.core.fonts import Font
from drawlib.v0_1.private.core.model import (
    IconStyle,
    ImageStyle,
    LineStyle,
    ShapeStyle,
    ShapeTextStyle,
    TextStyle,
)

SYSTEM_DEFAULT_ICON_STYLE = IconStyle(
    style="thin",
    color=Colors.Black,
    alpha=None,
    halign="center",
    valign="center",
)

SYSTEM_DEFAULT_IMAGE_STYLE = ImageStyle(
    halign="center",
    valign="center",
    lstyle="solid",
    lcolor=Colors.Black,
    lwidth=0,
    fcolor=None,
    alpha=None,
)

SYSTEM_DEFAULT_LINE_STYLE = LineStyle(
    width=1.0,
    color=Colors.Black,
    alpha=None,
    style="solid",
    ahscale=20.0,
    ahfill=False,
)

SYSTEM_DEFAULT_SHAPE_STYLE = ShapeStyle(
    halign="center",
    valign="center",
    lwidth=1.0,
    lstyle="solid",
    lcolor=Colors.Black,
    fcolor=Colors.White,
    alpha=None,
)

SYSTEM_DEFAULT_SHAPE_TEXT_STYLE = ShapeTextStyle(
    alpha=None,
    color=Colors.Black,
    size=16,
    halign="center",
    valign="center",
    font=Font.SANSSERIF_REGULAR,
    angle=None,
    flip=False,
    xy_shift=None,
)

SYSTEM_DEFAULT_TEXT_STYLE = TextStyle(
    alpha=None,
    color=Colors.Black,
    size=16,
    halign="center",
    valign="center",
    font=Font.SANSSERIF_REGULAR,
    bgalpha=None,
    bgfcolor=None,
    # they will be applied if one of them is not None
    bglcolor=Colors.Black,
    bglstyle="solid",
    bglwidth=1.0,
)
