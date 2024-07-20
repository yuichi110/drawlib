# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""GridLayout implementation module."""

import dataclasses
from typing import List, Optional, Tuple, Union

from drawlib.v0_2.private.core.model import ShapeStyle, ShapeTextStyle
from drawlib.v0_2.private.core.theme import dtheme
from drawlib.v0_2.private.core_canvas.canvas import rectangle


class GridLayout:
    """Class for rendering multiple rectangles which fit to grid."""

    def __init__(
        self,
        num_column: int,
        num_row: int,
        default_r: int = 0,
        default_style: Union[str, ShapeStyle, None] = None,
        default_textstyle: Union[str, ShapeTextStyle, None] = None,
    ) -> None:
        """Initialize class."""
        self._num_column = num_column
        self._num_row = num_row
        self._default_r = default_r
        if isinstance(default_style, str):
            default_style = dtheme.rectanglestyles.get(default_style)
        self._default_style = default_style
        if isinstance(default_textstyle, str):
            default_textstyle = dtheme.rectangletextstyles.get(default_textstyle)
        self._default_textstyle = default_textstyle

        self._items: List[_GridLayoutItem] = []

    def add(  # noqa: C901
        self,
        column_range: Tuple[int, int],
        row_range: Tuple[int, int],
        r: Optional[int] = None,
        style: Union[str, ShapeStyle, None] = None,
        text: str = "",
        textstyle: Union[str, ShapeTextStyle, None] = None,
    ) -> None:
        """
        Add an item to the grid layout.

        Args:
            column_range (Tuple[int, int]): The range of columns the item will span.
            row_range (Tuple[int, int]): The range of rows the item will span.
            r (Optional[int], optional): The radius of the item. Default is None, which uses the default radius.
            style (Union[str, ShapeStyle, None], optional):
                    The style of the item.
                    Can be a string key for a predefined style, a ShapeStyle object,
                    or None to use the default style.
            text (str, optional): The text associated with the item. Default is an empty string.
            textstyle (Union[str, ShapeTextStyle, None], optional):
                    The text style of the item. Can be a string key for a predefined text style,
                    a ShapeTextStyle object, or None to use the default text style.

        Raises:
            ValueError: If the column or row ranges are invalid or out of bounds.
        """
        # validate column
        c1, c2 = column_range
        if c1 > c2:
            raise ValueError()
        if c1 < 0:
            raise ValueError()
        if c2 > self._num_column:
            raise ValueError()

        # validate row
        r1, r2 = row_range
        if r1 > r2:
            raise ValueError()
        if r1 < 0:
            raise ValueError()
        if r2 > self._num_column:
            raise ValueError()

        # string style to Style class
        if isinstance(style, str):
            style = dtheme.rectanglestyles.get(style)
        if isinstance(textstyle, str):
            textstyle = dtheme.rectangletextstyles.get(textstyle)

        # apply default if args are None
        if r is None:
            r = self._default_r
        if style is None:
            style = self._default_style
        if textstyle is None:
            textstyle = self._default_textstyle

        # push
        item = _GridLayoutItem(
            column_range=column_range,
            row_range=row_range,
            r=r,
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
        outer_r: int = 0,
        outer_style: Union[str, ShapeStyle, None] = None,
    ) -> None:
        """Draw the grid layout.

        Args:
            xy (Tuple[float, float]): The x and y coordinates of the top-left corner of the grid.
            width (float): The total width of the grid.
            height (float): The total height of the grid.
            margin (float): The margin between grid items.
            outer_r (int, optional): The radius for the outer grid border. Default is 0.
            outer_style (Union[str, ShapeStyle, None], optional):
                    The style for the outer grid border. Can be a string key for a predefined style,
                    a ShapeStyle object, or None.
        """
        column_widths = [width / self._num_column] * self._num_column
        row_heights = [height / self._num_row] * self._num_row

        if outer_style is None:
            column_margins = [margin] + [margin * 2] * (self._num_column - 1) + [margin]
            row_margins = [margin] + [margin * 2] * (self._num_row - 1) + [margin]
        else:
            column_margins = [margin * 2] * (self._num_column + 1)
            row_margins = [margin * 2] * (self._num_row + 1)

        self.draw_flexible(
            xy=xy,
            column_widths=column_widths,
            column_margins=column_margins,
            row_heights=row_heights,
            row_margins=row_margins,
            outer_r=outer_r,
            outer_style=outer_style,
        )

    def draw_flexible(  # noqa: C901
        self,
        xy: Tuple[float, float],
        column_widths: List[float],
        column_margins: List[float],
        row_heights: List[float],
        row_margins: List[float],
        outer_r: int = 0,
        outer_style: Union[str, ShapeStyle, None] = None,
    ) -> None:
        """Draw the grid layout with flexible column widths and row heights.

        Args:
            xy (Tuple[float, float]): The x and y coordinates of the top-left corner of the grid.
            column_widths (List[float]): The widths of each column.
            column_margins (List[float]): The margins between columns.
            row_heights (List[float]): The heights of each row.
            row_margins (List[float]): The margins between rows.
            outer_r (int, optional): The radius for the outer grid border. Default is 0.
            outer_style (Union[str, ShapeStyle, None], optional):
                    The style for the outer grid border.
                    Can be a string key for a predefined style, a ShapeStyle object, or None.

        Raises:
            ValueError: If the lengths of column_widths, column_margins, row_heights, or row_margins are incorrect.
        """
        # validate
        if len(column_widths) != self._num_column:
            raise ValueError()
        if len(column_margins) != self._num_column + 1:
            raise ValueError()
        if len(row_heights) != self._num_row:
            raise ValueError()
        if len(row_margins) != self._num_row + 1:
            raise ValueError()

        # draw outer rectangle
        if outer_style is not None:
            if isinstance(outer_style, str):
                outer_style = dtheme.rectanglestyles.get(outer_style)
            outer_style.halign = "left"
            outer_style.valign = "bottom"
            rectangle(
                xy=xy,
                width=sum(column_widths),
                height=sum(row_heights),
                r=outer_r,
                style=outer_style,
            )

        # utility
        def sum_till_index(lst: List[float], index: int) -> float:
            if index == 0:
                return 0
            return sum([lst[i] for i in range(index)])

        for item in self._items:
            column_range = item.column_range
            row_range = item.row_range
            r = item.r
            style = item.style
            text = item.text
            textstyle = item.textstyle

            cr0 = column_range[0]
            cr1 = column_range[1]
            rr0 = row_range[0]
            rr1 = row_range[1]

            # coordinate without margin
            lb_xy = (sum_till_index(column_widths, cr0), sum_till_index(row_heights, rr0))
            width = sum_till_index(column_widths, cr1 + 1) - lb_xy[0]
            height = sum_till_index(row_heights, rr1 + 1) - lb_xy[1]

            # get margins
            margin_left = column_margins[cr0] if cr0 == 0 else column_margins[cr0] / 2
            margin_right = column_margins[cr1 + 1] if cr1 + 1 == self._num_column else column_margins[cr1 + 1] / 2
            margin_bottom = row_margins[rr0] if rr0 == 0 else row_margins[rr0] / 2
            margin_top = row_margins[rr1 + 1] if rr1 + 1 == self._num_row else row_margins[rr1 + 1] / 2

            # update coordinate
            lb_xy = (lb_xy[0] + margin_left, lb_xy[1] + margin_bottom)
            width = width - margin_left - margin_right
            height = height - margin_bottom - margin_top

            # set align left bottom
            if style is None:
                style = self._default_style
            if style is None:
                style = dtheme.rectanglestyles.get()
            else:
                style = style.copy()
            style.halign = "left"
            style.valign = "bottom"

            # apply default text style if specified text style is None
            if textstyle is None:
                textstyle = self._default_textstyle

            # draw
            rectangle(
                xy=(xy[0] + lb_xy[0], xy[1] + lb_xy[1]),
                width=width,
                height=height,
                r=r,
                style=style,
                text=text,
                textstyle=textstyle,
            )


@dataclasses.dataclass
class _GridLayoutItem:
    column_range: Tuple[int, int]
    row_range: Tuple[int, int]
    r: int
    style: Optional[ShapeStyle]
    text: str
    textstyle: Optional[ShapeTextStyle]
