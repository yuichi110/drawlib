# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility concept icon: cell_tower."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w_outer = 2.0
w_inner = 1.6


def _arc_band_polygon(
    cx: float,
    cy: float,
    r_mid: float,
    thickness: float,
    ang_start_deg: float,
    ang_end_deg: float,
) -> list[tuple[float, float]]:
    r_in = r_mid - thickness / 2.0
    r_out = r_mid + thickness / 2.0
    half_t = thickness / 2.0
    pts: list[tuple[float, float]] = []
    steps_arc = 20
    steps_cap = 10

    # Outer arc from start to end
    for i in range(steps_arc + 1):
        ang = math.radians(ang_start_deg + (ang_end_deg - ang_start_deg) * (i / steps_arc))
        pts.append((cx + r_out * math.cos(ang), cy + r_out * math.sin(ang)))

    # End round cap around (cx + r_mid*cos(end), cy + r_mid*sin(end))
    end_rad = math.radians(ang_end_deg)
    cap_end_cx = cx + r_mid * math.cos(end_rad)
    cap_end_cy = cy + r_mid * math.sin(end_rad)
    for i in range(1, steps_cap):
        ang = end_rad + math.pi * (i / steps_cap)
        pts.append((cap_end_cx + half_t * math.cos(ang), cap_end_cy + half_t * math.sin(ang)))

    # Inner arc from end back to start
    for i in range(steps_arc + 1):
        ang = math.radians(ang_end_deg - (ang_end_deg - ang_start_deg) * (i / steps_arc))
        pts.append((cx + r_in * math.cos(ang), cy + r_in * math.sin(ang)))

    # Start round cap around (cx + r_mid*cos(start), cy + r_mid*sin(start))
    start_rad = math.radians(ang_start_deg)
    cap_start_cx = cx + r_mid * math.cos(start_rad)
    cap_start_cy = cy + r_mid * math.sin(start_rad)
    for i in range(1, steps_cap):
        ang = start_rad + math.pi + math.pi * (i / steps_cap)
        pts.append((cap_start_cx + half_t * math.cos(ang), cap_start_cy + half_t * math.sin(ang)))

    return pts


# 1. Ground concrete pad
rectangle(
    (50.0, 14.5),
    width=42.0,
    height=5.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_outer, shape_r=2.5),
)

# 2. Tapered steel lattice A-frame tower body
tower_pts = [
    (34.0, 17.0),
    (66.0, 17.0),
    (55.0, 63.0),
    (45.0, 63.0),
]
polygon(tower_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(tower_pts, width_units=w_outer, color=Icon.DARK, closed=True)

# 3. Horizontal crossbars and X-bracing inside the lattice tower
levels = [
    (17.0, 34.0, 66.0),
    (33.0, 37.8, 62.2),
    (49.0, 41.7, 58.3),
    (63.0, 45.0, 55.0),
]
for y_lvl, x_l, x_r in levels[1:-1]:
    Icon.draw_round_segment((x_l, y_lvl), (x_r, y_lvl), width_units=w_inner, color=Icon.DARK)

for i in range(len(levels) - 1):
    y0, xl0, xr0 = levels[i]
    y1, xl1, xr1 = levels[i + 1]
    Icon.draw_round_segment((xl0, y0), (xr1, y1), width_units=w_inner, color=Icon.DARK)
    Icon.draw_round_segment((xr0, y0), (xl1, y1), width_units=w_inner, color=Icon.DARK)

# 4. Upper antenna mast and PASTEL_GREEN transmitter beacon
tx_cx, tx_cy = 50.0, 73.0
Icon.draw_round_segment((50.0, 63.0), (50.0, 68.5), width_units=w_outer, color=Icon.DARK)
circle(
    (tx_cx, tx_cy),
    radius=5.2,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer),
)

# 5. Radiating PASTEL_GREEN wireless signal arcs on left and right
for r_mid, ang_span in ((15.5, 34.0), (26.5, 38.0)):
    for center_deg in (0.0, 180.0):
        band = _arc_band_polygon(
            tx_cx,
            tx_cy,
            r_mid,
            4.2,
            center_deg - ang_span,
            center_deg + ang_span,
        )
        polygon(band, style=Icon.no_border_fill(Icon.PASTEL_GREEN))
        Icon.draw_round_polyline(band, width_units=w_inner, color=Icon.DARK, closed=True)

save()
