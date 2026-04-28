# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""Table implementation module."""

import dataclasses
from typing import Any, List, Literal, Optional, Tuple, Union

from drawlib.v0_2.private.core.colors import Colors, ColorsThemeEssentials
from drawlib.v0_2.private.core.fonts import Font
from drawlib.v0_2.private.core.model import LineStyle, ShapeStyle, ShapeTextStyle
from drawlib.v0_2.private.core.theme import dtheme
from drawlib.v0_2.private.core_canvas.canvas import line, rectangle
from drawlib.v0_2.private.util import error_handler


@dataclasses.dataclass
class _CellStyleOrder:
    order: Literal["range", "even_odd"]
    textstyle1: ShapeTextStyle
    background_color1: Union[Tuple[int, int, int], Tuple[int, int, int, float]]
    textstyle2: Optional[ShapeTextStyle] = None
    background_color2: Union[Tuple[int, int, int], Tuple[int, int, int, float], None] = None
    rows: Optional[List[int]] = None
    columns: Optional[List[int]] = None


@dataclasses.dataclass
class _CellInfo:
    xy: Tuple[float, float]
    width: float
    height: float
    background_color: Union[Tuple[int, int, int], Tuple[int, int, int, float]]
    textstyle: ShapeTextStyle
    text: str


class Table:
    """A class used to create and manage the style and drawing of a table."""

    @error_handler
    def __init__(self) -> None:
        """Initialize instance"""
        self._bs_top: Optional[LineStyle] = None
        self._bs_top2: Optional[LineStyle] = None
        self._bs_bottom: Optional[LineStyle] = None
        self._bs_left: Optional[LineStyle] = None
        self._bs_left2: Optional[LineStyle] = None
        self._bs_right: Optional[LineStyle] = None
        self._bs_between_columns: Optional[LineStyle] = None
        self._bs_between_rows: Optional[LineStyle] = None
        self._cell_style_orders: List[_CellStyleOrder] = []

        self.set_predefined_style("default")

    @error_handler
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

    @error_handler
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
            name (Literal["default", "monochrome", "white"]): The name of the predefined style.

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
                even_color=ColorsThemeEssentials.Snow,
                even_textstyle=ShapeTextStyle(color=ColorsThemeEssentials.Charcoal),
                odd_color=ColorsThemeEssentials.White,
                odd_textstyle=ShapeTextStyle(color=ColorsThemeEssentials.Charcoal),
            )
            self.set_style_cell_header(
                background_color=ColorsThemeEssentials.LightBlue,
                textstyle=ShapeTextStyle(color=ColorsThemeEssentials.White, font=Font.SANSSERIF_BOLD),
            )
            self.set_style_border(
                bottom=LineStyle(color=ColorsThemeEssentials.Charcoal, width=1),
            )

        elif name == "none":
            """
            header: background transparent
            even_odd: both background transparent
            border: no border
            """
            self.set_style_cell(
                background_color=Colors.Transparent,
                textstyle=ShapeTextStyle(color=ColorsThemeEssentials.Charcoal),
            )

        elif name == "monochrome":
            """
            header: background gray, bold font
            even_odd: even snow color, odd white color
            border: bottom only
            """
            self.set_style_cell_evenodd(
                even_color=ColorsThemeEssentials.Snow,
                even_textstyle=ShapeTextStyle(color=ColorsThemeEssentials.Charcoal),
                odd_color=ColorsThemeEssentials.White,
                odd_textstyle=ShapeTextStyle(color=ColorsThemeEssentials.Charcoal),
            )
            self.set_style_cell_header(
                background_color=ColorsThemeEssentials.Graphite,
                textstyle=ShapeTextStyle(color=ColorsThemeEssentials.White, font=Font.SANSSERIF_BOLD),
            )
            self.set_style_border(
                bottom=LineStyle(color=ColorsThemeEssentials.Charcoal, width=1),
            )

        elif name == "border_simple":
            """
            header: background white, bold font
            even_odd: both background white
            border: header1, header2(light), bottom
            """
            self.set_style_cell(
                background_color=ColorsThemeEssentials.White,
                textstyle=ShapeTextStyle(color=ColorsThemeEssentials.Charcoal),
            )
            self.set_style_cell_header(
                background_color=ColorsThemeEssentials.White,
                textstyle=ShapeTextStyle(color=ColorsThemeEssentials.Charcoal, font=Font.SANSSERIF_BOLD),
            )
            self.set_style_border(
                top=LineStyle(color=ColorsThemeEssentials.Charcoal, width=1.5),
                top2=LineStyle(color=ColorsThemeEssentials.Charcoal, width=0.75),
                bottom=LineStyle(color=ColorsThemeEssentials.Charcoal, width=1.5),
            )

        else:
            raise ValueError(f'Provided pre defined name "{name}" is not supported.')

    # cell styles

    @error_handler
    def set_style_cell_headers(
        self,
        background_color: Union[Tuple[int, int, int], Tuple[int, int, int, float]],
        textstyle: Union[str, ShapeTextStyle],
    ) -> None:
        """Sets the style for both column and row headers.

        Args:
            background_color (Union[Tuple[int, int, int], Tuple[int, int, int, float]]):
                    The background color of the headers.
            textstyle (Union[str, ShapeTextStyle]):
                    The text style of the headers. Can be a string key for predefined styles or a ShapeTextStyle object.
        """
        if isinstance(textstyle, str):
            textstyle = dtheme.shapetextstyles.get(textstyle)

        self.set_style_cell_rowheader(background_color=background_color, textstyle=textstyle)
        self.set_style_cell_header(background_color=background_color, textstyle=textstyle)

    @error_handler
    def set_style_cell_header(
        self,
        background_color: Union[Tuple[int, int, int], Tuple[int, int, int, float]],
        textstyle: Union[str, ShapeTextStyle],
    ) -> None:
        """
        Sets the style for the column header.

        Args:
            background_color (Union[Tuple[int, int, int], Tuple[int, int, int, float]]):
                    The background color of the column header.
            textstyle (Union[str, ShapeTextStyle]):
                    The text style of the column header.
                    Can be a string key for predefined styles or a ShapeTextStyle object.
        """
        if isinstance(textstyle, str):
            textstyle = dtheme.shapetextstyles.get(textstyle)

        self.set_style_cell(
            background_color=background_color,
            textstyle=textstyle,
            rows=[0],
        )

    @error_handler
    def set_style_cell_rowheader(
        self,
        background_color: Union[Tuple[int, int, int], Tuple[int, int, int, float]],
        textstyle: Union[str, ShapeTextStyle],
    ) -> None:
        """
        Sets the style for the row header.

        Args:
            background_color (Union[Tuple[int, int, int], Tuple[int, int, int, float]]):
                    The background color of the row header.
            textstyle (Union[str, ShapeTextStyle]):
                    The text style of the row header.
                    Can be a string key for predefined styles or a ShapeTextStyle object.
        """
        if isinstance(textstyle, str):
            textstyle = dtheme.shapetextstyles.get(textstyle)

        self.set_style_cell(
            background_color=background_color,
            textstyle=textstyle,
            columns=[0],
        )

    @error_handler
    def set_style_cell_evenodd(
        self,
        even_color: Union[Tuple[int, int, int], Tuple[int, int, int, float]],
        even_textstyle: Union[str, ShapeTextStyle],
        odd_color: Union[Tuple[int, int, int], Tuple[int, int, int, float]],
        odd_textstyle: Union[str, ShapeTextStyle],
    ) -> None:
        """
        Sets alternating styles for even and odd rows.

        Args:
            even_color (Union[Tuple[int, int, int], Tuple[int, int, int, float]]):
                    The background color for even rows.
            even_textstyle (Union[str, ShapeTextStyle]):
                    The text style for even rows.
                    Can be a string key for predefined styles or a ShapeTextStyle object.
            odd_color (Union[Tuple[int, int, int], Tuple[int, int, int, float]]):
                    The background color for odd rows.
            odd_textstyle (Union[str, ShapeTextStyle]):
                    The text style for odd rows.
                    Can be a string key for predefined styles or a ShapeTextStyle object.
        """
        if isinstance(even_textstyle, str):
            even_textstyle = dtheme.shapetextstyles.get(even_textstyle)
        if isinstance(odd_textstyle, str):
            odd_textstyle = dtheme.shapetextstyles.get(odd_textstyle)

        self._cell_style_orders.append(
            _CellStyleOrder(
                "even_odd",
                background_color1=even_color,
                background_color2=odd_color,
                textstyle1=even_textstyle,
                textstyle2=odd_textstyle,
            )
        )

    @error_handler
    def set_style_cell(
        self,
        background_color: Union[Tuple[int, int, int], Tuple[int, int, int, float]],
        textstyle: Union[str, ShapeTextStyle],
        rows: Optional[List[int]] = None,
        columns: Optional[List[int]] = None,
    ) -> None:
        """
        Sets the style for specific cells.

        Args:
            background_color (Union[Tuple[int, int, int], Tuple[int, int, int, float]]):
                    The background color of the cells.
            textstyle (Union[str, ShapeTextStyle]):
                    The text style of the cells.
                    Can be a string key for predefined styles or a ShapeTextStyle object.
            rows (Optional[List[int]]):
                    A list of row indices to apply the style to. If None, applies to all rows.
            columns (Optional[List[int]]):
                    A list of column indices to apply the style to. If None, applies to all columns.
        """
        if isinstance(textstyle, str):
            textstyle = dtheme.shapetextstyles.get(textstyle)

        self._cell_style_orders.append(
            _CellStyleOrder(
                "range",
                background_color1=background_color,
                textstyle1=textstyle,
                rows=rows,
                columns=columns,
            )
        )

    # border style

    @error_handler
    def set_style_border(  # noqa: C901
        self,
        top: Union[str, LineStyle, None] = None,
        top2: Union[str, LineStyle, None] = None,
        bottom: Union[str, LineStyle, None] = None,
        left: Union[str, LineStyle, None] = None,
        left2: Union[str, LineStyle, None] = None,
        right: Union[str, LineStyle, None] = None,
        between_columns: Union[str, LineStyle, None] = None,
        between_rows: Union[str, LineStyle, None] = None,
    ) -> None:
        """Sets the style for table borders.

        Args:
            top (Union[str, LineStyle, None]):
                    Style for the top border.
                    Can be a string key for predefined styles or a LineStyle object.
            top2 (Union[str, LineStyle, None]):
                    Style for the secondary top border.
                    Can be a string key for predefined styles or a LineStyle object.
            bottom (Union[str, LineStyle, None]):
                    Style for the bottom border.
                    Can be a string key for predefined styles or a LineStyle object.
            left (Union[str, LineStyle, None]):
                    Style for the left border.
                    Can be a string key for predefined styles or a LineStyle object.
            left2 (Union[str, LineStyle, None]):
                    Style for the secondary left border.
                    Can be a string key for predefined styles or a LineStyle object.
            right (Union[str, LineStyle, None]):
                    Style for the right border.
                    Can be a string key for predefined styles or a LineStyle object.
            between_columns (Union[str, LineStyle, None]):
                    Style for borders between columns.
                    Can be a string key for predefined styles or a LineStyle object.
            between_rows (Union[str, LineStyle, None]):
                    Style for borders between rows.
                    Can be a string key for predefined styles or a LineStyle object.
        """
        if isinstance(top, str):
            self._bs_top = dtheme.linestyles.get(top)
        elif isinstance(top, LineStyle):
            self._bs_top = top.copy()

        if isinstance(top2, str):
            self._bs_top2 = dtheme.linestyles.get(top2)
        elif isinstance(top2, LineStyle):
            self._bs_top2 = top2.copy()

        if isinstance(bottom, str):
            self._bs_bottom = dtheme.linestyles.get(bottom)
        elif isinstance(bottom, LineStyle):
            self._bs_bottom = bottom.copy()

        if isinstance(left, str):
            self._bs_left = dtheme.linestyles.get(left)
        elif isinstance(left, LineStyle):
            self._bs_left = left.copy()

        if isinstance(left2, str):
            self._bs_left2 = dtheme.linestyles.get(left2)
        elif isinstance(left2, LineStyle):
            self._bs_left2 = left2.copy()

        if isinstance(right, str):
            self._bs_right = dtheme.linestyles.get(right)
        elif isinstance(right, LineStyle):
            self._bs_right = right.copy()

        if isinstance(between_columns, str):
            self._bs_between_columns = dtheme.linestyles.get(between_columns)
        elif isinstance(between_columns, LineStyle):
            self._bs_between_columns = between_columns.copy()

        if isinstance(between_rows, str):
            self._bs_between_rows = dtheme.linestyles.get(between_rows)
        elif isinstance(between_rows, LineStyle):
            self._bs_between_rows = between_rows.copy()

    # draw

    @error_handler
    def draw(
        self,
        xy: Tuple[float, float],
        width: float,
        height: float,
        data: List[List[Any]],
    ) -> None:
        """Draws the table with equal-sized cells.

        Args:
            xy (Tuple[float, float]): The coordinates where the table should be drawn.
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

    @error_handler
    def draw_flexible(
        self,
        xy: Tuple[float, float],
        column_widths: List[float],
        row_heights: List[float],
        data: List[List[Any]],
    ) -> None:
        """Draws the table with flexible cell sizes.

        Args:
            xy (Tuple[float, float]): The coordinates where the table should be drawn.
            column_widths (List[float]): A list of widths for each column.
            row_heights (List[float]): A list of heights for each row.
            data (List[List[Any]]): The data to be displayed in the table.
        """
        # create blank matrix
        default_textstyle = dtheme.shapetextstyles.get()
        matrix: List[List[_CellInfo]] = []
        for row_data in data:
            row: List[_CellInfo] = []
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
        xy: Tuple[float, float],
        column_widths: List[float],
        row_heights: List[float],
        matrix: List[List[_CellInfo]],
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
        matrix: List[List[_CellInfo]],
    ) -> None:
        def style_even_odd(
            even_background_color: Union[Tuple[int, int, int], Tuple[int, int, int, float]],
            even_textstyle: ShapeTextStyle,
            odd_background_color: Union[Tuple[int, int, int], Tuple[int, int, int, float]],
            odd_textstyle: ShapeTextStyle,
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
            background_color: Union[Tuple[int, int, int], Tuple[int, int, int, float]],
            textstyle: ShapeTextStyle,
            rows: Optional[List[int]],
            columns: Optional[List[int]],
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
        matrix: List[List[_CellInfo]],
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
                    style=ShapeStyle(
                        lwidth=0,
                        lcolor=Colors.Transparent,
                        fcolor=bg_color,
                    ),
                    text=text,
                    textstyle=textstyle,
                )

    def _draw_border_lines(  # noqa: C901
        self,
        xy: Tuple[float, float],
        column_widths: List[float],
        row_heights: List[float],
    ) -> None:
        bs_top1: Optional[LineStyle] = None
        if self._bs_top is not None:
            bs_top1 = self._bs_top
        elif self._bs_between_columns is not None:
            bs_top1 = self._bs_between_columns

        bs_top2: Optional[LineStyle] = None
        if self._bs_top2 is not None:
            bs_top2 = self._bs_top2
        elif self._bs_between_columns is not None:
            bs_top2 = self._bs_between_columns

        bs_bottom: Optional[LineStyle] = None
        if self._bs_bottom is not None:
            bs_bottom = self._bs_bottom
        elif self._bs_between_columns is not None:
            bs_bottom = self._bs_between_columns

        bs_left1: Optional[LineStyle] = None
        if self._bs_left is not None:
            bs_left1 = self._bs_left
        elif self._bs_between_rows is not None:
            bs_left1 = self._bs_between_rows

        bs_left2: Optional[LineStyle] = None
        if self._bs_left2 is not None:
            bs_left2 = self._bs_left2
        elif self._bs_between_rows is not None:
            bs_left2 = self._bs_between_rows

        bs_right: Optional[LineStyle] = None
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
