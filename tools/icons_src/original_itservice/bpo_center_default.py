# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original IT Service concept icon: bpo_center (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import arc, circle, polygon, rectangle, regularpolygon, star
from drawlib.utils import Icon

# ruff: noqa: E501, F401
# fmt: off
Icon.setup()
w_outer, w_inner = 2.0, 1.6

# Operator avatar in center-left
circle((34, 62), radius=13.0, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_outer))
body_pts: list[tuple[float, float]] = [(14, 22), (20, 45), (48, 45), (54, 22)]
polygon(body_pts, style=Icon.fill_style(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(body_pts, width_units=w_outer, color=Icon.DARK, closed=True)
# Headset arc & earpieces + mic boom
arc((34, 63), width=30, height=28, angle_start=0, angle_end=180, style=Icon.stroke_style(width_units=2.6))
rectangle((18, 61), width=5, height=10, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_inner, shape_r=2.0))
rectangle((50, 61), width=5, height=10, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_inner, shape_r=2.0))
Icon.draw_round_polyline([(50, 57), (44, 52), (36, 52)], width_units=2.0, color=Icon.DARK)
# Automated process cards on right
for cy, col in ((72, Icon.PASTEL_BLUE_LIGHT), (50, Icon.WHITE), (28, Icon.PASTEL_GREEN)):
    rectangle((75, cy), width=26, height=14, style=Icon.fill_style(col, border_color=Icon.DARK, border_units=w_outer, shape_r=2.5))
    Icon.draw_round_segment((67, cy), (83, cy), width_units=1.6, color=Icon.DARK)
save()
# fmt: on
