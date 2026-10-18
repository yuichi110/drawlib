# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Client concept icon: smart_card."""

import math

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    draw_rounded_corner_block,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE
x0, y0, x1, y1 = 12.0, 24.0, 88.0, 76.0
r = 7.0

# 1. Rounded card base (WHITE) using exact circular corner arcs
draw_rounded_corner_block(
    x0,
    y0,
    x1,
    y1,
    r=r,
    round_tl=True,
    round_tr=True,
    round_bl=True,
    round_br=True,
    color=WHITE,
)

# 2. Top stripe (PASTEL_BLUE) matching exact circular top corners
draw_rounded_corner_block(
    x0,
    61.0,
    x1,
    y1,
    r=r,
    round_tl=True,
    round_tr=True,
    color=PASTEL_BLUE,
)
draw_round_segment((x0, 61.0), (x1, 61.0), width_units=2.0, color=DARK)

# Outer card border following exact circular corner arcs
steps = 16
border_pts: list[tuple[float, float]] = []
for cx, cy, start_deg in (
    (x0 + r, y0 + r, 180.0),
    (x1 - r, y0 + r, 270.0),
    (x1 - r, y1 - r, 0.0),
    (x0 + r, y1 - r, 90.0),
):
    for i in range(steps + 1):
        ang = math.radians(start_deg + 90.0 * (i / steps))
        border_pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
draw_round_polyline(border_pts, width_units=w, color=DARK, closed=True)

# 3. EMV contact chip pad (PASTEL_GREEN) with contact division lines
rectangle(
    (30.5, 42.5),
    width=21.0,
    height=17.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0, shape_r=3.0),
)
# Vertical chip division lines
draw_round_segment((27.0, 34.2), (27.0, 50.8), width_units=1.8, color=DARK)
draw_round_segment((34.0, 34.2), (34.0, 50.8), width_units=1.8, color=DARK)
# Horizontal chip pad division lines on left and right columns
draw_round_segment((20.2, 42.5), (27.0, 42.5), width_units=1.8, color=DARK)
draw_round_segment((34.0, 42.5), (40.8, 42.5), width_units=1.8, color=DARK)

# 4. Card data bars on bottom right
rectangle(
    (63.5, 45.5),
    width=27.0,
    height=4.5,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=1.6, shape_r=1.5),
)
draw_round_segment((50.5, 36.5), (70.5, 36.5), width_units=2.0, color=DARK)

save()
