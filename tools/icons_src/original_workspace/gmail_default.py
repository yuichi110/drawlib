# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Workspace concept icon: gmail."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 2.0
s = 0.95


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


seg_blue = _sc(
    [
        (14.59, 19.25),
        (27.64, 19.25),
        (27.64, 50.93),
        (9.00, 64.90),
        (9.00, 24.84),
        (9.02, 24.38),
        (9.07, 23.93),
        (9.16, 23.49),
        (9.29, 23.07),
        (9.44, 22.66),
        (9.62, 22.26),
        (9.84, 21.89),
        (10.08, 21.53),
        (10.35, 21.20),
        (10.64, 20.88),
        (10.95, 20.59),
        (11.29, 20.32),
        (11.65, 20.08),
        (12.02, 19.87),
        (12.42, 19.68),
        (12.83, 19.53),
        (13.25, 19.41),
        (13.68, 19.32),
        (14.13, 19.26),
    ]
)
seg_green = _sc(
    [
        (72.36, 19.25),
        (85.41, 19.25),
        (85.87, 19.26),
        (86.32, 19.32),
        (86.75, 19.41),
        (87.18, 19.53),
        (87.59, 19.69),
        (87.98, 19.87),
        (88.36, 20.08),
        (88.71, 20.33),
        (89.05, 20.59),
        (89.36, 20.88),
        (89.66, 21.20),
        (89.92, 21.54),
        (90.16, 21.89),
        (90.38, 22.27),
        (90.56, 22.66),
        (90.72, 23.07),
        (90.84, 23.49),
        (90.93, 23.93),
        (90.98, 24.38),
        (91.00, 24.84),
        (91.00, 64.90),
        (72.36, 50.93),
    ]
)
seg_yellow = _sc(
    [
        (72.36, 75.15),
        (72.36, 50.93),
        (91.00, 64.90),
        (91.00, 72.36),
        (90.94, 73.37),
        (90.77, 74.34),
        (90.50, 75.25),
        (90.13, 76.11),
        (89.68, 76.91),
        (89.15, 77.64),
        (88.54, 78.31),
        (87.87, 78.90),
        (87.14, 79.42),
        (86.36, 79.86),
        (85.54, 80.22),
        (84.69, 80.49),
        (83.81, 80.67),
        (82.92, 80.75),
        (82.01, 80.74),
        (81.10, 80.63),
        (80.19, 80.41),
        (79.30, 80.07),
        (78.43, 79.63),
        (77.58, 79.07),
    ]
)
seg_red = _sc(
    [
        (27.64, 50.93),
        (27.64, 75.15),
        (50.00, 58.38),
        (72.36, 75.15),
        (72.36, 50.93),
        (50.00, 34.15),
    ]
)
seg_dred = _sc(
    [
        (9.00, 72.36),
        (9.00, 64.90),
        (27.64, 50.93),
        (27.64, 75.15),
        (22.42, 79.07),
        (21.57, 79.63),
        (20.70, 80.07),
        (19.80, 80.41),
        (18.90, 80.63),
        (17.99, 80.74),
        (17.08, 80.75),
        (16.18, 80.67),
        (15.30, 80.49),
        (14.45, 80.22),
        (13.63, 79.86),
        (12.86, 79.42),
        (12.13, 78.90),
        (11.46, 78.31),
        (10.85, 77.64),
        (10.32, 76.91),
        (9.86, 76.11),
        (9.50, 75.25),
        (9.23, 74.34),
        (9.06, 73.37),
    ]
)

for pts, col in [
    (seg_blue, "#5797F2"),
    (seg_green, "#71C789"),
    (seg_yellow, "#F2C94F"),
    (seg_dred, "#E35C51"),
    (seg_red, "#F26458"),
]:
    polygon(pts, style=no_border_fill(col))
    draw_round_polyline(pts, width_units=w, color=DARK, closed=True)

save()
