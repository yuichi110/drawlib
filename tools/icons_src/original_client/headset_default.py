# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Client concept icon: headset."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

cx, cy = 50.0, 52.0
r_outer = 32.0
r_inner = 24.5
steps = 36

# 1. Inner headband top cushion (PASTEL_BLUE_LIGHT) tucked behind headband arch
pad_outer = [
    (cx + (r_inner + 2.0) * math.cos(math.radians(deg)), cy + (r_inner + 2.0) * math.sin(math.radians(deg)))
    for deg in range(52, 129, 4)
]
pad_inner = [
    (cx + (r_inner - 4.2) * math.cos(math.radians(deg)), cy + (r_inner - 4.2) * math.sin(math.radians(deg)))
    for deg in range(128, 51, -4)
]
pad_pts = pad_outer + pad_inner
polygon(pad_pts, style=no_border_fill(PASTEL_BLUE_LIGHT))
draw_round_polyline(pad_pts, width_units=2.0, color=DARK, closed=True)

# 2. Headband arch (PASTEL_BLUE)
outer_arc = [
    (cx + r_outer * math.cos(math.radians(180.0 * i / steps)), cy + r_outer * math.sin(math.radians(180.0 * i / steps)))
    for i in range(steps + 1)
]
inner_arc = [
    (cx + r_inner * math.cos(math.radians(180.0 * i / steps)), cy + r_inner * math.sin(math.radians(180.0 * i / steps)))
    for i in range(steps, -1, -1)
]
band_pts = outer_arc + inner_arc
polygon(band_pts, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(band_pts, width_units=w, color=DARK, closed=True)

# 3. Boom microphone arm from left earcup down-right
mic_arm_pts = [
    (19.5, 29.0),
    (21.5, 22.0),
    (28.5, 17.5),
    (49.0, 17.5),
]
draw_round_polyline(mic_arm_pts, width_units=3.2, color=DARK, corner_r=6.0)

# 4. Left and right earcup cushions (PASTEL_BLUE_LIGHT)
for cushion_x in (27.5, 72.5):
    rectangle(
        (cushion_x, 42.0),
        width=9.5,
        height=24.0,
        style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=2.2, shape_r=4.2),
    )

# 5. Left and right outer earcup shells (PASTEL_BLUE)
for cup_x in (19.5, 80.5):
    rectangle(
        (cup_x, 42.0),
        width=12.0,
        height=28.0,
        style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=5.5),
    )

# 6. Boom microphone capsule tip (PASTEL_GREEN)
rectangle(
    (52.5, 17.5),
    width=12.5,
    height=7.5,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.2, shape_r=3.7),
)

save()
