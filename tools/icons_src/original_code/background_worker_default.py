# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code concept icon: background_worker."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
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

b = 2.0
w_line = 2.0

# Back-left PASTEL_BLUE_LIGHT stacked task card
rectangle(
    (36.5, 62.5),
    width=52.0,
    height=48.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=b, shape_r=5.0),
)

# Front-left WHITE task card
rectangle(
    (40.0, 56.0),
    width=52.0,
    height=48.0,
    style=fill_style(WHITE, border_color=DARK, border_units=b, shape_r=5.0),
)

# 3 horizontal DARK task lines
draw_round_segment((23.0, 67.0), (57.0, 67.0), width_units=w_line, color=DARK)
draw_round_segment((23.0, 56.0), (55.0, 56.0), width_units=w_line, color=DARK)
draw_round_segment((23.0, 45.0), (47.0, 45.0), width_units=w_line, color=DARK)

# Bottom-right overlapping 8-tooth PASTEL_GREEN gear at (68, 30)
gx, gy = 68.0, 30.0
outer_r = 18.0
inner_r = 13.5
gear_pts: list[tuple[float, float]] = []
for k in range(8):
    base_deg = k * 45.0
    for deg_off, rad_val in (
        (-10.5, inner_r),
        (-7.5, outer_r),
        (7.5, outer_r),
        (10.5, inner_r),
    ):
        ang = math.radians(base_deg + deg_off)
        gear_pts.append((gx + rad_val * math.cos(ang), gy + rad_val * math.sin(ang)))
    for valley_step in (18.5, 26.5):
        ang = math.radians(base_deg + valley_step)
        gear_pts.append((gx + inner_r * math.cos(ang), gy + inner_r * math.sin(ang)))

polygon(gear_pts, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(gear_pts, width_units=b, color=DARK, closed=True)

circle(
    (gx, gy),
    radius=6.0,
    style=fill_style(WHITE, border_color=DARK, border_units=b),
)

save()
