# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security concept icon: soc_center."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
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

w_shape = 1.8

# Monitor stand neck & base
rectangle(
    (50.0, 27.0),
    width=12.0,
    height=10.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_shape),
)
rectangle(
    (50.0, 20.0),
    width=36.0,
    height=6.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_shape, shape_r=3.0),
)

# Wide monitor bezel
rectangle(
    (50.0, 56.0),
    width=78.0,
    height=48.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w_shape, shape_r=6.0),
)

# Inner WHITE dual-pane screen
rectangle(
    (50.0, 56.0),
    width=68.0,
    height=38.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w_shape, shape_r=3.5),
)

# Vertical pane divider at x=50
draw_round_segment((50.0, 37.0), (50.0, 75.0), width_units=1.8, color=DARK)

# Left pane: PASTEL_GREEN radar circle with DARK crosshairs and sweep line
rx, ry = 33.0, 56.0
r_radar = 11.0
circle(
    (rx, ry),
    radius=r_radar,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w_shape),
)
r_line = r_radar - 0.5
draw_round_segment((rx - r_line, ry), (rx + r_line, ry), width_units=2.2, color=DARK)
draw_round_segment((rx, ry - r_line), (rx, ry + r_line), width_units=2.2, color=DARK)
sweep_dx = r_line * math.cos(math.radians(45.0))
sweep_dy = r_line * math.sin(math.radians(45.0))
draw_round_segment((rx, ry), (rx + sweep_dx, ry + sweep_dy), width_units=2.2, color=DARK)
circle((rx, ry), radius=1.8, style=fill_style(DARK))

# Right pane: 3 vertical bar chart columns at x=57, 65, 73
y_base = 43.0
bars = [
    (57.0, 12.0, PASTEL_BLUE),
    (65.0, 18.0, PASTEL_BLUE),
    (73.0, 25.0, PASTEL_GREEN),
]
for bx, bh, bcol in bars:
    rectangle(
        (bx, y_base + bh / 2.0),
        width=5.0,
        height=bh,
        style=fill_style(bcol, border_color=DARK, border_units=w_shape, shape_r=1.2),
    )

save()
