# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original IT Service concept icon: architect_lead (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import arc, circle, polygon, rectangle, regularpolygon, star
from drawlib.utils import Icon

# ruff: noqa: E501, F401
# fmt: off
Icon.setup()
w_outer, w_inner = 2.0, 1.6

# System Architecture Topology Diagram at top
Icon.draw_round_segment((30, 78), (50, 84), width_units=2.0, color=Icon.DARK)
Icon.draw_round_segment((70, 78), (50, 84), width_units=2.0, color=Icon.DARK)
Icon.draw_round_segment((30, 78), (70, 78), width_units=1.8, color=Icon.DARK)
for nx, ny, col in ((30, 78, Icon.PASTEL_BLUE_LIGHT), (50, 84, Icon.PASTEL_GREEN), (70, 78, Icon.PASTEL_BLUE_LIGHT)):
    rectangle((nx, ny), width=14, height=10, style=Icon.fill_style(col, border_color=Icon.DARK, border_units=w_inner, shape_r=2.0))
# Architect Avatar on bottom-left
circle((30, 50), radius=10.5, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_outer))
body_pts: list[tuple[float, float]] = [(12, 16), (17, 36), (43, 36), (48, 16)]
polygon(body_pts, style=Icon.fill_style(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(body_pts, width_units=w_outer, color=Icon.DARK, closed=True)
# Blueprint Grid & Set Square on bottom-right
rectangle((68, 34), width=34, height=28, style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_outer, shape_r=2.5))
tri_pts: list[tuple[float, float]] = [(56, 24), (80, 24), (56, 44)]
polygon(tri_pts, style=Icon.fill_style(Icon.PASTEL_GREEN))
Icon.draw_round_polyline(tri_pts, width_units=w_inner, color=Icon.DARK, closed=True)
save()
# fmt: on
