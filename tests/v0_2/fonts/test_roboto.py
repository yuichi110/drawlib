# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_2.apis import *

OUTPUT_DIR = "../../../output_tests/v0_2/fonts/roboto/"


def test_roboto():
    text(
        (50, 10),
        "Hello World. あいうえお",
        style=TextStyle(font=FontRoboto.ROBOTO_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=TextStyle(font=FontRoboto.ROBOTO_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. あいうえお",
        style=TextStyle(font=FontRoboto.ROBOTO_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_roboto_serif():
    text(
        (50, 10),
        "Hello World. あいうえお",
        style=TextStyle(font=FontRoboto.SERIF_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=TextStyle(font=FontRoboto.SERIF_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. あいうえお",
        style=TextStyle(font=FontRoboto.SERIF_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_roboto_mono():
    text(
        (50, 10),
        "Hello World. あいうえお",
        style=TextStyle(font=FontRoboto.MONO_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=TextStyle(font=FontRoboto.MONO_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. あいうえお",
        style=TextStyle(font=FontRoboto.MONO_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_roboto_condensed():
    text(
        (50, 10),
        "Hello World. あいうえお",
        style=TextStyle(font=FontRoboto.CONDENSED_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=TextStyle(font=FontRoboto.CONDENSED_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. あいうえお",
        style=TextStyle(font=FontRoboto.CONDENSED_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_roboto_slab():
    text(
        (50, 10),
        "Hello World. あいうえお",
        style=TextStyle(font=FontRoboto.SLAB_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=TextStyle(font=FontRoboto.SLAB_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. あいうえお",
        style=TextStyle(font=FontRoboto.SLAB_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
