# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original IT Service concept icon: prime_contractor (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import arc, circle, polygon, rectangle, regularpolygon, star
from drawlib.utils import Icon

# ruff: noqa: E501, F401
# fmt: off
Icon.setup()
w_outer, w_inner = 2.0, 1.6

# Connector lines from Prime Hub to Sub-vendors
Icon.draw_round_segment((50, 52), (24, 24), width_units=w_outer, color=Icon.DARK)
Icon.draw_round_segment((50, 52), (50, 22), width_units=w_outer, color=Icon.DARK)
Icon.draw_round_segment((50, 52), (76, 24), width_units=w_outer, color=Icon.DARK)
# Prime Contractor Tier-1 Hub Card
rectangle((50, 68), width=60, height=30, style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_outer, shape_r=5.0))
star((33, 68), num_vertex=5, radius_ext=9.5, radius_int=4.5, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_inner))
rectangle((57, 72), width=22, height=5, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.4, shape_r=1.5))
rectangle((54, 63), width=16, height=4.5, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.4, shape_r=1.5))
# 3 Tier-2 Sub-vendor nodes below
for sx, col in ((24, Icon.PASTEL_BLUE_LIGHT), (50, Icon.WHITE), (76, Icon.PASTEL_BLUE_LIGHT)):
    rectangle((sx, 20), width=20, height=18, style=Icon.fill_style(col, border_color=Icon.DARK, border_units=w_outer, shape_r=3.0))
    circle((sx, 20), radius=4.0, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.4))
save()
# fmt: on
