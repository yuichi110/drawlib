# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original IT Service concept icon: steering_committee (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import arc, circle, polygon, rectangle, regularpolygon, star
from drawlib.utils import Icon

# ruff: noqa: E501, F401
# fmt: off
Icon.setup()
w_outer, w_inner = 2.0, 1.6

# Top and side executive members around oval table
for ex, ey, col in ((26, 76, Icon.PASTEL_BLUE_LIGHT), (50, 82, Icon.PASTEL_BLUE), (74, 76, Icon.PASTEL_BLUE_LIGHT)):
    circle((ex, ey), radius=7.0, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_inner))
    b_pts: list[tuple[float, float]] = [(ex - 10, ey - 16), (ex - 7, ey - 8), (ex + 7, ey - 8), (ex + 10, ey - 16)]
    polygon(b_pts, style=Icon.fill_style(col))
    Icon.draw_round_polyline(b_pts, width_units=w_inner, color=Icon.DARK, closed=True)
# Executive Oval Conference Table
rectangle((50, 44), width=76, height=30, style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_outer, shape_r=14.0))
# Strategy document & chart on table
rectangle((42, 44), width=20, height=14, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.5, shape_r=1.5))
circle((64, 44), radius=6.5, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.5))
# Front executive chairs
rectangle((32, 20), width=16, height=8, style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_inner, shape_r=3.0))
rectangle((68, 20), width=16, height=8, style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_inner, shape_r=3.0))
save()
# fmt: on
