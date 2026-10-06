# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for Table smart art rendering."""

import pytest
from pydantic import ValidationError

from drawlib.canvas import clear, save
from drawlib.smartarts import Table
from drawlib.styles import Colors, Styles

default_styles = Styles
OUTPUT_DIR = "../../../output_tests/smartarts/table/"


class TestTable:
    """Tests for the Table class drawing and styling operations."""

    def test_table_missing_styles_raises_error(self) -> None:
        """Verify Table initialization without mandatory styles raises ValidationError."""
        with pytest.raises(ValidationError):
            Table()  # type: ignore

    def test_table_default(self) -> None:
        """Verify basic Table drawing with standard styles."""
        clear()
        styles = default_styles
        t = Table(
            cell_style=styles.White,
            text_style=styles.Black,
            header_cell_style=styles.PrimarySolid,
            header_text_style=styles.WhiteBold,
            border_style=styles.PrimarySolid,
        )
        t.draw((10, 85), 30, 20, data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        save(f"{OUTPUT_DIR}test_table_default.png")

    def test_table_style_cell_headers(self) -> None:
        """Verify Table drawing with custom cell headers."""
        clear()
        styles = default_styles
        t = Table(
            cell_style=styles.White,
            text_style=styles.Black,
            header_cell_style=styles.White,
            header_text_style=styles.Black,
            border_style=styles.PrimarySolid,
            has_header=False,
        )
        t.set_style_cell_headers((220, 230, 245), styles.PrimaryBold)
        t.set_style_border(top=styles.PrimarySolid, bottom=styles.PrimarySolid)
        t.draw((10, 85), 30, 20, data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        save(f"{OUTPUT_DIR}test_table_headers.png")

    def test_table_style_cell_evenodd(self) -> None:
        """Verify Table drawing with even-odd cell styling."""
        clear()
        styles = default_styles
        t = Table(
            cell_style=styles.White,
            text_style=styles.Black,
            header_cell_style=styles.PrimarySolid,
            header_text_style=styles.WhiteBold,
            border_style=styles.PrimarySolid,
        )
        t.set_style_cell_evenodd(
            even_color=Colors.Gray3,
            even_text_style=styles.White,
            odd_color=Colors.White,
            odd_text_style=styles.Black,
        )
        t.set_style_border(bottom=styles.PrimarySolid)
        t.draw((10, 85), 30, 20, data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        save(f"{OUTPUT_DIR}test_table_evenodd.png")

    def test_table_reset_styles(self) -> None:
        """Verify Table reset_styles resets custom styles to initial table settings."""
        clear()
        styles = default_styles
        t = Table(
            cell_style=styles.White,
            text_style=styles.Black,
            header_cell_style=styles.PrimarySolid,
            header_text_style=styles.WhiteBold,
            border_style=styles.PrimarySolid,
        )
        initial_order_count = len(t._cell_style_orders)
        t.set_style_cell_evenodd(
            even_color=Colors.Gray3,
            even_text_style=styles.White,
            odd_color=Colors.White,
            odd_text_style=styles.Black,
        )
        assert len(t._cell_style_orders) > initial_order_count
        t.reset_styles()
        assert len(t._cell_style_orders) == initial_order_count

    def test_table_custom_styles(self) -> None:
        """Verify Table drawing with even-odd cell background coloring and custom borders."""
        clear()
        styles = default_styles
        t = Table(
            cell_style=styles.White,
            text_style=styles.Black,
            header_cell_style=styles.PrimarySolid,
            header_text_style=styles.WhiteBold,
            border_style=styles.PrimarySolid,
        )
        t.reset_styles()
        t.set_style_cell_evenodd(
            even_color=Colors.Gray3,
            even_text_style=styles.White,
            odd_color=Colors.White,
            odd_text_style=styles.Black,
        )
        t.set_style_border(top=styles.Black, top2=styles.BlackThin, bottom=styles.Black)
        t.draw((10, 85), 30, 20, data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        save(f"{OUTPUT_DIR}test_table_custom_style.png")

    def test_table_with_init_styles(self) -> None:
        """Verify Table initialized with purpose-specific styles."""
        clear()
        styles = default_styles
        t = Table(
            cell_style=styles.PrimarySolid,
            text_style=styles.Black,
            header_cell_style=styles.BlueSolid,
            header_text_style=styles.WhiteBold,
            border_style=styles.PrimarySolid,
        )
        t.draw((10, 85), 30, 20, data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])
