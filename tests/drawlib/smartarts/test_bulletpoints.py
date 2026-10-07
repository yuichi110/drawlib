# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for BulletPoints smart art."""

import pytest
from pydantic import ValidationError

from drawlib.canvas import clear, save
from drawlib.smartarts import BulletPoints
from drawlib.styles import Styles

default_styles = Styles
OUTPUT_DIR = "../../../output_tests/smartarts/bulletpoints/"


class TestBulletPoints:
    """Tests for the BulletPoints class drawing operations."""

    def test_bulletpoints_default(self) -> None:
        """Verify BulletPoints rendering with multi-level indents."""
        clear()
        styles = default_styles
        b = BulletPoints(text_style=styles.Black, vertical_margin=4, indent_width=4)
        b.add("level 0")
        b.set_indent(1)
        b.add("level 1-1")
        b.add("level 1-2")
        b.set_indent(2)
        b.add("level 2-1")
        b.add("level 2-2")
        b.set_indent(1)
        b.add("level 1-3")
        b.draw((10, 80))
        save(f"{OUTPUT_DIR}test_bulletpoints_default.png")

    def test_bulletpoints_japanese(self) -> None:
        """Verify BulletPoints rendering using Japanese text at multiple levels."""
        clear()
        styles = default_styles
        b = BulletPoints(text_style=styles.Black, vertical_margin=4, indent_width=4)
        b.add("レベル 0")
        b.set_indent(1)
        b.add("レベル 1-1")
        b.add("レベル 1-2")
        b.set_indent(2)
        b.add("レベル 2-1")
        b.add("レベル 2-2")
        b.set_indent(1)
        b.add("レベル 1-3")
        b.draw((10, 80))
        save(f"{OUTPUT_DIR}test_bulletpoints_japanese.png")

    def test_bulletpoints_missing_style_raises_error(self) -> None:
        """Verify that missing text_style raises ValidationError on __init__."""
        with pytest.raises(ValidationError):
            BulletPoints(vertical_margin=4, indent_width=4)  # type: ignore

    def test_bulletpoints_item_and_scale(self) -> None:
        """Verify BulletPointItem return, mutation, show flag, and scale parameter."""
        clear()
        styles = default_styles
        b = BulletPoints(text_style=styles.Black, vertical_margin=4, indent_width=4)
        item1 = b.add("Item 1")
        item2 = b.add("Item 2", show=False)
        item3 = b.add("Item 3")
        assert item1.text == "Item 1"
        assert item2.show is False
        item3.style = styles.PrimaryBold
        assert item3.text_style == styles.PrimaryBold
        b.draw((10, 80), scale=0.8)
        save(f"{OUTPUT_DIR}test_bulletpoints_scale.png")
