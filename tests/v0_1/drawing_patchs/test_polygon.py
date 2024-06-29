# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_1.apis import *

OUTPUT_DIR = "../../../output_tests/v0_1/drawing_patches/polygon/"


def test():
    polygon(xys=[(10, 10), (10, 50), (80, 30)])
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_align():
    polygon(
        xys=[(10, 10), (10, 50), (80, 30)],
        style=ShapeStyle(halign="center", valign="center"),  # should be ignored
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_style():
    polygon(
        xys=[(10, 10), (10, 50), (80, 30)],
        style=ShapeStyle(lwidth=3, lcolor=Colors.Red, lstyle="dashdot", fcolor=Colors.Green),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_text():
    polygon(xys=[(10, 10), (10, 50), (80, 30)], text="Hello Drawlib!!")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
