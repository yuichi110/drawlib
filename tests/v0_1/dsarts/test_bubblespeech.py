# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_1.apis import *

OUTPUT_DIR = "../../../output_tests/v0_1/dsarts/bubblespeech/"


def test_left():
    dsart.bubblespeech(
        xy=(30, 30),
        width=50,
        height=40,
        tail_edge="left",
        tail_from_ratio=0.2,
        tail_vertex_xy=(10, 50),
        tail_to_ratio=0.6,
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_top():
    dsart.bubblespeech(
        xy=(30, 30),
        width=50,
        height=40,
        tail_edge="top",
        tail_from_ratio=0.2,
        tail_vertex_xy=(50, 90),
        tail_to_ratio=0.6,
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_right():
    dsart.bubblespeech(
        xy=(30, 30),
        width=50,
        height=40,
        tail_edge="right",
        tail_from_ratio=0.2,
        tail_vertex_xy=(95, 50),
        tail_to_ratio=0.6,
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_bottom():
    dsart.bubblespeech(
        xy=(30, 30),
        width=50,
        height=40,
        tail_edge="bottom",
        tail_from_ratio=0.2,
        tail_vertex_xy=(50, 10),
        tail_to_ratio=0.6,
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_text():
    dsart.bubblespeech(
        xy=(30, 30),
        width=50,
        height=40,
        tail_edge="left",
        tail_from_ratio=0.2,
        tail_vertex_xy=(10, 50),
        tail_to_ratio=0.6,
        text="Hello Drawlib\nHello Python World!!",
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_textstyle():
    dsart.bubblespeech(
        xy=(30, 30),
        width=50,
        height=40,
        tail_edge="left",
        tail_from_ratio=0.2,
        tail_vertex_xy=(10, 50),
        tail_to_ratio=0.6,
        text="Hello Drawlib\nHello Python World!!",
        textstyle=ShapeTextStyle(color=Colors.Red, size=28),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")