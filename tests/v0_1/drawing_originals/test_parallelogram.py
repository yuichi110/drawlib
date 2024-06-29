# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_1.apis import *

OUTPUT_DIR = "../../../output_tests/v0_1/drawing_originals/parallelogram/"


def test():
    parallelogram((50, 50), 30, 20, 60)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_align_leftbottom():
    parallelogram((50, 50), 30, 20, 60, style=ShapeStyle(halign="left", valign="bottom"))
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_align_center():
    parallelogram((50, 50), 30, 20, 60, style=ShapeStyle(halign="center", valign="center"))
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_align_righttop():
    parallelogram((50, 50), 30, 20, 60, style=ShapeStyle(halign="right", valign="top"))
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_text():
    parallelogram((50, 50), 30, 20, 60, text="hello")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_textstyle():
    parallelogram(
        (50, 50),
        30,
        20,
        60,
        text="hello",
        textstyle=ShapeTextStyle(color=Colors.Red),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_style():
    parallelogram(
        (50, 50),
        30,
        20,
        60,
        style=ShapeStyle(lcolor=Colors.Red, fcolor=Colors.Transparent),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_cangle45():
    parallelogram((50, 50), 30, 20, 45)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_cangle75():
    parallelogram((50, 50), 30, 20, 75)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_rotate45():
    parallelogram((50, 50), 30, 20, 60, 45)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_rotate45_text():
    parallelogram((50, 50), 30, 20, 60, 45, text="hello", textstyle=ShapeTextStyle(color=Colors.Red))
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
