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
from drawlib.colors import Colors
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

OUTPUT_DIR = "../../output_tests/l3_fonts/serif/"
BASE_STYLE = Style(text_color=Colors.Black, text_size=16)


def test_courier():
    text(
        (50, 10),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=FontSerif.COURIER_REGULAR),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=FontSerif.COURIER_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_playfairdisplay():
    text(
        (50, 10),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=FontSerif.PLAYFAIRDISPLAY_REGULAR),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=FontSerif.PLAYFAIRDISPLAY_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_merriweather():
    text(
        (50, 10),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=FontSerif.MERRIWEATHER_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=FontSerif.MERRIWEATHER_REGULAR),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=FontSerif.MERRIWEATHER_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_platypi():
    text(
        (50, 10),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=FontSerif.PLATYPI_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=FontSerif.PLATYPI_REGULAR),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=FontSerif.PLATYPI_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
