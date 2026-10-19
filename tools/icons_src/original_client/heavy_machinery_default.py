# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Client concept icon: heavy_machinery."""

import math

from drawlib.canvas import save
from drawlib.shapes import arc, circle, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE


def _draw_segment_bar(x1: float, y1: float, x2: float, y2: float, half_w: float) -> None:
    dx, dy = x2 - x1, y2 - y1
    length = math.hypot(dx, dy)
    nx = -dy / length * half_w
    ny = dx / length * half_w
    pts = [
        (x1 + nx, y1 + ny),
        (x2 + nx, y2 + ny),
        (x2 - nx, y2 - ny),
        (x1 - nx, y1 - ny),
    ]
    polygon(pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
    Icon.draw_round_polyline(pts, width_units=w, color=Icon.DARK, closed=True)


# 1. Articulated excavator boom, stick, and bucket (PASTEL_BLUE)
_draw_segment_bar(45.0, 42.0, 65.0, 72.0, half_w=4.0)
_draw_segment_bar(65.0, 72.0, 81.0, 43.0, half_w=3.5)

bucket_pts = [
    (77.5, 43.5),
    (85.0, 41.5),
    (87.5, 31.0),
    (72.0, 27.5),
    (74.0, 35.5),
]
polygon(
    bucket_pts,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=1.5),
)

for jx, jy in ((65.0, 72.0), (81.0, 43.0)):
    circle(
        (jx, jy),
        radius=3.2,
        style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0),
    )

# 2. Caterpillar track base (PASTEL_BLUE_LIGHT) + track rollers (WHITE)
rectangle(
    (34.0, 20.0),
    width=44.0,
    height=13.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w, shape_r=6.5),
)
for rx in (21.5, 34.0, 46.5):
    circle(
        (rx, 20.0),
        radius=3.2,
        style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.8),
    )

# Turntable ring
rectangle(
    (34.0, 28.5),
    width=30.0,
    height=5.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=2.0, shape_r=1.5),
)

# 3. Excavator cab & engine house (PASTEL_BLUE) + cab window (WHITE)
cab_pts = [
    (14.0, 31.0),
    (14.0, 49.0),
    (20.5, 55.0),
    (46.0, 55.0),
    (50.0, 40.5),
    (50.0, 31.0),
]
polygon(
    cab_pts,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=2.0),
)

win_pts = [
    (31.0, 37.5),
    (31.0, 51.0),
    (43.2, 51.0),
    (46.2, 37.5),
]
polygon(win_pts, style=Icon.no_border_fill(Icon.WHITE))
Icon.draw_round_polyline(win_pts, width_units=2.0, color=Icon.DARK, closed=True)

# 4. Smart-construction beacon & signal arc on cab roof (PASTEL_GREEN)
bx, by = 32.0, 58.5
rectangle(
    (bx, by),
    width=8.5,
    height=7.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0, shape_r=3.5),
)

arc_cy = by + 3.0
for r in (10.5, 17.5):
    diam = r * 2.0
    arc(
        (bx, arc_cy),
        width=diam,
        height=diam,
        angle_start=45.0,
        angle_end=135.0,
        style=Icon.stroke_style(Icon.DARK, width_units=4.4),
    )
    for ang_deg in (45.0, 135.0):
        rad = math.radians(ang_deg)
        Icon.draw_cap(
            (bx + r * math.cos(rad), arc_cy + r * math.sin(rad)),
            width_units=4.4,
            color=Icon.DARK,
        )
    arc(
        (bx, arc_cy),
        width=diam,
        height=diam,
        angle_start=45.0,
        angle_end=135.0,
        style=Icon.stroke_style(Icon.PASTEL_GREEN, width_units=1.8),
    )
    for ang_deg in (45.0, 135.0):
        rad = math.radians(ang_deg)
        Icon.draw_cap(
            (bx + r * math.cos(rad), arc_cy + r * math.sin(rad)),
            width_units=1.8,
            color=Icon.PASTEL_GREEN,
        )

save()
