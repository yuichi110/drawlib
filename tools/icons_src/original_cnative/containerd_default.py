# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: containerd."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE
s = 0.96


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Scale points around (50, 50) so w=2.0 border sits cleanly inside [10, 90]."""
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


outer_rect = _sc([(21.85, 9.52), (78.27, 9.52), (78.27, 90.38), (21.85, 90.38)])
d_outer = _sc(
    [
        (31.26, 18.92),
        (68.88, 18.92),
        (68.88, 67.83),
        (57.58, 67.83),
        (57.58, 54.65),
        (31.26, 54.65),
    ]
)
d_hole = _sc([(42.54, 28.33), (57.58, 28.33), (57.58, 45.25), (42.54, 45.25)])

# 1. Outer vertical rectangle in Colors.Gray6 with w=2.0 DARK border
polygon(outer_rect, style=Icon.fill_style(Colors.Gray6))
Icon.draw_round_polyline(outer_rect, width_units=w, color=Icon.DARK, closed=True)

# 2. White block-letter "d" with inner hole revealing Colors.Gray6 underneath
polygon(d_outer, holes=[d_hole], style=Icon.fill_style(Icon.WHITE))
Icon.draw_round_polyline(d_outer, width_units=w, color=Icon.DARK, closed=True)
Icon.draw_round_polyline(d_hole, width_units=w, color=Icon.DARK, closed=True)

save()
