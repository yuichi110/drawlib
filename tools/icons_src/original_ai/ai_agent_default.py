# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: ai_agent."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.styles import Colors, Style
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE
cx, cy = 50.0, 48.0
orbit_r = 33.0

circle(
    (cx, cy),
    radius=orbit_r,
    style=Style(
        shape_fill_color=Colors.Transparent,
        shape_line_color=Icon.DARK,
        shape_line_width=Icon.pt(w),
    ),
)

sparkle_pts = Icon.build_sparkle_4pt_polygon(cx, cy, outer_r=17.5, inner_r=6.0)
polygon(sparkle_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(sparkle_pts, width_units=w, color=Icon.DARK, closed=True)
circle(
    (cx, cy),
    radius=3.6,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0),
)

for angle_deg in (90.0, 210.0, 330.0):
    rad = math.radians(angle_deg)
    sx = cx + orbit_r * math.cos(rad)
    sy = cy + orbit_r * math.sin(rad)
    circle(
        (sx, sy),
        radius=8.5,
        style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w),
    )

save()
