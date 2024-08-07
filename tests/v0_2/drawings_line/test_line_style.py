# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_2.apis import *

OUTPUT_DIR = "../../../output_tests/v0_2/drawings_line/style/"


def test_line_style():
    style = LineStyle(width=3, color=Colors.Red, style="dashdot", alpha=0.5)
    line((20, 80), (80, 20), style=style)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_line_arrow():
    line(
        (20, 20),
        (80, 80),
        arrowhead="->",
    )

    line(
        (20, 80),
        (80, 20),
        arrowhead="<->",
        style=LineStyle(color=Colors.Red, ahfill=True),
    )

    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_line_theme():
    line((10, 10), (90, 90), style="green")
    line((10, 90), (90, 10), arrowhead="->", style="red")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_line_curved_theme():
    line_curved(
        (20, 20),
        (80, 80),
        bend=-0.5,
        style="green",
    )

    line_curved(
        (20, 80),
        (80, 20),
        bend=-0.5,
        arrowhead="<->",
        style="red",
    )

    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_width():
    for y, width in [(10, 2), (20, 4), (30, 8), (40, 1), (50, 0.5)]:
        line((10, y), (90, y), width=width)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
