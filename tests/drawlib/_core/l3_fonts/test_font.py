# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.canvas import save
from drawlib.fonts import Font
from drawlib.styles import Colors
from drawlib.text import text
from drawlib.types import Style

OUTPUT_DIR = "../../../../output_tests/_core/l3_fonts/font/"
BASE_STYLE = Style(text_color=Colors.Black, text_size=16)


def test_sans():
    text(
        (10, 5),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=Font.SANSSERIF_THIN),
    )
    text(
        (10, 10),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=Font.SANSSERIF_REGULAR),
    )
    text(
        (10, 15),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=Font.SANSSERIF_BOLD),
    )
    text(
        (10, 20),
        "CJK Japanese: 今日はいい天気ですね。",
        style=BASE_STYLE.patch(text_font=Font.SANSSERIF_REGULAR),
    )
    text(
        (10, 25),
        "CJK Chinese: 今天天气很好。",
        style=BASE_STYLE.patch(text_font=Font.SANSSERIF_REGULAR),
    )
    text(
        (10, 30),
        "CJK Korean: 오늘은 날씨가 좋네요。",
        style=BASE_STYLE.patch(text_font=Font.SANSSERIF_REGULAR),
    )
    text(
        (10, 35),
        "Thai: วันนี้อากาศดีจังเลย",
        style=BASE_STYLE.patch(text_font=Font.SANSSERIF_REGULAR),
    )
    save(f"{OUTPUT_DIR}test_sans.png")


def test_serif():
    text(
        (10, 5),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=Font.SERIF_THIN),
    )
    text(
        (10, 10),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=Font.SERIF_REGULAR),
    )
    text(
        (10, 15),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=Font.SERIF_BOLD),
    )
    text(
        (10, 20),
        "CJK Japanese: 今日はいい天気ですね。",
        style=BASE_STYLE.patch(text_font=Font.SERIF_REGULAR),
    )
    text(
        (10, 25),
        "CJK Chinese: 今天天气很好。",
        style=BASE_STYLE.patch(text_font=Font.SERIF_REGULAR),
    )
    text(
        (10, 30),
        "CJK Korean: 오늘은 날씨가 좋네요。",
        style=BASE_STYLE.patch(text_font=Font.SERIF_REGULAR),
    )
    text(
        (10, 35),
        "Thai: วันนี้อากาศดีจังเลย",
        style=BASE_STYLE.patch(text_font=Font.SERIF_REGULAR),
    )
    save(f"{OUTPUT_DIR}test_serif.png")
