# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_2.apis import *
from drawlib.v0_2.private.core_canvas.line import LineArcHelper

OUTPUT_DIR = "../../../output_tests/v0_2/drawings_line/line_arc_calc/"


def _test(start_angle, end_angle):
    ellipse((50, 50), 30, 30, style="dashed")
    a, b, c, d = LineArcHelper.bezier_ellipse_arc_approximation((50, 50), 30, 30, start_angle, end_angle)
    circle(a, 1, style="black")
    circle(b, 1, style="red")
    circle(c, 1, style="green")
    circle(d, 1, style="blue")


def test_m45_45():
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_45_m45():
    _test(45, -45)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_45_275():
    _test(45, 275)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_275_45():
    _test(275, 45)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def _test_path_points(start_angle, end_angle):
    ellipse((50, 50), 30, 30, style="dashed")
    path_points = LineArcHelper.get_ellipse_path_points((50, 50), 30, 30, start_angle, end_angle)

    """
    print()
    for path_point in path_points:
        print(path_point)
    """

    circle(path_points[0], 1, style="black")  # type: ignore
    for path_point in path_points[1:]:
        circle(path_point[0], 1, style="red")  # type: ignore
        circle(path_point[1], 1, style="green")  # type: ignore
        circle(path_point[2], 1, style="blue")  # type: ignore

    line_arc((50, 50), 30, 30, start_angle, end_angle, arrowhead="<->")


def test_path_points():
    _test_path_points(180, 45)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
