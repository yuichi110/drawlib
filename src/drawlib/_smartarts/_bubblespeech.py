# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""bubblespeech() implementation module."""

from typing import Literal

from matplotlib.patches import Polygon
from pydantic import validate_call

from drawlib._core.canvas import canvas
from drawlib._core.types import Style, TypeAlpha, TypeCoordinate, TypePosFloat, TypeSize, TypeStr
from drawlib._core.utils import ShapeUtil, TextUtil


@validate_call
def bubblespeech(
    xy: TypeCoordinate,
    width: TypePosFloat,
    height: TypePosFloat,
    tail_edge: Literal["left", "top", "right", "bottom"],
    tail_start_ratio: TypeAlpha,
    tail_vertex_xy: TypeCoordinate,
    tail_end_ratio: TypeAlpha,
    *,
    style: Style,
    text: TypeStr = "",
    textsize: TypeSize | None = None,
    textstyle: Style | None = None,
) -> None:
    """Draw a bubble speech on the canvas.

    Args:
        xy: The (x, y) coordinates of the bottom-left corner of the bubble.
        width: The width of the bubble.
        height: The height of the bubble.
        tail_edge: The edge on which the tail will be positioned.
        tail_start_ratio: The ratio along the edge where the tail starts.
        tail_vertex_xy: The (x, y) coordinates of the tail's vertex.
        tail_end_ratio: The ratio along the edge where the tail ends.
        style: The style of the bubble (required).
        text: The text to display inside the bubble. Defaults to an empty string.
        textsize: The size of the text. Defaults to None.
        textstyle: The style of the text. Defaults to None.

    Returns:
        None

    """
    style, textstyle = ShapeUtil.format_styles(
        style,
        textstyle,
    )

    if tail_start_ratio > tail_end_ratio:
        raise ValueError("tail_start_ratio must be smaller than tail_end_ratio.")
    if tail_end_ratio > 1.0:
        raise ValueError("tail_start_ratio and tail_end_ratio must be smaller than 1.0")

    x, y = xy
    xys = []
    xys.append((x, y))  # left bottom
    if tail_edge == "left":
        xys.append((x, y + height * tail_start_ratio))
        xys.append(tail_vertex_xy)
        xys.append((x, y + height * tail_end_ratio))
    xys.append((x, y + height))  # left top
    if tail_edge == "top":
        xys.append((x + width * tail_start_ratio, y + height))
        xys.append(tail_vertex_xy)
        xys.append((x + width * tail_end_ratio, y + height))
    xys.append((x + width, y + height))  # right top
    if tail_edge == "right":
        xys.append((x + width, y + height * tail_end_ratio))
        xys.append(tail_vertex_xy)
        xys.append((x + width, y + height * tail_start_ratio))
    xys.append((x + width, y))  # right bottom
    if tail_edge == "bottom":
        xys.append((x + width * tail_end_ratio, y))
        xys.append(tail_vertex_xy)
        xys.append((x + width * tail_start_ratio, y))

    options = ShapeUtil.get_shape_options(style)
    canvas._artists.append(Polygon(xy=xys, closed=True, **options))

    if text:
        effective_textstyle = textstyle if textstyle is not None else style
        if textsize is not None:
            effective_textstyle = effective_textstyle.patch(text_size=textsize)
        TextUtil.validate_text_style(effective_textstyle)
        center_x = x + width / 2
        center_y = y + height / 2
        canvas._artists.append(
            ShapeUtil.get_shape_text(
                xy=(center_x, center_y),
                text=text,
                angle=0,
                style=effective_textstyle,
            )
        )
