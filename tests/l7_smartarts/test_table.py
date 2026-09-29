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

from drawlib.canvas import clear, save
from drawlib.smartarts import Table
from drawlib.styles import Colors, Styles

default_styles = Styles
OUTPUT_DIR = "../../output_tests/l7_smartarts/table/"


class TestTable:
    """Tests for the Table class drawing and styling operations."""

    def test_table_no_style_raises_error(self) -> None:
        """Verify Table drawing without styles raises ValueError."""
        clear()
        t = Table()
        with pytest.raises(ValueError, match="No text style provided for cell"):
            t.draw((10, 85), 30, 20, data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    def test_table_default(self) -> None:
        """Verify basic Table drawing with minimal styles."""
        clear()
        styles = default_styles
        t = Table(
            default_text_style=styles.black,
            border_style=styles.solid,
        )
        t.draw((10, 85), 30, 20, data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        save(f"{OUTPUT_DIR}test_table_default.png")

    def test_table_style_cell_headers(self) -> None:
        """Verify Table drawing with custom cell headers."""
        clear()
        styles = default_styles
        t = Table(default_text_style=styles.black)
        t.set_style_cell_headers((220, 230, 245), styles.bold)
        t.set_style_border(top=styles.solid, bottom=styles.solid)
        t.draw((10, 85), 30, 20, data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        save(f"{OUTPUT_DIR}test_table_headers.png")

    def test_table_style_cell_evenodd(self) -> None:
        """Verify Table drawing with even-odd cell styling."""
        clear()
        styles = default_styles
        t = Table()
        t.set_style_cell_evenodd(
            even_color=Colors.Gray3,
            even_textstyle=styles.white,
            odd_color=Colors.White,
            odd_textstyle=styles.black,
        )
        t.set_style_border(bottom=styles.solid)
        t.draw((10, 85), 30, 20, data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        save(f"{OUTPUT_DIR}test_table_evenodd.png")

    def test_table_clear_styles_raises_error(self) -> None:
        """Verify Table clear_styles resets styles and causes draw to raise ValueError."""
        clear()
        styles = default_styles
        t = Table(default_text_style=styles.black)
        t.clear_styles()
        with pytest.raises(ValueError, match="No text style provided for cell"):
            t.draw((10, 85), 30, 20, data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    def test_table_custom_styles(self) -> None:
        """Verify Table drawing with even-odd cell background coloring and custom borders."""
        clear()
        styles = default_styles
        t = Table()
        t.clear_styles()
        t.set_style_cell_evenodd(
            even_color=Colors.Gray3,
            even_textstyle=styles.white,
            odd_color=Colors.White,
            odd_textstyle=styles.black,
        )
        t.set_style_border(top=styles.black, top2=styles.black_light, bottom=styles.black)
        t.draw((10, 85), 30, 20, data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        save(f"{OUTPUT_DIR}test_table_custom_style.png")

    def test_table_with_init_styles(self) -> None:
        """Verify Table initialized with purpose-specific styles."""
        clear()
        styles = default_styles
        t = Table(
            default_cell_style=styles.solid,
            default_text_style=styles.black,
            header_cell_style=styles.blue_solid,
            header_text_style=styles.white_bold,
            border_style=styles.solid,
        )
        t.draw((10, 85), 30, 20, data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])
