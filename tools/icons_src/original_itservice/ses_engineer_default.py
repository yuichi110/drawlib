# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original IT Service concept icon: ses_engineer (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import arc, circle, polygon, rectangle, regularpolygon, star
from drawlib.utils import Icon

# ruff: noqa: E501, F401
# fmt: off
Icon.setup()
w_outer, w_inner = 2.0, 1.6

# Engineer avatar on left/center
circle((36, 70), radius=12.5, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_outer))
body_pts: list[tuple[float, float]] = [(12, 24), (18, 52), (54, 52), (60, 24)]
polygon(body_pts, style=Icon.fill_style(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(body_pts, width_units=w_outer, color=Icon.DARK, closed=True)
# Lanyard straps around neck
Icon.draw_round_segment((29, 52), (36, 36), width_units=2.0, color=Icon.DARK)
Icon.draw_round_segment((43, 52), (36, 36), width_units=2.0, color=Icon.DARK)
# Prominent Contractor ID Badge on right
rectangle((72, 48), width=28, height=38, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer, shape_r=3.5))
rectangle((72, 65), width=10, height=5, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.4, shape_r=1.5))
circle((72, 53), radius=5.5, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.5))
Icon.draw_round_segment((63, 40), (81, 40), width_units=1.8, color=Icon.DARK)
Icon.draw_round_segment((65, 34), (79, 34), width_units=1.8, color=Icon.DARK)
save()
# fmt: on
