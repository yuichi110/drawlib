# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original IT Service concept icon: support_operator (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import arc, circle, polygon, rectangle, regularpolygon, star
from drawlib.utils import Icon

# ruff: noqa: E501, F401
# fmt: off
Icon.setup()
w_outer, w_inner = 2.0, 1.6

# Support Operator Avatar
circle((42, 54), radius=14.0, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_outer))
body_pts: list[tuple[float, float]] = [(18, 16), (24, 36), (60, 36), (66, 16)]
polygon(body_pts, style=Icon.fill_style(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(body_pts, width_units=w_outer, color=Icon.DARK, closed=True)
# Headset & Microphone
arc((42, 55), width=32, height=30, angle_start=0, angle_end=180, style=Icon.stroke_style(width_units=2.6))
rectangle((25, 53), width=5.5, height=11, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_inner, shape_r=2.0))
rectangle((59, 53), width=5.5, height=11, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_inner, shape_r=2.0))
Icon.draw_round_polyline([(59, 49), (51, 44), (43, 44)], width_units=2.0, color=Icon.DARK)
# Speech Bubble with Checkmark at top-right
rectangle((74, 78), width=30, height=20, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer, shape_r=4.0))
Icon.draw_round_polyline([(67, 78), (72, 73), (82, 83)], width_units=2.4, color=Icon.DARK)
save()
# fmt: on
