# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""BoxList implementation module."""

import dataclasses
from typing import Any, List, Literal, Optional, Tuple, Union

from drawlib.v0_2.private.core.colors import Colors
from drawlib.v0_2.private.core.model import ShapeStyle, ShapeTextStyle
from drawlib.v0_2.private.core.theme import dtheme
from drawlib.v0_2.private.core_canvas.canvas import rectangle
from drawlib.v0_2.private.util import error_handler


class BoxList:
    """A class to draw a list of boxes with text, supporting highlighting of certain boxes.

    Args:
        default_box_style (Union[str, ShapeStyle, None]): The style for the boxes.
        default_text_style (Union[str, ShapeTextStyle, None]): The style for the text inside the boxes.

    """

    @error_handler
    def __init__(
        self,
        default_box_style: Union[str, ShapeStyle, None] = None,
        default_text_style: Union[str, ShapeTextStyle, None] = None,
    ) -> None:
        """Initialize BoxList.

        Args:
            default_box_style (Union[str, ShapeStyle, None]): The style for the boxes.
            default_text_style (Union[str, ShapeTextStyle, None]): The style for the text inside the boxes.

        """
        if isinstance(default_box_style, str):
            default_box_style = dtheme.rectanglestyles.get(default_box_style)
        if default_box_style is None:
            default_box_style = dtheme.rectanglestyles.get()
        default_box_style.halign = "center"
        default_box_style.valign = "center"
        self._default_box_style = default_box_style

        if isinstance(default_text_style, str):
            default_text_style = dtheme.rectangletextstyles.get(default_text_style)
        if default_text_style is None:
            default_text_style = dtheme.rectangletextstyles.get()
        self._default_text_style = default_text_style

        self._list: List[_Item] = []

    @error_handler
    def append(
        self,
        text: str,
        box_style: Union[str, ShapeStyle, None] = None,
        text_style: Union[str, ShapeTextStyle, None] = None,
    ) -> None:
        """
        Appends a new box with text to the BoxList.

        Args:
            text (str): The text to be displayed inside the box.
            box_style (Union[str, ShapeStyle, None], optional):
                The style for the box. Can be a style name, a ShapeStyle object, or None.
                If None, the default box style is used.
            text_style (Union[str, ShapeTextStyle, None], optional):
                The style for the text inside the box. Can be a style name, a ShapeTextStyle object, or None.
                If None, the default text style is used.

        """
        self.extend([text], box_style=box_style, text_style=text_style)

    @error_handler
    def insert(
        self,
        index: int,
        text: str,
        box_style: Union[str, ShapeStyle, None] = None,
        text_style: Union[str, ShapeTextStyle, None] = None,
    ) -> None:
        """
        Inserts a new box with text at a specified position in the BoxList.

        Args:
            index (int): The position at which to insert the new box.
            text (str): The text to be displayed inside the box.
            box_style (Union[str, ShapeStyle, None], optional):
                The style for the box. Can be a style name, a ShapeStyle object, or None.
                If None, the default box style is used.
            text_style (Union[str, ShapeTextStyle, None], optional):
                The style for the text inside the box. Can be a style name, a ShapeTextStyle object, or None.
                If None, the default text style is used.

        """
        is_custom_style = box_style is not None or text_style is not None

        if isinstance(box_style, str):
            box_style = dtheme.rectanglestyles.get(box_style)
        elif box_style is None:
            box_style = self._default_box_style

        if isinstance(text_style, str):
            text_style = dtheme.rectangletextstyles.get(text_style)
        elif text_style is None:
            text_style = self._default_text_style

        item = _Item(
            text=text,
            box_style=box_style,
            text_style=text_style,
            is_custom_style=is_custom_style,
        )
        self._list.insert(index, item)

    @error_handler
    def extend(
        self,
        texts: List[str],
        box_style: Union[str, ShapeStyle, None] = None,
        text_style: Union[str, ShapeTextStyle, None] = None,
    ) -> None:
        """
        Extends the BoxList by appending multiple boxes with text.

        Args:
            texts (List[str]): A list of texts to be displayed inside the boxes.
            box_style (Union[str, ShapeStyle, None], optional):
                The style for the boxes. Can be a style name, a ShapeStyle object, or None.
                If None, the default box style is used.
            text_style (Union[str, ShapeTextStyle, None], optional):
                The style for the text inside the boxes. Can be a style name, a ShapeTextStyle object, or None.
                If None, the default text style is used.

        """
        is_custom_style = box_style is not None or text_style is not None

        if isinstance(box_style, str):
            box_style = dtheme.rectanglestyles.get(box_style)
        elif box_style is None:
            box_style = self._default_box_style

        if isinstance(text_style, str):
            text_style = dtheme.rectangletextstyles.get(text_style)
        elif text_style is None:
            text_style = self._default_text_style

        for text in texts:
            item = _Item(
                text=text,
                box_style=box_style,
                text_style=text_style,
                is_custom_style=is_custom_style,
            )
            self._list.append(item)

    @error_handler
    def draw(
        self,
        xy: Tuple[float, float],
        box_width: float,
        box_height: float,
        align: Literal["left", "right", "bottom", "top"] = "left",
    ) -> None:
        """Draws a list of boxes at the specified location.

        Args:
            xy (Tuple[float, float]): The starting point (x, y) to draw the list of boxes.
            box_width (float): The width of each box.
            box_height (float): The height of each box.
            align (Literal["left", "right", "bottom", "top"]):
                    The alignment of the boxes relative to the starting point.

        """
        for index, item in enumerate(self._list):
            if item.is_custom_style:
                continue

            self._draw_cell(
                start_xy=xy,
                index=index,
                text=item.text,
                box_width=box_width,
                box_height=box_height,
                box_style=item.box_style,
                text_style=item.text_style,
                align=align,
            )

        for index, item in enumerate(self._list):
            if not item.is_custom_style:
                continue

            self._draw_cell(
                start_xy=xy,
                index=index,
                text=item.text,
                box_width=box_width,
                box_height=box_height,
                box_style=item.box_style,
                text_style=item.text_style,
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


@dataclasses.dataclass
class _Item:
    text: str
    box_style: ShapeStyle
    text_style: ShapeTextStyle
    is_custom_style: bool
