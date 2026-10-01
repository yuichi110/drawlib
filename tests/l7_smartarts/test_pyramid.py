# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for Pyramid smart art."""

import pytest

from drawlib.canvas import clear, save
from drawlib.smartarts import Pyramid
from drawlib.styles import Styles

default_styles = Styles
OUTPUT_DIR = "../../output_tests/l7_smartarts/pyramid/"


class TestPyramid:
    """Tests for the Pyramid class drawing operations."""

    def test_pyramid_default(self) -> None:
        """Verify basic Pyramid drawing with default vertex order and reversed base-to-vertex order."""
        clear()
        styles = default_styles
        p = Pyramid(default_style=styles.PrimarySolid, default_textstyle=styles.PrimaryBold)
        p.add(text="Hello")
        p.add(text="World")
        p.add(text="A")
        p.draw((10, 10), 30, 30, 2)
        p.draw((60, 10), 30, 30, 2, order="base_to_vertex")
        save(f"{OUTPUT_DIR}test_pyramid_default.png")

    def test_pyramid_align_bottom(self) -> None:
        """Verify Pyramid drawing aligned bottom."""
        clear()
        styles = default_styles
        p = Pyramid(default_style=styles.PrimarySolid, default_textstyle=styles.PrimaryBold)
        p.add(text="Hello")
        p.add(text="World")
        p.add(text="A")
        p.draw((10, 10), 30, 30, 2, align="bottom")
        p.draw((60, 10), 30, 30, 2, align="bottom", order="base_to_vertex")
        save(f"{OUTPUT_DIR}test_pyramid_align_bottom.png")

    def test_pyramid_align_top(self) -> None:
        """Verify Pyramid drawing aligned top."""
        clear()
        styles = default_styles
        p = Pyramid(default_style=styles.PrimarySolid, default_textstyle=styles.PrimaryBold)
        p.add(text="Hello")
        p.add(text="World")
        p.add(text="A")
        p.draw((10, 10), 30, 30, 2, align="top")
        p.draw((60, 10), 30, 30, 2, align="top", order="base_to_vertex")
        save(f"{OUTPUT_DIR}test_pyramid_align_top.png")

    def test_pyramid_align_left(self) -> None:
        """Verify Pyramid drawing aligned left."""
        clear()
        styles = default_styles
        p = Pyramid(default_style=styles.PrimarySolid, default_textstyle=styles.PrimaryBold)
        p.add(text="Hello")
        p.add(text="World")
        p.add(text="A")
        p.draw((10, 10), 30, 30, 2, align="left")
        p.draw((60, 10), 30, 30, 2, align="left", order="base_to_vertex")
        save(f"{OUTPUT_DIR}test_pyramid_align_left.png")

    def test_pyramid_align_right(self) -> None:
        """Verify Pyramid drawing aligned right."""
        clear()
        styles = default_styles
        p = Pyramid(default_style=styles.PrimarySolid, default_textstyle=styles.PrimaryBold)
        p.add(text="Hello")
        p.add(text="World")
        p.add(text="A")
        p.draw((10, 10), 30, 30, 2, align="right")
        p.draw((60, 10), 30, 30, 2, align="right", order="base_to_vertex")
        save(f"{OUTPUT_DIR}test_pyramid_align_right.png")

    def test_pyramid_missing_style_raises_error(self) -> None:
        """Verify that missing default_style or default_textstyle raises ValueError on add."""
        p_no_style = Pyramid()
        with pytest.raises(ValueError, match="Neither 'default_style' nor 'style' was provided"):
            p_no_style.add(text="Hello")

        styles = default_styles
        p_no_textstyle = Pyramid(default_style=styles.PrimarySolid)
        with pytest.raises(ValueError, match="Neither 'default_textstyle' nor 'textstyle' was provided"):
            p_no_textstyle.add(text="Hello")
