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
from pydantic import ValidationError

from drawlib.canvas import clear, save
from drawlib.smartarts import GridLayout
from drawlib.styles import Styles

default_styles = Styles
OUTPUT_DIR = "../../../output_tests/smartarts/gridlayout/"


class TestGridLayout:
    """Tests for the GridLayout class drawing operations."""

    def test_gridlayout_default(self) -> None:
        """Verify basic GridLayout item positioning and spanned cells."""
        clear()
        styles = default_styles
        gl = GridLayout(
            num_column=3,
            num_row=3,
            style=styles.PrimarySolid.patch(shape_r=2),
            text_style=styles.PrimaryBold,
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
            style=styles.PrimarySolid.patch(shape_r=2),
            text_style=styles.PrimaryBold,
        )
        gl.add((0, 0), 1, 1, text="A", text_style=styles.PrimaryBold.patch(angle=270))
        gl.add((0, 1), 1, 1, text="B", text_style=styles.PrimaryBold.patch(angle=90))
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
            style=styles.PrimarySolid.patch(shape_r=2),
            text_style=styles.PrimaryBold,
        )
        gl.add((0, 0), 1, 1, text="A", text_style=styles.PrimaryBold.patch(xy_shift=(3, 3)))
        gl.add((0, 1), 1, 1, text="B", text_style=styles.PrimaryBold.patch(xy_shift=(-3, -3)))
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
            style=styles.PrimarySolid.patch(shape_r=2),
            text_style=styles.PrimaryBold,
        )
        gl.add((0, 0), 1, 1, text="A")
        gl.add((0, 1), 1, 1, text="B")
        gl.add((0, 2), 1, 1, text="C")
        gl.add((1, 0), 1, 3, text="D")
        gl.add((2, 0), 1, 1, text="E")
        gl.draw((10, 10), 30, 30, 1, outer_style=styles.PrimarySolid.patch(shape_r=2))
        gl.draw((60, 10), 30, 30, 1, outer_style=styles.PrimarySolid)
        save(f"{OUTPUT_DIR}test_gridlayout_outerstyle.png")

    def test_gridlayout_missing_style_raises_error(self) -> None:
        """Verify that missing default styles raises ValidationError on __init__."""
        styles = default_styles
        with pytest.raises(ValidationError):
            GridLayout(num_column=2, num_row=2)  # type: ignore

        with pytest.raises(ValidationError):
            GridLayout(num_column=2, num_row=2, style=styles.PrimarySolid)  # type: ignore

        with pytest.raises(ValidationError):
            GridLayout(num_column=2, num_row=2, text_style=styles.PrimaryBold)  # type: ignore

    def test_gridlayout_item_and_scale(self) -> None:
        """Verify GridItem return, mutation, show flag, and scale parameter."""
        clear()
        styles = default_styles
        gl = GridLayout(
            num_column=2,
            num_row=2,
            style=styles.PrimarySolid.patch(shape_r=2),
            text_style=styles.PrimaryBold,
        )
        item_a = gl.add((0, 0), 1, 1, text="A")
        item_b = gl.add((0, 1), 1, 1, text="B", show=False)
        item_a.style = styles.SecondarySolid
        assert len(gl.items) == 2
        assert item_a.text == "A"
        assert item_b.show is False
        gl.draw((10, 10), 30, 30, 1, scale=0.8)
        save(f"{OUTPUT_DIR}test_gridlayout_scale.png")
