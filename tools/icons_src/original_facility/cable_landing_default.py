# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility concept icon: cable_landing."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w_outer = 2.0
w_inner = 1.6

# 1. Ocean water section on the right with smooth scalloped surface waves at y=46.0
ocean_pts: list[tuple[float, float]] = [
    (44.0, 14.0),
    (83.0, 14.0),
]
# Rounded bottom-right corner at (83, 18), r=4.0 -> reaches (87, 18)
for i in range(9):
    ang = math.radians(270.0 + 90.0 * (i / 8))
    ocean_pts.append((83.0 + 4.0 * math.cos(ang), 18.0 + 4.0 * math.sin(ang)))
# 3 scalloped wave crests from x=87.0 back to x=45.0 at y_base=46.0
for wave_cx in (80.0, 66.0, 52.0):
    for i in range(13):
        ang = math.radians(0.0 + 180.0 * (i / 12))
        ocean_pts.append((wave_cx + 7.0 * math.cos(ang), 46.0 + 3.2 * math.sin(ang)))
polygon(ocean_pts, style=no_border_fill(PASTEL_BLUE_LIGHT))
draw_round_polyline(ocean_pts, width_units=w_outer, color=DARK, closed=True)

# Secondary inner wave ripple line inside ocean
wave2_pts: list[tuple[float, float]] = []
for wave_cx in (58.0, 72.0):
    for i in range(13):
        ang = math.radians(180.0 - 180.0 * (i / 12))
        wave2_pts.append((wave_cx + 7.0 * math.cos(ang), 34.5 + 2.2 * math.sin(ang)))
draw_round_polyline(wave2_pts, width_units=w_inner, color=DARK)

# 2. Coastal cliff / seabed foundation block on the left (PASTEL_BLUE)
cliff_round: list[tuple[float, float]] = [
    (48.0, 14.0),
    (45.0, 46.0),
    (13.0, 46.0),
]
for i in range(9):
    ang = math.radians(180.0 + 90.0 * (i / 8))
    cliff_round.append((17.0 + 4.0 * math.cos(ang), 18.0 + 4.0 * math.sin(ang)))
polygon(cliff_round, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(cliff_round, width_units=w_outer, color=DARK, closed=True)

# 3. Coastal station building on top of cliff (WHITE walls + PASTEL_BLUE roof)
rectangle(
    (29.0, 61.5),
    width=28.0,
    height=31.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w_outer),
)
rectangle(
    (29.0, 80.0),
    width=32.0,
    height=7.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w_outer, shape_r=2.5),
)
for win_x in (23.5, 34.5):
    rectangle(
        (win_x, 64.5),
        width=7.0,
        height=11.0,
        style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_inner, shape_r=1.5),
    )

# 4. Undersea PASTEL_GREEN fiber optic cable running from station base down beneath waves
cable_pts: list[tuple[float, float]] = [
    (29.0, 46.0),
    (29.0, 28.0),
]
for i in range(1, 10):
    ang = math.radians(180.0 + 90.0 * (i / 9))
    cable_pts.append((36.0 + 7.0 * math.cos(ang), 28.0 + 7.0 * math.sin(ang)))
cable_pts.append((79.5, 21.0))

draw_round_polyline(cable_pts, width_units=6.2, color=DARK)
draw_round_polyline(cable_pts, width_units=3.2, color=PASTEL_GREEN)

# Optical termination nodes at both ends of the fiber cable
circle((29.0, 48.0), radius=3.5, style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w_inner))
circle((79.5, 21.0), radius=3.8, style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w_inner))

save()
