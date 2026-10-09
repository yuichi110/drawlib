# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""font_icon() implementation module."""

from pydantic import validate_call

from drawlib._core.l2_types import Coordinate, PosFloat
from drawlib._core.l3_fonts import FontFile
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import get_fontsize_from_charwidth, text
from drawlib._icons._utils import IconUtil


@validate_call
def font_icon(
    xy: Coordinate,
    width: PosFloat,
    code: str,
    file: str,
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
        style: The style of the icon (required).

    """
    style_obj = IconUtil.format_style(style)
    font_size = get_fontsize_from_charwidth(width)

    # convert Style to Style for text rendering
    text_style = Style(
        text_color=style_obj.icon_color,
        text_size=font_size,
        text_font=FontFile(file),
        halign=style_obj.halign if style_obj.halign is not None else "center",
        valign=style_obj.valign if style_obj.valign is not None else "center",
        xy_shift=style_obj.xy_shift,
        xy_abs_shift=style_obj.xy_abs_shift,
        angle=style_obj.angle,
        alpha=style_obj.alpha,
    )

    # draw icon as text
    text(xy=xy, text=code, style=text_style)
