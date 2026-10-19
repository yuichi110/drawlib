# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: tidb."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

Icon.setup()

w = 2.0
cx, cy = 50.0, 50.0
r_hex = 41.0
u = r_hex * math.cos(math.radians(30.0)) / 3.0
v = r_hex / 6.0


def _iso(iu: float, iv: float) -> tuple[float, float]:
    """Map 3x3 isometric grid coordinates (iu, iv) to canvas (x, y)."""
    return (cx + iu * u, cy + iv * v)


# 1. Outer pointy-top hexagon badge (Colors.Red3)
hex_pts = [
    _iso(0.0, 6.0),
    _iso(3.0, 3.0),
    _iso(3.0, -3.0),
    _iso(0.0, -6.0),
    _iso(-3.0, -3.0),
    _iso(-3.0, 3.0),
]
polygon(
    hex_pts,
    style=Icon.fill_style(Colors.Red3, border_color=Icon.DARK, border_units=w, shape_r=4.2),
)

# 2. Central isometric T-bar & vertical stem (WHITE)
t_pts = [
    _iso(0.0, 4.0),
    _iso(-2.0, 2.0),
    _iso(-2.0, 0.0),
    _iso(-1.0, 1.0),
    _iso(-1.0, -3.0),
    _iso(0.0, -4.0),
    _iso(0.0, 2.0),
    _iso(1.0, 3.0),
]
polygon(t_pts, style=Icon.no_border_fill(Icon.WHITE))
Icon.draw_round_polyline(t_pts, width_units=1.8, color=Icon.DARK, closed=True)

# 3. Right isometric vertical stem "I" (Colors.Red1)
i_pts = [
    _iso(1.0, 1.0),
    _iso(1.0, -3.0),
    _iso(2.0, -2.0),
    _iso(2.0, 2.0),
]
polygon(i_pts, style=Icon.no_border_fill(Colors.Red1))
Icon.draw_round_polyline(i_pts, width_units=1.8, color=Icon.DARK, closed=True)

save()
