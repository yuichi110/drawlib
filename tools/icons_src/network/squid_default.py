# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Network icon: squid (default variant)."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

Icon.setup()

SQUID_ORANGE = "#FF9900"
SQUID_BLUE = "#6699CC"
SQUID_BLACK = "#000000"

CX, CY = 50.0, 50.0
RADIUS = 38.5
BORDER_W = 5.0

# 1. Base steel-blue circle fill
circle((CX, CY), radius=RADIUS, style=Icon.fill_style(SQUID_BLUE))

# 2. Vertical S-curve centerline inside border (97 deg -> 258 deg)
s_curve: list[tuple[float, float]] = [
    (45.50, 87.20),
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
    (42.20, 13.30),
]

# 3. Left orange crescent bounded by circular arc (97 deg -> 258 deg) and S-curve
left_arc: list[tuple[float, float]] = []
steps = 36
ang_start = math.radians(97.0)
ang_end = math.radians(258.0)
for i in range(steps + 1):
    ang = ang_start + (ang_end - ang_start) * (i / steps)
    left_arc.append((CX + RADIUS * math.cos(ang), CY + RADIUS * math.sin(ang)))

crescent_pts = [*left_arc, *reversed(s_curve)]
polygon(crescent_pts, style=Icon.fill_style(SQUID_ORANGE))

# 4. Smooth black vertical S-curve divider
Icon.draw_round_polyline(s_curve, width_units=5.6, color=SQUID_BLACK, corner_r=2.0)

# 5. Characteristic black spiral curl inside the right steel-blue half
spiral_pts: list[tuple[float, float]] = [
    (86.00, 63.20),
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
    (76.50, 46.80),
]
Icon.draw_round_polyline(spiral_pts, width_units=4.8, color=SQUID_BLACK, corner_r=1.5)

# Crisp flat top cap on the inner tip of the spiral curl
polygon(
    [(74.10, 46.40), (78.90, 46.40), (78.90, 49.40), (74.10, 49.40)],
    style=Icon.fill_style(SQUID_BLACK),
)

# 6. Solid black outer circular border
circle(
    (CX, CY),
    radius=RADIUS,
    style=Icon.fill_style(Colors.Transparent, border_color=SQUID_BLACK, border_units=BORDER_W),
)

save()
