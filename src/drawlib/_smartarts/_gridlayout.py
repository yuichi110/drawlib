# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""GridLayout implementation module."""

from pydantic import BaseModel, validate_call

from drawlib._core.l2_types import Coordinate, PosFloat, PosInt
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import rectangle, transform


class GridItem(BaseModel):
    """Class for storing grid layout item information."""

    position: tuple[PosInt, PosInt]
    width: PosInt
    height: PosInt
    r: PosFloat
    style: Style
    text: str
    text_style: Style
    show: bool = True


class GridLayout:
    """Class for rendering multiple rectangles which fit to grid."""

    @validate_call
    def __init__(
        self,
        *,
        num_column: PosInt,
        num_row: PosInt,
        style: Style,
        text_style: Style,
        r: PosFloat = 0.0,
    ) -> None:
        """Initializes a GridLayout instance.

        Args:
            num_column: The number of columns in the grid.
            num_row: The number of rows in the grid.
            style: The default style for the cell rectangles.
            text_style: The default text style for the cell text.
            r: The default radius for the rectangles. Defaults to 0.0.
        """
        self._num_column = num_column
        self._num_row = num_row
        self._r = r
        self._style = style
        self._text_style = text_style

        self._items: list[GridItem] = []

    @property
    def items(self) -> list[GridItem]:
        """Return the registered grid layout items."""
        return self._items

    @validate_call
    def add(  # noqa: PLR0913
        self,
        position: tuple[PosInt, PosInt],
        width: PosInt,
        height: PosInt,
        *,
        r: PosFloat | None = None,
        style: Style | None = None,
        text: str = "",
        text_style: Style | None = None,
        show: bool = True,
    ) -> GridItem:
        """Add a cell spanning one or more grid positions.

        Args:
            position: Starting (column, row) coordinate for the cell.
            width: Number of columns this cell spans.
            height: Number of rows this cell spans.
            r: Corner radius for the cell rectangle. If None, default r is used.
            style: Style for the cell rectangle. If None, default style is used.
            text: Text to display inside the cell.
            text_style: Style for the text. If None, default text_style is used.
            show: Whether to render this grid cell. Defaults to True.

        Returns:
            GridItem: The created grid cell item instance.

        Raises:
            ValueError: If width/height < 1 or position is out of grid bounds.
        """
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

        cell_r = r if r is not None else self._r
        resolved_style = style if style is not None else self._style
        resolved_text_style = text_style if text_style is not None else self._text_style

        item = GridItem(
            position=(column_start, row_start),
            width=width,
            height=height,
            r=cell_r,
            text=text,
            style=resolved_style,
            text_style=resolved_text_style,
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
        outer_r: PosFloat | None = None,
        outer_style: Style | None = None,
        scale: PosFloat = 1.0,
    ) -> None:
        """Draw the grid layout.

        Args:
            xy (Tuple[float, float]): The x and y coordinates of the bottom-left corner of the grid.
            width (float): The total width of the grid.
            height (float): The total height of the grid.
            margin (float): The margin between grid items.
            outer_r (int, optional): The radius for the outer grid border. Default is 0.
            outer_style (Style, optional): The style for the outer grid border.
            scale (float): Proportional scale factor around xy. Defaults to 1.0.
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
            scale=scale,
        )

    @validate_call
    def draw_flexible(  # noqa: C901, PLR0912, PLR0913
        self,
        xy: Coordinate,
        column_widths: list[PosFloat],
        column_margins: list[PosFloat],
        row_heights: list[PosFloat],
        row_margins: list[PosFloat],
        outer_r: PosFloat | None = None,
        outer_style: Style | None = None,
        scale: PosFloat = 1.0,
    ) -> None:
        """Draw the grid layout with flexible column widths and row heights.

        Args:
            xy (Tuple[float, float]): The x and y coordinates of the bottom-left corner of the grid.
            column_widths (List[float]): The widths of each column.
            column_margins (List[float]): The margins between columns.
            row_heights (List[float]): The heights of each row.
            row_margins (List[float]): The margins between rows.
            outer_r (int, optional): The radius for the outer grid border. Default is 0.
            outer_style (Style, optional): The style for the outer grid border.
            scale (float): Proportional scale factor around xy. Defaults to 1.0.

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

        with transform(origin=xy, scale=scale):
            # draw outer rectangle
            if outer_style is not None:
                outer_style = outer_style.patch(halign="left", valign="bottom")
                if outer_r is None:
                    outer_r = self._r

                rectangle(
                    xy=xy,
                    width=sum(column_widths) + sum(column_margins),
                    height=sum(row_heights) + sum(row_margins),
                    r=outer_r,
                    style=outer_style,
                )

            # utility
            def get_position(column_index: int, row_index: int) -> Coordinate:
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
                if not item.show:
                    continue

                cr0 = item.position[0]
                cr1 = item.position[0] + item.width - 1
                rr0 = item.position[1]
                rr1 = item.position[1] + item.height - 1

                r = item.r
                style = item.style.patch(halign="left", valign="bottom")
                text = item.text
                text_style = item.text_style

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
                    text_style=text_style,
                )
