# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.apis import *

IMAGE_FILE = "../../assets/image.png"
OUTPUT_DIR = "../../../output_tests/v0_2/theme/line/"


def test_change_default_linearrow_fill():
    dtheme.change_default_linearrow_fill(True)

    line((20, 30), (80, 30), arrowhead="->")
    line((20, 50), (80, 50), arrowhead="<-", style="red")
    line((20, 80), (80, 80), arrowhead="<->", style="blue_dashed_bold")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
