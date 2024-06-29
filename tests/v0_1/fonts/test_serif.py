# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_1.apis import *

OUTPUT_DIR = "../../../output_tests/v0_1/fonts/serif/"


def test_courier():
    text(
        (50, 10),
        "Hello World. あいうえお",
        style=TextStyle(font=FontSerif.COURIER_REGULAR),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=TextStyle(font=FontSerif.COURIER_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_playfairdisplay():
    text(
        (50, 10),
        "Hello World. あいうえお",
        style=TextStyle(font=FontSerif.PLAYFAIRDISPLAY_REGULAR),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=TextStyle(font=FontSerif.PLAYFAIRDISPLAY_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_merriweather():
    text(
        (50, 10),
        "Hello World. あいうえお",
        style=TextStyle(font=FontSerif.MERRIWEATHER_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=TextStyle(font=FontSerif.MERRIWEATHER_REGULAR),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=TextStyle(font=FontSerif.MERRIWEATHER_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_platypi():
    text(
        (50, 10),
        "Hello World. あいうえお",
        style=TextStyle(font=FontSerif.PLATYPI_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=TextStyle(font=FontSerif.PLATYPI_REGULAR),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=TextStyle(font=FontSerif.PLATYPI_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
