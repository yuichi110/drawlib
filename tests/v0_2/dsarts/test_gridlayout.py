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
    gl = dsart.GridLayout(2, 2, 2, default_style="solid")
    gl.add((0, 0), (0, 0), text="A")
    gl.add((0, 0), (1, 1), text="B")
    gl.add((1, 1), (0, 1), text="C")
    gl.draw((10, 10), 30, 30, 1)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_angle():
    gl = dsart.GridLayout(2, 2, 2, default_style="solid")
    gl.add((0, 0), (0, 0), text="A", textangle=270)
    gl.add((0, 0), (1, 1), text="B", textangle=90)
    gl.add((1, 1), (0, 1), text="C")
    gl.draw((10, 10), 30, 30, 1)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_shift():
    gl = dsart.GridLayout(2, 2, 2, default_style="solid")
    gl.add((0, 0), (0, 0), text="A", text_xy_shift=(3, 3))
    gl.add((0, 0), (1, 1), text="B", text_xy_shift=(-3, -3))
    gl.add((1, 1), (0, 1), text="C")
    gl.draw((10, 10), 30, 30, 1)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_outerstyle():
    gl = dsart.GridLayout(2, 2, 2, default_style="solid")
    gl.add((0, 0), (0, 0), text="A")
    gl.add((0, 0), (1, 1), text="B")
    gl.add((1, 1), (0, 1), text="C")
    gl.draw((10, 10), 30, 30, 1, outer_r=2, outer_style="solid")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
