# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for GridLayout smart art."""

from drawlib.canvas import clear, save
from drawlib.preset_styles import default_styles
from drawlib.smartarts import GridLayout

OUTPUT_DIR = "../../output_tests/l7_smartarts/gridlayout/"


class TestGridLayout:
    """Tests for the GridLayout class drawing operations."""

    def test_gridlayout_default(self) -> None:
        """Verify basic GridLayout item positioning and spanned cells."""
        clear()
        styles = default_styles
        gl = GridLayout(styles=styles, num_column=3, num_row=3, default_r=2, default_style=styles.solid)
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
        gl = GridLayout(styles=styles, num_column=3, num_row=3, default_r=2, default_style=styles.solid)
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
        gl = GridLayout(styles=styles, num_column=3, num_row=3, default_r=2, default_style=styles.solid)
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
        gl = GridLayout(styles=styles, num_column=3, num_row=3, default_r=2, default_style=styles.solid)
        gl.add((0, 0), 1, 1, text="A")
        gl.add((0, 1), 1, 1, text="B")
        gl.add((0, 2), 1, 1, text="C")
        gl.add((1, 0), 1, 3, text="D")
        gl.add((2, 0), 1, 1, text="E")
        gl.draw((10, 10), 30, 30, 1, outer_style=styles.solid)
        gl.draw((60, 10), 30, 30, 1, outer_r=0, outer_style=styles.solid)
        save(f"{OUTPUT_DIR}test_gridlayout_outerstyle.png")
