# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps concept icon: vault."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import Icon


def _square_pts(cx: float, cy: float, half: float) -> list[tuple[float, float]]:
    """Build axis-aligned square vertices centered at (cx, cy)."""
    return [
        (cx - half, cy - half),
        (cx + half, cy - half),
        (cx + half, cy + half),
        (cx - half, cy + half),
    ]


Icon.setup()

w = 2.0
w_hole = 1.4

# 1. Downward-pointing outer triangle
tri_pts = [
    (11.5, 88.5),
    (50.0, 11.5),
    (88.5, 88.5),
]

# 2. Ten transparent square holes (3x3 grid + 1 bottom-center square)
half_sq = 2.45
step = 7.5
col_xs = [50.0 - step, 50.0, 50.0 + step]
row_ys = [73.0, 65.5, 58.0]

holes: list[list[tuple[float, float]]] = []
for ry in row_ys:
    for cx in col_xs:
        holes.append(_square_pts(cx, ry, half_sq))

# Bottom 10th square in center column
holes.append(_square_pts(50.0, 58.0 - step, half_sq))

# 3. Compound Amber2 fill with transparent holes + DARK borders
polygon(tri_pts, holes=holes, style=Icon.fill_style(Colors.Amber3))
Icon.draw_round_polyline(tri_pts, width_units=w, color=Icon.DARK, closed=True)
for hole in holes:
    Icon.draw_round_polyline(hole, width_units=w_hole, color=Icon.DARK, closed=True)

save()
