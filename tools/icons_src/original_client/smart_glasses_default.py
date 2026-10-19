# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Client concept icon: smart_glasses."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE


def rounded_rect_pts(
    cx: float,
    cy: float,
    width: float,
    height: float,
    r: float,
    steps: int = 10,
) -> list[tuple[float, float]]:
    """Return counter-clockwise rounded rectangle points."""
    x0, x1 = cx - width / 2.0, cx + width / 2.0
    y0, y1 = cy - height / 2.0, cy + height / 2.0
    pts: list[tuple[float, float]] = []
    corners = [
        (x1 - r, y1 - r, 0.0, 90.0),
        (x0 + r, y1 - r, 90.0, 180.0),
        (x0 + r, y0 + r, 180.0, 270.0),
        (x1 - r, y0 + r, 270.0, 360.0),
    ]
    for ccx, ccy, a0, a1 in corners:
        for i in range(steps + 1):
            ang = math.radians(a0 + (a1 - a0) * (i / steps))
            pts.append((ccx + r * math.cos(ang), ccy + r * math.sin(ang)))
    return pts


# 1. Left & right temple arms extending up and inward behind the front frame
left_arm: list[tuple[float, float]] = [
    (13.5, 51.0),
    (27.5, 75.5),
    (36.0, 75.5),
    (39.0, 70.5),
    (35.0, 68.5),
    (32.5, 70.5),
    (29.8, 70.5),
    (19.5, 51.0),
]
right_arm: list[tuple[float, float]] = [(100.0 - x, y) for x, y in left_arm]

for arm_pts in (left_arm, right_arm):
    polygon(arm_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE_LIGHT))
    Icon.draw_round_polyline(arm_pts, width_units=w, color=Icon.DARK, closed=True)

# 2. Unified front glasses frame (left rim + nose bridge + right rim)
# Build single outer silhouette so there are no stroke seams across the nose bridge
frame_pts: list[tuple[float, float]] = []
steps = 10

# Left rim outer corners: top-left (90->180), bottom-left (180->270), bottom-right (270->345)
lx0, lx1 = 12.5, 45.5
rx0, rx1 = 54.5, 87.5
y0, y1 = 27.0, 54.0
rf = 6.5

# Top bar from right-top to left-top (with subtle center dip)
for i in range(steps + 1):
    ang = math.radians(0.0 + 90.0 * (i / steps))
    frame_pts.append((rx1 - rf + rf * math.cos(ang), y1 - rf + rf * math.sin(ang)))

frame_pts.append((55.0, y1))
frame_pts.append((50.0, y1 - 1.2))
frame_pts.append((45.0, y1))

for i in range(steps + 1):
    ang = math.radians(90.0 + 90.0 * (i / steps))
    frame_pts.append((lx0 + rf + rf * math.cos(ang), y1 - rf + rf * math.sin(ang)))

for i in range(steps + 1):
    ang = math.radians(180.0 + 90.0 * (i / steps))
    frame_pts.append((lx0 + rf + rf * math.cos(ang), y0 + rf + rf * math.sin(ang)))

for i in range(steps + 1):
    ang = math.radians(270.0 + 90.0 * (i / steps))
    frame_pts.append((lx1 - rf + rf * math.cos(ang), y0 + rf + rf * math.sin(ang)))

# Nose bridge arch connecting left inner edge to right inner edge
frame_pts.append((lx1, 43.0))
for i in range(13):
    ang = math.radians(180.0 - 180.0 * (i / 12))
    frame_pts.append((50.0 + 4.5 * math.cos(ang), 43.0 + 4.5 * math.sin(ang)))
frame_pts.append((rx0, 43.0))

for i in range(steps + 1):
    ang = math.radians(180.0 + 90.0 * (i / steps))
    frame_pts.append((rx0 + rf + rf * math.cos(ang), y0 + rf + rf * math.sin(ang)))

for i in range(steps + 1):
    ang = math.radians(270.0 + 90.0 * (i / steps))
    frame_pts.append((rx1 - rf + rf * math.cos(ang), y0 + rf + rf * math.sin(ang)))

polygon(frame_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(frame_pts, width_units=w, color=Icon.DARK, closed=True)

# 3. Left & right WHITE lenses
for lcx in (29.0, 71.0):
    rectangle(
        (lcx, 40.5),
        width=23.5,
        height=18.0,
        style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0, shape_r=4.0),
    )

# 4. Smart corner camera on outer left frame lug
circle(
    (16.8, 49.5),
    radius=2.6,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.6),
)

# 5. PASTEL_GREEN AR HUD overlay inside the right lens
rectangle(
    (71.0, 42.2),
    width=12.5,
    height=7.5,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.7, shape_r=2.0),
)
Icon.draw_round_polyline([(66.5, 35.8), (75.5, 35.8)], width_units=1.8, color=Icon.DARK, closed=False)

save()
