# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security icon: osquery."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

# ruff: noqa: E501
Icon.setup()

w = 2.0
s = 0.96


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


# fmt: off
purple_blades = [
    _sc([(90.95, 91.0), (90.95, 70.48), (70.48, 50.0), (70.48, 70.56)]),
    _sc([(91.0, 9.05), (70.48, 9.05), (50.0, 29.52), (70.56, 29.52)]),
    _sc([(9.04, 9.0), (9.04, 29.52), (29.52, 50.0), (29.52, 29.44)]),
    _sc([(9.0, 90.96), (29.52, 90.96), (50.0, 70.48), (29.44, 70.48)]),
]

slate_blades = [
    _sc([(50.0, 91.0), (50.0, 70.48), (70.48, 50.0), (70.48, 70.56)]),
    _sc([(91.0, 50.0), (70.48, 50.0), (50.0, 29.52), (70.56, 29.52)]),
    _sc([(50.0, 9.0), (50.0, 29.52), (29.52, 50.0), (29.52, 29.44)]),
    _sc([(9.0, 50.0), (29.52, 50.0), (50.0, 70.48), (29.44, 70.48)]),
]
# fmt: on

# 1. Fill alternating purple (Colors.Purple3) and dark slate (Colors.Gray6) blades
#    (center diamond hole remains completely transparent)
for blade in purple_blades:
    polygon(blade, style=Icon.no_border_fill(Colors.Purple3))
for blade in slate_blades:
    polygon(blade, style=Icon.no_border_fill(Colors.Gray6))

# 2. Crisp DARK w=1.6 outlines around all 8 pinwheel blades
for blade in [*purple_blades, *slate_blades]:
    Icon.draw_round_polyline(blade, width_units=w, color=Icon.DARK, closed=True)

save()
