# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: key_management."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Outer flat-top hexagonal security plate
cx, cy = 50.0, 50.0
hex_r = 38.0
hex_angles = [0.0, 60.0, 120.0, 180.0, 240.0, 300.0]
hex_pts = [
    (cx + hex_r * math.cos(math.radians(a)), cy + hex_r * math.sin(math.radians(a)))
    for a in hex_angles
]
polygon(hex_pts, style=no_border_fill(WHITE))
draw_round_polyline(hex_pts, width_units=w, color=DARK, closed=True)

# Key shaft and two downward teeth on the right
shaft_pts = [
    (42.0, 55.0),
    (73.0, 55.0),
    (73.0, 40.0),
    (67.0, 40.0),
    (67.0, 48.0),
    (62.5, 48.0),
    (62.5, 42.5),
    (56.5, 42.5),
    (56.5, 48.0),
    (42.0, 48.0),
]
polygon(shaft_pts, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(shaft_pts, width_units=2.5, color=DARK, closed=True)

# Circular key bow on the left with inner keyhole
bow_xy = (34.0, 51.5)
circle(
    bow_xy,
    radius=12.5,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w),
)
circle(
    (32.5, 51.5),
    radius=4.5,
    style=fill_style(WHITE, border_color=DARK, border_units=2.2),
)

save()
