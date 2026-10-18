# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: argo."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    WHITE,
    draw_round_polyline,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Soft pastel Argo palette matching Drawlib Original tone
ARGO_CORAL = "#F8A07E"  # Pastel coral-orange octopus (softened from official #FE733E)
ARGO_SKY = "#D6ECFA"  # Pale ice-blue helmet glass (softened from official #CDECF6)
ARGO_RIM = "#ACC2FA"  # Pastel blue helmet latches & collar (matching #B5D2F3 / PASTEL_BLUE_LIGHT)

# Side helmet latch tabs behind the main helmet ring
for x_tab in (20.0, 80.0):
    rectangle(
        (x_tab, 58.0),
        width=6.5,
        height=15.0,
        style=fill_style(ARGO_RIM, border_color=DARK, border_units=2.0, shape_r=3.0),
    )

# Outer white space helmet ring
circle(
    (50.0, 58.0),
    radius=29.5,
    style=fill_style(WHITE, border_color=DARK, border_units=w),
)

# Inner pale ice-blue glass visor
circle(
    (50.0, 58.0),
    radius=24.5,
    style=fill_style(ARGO_SKY, border_color=DARK, border_units=2.0),
)

# Four rounded tentacles tucked neatly beneath the neck collar
tentacles = [
    (38.2, 20.5, 6.4, 17.0, 11.0),
    (46.0, 19.8, 6.4, 17.5, 3.5),
    (54.0, 19.8, 6.4, 17.5, -3.5),
    (61.8, 20.5, 6.4, 17.0, -11.0),
]
for tx, ty, tw, th, tang in tentacles:
    rectangle(
        (tx, ty),
        width=tw,
        height=th,
        style=fill_style(ARGO_CORAL, border_color=DARK, border_units=2.0, shape_r=3.2, angle=tang),
    )

# Rounded octopus head dome inside the helmet
head_pts: list[tuple[float, float]] = [(35.5, 29.0), (35.5, 58.5)]
steps = 24
for i in range(steps + 1):
    ang = math.radians(180.0 - 180.0 * (i / steps))
    head_pts.append((50.0 + 14.5 * math.cos(ang), 58.5 + 14.5 * math.sin(ang)))
head_pts.append((64.5, 29.0))

polygon(
    head_pts,
    style=fill_style(ARGO_CORAL, border_color=DARK, border_units=2.0),
)

# Pastel blue space-suit neck collar band
rectangle(
    (50.0, 29.0),
    width=36.0,
    height=7.0,
    style=fill_style(ARGO_RIM, border_color=DARK, border_units=2.0, shape_r=3.5),
)

# Two big adorable white circular eyes with dark pupils
for ex, px in ((40.5, 41.5), (59.5, 58.5)):
    circle(
        (ex, 53.5),
        radius=8.5,
        style=fill_style(WHITE, border_color=DARK, border_units=2.0),
    )
    circle(
        (px, 53.5),
        radius=3.5,
        style=fill_style(DARK),
    )

# Happy half-moon smile
smile_pts: list[tuple[float, float]] = []
for i in range(17):
    ang = math.radians(180.0 + 180.0 * (i / 16))
    smile_pts.append((50.0 + 5.2 * math.cos(ang), 41.5 + 4.2 * math.sin(ang)))
polygon(
    smile_pts,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0),
)

# Smooth rounded white reflection highlight on the glass visor
shine_pts: list[tuple[float, float]] = []
for i in range(13):
    ang = math.radians(125.0 + 28.0 * (i / 12))
    shine_pts.append((50.0 + 20.8 * math.cos(ang), 58.0 + 20.8 * math.sin(ang)))
draw_round_polyline(shine_pts, width_units=2.2, color=WHITE)

save()
