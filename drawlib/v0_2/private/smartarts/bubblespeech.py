# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""bubblespeech() implementation module."""

from typing import Literal, Optional, Tuple, Union

from matplotlib.patches import Polygon

import drawlib.v0_2.private.validators.args as validator
from drawlib.v0_2.private.core.model import ShapeStyle, ShapeTextStyle
from drawlib.v0_2.private.core.theme import dtheme
from drawlib.v0_2.private.core.util import ShapeUtil
from drawlib.v0_2.private.core_canvas.canvas import canvas
from drawlib.v0_2.private.util import error_handler


@error_handler
def bubblespeech(
    xy: Tuple[float, float],
    width: float,
    height: float,
    tail_edge: Literal["left", "top", "right", "bottom"],
    tail_from_ratio: float,
    tail_vertex_xy: Tuple[float, float],
    tail_to_ratio: float,
    style: Union[ShapeStyle, str, None] = None,
    text: str = "",
    textsize: Optional[float] = None,
    textstyle: Union[ShapeTextStyle, str, None] = None,
) -> None:
    """Draw a bubble speech on the canvas.

    Args:
        xy (Tuple[float, float]): The (x, y) coordinates of the bottom-left corner of the bubble.
        width (float): The width of the bubble.
        height (float): The height of the bubble.
        tail_edge (Literal["left", "top", "right", "bottom"]): The edge on which the tail will be positioned.
        tail_from_ratio (float): The ratio along the edge where the tail starts.
        tail_vertex_xy (Tuple[float, float]): The (x, y) coordinates of the tail's vertex.
        tail_to_ratio (float): The ratio along the edge where the tail ends.
        style (Union[ShapeStyle, str, None], optional): The style of the bubble. Defaults to None.
        text (str, optional): The text to display inside the bubble. Defaults to an empty string.
        textsize (Optional[float], optional): The size of the text. Defaults to None.
        textstyle (Union[ShapeTextStyle, str, None], optional): The style of the text. Defaults to None.

    Returns:
        None

    """
    style, textstyle = ShapeUtil.format_styles(
        style,
        textstyle,
        dtheme.bubblespeechstyles.get,
        dtheme.bubblespeechtextstyles.get,
    )
    validator.validate_shape_args(locals())

    if textsize is not None:
        textstyle.size = textsize

    if tail_from_ratio > tail_to_ratio:
        raise ValueError("tail_from_ratio must be smaller than tail_to_ratio.")
    if tail_to_ratio > 1.0:
        raise ValueError("tail_from_ratio and tail_to_ratio must be smaller than 1.0")

    x, y = xy
    xys = []
    xys.append((x, y))  # left bottom
    if tail_edge == "left":
        xys.append((x, y + height * tail_from_ratio))
        xys.append(tail_vertex_xy)
        xys.append((x, y + height * tail_to_ratio))
    xys.append((x, y + height))  # left top
    if tail_edge == "top":
        xys.append((x + width * tail_from_ratio, y + height))
        xys.append(tail_vertex_xy)
        xys.append((x + width * tail_to_ratio, y + height))
    xys.append((x + width, y + height))  # right top
    if tail_edge == "right":
        xys.append((x + width, y + height * tail_to_ratio))
        xys.append(tail_vertex_xy)
        xys.append((x + width, y + height * tail_from_ratio))
    xys.append((x + width, y))  # right bottom
    if tail_edge == "bottom":
        xys.append((x + width * tail_to_ratio, y))
        xys.append(tail_vertex_xy)
        xys.append((x + width * tail_from_ratio, y))

    options = ShapeUtil.get_shape_options(style)
    canvas._artists.append(Polygon(xy=xys, closed=True, **options))

    if text:
        center_x = x + width / 2
        center_y = y + height / 2
        canvas._artists.append(
            ShapeUtil.get_shape_text(
                xy=(center_x, center_y),
                text=text,
                angle=0,
                style=textstyle,
            )
        )
