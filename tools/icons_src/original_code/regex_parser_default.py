# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code concept icon: regex_parser."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

b = 2.0
w_line = 2.0

# Horizontal WHITE text strip
rectangle(
    (50.0, 54.0),
    width=78.0,
    height=28.0,
    style=fill_style(WHITE, border_color=DARK, border_units=b, shape_r=4.0),
)

# DARK text segments on left and right of match box
draw_round_segment((17.0, 58.0), (29.0, 58.0), width_units=w_line, color=DARK)
draw_round_segment((17.0, 50.0), (26.0, 50.0), width_units=w_line, color=DARK)
draw_round_segment((71.0, 58.0), (83.0, 58.0), width_units=w_line, color=DARK)
draw_round_segment((74.0, 50.0), (83.0, 50.0), width_units=w_line, color=DARK)

# Bottom PASTEL_BLUE filter handle + stem
draw_round_segment((50.0, 37.0), (50.0, 31.0), width_units=w_line, color=DARK)
rectangle(
    (50.0, 21.5),
    width=10.0,
    height=19.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=b, shape_r=4.5),
)

# Central PASTEL_GREEN highlighted match box
rectangle(
    (50.0, 54.0),
    width=30.0,
    height=34.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=b, shape_r=4.0),
)

# '.' dot and '*' 6-arm asterisk inside match box
circle((41.5, 48.0), radius=2.3, style=fill_style(DARK))

ax, ay = 54.5, 56.0
r_ast = 6.8
for deg in (90.0, 30.0, 150.0):
    rad = math.radians(deg)
    dx = r_ast * math.cos(rad)
    dy = r_ast * math.sin(rad)
    draw_round_segment((ax - dx, ay - dy), (ax + dx, ay + dy), width_units=w_line, color=DARK)

save()
