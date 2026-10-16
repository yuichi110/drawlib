# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: trino."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, ellipse, polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 1.9
cx, cy = 46.5, 34.5


def _bezier(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    steps: int = 16,
) -> list[tuple[float, float]]:
    """Sample cubic Bezier curve excluding p0."""
    pts: list[tuple[float, float]] = []
    for i in range(1, steps + 1):
        t = i / steps
        mt = 1.0 - t
        x = (mt**3) * p0[0] + 3 * (mt**2) * t * p1[0] + 3 * mt * (t**2) * p2[0] + (t**3) * p3[0]
        y = (mt**3) * p0[1] + 3 * (mt**2) * t * p1[1] + 3 * mt * (t**2) * p2[1] + (t**3) * p3[1]
        pts.append((x, y))
    return pts


# 1. Left upright bunny ear (WHITE outer + Colors.Pink3 inner with generous white rim)
left_ear_out = [
    (32.8, 53.0),
    *_bezier((32.8, 53.0), (29.2, 66.5), (29.0, 89.0), (36.2, 89.0), 16),
    *_bezier((36.2, 89.0), (43.4, 89.0), (43.4, 67.0), (42.8, 55.0), 16),
]
polygon(left_ear_out, style=no_border_fill(WHITE))
draw_round_polyline(left_ear_out, width_units=w, color=DARK, closed=True)

left_ear_in = [
    (35.8, 55.0),
    *_bezier((35.8, 55.0), (33.8, 65.5), (33.8, 82.0), (36.4, 82.0), 14),
    *_bezier((36.4, 82.0), (39.0, 82.0), (39.2, 66.0), (39.0, 56.0), 14),
]
polygon(left_ear_in, style=no_border_fill(Colors.Pink3))
draw_round_polyline(left_ear_in, width_units=1.5, color=DARK, closed=True)

# 2. Right tilted bunny ear (WHITE outer + Colors.Pink3 inner with generous white rim)
right_ear_out = [
    (51.2, 54.5),
    *_bezier((51.2, 54.5), (57.2, 72.0), (69.0, 89.0), (76.2, 85.8), 16),
    *_bezier((76.2, 85.8), (82.2, 82.5), (68.8, 63.0), (60.5, 50.5), 16),
]
polygon(right_ear_out, style=no_border_fill(WHITE))
draw_round_polyline(right_ear_out, width_units=w, color=DARK, closed=True)

right_ear_in = [
    (54.8, 53.8),
    *_bezier((54.8, 53.8), (60.2, 68.0), (68.2, 80.5), (71.5, 78.8), 14),
    *_bezier((71.5, 78.8), (74.2, 77.2), (65.0, 63.2), (57.8, 52.0), 14),
]
polygon(right_ear_in, style=no_border_fill(Colors.Pink3))
draw_round_polyline(right_ear_in, width_units=1.5, color=DARK, closed=True)

# 3. Right helmet antenna rod & bulb
draw_round_segment((69.5, 42.0), (69.5, 57.5), width_units=1.8, color=DARK)
circle(
    (69.5, 60.5),
    radius=4.2,
    style=fill_style(Colors.Pink3, border_color=DARK, border_units=1.7),
)

# 4. Side helmet ear-pods (Colors.Purple3)
for x_pod in (19.5, 73.5):
    rectangle(
        (x_pod, 33.5),
        width=8.0,
        height=14.0,
        style=fill_style(Colors.Purple3, border_color=DARK, border_units=1.8, shape_r=3.2),
    )

# 5. Curved space-suit neck collar at bottom (Colors.Purple3)
collar_pts: list[tuple[float, float]] = []
for i in range(17):
    ang = math.radians(212.0 + 116.0 * (i / 16))
    collar_pts.append((cx + 25.0 * math.cos(ang), cy + 24.5 * math.sin(ang)))
for i in range(17):
    ang = math.radians(328.0 - 116.0 * (i / 16))
    collar_pts.append((cx + 21.0 * math.cos(ang), cy - 3.5 + 21.5 * math.sin(ang)))
polygon(collar_pts, style=no_border_fill(Colors.Purple3))
draw_round_polyline(collar_pts, width_units=1.8, color=DARK, closed=True)

# 6. Main space helmet dome (WHITE)
ellipse(
    (cx, cy),
    width=52.0,
    height=46.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w),
)

# 7. Top helmet forehead cap panel (Colors.Purple3)
rectangle(
    (cx, 52.8),
    width=14.0,
    height=6.2,
    style=fill_style(Colors.Purple3, border_color=DARK, border_units=1.6, shape_r=1.6),
)

# 8. Inner glass visor (Colors.Teal2)
ellipse(
    (cx, 32.5),
    width=39.0,
    height=29.0,
    style=fill_style(Colors.Teal2, border_color=DARK, border_units=1.7),
)

# 9. Cute bunny face inside visor
for x_cheek in (32.0, 61.0):
    ellipse((x_cheek, 28.5), width=5.2, height=3.8, style=no_border_fill(WHITE))

for x_eye in (37.2, 55.8):
    circle((x_eye, 34.0), radius=2.7, style=fill_style(DARK))
    circle((x_eye + 0.7, 34.7), radius=0.8, style=fill_style(WHITE))

ellipse((cx, 29.8), width=3.8, height=2.6, style=fill_style(DARK))
draw_round_segment((cx, 29.0), (cx, 26.2), width_units=1.5, color=DARK)
smile_l = [(cx - 4.8, 27.0), *_bezier((cx - 4.8, 27.0), (cx - 3.8, 24.5), (cx - 1.2, 24.5), (cx, 26.2), 8)]
smile_r = [(cx, 26.2), *_bezier((cx, 26.2), (cx + 1.2, 24.5), (cx + 3.8, 24.5), (cx + 4.8, 27.0), 8)]
draw_round_polyline(smile_l, width_units=1.5, color=DARK)
draw_round_polyline(smile_r, width_units=1.5, color=DARK)

save()
