# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Business concept icon: supply_chain."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle, regularpolygon
from drawlib.utils import Icon

Icon.setup()
w_outer, w_inner = 2.0, 1.6

# 1. Three supply chain links (triangle layout)
p_top = (50.0, 74.0)
p_bl = (24.0, 28.0)
p_br = (76.0, 28.0)

Icon.draw_round_segment(p_top, p_bl, width_units=w_outer, color=Icon.DARK)
Icon.draw_round_segment(p_bl, p_br, width_units=w_outer, color=Icon.DARK)
Icon.draw_round_segment(p_br, p_top, width_units=w_outer, color=Icon.DARK)

# 2. Top node: Factory/Source hexagon (PASTEL_BLUE)
regularpolygon(
    p_top,
    radius=14.5,
    num_vertex=6,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_outer, shape_r=2.0, angle=30.0),
)
circle(p_top, radius=5.0, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_inner))

# 3. Bottom-left node: Warehouse box (PASTEL_BLUE_LIGHT)
rectangle(
    p_bl,
    width=25.0,
    height=23.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_outer, shape_r=3.0),
)
Icon.draw_round_segment((11.5, 28.0), (36.5, 28.0), width_units=w_inner, color=Icon.DARK)

# 4. Bottom-right node: Destination circle (PASTEL_GREEN)
circle(p_br, radius=13.5, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer))
Icon.draw_round_polyline([(70.5, 28.0), (74.5, 24.0), (81.5, 32.5)], width_units=w_outer, color=Icon.DARK)
save()
