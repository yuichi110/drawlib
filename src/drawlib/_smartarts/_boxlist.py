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

from typing import Literal

from pydantic import BaseModel, validate_call

from drawlib._core.l2_types import Coordinate, PosFloat
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import rectangle


class _Item(BaseModel):
    """Internal item class for BoxList."""

    text: str
    style: Style
    text_style: Style
    is_custom_style: bool


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
        self._style = style.patch(text_halign="center", text_valign="center")
        self._text_style = text_style
        self._list: list[_Item] = []

    @validate_call
    def append(
        self,
        text: str,
        *,
        style: Style | None = None,
        text_style: Style | None = None,
    ) -> None:
        """Append a box item to the list.

        Args:
            text: Text to display in the box.
            style: Style for the box. If None, default style is used.
            text_style: Style for the text inside the box. If None, default text_style is used.
        """
        self.extend([text], style=style, text_style=text_style)

    @validate_call
    def insert(
        self,
        index: int,
        text: str,
        *,
        style: Style | None = None,
        text_style: Style | None = None,
    ) -> None:
        """Insert a box item at the specified index.

        Args:
            index: Index where the item should be inserted.
            text: Text to display in the box.
            style: Style for the box. If None, default style is used.
            text_style: Style for the text inside the box. If None, default text_style is used.
        """
        is_custom_style = style is not None or text_style is not None

        if style is not None:
            resolved_style = style.patch(text_halign="center", text_valign="center")
        else:
            resolved_style = self._style

        if text_style is not None:
            resolved_text_style = text_style
        else:
            resolved_text_style = self._text_style

        item = _Item(
            text=text,
            style=resolved_style,
            text_style=resolved_text_style,
            is_custom_style=is_custom_style,
        )
        self._list.insert(index, item)

    @validate_call
    def extend(
        self,
        texts: list[str],
        *,
        style: Style | None = None,
        text_style: Style | None = None,
    ) -> None:
        """Extend the list with multiple box items.

        Args:
            texts: List of text strings to add as boxes.
            style: Style for the boxes. If None, default style is used.
            text_style: Style for the text inside the boxes. If None, default text_style is used.
        """
        for text in texts:
            self.insert(len(self._list), text, style=style, text_style=text_style)

    @validate_call
    def draw(
        self,
        xy: Coordinate,
        box_width: PosFloat,
        box_height: PosFloat,
        align: Literal["left", "right", "bottom", "top"] = "left",
    ) -> None:
        """Draw a list of boxes at the specified location.

        Args:
            xy: The starting point (x, y) to draw the list of boxes.
            box_width: The width of each box.
            box_height: The height of each box.
            align: The alignment of the boxes relative to the starting point.
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
                style=item.style,
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
                style=item.style,
                text_style=item.text_style,
                align=align,
            )

    @staticmethod
    def _draw_cell(
        start_xy: Coordinate,
        index: int,
        text: str,
        box_width: PosFloat,
        box_height: PosFloat,
        style: Style,
        text_style: Style,
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
            style=style,
            text=text,
            text_style=text_style,
        )
