# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_2.apis import *

OUTPUT_DIR = "../../../output_tests/v0_2/drawings/line/"


def test_line():
    line((10, 10), (90, 90))
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


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


def test_line_bezier1():
    style = LineStyle(width=3, color=Colors.Red, style="dotted", alpha=1)
    line_bezier1((20, 20), (50, 50), (80, 20), style=style)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_line_bezier2():
    style = LineStyle(width=3, color=Colors.Red, style="dotted", alpha=1)
    line_bezier2((20, 20), (20, 50), (80, 50), (80, 20), style=style)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_line_curved():
    line_curved(
        (20, 20),
        (80, 80),
        bend=-0.5,
        arrowhead="->",
    )

    line_curved(
        (20, 80),
        (80, 20),
        bend=-0.5,
        style=LineStyle(style="dashed", width=2, color=Colors.Red),
    )

    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_lines():
    lines(xys=[(20, 20), (40, 80), (70, 30)])
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_lines_curved():
    lines_curved(xys=[(20, 20), (40, 80), (70, 30), (90, 50)], r=5)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_lines_bezier():
    points = [
        ((10, 20), (20, 20)),
        (30, 20),
        ((40, 20), (40, 10)),
        ((40, 20), (50, 20)),
    ]
    lines_bezier(xy=(0, 30), path_points=points)
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
