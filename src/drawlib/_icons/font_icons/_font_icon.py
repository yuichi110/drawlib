# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""font_icon() implementation module."""

from drawlib._core.l1_core import guarded
from drawlib._core.l2_types import (
    TypeAngle,
    TypeCoordinate,
    TypePosFloat,
    TypeStr,
)
from drawlib._core.l3_fonts import FontFile
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import get_fontsize_from_charwidth, text
from drawlib._icons._utils import IconUtil


@guarded
def font_icon(
    xy: TypeCoordinate,
    width: TypePosFloat,
    code: TypeStr,
    file: TypeStr,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draw an icon from the provided icon font.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates where the icon will be drawn.
            Default alignment is center.
        width: The width of the icon.
        code: The Unicode character or code point of the icon glyph to be drawn.
        file: The path to the font file.
        angle: The rotation angle of the icon in degrees, ranging from 0.0 to 360.0. Defaults to 0.0.
        style: The style of the icon (required).

    """
    style_obj = IconUtil.format_style(style)
    font_size = get_fontsize_from_charwidth(width)

    # convert Style to Style for text rendering
    textstyle = Style(
        text_color=style_obj.icon_color,
        text_size=font_size,
        text_font=FontFile(file),
        text_halign="center",
        text_valign="center",
    )

    # draw icon as text
    text(xy=xy, text=code, angle=angle, style=textstyle)
