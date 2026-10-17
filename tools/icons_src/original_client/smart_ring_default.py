# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Client concept icon: smart_ring."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_compound_polygon,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

cx = 50.0
cy_top = 54.0
cy_bot = 38.0
rx_out = 33.0
ry_out = 17.5
rx_in = 22.5
ry_in = 11.0
steps = 64


def ellipse_pts(
    center_x: float,
    center_y: float,
    rad_x: float,
    rad_y: float,
    deg_start: float,
    deg_end: float,
    num: int = 48,
) -> list[tuple[float, float]]:
    """Return points along an elliptical arc from deg_start to deg_end."""
    pts: list[tuple[float, float]] = []
    for i in range(num + 1):
        ang = math.radians(deg_start + (deg_end - deg_start) * (i / num))
        pts.append((center_x + rad_x * math.cos(ang), center_y + rad_y * math.sin(ang)))
    return pts


# 1. Visible inner back wall of the ring band (seen through the top opening)
# Bounded by top inner ellipse upper arc (0 -> 180) and bottom inner ellipse upper arc (180 -> 0)
inner_back_top = ellipse_pts(cx, cy_top, rx_in, ry_in, 0.0, 180.0, 48)
inner_back_bot = ellipse_pts(cx, cy_bot, rx_in, ry_in, 180.0, 0.0, 48)
inner_wall_poly = inner_back_top + inner_back_bot
polygon(inner_wall_poly, style=no_border_fill(PASTEL_BLUE_LIGHT))

# 2. Inner biometric optical sensor domes along the visible inside wall
for sx, sy in ((39.0, 52.0), (50.0, 54.8), (61.0, 52.0)):
    circle(
        (sx, sy),
        radius=3.2,
        style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=1.8),
    )

# Clip/cover any lower part of sensors that falls below the bottom inner rim
# by redrawing the top rim and front band on top.

# Build bottom inner rim arc (only the segment visible inside the top hole)
# Solve where bottom inner ellipse y = cy_bot + ry_in * sin(t) is above top inner front arc y = cy_top - ry_in * sin(t)
visible_bot_inner: list[tuple[float, float]] = []
for i in range(65):
    ang = math.radians(15.0 + 150.0 * (i / 64))
    px = cx + rx_in * math.cos(ang)
    py = cy_bot + ry_in * math.sin(ang)
    # Check if inside top inner ellipse: ((px - cx)/rx_in)^2 + ((py - cy_top)/ry_in)^2 < 1
    val = ((px - cx) / rx_in) ** 2 + ((py - cy_top) / ry_in) ** 2
    if val <= 1.02:
        visible_bot_inner.append((px, py))

if len(visible_bot_inner) >= 2:
    draw_round_polyline(visible_bot_inner, width_units=2.0, color=DARK, closed=False)

# 3. Top annular rim surface (WHITE / PASTEL_BLUE_LIGHT flat top edge of the band)
top_outer_loop = ellipse_pts(cx, cy_top, rx_out, ry_out, 0.0, 360.0, 72)[:-1]
top_inner_loop = ellipse_pts(cx, cy_top, rx_in, ry_in, 0.0, 360.0, 72)[:-1]
draw_compound_polygon([top_outer_loop, top_inner_loop], color=WHITE)

# 4. Front outer cylindrical band wall (from top front arc 180..360 down to bottom front arc 360..180)
front_top_arc = ellipse_pts(cx, cy_top, rx_out, ry_out, 180.0, 360.0, 48)
front_bot_arc = ellipse_pts(cx, cy_bot, rx_out, ry_out, 360.0, 180.0, 48)
front_wall_poly = front_top_arc + front_bot_arc
polygon(front_wall_poly, style=no_border_fill(PASTEL_BLUE))

# 5. Subtle smart LED pill on the front band
led_pts = ellipse_pts(cx, (cy_top - ry_out + cy_bot - ry_out) / 2.0, 6.5, 2.2, 0.0, 360.0, 32)[:-1]
polygon(led_pts, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(led_pts, width_units=1.8, color=DARK, closed=True)

# 6. Crisp DARK outlines for all structural edges
draw_round_polyline(top_outer_loop, width_units=w, color=DARK, closed=True)
draw_round_polyline(top_inner_loop, width_units=w, color=DARK, closed=True)
draw_round_polyline(front_bot_arc, width_units=w, color=DARK, closed=False)
draw_round_polyline([(cx - rx_out, cy_top), (cx - rx_out, cy_bot)], width_units=w, color=DARK, closed=False)
draw_round_polyline([(cx + rx_out, cy_top), (cx + rx_out, cy_bot)], width_units=w, color=DARK, closed=False)

# 7. Wireless / biometric pulse arcs above the ring
for r_arc in (9.0, 15.5):
    pts_arc = ellipse_pts(cx, 72.0, r_arc, r_arc, 42.0, 138.0, num=24)
    draw_round_polyline(pts_arc, width_units=4.4, color=DARK, closed=False)
    draw_round_polyline(pts_arc, width_units=1.8, color=PASTEL_GREEN, closed=False)

save()
