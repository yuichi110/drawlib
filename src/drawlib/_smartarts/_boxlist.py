# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""BoxList implementation module."""

from typing import List, Literal

from pydantic import BaseModel

from drawlib._core.l1_core import guarded
from drawlib._core.l2_types import (
    TypeCoordinate,
    TypePosFloat,
    TypeStr,
)
from drawlib._core.l3_styles import Colors, ShapeStyle, ShapeTextStyle
from drawlib._core.l4_canvas import rectangle
from drawlib._theme import get_style


class _Item(BaseModel):
    """Internal item class for BoxList."""

    text: TypeStr
    box_style: ShapeStyle
    text_style: ShapeTextStyle
    is_custom_style: bool


class BoxList:
    """A class to draw a list of boxes with text, supporting highlighting of certain boxes.

    Args:
        default_box_style (Union[str, ShapeStyle, None]): The style for the boxes.
        default_text_style (Union[str, ShapeTextStyle, None]): The style for the text inside the boxes.

    """

    @guarded
    def __init__(
        self,
        default_box_style: TypeStr | ShapeStyle | None = None,
        default_text_style: TypeStr | ShapeTextStyle | None = None,
    ) -> None:
        """Initialize BoxList.

        Args:
            default_box_style (Union[str, ShapeStyle, None]): The style for the boxes.
            default_text_style (Union[str, ShapeTextStyle, None]): The style for the text inside the boxes.

        """
        default_box_style = get_style(default_box_style)
        default_box_style.text_halign = "center"
        default_box_style.text_valign = "center"
        self._default_box_style = default_box_style

        default_text_style = get_style(default_text_style)
        self._default_text_style = default_text_style

        self._list: List[_Item] = []

    @guarded
    def append(
        self,
        text: TypeStr,
        box_style: TypeStr | ShapeStyle | None = None,
        text_style: TypeStr | ShapeTextStyle | None = None,
    ) -> None:
        self.extend([text], box_style=box_style, text_style=text_style)

    @guarded
    def insert(
        self,
        index: int,
        text: TypeStr,
        box_style: TypeStr | ShapeStyle | None = None,
        text_style: TypeStr | ShapeTextStyle | None = None,
    ) -> None:
        is_custom_style = box_style is not None or text_style is not None

        box_style_resolved = get_style(box_style) if box_style is not None else self._default_box_style
        text_style_resolved = get_style(text_style) if text_style is not None else self._default_text_style

        item = _Item(
            text=text,
            box_style=box_style_resolved,
            text_style=text_style_resolved,
            is_custom_style=is_custom_style,
        )
        self._list.insert(index, item)

    @guarded
    def extend(
        self,
        texts: List[TypeStr],
        box_style: TypeStr | ShapeStyle | None = None,
        text_style: TypeStr | ShapeTextStyle | None = None,
    ) -> None:
        is_custom_style = box_style is not None or text_style is not None

        box_style_resolved = get_style(box_style) if box_style is not None else self._default_box_style
        text_style_resolved = get_style(text_style) if text_style is not None else self._default_text_style

        for text in texts:
            item = _Item(
                text=text,
                box_style=box_style_resolved,
                text_style=text_style_resolved,
                is_custom_style=is_custom_style,
            )
            self._list.append(item)

        for text in texts:
            item = _Item(
                text=text,
                box_style=box_style_resolved,
                text_style=text_style_resolved,
                is_custom_style=is_custom_style,
            )
            self._list.append(item)

    @guarded
    def draw(
        self,
        xy: TypeCoordinate,
        box_width: TypePosFloat,
        box_height: TypePosFloat,
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
        start_xy: TypeCoordinate,
        index: int,
        text: str,
        box_width: TypePosFloat,
        box_height: TypePosFloat,
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
