# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Client concept icon: connected_car."""

import math

from drawlib.canvas import save
from drawlib.shapes import arc, circle, polygon, rectangle
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

# 1. Connectivity signal arcs above roof (PASTEL_GREEN + DARK)
tx_cx, tx_cy = 44.0, 62.5
circle(
    (tx_cx, tx_cy),
    radius=3.5,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0),
)

ang_start = 40.0
ang_end = 140.0
for r in (11.5, 20.0):
    diam = r * 2.0
    arc(
        (tx_cx, tx_cy),
        width=diam,
        height=diam,
        angle_start=ang_start,
        angle_end=ang_end,
        style=stroke_style(DARK, width_units=5.0),
    )
    for ang_deg in (ang_start, ang_end):
        rad = math.radians(ang_deg)
        draw_cap(
            (tx_cx + r * math.cos(rad), tx_cy + r * math.sin(rad)),
            width_units=5.0,
            color=DARK,
        )
    arc(
        (tx_cx, tx_cy),
        width=diam,
        height=diam,
        angle_start=ang_start,
        angle_end=ang_end,
        style=stroke_style(PASTEL_GREEN, width_units=2.0),
    )
    for ang_deg in (ang_start, ang_end):
        rad = math.radians(ang_deg)
        draw_cap(
            (tx_cx + r * math.cos(rad), tx_cy + r * math.sin(rad)),
            width_units=2.0,
            color=PASTEL_GREEN,
        )

# 2. Modern side-view car body (PASTEL_BLUE)
car_pts = [
    (12.0, 24.0),
    (12.0, 39.0),
    (17.5, 41.5),
    (26.5, 55.5),
    (56.5, 55.5),
    (71.0, 41.5),
    (85.5, 38.5),
    (88.0, 34.0),
    (88.0, 24.0),
]
polygon(
    car_pts,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=2.5),
)

# 3. Rear window and front windshield/window (WHITE)
rear_win = [
    (28.0, 42.5),
    (30.5, 51.0),
    (43.5, 51.0),
    (43.5, 42.5),
]
polygon(rear_win, style=no_border_fill(WHITE))
draw_round_polyline(rear_win, width_units=2.0, color=DARK, closed=True)

front_win = [
    (48.0, 42.5),
    (48.0, 51.0),
    (54.8, 51.0),
    (65.5, 42.5),
]
polygon(front_win, style=no_border_fill(WHITE))
draw_round_polyline(front_win, width_units=2.0, color=DARK, closed=True)

# Door handle and front headlight
draw_round_segment((49.5, 37.5), (54.0, 37.5), width_units=1.8, color=DARK)
rectangle(
    (85.5, 34.0),
    width=4.5,
    height=4.5,
    style=fill_style(WHITE, border_color=DARK, border_units=1.8, shape_r=1.2),
)

# 4. Front and rear wheels (DARK tires + WHITE rims)
for wx in (28.0, 71.5):
    circle(
        (wx, 23.5),
        radius=8.8,
        style=fill_style(DARK),
    )
    circle(
        (wx, 23.5),
        radius=3.8,
        style=fill_style(WHITE),
    )

save()
