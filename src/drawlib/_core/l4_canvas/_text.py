# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Canvas's text feature implementation module."""

from matplotlib.text import Text
from pydantic import validate_call

from drawlib._core.l1_core import logger
from drawlib._core.l2_types import (
    Angle,
    Coordinate,
)
from drawlib._core.l3_math import rotate_point
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas._base import CanvasBase
from drawlib._core.l4_canvas._text_util import TextUtil


class CanvasTextFeature(CanvasBase):
    """A class for adding text features to a canvas using matplotlib."""

    def __init__(self) -> None:
        """Initializes a CanvasTextFeature object."""
        super().__init__()

    @validate_call
    def text(
        self,
        xy: Coordinate,
        text: str,
        *,
        style: Style,
    ) -> None:
        """Draw text on the canvas.

        Args:
            xy: Coordinates (x, y) of the text anchor point.
            text: Text string to be displayed.
            style: Style of the text (required).
        """
        style.validate_for("text")
        angle: Angle = style.angle if style.angle is not None else 0.0

        x, y = xy
        if style.xy_shift is not None:
            x_shift, y_shift = style.xy_shift
            if angle == 0:
                x += x_shift
                y += y_shift
            else:
                rx_shift, ry_shift = rotate_point((x_shift, y_shift), angle=angle)
                x += rx_shift
                y += ry_shift

        if style.xy_abs_shift is not None:
            x += style.xy_abs_shift[0]
            y += style.xy_abs_shift[1]

        options = TextUtil.get_text_options(style)
        fp = TextUtil.get_font_properties(style)
        bx = TextUtil.get_bbox_dict(style)

        self._artists.append(
            Text(
                x=x,
                y=y,
                text=text,
                rotation=angle,
                rotation_mode="anchor",
                fontproperties=fp,
                bbox=bx,
                **options,
            )
        )

    @validate_call
    def text_vertical(
        self,
        xy: Coordinate,
        text: str,
        *,
        style: Style,
    ) -> None:
        """Draw vertical text on the canvas.

        Args:
            xy: Coordinates (x, y) of the text anchor point.
            text: Text string to be displayed vertically.
            style: Style of the text (required).
        """
        style.validate_for("text")

        if style.halign != "center":
            logger.warning("Style.halign must be center on text_vertical(). Fix halign.")
            style = style.patch(halign="center")

        vertical_text = "\n".join(text)
        self.text(xy=xy, text=vertical_text, style=style)
