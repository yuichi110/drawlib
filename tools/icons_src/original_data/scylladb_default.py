# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: scylladb."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, ellipse, polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

Icon.setup()

w = 2.0

# 1. Sea monster domed head + 5 scalloped tentacle lobes at bottom (Colors.Teal3)
body_pts: list[tuple[float, float]] = []

steps_wall = 12
for i in range(steps_wall + 1):
    t = i / steps_wall
    x = 20.0 - 4.0 * math.sin(t * math.pi * 0.5)
    y = 20.0 + 36.0 * t
    body_pts.append((x, y))

steps_dome = 32
for i in range(1, steps_dome + 1):
    ang = math.radians(180.0 - 180.0 * (i / steps_dome))
    body_pts.append((50.0 + 34.0 * math.cos(ang), 56.0 + 30.0 * math.sin(ang)))

for i in range(1, steps_wall + 1):
    t = i / steps_wall
    x = 84.0 - 4.0 * (1.0 - math.cos(t * math.pi * 0.5))
    y = 56.0 - 36.0 * t
    body_pts.append((x, y))

for lobe_idx in range(5):
    lobe_cx = 74.0 - lobe_idx * 12.0
    for j in range(1, 13):
        ang = math.radians(0.0 - 180.0 * (j / 12))
        body_pts.append((lobe_cx + 6.0 * math.cos(ang), 20.0 + 6.5 * math.sin(ang)))

polygon(body_pts, style=Icon.no_border_fill(Colors.Teal3))

# 2. Cute pastel forehead spots (Colors.Teal2 & Colors.Blue3)
ellipse(
    (50.0, 78.0), width=14.0, height=6.5, style=Icon.fill_style(Colors.Teal2, border_color=Icon.DARK, border_units=1.5)
)
for sx in (34.0, 66.0):
    circle((sx, 73.5), radius=3.5, style=Icon.fill_style(Colors.Blue3, border_color=Icon.DARK, border_units=1.5))

# 3. Outer border + vertical tentacle division creases
Icon.draw_round_polyline(body_pts, width_units=w, color=Icon.DARK, closed=True)
for tx in (32.0, 44.0, 56.0, 68.0):
    Icon.draw_round_segment((tx, 20.0), (tx, 31.5), width_units=1.7, color=Icon.DARK)

# 4. Two big adorable rounded eyes (WHITE + DARK pupils)
for ex, px in ((37.5, 39.0), (62.5, 61.0)):
    circle(
        (ex, 55.5),
        radius=9.8,
        style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.8),
    )
    circle((px, 55.5), radius=4.2, style=Icon.fill_style(Icon.DARK))
    circle((px - 1.3, 57.0), radius=1.3, style=Icon.fill_style(Icon.WHITE))

# 5. Friendly curved smile + two cute little white teeth tucked cleanly beneath the smile curve
smile_cy = 44.5
smile_rx = 13.5
smile_ry = 6.0


def _smile_y(x_val: float) -> float:
    """Evaluate exact smile curve y at x_val."""
    cos_a = max(-1.0, min(1.0, (x_val - 50.0) / smile_rx))
    sin_a = -math.sqrt(max(0.0, 1.0 - cos_a * cos_a))
    return smile_cy + smile_ry * sin_a


smile_pts: list[tuple[float, float]] = []
for i in range(17):
    t = i / 16
    ang = math.radians(200.0 + 140.0 * t)
    smile_pts.append((50.0 + smile_rx * math.cos(ang), smile_cy + smile_ry * math.sin(ang)))

for tooth_x in (44.0, 56.0):
    xl, xr = tooth_x - 2.5, tooth_x + 2.5
    yl, yr = _smile_y(xl), _smile_y(xr)
    tooth_pts = [
        (xl, yl),
        (tooth_x - 2.1, 34.0),
        (tooth_x + 2.1, 34.0),
        (xr, yr),
    ]
    polygon(tooth_pts, style=Icon.no_border_fill(Icon.WHITE))
    Icon.draw_round_polyline(tooth_pts, width_units=1.5, color=Icon.DARK, closed=True)

Icon.draw_round_polyline(smile_pts, width_units=1.8, color=Icon.DARK)

save()
