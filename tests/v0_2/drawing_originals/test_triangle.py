# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_2.apis import *

OUTPUT_DIR = "../../../output_tests/v0_2/drawing_originals/triangle/"


def test():
    triangle((50, 50), 30, 40)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_style():
    triangle(
        (50, 50),
        30,
        40,
        style=ShapeStyle(lcolor=Colors.Red, lwidth=2, lstyle="dashdot", fcolor=Colors.Transparent),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_align_leftbottom():
    triangle(
        (50, 50),
        30,
        40,
        style=ShapeStyle(halign="left", valign="bottom"),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_align_center():
    triangle(
        (50, 50),
        30,
        40,
        style=ShapeStyle(halign="center", valign="center"),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_align_righttop():
    triangle(
        (50, 50),
        30,
        40,
        style=ShapeStyle(halign="right", valign="top"),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_text():
    triangle((50, 50), 30, 40, text="Hello")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_start0():
    triangle((50, 50), 30, 40, topvertex_x=0)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_startminus10():
    triangle((50, 50), 30, 40, topvertex_x=-10)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_start40():
    triangle((50, 50), 30, 40, topvertex_x=40)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_rotate45():
    triangle((50, 50), 30, 40, angle=45)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_rotate45_text():
    triangle((50, 50), 30, 40, angle=45, text="Hello")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
