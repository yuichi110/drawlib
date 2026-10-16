# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: opentelemetry."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, ellipse, polygon
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    fill_style,
    setup_icon,
)

setup_icon()

w = 2.6
angle_deg = 38.0
theta = math.radians(angle_deg)
ux, uy = math.cos(theta), math.sin(theta)
nx, ny = -uy, ux

cx_ref, cy_ref = 46.5, 47.5


def _tilted_rect(s0: float, s1: float, half_h: float) -> list[tuple[float, float]]:
    """Build a rectangle along the tilted telescope axis from s0 to s1."""
    p0x, p0y = cx_ref + s0 * ux, cy_ref + s0 * uy
    p1x, p1y = cx_ref + s1 * ux, cy_ref + s1 * uy
    return [
        (p0x - half_h * nx, p0y - half_h * ny),
        (p1x - half_h * nx, p1y - half_h * ny),
        (p1x + half_h * nx, p1y + half_h * ny),
        (p0x + half_h * nx, p0y + half_h * ny),
    ]


# 1. Eyepiece flange & lower-left narrower tube (PASTEL_BLUE_LIGHT)
polygon(
    _tilted_rect(-31.5, -26.0, 9.2),
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.4, shape_r=2.2),
)
polygon(
    _tilted_rect(-26.5, -9.0, 7.6),
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w, shape_r=2.5),
)

# 2. Middle main telescope tube (PASTEL_BLUE)
polygon(
    _tilted_rect(-10.0, 12.5, 11.6),
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=3.2),
)

# 3. Upper-right wide lens hood (PASTEL_GREEN) + WHITE glass ellipse
polygon(
    _tilted_rect(11.5, 28.0, 15.8),
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w, shape_r=3.8),
)
lens_cx = cx_ref + 25.0 * ux
lens_cy = cy_ref + 25.0 * uy
ellipse(
    (lens_cx, lens_cy),
    width=6.4,
    height=19.2,
    style=fill_style(WHITE, border_color=DARK, border_units=2.2, angle=angle_deg),
)

# 4. Circular mount / pivot ring below the middle tube
mount_cx = cx_ref + 2.0 * ux - 13.2 * nx
mount_cy = cy_ref + 2.0 * uy - 13.2 * ny
circle(
    (mount_cx, mount_cy),
    radius=9.2,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.4),
)
circle(
    (mount_cx, mount_cy),
    radius=4.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0),
)

# 5. Two small star / signal dots at top-right
circle(
    (82.0, 61.0),
    radius=3.8,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0),
)
circle(
    (84.5, 73.5),
    radius=2.8,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0),
)

save()
