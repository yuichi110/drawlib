# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps concept icon: k6."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

Icon.setup()

w = 2.0
w_in = 1.6


def _s(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Scale official 100x100 coords by 0.94 around (50, 50)."""
    return [(50.0 + (x - 50.0) * 0.94, 50.0 + (y - 50.0) * 0.94) for x, y in pts]


# 1. Double-peaked mountain polygon (Colors.Purple3)
mountain_pts = _s(
    [
        (90.89, 9.0),
        (9.11, 9.0),
        (36.34, 69.0),
        (52.74, 56.54),
        (74.13, 91.0),
    ]
)
polygon(mountain_pts, style=Icon.no_border_fill(Colors.Purple3))
Icon.draw_round_polyline(mountain_pts, width_units=w, color=Icon.DARK, closed=True)

# 2. Crisp WHITE 'k' polygon
k_pts = _s(
    [
        (42.62, 29.1),
        (47.39, 22.13),
        (52.49, 22.13),
        (46.87, 30.21),
        (51.86, 37.35),
        (48.55, 39.72),
        (47.09, 37.73),
        (42.61, 31.2),
        (42.61, 44.32),
        (38.15, 48.08),
        (38.15, 22.13),
        (42.61, 22.13),
    ]
)
polygon(k_pts, style=Icon.no_border_fill(Icon.WHITE))
Icon.draw_round_polyline(k_pts, width_units=w_in, color=Icon.DARK, closed=True)

# 3. Crisp WHITE '6' compound polygon (transparent inner counter showing Colors.Purple3)
six_outer = _s(
    [
        (60.9, 21.96),
        (62.28, 22.06),
        (63.45, 22.33),
        (64.56, 22.79),
        (65.58, 23.42),
        (66.51, 24.21),
        (67.33, 25.12),
        (67.99, 26.17),
        (68.47, 27.31),
        (68.76, 28.52),
        (68.85, 29.91),
        (68.76, 31.11),
        (68.46, 32.26),
        (67.98, 33.36),
        (67.31, 34.34),
        (66.41, 35.27),
        (65.37, 36.09),
        (64.22, 36.68),
        (62.97, 37.05),
        (61.79, 37.16),
        (61.11, 37.06),
        (65.43, 43.69),
        (61.99, 46.17),
        (60.37, 43.69),
        (56.2, 37.13),
        (55.07, 35.34),
        (54.19, 33.77),
        (53.57, 32.33),
        (53.2, 31.1),
        (53.06, 29.82),
        (53.15, 28.46),
        (53.43, 27.26),
        (53.91, 26.14),
        (54.55, 25.11),
        (55.36, 24.2),
        (56.28, 23.41),
        (57.3, 22.78),
        (58.4, 22.32),
        (59.55, 22.04),
    ]
)

six_hole = _s(
    [
        (60.91 + 3.32 * math.cos(2.0 * math.pi * i / 32), 29.7 + 3.39 * math.sin(2.0 * math.pi * i / 32))
        for i in range(32)
    ]
)

polygon(six_outer, holes=[six_hole], style=Icon.fill_style(Icon.WHITE))
Icon.draw_round_polyline(six_outer, width_units=w_in, color=Icon.DARK, closed=True)
Icon.draw_round_polyline(six_hole, width_units=w_in, color=Icon.DARK, closed=True)

save()
