# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: web_browser."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_segment,
    draw_rounded_corner_block,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Outer browser base fill
rectangle(
    (50.0, 50.0),
    width=76.0,
    height=64.0,
    style=fill_style(WHITE, shape_r=7.0),
)

# Top browser header fill
draw_rounded_corner_block(
    12.0,
    64.0,
    88.0,
    82.0,
    r=7.0,
    round_tl=True,
    round_tr=True,
    color=PASTEL_BLUE,
)

# Outer frame border and header divider
rectangle(
    (50.0, 50.0),
    width=76.0,
    height=64.0,
    style=fill_style(Colors.Transparent, border_color=DARK, border_units=w, shape_r=7.0),
)
draw_round_segment((12.0, 64.0), (88.0, 64.0), width_units=w, color=DARK)

# Window control dots
for x_dot, col in ((22.0, PASTEL_GREEN), (31.0, WHITE), (40.0, WHITE)):
    circle(
        (x_dot, 73.0),
        radius=2.8,
        style=fill_style(col, border_color=DARK, border_units=1.8),
    )

# Content area hero block and text lines
rectangle(
    (36.0, 41.0),
    width=26.0,
    height=26.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.2, shape_r=3.5),
)
draw_round_segment((57.0, 48.0), (77.0, 48.0), width_units=2.5, color=DARK)
draw_round_segment((57.0, 34.0), (72.0, 34.0), width_units=2.5, color=DARK)

save()
