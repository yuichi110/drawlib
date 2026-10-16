# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: dataset."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
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

# 1. Back dataset table sheet
rectangle(
    (56.0, 55.0),
    width=54.0,
    height=58.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w, shape_r=6.5),
)

# 2. Front dataset table sheet with PASTEL_BLUE header
rectangle(
    (43.0, 45.0),
    width=56.0,
    height=58.0,
    style=fill_style(WHITE, shape_r=6.5),
)
draw_rounded_corner_block(
    15.0,
    60.0,
    71.0,
    74.0,
    r=6.5,
    round_tl=True,
    round_tr=True,
    color=PASTEL_BLUE,
)
rectangle(
    (43.0, 45.0),
    width=56.0,
    height=58.0,
    style=fill_style(Colors.Transparent, border_color=DARK, border_units=w, shape_r=6.5),
)
draw_round_segment((15.0, 60.0), (71.0, 60.0), width_units=w, color=DARK)

# 3. 2x3 structured data cells inside front sheet
row_ys = [50.0, 38.0, 26.0]
col_xs = [32.5, 53.5]
for r_idx, ry in enumerate(row_ys):
    for c_idx, cx in enumerate(col_xs):
        cell_col = PASTEL_GREEN if (r_idx == 0 and c_idx == 0) else PASTEL_BLUE_LIGHT
        rectangle(
            (cx, ry),
            width=16.5,
            height=7.5,
            style=fill_style(cell_col, border_color=DARK, border_units=2.1, shape_r=2.0),
        )

save()
