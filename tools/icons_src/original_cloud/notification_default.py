# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: notification."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Bottom clapper and top loop
circle(
    (50.0, 20.5),
    radius=8.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w),
)
circle(
    (50.0, 81.5),
    radius=5.5,
    style=Icon.stroke_style(Icon.DARK, width_units=w),
)

# Smooth bell body polygon: upper dome (cx=50, cy=56, r=22) + lower flared skirt to y=29
dome_cx, dome_cy, dome_r = 50.0, 56.0, 22.0
bell_pts: list[tuple[float, float]] = []

steps_dome = 32
for i in range(steps_dome + 1):
    ang = math.radians(180.0 - 180.0 * (i / steps_dome))
    bell_pts.append((dome_cx + dome_r * math.cos(ang), dome_cy + dome_r * math.sin(ang)))

# Right skirt cubic Bezier from (72, 56) to (80, 29)
p0_r, p1_r, p2_r, p3_r = (72.0, 56.0), (72.0, 41.0), (79.0, 35.0), (80.0, 29.0)
steps_skirt = 16
for i in range(1, steps_skirt + 1):
    t = i / steps_skirt
    mt = 1.0 - t
    bx = (mt**3) * p0_r[0] + 3 * (mt**2) * t * p1_r[0] + 3 * mt * (t**2) * p2_r[0] + (t**3) * p3_r[0]
    by = (mt**3) * p0_r[1] + 3 * (mt**2) * t * p1_r[1] + 3 * mt * (t**2) * p2_r[1] + (t**3) * p3_r[1]
    bell_pts.append((bx, by))

# Left skirt cubic Bezier from (20, 29) back to (28, 56)
p0_l, p1_l, p2_l, p3_l = (20.0, 29.0), (21.0, 35.0), (28.0, 41.0), (28.0, 56.0)
for i in range(steps_skirt):
    t = i / steps_skirt
    mt = 1.0 - t
    bx = (mt**3) * p0_l[0] + 3 * (mt**2) * t * p1_l[0] + 3 * mt * (t**2) * p2_l[0] + (t**3) * p3_l[0]
    by = (mt**3) * p0_l[1] + 3 * (mt**2) * t * p1_l[1] + 3 * mt * (t**2) * p2_l[1] + (t**3) * p3_l[1]
    bell_pts.append((bx, by))

polygon(
    bell_pts,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w),
)

# Crisp white bottom rim bar
rectangle(
    (50.0, 29.0),
    width=66.0,
    height=8.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=4.0),
)

save()
