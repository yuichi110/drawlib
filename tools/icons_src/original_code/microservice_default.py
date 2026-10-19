# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code concept icon: microservice."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import Icon

Icon.setup()

w_shape = 2.0
w_line = 2.0

cx, cy = 50.0, 50.0
r_hex = 24.0
r_port_orbit = 34.0

# 1. Three radial DARK stems (w_line=2.7) at 90, 210, 330 degrees
port_angles = [90.0, 210.0, 330.0]
port_centers = [
    (
        cx + r_port_orbit * math.cos(math.radians(a)),
        cy + r_port_orbit * math.sin(math.radians(a)),
    )
    for a in port_angles
]
for px, py in port_centers:
    Icon.draw_round_segment((cx, cy), (px, py), width_units=w_line, color=Icon.DARK)

# 2. Central flat-top PASTEL_BLUE hexagon (cx=50, cy=50, r=24, border 1.8 in DARK)
hex_verts = [
    (
        cx + r_hex * math.cos(math.radians(k * 60.0)),
        cy + r_hex * math.sin(math.radians(k * 60.0)),
    )
    for k in range(6)
]
polygon(hex_verts, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(hex_verts, width_units=w_shape, color=Icon.DARK, closed=True)

# 3. Inner WHITE core circle (r=9.0, border 1.8 in DARK)
circle(
    (cx, cy),
    radius=9.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_shape),
)

# 4. Three outer PASTEL_GREEN circular port nodes (r=5.5, border 1.8 in DARK)
for px, py in port_centers:
    circle(
        (px, py),
        radius=5.5,
        style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_shape),
    )

save()
