# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""Pyramid implementation module."""

from typing import Literal

from pydantic import BaseModel, validate_call

from drawlib._core.l2_types import Angle, Coordinate, PosFloat
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import transform, trapezoid, triangle


class PyramidItem(BaseModel):
    """Class for storing pyramid item information."""

    style: Style
    text: str
    text_style: Style
    text_angle: Angle = 0.0
    text_xy_shift: Coordinate | None = None
    show: bool = True


def _resolve_pyramid_text_style(item: PyramidItem, *, ensure_angle: bool = False) -> Style:
    """Resolve effective text style for a pyramid item at draw time."""
    text_style = item.text_style
    patch_kwargs: dict = {}
    if item.text_angle != 0.0:
        patch_kwargs["angle"] = item.text_angle
    elif ensure_angle and text_style.angle is None:
        patch_kwargs["angle"] = 0
    if item.text_xy_shift is not None:
        patch_kwargs["xy_abs_shift"] = item.text_xy_shift
    if patch_kwargs:
        text_style = text_style.patch(**patch_kwargs)
    return text_style


class Pyramid:
    """Class for rendering smart art pyramids.

    This class provides methods to create and manipulate pyramid-shaped smart art
    diagrams. It supports custom styles, text styles, text angles, and text position
    adjustments.
    """

    @validate_call
    def __init__(
        self,
        *,
        style: Style,
        text_style: Style,
        text_angle: Angle = 0.0,
        text_xy_shift: Coordinate | None = None,
    ) -> None:
        """Initializes a Pyramid instance with default styles and settings.

        Args:
            style: The default style for the pyramid shapes.
            text_style: The default text style for the pyramid shapes.
            text_angle: The default rotation angle for the text within the pyramid shapes. Defaults to 0.0.
            text_xy_shift: The default x and y shift for the text within the pyramid shapes. Defaults to None.
        """
        self._style = style
        self._text_style = text_style
        self._text_angle = text_angle
        self._text_xy_shift = text_xy_shift

        self._items: list[PyramidItem] = []

    @property
    def items(self) -> list[PyramidItem]:
        """Return the registered pyramid items."""
        return self._items

    @validate_call
    def add(
        self,
        text: str,
        *,
        style: Style | None = None,
        text_style: Style | None = None,
        text_angle: Angle | None = None,
        text_xy_shift: Coordinate | None = None,
        show: bool = True,
    ) -> PyramidItem:
        """Add an item to the pyramid.

        Args:
            text: Text to display within the pyramid shape.
            style: Style for this pyramid shape. If None, default style is used.
            text_style: Text style for this pyramid shape. If None, default text_style is used.
            text_angle: Rotation angle for the text. If None, default text_angle is used.
            text_xy_shift: Position shift for the text. If None, default text_xy_shift is used.
            show: Whether to render this pyramid layer. Defaults to True.

        Returns:
            PyramidItem: The created pyramid item instance.
        """
        resolved_style = style if style is not None else self._style
        resolved_text_style = text_style if text_style is not None else self._text_style
        resolved_text_angle = text_angle if text_angle is not None else self._text_angle
        resolved_text_xy_shift = text_xy_shift if text_xy_shift is not None else self._text_xy_shift

        item = PyramidItem(
            text=text,
            style=resolved_style,
            text_style=resolved_text_style,
            text_angle=resolved_text_angle,
            text_xy_shift=resolved_text_xy_shift,
            show=show,
        )
        self._items.append(item)
        return item

    @validate_call
    def draw(  # noqa: PLR0913
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        margin: PosFloat,
        align: Literal["bottom", "top", "left", "right"] = "bottom",
        order: Literal["vertex_to_base", "base_to_vertex"] = "vertex_to_base",
        scale: PosFloat = 1.0,
    ) -> None:
        """Draw smart art pyramid.

        Args:
            xy (Tuple[float, float]): The x and y coordinates of the bottom-left corner of the pyramid.
            width (float): The width of the pyramid.
            height (float): The height of the pyramid.
            margin (float): The margin between pyramid items.
            align (str): Alignment of a pyramid.
            order (str): Item order. "vertex -> base" or "base -> vertex". default is "vertex -> base".
            scale (float): Proportional scale factor around xy. Defaults to 1.0.
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
            scale=scale,
        )

    @validate_call
    def draw_flexible(  # noqa: PLR0913
        self,
        xy: Coordinate,
        width: PosFloat,
        item_heights: list[PosFloat],
        margins: list[PosFloat],
        align: Literal["bottom", "top", "left", "right"] = "bottom",
        order: Literal["vertex_to_base", "base_to_vertex"] = "vertex_to_base",
        scale: PosFloat = 1.0,
    ) -> None:
        """Draw smart art pyramid with flexible pyramid item heights.

        Args:
            xy (Tuple[float, float]): The x and y coordinates of the bottom-left corner of the pyramid.
            width (float): The width of the pyramid.
            item_heights (float): The height of the each pyramid items.
            margins (float): The margin between pyramid items.
            align (str): Alignment of a pyramid.
            order (str): Item order. "vertex -> base" or "base -> vertex". default is "vertex -> base".
            scale (float): Proportional scale factor around xy. Defaults to 1.0.

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

        with transform(origin=xy, scale=scale):
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
        xy: Coordinate,
        width: PosFloat,
        item_heights: list[PosFloat],
        margins: list[PosFloat],
        items: list[PyramidItem],
    ) -> None:
        x = xy[0] + width / 2
        height = sum(item_heights) + sum(margins)
        current_height = 0.0
        for i, item in enumerate(items):
            text = item.text
            style = item.style.patch(text_halign="center", text_valign="bottom")
            text_style = _resolve_pyramid_text_style(item, ensure_angle=False)

            is_last = i == len(items) - 1
            if is_last:
                if item.show:
                    ratio = (height - current_height) / height
                    item_width = ratio * width
                    item_height = item_heights[i]
                    triangle(
                        (x, xy[1] + current_height),
                        width=item_width,
                        height=item_height,
                        style=style,
                        text=text,
                        text_style=text_style,
                    )
                continue

            item_height = item_heights[i]
            if item.show:
                bottom_ratio = (height - current_height) / height
                bottom_width = bottom_ratio * width
                top_ratio = (height - current_height - item_height) / height
                top_width = top_ratio * width
                trapezoid(
                    (x, xy[1] + current_height),
                    item_height,
                    bottomedge_width=bottom_width,
                    topedge_width=top_width,
                    style=style,
                    text=text,
                    text_style=text_style,
                )
            current_height += item_height + margins[i]

    @staticmethod
    def _draw_flexible_top(
        xy: Coordinate,
        width: PosFloat,
        item_heights: list[PosFloat],
        margins: list[PosFloat],
        items: list[PyramidItem],
    ) -> None:
        x = xy[0] + width / 2
        height = sum(item_heights) + sum(margins)
        current_height = 0.0
        for i, item in enumerate(items):
            text = item.text
            style = item.style.patch(text_halign="center", text_valign="bottom")
            text_style = _resolve_pyramid_text_style(item, ensure_angle=True)

            is_last = i == len(items) - 1
            if is_last:
                if item.show:
                    ratio = (height - current_height) / height
                    item_width = ratio * width
                    item_height = item_heights[i]
                    y = xy[1] + height - current_height - item_height
                    triangle(
                        (x, y),
                        width=item_width,
                        height=item_height,
                        style=style,
                        text=text,
                        text_style=text_style,
                        angle=180,
                    )
                continue

            item_height = item_heights[i]
            if item.show:
                bottom_ratio = (height - current_height) / height
                bottom_width = bottom_ratio * width
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
                    text_style=text_style,
                )
            current_height += item_height + margins[i]

    @staticmethod
    def _draw_flexible_left(
        xy: Coordinate,
        width: PosFloat,
        item_heights: list[PosFloat],
        margins: list[PosFloat],
        items: list[PyramidItem],
    ) -> None:
        y = xy[1] + width / 2
        height = sum(item_heights) + sum(margins)
        current_height = 0.0
        for i, item in enumerate(items):
            text = item.text
            style = item.style.patch(text_halign="center", text_valign="center")
            text_style = _resolve_pyramid_text_style(item, ensure_angle=True)

            is_last = i == len(items) - 1
            if is_last:
                if item.show:
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
                        text_style=text_style,
                        angle=270,
                    )
                continue

            item_height = item_heights[i]
            if item.show:
                bottom_ratio = (height - current_height) / height
                bottom_width = bottom_ratio * width
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
                    text_style=text_style,
                    angle=270,
                )
            current_height += item_height + margins[i]

    @staticmethod
    def _draw_flexible_right(
        xy: Coordinate,
        width: PosFloat,
        item_heights: list[PosFloat],
        margins: list[PosFloat],
        items: list[PyramidItem],
    ) -> None:
        y = xy[1] + width / 2
        height = sum(item_heights) + sum(margins)
        current_height = 0.0
        for i, item in enumerate(items):
            text = item.text
            style = item.style.patch(text_halign="center", text_valign="center")
            text_style = _resolve_pyramid_text_style(item, ensure_angle=True)

            is_last = i == len(items) - 1
            if is_last:
                if item.show:
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
                        text_style=text_style,
                        angle=90,
                    )
                continue

            item_height = item_heights[i]
            if item.show:
                bottom_ratio = (height - current_height) / height
                bottom_width = bottom_ratio * width
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
                    text_style=text_style,
                    angle=90,
                )
            current_height += item_height + margins[i]
