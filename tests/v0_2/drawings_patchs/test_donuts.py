# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_2.apis import *

OUTPUT_DIR = "../../../output_tests/v0_2/drawings_patches/donuts/"


def test():
    donuts((50, 50), radius=30, width=10)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_style():
    donuts(
        (50, 50),
        radius=30,
        width=10,
        style=ShapeStyle(lwidth=3, lcolor=Colors.Red, lstyle="dashdot", fcolor=Colors.Green),
        text="Hello",
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_align_leftbottom():
    donuts(
        (50, 50),
        radius=30,
        width=10,
        style=ShapeStyle(halign="left", valign="bottom"),
        text="Hello",
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_align_center():
    donuts(
        (50, 50),
        radius=30,
        width=10,
        style=ShapeStyle(halign="center", valign="center"),
        text="Hello",
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_align_righttop():
    donuts(
        (50, 50),
        radius=30,
        width=10,
        style=ShapeStyle(halign="right", valign="top"),
        text="Hello",
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_angle120():
    donuts((50, 50), radius=30, width=10, angle=120, text="hungy")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
