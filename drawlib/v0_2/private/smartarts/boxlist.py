# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""BoxList implementation module."""

from typing import Any, List, Literal, Optional, Tuple, Union

from drawlib.v0_2.private.core.colors import Colors
from drawlib.v0_2.private.core.model import ShapeStyle, ShapeTextStyle
from drawlib.v0_2.private.core.theme import dtheme
from drawlib.v0_2.private.core_canvas.canvas import rectangle
from drawlib.v0_2.private.util import error_handler


class BoxList:
    """A class to draw a list of boxes with text, supporting highlighting of certain boxes.

    Args:
        box_style (Union[str, ShapeStyle, None]): The style for the boxes.
        text_style (Union[str, ShapeTextStyle, None]): The style for the text inside the boxes.
        box_highlight_style (Union[str, ShapeStyle, None]): The style for the highlighted boxes.
        text_highlight_style (Union[str, ShapeTextStyle, None]): The style for the text inside the highlighted boxes.
    """

    @error_handler
    def __init__(
        self,
        box_style: Union[str, ShapeStyle, None] = None,
        text_style: Union[str, ShapeTextStyle, None] = None,
        box_highlight_style: Union[str, ShapeStyle, None] = None,
        text_highlight_style: Union[str, ShapeTextStyle, None] = None,
    ) -> None:
        """Initialize BoxList.

        Args:
            box_style (Union[str, ShapeStyle, None]): The style for the boxes.
            text_style (Union[str, ShapeTextStyle, None]): The style for the text inside the boxes.
            box_highlight_style (Union[str, ShapeStyle, None]): The style for the highlighted boxes.
            text_highlight_style (Union[str, ShapeTextStyle, None]):
                    The style for the text inside the highlighted boxes.
        """
        if isinstance(box_style, str):
            box_style = dtheme.rectanglestyles.get(box_style)
        if box_style is None:
            box_style = dtheme.rectanglestyles.get()
        box_style.halign = "center"
        box_style.valign = "center"
        self._box_style = box_style

        if isinstance(text_style, str):
            text_style = dtheme.rectangletextstyles.get(text_style)
        if text_style is None:
            text_style = dtheme.rectangletextstyles.get()
        self._text_style = text_style

        if isinstance(box_highlight_style, str):
            box_highlight_style = dtheme.rectanglestyles.get(box_highlight_style)
        if box_highlight_style is None:
            box_highlight_style = box_style
        box_highlight_style.halign = "center"
        box_highlight_style.valign = "center"
        self._box_highlight_style = box_highlight_style

        if isinstance(text_highlight_style, str):
            text_highlight_style = dtheme.rectangletextstyles.get(text_highlight_style)
        if text_highlight_style is None:
            text_highlight_style = text_style
        self._text_highlight_style = text_highlight_style

    @error_handler
    def draw(
        self,
        xy: Tuple[float, float],
        box_width: float,
        box_height: float,
        items: List[Any],
        highlight_indexs: Optional[List[int]] = None,
        length: Optional[int] = None,
        align: Literal["left", "right", "bottom", "top"] = "left",
    ) -> None:
        """Draws a list of boxes at the specified location.

        Args:
            xy (Tuple[float, float]): The starting point (x, y) to draw the list of boxes.
            box_width (float): The width of each box.
            box_height (float): The height of each box.
            items (List[Any]): The list of items to be displayed inside the boxes.
            highlight_indexs (Optional[List[int]]):
                    The list of indices of the boxes to be highlighted.
            length (Optional[int]): The total number of boxes to be drawn.
            align (Literal["left", "right", "bottom", "top"]):
                    The alignment of the boxes relative to the starting point.

        """
        if highlight_indexs is None:
            highlight_indexs = []

        if length is not None:
            indexs = range(length)
        else:
            indexs = range(len(items))

        non_highlight_indexs = [item for item in indexs if item not in highlight_indexs]
        highlight_indexs = [item for item in indexs if item in highlight_indexs]

        for index in non_highlight_indexs:
            if index <= len(items) - 1:
                text = str(items[index])
            else:
                text = ""

            self._draw_cell(
                start_xy=xy,
                index=index,
                text=text,
                box_width=box_width,
                box_height=box_height,
                box_style=self._box_style,
                text_style=self._text_style,
                align=align,
            )

        for index in highlight_indexs:
            if index <= len(items) - 1:
                text = str(items[index])
            else:
                text = ""

            self._draw_cell(
                start_xy=xy,
                index=index,
                text=text,
                box_width=box_width,
                box_height=box_height,
                box_style=self._box_highlight_style,
                text_style=self._text_highlight_style,
                align=align,
            )

    @staticmethod
    def _draw_cell(
        start_xy: Tuple[float, float],
        index: int,
        text: str,
        box_width: float,
        box_height: float,
        box_style: ShapeStyle,
        text_style: ShapeTextStyle,
        align: Literal["left", "right", "bottom", "top"],
    ) -> None:
        if align == "left":
            x = start_xy[0] + box_width * (index + 0.5)
            y = start_xy[1] + box_height / 2
        elif align == "right":
            x = start_xy[0] - box_width * (index + 0.5)
            y = start_xy[1] + box_height / 2
        elif align == "bottom":
            x = start_xy[0] + box_width / 2
            y = start_xy[1] + box_height * (index + 0.5)
        else:
            x = start_xy[0] + box_width / 2
            y = start_xy[1] - box_height * (index + 0.5)

        rectangle(
            xy=(x, y),
            width=box_width,
            height=box_height,
            style=box_style,
            text=text,
            textstyle=text_style,
        )
