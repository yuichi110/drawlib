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

from drawlib._core.l1_core import guarded, logger
from drawlib._core.l2_types import (
    TypeAngle,
    TypeCoordinate,
    TypeSize,
    TypeStr,
)
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas._base import CanvasBase
from drawlib._core.l4_canvas_utils import TextUtil


class CanvasTextFeature(CanvasBase):
    """A class for adding text features to a canvas using matplotlib."""

    def __init__(self) -> None:
        """Initializes a CanvasTextFeature object."""
        super().__init__()

    @guarded
    def text(
        self,
        xy: TypeCoordinate,
        text: TypeStr,
        *,
        style: Style,
        size: TypeSize | None = None,
        angle: TypeAngle = 0.0,
    ) -> None:
        """Draw text on the canvas.

        Args:
            xy: Coordinates (x, y) of the text anchor point.
            text: Text string to be displayed.
            style: Style of the text (required).
            size (optional): Font size of the text override.
            angle (optional): Rotation angle of the text (in degrees).
        """
        style = TextUtil.format_style(style)
        if size is not None:
            style = style.patch(text_size=size)

        options = TextUtil.get_text_options(style)
        fp = TextUtil.get_font_properties(style)
        bx = TextUtil.get_bbox_dict(style)

        self._artists.append(
            Text(
                x=xy[0],
                y=xy[1],
                text=text,
                rotation=angle,
                rotation_mode="anchor",
                fontproperties=fp,
                bbox=bx,
                **options,
            )
        )

    @guarded
    def text_vertical(
        self,
        xy: TypeCoordinate,
        text: TypeStr,
        *,
        style: Style,
        size: TypeSize | None = None,
        angle: TypeAngle = 0.0,
    ) -> None:
        """Draw vertical text on the canvas.

        Args:
            xy: Coordinates (x, y) of the text anchor point.
            text: Text string to be displayed vertically.
            style: Style of the text (required).
            size (optional): Font size of the text override.
            angle (optional): Rotation angle of the text (in degrees).
        """
        style = TextUtil.format_style(style)

        if style.text_halign != "center":
            logger.warning("Style.halign must be center on text_vertical(). Fix halign.")
            style = style.patch(text_halign="center")

        vertical_text = "\n".join(text)
        self.text(xy=xy, text=vertical_text, size=size, angle=angle, style=style)
