# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility concept icon: server_room."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w_outer = 2.0
w_inner = 1.6


def _top_rounded_box(x0: float, y0: float, x1: float, y1: float, r: float) -> list[tuple[float, float]]:
    pts: list[tuple[float, float]] = [(x0, y0), (x1, y0)]
    steps = 10
    for i in range(steps + 1):
        ang = math.radians(0.0 + 90.0 * (i / steps))
        pts.append((x1 - r + r * math.cos(ang), y1 - r + r * math.sin(ang)))
    for i in range(steps + 1):
        ang = math.radians(90.0 + 90.0 * (i / steps))
        pts.append((x0 + r + r * math.cos(ang), y1 - r + r * math.sin(ang)))
    return pts


# 1. Outer WHITE server room interior frame
rectangle(
    (50.0, 50.0),
    width=76.0,
    height=74.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_outer, shape_r=6.0),
)

# 2. Overhead cable tray / ceiling duct line
Icon.draw_round_segment((12.0, 80.0), (88.0, 80.0), width_units=w_inner, color=Icon.DARK)

# 3. Dual 19-inch server racks standing flush on the raised floor (y=21.0)
for rack_cx in (33.5, 66.5):
    rack_pts = _top_rounded_box(rack_cx - 12.5, 21.0, rack_cx + 12.5, 74.0, 3.0)
    polygon(rack_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
    Icon.draw_round_polyline(rack_pts, width_units=w_outer, color=Icon.DARK, closed=True)
    # 4 stacked chassis units per rack
    for slot_cy in (65.5, 53.5, 41.5, 29.5):
        rectangle(
            (rack_cx, slot_cy),
            width=19.0,
            height=7.5,
            style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_inner, shape_r=1.5),
        )
        Icon.draw_round_segment(
            (rack_cx - 6.0, slot_cy), (rack_cx - 1.0, slot_cy), width_units=w_inner, color=Icon.DARK
        )
        circle(
            (rack_cx + 5.2, slot_cy),
            radius=2.0,
            style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.4),
        )

# 4. Raised floor plenum line and floor tile seams
Icon.draw_round_segment((12.0, 21.0), (88.0, 21.0), width_units=w_outer, color=Icon.DARK)
for x_tile in (32.0, 50.0, 68.0):
    Icon.draw_round_segment((x_tile, 13.0), (x_tile, 21.0), width_units=w_inner, color=Icon.DARK)

save()
