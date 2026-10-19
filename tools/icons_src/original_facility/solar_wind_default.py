# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility concept icon: solar_wind."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import Icon

Icon.setup()

w_outer = 2.0
w_inner = 1.6


def _turbine_blade(cx: float, cy: float, angle_deg: float, length: float) -> list[tuple[float, float]]:
    ang = math.radians(angle_deg)
    ux, uy = math.cos(ang), math.sin(ang)
    nx, ny = -uy, ux

    pts_local = [
        (3.5, -2.0),
        (length * 0.35, -3.4),
        (length - 1.5, -1.2),
        (length, 0.0),
        (length - 1.5, 1.2),
        (length * 0.35, 2.2),
        (3.5, 1.8),
    ]
    return [(cx + lx * ux + ly * nx, cy + lx * uy + ly * ny) for lx, ly in pts_local]


# 1. Wind turbine tower on the right (WHITE tapered column)
hub_cx, hub_cy = 63.5, 65.0
tower_pts = [
    (59.5, 14.0),
    (67.5, 14.0),
    (65.3, 62.5),
    (61.7, 62.5),
]
polygon(tower_pts, style=Icon.no_border_fill(Icon.WHITE))
Icon.draw_round_polyline(tower_pts, width_units=w_outer, color=Icon.DARK, closed=True)

# 2. Three PASTEL_GREEN wind turbine blades at 90, 210, 330 degrees
for blade_ang in (90.0, 210.0, 330.0):
    blade = _turbine_blade(hub_cx, hub_cy, blade_ang, 22.0)
    polygon(blade, style=Icon.no_border_fill(Icon.PASTEL_GREEN))
    Icon.draw_round_polyline(blade, width_units=w_inner, color=Icon.DARK, closed=True)

circle(
    (hub_cx, hub_cy),
    radius=4.5,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_outer),
)

# 3. Solar panel mounting stand on the left
stand_pts = [
    (28.5, 14.0),
    (38.5, 14.0),
    (36.0, 22.0),
    (31.0, 22.0),
]
polygon(stand_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE_LIGHT))
Icon.draw_round_polyline(stand_pts, width_units=w_outer, color=Icon.DARK, closed=True)

# 4. Angled PASTEL_BLUE solar photovoltaic panel (trapezoid in 2D perspective)
pv_bl = (13.0, 21.0)
pv_br = (54.0, 21.0)
pv_tr = (48.0, 47.0)
pv_tl = (19.0, 47.0)
pv_pts = [pv_bl, pv_br, pv_tr, pv_tl]
polygon(pv_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(pv_pts, width_units=w_outer, color=Icon.DARK, closed=True)

# 5. PV cell grid lines (3x3 cells)
for frac_y in (1.0 / 3.0, 2.0 / 3.0):
    y_line = 21.0 + 26.0 * frac_y
    x_left = 13.0 + 6.0 * frac_y
    x_right = 54.0 - 6.0 * frac_y
    Icon.draw_round_segment((x_left, y_line), (x_right, y_line), width_units=w_inner, color=Icon.DARK)

for frac_x in (1.0 / 3.0, 2.0 / 3.0):
    xb = 13.0 + 41.0 * frac_x
    xt = 19.0 + 29.0 * frac_x
    Icon.draw_round_segment((xb, 21.0), (xt, 47.0), width_units=w_inner, color=Icon.DARK)

# 6. Ground foundation line
Icon.draw_round_segment((11.5, 14.0), (88.5, 14.0), width_units=w_outer, color=Icon.DARK)

save()
