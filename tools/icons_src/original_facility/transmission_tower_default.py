# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility concept icon: transmission_tower."""

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w_outer = 2.0
w_inner = 1.6


def _catenary_points(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    steps: int = 18,
) -> list[tuple[float, float]]:
    pts: list[tuple[float, float]] = []
    for i in range(steps + 1):
        t = i / steps
        mt = 1.0 - t
        bx = (mt**2) * p0[0] + 2.0 * mt * t * p1[0] + (t**2) * p2[0]
        by = (mt**2) * p0[1] + 2.0 * mt * t * p1[1] + (t**2) * p2[1]
        pts.append((bx, by))
    return pts


def _draw_green_cable(pts: list[tuple[float, float]]) -> None:
    draw_round_polyline(pts, width_units=4.6, color=DARK)
    draw_round_polyline(pts, width_units=2.1, color=PASTEL_GREEN)


# 1. Catenary PASTEL_GREEN power lines hanging down from insulator suspension points
# Upper cables: left outward sag, center sag across tower, right outward sag
_draw_green_cable(_catenary_points((12.0, 56.5), (17.0, 58.0), (22.0, 62.0)))
_draw_green_cable(_catenary_points((22.0, 62.0), (50.0, 53.0), (78.0, 62.0)))
_draw_green_cable(_catenary_points((78.0, 62.0), (83.0, 58.0), (88.0, 56.5)))

# Lower cables: left outward sag, center sag across tower, right outward sag
_draw_green_cable(_catenary_points((12.0, 36.5), (15.5, 38.0), (19.0, 42.5)))
_draw_green_cable(_catenary_points((19.0, 42.5), (50.0, 32.0), (81.0, 42.5)))
_draw_green_cable(_catenary_points((81.0, 42.5), (84.5, 38.0), (88.0, 36.5)))

# 2. Horizontal steel cross-arms (PASTEL_BLUE_LIGHT)
upper_arm = [
    (20.0, 67.0),
    (80.0, 67.0),
    (56.0, 72.0),
    (44.0, 72.0),
]
polygon(upper_arm, style=no_border_fill(PASTEL_BLUE_LIGHT))
draw_round_polyline(upper_arm, width_units=w_outer, color=DARK, closed=True)

lower_arm = [
    (17.0, 48.0),
    (83.0, 48.0),
    (57.5, 53.5),
    (42.5, 53.5),
]
polygon(lower_arm, style=no_border_fill(PASTEL_BLUE_LIGHT))
draw_round_polyline(lower_arm, width_units=w_outer, color=DARK, closed=True)

# 3. Hanging WHITE ceramic insulators under cross-arm tips
for ix, iy in ((22.0, 64.2), (78.0, 64.2), (19.0, 45.2), (81.0, 45.2)):
    rectangle(
        (ix, iy),
        width=3.6,
        height=5.5,
        style=fill_style(WHITE, border_color=DARK, border_units=w_inner, shape_r=1.5),
    )

# 4. Main tapered steel lattice pylon tower body (PASTEL_BLUE)
pylon_pts = [
    (36.0, 14.0),
    (64.0, 14.0),
    (56.0, 75.0),
    (50.0, 86.0),
    (44.0, 75.0),
]
polygon(pylon_pts, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(pylon_pts, width_units=w_outer, color=DARK, closed=True)

# 5. Lattice horizontal ties and X-bracing inside pylon
levels = [
    (14.0, 36.0, 64.0),
    (31.0, 38.2, 61.8),
    (48.0, 40.5, 59.5),
    (63.0, 42.4, 57.6),
    (75.0, 44.0, 56.0),
]
for y_lvl, x_l, x_r in levels[1:]:
    draw_round_segment((x_l, y_lvl), (x_r, y_lvl), width_units=w_inner, color=DARK)

for i in range(len(levels) - 1):
    y0, xl0, xr0 = levels[i]
    y1, xl1, xr1 = levels[i + 1]
    draw_round_segment((xl0, y0), (xr1, y1), width_units=w_inner, color=DARK)
    draw_round_segment((xr0, y0), (xl1, y1), width_units=w_inner, color=DARK)

# 6. Ground foundation line
draw_round_segment((28.0, 14.0), (72.0, 14.0), width_units=w_outer, color=DARK)

save()
