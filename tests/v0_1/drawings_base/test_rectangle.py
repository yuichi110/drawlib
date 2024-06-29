# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_1.apis import *

OUTPUT_DIR = "../../../output_tests/v0_1/drawings_base/rectangle/"


def test():
    rectangle((50, 50), 40, 20, text="Rectangle")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_align_leftbottom():
    rectangle((50, 50), 40, 20, text="Rectangle", style=ShapeStyle(halign="left", valign="bottom"))
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_align_center():
    rectangle((50, 50), 40, 20, text="Rectangle", style=ShapeStyle(halign="center", valign="center"))
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_align_righttop():
    rectangle((50, 50), 40, 20, text="Rectangle", style=ShapeStyle(halign="right", valign="top"))
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_angle0():
    rectangle((50, 50), 40, 20, angle=0, text="Rectangle")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_angle45():
    rectangle((50, 50), 40, 20, angle=45, text="Rectangle")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_angle90():
    rectangle((50, 50), 40, 20, angle=90, text="Rectangle")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_angle135():
    rectangle((50, 50), 40, 20, angle=135, text="Rectangle")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_angle135_shift():
    rectangle(
        (50, 50),
        40,
        20,
        angle=135,
        text="Rectangle",
        textstyle=ShapeTextStyle(xy_shift=(10, 5), flip=True, color=Colors.Red),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_style():
    rectangle(
        (50, 50),
        40,
        20,
        r=3.0,
        angle=45,
        text="Rectangle",
        style=ShapeStyle(
            lcolor=Colors.Blue,
            fcolor=Colors.Yellow,
            alpha=0.5,
            lstyle="dashed",
            lwidth=3,
        ),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_textsize():
    rectangle(
        (50, 50),
        40,
        20,
        text="Rectangle",
        textsize=36,
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
