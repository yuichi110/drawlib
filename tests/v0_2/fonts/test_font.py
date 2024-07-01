# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_2.apis import *

OUTPUT_DIR = "../../../output_tests/v0_2/fonts/font/"


def test_sans():
    text(
        (10, 5),
        "Hello World. あいうえお",
        style=TextStyle(font=Font.SANSSERIF_LIGHT),
    )
    text(
        (10, 10),
        "Hello World. あいうえお",
        style=TextStyle(font=Font.SANSSERIF_REGULAR),
    )
    text(
        (10, 15),
        "Hello World. あいうえお",
        style=TextStyle(font=Font.SANSSERIF_BOLD),
    )
    text(
        (10, 20),
        "CJK Japanese: 今日はいい天気ですね。",
        style=TextStyle(font=Font.SANSSERIF_REGULAR),
    )
    text(
        (10, 25),
        "CJK Chinese: 今天天气很好。",
        style=TextStyle(font=Font.SANSSERIF_REGULAR),
    )
    text(
        (10, 30),
        "CJK Korean: 오늘은 날씨가 좋네요。",
        style=TextStyle(font=Font.SANSSERIF_REGULAR),
    )
    text(
        (10, 35),
        "Thai: วันนี้อากาศดีจังเลย",
        style=TextStyle(font=Font.SANSSERIF_REGULAR),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_serif():
    text(
        (10, 5),
        "Hello World. あいうえお",
        style=TextStyle(font=Font.SERIF_LIGHT),
    )
    text(
        (10, 10),
        "Hello World. あいうえお",
        style=TextStyle(font=Font.SERIF_REGULAR),
    )
    text(
        (10, 15),
        "Hello World. あいうえお",
        style=TextStyle(font=Font.SERIF_BOLD),
    )
    text(
        (10, 20),
        "CJK Japanese: 今日はいい天気ですね。",
        style=TextStyle(font=Font.SERIF_REGULAR),
    )
    text(
        (10, 25),
        "CJK Chinese: 今天天气很好。",
        style=TextStyle(font=Font.SERIF_REGULAR),
    )
    text(
        (10, 30),
        "CJK Korean: 오늘은 날씨가 좋네요。",
        style=TextStyle(font=Font.SERIF_REGULAR),
    )
    text(
        (10, 35),
        "Thai: วันนี้อากาศดีจังเลย",
        style=TextStyle(font=Font.SERIF_REGULAR),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
