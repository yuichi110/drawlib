# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_2.apis import *

OUTPUT_DIR = "../../../output_tests/v0_2/fonts/monospace/"


def test_roboto_mono():
    text(
        (50, 10),
        "Hello World. あいうえお",
        style=TextStyle(font=FontMonoSpace.ROBOTO_MONO_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=TextStyle(font=FontMonoSpace.ROBOTO_MONO_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. あいうえお",
        style=TextStyle(font=FontMonoSpace.ROBOTO_MONO_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_courier():
    text(
        (50, 10),
        "Hello World. あいうえお",
        style=TextStyle(font=FontMonoSpace.COURIER_REGULAR),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=TextStyle(font=FontMonoSpace.COURIER_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_sourcecodepro():
    text(
        (50, 10),
        "Hello World. あいうえお",
        style=TextStyle(font=FontMonoSpace.SOURCECODEPRO_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. あいうえお",
        style=TextStyle(font=FontMonoSpace.SOURCECODEPRO_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. あいうえお",
        style=TextStyle(font=FontMonoSpace.SOURCECODEPRO_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
