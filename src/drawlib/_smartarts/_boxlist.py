# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""BoxList implementation module."""

from __future__ import annotations

from typing import Literal, Self

from pydantic import BaseModel

from drawlib._core.l1_core import validate_call
from drawlib._core.l2_types import Coordinate, PosFloat
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import rectangle, transform


class BoxListItem(BaseModel):
    """Item class for BoxList."""

    text: str
    style: Style
    text_style: Style
    show: bool = True


class BoxList:
    """A class to draw a list of boxes with text, supporting highlighting of certain boxes."""

    @validate_call
    def __init__(
        self,
        *,
        style: Style,
        text_style: Style,
    ) -> None:
        """Initialize BoxList.

        Args:
            style: The default style for the boxes.
            text_style: The default style for the text inside the boxes.
        """
        self._style = style
        self._text_style = text_style
        self._list: list[BoxListItem] = []

    @property
    def items(self) -> list[BoxListItem]:
        """Return the registered box list items."""
        return self._list

    @validate_call
    def add(
        self,
        text: str,
        *,
        style: Style | None = None,
        text_style: Style | None = None,
        show: bool = True,
    ) -> BoxListItem:
        """Add a box item to the list.

        Args:
            text: Text to display in the box.
            style: Style for the box. If None, default style is used.
            text_style: Style for the text inside the box. If None, default text_style is used.
            show: Whether to render this box item. Defaults to True.

        Returns:
            BoxListItem: The created box item instance.
        """
        resolved_style = style if style is not None else self._style
        resolved_text_style = text_style if text_style is not None else self._text_style

        item = BoxListItem(
            text=text,
            style=resolved_style,
            text_style=resolved_text_style,
            show=show,
        )
        self._list.append(item)
        return item

    @validate_call
    def draw(
        self,
        xy: Coordinate,
        box_width: PosFloat,
        box_height: PosFloat,
        direction: Literal["left", "right", "bottom", "top"] = "left",
        align: Literal["bottom_left", "center"] = "bottom_left",
        scale: PosFloat = 1.0,
    ) -> Self:
        """Draw a list of boxes at the specified location.

        Args:
            xy: Anchor coordinate (x, y) of the box list bounding box (interpreted via align).
            box_width: The width of each box.
            box_height: The height of each box.
            direction: Layout flow direction ("left", "right", "bottom", or "top"). Defaults to "left".
            align: Anchor alignment of xy ("bottom_left" or "center"). Defaults to "bottom_left".
            scale: Proportional scale factor around xy. Defaults to 1.0.

        Returns:
            Self: This BoxList instance for method chaining.
        """
        num_items = len(self._list)
        if num_items == 0:
            return self

        if direction in ("left", "right"):
            total_w = num_items * float(box_width)
            total_h = float(box_height)
        else:
            total_w = float(box_width)
            total_h = num_items * float(box_height)

        if align == "center":
            start_xy: Coordinate = (float(xy[0]) - total_w / 2.0, float(xy[1]) - total_h / 2.0)
        else:
            start_xy = (float(xy[0]), float(xy[1]))

        default_patched_style = self._style.patch(halign="center", valign="center")
        with transform(origin=xy, scale=scale):
            for is_custom_pass in (False, True):
                for index, item in enumerate(self._list):
                    if not item.show:
                        continue
                    patched_style = item.style.patch(halign="center", valign="center")
                    is_custom = patched_style != default_patched_style or item.text_style != self._text_style
                    if is_custom != is_custom_pass:
                        continue

                    self._draw_cell(
                        start_xy=start_xy,
                        index=index,
                        num_items=num_items,
                        text=item.text,
                        box_width=box_width,
                        box_height=box_height,
                        style=patched_style,
                        text_style=item.text_style,
                        direction=direction,
                    )
        return self

    @staticmethod
    def _draw_cell(  # noqa: PLR0913
        start_xy: Coordinate,
        index: int,
        num_items: int,
        text: str,
        box_width: PosFloat,
        box_height: PosFloat,
        style: Style,
        text_style: Style,
        direction: Literal["left", "right", "bottom", "top"],
    ) -> None:
        if direction == "left":
            x = start_xy[0] + box_width * (index + 0.5)
            y = start_xy[1] + box_height / 2
        elif direction == "right":
            x = start_xy[0] + box_width * (num_items - index - 0.5)
            y = start_xy[1] + box_height / 2
        elif direction == "bottom":
            x = start_xy[0] + box_width / 2
            y = start_xy[1] + box_height * (index + 0.5)
        else:
            x = start_xy[0] + box_width / 2
            y = start_xy[1] + box_height * (num_items - index - 0.5)

        rectangle(
            xy=(x, y),
            width=box_width,
            height=box_height,
            style=style,
            text=text,
            text_style=text_style,
        )
