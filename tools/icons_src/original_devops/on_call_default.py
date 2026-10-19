# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: on_call."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Left and right ringing sound-wave arcs with smooth round caps
left_wave = [
    (
        29.0 + 11.5 * math.cos(math.radians(deg)),
        52.0 + 15.0 * math.sin(math.radians(deg)),
    )
    for deg in range(132, 229, 4)
]
Icon.draw_round_polyline(left_wave, width_units=w, color=Icon.DARK)

right_wave = [
    (
        71.0 + 11.5 * math.cos(math.radians(deg)),
        52.0 + 15.0 * math.sin(math.radians(deg)),
    )
    for deg in range(-48, 25, 4)
]
Icon.draw_round_polyline(right_wave, width_units=w, color=Icon.DARK)

# Bottom clapper and top ring
circle(
    (50.0, 24.5),
    radius=6.5,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w),
)
circle(
    (50.0, 74.5),
    radius=4.5,
    style=Icon.stroke_style(Icon.DARK, width_units=w),
)

# Bell dome (cx=50, cy=53, r=18) + flared skirt down to y=32 (width=48 at base)
dome_cx, dome_cy, dome_r = 50.0, 53.0, 18.0
bell_pts: list[tuple[float, float]] = []

steps_dome = 32
for i in range(steps_dome + 1):
    ang = math.radians(180.0 - 180.0 * (i / steps_dome))
    bell_pts.append((dome_cx + dome_r * math.cos(ang), dome_cy + dome_r * math.sin(ang)))

p0_r, p1_r, p2_r, p3_r = (68.0, 53.0), (68.0, 41.0), (73.5, 36.0), (74.0, 32.0)
steps_skirt = 16
for i in range(1, steps_skirt + 1):
    t = i / steps_skirt
    mt = 1.0 - t
    bx = (mt**3) * p0_r[0] + 3 * (mt**2) * t * p1_r[0] + 3 * mt * (t**2) * p2_r[0] + (t**3) * p3_r[0]
    by = (mt**3) * p0_r[1] + 3 * (mt**2) * t * p1_r[1] + 3 * mt * (t**2) * p2_r[1] + (t**3) * p3_r[1]
    bell_pts.append((bx, by))

p0_l, p1_l, p2_l, p3_l = (26.0, 32.0), (26.5, 36.0), (32.0, 41.0), (32.0, 53.0)
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

# Bottom rim bar
rectangle(
    (50.0, 32.0),
    width=54.0,
    height=7.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=3.5),
)

# Bright alert badge on top-right of bell
circle(
    (67.5, 68.5),
    radius=9.5,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w),
)
circle(
    (67.5, 68.5),
    radius=3.2,
    style=Icon.fill_style(Icon.WHITE),
)

save()
