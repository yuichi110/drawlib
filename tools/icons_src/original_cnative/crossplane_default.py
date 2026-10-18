# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: crossplane."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
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
    no_border_fill,
    setup_icon,
)


def _clip_halfplane(
    pts: list[tuple[float, float]],
    *,
    c: float,
    keep_ge: bool,
) -> list[tuple[float, float]]:
    """Clip polygon pts against half-plane (y - x >= c) or (y - x <= c)."""
    out: list[tuple[float, float]] = []
    n = len(pts)
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        v1 = (y1 - x1) - c
        v2 = (y2 - x2) - c
        in1 = v1 >= 0.0 if keep_ge else v1 <= 0.0
        in2 = v2 >= 0.0 if keep_ge else v2 <= 0.0
        if in1:
            out.append((x1, y1))
        if in1 != in2 and abs(v1 - v2) > 1e-9:
            t = v1 / (v1 - v2)
            out.append((x1 + t * (x2 - x1), y1 + t * (y2 - y1)))
    return out


setup_icon()

w = ORIG_STROKE

# Bottom rounded popsicle stick
rectangle(
    (50.0, 22.0),
    width=14.0,
    height=24.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=2.0, shape_r=6.5),
)

# Build smooth popsicle body contour (x=28..72, y=30..88)
body_pts: list[tuple[float, float]] = []
steps = 24
# Bottom-left rounded corner (center (40, 42), r=12, 180..270 deg)
for i in range(steps + 1):
    ang = math.radians(180.0 + 90.0 * (i / steps))
    body_pts.append((40.0 + 12.0 * math.cos(ang), 42.0 + 12.0 * math.sin(ang)))
# Bottom-right rounded corner (center (60, 42), r=12, 270..360 deg)
for i in range(steps + 1):
    ang = math.radians(270.0 + 90.0 * (i / steps))
    body_pts.append((60.0 + 12.0 * math.cos(ang), 42.0 + 12.0 * math.sin(ang)))
# Top semicircle dome (center (50, 66), r=22, 0..180 deg)
for i in range(steps * 2 + 1):
    ang = math.radians(0.0 + 180.0 * (i / (steps * 2)))
    body_pts.append((50.0 + 22.0 * math.cos(ang), 66.0 + 22.0 * math.sin(ang)))

c_upper = 20.0
c_lower = -6.0

top_stripe = _clip_halfplane(body_pts, c=c_upper, keep_ge=True)
mid_stripe = _clip_halfplane(
    _clip_halfplane(body_pts, c=c_upper, keep_ge=False),
    c=c_lower,
    keep_ge=True,
)
bot_stripe = _clip_halfplane(body_pts, c=c_lower, keep_ge=False)

polygon(top_stripe, style=no_border_fill(WHITE))
polygon(mid_stripe, style=no_border_fill(PASTEL_BLUE))
polygon(bot_stripe, style=no_border_fill(PASTEL_GREEN))

# Diagonal stripe dividers
draw_round_segment((28.0, 48.0), (63.43, 83.43), width_units=2.0, color=DARK)
draw_round_segment((36.52, 30.52), (72.0, 66.0), width_units=2.0, color=DARK)

# Outer popsicle border
draw_round_polyline(body_pts, width_units=w, color=DARK, closed=True)

save()
