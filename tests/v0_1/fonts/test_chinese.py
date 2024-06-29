# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_1.apis import *

OUTPUT_DIR = "../../../output_tests/v0_1/fonts/chinese/"


def test_simplified_sans():
    text(
        (50, 10),
        "Hello World. 今天天气很好。",
        style=TextStyle(font=FontChinese.SIMPLIFIED_SANSSERIF_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. 今天天气很好。",
        style=TextStyle(font=FontChinese.SIMPLIFIED_SANSSERIF_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. 今天天气很好。",
        style=TextStyle(font=FontChinese.SIMPLIFIED_SANSSERIF_BOLD),
    )

    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_simplified_serif():
    text(
        (50, 10),
        "Hello World. 今天天气很好。",
        style=TextStyle(font=FontChinese.SIMPLIFIED_SERIF_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. 今天天气很好。",
        style=TextStyle(font=FontChinese.SIMPLIFIED_SERIF_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. 今天天气很好。",
        style=TextStyle(font=FontChinese.SIMPLIFIED_SERIF_BOLD),
    )

    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_traditional_sans():
    text(
        (50, 10),
        "Hello World. 今天天气很好。",
        style=TextStyle(font=FontChinese.TRADITIONAL_SANSSERIF_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. 今天天气很好。",
        style=TextStyle(font=FontChinese.TRADITIONAL_SANSSERIF_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. 今天天气很好。",
        style=TextStyle(font=FontChinese.TRADITIONAL_SANSSERIF_BOLD),
    )

    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_traditional_serif():
    text(
        (50, 10),
        "Hello World. 今天天气很好。",
        style=TextStyle(font=FontChinese.TRADITIONAL_SERIF_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. 今天天气很好。",
        style=TextStyle(font=FontChinese.TRADITIONAL_SERIF_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. 今天天气很好。",
        style=TextStyle(font=FontChinese.TRADITIONAL_SERIF_BOLD),
    )

    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_hongkong_sans():
    text(
        (50, 10),
        "Hello World. 今天天气很好。",
        style=TextStyle(font=FontChinese.HONGKONG_SANSSERIF_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. 今天天气很好。",
        style=TextStyle(font=FontChinese.HONGKONG_SANSSERIF_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. 今天天气很好。",
        style=TextStyle(font=FontChinese.HONGKONG_SANSSERIF_BOLD),
    )

    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_hongkong_serif():
    text(
        (50, 10),
        "Hello World. 今天天气很好。",
        style=TextStyle(font=FontChinese.HONGKONG_SERIF_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. 今天天气很好。",
        style=TextStyle(font=FontChinese.HONGKONG_SERIF_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. 今天天气很好。",
        style=TextStyle(font=FontChinese.HONGKONG_SERIF_BOLD),
    )

    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
