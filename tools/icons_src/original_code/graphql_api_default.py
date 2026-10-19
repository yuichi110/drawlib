# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code concept icon: graphql_api."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.utils import Icon

Icon.setup()

w_shape = 2.0
w_hex = 2.0
w_chord = 2.0

cx, cy = 50.0, 50.0
radius = 30.0

# 1. Six vertices of regular pointy-top hexagon (angles 90, 30, -30, -90, -150, 150)
angles_deg = [90.0, 30.0, -30.0, -90.0, -150.0, 150.0]
verts = [
    (
        cx + radius * math.cos(math.radians(a)),
        cy + radius * math.sin(math.radians(a)),
    )
    for a in angles_deg
]

# 2. Inner triangle chords (V0-V2-V4) and radial spokes to central hub (w_line=2.0 in DARK)
Icon.draw_round_polyline([verts[0], verts[2], verts[4]], width_units=w_chord, color=Icon.DARK, closed=True)
for idx in (1, 3, 5):
    Icon.draw_round_segment((cx, cy), verts[idx], width_units=w_chord, color=Icon.DARK)

# 3. Outer regular hexagon outline (w_line=2.7 in DARK)
Icon.draw_round_polyline(verts, width_units=w_hex, color=Icon.DARK, closed=True)

# 4. Central WHITE hub circle (r=7.0, border 1.8 in DARK)
circle(
    (cx, cy),
    radius=7.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_shape),
)

# 5. Six circular vertex nodes (r=6.0, border 1.8 in DARK, alternating PASTEL_BLUE and PASTEL_GREEN)
for i, v_xy in enumerate(verts):
    node_col = Icon.PASTEL_BLUE if i % 2 == 0 else Icon.PASTEL_GREEN
    circle(
        v_xy,
        radius=6.0,
        style=Icon.fill_style(node_col, border_color=Icon.DARK, border_units=w_shape),
    )

save()
