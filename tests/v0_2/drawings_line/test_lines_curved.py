# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_2.apis import *

OUTPUT_DIR = "../../../output_tests/v0_2/drawings_line/lines_curved/"


def test_lines_curved():
    lines_curved(xys=[(20, 20), (40, 80), (70, 30), (90, 50)], r=5)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
