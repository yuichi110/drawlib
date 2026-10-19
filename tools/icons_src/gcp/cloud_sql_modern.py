# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: cloud_sql."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import Gcp, Icon

Icon.setup()

cx = 50.0
dx = 38.0
dy = 15.0
x_left = cx - dx
x_right = cx + dx

r = 4.25
length = math.hypot(dx, dy)
nx = r * dy / length
ny = r * dx / length
rx = r * length / dy
ry = r * length / dx

y_mid = 74.0
y_top = y_mid + dy
y_bot = y_mid - dy

circle((x_left, y_mid), radius=r, style=Icon.fill_style(Gcp.YELLOW))
yellow_verts = [
    (x_left - nx, y_mid + ny),
    (cx - rx, y_top),
    (cx, y_top - ry),
    (x_left + rx, y_mid),
    (cx, y_bot + ry),
    (cx + rx, y_bot),
    (cx, y_bot - ry),
    (x_left - nx, y_mid - ny),
]
polygon(yellow_verts, style=Icon.fill_style(Gcp.YELLOW, shape_r=(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.8, 0.0)))

circle((x_right, y_mid), radius=r, style=Icon.fill_style(Gcp.RED))
red_verts = [
    (x_right + nx, y_mid - ny),
    (cx + rx, y_bot),
    (cx, y_bot + ry),
    (x_right - rx, y_mid),
    (cx, y_top - ry),
    (cx - rx, y_top),
    (cx, y_top + ry),
    (x_right + nx, y_mid + ny),
]
polygon(red_verts, style=Icon.fill_style(Gcp.RED, shape_r=(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.8, 0.0)))

for y_apex in (43.0, 27.0, 11.0):
    y_side = y_apex + dy

    circle((x_left, y_side), radius=r, style=Icon.fill_style(Gcp.GREEN))
    green_verts = [
        (x_left + nx, y_side + ny),
        (cx, y_apex + ry),
        (cx - rx, y_apex),
        (x_left - nx, y_side - ny),
    ]
    polygon(green_verts, style=Icon.fill_style(Gcp.GREEN))

    circle((x_right, y_side), radius=r, style=Icon.fill_style(Gcp.BLUE))
    blue_verts = [
        (x_right - nx, y_side + ny),
        (cx - rx, y_apex),
        (cx, y_apex - ry),
        (x_right + nx, y_side - ny),
    ]
    polygon(blue_verts, style=Icon.fill_style(Gcp.BLUE, shape_r=(0.0, 0.0, 1.8, 0.0)))

save()
