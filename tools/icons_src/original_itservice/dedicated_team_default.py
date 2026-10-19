# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original IT Service concept icon: dedicated_team (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import arc, circle, polygon, rectangle, regularpolygon, star
from drawlib.utils import Icon

# ruff: noqa: E501, F401
# fmt: off
Icon.setup()
w_outer, w_inner = 2.0, 1.6

# Dedicated Squad Circular Ring
circle((50, 50), radius=38.0, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_outer))
# Central Kanban / Sprint Board
rectangle((50, 52), width=32, height=22, style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_outer, shape_r=2.5))
Icon.draw_round_segment((40, 41), (40, 63), width_units=1.5, color=Icon.DARK)
Icon.draw_round_segment((60, 41), (60, 63), width_units=1.5, color=Icon.DARK)
# 3 Dedicated Squad Members around the board
for cx, cy, col in ((50, 80, Icon.PASTEL_BLUE), (24, 30, Icon.PASTEL_GREEN), (76, 30, Icon.PASTEL_BLUE)):
    circle((cx, cy + 5), radius=7.5, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_inner))
    b_pts: list[tuple[float, float]] = [(cx - 11, cy - 11), (cx - 8, cy - 2), (cx + 8, cy - 2), (cx + 11, cy - 11)]
    polygon(b_pts, style=Icon.fill_style(col))
    Icon.draw_round_polyline(b_pts, width_units=w_inner, color=Icon.DARK, closed=True)
save()
# fmt: on
