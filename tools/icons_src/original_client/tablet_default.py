# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Client concept icon: tablet."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Wide portrait tablet frame
rectangle(
    (45.5, 50.0),
    width=55.0,
    height=70.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=7.0),
)

# Inner WHITE screen
rectangle(
    (45.5, 50.0),
    width=43.0,
    height=54.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0, shape_r=3.5),
)

# Top camera dot
circle((45.5, 81.0), radius=1.2, style=fill_style(DARK))

# Screen UI widget and lines
rectangle(
    (43.0, 63.0),
    width=28.0,
    height=13.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=2.0, shape_r=2.5),
)
draw_round_segment((30.0, 48.0), (54.0, 48.0), width_units=2.0, color=DARK)
draw_round_segment((30.0, 40.5), (48.0, 40.5), width_units=2.0, color=DARK)
draw_round_segment((30.0, 33.0), (52.0, 33.0), width_units=2.0, color=DARK)

# Angled PASTEL_GREEN stylus with rounded top cap overlapping right side of tablet
tip = (61.5, 27.5)
ang = math.radians(63.0)
ux, uy = math.cos(ang), math.sin(ang)
nx, ny = -uy, ux
half_t = 3.6
cone_len = 8.5
body_len = 38.5

p_cone_l = (tip[0] + cone_len * ux + half_t * nx, tip[1] + cone_len * uy + half_t * ny)
p_cone_r = (tip[0] + cone_len * ux - half_t * nx, tip[1] + cone_len * uy - half_t * ny)
top_cx = tip[0] + body_len * ux
top_cy = tip[1] + body_len * uy

cap_pts: list[tuple[float, float]] = []
steps = 12
for i in range(steps + 1):
    theta = (ang - math.pi / 2.0) + math.pi * (i / steps)
    cap_pts.append((top_cx + half_t * math.cos(theta), top_cy + half_t * math.sin(theta)))

# Stylus cone tip (WHITE) and rounded barrel (PASTEL_GREEN)
polygon([tip, p_cone_r, p_cone_l], style=fill_style(WHITE))
polygon([p_cone_l, p_cone_r, *cap_pts], style=fill_style(PASTEL_GREEN))
draw_round_polyline([tip, p_cone_r, *cap_pts, p_cone_l], width_units=2.0, color=DARK, closed=True)
draw_round_segment(p_cone_l, p_cone_r, width_units=2.0, color=DARK)
circle(tip, radius=1.2, style=fill_style(DARK))

save()
