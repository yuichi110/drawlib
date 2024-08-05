# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_2.apis import *

OUTPUT_DIR = "../../../output_tests/v0_2/drawings_line/lines_bezier/"


def test_lines_bezier():
    points = [
        ((10, 20), (20, 20)),
        (30, 20),
        ((40, 20), (40, 10)),
        ((40, 20), (50, 20)),
    ]
    lines_bezier(xy=(0, 30), path_points=points)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
