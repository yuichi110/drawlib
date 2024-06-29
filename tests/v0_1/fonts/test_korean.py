# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_1.apis import *

OUTPUT_DIR = "../../../output_tests/v0_1/fonts/korean/"


def test_sans():
    text(
        (50, 10),
        "Hello World. 오늘은 날씨가 좋네요。",
        style=TextStyle(font=FontKorean.SANSSERIF_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. 오늘은 날씨가 좋네요。",
        style=TextStyle(font=FontKorean.SANSSERIF_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. 오늘은 날씨가 좋네요。",
        style=TextStyle(font=FontKorean.SANSSERIF_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_serif():
    text(
        (50, 10),
        "Hello World. 오늘은 날씨가 좋네요。",
        style=TextStyle(font=FontKorean.SERIF_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. 오늘은 날씨가 좋네요。",
        style=TextStyle(font=FontKorean.SERIF_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. 오늘은 날씨가 좋네요。",
        style=TextStyle(font=FontKorean.SERIF_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
