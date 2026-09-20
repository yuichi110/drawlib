# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""GridLayout implementation module."""

from pydantic import BaseModel

from drawlib._core.l1_core import guarded
from drawlib._core.l2_types import (
    TypeAngle,
    TypeCoordinate,
    TypePosFloat,
    TypePosInt,
    TypeStr,
)
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import rectangle
from drawlib._theme import get_style


class _GridLayoutItem(BaseModel):
    """Internal class for storing grid layout item information."""

    column_range: tuple[TypePosInt, TypePosInt]
    row_range: tuple[TypePosInt, TypePosInt]
    r: TypePosFloat
    style: Style
    text: TypeStr
    textstyle: Style


class GridLayout:
    """Class for rendering multiple rectangles which fit to grid.

    Args:
    num_column (int): The number of columns in the grid.
    num_row (int): The number of rows in the grid.
    default_r (int, optional): The default radius for the rectangles. Defaults to 0.
    default_style (Union[str, Style, None], optional): The default style for the rectangles.
        Can be a string key, a Style object, or None. Defaults to None.
    default_textstyle (Union[str, Style, None], optional): The default text style for the rectangles.
        Can be a string key, a Style object, or None. Defaults to None.
    default_textangle (Optional[float], optional): The default angle for the text inside the rectangles.
        If None, no angle is applied. Defaults to None.
    """

    @guarded
    def __init__(
        self,
        num_column: TypePosInt,
        num_row: TypePosInt,
        default_r: TypePosFloat = 0,
        default_style: TypeStr | Style | None = None,
        default_textstyle: TypeStr | Style | None = None,
        default_textangle: TypeAngle | None = None,
    ) -> None:
        """Initializes a GridLayout instance.

        Args:
            num_column (int): The number of columns in the grid.
            num_row (int): The number of rows in the grid.
            default_r (int, optional): The default radius for the rectangles. Defaults to 0.
            default_style (Union[str, Style, None], optional): The default style for the rectangles.
                Can be a string key, a Style object, or None. Defaults to None.
            default_textstyle (Union[str, Style, None], optional): The default text style for the rectangles.
                Can be a string key, a Style object, or None. Defaults to None.
            default_textangle (Optional[float], optional): The default angle for the text inside the rectangles.
                If None, no angle is applied. Defaults to None.

        """
        self._num_column = num_column
        self._num_row = num_row
        self._default_r = default_r
        if isinstance(default_style, str):
            default_style = get_style(default_style)
        self._default_style = default_style
        if isinstance(default_textstyle, str):
            default_textstyle = get_style(default_textstyle)
        self._default_textstyle = default_textstyle
        self._default_textangle = default_textangle

        self._items: list[_GridLayoutItem] = []

    @guarded
    def add(  # noqa: C901
        self,
        position: tuple[TypePosInt, TypePosInt],
        width: TypePosInt,
        height: TypePosInt,
        r: TypePosFloat | None = None,
        style: TypeStr | Style | None = None,
        text: TypeStr = "",
        textstyle: TypeStr | Style | None = None,
        textangle: TypeAngle | None = None,
        text_xy_shift: TypeCoordinate | None = None,
    ) -> None:
        if width < 1:
            raise ValueError("Grid cell must have 1+ columns")
        if height < 1:
            raise ValueError("Grid cell must have 1+ rows")

        column_start, row_start = position
        if not 0 <= column_start < self._num_column:
            raise ValueError("Grid cell's column start position must be between 0 ~ last-column.")
        if not 0 <= row_start < self._num_row:
            raise ValueError("Grid cell's row start position must be between 0 ~ last-column.")

        column_end = column_start + width - 1
        row_end = row_start + height - 1
        if column_end >= self._num_column:
            raise ValueError("Grid cell's column start position must be between 0 ~ last-column.")
        if row_end >= self._num_row:
            raise ValueError("Grid cell's row start position must be between 0 ~ last-column.")

        if isinstance(style, str):
            style = get_style(style)
        if isinstance(textstyle, str):
            textstyle = get_style(textstyle)

        if r is None:
            r = self._default_r
        if style is None:
            style = self._default_style
        if textstyle is None:
            textstyle = self._default_textstyle
        if textangle is None:
            textangle = self._default_textangle

        if style is None:
            style = get_style()
        else:
            style = style.copy()
        style.text_halign = "left"
        style.text_valign = "bottom"

        if textstyle is None:
            textstyle = get_style()
        if textangle is not None:
            textstyle.text_angle = textangle
        if text_xy_shift is not None:
            textstyle.text_xy_shift = text_xy_shift

        item = _GridLayoutItem(
            column_range=(column_start, column_end),
            row_range=(row_start, row_end),
            r=r,
            text=text,
            style=style,
            textstyle=textstyle,
        )
        self._items.append(item)

    @guarded
    def draw(
        self,
        xy: TypeCoordinate,
        width: TypePosFloat,
        height: TypePosFloat,
        margin: TypePosFloat,
        outer_r: TypePosFloat | None = None,
        outer_style: TypeStr | Style | None = None,
    ) -> None:
        """Draw the grid layout.

        Args:
            xy (Tuple[float, float]): The x and y coordinates of the top-left corner of the grid.
            width (float): The total width of the grid.
            height (float): The total height of the grid.
            margin (float): The margin between grid items.
            outer_r (int, optional): The radius for the outer grid border. Default is 0.
            outer_style (Union[str, Style, None], optional):
                    The style for the outer grid border. Can be a string key for a predefined style,
                    a Style object, or None.
        """
        if outer_style is None:
            column_widths = [(width - margin * (self._num_column - 1)) / self._num_column] * self._num_column
            row_heights = [(height - margin * (self._num_row - 1)) / self._num_row] * self._num_row
            column_margins = [0] + [margin] * (self._num_column - 1) + [0]
            row_margins = [0] + [margin] * (self._num_row - 1) + [0]
        else:
            column_widths = [(width - margin * (self._num_column + 1)) / self._num_column] * self._num_column
            row_heights = [(height - margin * (self._num_row + 1)) / self._num_row] * self._num_row
            column_margins = [margin] * (self._num_column + 1)
            row_margins = [margin] * (self._num_row + 1)

        self.draw_flexible(
            xy=xy,
            column_widths=column_widths,
            column_margins=column_margins,
            row_heights=row_heights,
            row_margins=row_margins,
            outer_r=outer_r,
            outer_style=outer_style,
        )

    @guarded
    def draw_flexible(  # noqa: C901
        self,
        xy: TypeCoordinate,
        column_widths: list[TypePosFloat],
        column_margins: list[TypePosFloat],
        row_heights: list[TypePosFloat],
        row_margins: list[TypePosFloat],
        outer_r: TypePosFloat | None = None,
        outer_style: TypeStr | Style | None = None,
    ) -> None:
        """Draw the grid layout with flexible column widths and row heights.

        Args:
            xy (Tuple[float, float]): The x and y coordinates of the top-left corner of the grid.
            column_widths (List[float]): The widths of each column.
            column_margins (List[float]): The margins between columns.
            row_heights (List[float]): The heights of each row.
            row_margins (List[float]): The margins between rows.
            outer_r (int, optional): The radius for the outer grid border. Default is 0.
            outer_style (Union[str, Style, None], optional):
                    The style for the outer grid border.
                    Can be a string key for a predefined style, a Style object, or None.

        Raises:
            ValueError: If the lengths of column_widths, column_margins, row_heights, or row_margins are incorrect.
        """
        # validate
        if len(column_widths) != self._num_column:
            raise ValueError('Length of arg "column_widths" does not match to num of columns')
        if len(column_margins) != self._num_column + 1:
            raise ValueError('Length of arg "column_margins" does not match to num of columns + 1')
        if len(row_heights) != self._num_row:
            raise ValueError('Length of arg "row_heights" does not match to num of rows')
        if len(row_margins) != self._num_row + 1:
            raise ValueError('Length of arg "row_margins" does not match to num of rows + 1')

        # draw outer rectangle
        if outer_style is not None:
            if isinstance(outer_style, str):
                outer_style = get_style(outer_style)
            else:
                outer_style = outer_style.copy()
            outer_style.text_halign = "left"
            outer_style.text_valign = "bottom"
            if outer_r is None:
                outer_r = self._default_r

            rectangle(
                xy=xy,
                width=sum(column_widths) + sum(column_margins),
                height=sum(row_heights) + sum(row_margins),
                r=outer_r,
                style=outer_style,
            )

        # utility
        def get_position(column_index: int, row_index: int) -> TypeCoordinate:
            x, y = xy
            if column_index == 0:
                new_x = x + column_margins[0]
            else:
                new_x = x + sum(column_margins[: column_index + 1]) + sum(column_widths[:column_index])

            if row_index == 0:
                new_y = y + row_margins[0]
            else:
                new_y = y + sum(row_margins[: row_index + 1]) + sum(row_heights[:row_index])

            return (new_x, new_y)

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

            item_xy_left_bottom = get_position(cr0, rr0)
            t = get_position(cr1, rr1)
            item_xy_right_top = (t[0] + column_widths[cr1], t[1] + row_heights[rr1])

            width, height = (
                item_xy_right_top[0] - item_xy_left_bottom[0],
                item_xy_right_top[1] - item_xy_left_bottom[1],
            )

            rectangle(
                xy=item_xy_left_bottom,
                width=width,
                height=height,
                r=r,
                style=style,
                text=text,
                textstyle=textstyle,
            )
