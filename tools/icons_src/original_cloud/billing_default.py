# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: billing."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
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

# 1. Main payment / billing card (x=12..78, y=28..76)
card_cx, card_cy = 45.0, 52.0
card_w, card_h = 66.0, 48.0
rectangle(
    (card_cx, card_cy),
    width=card_w,
    height=card_h,
    style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=6.0),
)

# Top magnetic stripe band in PASTEL_BLUE (y=58..68)
rectangle(
    (card_cx, 63.0),
    width=card_w,
    height=10.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w),
)

# EMV smart chip on left (PASTEL_BLUE_LIGHT)
rectangle(
    (26.0, 45.0),
    width=14.0,
    height=11.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=2.2, shape_r=2.5),
)

# Account / billing lines at bottom-left
draw_round_segment((20.0, 35.0), (34.0, 35.0), width_units=2.4, color=DARK)
draw_round_segment((40.0, 35.0), (48.0, 35.0), width_units=2.4, color=DARK)

# 2. Overlapping bottom-right billing $ badge (70, 34)
badge_cx, badge_cy = 70.0, 34.0
circle(
    (badge_cx, badge_cy),
    radius=16.5,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w),
)

# Currency symbol (vertical bar + S-curve) inside green badge
draw_round_segment((badge_cx, badge_cy - 9.8), (badge_cx, badge_cy + 9.8), width_units=2.4, color=DARK)

s_pts: list[tuple[float, float]] = []
rx, ry = 4.4, 3.3
for deg in range(35, 271, 15):
    rad = math.radians(deg)
    s_pts.append((badge_cx + rx * math.cos(rad), (badge_cy + ry) + ry * math.sin(rad)))
for deg in range(90, -146, -15):
    rad = math.radians(deg)
    s_pts.append((badge_cx + rx * math.cos(rad), (badge_cy - ry) + ry * math.sin(rad)))

draw_round_polyline(s_pts, width_units=2.4, color=DARK)

save()
