# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_2.apis import *

OUTPUT_DIR = "../../../output_tests/v0_2/fonts/japanese/"


def test_sans():
    text(
        (50, 10),
        "Hello World. あいうえお",
        style=TextStyle(font=FontJapanese.SANSSERIF_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=TextStyle(font=FontJapanese.SANSSERIF_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. あいうえお",
        style=TextStyle(font=FontJapanese.SANSSERIF_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_serif():
    text(
        (50, 10),
        "Hello World. あいうえお",
        style=TextStyle(font=FontJapanese.SERIF_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=TextStyle(font=FontJapanese.SERIF_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. あいうえお",
        style=TextStyle(font=FontJapanese.SERIF_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_mplus1p():
    text(
        (50, 10),
        "Hello World. あいうえお",
        style=TextStyle(font=FontJapanese.MPLUS1P_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=TextStyle(font=FontJapanese.MPLUS1P_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. あいうえお",
        style=TextStyle(font=FontJapanese.MPLUS1P_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_mplus_rounded1c():
    text(
        (50, 10),
        "Hello World. あいうえお",
        style=TextStyle(font=FontJapanese.MPLUSROUNDED1C_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=TextStyle(font=FontJapanese.MPLUSROUNDED1C_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. あいうえお",
        style=TextStyle(font=FontJapanese.MPLUSROUNDED1C_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_sawarabi():
    text(
        (50, 10),
        "Hello World. あいうえお",
        style=TextStyle(font=FontJapanese.SAWARABI_GOTHIC),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=TextStyle(font=FontJapanese.SAWARABI_MINCHO),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
