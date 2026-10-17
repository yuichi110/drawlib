# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Client concept icon: pos_terminal."""

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Top printed paper receipt with serrated tear edge
receipt_pts = [
    (31.5, 68.0),
    (31.5, 85.0),
    (36.0, 82.0),
    (40.5, 85.0),
    (45.0, 82.0),
    (49.5, 85.0),
    (54.0, 82.0),
    (58.5, 85.0),
    (58.5, 68.0),
]
polygon(receipt_pts, style=fill_style(WHITE))
draw_round_polyline(receipt_pts, width_units=2.2, color=DARK, closed=True)
draw_round_segment((36.5, 76.5), (53.5, 76.5), width_units=1.8, color=DARK)

# Countertop POS terminal body
rectangle(
    (45.0, 42.5),
    width=42.0,
    height=55.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=6.5),
)

# Receipt printer slot and WHITE display screen
draw_round_segment((30.0, 68.0), (60.0, 68.0), width_units=2.4, color=DARK)
rectangle(
    (45.0, 54.5),
    width=31.0,
    height=17.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0, shape_r=2.5),
)

# PIN keypad buttons (2 rows)
for ky in (37.5, 29.5):
    for kx in (35.0, 45.0, 55.0):
        rectangle(
            (kx, ky),
            width=6.8,
            height=4.8,
            style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=1.8, shape_r=1.5),
        )

# Swiped / tapped PASTEL_GREEN payment card on the right
rectangle(
    (71.5, 42.5),
    width=20.0,
    height=30.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w, shape_r=3.5),
)
rectangle(
    (68.5, 49.0),
    width=6.5,
    height=5.5,
    style=fill_style(WHITE, border_color=DARK, border_units=1.8, shape_r=1.2),
)
draw_round_segment((66.5, 36.0), (76.5, 36.0), width_units=2.0, color=DARK)

save()
