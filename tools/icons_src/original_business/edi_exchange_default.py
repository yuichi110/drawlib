# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Business concept icon: edi_exchange."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Icon

Icon.setup()
w_outer, w_inner = 2.0, 1.6

# 1. Left document (PASTEL_BLUE_LIGHT)
rectangle(
    (26.0, 62.0),
    width=28.0,
    height=36.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_outer, shape_r=3.5),
)
Icon.draw_round_segment((18.0, 68.0), (34.0, 68.0), width_units=w_inner, color=Icon.DARK)
Icon.draw_round_segment((18.0, 58.0), (34.0, 58.0), width_units=w_inner, color=Icon.DARK)

# 2. Right document (WHITE)
rectangle(
    (74.0, 38.0),
    width=28.0,
    height=36.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_outer, shape_r=3.5),
)
Icon.draw_round_segment((66.0, 44.0), (82.0, 44.0), width_units=w_inner, color=Icon.DARK)
Icon.draw_round_segment((66.0, 34.0), (82.0, 34.0), width_units=w_inner, color=Icon.DARK)

# 3. Central PASTEL_GREEN exchange hub and routing lines
Icon.draw_round_polyline([(40.0, 66.0), (68.0, 66.0), (68.0, 56.0)], width_units=w_outer, color=Icon.DARK)
Icon.draw_round_polyline([(60.0, 34.0), (32.0, 34.0), (32.0, 44.0)], width_units=w_outer, color=Icon.DARK)
circle(
    (50.0, 50.0), radius=13.5, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer)
)
Icon.draw_round_segment((43.0, 53.0), (57.0, 53.0), width_units=w_inner, color=Icon.DARK)
Icon.draw_round_segment((43.0, 47.0), (57.0, 47.0), width_units=w_inner, color=Icon.DARK)
save()
