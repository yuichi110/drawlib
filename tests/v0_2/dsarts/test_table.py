# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_2.apis import *

OUTPUT_DIR = "../../../output_tests/v0_2/dsarts/table/"


def test():
    t = dsart.Table()
    t.draw((10, 85), 30, 20, data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_predefined_style_default():
    t = dsart.Table()
    t.set_predefined_style("default")
    t.draw((10, 85), 30, 20, data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_predefined_style_monochrome():
    t = dsart.Table()
    t.set_predefined_style("monochrome")
    t.draw((10, 85), 30, 20, data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_predefined_style_border_simple():
    t = dsart.Table()
    t.set_predefined_style("border_simple")
    t.draw((10, 85), 30, 20, data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_predefined_style_none():
    t = dsart.Table()
    t.set_predefined_style("none")
    t.draw((10, 85), 30, 20, data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_style():
    t = dsart.Table()
    t.clear_styles()
    t.set_style_cell_evenodd(
        Colors.Gray,
        "white",
        Colors.White,
        "black",
    )
    t.set_style_border(top="black", top2="black_light", bottom="black")
    t.draw((10, 85), 30, 20, data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
