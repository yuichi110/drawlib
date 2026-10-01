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

from drawlib.canvas import clear, save
from drawlib.smartarts import BoxList
from drawlib.styles import Styles

default_styles = Styles
OUTPUT_DIR = "../../output_tests/l7_smartarts/boxlist/"


class TestBoxList:
    """Tests for the BoxList class drawing operations."""

    def test_boxlist_default_horizontal_left(self) -> None:
        """Verify BoxList drawing with default horizontal alignment starting from left."""
        clear()
        styles = default_styles
        b = BoxList(default_box_style=styles.PrimarySolid, default_text_style=styles.PrimaryBold)
        b.extend(["1", "2"])
        b.append("3", box_style=styles.RedSolid, text_style=styles.RedBold)
        b.append("4")
        b.draw((10, 10), 8, 6)
        save(f"{OUTPUT_DIR}test_boxlist_left.png")

    def test_boxlist_horizontal_right(self) -> None:
        """Verify BoxList drawing with horizontal alignment starting from right."""
        clear()
        styles = default_styles
        b = BoxList(default_box_style=styles.PrimarySolid, default_text_style=styles.PrimaryBold)
        b.extend(["1", "2"])
        b.append("3", box_style=styles.RedSolid, text_style=styles.RedBold)
        b.append("4")
        b.draw((90, 10), 8, 6, "right")
        save(f"{OUTPUT_DIR}test_boxlist_right.png")

    def test_boxlist_vertical_bottom(self) -> None:
        """Verify BoxList drawing with vertical alignment starting from bottom."""
        clear()
        styles = default_styles
        b = BoxList(default_box_style=styles.PrimarySolid, default_text_style=styles.PrimaryBold)
        b.extend(["1", "2"])
        b.append("3", box_style=styles.RedSolid, text_style=styles.RedBold)
        b.append("4")
        b.draw((10, 10), 8, 6, "bottom")
        save(f"{OUTPUT_DIR}test_boxlist_bottom.png")

    def test_boxlist_vertical_top(self) -> None:
        """Verify BoxList drawing with vertical alignment starting from top."""
        clear()
        styles = default_styles
        b = BoxList(default_box_style=styles.PrimarySolid, default_text_style=styles.PrimaryBold)
        b.extend(["1", "2"])
        b.append("3", box_style=styles.RedSolid, text_style=styles.RedBold)
        b.append("4")
        b.draw((10, 90), 8, 6, "top")
        save(f"{OUTPUT_DIR}test_boxlist_top.png")

    def test_boxlist_item_operations(self) -> None:
        """Verify item manipulation methods (append, insert, extend) work properly."""
        styles = default_styles
        b = BoxList(default_box_style=styles.PrimarySolid, default_text_style=styles.PrimaryBold)
        b.append("item1")
        assert len(b._list) == 1
        assert b._list[0].text == "item1"
        assert not b._list[0].is_custom_style

        b.extend(["item2", "item3"])
        assert len(b._list) == 3
        assert b._list[1].text == "item2"
        assert b._list[2].text == "item3"

        b.insert(1, "inserted", box_style=styles.RedSolid, text_style=styles.RedBold)
        assert len(b._list) == 4
        assert b._list[1].text == "inserted"
        assert b._list[1].is_custom_style
        assert b._list[2].text == "item2"
        assert b._list[3].text == "item3"

    def test_boxlist_missing_style_raises_error(self) -> None:
        """Verify that missing both default and item styles raises ValueError."""
        styles = default_styles
        b_empty = BoxList()
        with pytest.raises(ValueError, match="Neither 'default_box_style' nor 'box_style' was provided"):
            b_empty.append("item1")

        b_no_text = BoxList(default_box_style=styles.PrimarySolid)
        with pytest.raises(ValueError, match="Neither 'default_text_style' nor 'text_style' was provided"):
            b_no_text.append("item1")
