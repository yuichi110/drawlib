# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: email_service."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Envelope body: (50, 48), width=72, height=50, shape_r=6.0 -> x=14..86, y=23..73
x0, y0, x1, y1 = 14.0, 23.0, 86.0, 73.0
r = 6.0
rectangle(
    (50.0, 48.0),
    width=72.0,
    height=50.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=r),
)

# Bottom diagonal fold lines
draw_round_segment((16.5, 25.5), (38.0, 50.0), width_units=2.3, color=DARK)
draw_round_segment((83.5, 25.5), (62.0, 50.0), width_units=2.3, color=DARK)

# Top V-flap matching the rounded top corners of the envelope
flap_pts: list[tuple[float, float]] = []
steps = 12
for i in range(steps + 1):
    ang = math.radians(160.0 - 70.0 * (i / steps))
    flap_pts.append((x0 + r + r * math.cos(ang), y1 - r + r * math.sin(ang)))
for i in range(steps + 1):
    ang = math.radians(90.0 - 70.0 * (i / steps))
    flap_pts.append((x1 - r + r * math.cos(ang), y1 - r + r * math.sin(ang)))
flap_pts.append((50.0, 44.0))

polygon(flap_pts, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(flap_pts, width_units=w, color=DARK, closed=True)

# Circular send/check badge at bottom-right
badge_xy = (76.0, 28.0)
circle(
    badge_xy,
    radius=12.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w),
)
draw_round_polyline(
    [(70.5, 28.0), (74.5, 24.0), (82.0, 32.0)],
    width_units=2.8,
    color=DARK,
)

save()
