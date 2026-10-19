# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original IT Service concept icon: client_enterprise (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import arc, circle, polygon, rectangle, regularpolygon, star
from drawlib.utils import Icon

# ruff: noqa: E501, F401
# fmt: off
Icon.setup()
w_outer, w_inner = 2.0, 1.6

# Side wing & Main HQ tower
rectangle((73, 40), width=22, height=44, style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_outer, shape_r=3.0))
rectangle((43, 46), width=42, height=58, style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_outer, shape_r=3.5))
rectangle((50, 14), width=76, height=6, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_outer, shape_r=2.0))
# Entrance door
rectangle((43, 23), width=12, height=12, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_inner, shape_r=1.5))
# Window grid on HQ tower
for wy in (38, 50, 62):
    for wx in (31, 43, 55):
        rectangle((wx, wy), width=6.5, height=6.5, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.4, shape_r=1.0))
for wy in (30, 42, 52):
    rectangle((73, wy), width=8.0, height=6.0, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.4, shape_r=1.0))
# Crown / Flagship client badge on top of HQ
crown_pts: list[tuple[float, float]] = [(27, 75), (31, 89), (39, 81), (43, 91), (47, 81), (55, 89), (59, 75)]
polygon(crown_pts, style=Icon.fill_style(Icon.PASTEL_GREEN))
Icon.draw_round_polyline(crown_pts, width_units=w_outer, color=Icon.DARK, closed=True)
save()
# fmt: on
