# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_2.apis import *

OUTPUT_DIR = "../../../output_tests/v0_2/drawing_patches/ellipse/"


def test():
    ellipse(xy=(50, 50), width=40, height=20)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_style():
    ellipse(xy=(50, 50), width=40, height=20, style=ShapeStyle(lwidth=3, lcolor=Colors.Red, lstyle="dashdot"))
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_align_leftbottom():
    ellipse(xy=(50, 50), width=40, height=20, style=ShapeStyle(halign="left", valign="bottom"), text="Hello")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_align_center():
    ellipse(xy=(50, 50), width=40, height=20, style=ShapeStyle(halign="center", valign="center"), text="Hello")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_align_righttop():
    ellipse(xy=(50, 50), width=40, height=20, style=ShapeStyle(halign="right", valign="top"), text="Hello")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_angle45():
    ellipse(xy=(50, 50), width=40, height=20, angle=45, text="Hello")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_angle90():
    ellipse(xy=(50, 50), width=40, height=20, angle=90, text="Hello")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
