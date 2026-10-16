# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: function_calling."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    build_sparkle_4pt_polygon,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# 1. Left AI model card with 4-point sparkle
rectangle(
    (29.0, 50.0),
    width=32.0,
    height=44.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=6.5),
)
sparkle_pts = build_sparkle_4pt_polygon(29.0, 50.0, outer_r=11.0, inner_r=3.8)
polygon(sparkle_pts, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(sparkle_pts, width_units=2.3, color=DARK, closed=True)

# 2. Invocation arrow connecting model to tool box
draw_round_segment((45.0, 50.0), (57.0, 50.0), width_units=w, color=DARK)
draw_round_polyline(
    [(52.0, 55.0), (57.5, 50.0), (52.0, 45.0)],
    width_units=w,
    color=DARK,
)

# 3. Right function/tool box with gear
gx, gy = 73.0, 50.0
rectangle(
    (gx, gy),
    width=30.0,
    height=30.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=6.5),
)

for deg in range(0, 360, 45):
    rad = math.radians(deg)
    x0 = gx + 6.5 * math.cos(rad)
    y0 = gy + 6.5 * math.sin(rad)
    x1 = gx + 10.6 * math.cos(rad)
    y1 = gy + 10.6 * math.sin(rad)
    draw_round_segment((x0, y0), (x1, y1), width_units=3.0, color=DARK)

circle(
    (gx, gy),
    radius=8.2,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.3),
)
circle(
    (gx, gy),
    radius=3.2,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0),
)

save()
