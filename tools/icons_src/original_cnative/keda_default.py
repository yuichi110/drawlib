# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: keda."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import Icon

Icon.setup()

cx, cy = 50.0, 49.0
r_ring = 33.5
half_bar_w = 3.0

# 1. Compute 7 regular heptagon vertices (top vertex at 90 degrees)
vertices: list[tuple[float, float]] = []
for i in range(7):
    ang = math.radians(90.0 + i * (360.0 / 7.0))
    vertices.append((cx + r_ring * math.cos(ang), cy + r_ring * math.sin(ang)))

# 2. 7 straight PASTEL_BLUE_LIGHT ring segments
for i in range(7):
    x1, y1 = vertices[i]
    x2, y2 = vertices[(i + 1) % 7]
    dx, dy = x2 - x1, y2 - y1
    dist = math.hypot(dx, dy)
    nx = -dy / dist * half_bar_w
    ny = dx / dist * half_bar_w
    bar_pts = [
        (x1 + nx, y1 + ny),
        (x2 + nx, y2 + ny),
        (x2 - nx, y2 - ny),
        (x1 - nx, y1 - ny),
    ]
    polygon(
        bar_pts,
        style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=2.0),
    )

# 3. 7 PASTEL_BLUE vertex circles
for vx, vy in vertices:
    circle(
        (vx, vy),
        radius=6.8,
        style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=2.0),
    )

# 4. Bold central PASTEL_GREEN lightning bolt
bolt_pts = [
    (54.5, 70.0),
    (38.0, 47.0),
    (48.5, 47.0),
    (45.0, 27.5),
    (62.0, 50.5),
    (51.5, 50.5),
]
polygon(bolt_pts, style=Icon.no_border_fill(Icon.PASTEL_GREEN))
Icon.draw_round_polyline(bolt_pts, width_units=2.0, color=Icon.DARK, closed=True)

save()
