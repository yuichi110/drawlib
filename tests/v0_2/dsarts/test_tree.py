# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_2.apis import *

OUTPUT_DIR = "../../../output_tests/v0_2/dsarts/tree/"


def test():
    dtheme.apply_official_theme("essentials")
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
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_icon():
    tn = dsart.TreeNode
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
                    ).set_drawing_item(
                        location="before",
                        padding_width=5,
                        function=icon_phosphor.file_py,
                        style=dtheme.iconstyles.get(),
                        args={"width": 4},
                    ),
                    tn("Child1-2"),
                ],
            ),
            tn(
                "Child2",
                children=[
                    tn("Child2-1").set_drawing_item(
                        location="after",
                        padding_width=10,
                        function=icon_phosphor.file_py,
                        style=dtheme.iconstyles.get(),
                        args={"width": 4},
                    ),
                    tn("Child2-2"),
                ],
            ),
        ],
    )

    t.draw((10, 80))
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
