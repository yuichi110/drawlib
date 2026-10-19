# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: dns."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, ellipse, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# 1. Upper wireframe globe / sphere at (50, 56), radius=31.0 -> y=25..87
gx, gy = 50.0, 56.0
gr = 31.0

circle(
    (gx, gy),
    radius=gr,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w),
)
ellipse(
    (gx, gy),
    width=gr,
    height=gr * 2.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w),
)

# Vertical prime meridian and horizontal latitude lines
Icon.draw_round_segment((gx, gy - gr), (gx, gy + gr), width_units=2.0, color=Icon.DARK)
Icon.draw_round_segment((gx - gr, gy), (gx + gr, gy), width_units=2.0, color=Icon.DARK)

lat_dy = 14.5
lat_dx = math.sqrt(gr * gr - lat_dy * lat_dy)
Icon.draw_round_segment((gx - lat_dx, gy + lat_dy), (gx + lat_dx, gy + lat_dy), width_units=2.0, color=Icon.DARK)

# Re-stroke outer globe ring for crisp intersections
circle(
    (gx, gy),
    radius=gr,
    style=Icon.stroke_style(Icon.DARK, width_units=w),
)

# 2. Front "WWW" domain banner at (50, 27), width=76.0, height=24.0
by = 27.0
rectangle(
    (50.0, by),
    width=76.0,
    height=24.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w, shape_r=6.0),
)

# Three crisp vector "W" glyphs inside the banner
y_top = by + 6.2
y_mid = by + 2.2
y_bot = by - 6.2
for wx in (29.0, 50.0, 71.0):
    w_pts = [
        (wx - 6.8, y_top),
        (wx - 3.4, y_bot),
        (wx, y_mid),
        (wx + 3.4, y_bot),
        (wx + 6.8, y_top),
    ]
    Icon.draw_round_polyline(w_pts, width_units=2.0, color=Icon.DARK)

save()
