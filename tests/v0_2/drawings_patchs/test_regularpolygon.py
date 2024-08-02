# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_2.apis import *

OUTPUT_DIR = "../../../output_tests/v0_2/drawings_patches/regularpolygon/"


def test_vertices5():
    regularpolygon(xy=(50, 50), radius=30, num_vertex=5, text="Hello")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_vertices6():
    regularpolygon(xy=(50, 50), radius=30, num_vertex=6, text="Hello")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_vertices7():
    regularpolygon(xy=(50, 50), radius=30, num_vertex=7, text="Hello")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_vertices8():
    regularpolygon(xy=(50, 50), radius=30, num_vertex=8, text="Hello")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_vertices5_style():
    regularpolygon(
        xy=(50, 50),
        radius=30,
        num_vertex=5,
        style=ShapeStyle(lwidth=3, lcolor=Colors.Red, lstyle="dashdot", fcolor=Colors.Green),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_vertices8_align_leftbottom():
    regularpolygon(
        xy=(50, 50),
        radius=30,
        num_vertex=8,
        text="Hello",
        style=ShapeStyle(halign="left", valign="bottom"),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_vertices8_align_center():
    regularpolygon(
        xy=(50, 50),
        radius=30,
        num_vertex=8,
        text="Hello",
        style=ShapeStyle(halign="center", valign="center"),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_vertices8_align_righttop():
    regularpolygon(
        xy=(50, 50),
        radius=30,
        num_vertex=8,
        text="Hello",
        style=ShapeStyle(halign="right", valign="top"),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_vertices5_45():
    regularpolygon(xy=(50, 50), radius=30, num_vertex=5, angle=45, text="Hello")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
