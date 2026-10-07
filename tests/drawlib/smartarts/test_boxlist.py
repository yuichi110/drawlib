# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for BoxList smart art."""

import pytest
from pydantic import ValidationError

from drawlib.canvas import clear, save
from drawlib.smartarts import BoxList
from drawlib.styles import Styles

default_styles = Styles
OUTPUT_DIR = "../../../output_tests/smartarts/boxlist/"


class TestBoxList:
    """Tests for the BoxList class drawing operations."""

    def test_boxlist_default_horizontal_left(self) -> None:
        """Verify BoxList drawing with default horizontal alignment starting from left."""
        clear()
        styles = default_styles
        b = BoxList(style=styles.PrimarySolid, text_style=styles.PrimaryBold)
        b.add("1")
        b.add("2")
        b.add("3", style=styles.RedSolid, text_style=styles.RedBold)
        b.add("4")
        b.draw((10, 10), 8, 6)
        save(f"{OUTPUT_DIR}test_boxlist_left.png")

    def test_boxlist_horizontal_right(self) -> None:
        """Verify BoxList drawing with horizontal alignment starting from right."""
        clear()
        styles = default_styles
        b = BoxList(style=styles.PrimarySolid, text_style=styles.PrimaryBold)
        b.add("1")
        b.add("2")
        b.add("3", style=styles.RedSolid, text_style=styles.RedBold)
        b.add("4")
        b.draw((90, 10), 8, 6, "right")
        save(f"{OUTPUT_DIR}test_boxlist_right.png")

    def test_boxlist_vertical_bottom(self) -> None:
        """Verify BoxList drawing with vertical alignment starting from bottom."""
        clear()
        styles = default_styles
        b = BoxList(style=styles.PrimarySolid, text_style=styles.PrimaryBold)
        b.add("1")
        b.add("2")
        b.add("3", style=styles.RedSolid, text_style=styles.RedBold)
        b.add("4")
        b.draw((10, 10), 8, 6, "bottom")
        save(f"{OUTPUT_DIR}test_boxlist_bottom.png")

    def test_boxlist_vertical_top(self) -> None:
        """Verify BoxList drawing with vertical alignment starting from top."""
        clear()
        styles = default_styles
        b = BoxList(style=styles.PrimarySolid, text_style=styles.PrimaryBold)
        b.add("1")
        b.add("2")
        b.add("3", style=styles.RedSolid, text_style=styles.RedBold)
        b.add("4")
        b.draw((10, 90), 8, 6, "top")
        save(f"{OUTPUT_DIR}test_boxlist_top.png")

    def test_boxlist_item_operations(self) -> None:
        """Verify item manipulation methods (add, mutation, show, scale) work properly."""
        clear()
        styles = default_styles
        b = BoxList(style=styles.PrimarySolid, text_style=styles.PrimaryBold)
        item1 = b.add("item1")
        assert len(b._list) == 1
        assert item1.text == "item1"
        assert item1.show is True

        item2 = b.add("item2")
        item3 = b.add("item3", show=False)
        assert len(b._list) == 3
        assert item2.text == "item2"
        assert item3.show is False

        # Mutate item2 style post-add
        item2.style = styles.RedSolid
        item2.text_style = styles.RedBold
        b.draw((10, 10), 8, 6, scale=1.2)
        save(f"{OUTPUT_DIR}test_boxlist_mutation.png")

    def test_boxlist_missing_style_raises_error(self) -> None:
        """Verify that missing default styles raises ValidationError on __init__."""
        styles = default_styles
        with pytest.raises(ValidationError):
            BoxList()  # type: ignore

        with pytest.raises(ValidationError):
            BoxList(style=styles.PrimarySolid)  # type: ignore

        with pytest.raises(ValidationError):
            BoxList(text_style=styles.PrimaryBold)  # type: ignore
