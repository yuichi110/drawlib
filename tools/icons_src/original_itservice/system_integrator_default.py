# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original IT Service concept icon: system_integrator (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import arc, circle, polygon, rectangle, regularpolygon, star
from drawlib.utils import Icon

# ruff: noqa: E501, F401
# fmt: off
Icon.setup()
w_outer, w_inner = 2.0, 1.6

# Left module block with interlocking tab
rectangle((31, 56), width=32, height=32, style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_outer, shape_r=4.0))
circle((47, 56), radius=7.5, style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_outer))
# Right module block interlocking
rectangle((69, 44), width=32, height=32, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer, shape_r=4.0))
circle((53, 44), radius=7.5, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer))
# Integration gear badge at top right
circle((72, 78), radius=11.0, style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_outer))
circle((72, 78), radius=4.5, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.5))
# Nodes inside blocks
circle((28, 56), radius=4.5, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.5))
circle((72, 44), radius=4.5, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.5))
Icon.draw_round_segment((20, 26), (40, 26), width_units=w_outer, color=Icon.DARK)
Icon.draw_round_polyline([(35, 31), (41, 26), (35, 21)], width_units=w_outer, color=Icon.DARK)
save()
# fmt: on
