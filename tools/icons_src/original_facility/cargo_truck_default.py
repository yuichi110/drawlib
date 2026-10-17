# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility concept icon: cargo_truck."""

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

# 1. Underbody chassis rail (PASTEL_BLUE_LIGHT, x=22..87, y=26..30)
rectangle(
    (54.5, 28.0),
    width=65.0,
    height=4.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_outer, shape_r=1.0),
)

# 2. Heavy cargo box (WHITE, x=12..60, y=30..76)
rectangle(
    (36.0, 53.0),
    width=48.0,
    height=46.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w_outer, shape_r=3.0),
)

# Vertical cargo panel ribs (above and below stripe)
for rx in (28.0, 44.0):
    draw_round_segment((rx, 30.5), (rx, 49.0), width_units=w_inner, color=DARK)
    draw_round_segment((rx, 58.0), (rx, 75.5), width_units=w_inner, color=DARK)

# Bold PASTEL_GREEN horizontal logistics stripe across cargo box (y=49..58)
rectangle(
    (36.0, 53.5),
    width=48.0,
    height=9.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w_outer),
)

# 3. Truck cab (PASTEL_BLUE, x=60..88, y=30..64)
cab_pts = [
    (60.0, 30.0),
    (60.0, 64.0),
    (74.5, 64.0),
    (82.0, 49.0),
    (88.0, 47.0),
    (88.0, 30.0),
]
polygon(cab_pts, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(cab_pts, width_units=w_outer, color=DARK, closed=True)

# Cab window (WHITE)
win_pts = [
    (64.0, 50.0),
    (64.0, 60.0),
    (72.8, 60.0),
    (77.8, 50.0),
]
polygon(win_pts, style=no_border_fill(WHITE))
draw_round_polyline(win_pts, width_units=w_inner, color=DARK, closed=True)

# Cab door handle & headlight
draw_round_segment((65.0, 45.0), (69.5, 45.0), width_units=w_inner, color=DARK)
rectangle(
    (86.0, 38.0),
    width=4.0,
    height=5.5,
    style=fill_style(WHITE, border_color=DARK, border_units=w_inner, shape_r=1.0),
)
# Front bumper
rectangle(
    (86.5, 29.0),
    width=5.0,
    height=4.5,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_outer, shape_r=1.2),
)

# 4. Three heavy freight wheels (dual rear axle + front cab axle)
for wx in (23.0, 41.0, 75.0):
    circle(
        (wx, 24.0),
        radius=8.0,
        style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w_outer),
    )
    circle(
        (wx, 24.0),
        radius=3.5,
        style=fill_style(WHITE, border_color=DARK, border_units=w_inner),
    )

save()
