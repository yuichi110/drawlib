# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code icon: protobuf."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

# ruff: noqa: E501
# fmt: off
setup_icon()

w = 2.0
s = 40.0 / 41.0


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


red_top_left = _sc([(17.62, 62.71), (24.91, 72.65), (44.8, 72.65), (27.69, 49.61)])
blue_bot_left = _sc([(9.0, 49.89), (9.0, 50.06), (9.01, 50.22), (9.03, 50.39), (9.07, 50.57), (9.14, 50.76), (9.24, 50.99), (9.37, 51.26), (9.56, 51.57), (9.79, 51.95), (10.09, 52.39), (10.44, 52.91), (10.87, 53.52), (11.38, 54.23), (11.97, 55.04), (12.65, 55.97), (13.42, 57.03), (14.3, 58.22), (15.29, 59.56), (16.39, 61.05), (17.62, 62.71), (44.8, 27.35), (25.36, 27.35), (23.02, 30.36), (20.93, 33.08), (19.05, 35.52), (17.38, 37.69), (15.9, 39.61), (14.61, 41.29), (13.5, 42.76), (12.54, 44.03), (11.72, 45.12), (11.05, 46.05), (10.49, 46.82), (10.05, 47.46), (9.7, 47.99), (9.44, 48.42), (9.26, 48.77), (9.13, 49.06), (9.06, 49.29), (9.02, 49.5), (9.0, 49.69)])
yellow_bot_right = _sc([(71.63, 50.67), (81.94, 37.07), (74.42, 27.35), (54.97, 27.35)])
green_top_right = _sc([(54.97, 72.65), (74.2, 72.65), (76.5, 69.65), (78.58, 66.93), (80.45, 64.49), (82.13, 62.31), (83.61, 60.36), (84.92, 58.65), (86.07, 57.14), (87.06, 55.84), (87.91, 54.71), (88.63, 53.75), (89.23, 52.94), (89.72, 52.26), (90.11, 51.71), (90.41, 51.26), (90.63, 50.9), (90.79, 50.61), (90.9, 50.38), (90.96, 50.19), (90.99, 50.04), (91.0, 49.89), (91.0, 49.75), (90.99, 49.6), (90.96, 49.45), (90.92, 49.28), (90.84, 49.08), (90.73, 48.85), (90.58, 48.58), (90.38, 48.25), (90.13, 47.86), (89.82, 47.4), (89.44, 46.86), (88.98, 46.23), (88.45, 45.51), (87.83, 44.69), (87.12, 43.75), (86.31, 42.69), (85.39, 41.5), (84.36, 40.17), (83.21, 38.7), (81.94, 37.07)])
# fmt: on

# 1. Left '<' angle segments (Google red & blue)
polygon(red_top_left, style=no_border_fill("#F15549"))
polygon(blue_bot_left, style=no_border_fill("#518FEA"))
draw_round_polyline(red_top_left, width_units=w, color=DARK, closed=True)
draw_round_polyline(blue_bot_left, width_units=w, color=DARK, closed=True)

# 2. Right '>' angle segments (Google yellow & green)
polygon(yellow_bot_right, style=no_border_fill("#F1C946"))
polygon(green_top_right, style=no_border_fill("#5ED09E"))
draw_round_polyline(yellow_bot_right, width_units=w, color=DARK, closed=True)
draw_round_polyline(green_top_right, width_units=w, color=DARK, closed=True)

save()
