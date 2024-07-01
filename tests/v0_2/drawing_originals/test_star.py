# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_2.apis import *

OUTPUT_DIR = "../../../output_tests/v0_2/drawing_originals/star/"


def test_vertex3():
    star((50, 50), 3, 30, 5, text="Hello")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_vertex4():
    star((50, 50), 4, 30, 15, text="Hello")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_vertex5():
    star((50, 50), 5, 30, 15, text="Hello")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_vertex5_align_leftbottom():
    star(
        (50, 50),
        5,
        30,
        15,
        style=ShapeStyle(halign="left", valign="bottom"),
        text="Hello",
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_vertex5_align_center():
    star(
        (50, 50),
        5,
        30,
        15,
        style=ShapeStyle(halign="center", valign="center"),
        text="Hello",
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_vertex5_align_righttop():
    star(
        (50, 50),
        5,
        30,
        15,
        style=ShapeStyle(halign="right", valign="top"),
        text="Hello",
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_vertex5_style():
    star(
        (50, 50),
        5,
        30,
        15,
        style=ShapeStyle(lcolor=Colors.Red, lstyle="dashdot", lwidth=2, fcolor=Colors.Transparent),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_vertex5_angle45():
    star((50, 50), 5, 30, 15, angle=45, text="Hello")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_vertex5_angle90():
    star((50, 50), 5, 30, 15, angle=90, text="Hello")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_vertex6():
    star((50, 50), 6, 30, 15, text="Hello")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_vertex7():
    star((50, 50), 7, 30, 15, text="Hello")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_vertex8():
    star((50, 50), 8, 30, 15, text="Hello")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_vertex9():
    star((50, 50), 9, 30, 15, text="Hello")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_vertex10():
    star((50, 50), 10, 30, 15, text="Hello")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
