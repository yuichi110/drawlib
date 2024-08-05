# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_2.apis import *

OUTPUT_DIR = "../../../output_tests/v0_2/drawings_line/bezier/"


def test_line_bezier1():
    style = LineStyle(width=3, color=Colors.Red, style="dotted", alpha=1)
    line_bezier1((20, 20), (50, 50), (80, 20), style=style)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_line_bezier2():
    style = LineStyle(width=3, color=Colors.Red, style="dotted", alpha=1)
    line_bezier2((20, 20), (20, 50), (80, 50), (80, 20), style=style)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
