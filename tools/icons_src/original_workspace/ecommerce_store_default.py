# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Workspace concept icon: ecommerce_store."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w_outer = 2.0
w_inner = 1.6

# 1. Top WHITE shopping bag handle arch (centered at x=45.0, y=72.0..85.5)
h_cx, h_cy = 45.0, 72.0
r_out, r_in = 13.5, 8.5
steps = 28
handle_pts = [
    (h_cx + r_out * math.cos(math.radians(180.0 * i / steps)), h_cy + r_out * math.sin(math.radians(180.0 * i / steps)))
    for i in range(steps + 1)
] + [
    (
        h_cx + r_in * math.cos(math.radians(180.0 * (steps - i) / steps)),
        h_cy + r_in * math.sin(math.radians(180.0 * (steps - i) / steps)),
    )
    for i in range(steps + 1)
]
polygon(handle_pts, style=no_border_fill(WHITE))
draw_round_polyline(handle_pts, width_units=w_outer, color=DARK, closed=True)

# 2. PASTEL_BLUE shopping bag body (x=17.0..73.0, y=16.0..72.0, rounded bottom corners)
x_left, x_right = 17.0, 73.0
y_bot, y_top = 16.0, 72.0
r_bot = 6.0
bag_pts: list[tuple[float, float]] = [(x_left, y_top)]
for i in range(11):
    ang = math.radians(180.0 + 90.0 * (i / 10))
    bag_pts.append((x_left + r_bot + r_bot * math.cos(ang), y_bot + r_bot + r_bot * math.sin(ang)))
for i in range(11):
    ang = math.radians(270.0 + 90.0 * (i / 10))
    bag_pts.append((x_right - r_bot + r_bot * math.cos(ang), y_bot + r_bot + r_bot * math.sin(ang)))
bag_pts.append((x_right, y_top))

polygon(bag_pts, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(bag_pts, width_units=w_outer, color=DARK, closed=True)

# 3. Four storefront scalloped awning stripes flush across top of bag (WHITE & PASTEL_BLUE_LIGHT)
n_stripes = 4
y_awn_bot = 60.0
ry_scallop = 4.2

for idx in range(n_stripes):
    col = WHITE if idx % 2 == 0 else PASTEL_BLUE_LIGHT
    xs0 = x_left + (x_right - x_left) * (idx / n_stripes)
    xs1 = x_left + (x_right - x_left) * ((idx + 1) / n_stripes)
    sc_cx = 0.5 * (xs0 + xs1)
    sc_rx = 0.5 * (xs1 - xs0)

    scallop_pts = [
        (
            sc_cx + sc_rx * math.cos(math.radians(180.0 + 180.0 * (s / 12))),
            y_awn_bot + ry_scallop * math.sin(math.radians(180.0 + 180.0 * (s / 12))),
        )
        for s in range(13)
    ]
    stripe_pts = [(xs0, y_top), *scallop_pts, (xs1, y_top)]
    polygon(stripe_pts, style=no_border_fill(col))
    draw_round_polyline(stripe_pts, width_units=w_outer, color=DARK, closed=True)

# 4. PASTEL_GREEN angled price tag badge at bottom-right
tag_cx, tag_cy = 70.5, 29.5
ang_tag = math.radians(135.0)
ux, uy = math.cos(ang_tag), math.sin(ang_tag)
nx, ny = -uy, ux


def _tag_pt(s: float, d: float) -> tuple[float, float]:
    return (tag_cx + s * ux + d * nx, tag_cy + s * uy + d * ny)


tag_pts = [
    _tag_pt(13.5, 0.0),
    _tag_pt(6.0, 7.8),
    _tag_pt(-12.5, 7.8),
    _tag_pt(-12.5, -7.8),
    _tag_pt(6.0, -7.8),
]
polygon(tag_pts, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(tag_pts, width_units=w_outer, color=DARK, closed=True)

hole_xy = _tag_pt(6.5, 0.0)
circle(
    hole_xy,
    radius=2.5,
    style=fill_style(WHITE, border_color=DARK, border_units=w_inner),
)

save()
