# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility concept icon: cargo_ship."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w_outer = 2.0
w_inner = 1.6

# 1. Stern bridge superstructure (x=15..33, y=46..82)
# Funnel / mast on top
rectangle(
    (23.0, 78.0),
    width=6.0,
    height=8.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_outer, shape_r=1.0),
)
# Upper bridge cabin (WHITE, overhanging slightly)
rectangle(
    (24.0, 69.5),
    width=19.0,
    height=9.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_outer, shape_r=1.5),
)
# Bridge windows
rectangle(
    (25.0, 69.5),
    width=13.0,
    height=4.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_inner, shape_r=0.8),
)
# Lower accommodation tower
rectangle(
    (24.0, 55.5),
    width=16.0,
    height=19.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_outer),
)

# 2. Stacked shipping containers (2x2 grid, x=35..75, y=46..70)
containers = [
    (45.0, 52.0, Icon.PASTEL_GREEN),
    (65.0, 52.0, Icon.WHITE),
    (45.0, 64.0, Icon.WHITE),
    (65.0, 64.0, Icon.PASTEL_GREEN),
]
for cx, cy, col in containers:
    rectangle(
        (cx, cy),
        width=20.0,
        height=12.0,
        style=Icon.fill_style(col, border_color=Icon.DARK, border_units=w_outer),
    )
    for dx in (-5.0, 0.0, 5.0):
        Icon.draw_round_segment((cx + dx, cy - 3.5), (cx + dx, cy + 3.5), width_units=w_inner, color=Icon.DARK)

# 3. Vessel hull (PASTEL_BLUE, x=11..89, y=19..51)
hull_pts = [
    (11.0, 46.0),
    (73.0, 46.0),
    (77.0, 51.0),
    (89.0, 51.0),
    (80.5, 19.0),
    (17.5, 19.0),
]
polygon(hull_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE))

# Upper hull accent stripe (WHITE)
Icon.draw_round_polyline(
    [(13.5, 38.0), (74.5, 38.0), (78.5, 42.5), (86.0, 42.5)], width_units=w_inner, color=Icon.WHITE
)

# Hull outer contour
Icon.draw_round_polyline(hull_pts, width_units=w_outer, color=Icon.DARK, closed=True)

# Bow anchor porthole
circle((80.5, 46.5), radius=1.8, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_inner))

# 4. Ocean wave band along waterline (y=15..23)
wave_pts: list[tuple[float, float]] = [(12.0, 15.0), (88.0, 15.0)]
steps = 48
for i in range(steps + 1):
    x = 88.0 - 76.0 * (i / steps)
    y = 22.0 + 1.8 * math.sin((i / steps) * 6.0 * math.pi)
    wave_pts.append((x, y))
polygon(wave_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE_LIGHT))
Icon.draw_round_polyline(wave_pts, width_units=w_outer, color=Icon.DARK, closed=True)

save()
