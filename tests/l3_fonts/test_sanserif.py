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

OUTPUT_DIR = "../../output_tests/l3_fonts/sansserif/"
BASE_STYLE = Style(text_color=Colors.Black, text_size=16)


def test_lato():
    text(
        (50, 10),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=FontSansSerif.LATO_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=FontSansSerif.LATO_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=FontSansSerif.LATO_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_raleways():
    text(
        (50, 10),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=FontSansSerif.RALEWAYS_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=FontSansSerif.RALEWAYS_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=FontSansSerif.RALEWAYS_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_montserrat():
    text(
        (50, 10),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=FontSansSerif.MONTSERRAT_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=FontSansSerif.MONTSERRAT_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=FontSansSerif.MONTSERRAT_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_oswald():
    text(
        (50, 10),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=FontSansSerif.OSWALD_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=FontSansSerif.OSWALD_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=FontSansSerif.OSWALD_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_poppins():
    text(
        (50, 10),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=FontSansSerif.POPPINS_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=FontSansSerif.POPPINS_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=FontSansSerif.POPPINS_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
