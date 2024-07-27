# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_2.apis import *

OUTPUT_DIR = "../../../output_tests/v0_2/dsarts/boxlist/"


def test():
    b = dsart.BoxList("solid", "", "red_solid_bold", "red_bold")
    b.draw((10, 10), 8, 6, [1, 2, 3, 4], [2], 7)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_right():
    b = dsart.BoxList("solid", "", "red_solid_bold", "red_bold")
    b.draw((90, 10), 8, 6, [1, 2, 3, 4], [2], 7, "right")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_bottom():
    b = dsart.BoxList("solid", "", "red_solid_bold", "red_bold")
    b.draw((10, 10), 8, 6, [1, 2, 3, 4], [2], 7, "bottom")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_top():
    b = dsart.BoxList("solid", "", "red_solid_bold", "red_bold")
    b.draw((10, 90), 8, 6, [1, 2, 3, 4], [2], 7, "top")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
