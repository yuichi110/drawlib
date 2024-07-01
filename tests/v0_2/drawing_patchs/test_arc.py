# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_2.apis import *

OUTPUT_DIR = "../../../output_tests/v0_2/drawing_patches/arc/"


def test():
    arc((50, 50), 30, 50)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_align_leftbottom():
    arc((50, 50), 30, 50, style=ShapeStyle(halign="left", valign="bottom"), text="Hello")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_align_center():
    arc((50, 50), 30, 50, style=ShapeStyle(halign="center", valign="center"), text="Hello")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_align_righttop():
    arc((50, 50), 30, 50, style=ShapeStyle(halign="right", valign="top"), text="Hello")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_style():
    arc((50, 50), 30, 50, style=ShapeStyle(lcolor=Colors.Red, lwidth=5, lstyle="dashdot", fcolor=Colors.Blue))
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_text():
    arc((50, 50), 30, 50, text="Hello")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_angle45():
    arc((50, 50), 30, 50, angle=45)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_angle45_text():
    arc((50, 50), 30, 50, angle=45, text="Hello")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_angle45_theta():
    arc((50, 50), 30, 50, angle=45, from_angle=90, to_angle=270)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
