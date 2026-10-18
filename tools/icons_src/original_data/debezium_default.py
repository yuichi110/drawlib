# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: debezium."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)


def _arc_points(
    cx: float,
    cy: float,
    radius: float,
    deg_start: float,
    deg_end: float,
    steps: int = 14,
) -> list[tuple[float, float]]:
    """Sample circular arc points from deg_start to deg_end inclusive."""
    pts: list[tuple[float, float]] = []
    for i in range(steps + 1):
        t = i / steps
        ang = math.radians(deg_start + (deg_end - deg_start) * t)
        pts.append((cx + radius * math.cos(ang), cy + radius * math.sin(ang)))
    return pts


def _build_cascade_band(
    cells: list[tuple[int, int]],
    x0: list[float],
    x1: list[float],
    y0: list[float],
    y1: list[float],
    r_out: float,
    r_in: float,
) -> list[tuple[float, float]]:
    """Build closed polygon for a diagonal chain of cascading Debezium cells."""
    k = len(cells)
    pts: list[tuple[float, float]] = []

    # Start at sharp top-left corner of the first cell
    c0, row0 = cells[0]
    pts.append((x0[c0], y1[row0]))

    # Trace upper-right boundary from top-left cell to bottom-right cell
    for i, (c, row) in enumerate(cells):
        pts.extend(_arc_points(x1[c] - r_out, y1[row] - r_out, r_out, 90.0, 0.0))
        if i < k - 1:
            pts.extend(_arc_points(x1[c] + r_in, y0[row] + r_out, r_in, 180.0, 270.0))
        else:
            pts.append((x1[c], y0[row]))

    # Trace lower-left boundary back from bottom-right cell to top-left cell
    for i in range(k - 1, -1, -1):
        c, row = cells[i]
        pts.extend(_arc_points(x0[c] + r_out, y0[row] + r_out, r_out, 270.0, 180.0))
        if i > 0:
            pts.extend(_arc_points(x0[c] - r_in, y1[row] - r_out, r_in, 0.0, 90.0))

    return pts


setup_icon()

# 3x3 cascading grid spanning [12.0, 88.0] x [12.0, 88.0]
cell_w = 21.6
gap = 5.6
r_convex = 9.6
r_concave = r_convex + gap  # 15.2 for exact G1 tangent waist joins

grid_x0 = [12.0 + i * (cell_w + gap) for i in range(3)]
grid_x1 = [x + cell_w for x in grid_x0]
grid_y0 = [12.0 + i * (cell_w + gap) for i in range(3)]
grid_y1 = [y + cell_w for y in grid_y0]

bands = [
    ([(0, 0)], Colors.Teal2),
    ([(0, 1), (1, 0)], Colors.Teal3),
    ([(0, 2), (1, 1), (2, 0)], Colors.Green3),
    ([(1, 2), (2, 1)], Colors.Blue3),
    ([(2, 2)], Colors.Blue2),
]

for cell_chain, fill_col in bands:
    poly_pts = _build_cascade_band(
        cell_chain,
        grid_x0,
        grid_x1,
        grid_y0,
        grid_y1,
        r_convex,
        r_concave,
    )
    polygon(poly_pts, style=no_border_fill(fill_col))
    draw_round_polyline(poly_pts, width_units=2.0, color=DARK, closed=True)

save()
