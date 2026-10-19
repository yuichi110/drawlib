# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code concept icon: json_schema."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

b = 2.0
w_line = 2.0

# Rounded WHITE schema card
rectangle(
    (50.0, 50.0),
    width=74.0,
    height=66.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=b, shape_r=6.0),
)

# Left PASTEL_BLUE curly brace '{'
left_brace = [
    (32.5, 71.0),
    (32.5, 66.0),
    (28.0, 66.0),
    (28.0, 53.5),
    (24.5, 50.0),
    (28.0, 46.5),
    (28.0, 34.0),
    (32.5, 34.0),
    (32.5, 29.0),
    (23.0, 29.0),
    (23.0, 44.5),
    (19.0, 50.0),
    (23.0, 55.5),
    (23.0, 71.0),
]
polygon(left_brace, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(left_brace, width_units=b, color=Icon.DARK, closed=True)

# Right PASTEL_BLUE curly brace '}' (mirrored across x=50)
right_brace = [(100.0 - x, y) for x, y in left_brace]
polygon(right_brace, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(right_brace, width_units=b, color=Icon.DARK, closed=True)

# 2 PASTEL_GREEN key dots and DARK value bars in the middle
for y_row, x_end in ((57.0, 61.5), (43.0, 58.0)):
    circle(
        (40.5, y_row),
        radius=3.5,
        style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=b),
    )
    Icon.draw_round_segment((48.5, y_row), (x_end, y_row), width_units=w_line, color=Icon.DARK)

save()
