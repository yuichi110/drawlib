# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: agent_memory."""

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

# 1. Top: Simple AI Agent robot head (unified with multi_agent_default.py)
rx, ry = 50.0, 65.0
rw, rh = 44.0, 28.0

draw_round_segment((rx, ry + rh / 2.0), (rx, 85.0), width_units=w, color=DARK)
circle(
    (rx, 87.5),
    radius=3.5,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=2.0),
)
rectangle(
    (rx, ry),
    width=rw,
    height=rh,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=8.0),
)
for eye_x in (rx - 9.0, rx + 9.0):
    circle(
        (eye_x, ry),
        radius=4.2,
        style=fill_style(WHITE, border_color=DARK, border_units=2.0),
    )

# 2. Bottom: RAM / Memory module (matching memory module style)
mcx, mcy = 50.0, 27.0
mw, mh = 58.0, 22.0

for px in (33.0, 44.3, 55.7, 67.0):
    draw_round_segment((px, mcy + mh / 2.0), (px, mcy + mh / 2.0 + 5.5), width_units=2.0, color=DARK)
    draw_round_segment((px, mcy - mh / 2.0 - 5.5), (px, mcy - mh / 2.0), width_units=2.0, color=DARK)

rectangle(
    (mcx, mcy),
    width=mw,
    height=mh,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w, shape_r=5.0),
)

for cell_x in (34.0, 50.0, 66.0):
    rectangle(
        (cell_x, mcy),
        width=9.5,
        height=11.0,
        style=fill_style(WHITE, border_color=DARK, border_units=2.0, shape_r=2.0),
    )

save()
