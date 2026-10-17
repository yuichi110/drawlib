# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Workspace concept icon: figma."""

import math
from typing import Any

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import DARK, draw_round_polyline, fill_style, no_border_fill, setup_icon

setup_icon()
w = 1.9
s = 38.8 / 41.0
r = 41.0 / 3.0


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


def _arc(cx: float, cy: float, rad: float, deg0: float, deg1: float, steps: int = 24) -> list[tuple[float, float]]:
    return [
        (
            cx + rad * math.cos(math.radians(deg0 + (deg1 - deg0) * i / steps)),
            cy + rad * math.sin(math.radians(deg0 + (deg1 - deg0) * i / steps)),
        )
        for i in range(steps + 1)
    ]


# 1. Bottom-left droplet (green #6BE2B4)
bl_green = _sc([(50.0, 50.0 - r), *_arc(50.0 - r, 50.0 - 2.0 * r, r, 0.0, -270.0, 36)])

# 2. Middle-left half-pill (purple #C494FF)
ml_purple = _sc([(50.0, 50.0 + r), *_arc(50.0 - r, 50.0, r, 90.0, 270.0, 24), (50.0, 50.0 - r)])

# 3. Top-left half-pill (red-orange #F78C6B)
tl_orange = _sc([(50.0, 50.0 + 3.0 * r), *_arc(50.0 - r, 50.0 + 2.0 * r, r, 90.0, 270.0, 24), (50.0, 50.0 + r)])

# 4. Top-right half-pill (coral #FFA399)
tr_coral = _sc([(50.0, 50.0 + r), *_arc(50.0 + r, 50.0 + 2.0 * r, r, -90.0, 90.0, 24), (50.0, 50.0 + 3.0 * r)])

blocks: list[tuple[list[tuple[float, float]], Any]] = [
    (bl_green, "#6BE2B4"),
    (ml_purple, "#C494FF"),
    (tl_orange, "#F78C6B"),
    (tr_coral, "#FFA399"),
]

for pts, col in blocks:
    polygon(pts, style=no_border_fill(col))
    draw_round_polyline(pts, width_units=w, color=DARK, closed=True)

# 5. Middle-right circle (cyan #73D6FE)
cx_mr, cy_mr = _sc([(50.0 + r, 50.0)])[0]
circle((cx_mr, cy_mr), radius=r * s, style=fill_style("#73D6FE", border_color=DARK, border_units=w))

save()
