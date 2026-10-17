# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security concept icon: microsoft_defender."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    draw_round_segment,
    no_border_fill,
    setup_icon,
)

# ruff: noqa: E501
# fmt: off
setup_icon()

w = 1.8
s = 0.96


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


center_pt = _sc([(50.0, 52.5)])[0]
tl_curve = _sc([
    (11.22, 52.5), (11.02, 53.71), (10.87, 54.93), (10.74, 56.16), (10.65, 57.39),
    (10.6, 58.62), (10.58, 59.85), (10.58, 77.59), (10.59, 77.82), (10.62, 78.05),
    (10.67, 78.27), (10.73, 78.49), (10.82, 78.71), (10.92, 78.91), (11.04, 79.11),
    (11.18, 79.29), (11.33, 79.46), (11.5, 79.62), (11.68, 79.76), (11.87, 79.89),
    (12.08, 80.0), (12.29, 80.09), (12.5, 80.17), (12.73, 80.22), (12.96, 80.26),
    (13.18, 80.27), (14.97, 80.33), (16.65, 80.41), (18.22, 80.51), (19.69, 80.65),
    (21.08, 80.82), (22.38, 81.01), (23.6, 81.23), (24.76, 81.48), (25.85, 81.76),
    (26.89, 82.07), (27.89, 82.41), (28.84, 82.77), (29.76, 83.17), (30.66, 83.59),
    (31.54, 84.05), (32.41, 84.53), (33.27, 85.04), (34.14, 85.58), (35.02, 86.15),
    (35.92, 86.75), (37.5, 87.75), (39.15, 88.63), (40.86, 89.37), (42.63, 89.98),
    (44.44, 90.45), (46.27, 90.78), (48.13, 90.96), (50.0, 91.0),
])
tr_curve = _sc([
    (50.0, 91.0), (51.87, 90.96), (53.73, 90.78), (55.57, 90.45), (57.37, 89.98),
    (59.14, 89.37), (60.85, 88.63), (62.5, 87.75), (64.08, 86.75), (64.98, 86.15),
    (65.86, 85.58), (66.73, 85.04), (67.6, 84.53), (68.46, 84.05), (69.34, 83.59),
    (70.24, 83.17), (71.16, 82.78), (72.12, 82.41), (73.11, 82.07), (74.15, 81.76),
    (75.24, 81.48), (76.4, 81.23), (77.62, 81.01), (78.92, 80.82), (80.31, 80.65),
    (81.78, 80.52), (83.35, 80.41), (85.03, 80.33), (86.82, 80.27), (87.05, 80.26),
    (87.27, 80.22), (87.5, 80.17), (87.71, 80.09), (87.92, 80.0), (88.13, 79.89),
    (88.32, 79.76), (88.5, 79.62), (88.67, 79.46), (88.82, 79.29), (88.96, 79.11),
    (89.08, 78.91), (89.18, 78.7), (89.27, 78.49), (89.33, 78.27), (89.38, 78.05),
    (89.41, 77.82), (89.42, 77.59), (89.42, 59.86), (89.4, 58.63), (89.34, 57.4),
    (89.25, 56.17), (89.13, 54.94), (88.97, 53.72), (88.78, 52.5),
])
br_curve = _sc([
    (88.78, 52.5), (88.62, 51.58), (88.05, 49.01), (87.32, 46.51), (86.45, 44.06),
    (85.43, 41.67), (84.26, 39.33), (82.96, 37.04), (81.51, 34.81), (79.94, 32.62),
    (78.23, 30.48), (76.38, 28.38), (74.42, 26.32), (72.32, 24.3), (70.1, 22.33),
    (67.77, 20.38), (65.31, 18.47), (62.74, 16.6), (60.06, 14.75), (57.27, 12.93),
    (54.37, 11.13), (51.37, 9.36), (51.16, 9.25), (50.94, 9.16), (50.71, 9.09),
    (50.48, 9.04), (50.24, 9.01), (50.0, 9.0),
])
bl_curve = _sc([
    (50.0, 9.0), (49.76, 9.01), (49.52, 9.04), (49.29, 9.09), (49.06, 9.16),
    (48.84, 9.25), (48.62, 9.36), (45.62, 11.13), (42.73, 12.93), (39.93, 14.75),
    (37.25, 16.6), (34.69, 18.48), (32.23, 20.39), (29.9, 22.33), (27.68, 24.31),
    (25.58, 26.32), (23.61, 28.38), (21.77, 30.48), (20.06, 32.62), (18.49, 34.81),
    (17.04, 37.05), (15.74, 39.33), (14.58, 41.67), (13.56, 44.06), (12.68, 46.51),
    (11.96, 49.02), (11.38, 51.58), (11.22, 52.5),
])
# fmt: on

# 1. Four quadrant fills in pastel blues
polygon([center_pt, *tl_curve], style=no_border_fill(Colors.Blue1))
polygon([center_pt, *tr_curve], style=no_border_fill(Colors.Blue2))
polygon([center_pt, *bl_curve], style=no_border_fill(Colors.Blue3))
polygon([center_pt, *br_curve], style=no_border_fill(Colors.Blue4))

# 2. Inner cross dividers and outer shield perimeter in DARK 1.8
draw_round_segment(bl_curve[0], tl_curve[-1], width_units=w, color=DARK)
draw_round_segment(tl_curve[0], tr_curve[-1], width_units=w, color=DARK)

outer_shield = [*tl_curve[:-1], *tr_curve[:-1], *br_curve[:-1], *bl_curve[:-1]]
draw_round_polyline(outer_shield, width_units=w, color=DARK, closed=True)

save()
