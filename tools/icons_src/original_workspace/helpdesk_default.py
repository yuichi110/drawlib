# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Workspace concept icon: helpdesk."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w_outer = 2.0
w_inner = 1.6

# 1. Support headset headband arc (PASTEL_BLUE band centered at (50.0, 52.0))
hb_cx, hb_cy = 50.0, 52.0
r_out = 33.0
r_in = 27.0
steps = 36
outer_arc = [
    (
        hb_cx + r_out * math.cos(math.radians(180.0 * i / steps)),
        hb_cy + r_out * math.sin(math.radians(180.0 * i / steps)),
    )
    for i in range(steps + 1)
]
inner_arc = [
    (
        hb_cx + r_in * math.cos(math.radians(180.0 * (steps - i) / steps)),
        hb_cy + r_in * math.sin(math.radians(180.0 * (steps - i) / steps)),
    )
    for i in range(steps + 1)
]
band_pts = outer_arc + inner_arc
polygon(band_pts, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(band_pts, width_units=w_outer, color=DARK, closed=True)

# 2. Boom microphone arm from bottom of left ear cup to mic tip
draw_round_polyline(
    [(20.0, 38.0), (20.0, 22.0), (24.0, 17.5), (38.0, 17.5)],
    width_units=w_outer,
    color=DARK,
    corner_r=5.0,
)
rectangle(
    (41.5, 17.5),
    width=10.0,
    height=6.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w_outer, shape_r=3.0),
)

# 3. Left and right ear cups (PASTEL_BLUE_LIGHT)
for x_cup in (20.0, 80.0):
    rectangle(
        (x_cup, 48.0),
        width=12.0,
        height=22.0,
        style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_outer, shape_r=5.5),
    )

# 4. Central WHITE support ticket card framed by headset
rectangle(
    (50.0, 46.5),
    width=34.0,
    height=37.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w_outer, shape_r=4.5),
)

# 5. PASTEL_GREEN checkmark circle + DARK ticket lines on card
circle(
    (50.0, 51.5),
    radius=8.5,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w_inner),
)
draw_round_polyline(
    [(46.5, 51.2), (49.2, 48.5), (54.0, 54.0)],
    width_units=w_inner,
    color=DARK,
)
draw_round_segment((40.0, 37.5), (60.0, 37.5), width_units=w_inner, color=DARK)
draw_round_segment((43.0, 32.5), (57.0, 32.5), width_units=w_inner, color=DARK)

save()
