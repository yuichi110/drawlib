# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_2.apis import *

OUTPUT_DIR = "../../../output_tests/v0_2/drawing_patches/fan/"


def test():
    fan((50, 50), radius=30, from_angle=45, to_angle=90)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_style():
    fan(
        (50, 50),
        radius=30,
        from_angle=45,
        to_angle=90,
        style=ShapeStyle(lwidth=3, lcolor=Colors.Red, lstyle="dashdot", fcolor=Colors.Green),
        text="Hello",
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_align_leftbottom():
    fan(
        (50, 50),
        radius=30,
        from_angle=45,
        to_angle=90,
        style=ShapeStyle(halign="left", valign="bottom"),
        text="Hello",
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_align_center():
    fan(
        (50, 50),
        radius=30,
        from_angle=45,
        to_angle=90,
        style=ShapeStyle(halign="center", valign="center"),
        text="Hello",
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_align_righttop():
    fan(
        (50, 50),
        radius=30,
        from_angle=45,
        to_angle=90,
        style=ShapeStyle(halign="right", valign="top"),
        text="Hello",
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_angle120():
    fan((50, 50), radius=30, from_angle=45, to_angle=270, angle=120, text="Hello")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
