# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Business concept icon: order_management."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Icon

Icon.setup()
w_outer, w_inner = 2.0, 1.6

# 1. Clipboard board (PASTEL_BLUE) and paper (WHITE)
rectangle(
    (44.0, 49.0),
    width=60.0,
    height=68.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_outer, shape_r=6.0),
)
rectangle(
    (44.0, 47.0),
    width=48.0,
    height=54.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_inner, shape_r=3.0),
)
rectangle(
    (44.0, 82.0),
    width=24.0,
    height=9.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_outer, shape_r=3.0),
)

# 2. Order checklist items
for y_row in (62.0, 48.0, 34.0):
    circle(
        (29.0, y_row),
        radius=3.0,
        style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_inner),
    )
    Icon.draw_round_segment((37.0, y_row), (58.0, y_row), width_units=w_inner, color=Icon.DARK)

# 3. PASTEL_GREEN package box badge at bottom-right
rectangle(
    (74.0, 26.0),
    width=26.0,
    height=24.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer, shape_r=3.0),
)
Icon.draw_round_segment((61.0, 26.0), (87.0, 26.0), width_units=w_inner, color=Icon.DARK)
Icon.draw_round_segment((74.0, 26.0), (74.0, 38.0), width_units=w_inner, color=Icon.DARK)
save()
