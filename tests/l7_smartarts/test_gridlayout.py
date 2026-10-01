# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for GridLayout smart art."""

import pytest

from drawlib.canvas import clear, save
from drawlib.smartarts import GridLayout
from drawlib.styles import Styles

default_styles = Styles
OUTPUT_DIR = "../../output_tests/l7_smartarts/gridlayout/"


class TestGridLayout:
    """Tests for the GridLayout class drawing operations."""

    def test_gridlayout_default(self) -> None:
        """Verify basic GridLayout item positioning and spanned cells."""
        clear()
        styles = default_styles
        gl = GridLayout(
            num_column=3,
            num_row=3,
            default_r=2,
            default_style=styles.PrimarySolid,
            default_textstyle=styles.PrimaryBold,
        )
        gl.add((0, 0), 1, 1, text="A")
        gl.add((0, 1), 1, 1, text="B")
        gl.add((0, 2), 1, 1, text="C")
        gl.add((1, 0), 1, 3, text="D")
        gl.add((2, 0), 1, 1, text="E")
        gl.draw((10, 10), 30, 30, 1)
        save(f"{OUTPUT_DIR}test_gridlayout_default.png")

    def test_gridlayout_text_angle(self) -> None:
        """Verify GridLayout cells containing rotated text."""
        clear()
        styles = default_styles
        gl = GridLayout(
            num_column=3,
            num_row=3,
            default_r=2,
            default_style=styles.PrimarySolid,
            default_textstyle=styles.PrimaryBold,
        )
        gl.add((0, 0), 1, 1, text="A", textangle=270)
        gl.add((0, 1), 1, 1, text="B", textangle=90)
        gl.add((0, 2), 1, 1, text="C")
        gl.add((1, 0), 1, 3, text="D")
        gl.add((2, 0), 1, 1, text="E")
        gl.draw((10, 10), 30, 30, 1)
        save(f"{OUTPUT_DIR}test_gridlayout_angle.png")

    def test_gridlayout_text_shift(self) -> None:
        """Verify GridLayout cells containing offset/shifted text positions."""
        clear()
        styles = default_styles
        gl = GridLayout(
            num_column=3,
            num_row=3,
            default_r=2,
            default_style=styles.PrimarySolid,
            default_textstyle=styles.PrimaryBold,
        )
        gl.add((0, 0), 1, 1, text="A", text_xy_shift=(3, 3))
        gl.add((0, 1), 1, 1, text="B", text_xy_shift=(-3, -3))
        gl.add((0, 2), 1, 1, text="C")
        gl.add((1, 0), 1, 3, text="D")
        gl.add((2, 0), 1, 1, text="E")
        gl.draw((10, 10), 30, 30, 1)
        save(f"{OUTPUT_DIR}test_gridlayout_shift.png")

    def test_gridlayout_outer_style(self) -> None:
        """Verify GridLayout drawing with solid/rounded outer frame styles."""
        clear()
        styles = default_styles
        gl = GridLayout(
            num_column=3,
            num_row=3,
            default_r=2,
            default_style=styles.PrimarySolid,
            default_textstyle=styles.PrimaryBold,
        )
        gl.add((0, 0), 1, 1, text="A")
        gl.add((0, 1), 1, 1, text="B")
        gl.add((0, 2), 1, 1, text="C")
        gl.add((1, 0), 1, 3, text="D")
        gl.add((2, 0), 1, 1, text="E")
        gl.draw((10, 10), 30, 30, 1, outer_style=styles.PrimarySolid)
        gl.draw((60, 10), 30, 30, 1, outer_r=0, outer_style=styles.PrimarySolid)
        save(f"{OUTPUT_DIR}test_gridlayout_outerstyle.png")

    def test_gridlayout_missing_style_raises_error(self) -> None:
        """Verify that missing default_style or default_textstyle raises ValueError on add."""
        gl_no_style = GridLayout(num_column=2, num_row=2)
        with pytest.raises(ValueError, match="Neither 'default_style' nor 'style' was provided"):
            gl_no_style.add((0, 0), 1, 1)

        styles = default_styles
        gl_no_textstyle = GridLayout(num_column=2, num_row=2, default_style=styles.PrimarySolid)
        with pytest.raises(ValueError, match="Neither 'default_textstyle' nor 'textstyle' was provided"):
            gl_no_textstyle.add((0, 0), 1, 1, text="Test")
