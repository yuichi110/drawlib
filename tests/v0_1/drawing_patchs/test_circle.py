# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_1.apis import *

OUTPUT_DIR = "../../../output_tests/v0_1/drawing_patches/circle/"


def test():
    circle(xy=(50, 50), radius=30)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_align_leftbottom():
    circle(
        xy=(50, 50),
        radius=30,
        style=ShapeStyle(halign="left", valign="bottom"),
        text="Hello",
        angle=45,
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_align_center():
    circle(
        xy=(50, 50),
        radius=30,
        style=ShapeStyle(halign="center", valign="center"),
        text="Hello",
        angle=45,
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_align_righttop():
    circle(
        xy=(50, 50),
        radius=30,
        style=ShapeStyle(halign="right", valign="top"),
        text="Hello",
        angle=45,
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_style():
    circle(
        xy=(50, 50),
        radius=30,
        style=ShapeStyle(lcolor=Colors.Red, lwidth=5, lstyle="dashdot", fcolor=Colors.Blue, alpha=0.7),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_text():
    circle(xy=(50, 50), radius=30, text="Circle", angle=45)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_theme():
    circle(xy=(25, 25), radius=20, style="blue")
    circle(xy=(25, 75), radius=20, style="green")
    circle(xy=(75, 25), radius=20, style="red")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
