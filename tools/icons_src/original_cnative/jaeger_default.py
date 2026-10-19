# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: jaeger."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, ellipse, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w = 2.0

# 1. Cute rounded ears peeking near the hat brim
for ex in (26.5, 73.5):
    circle(
        (ex, 63.0),
        radius=7.0,
        style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w),
    )
    circle(
        (ex, 63.0),
        radius=3.2,
        style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=1.8),
    )

# 2. Explorer hat feather on top-right
feather_pts = [
    (63.0, 69.0),
    (68.0, 81.5),
    (75.5, 86.0),
    (73.5, 76.0),
    (68.0, 68.0),
]
polygon(feather_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE_LIGHT))
Icon.draw_round_polyline(feather_pts, width_units=2.0, color=Icon.DARK, closed=True)

# 3. Explorer hat crown (PASTEL_GREEN) + WHITE hat band
crown_pts: list[tuple[float, float]] = [(29.0, 65.0)]
steps = 20
for i in range(steps + 1):
    t = i / steps
    ang = math.pi * (1.0 - t)
    cx_hat = 50.0 + 21.0 * math.cos(ang)
    cy_hat = 65.0 + 19.5 * math.sin(ang)
    crown_pts.append((cx_hat, cy_hat))
crown_pts.append((71.0, 65.0))
polygon(crown_pts, style=Icon.no_border_fill(Icon.PASTEL_GREEN))

# White hat band conforming to the exact dome slope at y=67.2..72.4
band_pts = [
    (29.13, 67.2),
    (70.87, 67.2),
    (69.43, 72.4),
    (30.57, 72.4),
]
polygon(band_pts, style=Icon.no_border_fill(Icon.WHITE))
Icon.draw_round_segment((30.57, 72.4), (69.43, 72.4), width_units=2.0, color=Icon.DARK)
Icon.draw_round_segment((29.13, 67.2), (70.87, 67.2), width_units=2.0, color=Icon.DARK)
Icon.draw_round_polyline(crown_pts, width_units=w, color=Icon.DARK, closed=True)

# 4. Gopher rounded body (PASTEL_BLUE)
rectangle(
    (50.0, 39.5),
    width=50.0,
    height=47.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=13.0),
)

# 5. Explorer hat wide brim (PASTEL_GREEN) sitting over top of head
ellipse(
    (50.0, 64.0),
    width=64.0,
    height=7.5,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w),
)

# 6. Two big WHITE circular eyes + DARK pupils
for ex, px in ((38.5, 40.0), (61.5, 59.5)):
    circle(
        (ex, 46.5),
        radius=9.5,
        style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0),
    )
    circle(
        (px, 45.5),
        radius=3.8,
        style=Icon.fill_style(Icon.DARK),
    )
    circle(
        (px - 1.2, 47.0),
        radius=1.2,
        style=Icon.fill_style(Icon.WHITE),
    )

# 7. Two small WHITE buck teeth below the snout
for tx in (47.0, 53.0):
    rectangle(
        (tx, 23.5),
        width=5.6,
        height=8.0,
        style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0, shape_r=2.0),
    )

# 8. WHITE oval snout + DARK nose oval
ellipse(
    (50.0, 31.0),
    width=23.0,
    height=10.5,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0),
)
ellipse(
    (50.0, 34.0),
    width=9.5,
    height=5.5,
    style=Icon.fill_style(Icon.DARK),
)

save()
