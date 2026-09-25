# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""Table implementation module."""

from typing import Any, Literal

from PIL.ExifTags import Base
from pydantic import BaseModel

from drawlib._core.l1_core import guarded
from drawlib._core.l2_types import (
    TypeColor,
    TypeCoordinate,
    TypePosFloat,
    TypePosInt,
    TypeStr,
)
from drawlib._core.l3_fonts import Font
from drawlib._core.l3_styles import (
    Colors,
    ColorsEssentials,
    Style,
)
from drawlib._core.l4_canvas import line, rectangle
from drawlib._preset_styles import BasePresetStyles


class _CellStyleOrder(BaseModel):
    """Represents the style order of cells."""

    order: Literal["range", "even_odd"]
    textstyle1: Style
    background_color1: TypeColor
    textstyle2: Style | None = None
    background_color2: TypeColor | None = None
    rows: list[TypePosInt] | None = None
    columns: list[TypePosInt] | None = None


class _CellInfo(BaseModel):
    """Represents information about a cell."""

    xy: TypeCoordinate
    width: TypePosFloat
    height: TypePosFloat
    background_color: TypeColor
    textstyle: Style
    text: TypeStr


class Table:
    """A class used to create and manage the style and drawing of a table."""

    @guarded
    def __init__(self, *, styles: BasePresetStyles) -> None:
        """Initialize instance

        Args:
            styles: The preset styles catalog (required).
        """
        self._styles = styles
        self._bs_top: Style | None = None
        self._bs_top2: Style | None = None
        self._bs_bottom: Style | None = None
        self._bs_left: Style | None = None
        self._bs_left2: Style | None = None
        self._bs_right: Style | None = None
        self._bs_between_columns: Style | None = None
        self._bs_between_rows: Style | None = None
        self._cell_style_orders: list[_CellStyleOrder] = []

        self.set_predefined_style("default")

    @guarded
    def clear_styles(self) -> None:
        """Clears all cell and border styles, resetting the table to have no styles."""
        self._bs_top = None
        self._bs_top2 = None
        self._bs_bottom = None
        self._bs_left = None
        self._bs_left2 = None
        self._bs_right = None
        self._bs_between_columns = None
        self._bs_between_rows = None
        self._cell_style_orders = []

    @guarded
    def set_predefined_style(
        self,
        name: Literal[
            "default",
            "none",
            "monochrome",
            "border_simple",
        ],
    ) -> None:
        """Sets a predefined style for the table based on the given name.

        Args:
            name (Literal["default", "none", "monochrome", "border_simple"]): The name of the predefined style.

        Raises:
            ValueError: If the provided style name is not recognized.
        """
        self.clear_styles()

        if name == "default":
            """
            header: background light blue, bold white font
            even_odd: even snow color, odd white color
            border: bottom only
            """
            self.set_style_cell_evenodd(
                even_color=ColorsEssentials.Snow,
                even_textstyle=self._styles.primary.patch(text_color=ColorsEssentials.Charcoal),
                odd_color=ColorsEssentials.White,
                odd_textstyle=self._styles.primary.patch(text_color=ColorsEssentials.Charcoal),
            )
            self.set_style_cell_header(
                background_color=ColorsEssentials.LightBlue,
                textstyle=self._styles.bold.patch(text_color=ColorsEssentials.White, text_font=Font.SANSSERIF_BOLD),
            )
            self.set_style_border(
                bottom=self._styles.solid.patch(line_color=ColorsEssentials.Charcoal, line_width=1),
            )

        elif name == "none":
            """
            header: background transparent
            even_odd: both background transparent
            border: no border
            """
            self.set_style_cell(
                background_color=Colors.Transparent,
                textstyle=self._styles.primary.patch(text_color=ColorsEssentials.Charcoal),
            )

        elif name == "monochrome":
            """
            header: background gray, bold font
            even_odd: even snow color, odd white color
            border: bottom only
            """
            self.set_style_cell_evenodd(
                even_color=ColorsEssentials.Snow,
                even_textstyle=self._styles.primary.patch(text_color=ColorsEssentials.Charcoal),
                odd_color=ColorsEssentials.White,
                odd_textstyle=self._styles.primary.patch(text_color=ColorsEssentials.Charcoal),
            )
            self.set_style_cell_header(
                background_color=ColorsEssentials.Graphite,
                textstyle=self._styles.bold.patch(text_color=ColorsEssentials.White, text_font=Font.SANSSERIF_BOLD),
            )
            self.set_style_border(
                bottom=self._styles.solid.patch(line_color=ColorsEssentials.Charcoal, line_width=1),
            )

        elif name == "border_simple":
            """
            header: background white, bold font
            even_odd: both background white
            border: header1, header2(light), bottom
            """
            self.set_style_cell(
                background_color=ColorsEssentials.White,
                textstyle=self._styles.primary.patch(text_color=ColorsEssentials.Charcoal),
            )
            self.set_style_cell_header(
                background_color=ColorsEssentials.White,
                textstyle=self._styles.bold.patch(text_color=ColorsEssentials.Charcoal, text_font=Font.SANSSERIF_BOLD),
            )
            self.set_style_border(
                top=self._styles.solid.patch(line_color=ColorsEssentials.Charcoal, line_width=1.5),
                top2=self._styles.solid.patch(line_color=ColorsEssentials.Charcoal, line_width=0.75),
                bottom=self._styles.solid.patch(line_color=ColorsEssentials.Charcoal, line_width=1.5),
            )

        else:
            raise ValueError(f'Provided pre defined name "{name}" is not supported.')

    # cell styles

    @guarded
    def set_style_cell_headers(
        self,
        background_color: TypeColor,
        textstyle: Style,
    ) -> None:
        """Sets the style for both column and row headers.

        Args:
            background_color: The background color of the headers.
            textstyle: The text style of the headers.
        """
        self.set_style_cell_rowheader(background_color=background_color, textstyle=textstyle)
        self.set_style_cell_header(background_color=background_color, textstyle=textstyle)

    @guarded
    def set_style_cell_header(
        self,
        background_color: TypeColor,
        textstyle: Style,
    ) -> None:
        """Sets the style for the column header.

        Args:
            background_color: The background color of the column header.
            textstyle: The text style of the column header.
        """
        self.set_style_cell(
            background_color=background_color,
            textstyle=textstyle,
            rows=[0],
        )

    @guarded
    def set_style_cell_rowheader(
        self,
        background_color: TypeColor,
        textstyle: Style,
    ) -> None:
        """Sets the style for the row header.

        Args:
            background_color: The background color of the row header.
            textstyle: The text style of the row header.
        """
        self.set_style_cell(
            background_color=background_color,
            textstyle=textstyle,
            columns=[0],
        )

    @guarded
    def set_style_cell_evenodd(
        self,
        even_color: TypeColor,
        even_textstyle: Style,
        odd_color: TypeColor,
        odd_textstyle: Style,
    ) -> None:
        """Sets alternating styles for even and odd rows.

        Args:
            even_color: The background color for even rows.
            even_textstyle: The text style for even rows.
            odd_color: The background color for odd rows.
            odd_textstyle: The text style for odd rows.
        """
        self._cell_style_orders.append(
            _CellStyleOrder(
                order="even_odd",
                background_color1=even_color,
                background_color2=odd_color,
                textstyle1=even_textstyle,
                textstyle2=odd_textstyle,
            )
        )

    @guarded
    def set_style_cell(
        self,
        background_color: TypeColor,
        textstyle: Style,
        rows: list[TypePosInt] | None = None,
        columns: list[TypePosInt] | None = None,
    ) -> None:
        """Sets the style for specific cells.

        Args:
            background_color: The background color of the cells.
            textstyle: The text style of the cells.
            rows: A list of row indices to apply the style to. If None, applies to all rows.
            columns: A list of column indices to apply the style to. If None, applies to all columns.
        """
        self._cell_style_orders.append(
            _CellStyleOrder(
                order="range",
                background_color1=background_color,
                textstyle1=textstyle,
                rows=rows,
                columns=columns,
            )
        )

    # border style

    @guarded
    def set_style_border(
        self,
        top: Style | None = None,
        top2: Style | None = None,
        bottom: Style | None = None,
        left: Style | None = None,
        left2: Style | None = None,
        right: Style | None = None,
        between_columns: Style | None = None,
        between_rows: Style | None = None,
    ) -> None:
        """Sets the style for table borders.

        Args:
            top: Style for the top border.
            top2: Style for the secondary top border.
            bottom: Style for the bottom border.
            left: Style for the left border.
            left2: Style for the secondary left border.
            right: Style for the right border.
            between_columns: Style for borders between columns.
            between_rows: Style for borders between rows.
        """
        self._bs_top = top
        self._bs_top2 = top2
        self._bs_bottom = bottom
        self._bs_left = left
        self._bs_left2 = left2
        self._bs_right = right
        self._bs_between_columns = between_columns
        self._bs_between_rows = between_rows

    # draw

    @guarded
    def draw(
        self,
        xy: TypeCoordinate,
        width: TypePosFloat,
        height: TypePosFloat,
        data: list[list[Any]],
    ) -> None:
        """Draws the table with equal-sized cells.

        Args:
            xy (tuple[float, float]): The coordinates where the table should be drawn.
            width (float): The total width of the table.
            height (float): The total height of the table.
            data (List[List[Any]]): The data to be displayed in the table.
        """
        num_rows = len(data)
        num_cols = len(data[0])

        column_widths = [width / num_cols] * num_cols
        row_heights = [height / num_rows] * num_rows
        self.draw_flexible(
            xy=xy,
            column_widths=column_widths,
            row_heights=row_heights,
            data=data,
        )

    @guarded
    def draw_flexible(
        self,
        xy: TypeCoordinate,
        column_widths: list[TypePosFloat],
        row_heights: list[TypePosFloat],
        data: list[list[Any]],
    ) -> None:
        """Draws the table with flexible cell sizes.

        Args:
            xy (tuple[float, float]): The coordinates where the table should be drawn.
            column_widths (List[float]): A list of widths for each column.
            row_heights (List[float]): A list of heights for each row.
            data (List[List[Any]]): The data to be displayed in the table.
        """
        # create blank matrix
        default_textstyle = self._styles.primary
        matrix: list[list[_CellInfo]] = []
        for row_data in data:
            row: list[_CellInfo] = []
            for column in row_data:
                cell = _CellInfo(
                    xy=(0, 0),
                    width=0,
                    height=0,
                    background_color=Colors.White,
                    textstyle=default_textstyle,
                    text=str(column),
                )
                row.append(cell)
            matrix.append(row)

        # update matrix
        self._update_cell_xy_size(
            xy,
            column_widths=column_widths,
            row_heights=row_heights,
            matrix=matrix,
        )
        self._update_cell_style(matrix)

        # draw matrix
        self._draw_cells(matrix=matrix)

        # draw border line
        self._draw_border_lines(
            xy=xy,
            column_widths=column_widths,
            row_heights=row_heights,
        )

    # private

    @staticmethod
    def _update_cell_xy_size(
        xy: TypeCoordinate,
        column_widths: list[TypePosFloat],
        row_heights: list[TypePosFloat],
        matrix: list[list[_CellInfo]],
    ) -> None:
        x = xy[0]
        y = xy[1]
        for i, row_hight in enumerate(row_heights):
            for j, column_width in enumerate(column_widths):
                cell = matrix[i][j]
                cell.xy = (x + column_width / 2, y - row_hight / 2)
                cell.width = column_width
                cell.height = row_hight
                x += column_width
            x = xy[0]
            y -= row_hight

    def _update_cell_style(  # noqa: C901
        self,
        matrix: list[list[_CellInfo]],
    ) -> None:
        def style_even_odd(
            even_background_color: TypeColor,
            even_textstyle: Style,
            odd_background_color: TypeColor,
            odd_textstyle: Style,
        ) -> None:
            for i, row in enumerate(matrix):
                if i % 2 == 0:
                    for c in row:
                        c.background_color = even_background_color
                        c.textstyle = even_textstyle
                else:
                    for c in row:
                        c.background_color = odd_background_color
                        c.textstyle = odd_textstyle

        def style_range(
            background_color: TypeColor,
            textstyle: Style,
            rows: list[int] | None,
            columns: list[int] | None,
        ) -> None:
            if rows is None:
                rows = list(range(len(matrix)))
            if columns is None:
                columns = list(range(len(matrix[0])))

            for i, row in enumerate(matrix):
                for j, col in enumerate(row):
                    if i not in rows:
                        continue
                    if j not in columns:
                        continue
                    col.background_color = background_color
                    col.textstyle = textstyle

        for cso in self._cell_style_orders:
            if cso.order == "even_odd":
                if cso.background_color2 is None:
                    raise ValueError("Drawlib Internal error.")
                if cso.textstyle2 is None:
                    raise ValueError("Drawlib Internal error.")

                style_even_odd(
                    cso.background_color1,
                    cso.textstyle1,
                    cso.background_color2,
                    cso.textstyle2,
                )

            else:
                style_range(
                    cso.background_color1,
                    cso.textstyle1,
                    cso.rows,
                    cso.columns,
                )

    @staticmethod
    def _draw_cells(
        matrix: list[list[_CellInfo]],
    ) -> None:
        for row in matrix:
            for col in row:
                cell_xy = col.xy
                width = col.width
                height = col.height
                bg_color = col.background_color
                textstyle = col.textstyle
                text = col.text

                rectangle(
                    xy=cell_xy,
                    width=width,
                    height=height,
                    style=Style(
                        shape_line_width=0,
                        shape_line_color=Colors.Transparent,
                        shape_fill_color=bg_color,
                    ),
                    text=text,
                    textstyle=textstyle,
                )

    def _draw_border_lines(  # noqa: C901
        self,
        xy: TypeCoordinate,
        column_widths: list[TypePosFloat],
        row_heights: list[TypePosFloat],
    ) -> None:
        bs_top1: Style | None = None
        if self._bs_top is not None:
            bs_top1 = self._bs_top
        elif self._bs_between_columns is not None:
            bs_top1 = self._bs_between_columns

        bs_top2: Style | None = None
        if self._bs_top2 is not None:
            bs_top2 = self._bs_top2
        elif self._bs_between_columns is not None:
            bs_top2 = self._bs_between_columns

        bs_bottom: Style | None = None
        if self._bs_bottom is not None:
            bs_bottom = self._bs_bottom
        elif self._bs_between_columns is not None:
            bs_bottom = self._bs_between_columns

        bs_left1: Style | None = None
        if self._bs_left is not None:
            bs_left1 = self._bs_left
        elif self._bs_between_rows is not None:
            bs_left1 = self._bs_between_rows

        bs_left2: Style | None = None
        if self._bs_left2 is not None:
            bs_left2 = self._bs_left2
        elif self._bs_between_rows is not None:
            bs_left2 = self._bs_between_rows

        bs_right: Style | None = None
        if self._bs_right is not None:
            bs_right = self._bs_right
        elif self._bs_between_rows is not None:
            bs_right = self._bs_between_rows

        # draw rows
        x = xy[0]
        y1 = xy[1]
        y2 = xy[1] - sum(row_heights)
        for i, col_width in enumerate(column_widths):
            if i == 0:
                if bs_left1 is not None:
                    line((x, y1), (x, y2), style=bs_left1)
            elif i == 1:
                if bs_left2 is not None:
                    line((x, y1), (x, y2), style=bs_left2)
            elif i == len(column_widths) - 1:
                # right -1
                if self._bs_between_columns:
                    line((x, y1), (x, y2), style=self._bs_between_columns)

                # right. It is last
                x += col_width
                if bs_right is not None:
                    line((x, y1), (x, y2), style=bs_right)
                elif self._bs_between_columns:
                    line((x, y1), (x, y2), style=self._bs_between_columns)

            elif self._bs_between_columns:
                line((x, y1), (x, y2), style=self._bs_between_columns)

            x += col_width

        y = xy[1]
        x1 = xy[0]
        x2 = xy[0] + sum(column_widths)
        for i, row_height in enumerate(row_heights):
            if i == 0:
                if bs_top1 is not None:
                    line((x1, y), (x2, y), style=bs_top1)
            elif i == 1:
                if bs_top2 is not None:
                    line((x1, y), (x2, y), style=bs_top2)
            elif i == len(row_heights) - 1:
                # bottom -1
                if self._bs_between_rows:
                    line((x1, y), (x2, y), style=self._bs_between_rows)

                # right. It is last
                y -= row_height
                if bs_bottom is not None:
                    line((x1, y), (x2, y), style=bs_bottom)
                elif self._bs_between_rows:
                    line((x1, y), (x2, y), style=self._bs_between_rows)

            elif self._bs_between_rows:
                line((x1, y), (x2, y), style=self._bs_between_rows)

            y -= row_height
