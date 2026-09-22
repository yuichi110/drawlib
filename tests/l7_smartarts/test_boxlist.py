# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for BoxList smart art."""

from drawlib.canvas import clear, save
from drawlib.smartarts import BoxList

OUTPUT_DIR = "../../output_tests/l7_smartarts/boxlist/"


class TestBoxList:
    """Tests for the BoxList class drawing operations."""

    def test_boxlist_default_horizontal_left(self) -> None:
        """Verify BoxList drawing with default horizontal alignment starting from left."""
        clear()
        b = BoxList("solid", "")
        b.extend(["1", "2"])
        b.append("3", "red_solid_bold", "red_bold")
        b.append("4")
        b.draw((10, 10), 8, 6)
        save(f"{OUTPUT_DIR}test_boxlist_left.png")

    def test_boxlist_horizontal_right(self) -> None:
        """Verify BoxList drawing with horizontal alignment starting from right."""
        clear()
        b = BoxList("solid", "")
        b.extend(["1", "2"])
        b.append("3", "red_solid_bold", "red_bold")
        b.append("4")
        b.draw((90, 10), 8, 6, "right")
        save(f"{OUTPUT_DIR}test_boxlist_right.png")

    def test_boxlist_vertical_bottom(self) -> None:
        """Verify BoxList drawing with vertical alignment starting from bottom."""
        clear()
        b = BoxList("solid", "")
        b.extend(["1", "2"])
        b.append("3", "red_solid_bold", "red_bold")
        b.append("4")
        b.draw((10, 10), 8, 6, "bottom")
        save(f"{OUTPUT_DIR}test_boxlist_bottom.png")

    def test_boxlist_vertical_top(self) -> None:
        """Verify BoxList drawing with vertical alignment starting from top."""
        clear()
        b = BoxList("solid", "")
        b.extend(["1", "2"])
        b.append("3", "red_solid_bold", "red_bold")
        b.append("4")
        b.draw((10, 90), 8, 6, "top")
        save(f"{OUTPUT_DIR}test_boxlist_top.png")

    def test_boxlist_item_operations(self) -> None:
        """Verify item manipulation methods (append, insert, extend) work properly."""
        b = BoxList()
        b.append("item1")
        assert len(b._list) == 1
        assert b._list[0].text == "item1"
        assert not b._list[0].is_custom_style

        b.extend(["item2", "item3"])
        assert len(b._list) == 3
        assert b._list[1].text == "item2"
        assert b._list[2].text == "item3"

        b.insert(1, "inserted", box_style="red")
        assert len(b._list) == 4
        assert b._list[1].text == "inserted"
        assert b._list[1].is_custom_style
        assert b._list[2].text == "item2"
        assert b._list[3].text == "item3"
