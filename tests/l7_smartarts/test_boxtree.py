# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for the BoxTreeNode class."""

from drawlib._core.l3_styles import Style
from drawlib._smartarts._boxtree import BoxTreeNode
from drawlib.preset_styles import default_styles


class TestBoxTreeNode:
    """Tests for the BoxTreeNode class constructor and methods."""

    def test_boxtreenode_initialization_defaults(self) -> None:
        """Verify that BoxTreeNode initializes correctly with minimal/default arguments."""
        node = BoxTreeNode(text="Root")
        assert node._text == "Root"
        assert node._boxsize is None
        assert node._boxstyle is None
        assert node._box_r is None
        assert node._box_horizontal_margin is None
        assert node._box_vertical_margin is None
        assert node._textstyle is None
        assert node._linestyle is None
        assert node._children == []

    def test_boxtreenode_initialization_custom(self) -> None:
        """Verify that BoxTreeNode parses custom styling and size structures correctly."""
        box_style = Style(shape_fill_color=(255, 0, 0, 1.0))
        text_style = Style(text_color=(0, 255, 0, 1.0), text_size=12)
        line_style = Style(line_color=(0, 0, 255, 1.0), line_width=2.0)
        child1 = BoxTreeNode(text="Child1")
        child2 = BoxTreeNode(text="Child2")

        node = BoxTreeNode(
            text="Root",
            boxsize=(10.0, 5.0),
            boxstyle=box_style,
            box_r=1.0,
            box_horizontal_margin=0.5,
            box_vertical_margin=0.5,
            textstyle=text_style,
            linestyle=line_style,
            line_horizontal_length=3.0,
            line_vertical_length=4.0,
            children=[child1, child2],
        )

        assert node._text == "Root"
        assert node._boxsize == (10.0, 5.0)
        assert node._boxstyle == box_style
        assert node._box_r == 1.0
        assert node._box_horizontal_margin == 0.5
        assert node._box_vertical_margin == 0.5
        assert node._textstyle == text_style
        assert node._linestyle == line_style
        assert node._line_horizontal_length == 3.0
        assert node._line_vertical_length == 4.0
        assert len(node._children) == 2
        assert node._children[0] == child1
        assert node._children[1] == child2

    def test_boxtreenode_draw_stub(self) -> None:
        """Verify calling the draw stub executes without crash/exceptions."""
        styles = default_styles
        node = BoxTreeNode(text="Root")
        # Call draw with different parameters
        node.draw(xy=(10, 10), styles=styles, orientation="horizontal", align="center")
        node.draw(xy=(20, 20), styles=styles, orientation="vertical", align="left")
