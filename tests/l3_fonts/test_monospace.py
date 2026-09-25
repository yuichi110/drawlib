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

OUTPUT_DIR = "../../output_tests/l3_fonts/monospace/"
BASE_STYLE = Style(text_color=Colors.Black, text_size=16)


def test_roboto_mono():
    text(
        (50, 10),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=FontMonoSpace.ROBOTO_MONO_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=FontMonoSpace.ROBOTO_MONO_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=FontMonoSpace.ROBOTO_MONO_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_courier():
    text(
        (50, 10),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=FontMonoSpace.COURIER_REGULAR),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=FontMonoSpace.COURIER_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_sourcecodepro():
    text(
        (50, 10),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=FontMonoSpace.SOURCECODEPRO_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=FontMonoSpace.SOURCECODEPRO_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. あいうえお",
        style=BASE_STYLE.patch(text_font=FontMonoSpace.SOURCECODEPRO_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
