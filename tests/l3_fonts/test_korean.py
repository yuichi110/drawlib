# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib._utils import dutil_script
from drawlib.canvas import clear, save
from drawlib.fonts import (
    Font,
    FontArabic,
    FontBrahmic,
    FontChinese,
    FontFile,
    FontJapanese,
    FontKorean,
    FontMonoSpace,
    FontRoboto,
    FontSansSerif,
    FontSerif,
    FontSourceCode,
    FontThai,
)
from drawlib.text import text
from drawlib.types import Style

OUTPUT_DIR = "../../output_tests/l3_fonts/korean/"


def test_sans():
    text(
        (50, 10),
        "Hello World. 오늘은 날씨가 좋네요。",
        style=Style(text_font=FontKorean.SANSSERIF_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. 오늘은 날씨가 좋네요。",
        style=Style(text_font=FontKorean.SANSSERIF_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. 오늘은 날씨가 좋네요。",
        style=Style(text_font=FontKorean.SANSSERIF_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_serif():
    text(
        (50, 10),
        "Hello World. 오늘은 날씨가 좋네요。",
        style=Style(text_font=FontKorean.SERIF_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. 오늘은 날씨가 좋네요。",
        style=Style(text_font=FontKorean.SERIF_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. 오늘은 날씨가 좋네요。",
        style=Style(text_font=FontKorean.SERIF_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
