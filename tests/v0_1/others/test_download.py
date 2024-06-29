# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_1.apis import *

OUTPUT_DIR = "../../../output_tests/v0_1/others/download/"


def test_font_enum():
    print(Font.SANSSERIF_LIGHT.value)


def test_use_font():
    text(
        (10, 5),
        "Hello World. あいうえお",
        style=TextStyle(font=Font.SANSSERIF_LIGHT),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
