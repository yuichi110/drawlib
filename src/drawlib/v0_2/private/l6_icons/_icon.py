# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""icon() implementation module."""

from drawlib.v0_2.private.l1_core import guarded
from drawlib.v0_2.private.l2_types import (
    TypeAngle,
    TypeCoordinate,
    TypePosFloat,
    TypeStr,
)
from drawlib.v0_2.private.l3_fonts import FontFile
from drawlib.v0_2.private.l3_styles import IconStyle, TextStyle
from drawlib.v0_2.private.l4_theme import dtheme
from drawlib.v0_2.private.l5_canvas import get_fontsize_from_charwidth, text
from drawlib.v0_2.private.l6_icons._utils import IconUtil


@guarded
def icon(
    xy: TypeCoordinate,
    width: TypePosFloat,
    code: TypeStr,
    file: TypeStr,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draw an icon from the provided icon font.

    Args:
        xy (Tuple[float, float]): The (x, y) coordinates where the icon will be drawn.
                                   Default alignment is left and bottom if angle is not specified,
                                   center if specified.
        width (float): The width of the icon. The icon might have transparent space.
        code (str): The code point of the icon to be drawn.
        file (str): The path to the font file.
        angle (Union[int, float], optional): The rotation angle of the icon,
                                             ranging from 0.0 to 360.0. Defaults to 0.0.
        style (Union[IconStyle, str, None], optional): The style of the icon, including alignment
                                                       and other properties. Defaults to None.

    Returns:
        None

    """
    style = IconUtil.format_style(style)
    font_size = get_fontsize_from_charwidth(width)

    # convert IconStyle to TextStyle
    textstyle = TextStyle(
        color=style.color,
        size=font_size,
        font=FontFile(file),
        halign=style.halign,
        valign=style.valign,
    )

    # draw icon as text
    text(xy=xy, text=code, angle=angle, style=textstyle)
