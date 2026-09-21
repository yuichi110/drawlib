# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for TreeNode smart art hierarchical rendering."""

from drawlib._theme import get_style
from drawlib.canvas import clear, save
from drawlib.icons import phosphor
from drawlib.smartarts import dsart

OUTPUT_DIR = "../../output_tests/l7_smartarts/tree/"


class TestTree:
    """Tests for the TreeNode class hierarchical drawing and custom decorators."""

    def test_tree_default(self) -> None:
        """Verify standard TreeNode hierarchy rendering with custom styled child nodes."""
        clear()
        tn = dsart.TreeNode
        t = tn(
            "Root",
            default_textstyle="",
            default_linestyle="light",
            default_line_horizontal_margin=2,
            default_line_horizontal_length=2,
            default_line_vertical_margin=5,
            children=[
                tn(
                    "Child1",
                    children=[
                        tn(
                            "Child1-1",
                            children=[
                                tn("Child1-1-1"),
                            ],
                        ),
                        tn("Child1-2", textstyle="red"),
                    ],
                ),
                tn(
                    text="Child2",
                    default_textstyle="blue",
                    children=[
                        tn("Child2-1"),
                        tn("Child2-2"),
                    ],
                ),
            ],
        )

        t.draw((10, 80))
        save(f"{OUTPUT_DIR}test_tree_default.png")

    def test_tree_with_icon_item_decorators(self) -> None:
        """Verify TreeNode hierarchy rendering including registered icon drawing decorators."""
        clear()
        tn = dsart.TreeNode
        tn.register_drawing_item(
            name="py_file",
            location="before",
            padding_width=5,
            function=phosphor.file_py,
            style=get_style(),
            args={"width": 4},
        )

        t = tn(
            "Root",
            default_textstyle="",
            default_linestyle="",
            default_line_horizontal_margin=2,
            default_line_horizontal_length=2,
            default_line_vertical_margin=5,
            children=[
                tn(
                    "Child1",
                    children=[
                        tn(
                            "Child1-1",
                        ).set_drawing_item("py_file"),
                        tn("Child1-2"),
                    ],
                ),
                tn(
                    "Child2",
                    children=[
                        tn("Child2-1").set_drawing_item("py_file"),
                        tn("Child2-2"),
                    ],
                ),
            ],
        )

        t.draw((10, 80))
        save(f"{OUTPUT_DIR}test_tree_icon.png")
