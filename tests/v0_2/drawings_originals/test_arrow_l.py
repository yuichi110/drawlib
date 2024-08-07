# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_2.apis import *

OUTPUT_DIR = "../../../output_tests/v0_2/drawings_originals/arrow_l/"


def test():
    arrow_l(
        (50, 25),
        width=30,
        height=20,
        tail_width=5,
        head_width=10,
        head_length=10,
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_right():
    arrow_l(
        xy=(50, 50),
        width=60,
        height=30,
        tail_width=2,
        head_length=3,
        head_width=5,
        head="->",
        r=5,
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_right_90():
    arrow_l(
        xy=(50, 50),
        width=60,
        height=30,
        tail_width=2,
        head_length=3,
        head_width=5,
        head="->",
        r=5,
        angle=90,
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_right_180():
    arrow_l(
        xy=(50, 50),
        width=60,
        height=30,
        tail_width=2,
        head_length=3,
        head_width=5,
        head="->",
        r=5,
        angle=180,
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_right_270():
    arrow_l(
        xy=(50, 50),
        width=60,
        height=30,
        tail_width=2,
        head_length=3,
        head_width=5,
        head="->",
        r=5,
        angle=270,
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_left():
    arrow_l(
        xy=(50, 50),
        width=60,
        height=30,
        tail_width=2,
        head_length=3,
        head_width=5,
        head="<-",
        r=5,
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_both():
    arrow_l(
        xy=(50, 50),
        width=60,
        height=30,
        tail_width=2,
        head_length=3,
        head_width=5,
        head="<->",
        r=5,
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
