# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_2.apis import *

FONT_AWESOME_FREE = "../../assets/fontawesome-free/brands.ttf"
OUTPUT_DIR = "../../../output_tests/v0_2/drawing_icons/icon/"


def test_icon():
    icon(
        xy=(50, 50),
        width=20,
        code="\uf1a0",
        file=FONT_AWESOME_FREE,
        style=IconStyle(
            color=Colors.Red,
            halign="center",
            valign="center",
        ),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
