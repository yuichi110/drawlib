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
from typing import List, Literal, Optional, Tuple, Union

from drawlib.v0_2.private.core.model import ShapeStyle, ShapeTextStyle
from drawlib.v0_2.private.core.theme import dtheme
from drawlib.v0_2.private.core_canvas.canvas import trapezoid, triangle
from drawlib.v0_2.private.util import error_handler


@dataclasses.dataclass
class _PyramidItem:
    style: ShapeStyle
    text: str
    textstyle: ShapeTextStyle


class Pyramid:
    """Class for rendering smart art pyramids.

    This class provides methods to create and manipulate pyramid-shaped smart art
    diagrams. It supports custom styles, text styles, text angles, and text position
    adjustments.
    """

    @error_handler
    def __init__(
        self,
        default_style: Union[str, ShapeStyle, None] = None,
        default_textstyle: Union[str, ShapeTextStyle, None] = None,
        default_textangle: Optional[float] = None,
        default_text_xy_shift: Optional[Tuple[float, float]] = None,
    ) -> None:
        """Initializes a Pyramid instance with optional default styles and settings.

        Args:
            default_style (Union[str, ShapeStyle, None], optional): The default
                style for the pyramid shapes. It can be a string that maps to a
                `ShapeStyle` or a `ShapeStyle` instance. Defaults to None.
            default_textstyle (Union[str, ShapeTextStyle, None], optional): The
                default text style for the pyramid shapes. It can be a string that
                maps to a `ShapeTextStyle` or a `ShapeTextStyle` instance. Defaults to None.
            default_textangle (Optional[float], optional): The default rotation
                angle for the text within the pyramid shapes. Defaults to None.
            default_text_xy_shift (Optional[Tuple[float, float]], optional): The
                default x and y shift for the text within the pyramid shapes.
                Defaults to None.
        """
        if isinstance(default_style, str):
            default_style = dtheme.rectanglestyles.get(default_style)
        self._default_style = default_style
        if isinstance(default_textstyle, str):
            default_textstyle = dtheme.rectangletextstyles.get(default_textstyle)
        self._default_textstyle = default_textstyle
        self._default_textangle = default_textangle
        self._default_text_xy_shift = default_text_xy_shift

        self._items: List[_PyramidItem] = []

    @error_handler
    def add(  # noqa: C901
        self,
        text: str,
        style: Union[str, ShapeStyle, None] = None,
        textstyle: Union[str, ShapeTextStyle, None] = None,
        textangle: Optional[float] = None,
        text_xy_shift: Optional[Tuple[float, float]] = None,
    ) -> None:
        """
        Add an item to the pyramid.

        Args:
            text (str): The text associated with the item.
            style (Union[str, ShapeStyle, None], optional):
                    The style of the item.
                    Can be a string key for a predefined style, a ShapeStyle object,
                    or None to use the default style.
            textstyle (Union[str, ShapeTextStyle, None], optional):
                    The text style of the item. Can be a string key for a predefined text style,
                    a ShapeTextStyle object, or None to use the default text style.
            textangle (Optional[float], optional):
                    The angle of the text. Default is None, which is same to 0.
            text_xy_shift (Optional[Tuple[float, float]], optional):
                    The XY shift of the text. Default is None, which is same to (0, 0).
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

        # apply align to shape style
        if style is None:
            style = dtheme.rectanglestyles.get()
        else:
            style = style.copy()

        # apply angle and shift to shape text style
        if textstyle is None:
            textstyle = dtheme.shapetextstyles.get()
        else:
            textstyle = textstyle.copy()
        if textangle is None:
            textangle = self._default_textangle
        if textangle is not None:
            textstyle.angle = textangle
        if text_xy_shift is None:
            text_xy_shift = self._default_text_xy_shift
        if text_xy_shift is not None:
            textstyle.xy_abs_shift = text_xy_shift

        # push
        item = _PyramidItem(
            text=text,
            style=style,
            textstyle=textstyle,
        )
        self._items.append(item)

    @error_handler
    def draw(
        self,
        xy: Tuple[float, float],
        width: float,
        height: float,
        margin: float,
        align: Literal["bottom", "top", "left", "right"] = "bottom",
        order: Literal["vertex_to_base", "base_to_vertex"] = "vertex_to_base",
    ) -> None:
        """Draw smart art pyramid.

        Args:
            xy (Tuple[float, float]): The x and y coordinates of the bottom-left corner of the pyramid.
            width (float): The width of the pyramid.
            height (float): The heifht of the pyramid.
            margin (float): The margin between pyramid items.
            align (str): Alignment of a pyramid.
            order (str): Item order. "vertex -> base" or "base -> vertex". default is "vertex -> base".
        """
        if len(self._items) == 0:
            raise ValueError("Number of pyramid item is 0.")

        margins = [margin] * (len(self._items) - 1)
        item_height = (height - sum(margins)) / len(self._items)
        item_heights = [item_height] * len(self._items)

        self.draw_flexible(
            xy=xy,
            width=width,
            item_heights=item_heights,
            margins=margins,
            align=align,
            order=order,
        )

    @error_handler
    def draw_flexible(
        self,
        xy: Tuple[float, float],
        width: float,
        item_heights: List[float],
        margins: List[float],
        align: Literal["bottom", "top", "left", "right"] = "bottom",
        order: Literal["vertex_to_base", "base_to_vertex"] = "vertex_to_base",
    ) -> None:
        """Draw smart art pyramid with flexible pyramid item heights.

        Args:
            xy (Tuple[float, float]): The x and y coordinates of the bottom-left corner of the pyramid.
            width (float): The width of the pyramid.
            item_heights (float): The height of the each pyramid items.
            margins (float): The margin between pyramid items.
            align (str): Alignment of a pyramid.
            order (str): Item order. "vertex -> base" or "base -> vertex". default is "vertex -> base".

        Raises:
            ValueError: If the lengths of column_widths, column_margins, row_heights, or row_margins are incorrect.
        """
        # validate
        if len(self._items) == 0:
            raise ValueError("Number of pyramid item is 0.")

        if len(self._items) != len(item_heights):
            raise ValueError('Number of pyramid item and arg "items_heights" length are different.')

        if len(self._items) != len(margins) + 1:
            raise ValueError('Number of pyramid item and arg "margins" length does not match.')

        items = self._items[::-1] if order == "vertex_to_base" else self._items[::]

        if align == "bottom":
            self._draw_flexible_bottom(xy, width, item_heights, margins, items)
        elif align == "top":
            self._draw_flexible_top(xy, width, item_heights, margins, items)
        elif align == "left":
            self._draw_flexible_left(xy, width, item_heights, margins, items)
        elif align == "right":
            self._draw_flexible_right(xy, width, item_heights, margins, items)
        else:
            raise ValueError("Drawlib internal error.")

    @staticmethod
    def _draw_flexible_bottom(
        xy: Tuple[float, float],
        width: float,
        item_heights: List[float],
        margins: List[float],
        items: List[_PyramidItem],
    ) -> None:
        x = xy[0] + width / 2
        height = sum(item_heights) + sum(margins)
        current_height = 0
        for i, item in enumerate(items):
            text = item.text
            style = item.style
            style.halign = "center"
            style.valign = "bottom"
            textstyle = item.textstyle

            is_last = i == len(items) - 1
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

    @staticmethod
    def _draw_flexible_top(
        xy: Tuple[float, float],
        width: float,
        item_heights: List[float],
        margins: List[float],
        items: List[_PyramidItem],
    ) -> None:
        x = xy[0] + width / 2
        height = sum(item_heights) + sum(margins)
        current_height = 0
        for i, item in enumerate(items):
            text = item.text
            style = item.style
            style.halign = "center"
            style.valign = "bottom"
            textstyle = item.textstyle

            is_last = i == len(items) - 1
            if is_last:
                ratio = (height - current_height) / height
                item_width = ratio * width
                item_height = item_heights[i]
                y = xy[1] + height - current_height - item_height
                if textstyle.angle is None:
                    textstyle.angle = 0
                triangle(
                    (x, y),
                    width=item_width,
                    height=item_height,
                    style=style,
                    text=text,
                    textstyle=textstyle,
                    angle=180,
                )
                continue

            bottom_ratio = (height - current_height) / height
            bottom_width = bottom_ratio * width
            item_height = item_heights[i]
            top_ratio = (height - current_height - item_height) / height
            top_width = top_ratio * width
            y = xy[1] + height - current_height - item_height
            trapezoid(
                (x, y),
                item_height,
                bottomedge_width=top_width,
                topedge_width=bottom_width,
                style=style,
                text=text,
                textstyle=textstyle,
            )
            current_height += item_height + margins[i]

    @staticmethod
    def _draw_flexible_left(
        xy: Tuple[float, float],
        width: float,
        item_heights: List[float],
        margins: List[float],
        items: List[_PyramidItem],
    ) -> None:
        y = xy[1] + width / 2
        height = sum(item_heights) + sum(margins)
        current_height = 0
        for i, item in enumerate(items):
            text = item.text
            style = item.style
            style.halign = "center"
            style.valign = "center"
            textstyle = item.textstyle

            if textstyle.angle is None:
                textstyle.angle = 0

            is_last = i == len(items) - 1
            if is_last:
                ratio = (height - current_height) / height
                item_width = ratio * width
                item_height = item_heights[i]
                x = xy[0] + current_height + item_height / 2
                triangle(
                    (x, y),
                    width=item_width,
                    height=item_height,
                    style=style,
                    text=text,
                    textstyle=textstyle,
                    angle=270,
                )
                continue

            bottom_ratio = (height - current_height) / height
            bottom_width = bottom_ratio * width
            item_height = item_heights[i]
            top_ratio = (height - current_height - item_height) / height
            top_width = top_ratio * width
            x = xy[0] + current_height + item_height / 2
            trapezoid(
                (x, y),
                item_height,
                bottomedge_width=bottom_width,
                topedge_width=top_width,
                style=style,
                text=text,
                textstyle=textstyle,
                angle=270,
            )
            current_height += item_height + margins[i]

    @staticmethod
    def _draw_flexible_right(
        xy: Tuple[float, float],
        width: float,
        item_heights: List[float],
        margins: List[float],
        items: List[_PyramidItem],
    ) -> None:
        y = xy[1] + width / 2
        height = sum(item_heights) + sum(margins)
        current_height = 0
        for i, item in enumerate(items):
            text = item.text
            style = item.style
            style.halign = "center"
            style.valign = "center"
            textstyle = item.textstyle
            if textstyle.angle is None:
                textstyle.angle = 0

            is_last = i == len(items) - 1
            if is_last:
                ratio = (height - current_height) / height
                item_width = ratio * width
                item_height = item_heights[i]
                x = xy[0] + height - current_height - item_height / 2
                triangle(
                    (x, y),
                    width=item_width,
                    height=item_height,
                    style=style,
                    text=text,
                    textstyle=textstyle,
                    angle=90,
                )
                continue

            bottom_ratio = (height - current_height) / height
            bottom_width = bottom_ratio * width
            item_height = item_heights[i]
            top_ratio = (height - current_height - item_height) / height
            top_width = top_ratio * width
            x = xy[0] + height - current_height - item_height / 2
            trapezoid(
                (x, y),
                item_height,
                bottomedge_width=bottom_width,
                topedge_width=top_width,
                style=style,
                text=text,
                textstyle=textstyle,
                angle=90,
            )
            current_height += item_height + margins[i]
