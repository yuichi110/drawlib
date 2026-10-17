# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Network concept icon: squid."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.styles import Colors
from drawlib.utils import DARK, draw_round_polyline, no_border_fill, setup_icon, stroke_style

setup_icon()

CX, CY = 50.0, 50.0
RADIUS = 38.5
W = 2.2

# 1. Base pastel blue circle fill
circle((CX, CY), radius=RADIUS, style=no_border_fill(Colors.Blue2))

# 2. Vertical S-curve centerline inside border (97 deg -> 258 deg)
s_curve: list[tuple[float, float]] = [
    (45.31, 88.21),
    (43.20, 83.20),
    (41.40, 78.50),
    (40.30, 73.50),
    (40.00, 68.50),
    (40.30, 63.50),
    (41.10, 58.50),
    (42.10, 53.50),
    (43.30, 48.50),
    (44.50, 43.50),
    (45.50, 38.50),
    (46.20, 33.50),
    (46.30, 28.50),
    (45.70, 23.50),
    (44.20, 18.50),
    (42.00, 12.34),
]

# 3. Left pastel orange crescent bounded by circular arc (97 deg -> 258 deg) and S-curve
left_arc: list[tuple[float, float]] = []
steps = 36
ang_start = math.radians(97.0)
ang_end = math.radians(258.0)
for i in range(steps + 1):
    ang = ang_start + (ang_end - ang_start) * (i / steps)
    left_arc.append((CX + RADIUS * math.cos(ang), CY + RADIUS * math.sin(ang)))

crescent_pts = [*left_arc, *reversed(s_curve)]
polygon(crescent_pts, style=no_border_fill(Colors.Orange2))

# 4. Smooth DARK vertical S-curve divider
draw_round_polyline(s_curve, width_units=W, color=DARK, corner_r=2.0)

# 5. Characteristic DARK spiral wave curl inside the right pastel-blue half
spiral_pts: list[tuple[float, float]] = [
    (86.07, 63.48),
    (82.60, 65.40),
    (78.80, 66.20),
    (74.80, 65.80),
    (70.80, 64.20),
    (67.20, 61.40),
    (64.80, 57.60),
    (63.60, 53.20),
    (63.80, 48.80),
    (65.40, 45.20),
    (68.20, 42.80),
    (71.80, 42.30),
    (75.00, 43.80),
    (76.50, 46.20),
    (76.50, 47.40),
]
draw_round_polyline(spiral_pts, width_units=W, color=DARK, corner_r=1.5)

# 6. Bold DARK outer circular border
circle((CX, CY), radius=RADIUS, style=stroke_style(DARK, width_units=W))

save()
