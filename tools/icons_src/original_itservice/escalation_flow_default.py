# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original IT Service concept icon: escalation_flow (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import arc, circle, polygon, rectangle, regularpolygon, star
from drawlib.utils import Icon

# ruff: noqa: E501, F401
# fmt: off
Icon.setup()
w_outer, w_inner = 2.0, 1.6

# 3 Stepped Escalation Tiers (L1 -> L2 -> L3)
rectangle((24, 24), width=24, height=18, style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_outer, shape_r=2.5))
rectangle((50, 38), width=24, height=28, style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_outer, shape_r=2.5))
rectangle((76, 54), width=24, height=42, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer, shape_r=2.5))
# Upward Escalation Arrow across tiers
Icon.draw_round_polyline([(18, 42), (44, 62), (66, 82)], width_units=2.8, color=Icon.DARK)
Icon.draw_round_polyline([(56, 82), (66, 82), (66, 72)], width_units=2.8, color=Icon.DARK)
# Alert Beacon at L3 top right
circle((76, 85), radius=5.5, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_inner))
save()
# fmt: on
