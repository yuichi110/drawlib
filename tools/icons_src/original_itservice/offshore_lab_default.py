# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original IT Service concept icon: offshore_lab (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import arc, circle, polygon, rectangle, regularpolygon, star
from drawlib.utils import Icon

# ruff: noqa: E501, F401
# fmt: off
Icon.setup()
w_outer, w_inner = 2.0, 1.6

# Globe on left
circle((30, 56), radius=20.0, style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_outer))
arc((30, 56), width=20, height=39, angle_start=0, angle_end=360, style=Icon.stroke_style(width_units=1.5))
Icon.draw_round_segment((10, 56), (50, 56), width_units=1.5, color=Icon.DARK)
Icon.draw_round_segment((30, 36), (30, 76), width_units=1.5, color=Icon.DARK)
# Remote Offshore Lab Building on right
rectangle((74, 42), width=30, height=44, style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_outer, shape_r=3.0))
for wy in (32, 44, 54):
    for wx in (67, 81):
        rectangle((wx, wy), width=7, height=6, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.4, shape_r=1.0))
# Global delivery bridge arc connecting globe and lab
Icon.draw_round_polyline([(34, 78), (54, 90), (74, 70)], width_units=2.4, color=Icon.DARK)
circle((54, 86), radius=5.0, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_inner))
save()
# fmt: on
