# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: linkerd."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

Icon.setup()

w = 2.0
cos30 = math.cos(math.radians(30.0))
sin30 = math.sin(math.radians(30.0))

# Isometric coordinate helper: (u, v) on top diamond [0, 36] x [0, 36], z downwards
# Front corner of top diamond is (u=0, v=0, z=0) at (50.0, 48.0).
cx_front, cy_front = 50.0, 48.0


def _iso(u: float, v: float, z: float = 0.0) -> tuple[float, float]:
    """Convert isometric coordinates (u, v, z) to 2D canvas coordinates."""
    x = cx_front + (u - v) * cos30
    y = cy_front + (u + v) * sin30 - z
    return (x, y)


def _draw_iso_poly(pts: list[tuple[float, float]], color: str) -> None:
    """Draw an isometric polygon with rounded corner joins."""
    polygon(pts, style=Icon.no_border_fill(color))
    Icon.draw_round_polyline(pts, width_units=w, color=Icon.DARK, closed=True)


# 1. 4 vertical front pillars (2 on front-left face u=0, 2 on front-right face v=0)
pillar_h = 31.0

_draw_iso_poly(
    [_iso(0.0, 36.0, 0.0), _iso(0.0, 26.5, 0.0), _iso(0.0, 26.5, pillar_h), _iso(0.0, 36.0, pillar_h)],
    Icon.PASTEL_BLUE,
)
_draw_iso_poly(
    [_iso(0.0, 14.5, 0.0), _iso(0.0, 5.0, 0.0), _iso(0.0, 5.0, pillar_h), _iso(0.0, 14.5, pillar_h)],
    Icon.PASTEL_BLUE_LIGHT,
)
_draw_iso_poly(
    [_iso(5.0, 0.0, 0.0), _iso(14.5, 0.0, 0.0), _iso(14.5, 0.0, pillar_h), _iso(5.0, 0.0, pillar_h)],
    Icon.PASTEL_BLUE_LIGHT,
)
_draw_iso_poly(
    [_iso(26.5, 0.0, 0.0), _iso(36.0, 0.0, 0.0), _iso(36.0, 0.0, pillar_h), _iso(26.5, 0.0, pillar_h)],
    Icon.PASTEL_BLUE,
)

# 2. Top isometric woven lattice (3 bars along u in WHITE, 3 bars along v in PASTEL_GREEN)
bands = [(0.0, 9.0), (13.5, 22.5), (27.0, 36.0)]

# Draw WHITE bars along u first
for u0, u1 in bands:
    _draw_iso_poly(
        [_iso(u0, 0.0), _iso(u1, 0.0), _iso(u1, 36.0), _iso(u0, 36.0)],
        Icon.WHITE,
    )

# Draw PASTEL_GREEN bars along v second
for v0, v1 in bands:
    _draw_iso_poly(
        [_iso(0.0, v0), _iso(36.0, v0), _iso(36.0, v1), _iso(0.0, v1)],
        Icon.PASTEL_GREEN,
    )

# 3. Over-weave patches where WHITE bars pass over PASTEL_GREEN bars ((i + j) % 2 == 1)
# Fill with WHITE across the crossing and stroke only the two side edges (u=u0 and u=u1)
# so the WHITE bar flows continuously without cross-seams.
for i, (u0, u1) in enumerate(bands):
    for j, (v0, v1) in enumerate(bands):
        if (i + j) % 2 == 1:
            vp0 = max(0.0, v0 - 1.8)
            vp1 = min(36.0, v1 + 1.8)
            polygon(
                [_iso(u0, vp0), _iso(u1, vp0), _iso(u1, vp1), _iso(u0, vp1)],
                style=Icon.no_border_fill(Icon.WHITE),
            )
            Icon.draw_round_segment(_iso(u0, vp0), _iso(u0, vp1), width_units=w, color=Icon.DARK)
            Icon.draw_round_segment(_iso(u1, vp0), _iso(u1, vp1), width_units=w, color=Icon.DARK)
            if v0 == 0.0:
                Icon.draw_round_segment(_iso(u0, 0.0), _iso(u1, 0.0), width_units=w, color=Icon.DARK)
            if v1 == 36.0:
                Icon.draw_round_segment(_iso(u0, 36.0), _iso(u1, 36.0), width_units=w, color=Icon.DARK)

save()
