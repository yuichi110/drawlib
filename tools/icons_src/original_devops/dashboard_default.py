# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: dashboard."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_segment,
    draw_rounded_corner_block,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Wide observability dashboard base fill
rectangle(
    (50.0, 50.0),
    width=74.0,
    height=58.0,
    style=fill_style(WHITE, shape_r=7.0),
)

# Top header bar
draw_rounded_corner_block(
    13.0,
    65.0,
    87.0,
    79.0,
    r=7.0,
    round_tl=True,
    round_tr=True,
    color=PASTEL_BLUE,
)

# Outer frame border and header divider
rectangle(
    (50.0, 50.0),
    width=74.0,
    height=58.0,
    style=fill_style(Colors.Transparent, border_color=DARK, border_units=w, shape_r=7.0),
)
draw_round_segment((13.0, 65.0), (87.0, 65.0), width_units=w, color=DARK)

# Header dots
for x_dot, col in ((22.0, PASTEL_GREEN), (30.5, WHITE)):
    circle(
        (x_dot, 72.0),
        radius=2.5,
        style=fill_style(col, border_color=DARK, border_units=1.8),
    )

# Bottom-left gauge widget
circle(
    (32.0, 42.5),
    radius=12.5,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.4),
)
draw_round_segment((32.0, 42.5), (39.5, 50.0), width_units=2.4, color=DARK)
circle(
    (32.0, 42.5),
    radius=3.0,
    style=fill_style(WHITE, border_color=DARK, border_units=1.8),
)

# Bottom-right 3 rising metric bars
bars = [
    (54.0, 11.0, PASTEL_BLUE_LIGHT),
    (64.0, 18.0, PASTEL_BLUE),
    (74.0, 25.0, PASTEL_GREEN),
]
for bx, bh, bcol in bars:
    rectangle(
        (bx, 30.0 + bh / 2.0),
        width=6.5,
        height=bh,
        style=fill_style(bcol, border_color=DARK, border_units=2.2, shape_r=1.5),
    )

save()
