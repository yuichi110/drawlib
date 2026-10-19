# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original IT Service concept icon: raci_matrix (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import arc, circle, polygon, rectangle, regularpolygon, star
from drawlib.utils import Icon

# ruff: noqa: E501, F401
# fmt: off
Icon.setup()
w_outer, w_inner = 2.0, 1.6

# Matrix Table Frame
rectangle((50, 50), width=78, height=76, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_outer, shape_r=4.5))
rectangle((50, 80), width=78, height=16, style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_outer, shape_r=3.5))
rectangle((22, 42), width=22, height=60, style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_outer, shape_r=2.0))
# Grid lines
for gy in (32, 52):
    Icon.draw_round_segment((11, gy), (89, gy), width_units=1.6, color=Icon.DARK)
for gx in (52, 70):
    Icon.draw_round_segment((gx, 12), (gx, 88), width_units=1.6, color=Icon.DARK)
# R, A, C, I colored badges in matrix cells
circle((42, 62), radius=5.5, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.5))
circle((61, 62), radius=5.5, style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.5))
circle((80, 62), radius=5.5, style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=1.5))
circle((42, 42), radius=5.5, style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=1.5))
circle((61, 42), radius=5.5, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.5))
circle((80, 42), radius=5.5, style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.5))
circle((42, 22), radius=5.5, style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.5))
circle((61, 22), radius=5.5, style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=1.5))
circle((80, 22), radius=5.5, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.5))
save()
# fmt: on
