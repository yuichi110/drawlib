# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: audit_compliance."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Clipboard board
rectangle(
    (50.0, 46.0),
    width=60.0,
    height=64.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=7.0),
)

# Top clipboard clamp
rectangle(
    (50.0, 78.0),
    width=28.0,
    height=12.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=4.0),
)

# 2 checklist rows inside
for y in (54.0, 34.0):
    circle(
        (34.0, y),
        radius=5.5,
        style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.2),
    )
    draw_round_segment((46.0, y), (68.0, y), width_units=2.6, color=DARK)

save()
