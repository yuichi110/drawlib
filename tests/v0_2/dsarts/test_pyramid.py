# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_2.apis import *

OUTPUT_DIR = "../../../output_tests/v0_2/dsarts/pyramid/"


def test():
    p = dsart.Pyramid(default_style="solid")
    p.add(text="Hello")
    p.add(text="World")
    p.add(text="A")
    p.draw((10, 10), 30, 30, 2)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_align_bottom():
    p = dsart.Pyramid(default_style="solid")
    p.add(text="Hello")
    p.add(text="World")
    p.add(text="A")
    p.draw((10, 10), 30, 30, 2, align="bottom")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_align_top():
    p = dsart.Pyramid(default_style="solid")
    p.add(text="Hello")
    p.add(text="World")
    p.add(text="A")
    p.draw((10, 10), 30, 30, 2, align="top")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_align_left():
    p = dsart.Pyramid(default_style="solid")
    p.add(text="Hello")
    p.add(text="World")
    p.add(text="A")
    p.draw((10, 10), 30, 30, 2, align="left")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_align_right():
    p = dsart.Pyramid(default_style="solid")
    p.add(text="Hello")
    p.add(text="World")
    p.add(text="A")
    p.draw((10, 10), 30, 30, 2, align="right")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
