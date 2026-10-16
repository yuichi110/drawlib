# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: backstage."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE


def build_2d_b(x0: float, y0: float) -> list[tuple[float, float]]:
    """Build a bold, rounded upright 2D letter 'B' contour with bottom-left at (x0, y0)."""
    height = 56.0
    r_left = 5.5
    waist_x = x0 + 25.5
    pts: list[tuple[float, float]] = []

    # Bottom-left rounded corner (180 deg to 270 deg around (x0 + r_left, y0 + r_left))
    steps_c = 8
    for i in range(steps_c + 1):
        ang = math.radians(180.0 + 90.0 * (i / steps_c))
        pts.append((x0 + r_left + r_left * math.cos(ang), y0 + r_left + r_left * math.sin(ang)))

    # Lower bowl arc from (waist_x, y0) around right to (waist_x, y0 + 28.8)
    lower_cy = y0 + 14.4
    lower_rx = 18.0
    lower_ry = 14.4
    steps_b = 20
    for i in range(steps_b + 1):
        ang = math.radians(-90.0 + 180.0 * (i / steps_b))
        pts.append((waist_x + lower_rx * math.cos(ang), lower_cy + lower_ry * math.sin(ang)))

    # Upper bowl arc from (waist_x, y0 + 28.8) around right to (waist_x, y0 + height)
    upper_cy = y0 + 42.4
    upper_rx = 16.0
    upper_ry = 13.6
    for i in range(1, steps_b + 1):
        ang = math.radians(-90.0 + 180.0 * (i / steps_b))
        pts.append((waist_x + upper_rx * math.cos(ang), upper_cy + upper_ry * math.sin(ang)))

    # Top-left rounded corner (90 deg to 180 deg around (x0 + r_left, y0 + height - r_left))
    for i in range(steps_c + 1):
        ang = math.radians(90.0 + 90.0 * (i / steps_c))
        pts.append((x0 + r_left + r_left * math.cos(ang), y0 + height - r_left + r_left * math.sin(ang)))

    return pts


def build_b_counter(
    x_left: float, y_bot: float, y_top: float, x_arc_center: float, rx: float
) -> list[tuple[float, float]]:
    """Build a tangential D-shaped inner counter hole with rounded left corners."""
    r_in = 2.0
    cy = 0.5 * (y_bot + y_top)
    ry = 0.5 * (y_top - y_bot)
    pts: list[tuple[float, float]] = []

    steps_c = 6
    # Bottom-left inner corner
    for i in range(steps_c + 1):
        ang = math.radians(180.0 + 90.0 * (i / steps_c))
        pts.append((x_left + r_in + r_in * math.cos(ang), y_bot + r_in + r_in * math.sin(ang)))

    # Tangential right semicircular arc
    steps_a = 16
    for i in range(steps_a + 1):
        ang = math.radians(-90.0 + 180.0 * (i / steps_a))
        pts.append((x_arc_center + rx * math.cos(ang), cy + ry * math.sin(ang)))

    # Top-left inner corner
    for i in range(steps_c + 1):
        ang = math.radians(90.0 + 90.0 * (i / steps_c))
        pts.append((x_left + r_in + r_in * math.cos(ang), y_top - r_in + r_in * math.sin(ang)))

    return pts


# Three cascading 2D upright 'B' layers (back-right to front-left)
layers = [
    (35.5, 16.0, PASTEL_GREEN),
    (28.5, 22.0, PASTEL_BLUE_LIGHT),
    (21.5, 28.0, PASTEL_BLUE),
]

for lx, ly, color in layers:
    b_pts = build_2d_b(lx, ly)
    polygon(b_pts, style=no_border_fill(color))
    draw_round_polyline(b_pts, width_units=w, color=DARK, closed=True)

# Crisp white D-shaped inner cutouts on the front 'B' layer (lx=21.5, ly=28.0)
front_x, front_y = 21.5, 28.0
for y_b, y_t, x_c, rx in (
    (front_y + 8.5, front_y + 21.0, front_x + 21.5, 9.5),
    (front_y + 35.0, front_y + 47.5, front_x + 21.0, 8.0),
):
    hole_pts = build_b_counter(front_x + 12.0, y_b, y_t, x_c, rx)
    polygon(hole_pts, style=no_border_fill(WHITE))
    draw_round_polyline(hole_pts, width_units=2.4, color=DARK, closed=True)

save()
