# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: user."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE
cx = 50.0
rx = 32.0
y_bot = 16.0
y_arch_base = 24.0
ry = 24.0
corner_r = 5.0

pts: list[tuple[float, float]] = []
steps_corner = 12
steps_arch = 40

# Bottom-left rounded corner (180 -> 270 deg)
c_bl = (cx - rx + corner_r, y_bot + corner_r)
for i in range(steps_corner + 1):
    ang = math.radians(180.0 + 90.0 * (i / steps_corner))
    pts.append((c_bl[0] + corner_r * math.cos(ang), c_bl[1] + corner_r * math.sin(ang)))

# Bottom-right rounded corner (270 -> 360 deg)
c_br = (cx + rx - corner_r, y_bot + corner_r)
for i in range(steps_corner + 1):
    ang = math.radians(270.0 + 90.0 * (i / steps_corner))
    pts.append((c_br[0] + corner_r * math.cos(ang), c_br[1] + corner_r * math.sin(ang)))

# Upper shoulder arch (0 -> 180 deg)
for i in range(steps_arch + 1):
    ang = math.radians(180.0 * (i / steps_arch))
    pts.append((cx + rx * math.cos(ang), y_arch_base + ry * math.sin(ang)))

polygon(
    pts,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w),
)

circle(
    (50.0, 68.0),
    radius=15.5,
    style=fill_style(WHITE, border_color=DARK, border_units=w),
)

circle(
    (67.0, 26.0),
    radius=5.2,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.2),
)

save()
