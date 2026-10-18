# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: clickhouse."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w = 2.0

# 4 tall vertical column bars + 1 short right accent bar (centered in [13, 87] x [13, 87])
bar_w = 10.4
bar_h = 74.0
y_cy = 50.0
r_bar = 2.8

x_cols = [18.2, 34.1, 50.0, 65.9]

# 1. Draw the 4 tall column bars (alternating Colors.Amber3 and Colors.Amber2 for depth)
for i, xc in enumerate(x_cols):
    col = Colors.Amber3 if i % 2 == 0 else Colors.Amber2
    rectangle(
        (xc, y_cy),
        width=bar_w,
        height=bar_h,
        style=fill_style(col, border_color=DARK, border_units=w, shape_r=r_bar),
    )

# 2. Accent cap at the bottom of the 1st column bar (Colors.Red3)
cap_h = 15.0
y_cap_cy = 13.0 + cap_h / 2.0
rectangle(
    (x_cols[0], y_cap_cy),
    width=bar_w,
    height=cap_h,
    style=fill_style(Colors.Red3, border_color=DARK, border_units=w, shape_r=r_bar),
)
# Crisp horizontal divider line at top of bottom accent cap (y = 28.0)
draw_round_segment(
    (x_cols[0] - bar_w / 2.0, 28.0),
    (x_cols[0] + bar_w / 2.0, 28.0),
    width_units=1.8,
    color=DARK,
)

# 3. Short 5th column bar floating on the right at vertical center (Colors.Amber3)
rectangle(
    (81.8, y_cy),
    width=bar_w,
    height=20.0,
    style=fill_style(Colors.Amber3, border_color=DARK, border_units=w, shape_r=r_bar),
)

save()
