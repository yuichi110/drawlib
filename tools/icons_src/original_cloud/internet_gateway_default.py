# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: internet_gateway."""

from drawlib.canvas import save
from drawlib.shapes import circle, ellipse
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    setup_icon,
    stroke_style,
)

setup_icon()

w = ORIG_STROKE

# Wireframe globe shifted slightly upper-left to pair with gateway badge
gx, gy = 43.0, 55.0
gr = 29.0

circle(
    (gx, gy),
    radius=gr,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w),
)

ellipse(
    (gx, gy),
    width=28.0,
    height=gr * 2.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.3),
)

# Vertical axis and latitude lines
draw_round_segment((gx, gy - gr), (gx, gy + gr), width_units=2.2, color=DARK)
draw_round_segment((gx - gr, gy), (gx + gr, gy), width_units=2.3, color=DARK)
draw_round_segment((gx - 25.0, gy + 14.0), (gx + 25.0, gy + 14.0), width_units=2.2, color=DARK)
draw_round_segment((gx - 25.0, gy - 14.0), (gx + 25.0, gy - 14.0), width_units=2.2, color=DARK)

# Clean outer globe ring
circle(
    (gx, gy),
    radius=gr,
    style=stroke_style(DARK, width_units=w),
)

# Foreground gateway portal badge at bottom-right
bx, by = 70.0, 29.0
br = 16.5

circle(
    (bx, by),
    radius=br,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w),
)

# Bidirectional ingress/egress arrows inside gateway badge
aw = 2.4
# Top egress arrow (pointing right)
draw_round_segment((62.0, 34.0), (77.5, 34.0), width_units=aw, color=DARK)
draw_round_polyline([(73.0, 38.0), (77.5, 34.0), (73.0, 30.0)], width_units=aw, color=DARK)

# Bottom ingress arrow (pointing left)
draw_round_segment((62.5, 24.0), (78.0, 24.0), width_units=aw, color=DARK)
draw_round_polyline([(67.0, 28.0), (62.5, 24.0), (67.0, 20.0)], width_units=aw, color=DARK)

save()
