# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Canvas's text feature implementation module."""

from typing import Optional, Tuple, Union

from matplotlib.text import Text

import drawlib.v0_2.private.validators.args as validator
from drawlib.v0_2.private.core.model import TextStyle
from drawlib.v0_2.private.core.util import TextUtil
from drawlib.v0_2.private.core_canvas.base import CanvasBase
from drawlib.v0_2.private.logging import logger
from drawlib.v0_2.private.util import error_handler


class CanvasTextFeature(CanvasBase):
    """A class for adding text features to a canvas using matplotlib."""

    def __init__(self) -> None:
        """Initializes a CanvasTextFeature object.

        Initializes an instance of CanvasTextFeature by calling the constructor
        of its superclass, CanvasBase.

        """
        super().__init__()

    @error_handler
    def text(
        self,
        xy: Tuple[float, float],
        text: str,
        size: Optional[float] = None,
        angle: Union[int, float] = 0.0,
        style: Union[TextStyle, str, None] = None,
    ) -> None:
        """Draw text on the canvas.

        Args:
            xy: Coordinates (x, y) of the text anchor point.
            text: Text string to be displayed.
            size (optional): Font size of the text.
            angle (optional): Rotation angle of the text (in degrees).
            style (optional): Style of the text.

        Returns:
            None

        """
        # validate args

        style = TextUtil.format_style(style)
        validator.validate_text_args(locals())
        if size is not None:
            style.size = size

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

    @error_handler
    def text_vertical(
        self,
        xy: Tuple[float, float],
        text: str,
        size: Optional[float] = None,
        angle: Union[int, float] = 0.0,
        style: Optional[TextStyle] = None,
    ) -> None:
        """Draw vertical text on the canvas.

        Args:
            xy: Coordinates (x, y) of the text anchor point.
            text: Text string to be displayed vertically.
            size (optional): Font size of the text.
            angle (optional): Rotation angle of the text (in degrees).
            style (optional): Style of the text.

        Returns:
            None

        """
        # validate args
        style = TextUtil.format_style(style)
        validator.validate_text_args(locals())

        if style.halign != "center":
            logger.warning("TextStyle.halign must be center on text_vertical(). Fix halign.")
            style.halign = "center"

        vertical_text = "\n".join(text)
        self.text(xy=xy, text=vertical_text, size=size, angle=angle, style=style)
