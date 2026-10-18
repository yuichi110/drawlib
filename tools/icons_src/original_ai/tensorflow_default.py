# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI concept icon: tensorflow."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 2.0
SCALE = 0.95


def _scale(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Scale polygon points around (50.0, 50.0) so border stays inside [9.0, 91.0]."""
    return [(50.0 + (x - 50.0) * SCALE, 50.0 + (y - 50.0) * SCALE) for x, y in pts]


# Official two flat isometric halves separated by a vertical gap, both in Colors.Orange3
left_t_pts = _scale(
    [
        (48.43, 9.0),
        (34.44, 17.12),
        (34.44, 65.02),
        (13.36, 52.84),
        (13.41, 70.99),
        (48.43, 91.0),
    ]
)

right_f_pts = _scale(
    [
        (51.58, 91.0),
        (51.58, 9.0),
        (65.57, 17.12),
        (65.57, 40.19),
        (76.13, 34.09),
        (76.07, 49.87),
        (65.57, 55.86),
        (65.57, 65.02),
        (86.64, 52.84),
        (86.59, 70.99),
    ]
)

for half_pts in (left_t_pts, right_f_pts):
    polygon(half_pts, style=no_border_fill(Colors.Orange3))
    draw_round_polyline(half_pts, width_units=w, color=DARK, closed=True)

save()
