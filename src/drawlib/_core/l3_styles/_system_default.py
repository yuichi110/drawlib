# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Module for defining default parameter of styling models."""

from drawlib._core.l3_fonts import Font
from drawlib._core.l3_styles._colors import Colors
from drawlib._core.l3_styles._style_models import (
    IconStyle,
    ImageStyle,
    LineStyle,
    ShapeStyle,
    ShapeTextStyle,
    TextStyle,
)

SYSTEM_DEFAULT_ICON_STYLE = IconStyle(
    icon_style="thin",
    text_color=Colors.Black,
    fill_alpha=None,
    text_halign="center",
    text_valign="center",
)

SYSTEM_DEFAULT_IMAGE_STYLE = ImageStyle(
    text_halign="center",
    text_valign="center",
    line_style="solid",
    line_color=None,
    line_width=0,
    fill_color=None,
    fill_alpha=None,
)

SYSTEM_DEFAULT_LINE_STYLE = LineStyle(
    line_width=1.0,
    line_color=Colors.Black,
    fill_alpha=None,
    line_style="solid",
    arrow_head_scale=20.0,
    arrow_head_fill=False,
)

SYSTEM_DEFAULT_SHAPE_STYLE = ShapeStyle(
    text_halign="center",
    text_valign="center",
    line_width=1.0,
    line_style="solid",
    line_color=Colors.Black,
    fill_color=Colors.White,
    fill_alpha=None,
)

SYSTEM_DEFAULT_SHAPE_TEXT_STYLE = ShapeTextStyle(
    fill_alpha=None,
    text_color=Colors.Black,
    text_size=16,
    text_halign="center",
    text_valign="center",
    text_font=Font.SANSSERIF_REGULAR,
    text_angle=None,
    text_flip=False,
    text_xy_shift=None,
)

SYSTEM_DEFAULT_TEXT_STYLE = TextStyle(
    fill_alpha=None,
    text_color=Colors.Black,
    text_size=16,
    text_halign="center",
    text_valign="center",
    text_font=Font.SANSSERIF_REGULAR,
    text_bg_fill_alpha=None,
    text_bg_fill_color=None,
    # they will be applied if one of them is not None
    text_bg_line_color=Colors.Black,
    text_bg_line_style="solid",
    text_bg_line_width=1.0,
)
