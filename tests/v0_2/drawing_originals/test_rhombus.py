# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_2.apis import *

OUTPUT_DIR = "../../../output_tests/v0_2/drawing_originals/rhombus/"


def test():
    rhombus((50, 50), 20, 40)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_style():
    rhombus(
        (50, 50),
        20,
        40,
        style=ShapeStyle(
            lcolor=Colors.Red,
            fcolor=Colors.Transparent,
            lwidth=3,
        ),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_align_leftbottom():
    rhombus((50, 50), 20, 40, style=ShapeStyle(halign="left", valign="bottom"))
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_align_center():
    rhombus((50, 50), 20, 40, style=ShapeStyle(halign="center", valign="center"))
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_align_righttop():
    rhombus((50, 50), 20, 40, style=ShapeStyle(halign="right", valign="top"))
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_text():
    rhombus((50, 50), 20, 40, text="hello")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_rotate45():
    rhombus((50, 50), 20, 40, angle=45)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_rotate45_text():
    rhombus((50, 50), 20, 40, angle=45, text="hello")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
