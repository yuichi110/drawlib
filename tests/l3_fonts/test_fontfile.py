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

FONT_AVENGER = "../assets/avenger/regular.ttf"
FONT_MPLUS1P = "../assets/mplus1p/regular.ttf"

OUTPUT_DIR = "../../output_tests/l3_fonts/font_file/"


def test():
    text(
        (20, 30),
        "Hello World. あいうえお",
        style=Style(text_font=FontFile(FONT_MPLUS1P)),
    )
    text(
        (20, 70),
        "Hello World. あいうえお",
        style=Style(text_font=FontFile(FONT_AVENGER)),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
