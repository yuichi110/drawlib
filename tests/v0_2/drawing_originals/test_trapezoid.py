# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_2.apis import *

OUTPUT_DIR = "../../../output_tests/v0_2/drawing_originals/trapezoid/"


def test():
    trapezoid((50, 50), 30, 40, 20)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_text():
    trapezoid((50, 50), 30, 40, 20, text="Hello")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_style():
    trapezoid(
        (50, 50),
        30,
        40,
        20,
        style=ShapeStyle(lcolor=Colors.Red, fcolor=Colors.Transparent, lwidth=2, lstyle="dashdot"),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_align_leftbottom():
    trapezoid((50, 50), 30, 40, 20, style=ShapeStyle(halign="left", valign="bottom"))
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_align_center():
    trapezoid((50, 50), 30, 40, 20, style=ShapeStyle(halign="center", valign="center"))
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_align_righttop():
    trapezoid((50, 50), 30, 40, 20, style=ShapeStyle(halign="right", valign="top"))
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_tw60():
    trapezoid((50, 50), 30, 40, 60, style=ShapeStyle(halign="center", valign="center"))
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_ts0():
    trapezoid((50, 50), 30, 40, 20, topedge_x=0)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_ts5():
    trapezoid((50, 50), 30, 40, 20, topedge_x=5)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_ts20():
    trapezoid((50, 50), 30, 40, 20, topedge_x=20)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_ts25():
    trapezoid((50, 50), 30, 40, 20, topedge_x=25)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_tsminus10():
    trapezoid((50, 50), 30, 40, 20, topedge_x=-10)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_rotate45():
    trapezoid((50, 50), 30, 40, 20, angle=45)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_rotate45_text():
    trapezoid((50, 50), 30, 40, 20, angle=45, text="Hello")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
