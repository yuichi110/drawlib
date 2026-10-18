# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: iot_hub."""

import math

from drawlib.canvas import save
from drawlib.shapes import arc, circle, polygon
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_cap,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
    stroke_style,
)

setup_icon()

w = ORIG_STROKE
cx, cy = 50.0, 50.0

satellites = [
    (22.0, 78.0),
    (78.0, 78.0),
    (22.0, 22.0),
    (78.0, 22.0),
]

# 4 diagonal spoke connections
for sx, sy in satellites:
    draw_round_segment((cx, cy), (sx, sy), width_units=w, color=DARK)

# Left and right telemetry signal arcs radiating around the hub
for r_arc, half_ang in ((26.5, 24.0), (33.5, 18.0)):
    for base_ang in (0.0, 180.0):
        a0 = base_ang - half_ang
        a1 = base_ang + half_ang
        arc(
            (cx, cy),
            width=r_arc * 2.0,
            height=r_arc * 2.0,
            angle_start=a0,
            angle_end=a1,
            style=stroke_style(DARK, width_units=2.0),
        )
        for deg in (a0, a1):
            rad = math.radians(deg)
            draw_cap((cx + r_arc * math.cos(rad), cy + r_arc * math.sin(rad)), width_units=2.0, color=DARK)

# Central pointy-top hexagonal IoT hub
hex_r = 20.0
hex_angles = [90.0, 30.0, 330.0, 270.0, 210.0, 150.0]
hex_pts = [
    (cx + hex_r * math.cos(math.radians(a)), cy + hex_r * math.sin(math.radians(a)))
    for a in hex_angles
]
polygon(hex_pts, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(hex_pts, width_units=w, color=DARK, closed=True)

# Inner core circle
circle(
    (cx, cy),
    radius=8.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0),
)

# 4 outer sensor satellite nodes
for sx, sy in satellites:
    circle(
        (sx, sy),
        radius=8.0,
        style=fill_style(WHITE, border_color=DARK, border_units=2.0),
    )
    circle(
        (sx, sy),
        radius=3.0,
        style=fill_style(PASTEL_GREEN),
    )

save()
