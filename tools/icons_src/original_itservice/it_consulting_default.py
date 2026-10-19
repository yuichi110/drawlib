# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original IT Service concept icon: it_consulting (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import arc, circle, polygon, rectangle, regularpolygon, star
from drawlib.utils import Icon

# ruff: noqa: E501, F401
# fmt: off
Icon.setup()
w_outer, w_inner = 2.0, 1.6

# Strategy whiteboard on right
rectangle((62, 58), width=48, height=38, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_outer, shape_r=3.5))
rectangle((62, 73), width=48, height=8, style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_outer, shape_r=2.0))
# Rising strategy trend line on board
Icon.draw_round_polyline([(44, 46), (55, 55), (64, 50), (78, 64)], width_units=w_outer, color=Icon.DARK)
circle((78, 64), radius=3.2, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.4))
# Lightbulb idea badge at top-left
circle((24, 78), radius=10.5, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer))
rectangle((24, 65), width=7, height=4, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.4, shape_r=1.0))
# Consultant avatar on bottom-left
circle((28, 42), radius=9.5, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_outer))
body_pts: list[tuple[float, float]] = [(12, 14), (16, 30), (40, 30), (44, 14)]
polygon(body_pts, style=Icon.fill_style(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(body_pts, width_units=w_outer, color=Icon.DARK, closed=True)
save()
# fmt: on
