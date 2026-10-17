# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility concept icon: public_building."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    WHITE,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w_outer = 2.0
w_inner = 1.6

# 1. Recessed back wall behind the classical pillars (PASTEL_BLUE_LIGHT)
rectangle(
    (50.0, 43.0),
    width=54.0,
    height=34.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_inner, shape_r=1.0),
)

# 2. Stepped classical base foundation (PASTEL_BLUE & PASTEL_BLUE_LIGHT)
rectangle(
    (50.0, 17.0),
    width=76.0,
    height=6.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w_outer, shape_r=1.8),
)
rectangle(
    (50.0, 23.0),
    width=66.0,
    height=6.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_outer, shape_r=1.8),
)

# 3. Four classical columns with capital and base pads (WHITE)
col_xs = [26.5, 42.2, 57.8, 73.5]
for cx in col_xs:
    # Column shaft
    rectangle(
        (cx, 43.0),
        width=7.2,
        height=34.0,
        style=fill_style(WHITE, border_color=DARK, border_units=w_inner, shape_r=0.8),
    )
    # Column base pad
    rectangle(
        (cx, 27.8),
        width=10.4,
        height=3.6,
        style=fill_style(WHITE, border_color=DARK, border_units=w_inner, shape_r=1.0),
    )
    # Column capital pad
    rectangle(
        (cx, 58.2),
        width=10.4,
        height=3.6,
        style=fill_style(WHITE, border_color=DARK, border_units=w_inner, shape_r=1.0),
    )

# 4. Horizontal entablature / architrave beam above columns (WHITE)
rectangle(
    (50.0, 63.0),
    width=68.0,
    height=6.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w_outer, shape_r=1.5),
)

# 5. Triangular pediment roof (PASTEL_BLUE) with central WHITE medallion
pediment_pts = [
    (13.0, 66.0),
    (87.0, 66.0),
    (50.0, 86.0),
]
polygon(pediment_pts, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(pediment_pts, width_units=w_outer, color=DARK, closed=True)

circle(
    (50.0, 73.5),
    radius=4.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w_inner),
)

save()
