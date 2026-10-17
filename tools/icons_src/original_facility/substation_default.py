# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility concept icon: substation."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w_outer = 2.0
w_inner = 1.6


def _top_rounded_box(x0: float, y0: float, x1: float, y1: float, r: float) -> list[tuple[float, float]]:
    pts: list[tuple[float, float]] = [(x0, y0), (x1, y0)]
    steps = 10
    for i in range(steps + 1):
        ang = math.radians(0.0 + 90.0 * (i / steps))
        pts.append((x1 - r + r * math.cos(ang), y1 - r + r * math.sin(ang)))
    for i in range(steps + 1):
        ang = math.radians(90.0 + 90.0 * (i / steps))
        pts.append((x0 + r + r * math.cos(ang), y1 - r + r * math.sin(ang)))
    return pts


# 1. Overhead high-voltage busbar connecting the three insulator terminals
draw_round_segment((22.0, 84.0), (78.0, 84.0), width_units=w_outer, color=DARK)

# 2. Three tall ribbed WHITE porcelain insulator bushings
for bx in (33.0, 50.0, 67.0):
    draw_round_segment((bx, 54.0), (bx, 84.0), width_units=w_outer, color=DARK)
    for sy, sw in ((60.0, 10.5), (67.5, 9.0), (75.0, 7.5)):
        rectangle(
            (bx, sy),
            width=sw,
            height=4.8,
            style=fill_style(WHITE, border_color=DARK, border_units=w_inner, shape_r=2.2),
        )
    circle(
        (bx, 84.0),
        radius=2.3,
        style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w_inner),
    )

# 3. Left and right cooling radiator fin banks (PASTEL_BLUE_LIGHT)
for rx in (19.0, 81.0):
    rectangle(
        (rx, 34.0),
        width=10.0,
        height=28.0,
        style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_outer, shape_r=2.5),
    )
    for dx in (-1.8, 1.8):
        draw_round_segment((rx + dx, 23.5), (rx + dx, 44.5), width_units=w_inner, color=DARK)

# 4. Main central high-voltage transformer tank (PASTEL_BLUE)
tank_pts = _top_rounded_box(24.0, 14.0, 76.0, 54.0, r=4.0)
polygon(tank_pts, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(tank_pts, width_units=w_outer, color=DARK, closed=True)

# 5. Central PASTEL_GREEN high-voltage lightning bolt on transformer front
bolt_pts = [
    (53.5, 48.0),
    (41.5, 33.5),
    (49.5, 33.5),
    (46.5, 20.0),
    (58.5, 34.5),
    (50.5, 34.5),
]
polygon(bolt_pts, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(bolt_pts, width_units=w_inner, color=DARK, closed=True)

# 6. Ground foundation line
draw_round_segment((11.5, 14.0), (88.5, 14.0), width_units=w_outer, color=DARK)

save()
