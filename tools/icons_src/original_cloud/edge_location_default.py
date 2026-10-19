# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: edge_location."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, ellipse, polygon
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Perspective edge ground ring
ellipse(
    (50.0, 22.0),
    width=64.0,
    height=18.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w),
)

# Teardrop map pin geometry
cx, cy = 50.0, 62.0
r = 22.0
y_tip = 24.0
d = cy - y_tip
alpha_deg = math.degrees(math.asin(r / d))

ang_start = -alpha_deg
ang_end = 180.0 + alpha_deg
steps = 48

pin_pts: list[tuple[float, float]] = [(cx, y_tip)]
for i in range(steps + 1):
    ang = math.radians(ang_start + (ang_end - ang_start) * (i / steps))
    pin_pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))

hole_r = 9.5
hole_pts = [
    (
        cx + hole_r * math.cos(math.radians(360.0 * i / steps)),
        cy + hole_r * math.sin(math.radians(360.0 * i / steps)),
    )
    for i in range(steps)
]

polygon(pin_pts, holes=[hole_pts], style=Icon.fill_style(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(pin_pts, width_units=w, color=Icon.DARK, closed=True)

# Inner pin cutout circle border
circle(
    (cx, cy),
    radius=hole_r,
    style=Icon.stroke_style(Icon.DARK, width_units=2.0),
)

save()
