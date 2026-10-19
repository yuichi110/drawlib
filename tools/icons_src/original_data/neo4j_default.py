# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: neo4j."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

Icon.setup()

w = 2.0

# 1. Top-right rounded 'n' arch (Colors.Blue4)
cx_arch, cy_arch = 63.8, 61.5
r_out = 26.8
r_in = 16.0
y_right_bot = 32.5

# Concave bottom-left cutout arc centered on hub node (41.8, 37.0) with radius 13.8
cx_hub, cy_hub = 41.8, 37.0
r_cut = 13.8

arch_pts: list[tuple[float, float]] = []

# Left outer leg from cutout top-left up to arch start (61.5)
x_left_out = cx_arch - r_out  # 37.0
y_left_out_bot = cy_hub + math.sqrt(max(0.0, r_cut**2 - (x_left_out - cx_hub) ** 2))

# Outer semicircle from 180 deg CW to 0 deg around (cx_arch, cy_arch)
arch_pts.append((x_left_out, y_left_out_bot))
steps_arch = 28
for i in range(steps_arch + 1):
    ang = math.radians(180.0 - 180.0 * (i / steps_arch))
    arch_pts.append((cx_arch + r_out * math.cos(ang), cy_arch + r_out * math.sin(ang)))

# Right outer leg down to y_right_bot, then across to right inner leg
x_right_out = cx_arch + r_out  # 90.6
x_right_in = cx_arch + r_in  # 79.8
arch_pts.append((x_right_out, y_right_bot))
arch_pts.append((x_right_in, y_right_bot))

# Inner semicircle from 0 deg CCW to 180 deg around (cx_arch, cy_arch)
for i in range(steps_arch + 1):
    ang = math.radians(180.0 * (i / steps_arch))
    arch_pts.append((cx_arch + r_in * math.cos(ang), cy_arch + r_in * math.sin(ang)))

# Left inner leg down to cutout arc, then concave arc back to (x_left_out, y_left_out_bot)
x_left_in = cx_arch - r_in  # 47.8
y_left_in_bot = cy_hub + math.sqrt(max(0.0, r_cut**2 - (x_left_in - cx_hub) ** 2))
a_in = math.degrees(math.atan2(y_left_in_bot - cy_hub, x_left_in - cx_hub))
a_out = math.degrees(math.atan2(y_left_out_bot - cy_hub, x_left_out - cx_hub))

steps_cut = 10
for i in range(steps_cut + 1):
    ang = math.radians(a_in + (a_out - a_in) * (i / steps_cut))
    arch_pts.append((cx_hub + r_cut * math.cos(ang), cy_hub + r_cut * math.sin(ang)))

polygon(arch_pts, style=Icon.no_border_fill(Colors.Blue4))
Icon.draw_round_polyline(arch_pts, width_units=w, color=Icon.DARK, closed=True)

# 2. Graph link bars connecting the 3 bottom-left nodes (WHITE)
n_top = (18.2, 53.2)
n_bot = (18.2, 20.8)
n_mid = (cx_hub, cy_hub)
half_link_w = 2.8

for p1, p2 in ((n_top, n_mid), (n_bot, n_mid)):
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    dist = math.hypot(dx, dy)
    nx = -dy / dist * half_link_w
    ny = dx / dist * half_link_w
    bar_pts = [
        (p1[0] + nx, p1[1] + ny),
        (p2[0] + nx, p2[1] + ny),
        (p2[0] - nx, p2[1] - ny),
        (p1[0] - nx, p1[1] - ny),
    ]
    polygon(bar_pts, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.7))

# 3. Three graph node circles (Colors.Blue2 & Colors.Teal3 satellites + Colors.Blue3 hub)
circle(n_top, radius=8.6, style=Icon.fill_style(Colors.Blue2, border_color=Icon.DARK, border_units=1.8))
circle(n_bot, radius=8.6, style=Icon.fill_style(Colors.Teal3, border_color=Icon.DARK, border_units=1.8))
circle(n_mid, radius=8.8, style=Icon.fill_style(Colors.Blue3, border_color=Icon.DARK, border_units=1.8))

save()
