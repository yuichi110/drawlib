# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

import pytest

from drawlib.v0_1.apis import *

OUTPUT_DIR = "../../../output_tests/v0_1/drawing_originals/chevron/"


def test_60():
    chevron(xy=(50, 50), width=10, height=15, corner_angle=60)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_60_align_leftbottom():
    chevron(
        xy=(50, 50),
        width=10,
        height=15,
        corner_angle=60,
        style=ShapeStyle(halign="left", valign="bottom"),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_60_align_center():
    chevron(
        xy=(50, 50),
        width=10,
        height=15,
        corner_angle=60,
        style=ShapeStyle(halign="center", valign="center"),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_60_align_righttop():
    chevron(
        xy=(50, 50),
        width=10,
        height=15,
        corner_angle=60,
        style=ShapeStyle(halign="right", valign="top"),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_60_text():
    chevron(xy=(50, 50), width=10, height=15, corner_angle=60, text="Hello")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_60_style():
    chevron(
        xy=(50, 50),
        width=10,
        height=15,
        corner_angle=60,
        style=ShapeStyle(
            lcolor=Colors.Yellow,
            fcolor=Colors.Blue,
            lwidth=3,
        ),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_60_textstyle():
    chevron(
        xy=(50, 50),
        width=10,
        height=15,
        corner_angle=60,
        text="hello",
        textstyle=ShapeTextStyle(
            color=Colors.Red,
            size=28,
        ),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_30():
    chevron(xy=(50, 50), width=10, height=15, corner_angle=30)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_120():
    with pytest.raises(ValueError):
        chevron(xy=(50, 50), width=10, height=15, corner_angle=120)
        save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_60_mirror():
    chevron(xy=(50, 50), width=10, height=15, corner_angle=60, mirror=True)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_angle45():
    chevron(xy=(50, 50), width=10, height=15, corner_angle=60, angle=45)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_angle45_text():
    chevron(xy=(50, 50), width=10, height=15, corner_angle=60, angle=45, text="chevron")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
