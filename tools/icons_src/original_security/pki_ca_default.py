# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security concept icon: pki_ca (PKI & Certificate Authority)."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w_shape = 1.8
w_line = 2.7

# 1. WHITE certificate card
rectangle(
    (48.0, 56.0),
    width=68.0,
    height=52.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w_shape, shape_r=6.0),
)

# 2. Horizontal certificate lines on the left
draw_round_segment((24.0, 66.0), (54.0, 66.0), width_units=w_line, color=DARK)
draw_round_segment((24.0, 52.0), (54.0, 52.0), width_units=w_line, color=DARK)

# 3. Bottom-right PASTEL_BLUE ribbon tails
ribbon_pts = [
    (56.0, 38.0),
    (56.0, 16.0),
    (64.0, 22.0),
    (72.0, 16.0),
    (72.0, 38.0),
]
polygon(ribbon_pts, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(ribbon_pts, width_units=w_shape, color=DARK, closed=True)

# 4. PASTEL_GREEN circular medal seal with WHITE inner circle
circle(
    (64.0, 38.0),
    radius=14.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w_shape),
)
circle(
    (64.0, 38.0),
    radius=6.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w_shape),
)

save()
