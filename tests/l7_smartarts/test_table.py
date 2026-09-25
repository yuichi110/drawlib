# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for Table smart art rendering."""

from drawlib.canvas import clear, save
from drawlib.colors import Colors
from drawlib.preset_styles import get_default_styles
from drawlib.smartarts import Table

OUTPUT_DIR = "../../output_tests/l7_smartarts/table/"


class TestTable:
    """Tests for the Table class drawing and styling operations."""

    def test_table_default(self) -> None:
        """Verify basic Table drawing with standard grid layout."""
        clear()
        styles = get_default_styles()
        t = Table(styles=styles)
        t.draw((10, 85), 30, 20, data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        save(f"{OUTPUT_DIR}test_table_default.png")

    def test_table_predefined_style_default(self) -> None:
        """Verify Table drawing with predefined 'default' styling."""
        clear()
        styles = get_default_styles()
        t = Table(styles=styles)
        t.set_predefined_style("default")
        t.draw((10, 85), 30, 20, data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        save(f"{OUTPUT_DIR}test_table_predefined_default.png")

    def test_table_predefined_style_monochrome(self) -> None:
        """Verify Table drawing with predefined 'monochrome' styling."""
        clear()
        styles = get_default_styles()
        t = Table(styles=styles)
        t.set_predefined_style("monochrome")
        t.draw((10, 85), 30, 20, data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        save(f"{OUTPUT_DIR}test_table_predefined_monochrome.png")

    def test_table_predefined_style_border_simple(self) -> None:
        """Verify Table drawing with predefined 'border_simple' styling."""
        clear()
        styles = get_default_styles()
        t = Table(styles=styles)
        t.set_predefined_style("border_simple")
        t.draw((10, 85), 30, 20, data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        save(f"{OUTPUT_DIR}test_table_predefined_border_simple.png")

    def test_table_predefined_style_none(self) -> None:
        """Verify Table drawing with predefined 'none' styling."""
        clear()
        styles = get_default_styles()
        t = Table(styles=styles)
        t.set_predefined_style("none")
        t.draw((10, 85), 30, 20, data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        save(f"{OUTPUT_DIR}test_table_predefined_none.png")

    def test_table_custom_styles(self) -> None:
        """Verify Table drawing with even-odd cell background coloring and custom borders."""
        clear()
        styles = get_default_styles()
        t = Table(styles=styles)
        t.clear_styles()
        t.set_style_cell_evenodd(
            even_color=Colors.Gray,
            even_textstyle=styles.white,
            odd_color=Colors.White,
            odd_textstyle=styles.black,
        )
        t.set_style_border(top=styles.black, top2=styles.black_light, bottom=styles.black)
        t.draw((10, 85), 30, 20, data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        save(f"{OUTPUT_DIR}test_table_custom_style.png")
