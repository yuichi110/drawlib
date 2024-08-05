# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_2.apis import *

OUTPUT_DIR = "../../../output_tests/v0_2/drawings_line/curved/"


def test_line_curved():
    line_curved(
        (20, 20),
        (80, 80),
        bend=-0.5,
        arrowhead="->",
    )

    line_curved(
        (20, 80),
        (80, 20),
        bend=-0.5,
        style=LineStyle(style="dashed", width=2, color=Colors.Red),
    )

    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
