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

OUTPUT_DIR = "../../../output_tests/v0_2/drawings_line/arc/"


def test_circle():
    line_arc(xy=(25, 25), width=20, height=20, angle_start=45, angle_end=135, arrowhead="->")
    line_arc(xy=(25, 75), width=20, height=20, angle_start=10, angle_end=190, arrowhead="->")
    line_arc(xy=(75, 25), width=20, height=20, angle_start=270, angle_end=135, arrowhead="->")
    line_arc(xy=(75, 75), width=20, height=20, angle_start=0, angle_end=360, arrowhead="->")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_ellipse():
    line_arc(xy=(25, 25), width=30, height=15, angle_start=45, angle_end=135, arrowhead="->")
    line_arc(xy=(25, 75), width=30, height=15, angle_start=10, angle_end=190, arrowhead="->")
    line_arc(xy=(75, 25), width=30, height=15, angle_start=270, angle_end=135, arrowhead="->")
    line_arc(xy=(75, 75), width=30, height=15, angle_start=0, angle_end=360, arrowhead="->")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_ellipse_angle45():
    line_arc(xy=(25, 25), width=30, height=15, angle_start=45, angle_end=135, arrowhead="->", angle=45)
    line_arc(xy=(25, 75), width=30, height=15, angle_start=10, angle_end=190, arrowhead="->", angle=45)
    line_arc(xy=(75, 25), width=30, height=15, angle_start=270, angle_end=135, arrowhead="->", angle=45)
    line_arc(xy=(75, 75), width=30, height=15, angle_start=0, angle_end=360, arrowhead="->", angle=45)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


# Calcurations


def _test_calc(start_angle, end_angle):
    ellipse((50, 50), 30, 30, style="dashed")
    a, b, c, d = LineArcHelper.bezier_ellipse_arc_approximation((50, 50), 30, 30, start_angle, end_angle)
    circle(a, 1, style="black")
    circle(b, 1, style="red")
    circle(c, 1, style="green")
    circle(d, 1, style="blue")


def test_calc_m45_45():
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_45_m45():
    _test_calc(45, -45)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_calc_45_275():
    _test_calc(45, 275)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_calc_275_45():
    _test_calc(275, 45)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def _test_calc_path_points(start_angle, end_angle):
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


def test_calc_path_points():
    _test_calc_path_points(180, 45)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
