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
from drawlib.types import TextStyle

OUTPUT_DIR = "../../output_tests/l3_fonts/roboto/"


def test_roboto():
    text(
        (50, 10),
        "Hello World. あいうえお",
        style=TextStyle(text_font=FontRoboto.ROBOTO_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=TextStyle(text_font=FontRoboto.ROBOTO_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. あいうえお",
        style=TextStyle(text_font=FontRoboto.ROBOTO_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_roboto_serif():
    text(
        (50, 10),
        "Hello World. あいうえお",
        style=TextStyle(text_font=FontRoboto.SERIF_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=TextStyle(text_font=FontRoboto.SERIF_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. あいうえお",
        style=TextStyle(text_font=FontRoboto.SERIF_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_roboto_mono():
    text(
        (50, 10),
        "Hello World. あいうえお",
        style=TextStyle(text_font=FontRoboto.MONO_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=TextStyle(text_font=FontRoboto.MONO_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. あいうえお",
        style=TextStyle(text_font=FontRoboto.MONO_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_roboto_condensed():
    text(
        (50, 10),
        "Hello World. あいうえお",
        style=TextStyle(text_font=FontRoboto.CONDENSED_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=TextStyle(text_font=FontRoboto.CONDENSED_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. あいうえお",
        style=TextStyle(text_font=FontRoboto.CONDENSED_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_roboto_slab():
    text(
        (50, 10),
        "Hello World. あいうえお",
        style=TextStyle(text_font=FontRoboto.SLAB_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=TextStyle(text_font=FontRoboto.SLAB_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. あいうえお",
        style=TextStyle(text_font=FontRoboto.SLAB_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
