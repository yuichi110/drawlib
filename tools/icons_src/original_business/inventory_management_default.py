# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Business concept icon: inventory_management."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Icon

Icon.setup()
w_outer, w_inner = 2.0, 1.6

# 1. Warehouse rack uprights and shelves
for x_up in (16.0, 74.0):
    Icon.draw_round_segment((x_up, 16.0), (x_up, 86.0), width_units=w_outer, color=Icon.DARK)
for y_sh in (24.0, 52.0, 80.0):
    Icon.draw_round_segment((16.0, y_sh), (74.0, y_sh), width_units=w_outer, color=Icon.DARK)

# 2. Boxes on upper shelf
rectangle(
    (32.0, 63.0),
    width=20.0,
    height=20.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_outer, shape_r=2.0),
)
rectangle(
    (57.0, 61.0),
    width=20.0,
    height=16.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_outer, shape_r=2.0),
)

# 3. Boxes on lower shelf
rectangle(
    (30.0, 35.0),
    width=20.0,
    height=20.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_outer, shape_r=2.0),
)
rectangle(
    (54.0, 35.0),
    width=18.0,
    height=20.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_outer, shape_r=2.0),
)

# 4. PASTEL_GREEN check badge at bottom-right
circle(
    (75.0, 27.0), radius=14.0, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer)
)
Icon.draw_round_polyline([(69.0, 27.0), (73.5, 22.5), (81.5, 32.0)], width_units=w_outer, color=Icon.DARK)
save()
