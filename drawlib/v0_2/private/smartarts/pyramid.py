# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""Pyramid implementation module."""

import dataclasses
from typing import List, Optional, Tuple, Union

from drawlib.v0_2.private.core.model import ShapeStyle, ShapeTextStyle
from drawlib.v0_2.private.core.theme import dtheme
from drawlib.v0_2.private.core_canvas.canvas import trapezoid, triangle


class Pyramid:
    """Class for rendering smart art pyramid."""

    def __init__(
        self,
        default_style: Union[str, ShapeStyle, None] = None,
        default_textstyle: Union[str, ShapeTextStyle, None] = None,
    ) -> None:
        """Initialize class."""
        if isinstance(default_style, str):
            default_style = dtheme.rectanglestyles.get(default_style)
        self._default_style = default_style
        if isinstance(default_textstyle, str):
            default_textstyle = dtheme.rectangletextstyles.get(default_textstyle)
        self._default_textstyle = default_textstyle

        self._items: List[_PyramidItem] = []

    def add(  # noqa: C901
        self,
        style: Union[str, ShapeStyle, None] = None,
        text: str = "",
        textstyle: Union[str, ShapeTextStyle, None] = None,
    ) -> None:
        """
        Add an item to the pyramid.

        Args:
            style (Union[str, ShapeStyle, None], optional):
                    The style of the item.
                    Can be a string key for a predefined style, a ShapeStyle object,
                    or None to use the default style.
            text (str, optional): The text associated with the item. Default is an empty string.
            textstyle (Union[str, ShapeTextStyle, None], optional):
                    The text style of the item. Can be a string key for a predefined text style,
                    a ShapeTextStyle object, or None to use the default text style.
        """
        # string style to Style class
        if isinstance(style, str):
            style = dtheme.rectanglestyles.get(style)
        if isinstance(textstyle, str):
            textstyle = dtheme.rectangletextstyles.get(textstyle)

        # apply default if args are None
        if style is None:
            style = self._default_style
        if textstyle is None:
            textstyle = self._default_textstyle

        # push
        item = _PyramidItem(
            text=text,
            style=style,
            textstyle=textstyle,
        )
        self._items.append(item)

    def draw(
        self,
        xy: Tuple[float, float],
        width: float,
        height: float,
        margin: float,
    ) -> None:
        """Draw smart art pyramid.

        Args:
            xy (Tuple[float, float]): The x and y coordinates of the bottom-left corner of the pyramid.
            width (float): The width of the pyramid.
            height (float): The heifht of the pyramid.
            margin (float): The margin between pyramid items.
        """
        if len(self._items) == 0:
            raise ValueError()

        margins = [margin] * (len(self._items) - 1)
        item_height = (height - sum(margins)) / len(self._items)
        item_heights = [item_height] * len(self._items)

        self.draw_flexible(
            xy=xy,
            width=width,
            item_heights=item_heights,
            margins=margins,
        )

    def draw_flexible(  # noqa: C901
        self,
        xy: Tuple[float, float],
        width: float,
        item_heights: List[float],
        margins: List[float],
    ) -> None:
        """Draw smart art pyramid with flexible pyramid item heights.

        Args:
            xy (Tuple[float, float]): The x and y coordinates of the bottom-left corner of the pyramid.
            width (float): The width of the pyramid.
            item_heights (float): The height of the each pyramid items.
            margins (float): The margin between pyramid items.

        Raises:
            ValueError: If the lengths of column_widths, column_margins, row_heights, or row_margins are incorrect.
        """
        # validate
        if len(self._items) == 0:
            raise ValueError()

        if len(self._items) != len(item_heights):
            raise ValueError()

        if len(self._items) != len(margins) + 1:
            raise ValueError()

        x = xy[0] + width / 2
        height = sum(item_heights) + sum(margins)
        current_height = 0
        for i, item in enumerate(self._items):
            text = item.text
            textstyle = item.textstyle
            if textstyle is None:
                textstyle = self._default_textstyle
            style = item.style
            if style is None:
                style = self._default_style
            if style is None:
                style = dtheme.rectanglestyles.get()
            else:
                style = style.copy()
            style.halign = "center"
            style.valign = "bottom"

            is_last = i == len(self._items) - 1
            if is_last:
                ratio = (height - current_height) / height
                item_width = ratio * width
                item_height = item_heights[i]
                triangle(
                    (x, xy[1] + current_height),
                    width=item_width,
                    height=item_height,
                    style=style,
                    text=text,
                    textstyle=textstyle,
                )
                continue

            bottom_ratio = (height - current_height) / height
            bottom_width = bottom_ratio * width
            item_height = item_heights[i]
            top_ratio = (height - current_height - item_height) / height
            top_width = top_ratio * width
            trapezoid(
                (x, xy[1] + current_height),
                item_height,
                bottomedge_width=bottom_width,
                topedge_width=top_width,
                style=style,
                text=text,
                textstyle=textstyle,
            )
            current_height += item_height + margins[i]


@dataclasses.dataclass
class _PyramidItem:
    style: Optional[ShapeStyle]
    text: str
    textstyle: Optional[ShapeTextStyle]
