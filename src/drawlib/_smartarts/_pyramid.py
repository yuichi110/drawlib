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

from drawlib._core.shapes import trapezoid, triangle
from drawlib._core.types import Style, TypeAngle, TypeCoordinate, TypePosFloat, TypeStr
from drawlib._preset_styles import BasePresetStyles


class _PyramidItem(BaseModel):
    """Internal class for storing pyramid item information."""

    style: Style
    text: TypeStr
    textstyle: Style


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
        styles: BasePresetStyles,
        default_style: Style | None = None,
        default_textstyle: Style | None = None,
        default_textangle: TypeAngle | None = None,
        default_text_xy_shift: TypeCoordinate | None = None,
    ) -> None:
        """Initializes a Pyramid instance with optional default styles and settings.

        Args:
            styles: The preset styles catalog (required).
            default_style: The default style for the pyramid shapes. Defaults to None.
            default_textstyle: The default text style for the pyramid shapes. Defaults to None.
            default_textangle: The default rotation angle for the text within the pyramid shapes. Defaults to None.
            default_text_xy_shift: The default x and y shift for the text within the pyramid shapes. Defaults to None.
        """
        self._styles = styles
        self._default_style = default_style if default_style is not None else styles.primary
        self._default_textstyle = default_textstyle if default_textstyle is not None else styles.bold
        self._default_textangle = default_textangle
        self._default_text_xy_shift = default_text_xy_shift

        self._items: list[_PyramidItem] = []

    @validate_call
    def add(  # noqa: C901
        self,
        text: TypeStr,
        style: Style | None = None,
        textstyle: Style | None = None,
        textangle: TypeAngle | None = None,
        text_xy_shift: TypeCoordinate | None = None,
    ) -> None:
        resolved_style = style if style is not None else self._default_style
        resolved_textstyle = textstyle if textstyle is not None else self._default_textstyle

        if textangle is None:
            textangle = self._default_textangle
        if text_xy_shift is None:
            text_xy_shift = self._default_text_xy_shift

        patch_kwargs: dict = {}
        if textangle is not None:
            patch_kwargs["text_angle"] = textangle
        if text_xy_shift is not None:
            patch_kwargs["text_xy_abs_shift"] = text_xy_shift
        if patch_kwargs:
            resolved_textstyle = resolved_textstyle.patch(**patch_kwargs)

        item = _PyramidItem(
            text=text,
            style=resolved_style,
            textstyle=resolved_textstyle,
        )
        self._items.append(item)

    @validate_call
    def draw(
        self,
        xy: TypeCoordinate,
        width: TypePosFloat,
        height: TypePosFloat,
        margin: TypePosFloat,
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

    @validate_call
    def draw_flexible(
        self,
        xy: TypeCoordinate,
        width: TypePosFloat,
        item_heights: list[TypePosFloat],
        margins: list[TypePosFloat],
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
        xy: TypeCoordinate,
        width: TypePosFloat,
        item_heights: list[TypePosFloat],
        margins: list[TypePosFloat],
        items: list[_PyramidItem],
    ) -> None:
        x = xy[0] + width / 2
        height = sum(item_heights) + sum(margins)
        current_height = 0
        for i, item in enumerate(items):
            text = item.text
            style = item.style.patch(text_halign="center", text_valign="bottom")
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
        xy: TypeCoordinate,
        width: TypePosFloat,
        item_heights: list[TypePosFloat],
        margins: list[TypePosFloat],
        items: list[_PyramidItem],
    ) -> None:
        x = xy[0] + width / 2
        height = sum(item_heights) + sum(margins)
        current_height = 0
        for i, item in enumerate(items):
            text = item.text
            style = item.style.patch(text_halign="center", text_valign="bottom")
            textstyle = item.textstyle.patch(
                text_angle=item.textstyle.text_angle if item.textstyle.text_angle is not None else 0,
            )

            is_last = i == len(items) - 1
            if is_last:
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
        xy: TypeCoordinate,
        width: TypePosFloat,
        item_heights: list[TypePosFloat],
        margins: list[TypePosFloat],
        items: list[_PyramidItem],
    ) -> None:
        y = xy[1] + width / 2
        height = sum(item_heights) + sum(margins)
        current_height = 0
        for i, item in enumerate(items):
            text = item.text
            style = item.style.patch(text_halign="center", text_valign="center")
            textstyle = item.textstyle.patch(
                text_angle=item.textstyle.text_angle if item.textstyle.text_angle is not None else 0,
            )

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
        xy: TypeCoordinate,
        width: TypePosFloat,
        item_heights: list[TypePosFloat],
        margins: list[TypePosFloat],
        items: list[_PyramidItem],
    ) -> None:
        y = xy[1] + width / 2
        height = sum(item_heights) + sum(margins)
        current_height = 0
        for i, item in enumerate(items):
            text = item.text
            style = item.style.patch(text_halign="center", text_valign="center")
            textstyle = item.textstyle.patch(
                text_angle=item.textstyle.text_angle if item.textstyle.text_angle is not None else 0,
            )

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
