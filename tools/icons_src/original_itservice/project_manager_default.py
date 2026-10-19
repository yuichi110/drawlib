# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original IT Service concept icon: project_manager (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import arc, circle, polygon, rectangle, regularpolygon, star
from drawlib.utils import Icon

# ruff: noqa: E501, F401
# fmt: off
Icon.setup()
w_outer, w_inner = 2.0, 1.6

# PM Avatar on left
circle((30, 68), radius=11.5, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_outer))
body_pts: list[tuple[float, float]] = [(12, 28), (17, 52), (43, 52), (48, 28)]
polygon(body_pts, style=Icon.fill_style(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(body_pts, width_units=w_outer, color=Icon.DARK, closed=True)
tie_pts: list[tuple[float, float]] = [(30, 50), (27, 36), (30, 32), (33, 36)]
polygon(tie_pts, style=Icon.fill_style(Icon.PASTEL_GREEN))
Icon.draw_round_polyline(tie_pts, width_units=1.4, color=Icon.DARK, closed=True)
# Milestone Flag & Project Timeline on right
Icon.draw_round_segment((62, 22), (62, 84), width_units=2.6, color=Icon.DARK)
flag_pts: list[tuple[float, float]] = [(62, 84), (88, 74), (62, 64)]
polygon(flag_pts, style=Icon.fill_style(Icon.PASTEL_GREEN))
Icon.draw_round_polyline(flag_pts, width_units=w_outer, color=Icon.DARK, closed=True)
rectangle((50, 18), width=76, height=7, style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_outer, shape_r=3.0))
for tx, col in ((24, Icon.WHITE), (50, Icon.PASTEL_GREEN), (76, Icon.WHITE)):
    circle((tx, 18), radius=4.5, style=Icon.fill_style(col, border_color=Icon.DARK, border_units=w_inner))
save()
# fmt: on
