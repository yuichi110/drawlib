# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Workspace concept icon: kanban_board."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_segment,
    draw_rounded_corner_block,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w_outer = 2.0
w_inner = 1.6

# 1. Board background (x=12.5..87.5, y=16.0..84.0)
rectangle(
    (50.0, 50.0),
    width=75.0,
    height=68.0,
    style=no_border_fill(WHITE, shape_r=6.0),
)

# 2. Top PASTEL_BLUE header bar (y=70.0..84.0)
draw_rounded_corner_block(
    12.5,
    70.0,
    87.5,
    84.0,
    r=6.0,
    round_tl=True,
    round_tr=True,
    color=PASTEL_BLUE,
)

# 3. Header divider, 2 vertical column dividers, and outer frame border
draw_round_segment((12.5, 70.0), (87.5, 70.0), width_units=w_outer, color=DARK)
for x_div in (37.5, 62.5):
    draw_round_segment((x_div, 16.0), (x_div, 70.0), width_units=w_inner, color=DARK)

rectangle(
    (50.0, 50.0),
    width=75.0,
    height=68.0,
    style=fill_style(Colors.Transparent, border_color=DARK, border_units=w_outer, shape_r=6.0),
)

# 4. Three WHITE column header pills inside top bar
for cx_col in (25.0, 50.0, 75.0):
    rectangle(
        (cx_col, 77.0),
        width=12.0,
        height=4.4,
        style=fill_style(WHITE, border_color=DARK, border_units=w_inner, shape_r=2.2),
    )

# 5. Task cards stacked across the 3 columns
cards = [
    # Column 1 (To Do): 3 cards
    (25.0, 58.0, PASTEL_BLUE_LIGHT),
    (25.0, 42.5, PASTEL_BLUE_LIGHT),
    (25.0, 27.0, PASTEL_BLUE_LIGHT),
    # Column 2 (In Progress): 2 cards
    (50.0, 58.0, PASTEL_GREEN),
    (50.0, 42.5, PASTEL_BLUE_LIGHT),
    # Column 3 (Done): 2 cards
    (75.0, 58.0, PASTEL_GREEN),
    (75.0, 42.5, PASTEL_GREEN),
]
for cx, cy, col in cards:
    rectangle(
        (cx, cy),
        width=17.0,
        height=11.0,
        style=fill_style(col, border_color=DARK, border_units=w_inner, shape_r=2.5),
    )
    draw_round_segment((cx - 4.5, cy), (cx + 4.5, cy), width_units=w_inner, color=DARK)

save()
