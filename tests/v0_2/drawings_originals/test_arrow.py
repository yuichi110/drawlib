# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_2.apis import *

OUTPUT_DIR = "../../../output_tests/v0_2/drawings_originals/arrow/"


def test_right_arrow():
    arrow(
        (10, 10),
        (80, 60),
        tail_width=10,
        head_width=30,
        head_length=10,
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_right_arrow_style():
    arrow(
        (10, 10),
        (80, 60),
        tail_width=10,
        head_width=30,
        head_length=10,
        style=ShapeStyle(
            lcolor=Colors.Red,
            fcolor=Colors.Transparent,
            lwidth=5,
            lstyle="dotted",
        ),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_right_arrow_text():
    arrow(
        (10, 10),
        (80, 60),
        tail_width=10,
        head_width=30,
        head_length=10,
        text="Hello Drawlib",
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_right_arrow_text_flip():
    arrow(
        (80, 60),
        (10, 10),
        tail_width=10,
        head_width=30,
        head_length=10,
        text="Hello Drawlib",
        textstyle=ShapeTextStyle(flip=True),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_left_arrow():
    arrow(
        (10, 10),
        (80, 60),
        tail_width=10,
        head_width=30,
        head_length=10,
        head="<-",
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_duble_arrow():
    arrow(
        (10, 10),
        (80, 60),
        tail_width=10,
        head_width=30,
        head_length=10,
        head="<->",
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_arrow_text_shift():
    arrow(
        (10, 10),
        (80, 60),
        tail_width=10,
        head_width=30,
        head_length=10,
        head="->",
        text="Hello Drawlib",
        textstyle=ShapeTextStyle(xy_shift=(2.5, 2.5)),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_arrow_theme():
    arrow(
        (10, 25),
        (40, 25),
        tail_width=10,
        head_width=30,
        head_length=10,
        head="->",
        style="blue",
        text="Hello Drawlib",
        textstyle="white",
    )
    arrow(
        (10, 75),
        (40, 75),
        tail_width=10,
        head_width=30,
        head_length=10,
        head="->",
        style="green",
        text="Hello Drawlib",
    )
    arrow(
        (60, 25),
        (90, 25),
        tail_width=10,
        head_width=30,
        head_length=10,
        head="->",
        style="red",
        text="Hello Drawlib",
        textstyle="red",
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
