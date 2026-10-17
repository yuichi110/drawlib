# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Client concept icon: nfc_tag."""

import math

from drawlib.canvas import save
from drawlib.shapes import arc, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_cap,
    fill_style,
    setup_icon,
    stroke_style,
)

setup_icon()

w = ORIG_STROKE

# 1. Outer contactless NFC badge (PASTEL_BLUE)
rectangle(
    (50.0, 50.0),
    width=74.0,
    height=74.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=15.0),
)

# 2. Inner NFC card plate (WHITE)
rectangle(
    (50.0, 50.0),
    width=56.0,
    height=56.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.2, shape_r=10.0),
)

# 3. NFC tag transmitter pad on left (PASTEL_GREEN)
tx_cx, tx_cy = 32.5, 50.0
rectangle(
    (tx_cx, tx_cy),
    width=9.5,
    height=15.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.2, shape_r=3.5),
)

# 4. Three concentric contactless radio wave arcs (PASTEL_GREEN with DARK borders)
ang_start = -38.0
ang_end = 38.0

for r in (14.0, 23.0, 32.0):
    diam = r * 2.0
    # Outer DARK stroke + caps
    arc(
        (tx_cx, tx_cy),
        width=diam,
        height=diam,
        angle_start=ang_start,
        angle_end=ang_end,
        style=stroke_style(DARK, width_units=5.2),
    )
    for ang_deg in (ang_start, ang_end):
        rad = math.radians(ang_deg)
        draw_cap(
            (tx_cx + r * math.cos(rad), tx_cy + r * math.sin(rad)),
            width_units=5.2,
            color=DARK,
        )
    # Inner PASTEL_GREEN stroke + caps
    arc(
        (tx_cx, tx_cy),
        width=diam,
        height=diam,
        angle_start=ang_start,
        angle_end=ang_end,
        style=stroke_style(PASTEL_GREEN, width_units=2.2),
    )
    for ang_deg in (ang_start, ang_end):
        rad = math.radians(ang_deg)
        draw_cap(
            (tx_cx + r * math.cos(rad), tx_cy + r * math.sin(rad)),
            width_units=2.2,
            color=PASTEL_GREEN,
        )

save()
