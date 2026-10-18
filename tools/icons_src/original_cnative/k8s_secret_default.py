# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: k8s_secret."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    PASTEL_GREEN,
    WHITE,
    draw_original_k8s_heptagon,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

draw_original_k8s_heptagon()

# White padlock shackle arch centered at (50, 56)
cx, cy = 50.0, 56.0
r_outer = 12.5
r_inner = 7.0
y_base = 48.0
steps = 24

shackle_pts: list[tuple[float, float]] = [(cx - r_outer, y_base)]
for i in range(steps + 1):
    ang = math.radians(180.0 - 180.0 * (i / steps))
    shackle_pts.append((cx + r_outer * math.cos(ang), cy + r_outer * math.sin(ang)))
shackle_pts.append((cx + r_outer, y_base))
shackle_pts.append((cx + r_inner, y_base))
for i in range(steps + 1):
    ang = math.radians(0.0 + 180.0 * (i / steps))
    shackle_pts.append((cx + r_inner * math.cos(ang), cy + r_inner * math.sin(ang)))
shackle_pts.append((cx - r_inner, y_base))

polygon(
    shackle_pts,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0),
)

# Rounded pastel green padlock body
rectangle(
    (50.0, 39.0),
    width=34.0,
    height=24.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0, shape_r=4.5),
)

# White keyhole circle and dark vertical slot
circle(
    (50.0, 41.5),
    radius=4.2,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0),
)
draw_round_segment((50.0, 37.3), (50.0, 33.0), width_units=2.0, color=DARK)

save()
