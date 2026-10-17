# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility concept icon: underground_conduit."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w_outer = 2.0
w_inner = 1.6

# 1. Underground utility trench / vault chamber (PASTEL_BLUE_LIGHT)
rectangle(
    (50.0, 32.0),
    width=72.0,
    height=32.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_outer, shape_r=5.5),
)

# 2. Vertical manhole access shaft connecting ground surface to vault (WHITE)
rectangle(
    (50.0, 58.0),
    width=26.0,
    height=24.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w_outer, shape_r=2.0),
)

# Access ladder rungs inside the shaft
for rung_y in (63.0, 56.0):
    draw_round_segment((44.5, rung_y), (55.5, rung_y), width_units=w_inner, color=DARK)

# 3. Street ground surface lines on left and right of shaft
draw_round_segment((12.0, 70.0), (37.0, 70.0), width_units=w_outer, color=DARK)
draw_round_segment((63.0, 70.0), (88.0, 70.0), width_units=w_outer, color=DARK)

# Subtle underground earth hatch ticks beneath ground surface
for hx in (16.0, 23.0, 30.0, 70.0, 77.0, 84.0):
    draw_round_segment((hx, 70.0), (hx - 2.5, 65.5), width_units=w_inner, color=DARK)

# 4. Manhole cover rim on top of the shaft (WHITE)
rectangle(
    (50.0, 73.5),
    width=34.0,
    height=7.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w_outer, shape_r=3.0),
)
# Two grip notches on manhole cover
for nx in (44.0, 56.0):
    draw_round_segment((nx - 1.8, 73.5), (nx + 1.8, 73.5), width_units=w_inner, color=DARK)

# 5. Two horizontal underground conduit pipes (PASTEL_BLUE & PASTEL_GREEN)
conduits = [
    (38.0, PASTEL_BLUE),
    (25.5, PASTEL_GREEN),
]
for cy, col in conduits:
    rectangle(
        (50.0, cy),
        width=62.0,
        height=8.2,
        style=fill_style(col, border_color=DARK, border_units=w_outer, shape_r=4.1),
    )
    # Pipe coupling bands on left and right
    for jx in (31.0, 69.0):
        rectangle(
            (jx, cy),
            width=4.6,
            height=9.8,
            style=fill_style(WHITE, border_color=DARK, border_units=w_inner, shape_r=1.5),
        )

save()
