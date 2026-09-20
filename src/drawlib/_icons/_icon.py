# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""icon() implementation module."""

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
from drawlib._theme import get_style


@guarded
def icon(
    xy: TypeCoordinate,
    width: TypePosFloat,
    code: TypeStr,
    file: TypeStr,
    angle: TypeAngle = 0.0,
    style: Style | TypeStr | None = None,
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
        style (Union[Style, str, None], optional): The style of the icon, including alignment
                                                       and other properties. Defaults to None.

    Returns:
        None

    """
    style = IconUtil.format_style(style)
    font_size = get_fontsize_from_charwidth(width)

    # convert Style to Style
    textstyle = Style(
        text_color=style.text_color,
        text_size=font_size,
        text_font=FontFile(file),
        text_halign=style.text_halign,
        text_valign=style.text_valign,
    )

    # draw icon as text
    text(xy=xy, text=code, angle=angle, style=textstyle)
