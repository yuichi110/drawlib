# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Client concept icon: vr_headset."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Top overhead strap and left/right side strap lugs
rectangle(
    (50.0, 73.5),
    width=15.0,
    height=18.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w, shape_r=4.5),
)
for sx in (16.5, 83.5):
    rectangle(
        (sx, 48.0),
        width=9.0,
        height=17.0,
        style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w, shape_r=3.5),
    )

# Front VR visor contour with rounded outer corners and curved nose bridge notch
x_l, x_r = 18.0, 82.0
y_b, y_t = 28.0, 68.0
rc = 9.0
steps = 12
visor_pts: list[tuple[float, float]] = []

# Top-left corner (90 -> 180 deg)
for i in range(steps + 1):
    ang = math.radians(90.0 + 90.0 * (i / steps))
    visor_pts.append((x_l + rc + rc * math.cos(ang), y_t - rc + rc * math.sin(ang)))

# Bottom-left corner (180 -> 270 deg)
for i in range(steps + 1):
    ang = math.radians(180.0 + 90.0 * (i / steps))
    visor_pts.append((x_l + rc + rc * math.cos(ang), y_b + rc + rc * math.sin(ang)))

# Nose bridge arch at bottom center
visor_pts.append((39.5, y_b))
for i in range(steps + 1):
    ang = math.radians(180.0 - 180.0 * (i / steps))
    visor_pts.append((50.0 + 10.5 * math.cos(ang), y_b + 8.5 * math.sin(ang)))
visor_pts.append((60.5, y_b))

# Bottom-right corner (270 -> 360 deg)
for i in range(steps + 1):
    ang = math.radians(270.0 + 90.0 * (i / steps))
    visor_pts.append((x_r - rc + rc * math.cos(ang), y_b + rc + rc * math.sin(ang)))

# Top-right corner (0 -> 90 deg)
for i in range(steps + 1):
    ang = math.radians(0.0 + 90.0 * (i / steps))
    visor_pts.append((x_r - rc + rc * math.cos(ang), y_t - rc + rc * math.sin(ang)))

polygon(visor_pts, style=Icon.fill_style(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(visor_pts, width_units=w, color=Icon.DARK, closed=True)

# Dual VR optics lenses (WHITE outer rim + PASTEL_GREEN lens highlight)
for lx in (35.5, 64.5):
    circle(
        (lx, 49.5),
        radius=11.0,
        style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0),
    )
    circle(
        (lx, 49.5),
        radius=6.0,
        style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.8),
    )

save()
