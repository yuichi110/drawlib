# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps concept icon: buildkite."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 2.0
scale = 0.95


def _sc(x: float, y: float) -> tuple[float, float]:
    return (50.0 + (x - 50.0) * scale, 50.0 + (y - 50.0) * scale)


panel_1 = [_sc(9.00, 77.33), _sc(36.33, 63.94), _sc(36.33, 36.61), _sc(9.00, 50.00)]
panel_2 = [_sc(63.94, 77.33), _sc(91.00, 63.94), _sc(63.94, 50.00)]
panel_3 = [_sc(63.94, 77.33), _sc(36.33, 63.94), _sc(36.33, 36.61), _sc(63.94, 50.00)]
panel_4 = [_sc(91.00, 63.94), _sc(63.94, 50.00), _sc(63.94, 22.67), _sc(91.00, 36.61)]

# 1. Four isometric ribbon panels in Colors.Green2 and Colors.Green3
polygon(panel_1, style=no_border_fill(Colors.Green2))
polygon(panel_2, style=no_border_fill(Colors.Green2))
polygon(panel_3, style=no_border_fill(Colors.Green3))
polygon(panel_4, style=no_border_fill(Colors.Green3))

# 2. Crisp DARK w=1.9 outlines on all four panels
for p in (panel_1, panel_2, panel_3, panel_4):
    draw_round_polyline(p, width_units=w, color=DARK, closed=True)

save()
