# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI concept icon: ray."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w = 2.0
sq_size = 15.8
spoke_half_w = 2.15
RAY_CYAN = "#3DB4D8"

# Node centers
p_left = (18.4, 50.0)
p_mid = (50.0, 50.0)
p_top = (50.0, 81.6)
p_bot = (50.0, 18.4)
p_right = (81.6, 50.0)


def _spoke_rect(p1: tuple[float, float], p2: tuple[float, float], half_w: float) -> list[tuple[float, float]]:
    """Build a rectangular bar polygon between p1 and p2 with perpendicular half-width half_w."""
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    length = math.hypot(dx, dy)
    nx = -dy / length * half_w
    ny = dx / length * half_w
    return [
        (p1[0] + nx, p1[1] + ny),
        (p2[0] + nx, p2[1] + ny),
        (p2[0] - nx, p2[1] - ny),
        (p1[0] - nx, p1[1] - ny),
    ]


# 1. Outer DARK borders (w = 1.9) for all 3 spoke bars and all 5 squares
for p_start in (p_left, p_top, p_bot):
    bar = _spoke_rect(p_start, p_right, spoke_half_w)
    polygon(bar, style=Icon.no_border_fill(RAY_CYAN))
    Icon.draw_round_polyline(bar, width_units=w, color=Icon.DARK, closed=True)

sq_style = Icon.fill_style(RAY_CYAN, border_color=Icon.DARK, border_units=w, shape_r=1.6)
for pos in (p_left, p_mid, p_top, p_bot, p_right):
    rectangle(pos, width=sq_size, height=sq_size, style=sq_style)

# 2. Inset borderless fills so spoke bars and squares merge seamlessly with no internal seams
inner_spoke_half_w = spoke_half_w - w / 2.0
for p_start in (p_left, p_top, p_bot):
    polygon(_spoke_rect(p_start, p_right, inner_spoke_half_w), style=Icon.no_border_fill(RAY_CYAN))

inner_sq_size = sq_size - w
inner_sq_style = Icon.no_border_fill(RAY_CYAN, shape_r=0.65)
for pos in (p_left, p_mid, p_top, p_bot, p_right):
    rectangle(pos, width=inner_sq_size, height=inner_sq_size, style=inner_sq_style)

save()
