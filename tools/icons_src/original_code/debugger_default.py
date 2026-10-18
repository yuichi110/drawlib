# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code concept icon: debugger."""

from drawlib.canvas import save
from drawlib.shapes import circle, ellipse, rectangle
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

cx, cy = 46.0, 52.0

# Diagonal PASTEL_BLUE magnifying handle extending to (82, 16)
rectangle(
    (72.5, 25.5),
    width=27.0,
    height=9.5,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=b, shape_r=3.5, angle=-45.0),
)

# Outer PASTEL_BLUE magnifying bezel and inner WHITE lens
circle(
    (cx, cy),
    radius=31.5,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=b),
)
circle(
    (cx, cy),
    radius=26.0,
    style=fill_style(WHITE, border_color=DARK, border_units=b),
)

# 3 pairs of DARK bug legs
leg_pairs = [
    ((35.5, 58.0), (27.5, 62.0), (56.5, 58.0), (64.5, 62.0)),
    ((33.0, 50.0), (25.0, 50.0), (59.0, 50.0), (67.0, 50.0)),
    ((35.5, 42.0), (27.5, 38.0), (56.5, 42.0), (64.5, 38.0)),
]
for l_in, l_out, r_in, r_out in leg_pairs:
    draw_round_segment(l_in, l_out, width_units=w_line, color=DARK)
    draw_round_segment(r_in, r_out, width_units=w_line, color=DARK)

# Small PASTEL_BLUE bug head
circle(
    (cx, 68.5),
    radius=5.8,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=b),
)

# Central PASTEL_GREEN oval bug body + wing split line
ellipse(
    (cx, 50.5),
    width=25.0,
    height=31.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=b),
)
draw_round_segment((cx, 35.5), (cx, 65.5), width_units=b, color=DARK)

save()
