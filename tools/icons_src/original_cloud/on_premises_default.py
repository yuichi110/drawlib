# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: on_premises."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE


def _top_rounded_tower(
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    r: float,
) -> list[tuple[float, float]]:
    pts: list[tuple[float, float]] = [(x0, y0), (x1, y0)]
    steps = 12
    c_tr = (x1 - r, y1 - r)
    for i in range(steps + 1):
        ang = math.radians(0.0 + 90.0 * (i / steps))
        pts.append((c_tr[0] + r * math.cos(ang), c_tr[1] + r * math.sin(ang)))
    c_tl = (x0 + r, y1 - r)
    for i in range(steps + 1):
        ang = math.radians(90.0 + 90.0 * (i / steps))
        pts.append((c_tl[0] + r * math.cos(ang), c_tl[1] + r * math.sin(ang)))
    return pts


# Right secondary building wing
polygon(
    _top_rounded_tower(54.0, 16.0, 80.0, 64.0, r=4.5),
    style=fill_style(WHITE, border_color=DARK, border_units=w),
)

# Left main server tower
polygon(
    _top_rounded_tower(19.0, 16.0, 57.0, 84.0, r=4.5),
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w),
)

# Ground foundation line
draw_round_segment((12.0, 16.0), (88.0, 16.0), width_units=w, color=DARK)

# Server bay slots in main tower
for y_slot in (68.0, 54.0, 40.0):
    rectangle(
        (38.0, y_slot),
        width=22.0,
        height=6.5,
        style=fill_style(WHITE, border_color=DARK, border_units=2.0, shape_r=2.0),
    )

# Status indicator dots in right wing
for y_dot in (50.0, 36.0):
    circle(
        (68.5, y_dot),
        radius=3.6,
        style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0),
    )

save()
