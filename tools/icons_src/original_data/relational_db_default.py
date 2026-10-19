# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: relational_db."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.utils import Icon

Icon.setup()
w = Icon.ORIG_STROKE
Icon.draw_cylinder_tier(
    40.0, 20.0, 52.0, 56.0, 10.0, body_color=Icon.PASTEL_BLUE, top_color=Icon.PASTEL_BLUE_LIGHT, border_units=w
)
# Relational table overlay on bottom-right
rectangle(
    (64.0, 38.0),
    width=44.0,
    height=36.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=4.0),
)
rectangle(
    (64.0, 50.0),
    width=44.0,
    height=12.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w, shape_r=3.0),
)
for y_line in (32.0, 44.0):
    Icon.draw_round_segment((42.0, y_line), (86.0, y_line), width_units=w, color=Icon.DARK)
for x_line in (56.0, 72.0):
    Icon.draw_round_segment((x_line, 20.0), (x_line, 56.0), width_units=w, color=Icon.DARK)
save()
