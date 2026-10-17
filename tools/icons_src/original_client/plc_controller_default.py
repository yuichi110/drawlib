# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Client concept icon: plc_controller."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# 1. Horizontal DIN-rail mounting bar behind controller (PASTEL_BLUE_LIGHT)
rectangle(
    (50.0, 50.0),
    width=78.0,
    height=16.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w, shape_r=2.5),
)

# 2. Main industrial PLC housing (PASTEL_BLUE)
rectangle(
    (50.0, 50.0),
    width=60.0,
    height=70.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=6.0),
)

# 3. Top and bottom I/O terminal block strips (WHITE) with screw dots
for ty in (77.5, 22.5):
    rectangle(
        (50.0, ty),
        width=48.0,
        height=9.0,
        style=fill_style(WHITE, border_color=DARK, border_units=2.0, shape_r=2.0),
    )
    for tx in (32.0, 41.0, 50.0, 59.0, 68.0):
        circle((tx, ty), radius=1.8, style=fill_style(DARK))

# 4. Left-center HMI status LCD screen (WHITE)
rectangle(
    (41.5, 55.5),
    width=29.0,
    height=20.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.2, shape_r=3.0),
)
draw_round_segment((31.5, 58.5), (49.5, 58.5), width_units=1.8, color=DARK)
draw_round_segment((31.5, 52.5), (43.5, 52.5), width_units=1.8, color=DARK)

# 5. Right-side status LEDs (PASTEL_GREEN)
for ly in (62.5, 55.5, 48.5):
    circle(
        (66.5, ly),
        radius=3.2,
        style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=1.8),
    )

# 6. Lower HMI control buttons (PASTEL_BLUE_LIGHT)
for bx in (33.5, 44.5, 55.5):
    rectangle(
        (bx, 36.5),
        width=8.0,
        height=5.5,
        style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=1.8, shape_r=1.5),
    )

save()
