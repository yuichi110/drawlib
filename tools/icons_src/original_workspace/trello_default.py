# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Workspace concept icon: trello."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import DARK, WHITE, draw_round_polyline, no_border_fill, setup_icon

setup_icon()
w = 2.0
u = 77.6 / 256.0
x0_base = 11.2
y0_base = 11.2


def _rrect(x_svg: float, y_svg_top: float, w_svg: float, h_svg: float, r_svg: float) -> list[tuple[float, float]]:
    x_left = x0_base + x_svg * u
    x_right = x_left + w_svg * u
    y_top = 100.0 - y0_base - y_svg_top * u
    y_bot = y_top - h_svg * u
    rad = r_svg * u
    corners = [
        (x_right - rad, y_top - rad, 90.0, 0.0),
        (x_right - rad, y_bot + rad, 0.0, -90.0),
        (x_left + rad, y_bot + rad, -90.0, -180.0),
        (x_left + rad, y_top - rad, 180.0, 90.0),
    ]
    pts: list[tuple[float, float]] = []
    steps = 12
    for cx, cy, deg0, deg1 in corners:
        for i in range(steps + 1):
            ang = math.radians(deg0 + (deg1 - deg0) * (i / steps))
            pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    return pts


bg_sq = _rrect(0.0, 0.0, 256.0, 256.0, 25.0)
left_bar = _rrect(33.28, 33.28, 78.08, 176.0, 12.0)
right_bar = _rrect(144.64, 33.28, 78.08, 112.0, 12.0)

for pts, col in (
    (bg_sq, "#4EAAEB"),
    (left_bar, WHITE),
    (right_bar, WHITE),
):
    polygon(pts, style=no_border_fill(col))
    draw_round_polyline(pts, width_units=w, color=DARK, closed=True)

save()
