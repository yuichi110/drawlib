# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_2.apis import *

FONT_AVENGER = "../../assets/avenger/regular.ttf"
FONT_MPLUS1P = "../../assets/mplus1p/regular.ttf"
OUTPUT_DIR = "../../../output_tests/v0_2/drawings/text/"


def test():
    text((30, 30), "Hello World")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_size():
    text((30, 30), "Hello World", style=TextStyle(size=12))
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_textsize():
    text((30, 30), "Hello World", size=36, style=TextStyle(size=12))
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_background():
    text(
        (30, 30),
        "Hello World",
        angle=90,
        style=TextStyle(
            bglcolor=Colors.Blue,
            bgfcolor=Colors.Yellow,
            bglstyle="dotted",
            bglwidth=2,
        ),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_myfont():
    text(
        (20, 30),
        "Hello World. あいうえお",
        style=TextStyle(font=FontFile(FONT_MPLUS1P)),
    )
    text(
        (20, 70),
        "Hello World. あいうえお",
        style=TextStyle(font=FontFile(FONT_AVENGER)),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
