# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""Canvas's original arrow feature implementation module."""

from typing import Literal, Optional, Tuple, Union

import drawlib.v0_1.private.validators.args as validator
from drawlib.v0_1.private.core.model import ShapeStyle, ShapeTextStyle
from drawlib.v0_1.private.core.theme import dtheme
from drawlib.v0_1.private.core.util import ShapeUtil
from drawlib.v0_1.private.core_canvas.base import CanvasBase
from drawlib.v0_1.private.util import (
    error_handler,
    get_angle,
    get_distance,
)


class CanvasOriginalArrowFeature(CanvasBase):
    """Canvas's original arrow feature implementation module.

    This class provides methods to draw single-headed and double-headed arrows
    on a canvas. The arrows can be customized with various styles for the tail,
    head, and optional text annotations.
    """

    def __init__(self) -> None:
        """Initialize CanvasOriginalArrowFeature.

        This initializes the CanvasOriginalArrowFeature class, inheriting from
        CanvasBase. It sets up the basic canvas features required for drawing
        original arrow shapes.
        """
        super().__init__()

    @error_handler
    def arrow(
        self,
        xy1: Tuple[float, float],
        xy2: Tuple[float, float],
        tail_width: float,
        head_width: float,
        head_length: float,
        head: Literal[
            "->",
            "<-",
            "<->",
        ] = "->",
        style: Union[ShapeStyle, str, None] = None,
        text: str = "",
        textsize: Optional[float] = None,
        textstyle: Union[ShapeTextStyle, str, None] = None,
    ) -> None:
        """Draw single and double-headed arrow.

        Args:
            xy1: Tuple[float, float]: Arrow start point.
            xy2: Tuple[float, float]: Arrow end point.
            tail_width: float: Width of the arrow tail.
            head_width: float: Width of the arrow head.
            head_length: float: Length of the arrow head.
            head: Literal["->", "<-", "<->"]: Arrow head style ("->", "<-", "<->").
            style: Union[ShapeStyle, str, None]: Optional style of the arrow.
            text: str: Optional text to display at the center of the arrow.
            textsize: Optional[float]: Optional size of the text.
            textstyle: Union[ShapeTextStyle, str, None]: Optional style of the text.

        Returns:
            None
        """
        # matplotlib FancyArrow, FancyArrowPatch seems not good
        # for implement this function.
        # Calculate arrow points pass it to shape().

        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
            dtheme.arrowstyles.get,
            dtheme.arrowtextstyles.get,
        )
        validator.validate_shape_args(locals())

        x1, y1 = xy1
        x2, y2 = xy2
        x, y = ((x1 + x2) / 2, (y1 + y2) / 2)
        angle = get_angle(xy1, xy2)
        style.halign = "center"  # no choice
        style.valign = "center"  # no choice

        # arrow_tail_external_rectangle. left-bottom -> left-top ...
        distance = get_distance(xy1, xy2)
        p11 = (0, head_width / 2 - tail_width / 2)
        p12 = (0, head_width / 2 + tail_width / 2)
        p13 = (distance, head_width / 2 + tail_width / 2)
        p14 = (distance, head_width / 2 - tail_width / 2)

        # arrow_head_rectangle. left-bottom -> left-top ...
        distance2 = distance - head_length * 2
        p21 = (head_length, 0)
        p22 = (head_length, head_width)
        p23 = (head_length + distance2, head_width)
        p24 = (head_length + distance2, 0)

        # arrow_tail_internal_rectangle. left-bottom -> left-top ...
        p31 = (head_length, head_width / 2 - tail_width / 2)
        p32 = (head_length, head_width / 2 + tail_width / 2)
        p33 = (head_length + distance2, head_width / 2 + tail_width / 2)
        p34 = (head_length + distance2, head_width / 2 - tail_width / 2)

        # start, end
        p41 = (0, head_width / 2)
        p42 = (distance, head_width / 2)

        if head == "->":
            points = [p11, p12, p33, p23, p42, p24, p34]
        elif head == "<-":
            points = [p41, p22, p32, p13, p14, p31, p21]
        elif head == "<->":
            points = [p41, p22, p32, p33, p23, p42, p24, p34, p31, p21]
        else:
            raise Exception()

        self.shape(
            xy=(x, y),
            path_points=points,
            angle=angle,
            style=style,
            text=text,
            textsize=textsize,
            textstyle=textstyle,
        )
