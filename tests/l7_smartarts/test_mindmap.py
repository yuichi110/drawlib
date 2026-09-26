# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and visual integration tests for MindMapNode smart art."""

from drawlib._core.l3_styles import Style
from drawlib.canvas import clear, save
from drawlib.preset_styles import default_styles
from drawlib.smartarts import MindMapNode

OUTPUT_DIR = "../../output_tests/l7_smartarts/mindmap/"


class TestMindMapNode:
    """Tests for MindMapNode class initialization, layout, and rendering."""

    def test_mindmap_initialization(self) -> None:
        """Verify initialization and default attributes."""
        node = MindMapNode(text="Center")
        assert node._text == "Center"
        assert node._shape is None
        assert node._size is None
        assert node._branch is None
        assert node._children == []

        child = MindMapNode("Child", shape="oval", branch="right", xy_shift=(2.0, 3.0))
        parent = MindMapNode("Parent", children=[child])
        assert len(parent._children) == 1
        assert parent._children[0]._shape == "oval"
        assert parent._children[0]._branch == "right"
        assert parent._children[0]._xy_shift == (2.0, 3.0)

    def test_mindmap_vertical_bottom(self) -> None:
        """Verify vertical bottom expansion (organizational hierarchy)."""
        clear()
        styles = default_styles
        root = MindMapNode(
            "CEO",
            shape="rectangle",
            size=(22.0, 8.0),
            style=styles.solid,
            default_size=(18.0, 7.0),
            default_style=styles.solid,
            children=[
                MindMapNode(
                    "CTO",
                    children=[
                        MindMapNode("Dev Team", shape="none"),
                        MindMapNode("QA Team", shape="none"),
                    ],
                ),
                MindMapNode(
                    "CFO",
                    children=[
                        MindMapNode("Accounting", shape="none"),
                    ],
                ),
            ],
        )
        root.draw(xy=(50.0, 85.0), branch="bottom", styles=styles)
        save(f"{OUTPUT_DIR}test_mindmap_bottom.png")

    def test_mindmap_vertical_top(self) -> None:
        """Verify vertical top expansion."""
        clear()
        styles = default_styles
        root = MindMapNode(
            "Root",
            shape="rectangle",
            size=(20.0, 8.0),
            children=[
                MindMapNode("Leaf A"),
                MindMapNode("Leaf B"),
            ],
        )
        root.draw(xy=(50.0, 20.0), branch="top", styles=styles)
        save(f"{OUTPUT_DIR}test_mindmap_top.png")

    def test_mindmap_horizontal_right(self) -> None:
        """Verify horizontal right expansion."""
        clear()
        styles = default_styles
        root = MindMapNode(
            "Topic",
            shape="oval",
            size=(20.0, 10.0),
            children=[
                MindMapNode("Sub 1", shape="rectangle"),
                MindMapNode("Sub 2", shape="none"),
            ],
        )
        root.draw(xy=(20.0, 50.0), branch="right", styles=styles)
        save(f"{OUTPUT_DIR}test_mindmap_right.png")

    def test_mindmap_horizontal_left(self) -> None:
        """Verify horizontal left expansion."""
        clear()
        styles = default_styles
        root = MindMapNode(
            "Topic",
            shape="oval",
            size=(20.0, 10.0),
            children=[
                MindMapNode("Sub 1", shape="rectangle"),
                MindMapNode("Sub 2", shape="none"),
            ],
        )
        root.draw(xy=(80.0, 50.0), branch="left", styles=styles)
        save(f"{OUTPUT_DIR}test_mindmap_left.png")

    def test_mindmap_multidirectional_mindmap(self) -> None:
        """Verify central topic branching into multiple directions (mind map)."""
        clear()
        styles = default_styles
        root = MindMapNode(
            "Main Concept",
            shape="oval",
            size=(26.0, 12.0),
            style=styles.bold,
            children=[
                # Right branch
                MindMapNode(
                    "Pros",
                    branch="right",
                    shape="rectangle",
                    style=styles.solid,
                    children=[
                        MindMapNode("Speed", shape="none"),
                        MindMapNode("Clarity", shape="none"),
                    ],
                ),
                # Left branch
                MindMapNode(
                    "Cons",
                    branch="left",
                    shape="rectangle",
                    style=styles.solid,
                    children=[
                        MindMapNode("Complexity", shape="none"),
                    ],
                ),
                # Top branch
                MindMapNode(
                    "Goals",
                    branch="top",
                    shape="rectangle",
                    style=styles.solid,
                ),
                # Bottom branch
                MindMapNode(
                    "Next Steps",
                    branch="bottom",
                    shape="rectangle",
                    style=styles.solid,
                    xy_shift=(0.0, -2.0),
                ),
            ],
        )
        root.draw(xy=(50.0, 50.0), styles=styles)
        save(f"{OUTPUT_DIR}test_mindmap_multi.png")
