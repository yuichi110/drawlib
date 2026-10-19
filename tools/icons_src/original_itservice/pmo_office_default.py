# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original IT Service concept icon: pmo_office (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import arc, circle, polygon, rectangle, regularpolygon, star
from drawlib.utils import Icon

# ruff: noqa: E501, F401
# fmt: off
Icon.setup()
w_outer, w_inner = 2.0, 1.6

# Project portfolio dashboard board
rectangle((50, 48), width=74, height=68, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_outer, shape_r=5.0))
rectangle((50, 75), width=74, height=14, style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_outer, shape_r=4.0))
for cx in (22, 30, 38):
    circle((cx, 75), radius=2.3, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.3))
# Gantt chart bars inside dashboard
rectangle((34, 56), width=26, height=7, style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_inner, shape_r=2.0))
rectangle((52, 42), width=30, height=7, style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_inner, shape_r=2.0))
rectangle((64, 28), width=24, height=7, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_inner, shape_r=2.0))
# Milestone diamond & vertical target line
Icon.draw_round_segment((74, 20), (74, 64), width_units=1.8, color=Icon.DARK)
regularpolygon((74, 56), radius=5.5, num_vertex=4, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_inner))
save()
# fmt: on
