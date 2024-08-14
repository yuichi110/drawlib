# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_2.apis import *

OUTPUT_DIR = "../../../output_tests/v0_2/dsarts/gridlayout/"


def test():
    gl = dsart.GridLayout(3, 3, 2, default_style="solid")
    gl.add((0, 0), 1, 1, text="A")
    gl.add((0, 1), 1, 1, text="B")
    gl.add((0, 2), 1, 1, text="C")
    gl.add((1, 0), 1, 3, text="D")
    gl.add((2, 0), 1, 1, text="E")
    gl.draw((10, 10), 30, 30, 1)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_angle():
    gl = dsart.GridLayout(3, 3, 2, default_style="solid")
    gl.add((0, 0), 1, 1, text="A", textangle=270)
    gl.add((0, 1), 1, 1, text="B", textangle=90)
    gl.add((0, 2), 1, 1, text="C")
    gl.add((1, 0), 1, 3, text="D")
    gl.add((2, 0), 1, 1, text="E")
    gl.draw((10, 10), 30, 30, 1)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_shift():
    gl = dsart.GridLayout(3, 3, 2, default_style="solid")
    gl.add((0, 0), 1, 1, text="A", text_xy_shift=(3, 3))
    gl.add((0, 1), 1, 1, text="B", text_xy_shift=(-3, -3))
    gl.add((0, 2), 1, 1, text="C")
    gl.add((1, 0), 1, 3, text="D")
    gl.add((2, 0), 1, 1, text="E")
    gl.draw((10, 10), 30, 30, 1)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_outerstyle():
    gl = dsart.GridLayout(3, 3, 2, default_style="solid")
    gl.add((0, 0), 1, 1, text="A")
    gl.add((0, 1), 1, 1, text="B")
    gl.add((0, 2), 1, 1, text="C")
    gl.add((1, 0), 1, 3, text="D")
    gl.add((2, 0), 1, 1, text="E")
    gl.draw((10, 10), 30, 30, 1, outer_style="solid")
    gl.draw((60, 10), 30, 30, 1, outer_r=0, outer_style="solid")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
