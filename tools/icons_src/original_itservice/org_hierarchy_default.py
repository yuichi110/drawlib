# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original IT Service concept icon: org_hierarchy (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import arc, circle, polygon, rectangle, regularpolygon, star
from drawlib.utils import Icon

# ruff: noqa: E501, F401
# fmt: off
Icon.setup()
w_outer, w_inner = 2.0, 1.6

# Hierarchy connector lines
Icon.draw_round_segment((50, 74), (50, 62), width_units=2.2, color=Icon.DARK)
Icon.draw_round_segment((26, 62), (74, 62), width_units=2.2, color=Icon.DARK)
Icon.draw_round_segment((26, 62), (26, 52), width_units=2.2, color=Icon.DARK)
Icon.draw_round_segment((74, 62), (74, 52), width_units=2.2, color=Icon.DARK)
Icon.draw_round_segment((26, 40), (26, 32), width_units=2.0, color=Icon.DARK)
Icon.draw_round_segment((15, 32), (37, 32), width_units=2.0, color=Icon.DARK)
Icon.draw_round_segment((15, 32), (15, 24), width_units=2.0, color=Icon.DARK)
Icon.draw_round_segment((37, 32), (37, 24), width_units=2.0, color=Icon.DARK)
Icon.draw_round_segment((74, 40), (74, 32), width_units=2.0, color=Icon.DARK)
Icon.draw_round_segment((63, 32), (85, 32), width_units=2.0, color=Icon.DARK)
Icon.draw_round_segment((63, 32), (63, 24), width_units=2.0, color=Icon.DARK)
Icon.draw_round_segment((85, 32), (85, 24), width_units=2.0, color=Icon.DARK)
# Level 1 Executive / Client Node
rectangle((50, 81), width=30, height=14, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer, shape_r=3.0))
# Level 2 Prime / PM Nodes
rectangle((26, 46), width=26, height=13, style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_outer, shape_r=2.5))
rectangle((74, 46), width=26, height=13, style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_outer, shape_r=2.5))
# Level 3 Delivery Squad Nodes
for bx in (15, 37, 63, 85):
    rectangle((bx, 18), width=16, height=12, style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_inner, shape_r=2.0))
save()
# fmt: on
