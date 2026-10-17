# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Workspace concept icon: project_plan."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle, rhombus
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

# 1. Gantt card background (x=12.5..87.5, y=16.0..84.0)
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

# 3. Header divider and outer frame border
draw_round_segment((12.5, 70.0), (87.5, 70.0), width_units=w_outer, color=DARK)
rectangle(
    (50.0, 50.0),
    width=75.0,
    height=68.0,
    style=fill_style(Colors.Transparent, border_color=DARK, border_units=w_outer, shape_r=6.0),
)

# 4. Header dots on left
for x_dot in (21.0, 29.0):
    circle(
        (x_dot, 77.0),
        radius=2.2,
        style=fill_style(WHITE, border_color=DARK, border_units=w_inner),
    )

# 5. Vertical milestone line at x=73.0 + top diamond marker
draw_round_segment((73.0, 16.0), (73.0, 70.0), width_units=w_inner, color=DARK)
rhombus(
    (73.0, 56.5),
    width=9.0,
    height=9.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w_inner),
)

# 6. Three staggered horizontal timeline bars
timeline_bars = [
    # (cx, cy, width, fill_color)
    (32.5, 56.5, 25.0, PASTEL_BLUE),
    (46.5, 42.5, 27.0, PASTEL_GREEN),
    (59.0, 28.5, 28.0, PASTEL_BLUE_LIGHT),
]
for cx, cy, bw, col in timeline_bars:
    rectangle(
        (cx, cy),
        width=bw,
        height=8.8,
        style=fill_style(col, border_color=DARK, border_units=w_inner, shape_r=4.4),
    )

save()
