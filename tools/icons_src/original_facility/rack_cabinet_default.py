# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility concept icon: rack_cabinet."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    fill_style,
    setup_icon,
)

setup_icon()

w_outer = 2.0
w_inner = 1.6

# 1. Leveling feet at bottom of cabinet
for fx in (31.0, 69.0):
    rectangle(
        (fx, 13.5),
        width=7.5,
        height=4.5,
        style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_inner, shape_r=1.5),
    )

# 2. Tall 42U rack cabinet outer frame (PASTEL_BLUE)
rectangle(
    (50.0, 51.5),
    width=52.0,
    height=73.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w_outer, shape_r=5.0),
)

# 3. Top status LED bar (PASTEL_GREEN)
rectangle(
    (50.0, 81.5),
    width=30.0,
    height=5.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w_inner, shape_r=2.5),
)

# 4. Recessed inner rack bay (PASTEL_BLUE_LIGHT)
rectangle(
    (50.0, 48.0),
    width=40.0,
    height=53.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_inner, shape_r=2.0),
)

# 5. Four mounted equipment shelves between the rails
unit_ys = [67.0, 54.5, 42.0, 29.5]
for idx, uy in enumerate(unit_ys):
    u_col = WHITE if idx % 2 == 0 else PASTEL_BLUE
    rectangle(
        (50.0, uy),
        width=28.0,
        height=9.2,
        style=fill_style(u_col, border_color=DARK, border_units=w_inner, shape_r=1.5),
    )
    # Status indicator LED dot on each unit
    led_col = PASTEL_GREEN if idx < 2 else WHITE
    circle(
        (59.0, uy),
        radius=1.7,
        style=fill_style(led_col, border_color=DARK, border_units=1.3),
    )

# 6. Left and right vertical 19-inch mounting rails (WHITE)
for rx in (33.0, 67.0):
    rectangle(
        (rx, 48.0),
        width=6.0,
        height=53.0,
        style=fill_style(WHITE, border_color=DARK, border_units=w_inner, shape_r=1.0),
    )
    # U-hole mounting dots along each rail
    for hy in (70.0, 62.5, 55.0, 47.5, 40.0, 32.5, 25.0):
        circle((rx, hy), radius=0.95, style=fill_style(DARK))

save()
